from qgis import processing
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
)


class FixGeometries(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    def createInstance(self):
        return FixGeometries()

    def name(self):
        return "fix_geometries"

    def displayName(self):
        return "Correggi geometrie"

    def group(self):
        return "Algoritmi"

    def groupId(self):
        return "algorithms"

    def shortHelpString(self):
        return "Algoritmo per correggere le geometrie"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                "Layer con le geometrie",
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT, "Output layer"))

    def processAlgorithm(self, parameters, context, feedback):

        result = processing.run(
            "native:fixgeometries",
            {"INPUT": parameters[self.INPUT], "OUTPUT": "memory:"},
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        result = processing.run(
            "pzp_utils:merge_by_area",
            {
                "INPUT": result["OUTPUT"],
                "MODE": 2,
                "OUTPUT": parameters[self.OUTPUT],
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        result = processing.run(
            "native:snappointstogrid",
            {
                "INPUT": result["OUTPUT"],
                "HSPACING": 0.001,
                "VSPACING": 0.001,
                "ZSPACING": 0,
                "MSPACING": 0,
                "OUTPUT": "memory:",
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        result = processing.run(
            "native:buffer",
            {
                "INPUT": result["OUTPUT"],
                "DISTANCE": -1e-06,
                "SEGMENTS": 5,
                "END_CAP_STYLE": 0,
                "JOIN_STYLE": 0,
                "MITER_LIMIT": 2,
                "DISSOLVE": False,
                "OUTPUT": "memory:",
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        result = processing.run(
            "native:snappointstogrid",
            {
                "INPUT": result["OUTPUT"],
                "HSPACING": 0.001,
                "VSPACING": 0.001,
                "ZSPACING": 0,
                "MSPACING": 0,
                "OUTPUT": "memory:",
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        result = processing.run(
            "native:buffer",
            {
                "INPUT": result["OUTPUT"],
                "DISTANCE": 1e-06,
                "SEGMENTS": 5,
                "END_CAP_STYLE": 0,
                "JOIN_STYLE": 0,
                "MITER_LIMIT": 2,
                "DISSOLVE": False,
                "OUTPUT": "memory:",
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        result = processing.run(
            "native:snappointstogrid",
            {
                "INPUT": result["OUTPUT"],
                "HSPACING": 0.001,
                "VSPACING": 0.001,
                "ZSPACING": 0,
                "MSPACING": 0,
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

        return {self.OUTPUT: result["OUTPUT"]}
