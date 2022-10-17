from qgis.core import (
    QgsFeature,
    QgsFeatureSink,
    QgsField,
    QgsFields,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterMatrix,
)
from qgis.PyQt.QtCore import QVariant


class ApplyMatrix(QgsProcessingAlgorithm):

    INPUT = "INPUT"
    PERIOD_FIELD = "PERIOD_FIELD"
    INTENSITY_FIELD = "INTENSITY_FIELD"
    MATRIX = "MATRIX_LAYER"
    OUTPUT = "OUTPUT"

    def createInstance(self):
        return ApplyMatrix()

    def name(self):
        return "apply_matrix"

    def displayName(self):
        return "Applica matrice"

    def group(self):
        return "Algoritmi"

    def groupId(self):
        return "algorithms"

    def shortHelpString(self):
        return "Algoritmo per applicare il valore della matrice alle zone"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                "Layer con le geometrie (intensità)",
                [QgsProcessing.TypeVectorPolygon],
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
                name=self.INTENSITY_FIELD,
                description="Campo contenente l'intensità",
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.Numeric,
            )
        )

        self.addParameter(
            QgsProcessingParameterMatrix(
                self.MATRIX,
                "Matrice da applicare",
                headers=["Intensità", "Periodo ritorno max", "Valore"],
                defaultValue=[
                    1002,
                    30,
                    2,
                    1002,
                    100,
                    1,
                    1002,
                    300,
                    1,
                    1002,
                    99999,
                    0,
                    1003,
                    30,
                    2,
                    1003,
                    100,
                    2,
                    1003,
                    300,
                    2,
                    1003,
                    99999,
                    0,
                    1004,
                    30,
                    3,
                    1004,
                    100,
                    3,
                    1004,
                    300,
                    3,
                    1004,
                    99999,
                    0,
                    1000,
                    99999,
                    0,
                ],
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
        fields.append(QgsField("Grado di pericolo", QVariant.Int))

        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            source.wkbType(),
            source.sourceCrs(),
        )

        # Send some information to the user
        feedback.pushInfo(f"CRS is {source.sourceCrs().authid()}")

        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

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

        matrix = self.parameterAsMatrix(
            parameters,
            self.MATRIX,
            context,
        )

        processed_matrix = self.process_matrix_param(matrix)
        feedback.pushInfo(f"Processed matrix is {processed_matrix}")

        new_features = []

        for feature in source.getFeatures():
            intensity = feature.attribute(intensity_field)
            period = feature.attribute(period_field)

            new_feature = QgsFeature()
            new_feature.setGeometry(feature.geometry())
            new_feature.setAttributes(
                [
                    self.get_matrix_value(processed_matrix, intensity, period),
                ]
            )

            new_features.append(new_feature)

        sink.addFeatures(new_features, QgsFeatureSink.FastInsert)
        return {self.OUTPUT: dest_id}

    def process_matrix_param(self, matrix):
        """Return dict of dicts e.g. { intensity = { return_years = value, return_years = value}}"""

        result = {}
        for i in range(0, len(matrix), 3):
            inner_dict = result.get(matrix[i], None)

            if inner_dict:
                result[matrix[i]][matrix[i + 1]] = matrix[i + 2]
            else:
                result[matrix[i]] = {matrix[i + 1]: matrix[i + 2]}

        return result

    def get_matrix_value(self, processed_matrix, intensity, return_years):

        inner_dict = processed_matrix[intensity]

        # Smallest key in matrix greater than or equal to return years
        min_key = min(i for i in inner_dict.keys() if i >= return_years)

        return inner_dict[min_key]
