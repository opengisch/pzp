from qgis import processing
from qgis.core import (
    QgsField,
    QgsFields,
    QgsFeature,
    QgsWkbTypes,
    QgsFeatureSink,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterCrs,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterVectorDestination,
    QgsProcessingParameterFeatureSink,
)
from qgis.PyQt.QtCore import QVariant


class MergeIntensityLayers(QgsProcessingAlgorithm):

    NUM_OF_LAYERS = 5
    LAYERS = [f"LAYER{i}" for i in range(NUM_OF_LAYERS)]
    INTENSITY_FIELDS = [f"INTENSITY_FIELD{i}" for i in range(NUM_OF_LAYERS)]
    PERIODS = [f"PERIOD{i}" for i in range(NUM_OF_LAYERS)]

    CRS = 'CRS'
    OUTPUT = "OUTPUT"

    def createInstance(self):
        return MergeIntensityLayers()

    def name(self):
        return "merge_intensity_layers"

    def displayName(self):
        return "Fondi layer intensità"

    def group(self):
        return "Algoritmi"

    def groupId(self):
        return "algorithms"

    def shortHelpString(self):
        return "Algoritmo per fondere layer con intensità separati per periodo di ritorno"

    def initAlgorithm(self, config=None):

        for i in range(self.NUM_OF_LAYERS):
            self.addParameter(
                QgsProcessingParameterVectorLayer(
                    name=self.LAYERS[i],
                    description=f"Input layer {i}",
                    types=[QgsProcessing.TypeVectorPolygon],
                    optional=True,
                )
            )

            self.addParameter(
                QgsProcessingParameterField(
                    name=self.INTENSITY_FIELDS[i],
                    description="Campo contenente le intensità",
                    parentLayerParameterName=self.LAYERS[i],
                    type=QgsProcessingParameterField.Numeric,
                    optional=True,
                )
            )

            self.addParameter(
                QgsProcessingParameterNumber(
                    name=self.PERIODS[i],
                    description="Periodo di ritorno",
                    type=QgsProcessingParameterNumber.Integer,
                    optional=True,
                )
            )

        self.addParameter(QgsProcessingParameterCrs(
            self.CRS, "CRS", defaultValue = "EPSG:2056")
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, "Intensità completo")
        )

    def processAlgorithm(self, parameters, context, feedback):

        fields = QgsFields()
        fields.append(QgsField("intensity", QVariant.Int))
        fields.append(QgsField("period", QVariant.Int))

        crs = self.parameterAsCrs(
            parameters,
            self.CRS,
            context
        )

        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            QgsWkbTypes.MultiPolygon,
            crs,
        )

        new_features = []

        for i in range(self.NUM_OF_LAYERS):
            layer = self.parameterAsSource(
                parameters,
                self.LAYERS[i],
                context
            )
            if not layer:
                continue

            intensity_field = self.parameterAsFields(
                parameters,
                self.INTENSITY_FIELDS[i],
                context,
            )[0]

            period = self.parameterAsInt(
                parameters,
                self.PERIODS[i],
                context,
            )

            for feature in layer.getFeatures():
                new_feature = QgsFeature()
                new_feature.setGeometry(feature.geometry())
                new_feature.setAttributes([feature[intensity_field], period])
                new_features.append(new_feature)

        sink.addFeatures(new_features, QgsFeatureSink.FastInsert)
        return {self.OUTPUT: dest_id}
