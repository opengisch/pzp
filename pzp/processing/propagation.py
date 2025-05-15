from qgis import processing
from qgis.core import (
    Qgis,
    QgsFeature,
    QgsField,
    QgsGeometry,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
)
from qgis.PyQt.QtCore import QVariant

from . import domains


class Propagation(QgsProcessingAlgorithm):
    BREAKING_LAYER = "BREAKING_LAYER"
    BREAKING_FIELD = "BREAKING_FIELD"
    SOURCE_FIELD = "SOURCE_FIELD"
    PROPAGATION_LAYER = "PROPAGATION_LAYER"
    PROPAGATION_FIELD = "PROPAGATION_FIELD"
    BREAKING_FIELD_PROP = "BREAKING_FIELD_PROP"
    SOURCE_FIELD_PROP = "SOURCE_FIELD_PROP"
    OUTPUT = "OUTPUT"

    def createInstance(self):
        return Propagation()

    def name(self):
        return "propagation"

    def displayName(self):
        return "Propagazione"

    def group(self):
        return "Algoritmi"

    def groupId(self):
        return "algorithms"

    def shortHelpString(self):
        return "Algoritmo per calcolare le probabilità di accadimento in base alle linee di propagazione"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.BREAKING_LAYER,
                "Layer con le probabilità di rottura",
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.BREAKING_FIELD,
                description="Campo contenente la probabilità di rottura",
                parentLayerParameterName=self.BREAKING_LAYER,
                type=QgsProcessingParameterField.Numeric,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.SOURCE_FIELD,
                description="Campo contenente la fonte del processo",
                parentLayerParameterName=self.BREAKING_LAYER,
                type=QgsProcessingParameterField.String,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.PROPAGATION_LAYER,
                "Layer con le linee di propagazione",
                [QgsProcessing.TypeVectorLine],
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.PROPAGATION_FIELD,
                description="Campo contenente la probabilità di propagazione",
                parentLayerParameterName=self.PROPAGATION_LAYER,
                type=QgsProcessingParameterField.Numeric,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.BREAKING_FIELD_PROP,
                description="Campo contenente la probabilità di rottura",
                parentLayerParameterName=self.PROPAGATION_LAYER,
                type=QgsProcessingParameterField.Numeric,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.SOURCE_FIELD_PROP,
                description="Campo contenente la fonte del processo",
                parentLayerParameterName=self.PROPAGATION_LAYER,
                type=QgsProcessingParameterField.String,
            )
        )

        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT, "Output layer"))

    def processAlgorithm(self, parameters, context, feedback):
        breaking_layer = self.parameterAsVectorLayer(parameters, self.BREAKING_LAYER, context)
        breaking_field = self.parameterAsFields(
            parameters,
            self.BREAKING_FIELD,
            context,
        )[0]
        source_field = self.parameterAsFields(
            parameters,
            self.SOURCE_FIELD,
            context,
        )[0]

        propagation_layer = self.parameterAsVectorLayer(parameters, self.PROPAGATION_LAYER, context)
        propagation_field = self.parameterAsFields(
            parameters,
            self.PROPAGATION_FIELD,
            context,
        )[0]
        breaking_field_prop = self.parameterAsFields(
            parameters,
            self.BREAKING_FIELD_PROP,
            context,
        )[0]
        source_field_prop = self.parameterAsFields(
            parameters,
            self.SOURCE_FIELD_PROP,
            context,
        )[0]

        breaking_field_idx = -1
        one_feature = next(breaking_layer.getFeatures()) if breaking_layer.featureCount() > 0 else None
        if one_feature:
            breaking_field_idx = one_feature.fieldNameIndex(breaking_field)

        propagation_field_idx = -1
        one_feature = next(propagation_layer.getFeatures()) if propagation_layer.featureCount() > 0 else None
        if one_feature:
            propagation_field_idx = one_feature.fieldNameIndex(propagation_field)

        # Output layer a.k.a. intensity layer
        fields = breaking_layer.fields()
        fields.append(QgsField("periodo_ritorno", QVariant.Int))
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            breaking_layer.wkbType(),
            breaking_layer.sourceCrs(),
        )

        used_breaking_values = set()
        used_source_values = set()
        for feature in breaking_layer.getFeatures():
            used_breaking_values.add(feature[breaking_field])
            used_source_values.add(feature[source_field])

        used_breaking_values = sorted(used_breaking_values, reverse=True)

        feedback.pushInfo(f"Used breaking values {used_breaking_values}")
        feedback.pushInfo(f"Used source values {used_source_values}")

        for source_value in used_source_values:
            for breaking_value in used_breaking_values:
                subset_breaking = processing.run(
                    "native:extractbyexpression",
                    {
                        "INPUT": parameters[self.BREAKING_LAYER],
                        "EXPRESSION": f'"{breaking_field}" = {breaking_value} AND "{source_field}" = \'{source_value}\'',
                        "OUTPUT": "memory:",
                    },
                    context=context,
                    feedback=feedback,
                    # is_child_algorithm=True,
                )

                subset_propagation = processing.run(
                    "native:extractbyexpression",
                    {
                        "INPUT": parameters[self.PROPAGATION_LAYER],
                        "EXPRESSION": f'"{breaking_field_prop}" = {breaking_value} AND "{source_field_prop}" = \'{source_value}\'',
                        "OUTPUT": "memory:",
                    },
                    context=context,
                    feedback=feedback,
                    # is_child_algorithm=True,
                )

                result = processing.run(
                    "native:splitwithlines",
                    {
                        "INPUT": subset_breaking["OUTPUT"],
                        "LINES": subset_propagation["OUTPUT"],
                        "OUTPUT": "memory:",
                    },
                    context=context,
                    feedback=feedback,
                    # is_child_algorithm=True,
                )

                lines = list(subset_propagation["OUTPUT"].getFeatures())
                lines = sorted(lines, key=lambda line: -line[propagation_field])
                features_to_add = []
                already_added_polygons = []

                for line in lines:
                    for polygon in result["OUTPUT"].getFeatures():
                        if polygon in already_added_polygons:
                            continue

                        left = self.left_of_line(polygon, line)
                        if not left:
                            new_feature = QgsFeature(fields)
                            new_feature.setGeometry(polygon.geometry())
                            attributes = polygon.attributes()

                            breaking_probability = polygon.attributes()[breaking_field_idx]
                            propagation_probability = line.attributes()[propagation_field_idx]

                            acca_prob = domains.MATRIX_BREAKING[propagation_probability][breaking_probability]

                            feedback.pushInfo(f"{breaking_probability=}, {propagation_probability=}, {acca_prob=}")
                            attributes.append(acca_prob)
                            new_feature.setAttributes(attributes)
                            features_to_add.append(new_feature)
                            already_added_polygons.append(polygon)

                sink.addFeatures(features_to_add)
        return {self.OUTPUT: dest_id}

    def left_of_line(self, poly, line):
        # Extend the line at the beginning and at the end,
        # so that the single-sided buffer is wider, making
        # it more probable to find corresponding polygons
        const_line = line.geometry().constGet()
        cloned_line = QgsGeometry(const_line.clone())
        extended_line = cloned_line.extendLine(100, 100)

        # Expand the line on the left side and check if a point in the polygon is inside the buffer
        buf = extended_line.singleSidedBuffer(1000000, 4, Qgis.BufferSide.Left)
        return buf.contains(poly.geometry().pointOnSurface())
