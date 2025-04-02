from qgis import processing
from qgis.core import (
    QgsField,
    QgsFields,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
)
from qgis.PyQt.QtCore import QVariant

from pzp.processing.merge_by_area import MergeByArea
from pzp.processing.merge_by_form_factor import MergeByFormFactor


class DangerZones(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    MATRIX_FIELD = "MATRIX_FIELD"
    PROCESS_SOURCE_FIELD = "PROCESS_SOURCE_FIELD"
    MERGE_FORM_FACTOR = "MERGE_FORM_FACTOR"
    OUTPUT = "OUTPUT"

    def createInstance(self):
        return DangerZones()

    def name(self):
        return "danger_zones"

    def displayName(self):
        return "Zone di pericolo"

    def group(self):
        return "Algoritmi"

    def groupId(self):
        return "algorithms"

    def shortHelpString(self):
        return "Algoritmo per il calcolo delle zone di pericolo"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(self.INPUT, "Input layer", [QgsProcessing.TypeVectorPolygon])
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.MATRIX_FIELD,
                description="Campo contenente il valore della matrice",
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.Numeric,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.PROCESS_SOURCE_FIELD,
                description="Campo contenente la fonte del processo",
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.String,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.MERGE_FORM_FACTOR,
                description="Fusiona le geometrie con superficie inferiore a 10m2 se rispondono al fattore di forma."
                "Ad esempio con un fattore di 0.1 le geometrie di 1x10m o più allungate verranno fusionate."
                "Un fattore di 0 o negativo viene ignorato.",
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.Numeric,
            )
        )

        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT, "Zone di pericolo"))

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)

        if source is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))

        fields = QgsFields()
        fields.append(QgsField("Grado di pericolo", QVariant.Int))

        matrix_field = self.parameterAsFields(
            parameters,
            self.MATRIX_FIELD,
            context,
        )[0]

        process_source_field = self.parameterAsFields(
            parameters,
            self.PROCESS_SOURCE_FIELD,
            context,
        )[0]

        merge_form_factor = self.parameterAsDouble(parameters, self.MERGE_FORM_FACTOR, context)

        # # Send some information to the user
        # feedback.pushInfo(f"CRS is {source.sourceCrs().authid()}")

        # if sink is None:
        #    raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        # Compute the number of steps to display within the progress bar and
        # total = 100.0 / source.featureCount() if source.featureCount() else 0

        used_matrix_values = set()
        process_sources = set()

        for feature in source.getFeatures():
            process_sources.add(feature[process_source_field])
            used_matrix_values.add(feature[matrix_field])

        used_matrix_values = sorted(used_matrix_values, reverse=False)

        # The order of the codes is not the logical order of the values, 1000 (aka 0) should
        # be at the end (after -10 too since is logically smaller i.e. -10 means "pericolo residuo", 0 is "non in pericolo"
        if 1000 in used_matrix_values:
            used_matrix_values.remove(1000)  # Remove the '1000' element
            used_matrix_values.append(1000)  # Insert '1000' at the end

        feedback.pushInfo(f"Used matrix values {used_matrix_values}")
        feedback.pushInfo(f"Process sources {process_sources}")

        result = processing.run(
            "native:dissolve",
            {
                "INPUT": parameters[self.INPUT],
                "FIELD": f"{matrix_field};{process_source_field}",
                "SEPARATE_DISJOINT": True,
                "OUTPUT": "memory:",
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )
        input_layer = result["OUTPUT"]

        final_layer = None
        for process_source in process_sources:
            result = self.prepare_process_source(
                input_layer,
                used_matrix_values,
                process_source,
                matrix_field,
                process_source_field,
                merge_form_factor,
                parameters,
                context,
                feedback,
            )

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

    def prepare_process_source(
        self,
        input_layer,
        used_matrix_values,
        process_source,
        matrix_field,
        process_source_field,
        merge_form_factor,
        parameters,
        context,
        feedback,
    ):
        # Escape ' in process_source
        process_source = process_source.replace("'", "''")

        final_layer = None
        for matrix_value in used_matrix_values:
            feedback.pushInfo(f'"{matrix_field}" = {matrix_value} AND "{process_source_field}" = \'{process_source}\'')
            result = processing.run(
                "native:extractbyexpression",
                {
                    "INPUT": input_layer,
                    "EXPRESSION": f'"{matrix_field}" = {matrix_value} AND "{process_source_field}" = \'{process_source}\'',
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

                result = processing.run(
                    "native:multiparttosingleparts",
                    {
                        "INPUT": result["OUTPUT"],
                        "OUTPUT": "memory:",
                    },
                    context=context,
                    feedback=feedback,
                    is_child_algorithm=True,
                )

                result = processing.run(
                    "native:fixgeometries",
                    {"INPUT": result["OUTPUT"], "OUTPUT": "memory:"},
                    context=context,
                    feedback=feedback,
                    is_child_algorithm=True,
                )

                result = processing.run(
                    "pzp_utils:merge_by_area",
                    {
                        "INPUT": result["OUTPUT"],
                        "MODE": MergeByArea.MODE_BOUNDARY,
                        "OUTPUT": "memory:",
                    },
                    context=context,
                    feedback=feedback,
                    is_child_algorithm=True,
                )

                result = processing.run(
                    "native:multiparttosingleparts",
                    {
                        "INPUT": result["OUTPUT"],
                        "OUTPUT": "memory:",
                    },
                    context=context,
                    feedback=feedback,
                    is_child_algorithm=True,
                )

                if merge_form_factor > 0:
                    result = processing.run(
                        "pzp_utils:merge_by_form_factor",
                        {
                            "INPUT": result["OUTPUT"],
                            "MODE": MergeByFormFactor.MODE_BOUNDARY,
                            "FORM_FACTOR": merge_form_factor,
                            "AREA_TRESHOLD": 10,
                            "OUTPUT": "memory:",
                        },
                        context=context,
                        feedback=feedback,
                        is_child_algorithm=True,
                    )

                    result = processing.run(
                        "native:multiparttosingleparts",
                        {
                            "INPUT": result["OUTPUT"],
                            "OUTPUT": "memory:",
                        },
                        context=context,
                        feedback=feedback,
                        is_child_algorithm=True,
                    )

                # Workaround to re-remove small invalid parts that comes back after multi to single
                result = processing.run(
                    "pzp_utils:remove_by_area",
                    {
                        "INPUT": result["OUTPUT"],
                        "OUTPUT": "memory:",
                    },
                    context=context,
                    feedback=feedback,
                    is_child_algorithm=True,
                )

            final_layer = result["OUTPUT"]

        result = processing.run(
            "native:multiparttosingleparts",
            {
                "INPUT": final_layer,
                "OUTPUT": "memory:",
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        result = processing.run(
            "native:deletecolumn",
            {
                "INPUT": result["OUTPUT"],
                "COLUMN": ["fid", "layer", "path"],
                "OUTPUT": parameters[self.OUTPUT],
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        return result
