from qgis import processing
from qgis.core import (
    QgsField,
    QgsFields,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterFeatureSink,
    QgsApplication,
)
from qgis.PyQt.QtCore import QVariant


class RemoveOverlappings(QgsProcessingAlgorithm):

    INPUT = "INPUT"
    INTENSITY_FIELD = "INTENSITY_FIELD"
    PERIOD_FIELD = "PERIOD_FIELD"
    SOURCE_FIELD = "SOURCE_FIELD"
    OUTPUT = "OUTPUT"

    def createInstance(self):
        return RemoveOverlappings()

    def name(self):
        return "remove_overlappings"

    def displayName(self):
        return "Rimuovi sovrapposizioni"

    def group(self):
        return "Algoritmi"

    def groupId(self):
        return "algorithms"

    def shortHelpString(self):
        return "Algoritmo per la rimozione di sovrapposizioni nei layer intensità"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT, "Input layer", [QgsProcessing.TypeVectorPolygon]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.INTENSITY_FIELD,
                description="Campo contenente l'intensità",
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.Numeric,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.PERIOD_FIELD,
                description="Campo contenente il periodo di ritorno",
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.Numeric,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.SOURCE_FIELD,
                description="Campo contenente la fonte del processo",
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.String,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, "Senza sovrapposizioni")
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)

        if source is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )

        intensity_field = self.parameterAsFields(
            parameters,
            self.INTENSITY_FIELD,
            context,
        )[0]

        period_field = self.parameterAsFields(
            parameters,
            self.PERIOD_FIELD,
            context,
        )[0]

        source_field = self.parameterAsFields(
            parameters,
            self.SOURCE_FIELD,
            context,
        )[0]

        intensities = set()
        periods = set()
        sources = set()

        for feature in source.getFeatures():
            intensities.add(feature[intensity_field])
            periods.add(feature[period_field])
            sources.add(feature[source_field])

        intensities = sorted(intensities, reverse=True)
        periods = sorted(periods, reverse=True)

        final_layer = None
        for source in sources:
            for period in periods:
                result = self.prepare_period(
                    intensities,
                    intensity_field,
                    period,
                    period_field,
                    source,
                    source_field,
                    parameters,
                    context,
                    feedback)
                if final_layer:
                    result = processing.run(
                        "native:mergevectorlayers",
                        {
                            "LAYERS": [result["OUTPUT"], final_layer],
                            "OUTPUT": "memory:",
                        },
                        context=context,
                        feedback=feedback,
                        is_child_algorithm=True,
                    )
                final_layer = result["OUTPUT"]

        return {self.OUTPUT: final_layer}

    def prepare_period(self, intensities, intensity_field, period, period_field, source, source_field, parameters, context, feedback):

        final_layer = None
        for intensity in intensities:
            result = processing.run(
                "native:extractbyexpression",
                {
                    "INPUT": parameters[self.INPUT],
                    "EXPRESSION": f'"{intensity_field}" = {intensity} AND "{period_field}" = \'{period}\' AND "{source_field}" = \'{source}\'',
                    "OUTPUT": "memory:",
                },
                context=context,
                feedback=feedback,
                is_child_algorithm=True,
            )
            result = processing.run(
                "native:dissolve",
                {
                    "INPUT": result["OUTPUT"],
                    "FIELD": f"{intensity_field}",
                    "SEPARATE_DISJOINT": True,
                    "OUTPUT": "memory:",
                },
                context=context,
                feedback=feedback,
                is_child_algorithm=True,
            )

            if final_layer:
                result = processing.run(
                    "native:difference",
                    {
                        "INPUT": result["OUTPUT"],
                        "OVERLAY": final_layer,
                        "OUTPUT": "memory:",
                    },
                    context=context,
                    feedback=feedback,
                    is_child_algorithm=True,
                )

                result = processing.run(
                    "native:mergevectorlayers",
                    {
                        "LAYERS": [result["OUTPUT"], final_layer],
                        "OUTPUT": "memory:",
                    },
                    context=context,
                    feedback=feedback,
                    is_child_algorithm=True,
                )

            final_layer = result["OUTPUT"]

        # Apply very small negative buffer to remove artifacts
        result = processing.run(
            "native:buffer",
            {
                "INPUT": final_layer,
                "DISTANCE": -0.0000001,
                "OUTPUT": "memory:",
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )
        # Snap to layer
        result = processing.run(
            "native:snapgeometries",
            {
                "INPUT": result["OUTPUT"],
                "REFERENCE_LAYER": result["OUTPUT"],
                "TOLERANCE": 0.1,
                "BEHAVIOR": 0,
                "OUTPUT": "memory:",
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )
        # Snap to grid
        result = processing.run(
            "native:snappointstogrid",
            {
                "INPUT": result["OUTPUT"],
                "HSPACING": 0.001,
                "MSPACING": 0,
                "VSPACING": 0.001,
                "ZSPACING": 0,
                "OUTPUT": "memory:",
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        result = processing.run(
            "native:multiparttosingleparts",
            {
                'INPUT': result["OUTPUT"],
                "OUTPUT": "memory:",
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        # qgis:deletecolumn has been renamed native:deletecolumn after qgis 3.16
        deletecolumn_id = "qgis:deletecolumn"
        if "qgis:deletecolumn" not in [x.id() for x in QgsApplication.processingRegistry().algorithms()]:
            deletecolumn_id = "native:deletecolumn"

        result = processing.run(
            deletecolumn_id,
            {'INPUT': result["OUTPUT"],
             'COLUMN':['fid', 'layer', 'path'],
             "OUTPUT": parameters[self.OUTPUT],
             },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        return result
