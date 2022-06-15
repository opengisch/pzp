from qgis import processing
from qgis.core import (
    QgsFeature,
    QgsFeatureSink,
    QgsField,
    QgsFields,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
)
from qgis.PyQt.QtCore import QVariant


class DangerZones(QgsProcessingAlgorithm):

    INPUT = "INPUT"
    PROCESS_FIELD = "PROCESS_FIELD"
    PROBABILITY_FIELD = "PROBABILITY_FIELD"
    INTENSITY_FIELD = "INTENSITY_FIELD"
    PROCESS_TYPE = "PROCESS_TYPE"
    OUTPUT = "OUTPUT"
    PROCESS_TYPES = [
        ("Alluvionamento corso d'acqua minore", 1110),
        ("Alluvionamento corso d'acqua principale", 1120),
        ("Flusso detrito", 1200),
        ("Ruscellamento superficiale", 1400),
        ("Scivolamento spontaneo", 2001),
        ("Colata detritica di versante", 2002),
        ("Caduta sassi o blocchi", 3000),
        ("Valanga radente", 4100),
        ("Valanga polverosa", 4200),
    ]

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
            QgsProcessingParameterFeatureSource(
                self.INPUT, "Input layer", [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.PROCESS_FIELD,
                description="Campo contenente il processo",
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.Numeric,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.PROBABILITY_FIELD,
                description="Campo contenente la probabilità",
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.Numeric,
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
            QgsProcessingParameterEnum(
                name=self.PROCESS_TYPE,
                description="Tipo di processo",
                options=[x[0] for x in self.PROCESS_TYPES],
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, "Output layer")
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)

        if source is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )

        fields = QgsFields()
        fields.append(QgsField("pericolo", QVariant.String))

        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            source.wkbType(),
            source.sourceCrs(),
        )

        process_field = self.parameterAsFields(
            parameters,
            self.PROCESS_FIELD,
            context,
        )[0]

        intensity_field = self.parameterAsFields(
            parameters,
            self.INTENSITY_FIELD,
            context,
        )[0]

        probability_field = self.parameterAsFields(
            parameters,
            self.PROBABILITY_FIELD,
            context,
        )[0]

        process_type = self.parameterAsEnum(
            parameters,
            self.PROCESS_TYPE,
            context,
        )

        # Send some information to the user
        feedback.pushInfo("CRS is {}".format(source.sourceCrs().authid()))

        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        # Compute the number of steps to display within the progress bar and
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        # TODO: The union should happen only on features with the correct process type
        # by selecting the correct ones and then run the algo only on them
        union = processing.run(
            "native:union",
            {
                "INPUT": self.parameterAsString(parameters, self.INPUT, context),
                "OVERLAY": None,
                "OVERLAY_FIELDS_PREFIX": "",
                "OUTPUT": "TEMPORARY_OUTPUT",
            },
            context=context,
            feedback=feedback,
        )["OUTPUT"]

        new_features = []

        for current, feature in enumerate(union.getFeatures()):
            if feedback.isCanceled():
                break

            intensity = feature.attribute(intensity_field)
            probability = feature.attribute(probability_field)
            process = feature.attribute(process_field)

            # Check if feature is for the right processo otherwise continue
            if not process == self.PROCESS_TYPES[process_type][1]:
                continue

            for i, new_feature in enumerate(new_features):
                if feature.geometry().equals(new_feature.geometry()):
                    danger = self._get_danger(process, intensity, probability)
                    if danger > new_feature.attribute(0):
                        new_feature = QgsFeature()
                        new_feature.setGeometry(feature.geometry())
                        new_feature.setAttributes([danger])
                        new_features.append(new_feature)
                        new_features[i] = new_feature
                    break
            else:
                new_feature = QgsFeature()
                new_feature.setGeometry(feature.geometry())
                new_feature.setAttributes(
                    [self._get_danger(process, intensity, probability)]
                )
                new_features.append(new_feature)

            feedback.setProgress(int(current * total))

        sink.addFeatures(new_features, QgsFeatureSink.FastInsert)
        return {self.OUTPUT: dest_id}

    def _get_danger(self, process, intensity, probability):

        # TODO: validate data based on the process type
        matrix = {  # {probability: {intensity: danger}}
            1000: {
                1002: -10,
                1003: -10,
                1004: -10,
            },
            1001: {
                1002: 1,
                1003: 4,
                1004: 7,
            },
            1002: {
                1002: 2,
                1003: 5,
                1004: 8,
            },
            1003: {
                1002: 3,
                1003: 6,
                1004: 9,
            },
        }

        return matrix[probability][intensity]
