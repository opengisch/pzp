from qgis import processing
from qgis.core import (
    QgsField,
    QgsFields,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterVectorDestination,
)
from qgis.PyQt.QtCore import QVariant


class DangerZones(QgsProcessingAlgorithm):

    INPUT = "INPUT"
    DANGER_FIELD = "DANGER_FIELD"
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
                self.INPUT, "Input layer", [QgsProcessing.TypeVectorPolygon]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.DANGER_FIELD,
                description="Campo contenente il grado di pericolo",
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.Numeric,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorDestination(self.OUTPUT, "Zone di pericolo")
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)

        if source is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )

        fields = QgsFields()
        fields.append(QgsField("Grado di pericolo", QVariant.Int))

        danger_field = self.parameterAsFields(
            parameters,
            self.DANGER_FIELD,
            context,
        )[0]

        # # Send some information to the user
        # feedback.pushInfo(f"CRS is {source.sourceCrs().authid()}")

        # if sink is None:
        #    raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        # Compute the number of steps to display within the progress bar and
        # total = 100.0 / source.featureCount() if source.featureCount() else 0

        final_layer = None

        used_grades = set()

        for feature in source.getFeatures():
            # name = feature["name"]
            used_grades.add(feature[danger_field])

        used_grades = sorted(used_grades, reverse=True)

        feedback.pushInfo(f"Used grades {used_grades}")

        for grado in used_grades:
            feedback.pushInfo(f'"{danger_field}" = {grado}')
            result = processing.run(
                "native:extractbyexpression",
                {
                    "INPUT": parameters[self.INPUT],
                    "EXPRESSION": f'"{danger_field}" = {grado}',
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
                    "FIELD": f"{danger_field}",
                    "SEPARATE_DISJOINT": True,
                    "OUTPUT": "memory:",
                },
                context=context,
                feedback=feedback,
                is_child_algorithm=True,
            )

            if grado == max(used_grades):
                final_layer = result["OUTPUT"]
            else:
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
                "DISTANCE": -0.0000001,
                "TOLERANCE": 1,
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
                "OUTPUT": parameters[self.OUTPUT],
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        return {self.OUTPUT: result["OUTPUT"]}
