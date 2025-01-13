from collections import OrderedDict

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
    QgsProcessingParameterEnum,
)
from qgis.PyQt.QtCore import QVariant

from . import domains

class ApplyMatrix(QgsProcessingAlgorithm):

    INPUT = "INPUT"
    PERIOD_FIELD = "PERIOD_FIELD"
    INTENSITY_FIELD = "INTENSITY_FIELD"
    MATRIX = "MATRIX"
    PREDEFINED_MATRIX = "PREDEFINED_MATRIX"
    OUTPUT = "OUTPUT"

    PREDEFINED_MATRIX_CHOICES = list(
        domains.PROCESS_TYPES.values()
    )
    PREDEFINED_MATRIX_CHOICES.insert(0, "Inserimento manuale")

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
            QgsProcessingParameterEnum(
                self.PREDEFINED_MATRIX,
                "Matrice predefinita",
                self.PREDEFINED_MATRIX_CHOICES,
                defaultValue = 0,
        ))

        self.addParameter(
            QgsProcessingParameterMatrix(
                self.MATRIX,
                "Matrice manuale",
                headers=["Intensità", "Periodo ritorno max", "Valore matrice", "Valore pericolo"],
                defaultValue=[
                    1002,
                    30,
                    3,
                    1003,
                    1002,
                    100,
                    2,
                    1002,
                    1002,
                    300,
                    1,
                    1002,
                    1002,
                    99999,
                    -10,
                    1001,
                    1003,
                    30,
                    6,
                    1003,
                    1003,
                    100,
                    5,
                    1003,
                    1003,
                    300,
                    4,
                    1003,
                    1003,
                    99999,
                    -10,
                    1001,
                    1004,
                    30,
                    9,
                    1004,
                    1004,
                    100,
                    8,
                    1004,
                    1004,
                    300,
                    7,
                    1004,
                    1004,
                    99999,
                    -10,
                    1001,
                    1000,
                    99999,
                    -10,
                    1000,
                ],
            )
        )


        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, "Matrice applicata")
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)

        if source is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )

        fields = source.fields()
        fields.append(QgsField("grado_pericolo", QVariant.Int))
        fields.append(QgsField("matrice", QVariant.Int))

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

        predefined_matrix_idx = self.parameterAsInt(
            parameters,
            self.PREDEFINED_MATRIX,
            context,
        )

        # Manual matrix
        matrix = self.parameterAsMatrix(
            parameters,
            self.MATRIX,
            context,
        )

        # Predefined matrix
        if not predefined_matrix_idx == 0:
            predefined_matrix_idx -= 1  # first element is "Inserimento manuale"
            process_type = list(domains.PROCESS_TYPES.keys())[predefined_matrix_idx]
            matrix = domains.MATRICES[process_type]

        processed_matrix = self.process_matrix_param(matrix)
        feedback.pushInfo(f"Processed matrix is {processed_matrix}")

        new_features = []

        for feature in source.getFeatures():
            intensity = feature.attribute(intensity_field)
            period = feature.attribute(period_field)

            attributes = feature.attributes()

            matrice, grado_pericolo = self.get_matrix_value(processed_matrix, intensity, period)
            # grado_pericolo
            attributes.append(grado_pericolo)

            # matrice
            attributes.append(matrice)

            feature.setAttributes(attributes)

            new_features.append(feature)

        sink.addFeatures(new_features, QgsFeatureSink.FastInsert)
        return {self.OUTPUT: dest_id}

    def process_matrix_param(self, matrix):
        """Return dict of dicts e.g. { intensity = { return_years = (matrix_value, danger), return_years = (matrix_value, danger}}"""

        # Convert elements to int
        for i in range(len(matrix)):
            matrix[i] = int(matrix[i])

        result = {}
        for i in range(0, len(matrix), 4):
            inner_dict = result.get(matrix[i], None)

            if inner_dict:
                result[matrix[i]][matrix[i + 1]] = (matrix[i + 2], matrix[i + 3])
            else:
                result[matrix[i]] = {matrix[i + 1]: (matrix[i + 2], matrix[i + 3])}

        return result

    def get_matrix_value(self, processed_matrix, intensity, return_years):

        inner_dict = processed_matrix[intensity]

        # Smallest key in matrix greater than or equal to return years
        min_key = min(i for i in inner_dict.keys() if i >= return_years)

        return inner_dict[min_key]
