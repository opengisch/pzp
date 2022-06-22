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

from pzp import domains


class DangerZones(QgsProcessingAlgorithm):

    INPUT = "INPUT"
    PROCESS_FIELD = "PROCESS_FIELD"
    PROBABILITY_FIELD = "PROBABILITY_FIELD"
    INTENSITY_FIELD = "INTENSITY_FIELD"
    PROCESS_TYPE = "PROCESS_TYPE"
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
                options=domains.PROCESS_TYPES.values(),
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, "Gradi di pericolo")
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)

        if source is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )

        fields = QgsFields()
        fields.append(QgsField("Processo", QVariant.Int))
        fields.append(
            QgsField("Grado di pericolo", QVariant.Int)
        )  # Result of the matrix (DANGER_LEVEL)
        fields.append(
            QgsField("Tipo di pericolo", QVariant.Int)
        )  # What is showed on the map (DANGER_TYPE)

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

        process_type_idx = self.parameterAsEnum(
            parameters,
            self.PROCESS_TYPE,
            context,
        )

        process_type_id, process_type = list(domains.PROCESS_TYPES.items())[
            process_type_idx
        ]

        # Send some information to the user
        feedback.pushInfo(f"CRS is {source.sourceCrs().authid()}")
        feedback.pushInfo(f"Process type is {process_type} ({process_type_id})")

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

            # Check if feature is for the right process otherwise continue
            if not process == process_type_id:
                continue

            # Compare with the already added features
            for i, new_feature in enumerate(new_features):
                if feature.geometry().equals(new_feature.geometry()):
                    danger_level, danger_type = self._get_danger(
                        process, intensity, probability
                    )
                    if danger_level < new_feature.attribute(1):
                        new_feature = QgsFeature()
                        new_feature.setGeometry(feature.geometry())
                        new_feature.setAttributes([process, danger_level, danger_type])
                        new_features[i] = new_feature
                    break
            else:
                new_feature = QgsFeature()
                new_feature.setGeometry(feature.geometry())
                danger_level, danger_type = self._get_danger(
                    process, intensity, probability
                )
                new_feature.setAttributes([process, danger_level, danger_type])
                new_features.append(new_feature)

            feedback.setProgress(int(current * total))

        sink.addFeatures(new_features, QgsFeatureSink.FastInsert)
        return {self.OUTPUT: dest_id}

    def _get_danger(self, process, intensity, probability):
        """Return danger level and danger type"""

        prefer_lower = True

        # TODO: validate data based on the process type

        if process in [1110, 1120]:
            matrix = {  # {probability: {intensity: (danger_level, danger_type)}}
                1000: {
                    1002: (1010, 1001),
                    1003: (1010, 1001),
                    1004: (1010, 1001),
                },
                1001: {
                    1002: (1009, 1002),
                    1003: (1006, 1003),
                    1004: (1003, 1004),
                },
                1002: {
                    1002: (1008, 1002),
                    1003: (1005, 1003),
                    1004: (1002, 1004),
                },
                1003: {
                    1002: (1007, 1003),
                    1003: (1004, 1003),
                    1004: (1001, 1004),
                },
            }
            danger = matrix[probability][intensity]
        elif process in [1200]:
            matrix = {  # {probability: {intensity: (danger_level, danger_type)}}
                1000: {
                    1002: (1010, 1001),
                    1003: (1010, 1001),
                    1004: (1010, 1001),
                },
                1001: {
                    1002: (1009, 1002),
                    1003: (1006, 1002),
                    1004: (1003, 1004),
                },
                1002: {
                    1002: (1008, 1002),
                    1003: (1005, 1003),
                    1004: (1002, 1004),
                },
                1003: {
                    1002: (1007, 1003),
                    1003: (1004, 1003),
                    1004: (1001, 1004),
                },
            }
            if not prefer_lower:
                matrix[1001][1003] = (1006, 1003)
            danger = matrix[probability][intensity]
        else:
            danger = None
        return danger
