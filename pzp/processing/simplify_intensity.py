import os
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsFeatureSink,
    QgsFeatureRequest,
    QgsProcessingAlgorithm,
    QgsProcessingParameterCrs,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingFeatureSourceDefinition,
)

from qgis import processing


class SimplifyIntensity(QgsProcessingAlgorithm):
    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'
    MIN_AREA_TO_KEEP = 'MIN_AREA_TO_KEEP'
    DELETE_HOLES_AREA = 'DELETE_HOLES_AREA'
    INTENSITY_FIELD = 'INTENSITY_FIELD'
    CHAIKEN_THRESHOLD = 'CHAIKEN_THRESHOLD'
    REDUCE_THRESHOLD = 'REDUCE_THRESHOLD'
    CRS = 'CRS'

    def __init__(self):
        super().__init__()

    def name(self):
        return "simplifyintensity"

    def displayName(self):
        return "Semplifica Intensità"

    def group(self):
        return "Algoritmi"

    def groupId(self):
        return "algorithms"

    def shortHelpString(self):
        return "Algoritmo per la semplificazione delle mappe con le intensità"

    def createInstance(self):
        return type(self)()

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.INPUT, "Input intensity layer"))

        self.addParameter(
            QgsProcessingParameterField(
                name=self.INTENSITY_FIELD,
                description="Campo contenente l'intensità",
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.Numeric,
            )
        )

        self.addParameter(QgsProcessingParameterNumber(
            name=self.MIN_AREA_TO_KEEP,
            description="Area minima dei poligoni in m2. Poligoni più piccoli non vengono considerati",
            defaultValue = 200))

        self.addParameter(QgsProcessingParameterNumber(
            name=self.DELETE_HOLES_AREA,
            description="Area minima in m2 che un buco deve avere per esistere come buco. Buchi più piccoli vengono eliminati",
            defaultValue = 500))

        self.addParameter(QgsProcessingParameterNumber(
            self.CHAIKEN_THRESHOLD, "Chaiken threshold", defaultValue = 5))

        self.addParameter(QgsProcessingParameterNumber(
            self.REDUCE_THRESHOLD, "Reduce threshold", defaultValue = 20))

        self.addParameter(QgsProcessingParameterCrs(
            self.CRS, "CRS", defaultValue = "EPSG:2056"))

        self.addParameter(QgsProcessingParameterFeatureSink(
            self.OUTPUT, "Output layer"))

    def processAlgorithm(self, parameters, context, feedback):

        intensity_field = self.parameterAsFields(parameters, self.INTENSITY_FIELD, context)[0]
        min_area_to_keep = self.parameterAsInt(parameters, self.MIN_AREA_TO_KEEP, context)
        delete_holes_area = self.parameterAsInt(parameters, self.DELETE_HOLES_AREA, context)
        chaiken_threshold = self.parameterAsInt(parameters, self.CHAIKEN_THRESHOLD, context)
        reduce_threshold = self.parameterAsInt(parameters, self.REDUCE_THRESHOLD, context)
        crs = self.parameterAsCrs(parameters, self.CRS, context)

        result = processing.run(
            "native:assignprojection",
            {
                'INPUT': parameters[self.INPUT],
                'CRS': crs,
                'OUTPUT': 'memory:',
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        result = processing.run(
            "native:dissolve",
            {
                'INPUT': result['OUTPUT'],
                'FIELD': intensity_field,
                'SEPARATE_DISJOINT': True,
                'OUTPUT': 'memory:',
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        result = processing.run(
            "native:extractbyexpression",
            {
                'INPUT': result['OUTPUT'],
                'EXPRESSION': f'$area >= {min_area_to_keep}',
                'OUTPUT': 'memory:',
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        result = processing.run(
            "native:deleteholes",
            {
                'INPUT': result['OUTPUT'],
                'MIN_AREA': delete_holes_area,
                'OUTPUT': 'memory:',
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        result = processing.run(
            "grass7:v.generalize",
            {
                'input': result['OUTPUT'],
                'type': [0,1,2],
                'cats': '',
                'where': '',
                'method': 8,  # Chaiken
                'threshold': chaiken_threshold,
                'look_ahead': 7,
                'reduction': 1,
                'slide': 0.5,
                'angle_thresh': 3,
                'degree_thresh': 0,
                'closeness_thresh': 0,
                'betweeness_thresh': 0,
                'alpha': 1,
                'beta': 1,
                'iterations': 1,
                '-t': False,
                '-l': False,
                'GRASS_REGION_PARAMETER': None,
                'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
                'GRASS_MIN_AREA_PARAMETER': 0.0001,
                'GRASS_OUTPUT_TYPE_PARAMETER': 0,
                'GRASS_VECTOR_DSCO': '',
                'GRASS_VECTOR_LCO': '',
                'GRASS_VECTOR_EXPORT_NOCAT': False,

                'error': 'memory:',
                'output': 'TEMPORARY_OUTPUT',
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )
        result['OUTPUT'] = result['output']

        result = processing.run(
            "grass7:v.generalize",
            {
                'input': result['OUTPUT'],
                'type': [0,1,2],
                'cats': '',
                'where': '',
                'method': 3,  # Reduce
                'threshold': reduce_threshold,
                'look_ahead': 7,
                'reduction': 1,
                'slide': 0.5,
                'angle_thresh': 3,
                'degree_thresh': 0,
                'closeness_thresh': 0,
                'betweeness_thresh': 0,
                'alpha': 1,
                'beta': 1,
                'iterations': 1,
                '-t': False,
                '-l': False,
                'GRASS_REGION_PARAMETER': None,
                'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
                'GRASS_MIN_AREA_PARAMETER': 0.0001,
                'GRASS_OUTPUT_TYPE_PARAMETER': 0,
                'GRASS_VECTOR_DSCO': '',
                'GRASS_VECTOR_LCO': '',
                'GRASS_VECTOR_EXPORT_NOCAT': False,

                'error': 'memory:',
                'output': 'TEMPORARY_OUTPUT',
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )
        result['OUTPUT'] = result['output']

        result = processing.run(
            "native:fixgeometries",
            {
                'INPUT': result['OUTPUT'],
                'OUTPUT': 'TEMPORARY_OUTPUT'
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        result = processing.run(
            "native:dissolve",
            {

                'INPUT': result['OUTPUT'],
                'FIELD': intensity_field,
                'SEPARATE_DISJOINT': True,
                'OUTPUT': 'memory:',
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        result = processing.run(
            "native:extractbyexpression",
            {
                'INPUT': result['OUTPUT'],
                'EXPRESSION': f'$area >= {min_area_to_keep}',
                'OUTPUT': 'memory:',
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        result = processing.run(
            "native:deleteholes",
            {
                'INPUT': result['OUTPUT'],
                'MIN_AREA': delete_holes_area,
                'OUTPUT': parameters[self.OUTPUT],
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        return {self.OUTPUT: result['OUTPUT']}
