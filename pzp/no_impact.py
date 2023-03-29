from qgis import processing
from qgis.core import QgsExpressionContextUtils, edit


def guess_params(group):
    # process and layers
    layer_nodes = group.findLayers()
    layer_intensity = None
    layer_area = None
    process_type = None

    for layer_node in layer_nodes:
        if layer_node.name() == "Intensità completa":
            layer_intensity = layer_node.layer()
            process_type = int(
                QgsExpressionContextUtils.layerScope(layer_intensity).variable(
                    "pzp_process"
                )
            )
        elif layer_node.name() == "Area di studio":
            layer_area = layer_node.layer()

    return process_type, layer_intensity, layer_area


def calculate(process_type, layer_intensity, layer_area):
    result = processing.run(
        "pzp:no_impact",
        {
            "AREA_LAYER": layer_area.id(),
            "AREA_PROCESS_SOURCE_FIELD": "fonte_proc",
            "INTENSITY_PROCESS_SOURCE_FIELD": "fonte_proc",
            "INTENSITY_LAYER": layer_intensity.id(),
            "PERIOD_FIELD": "periodo_ritorno",
            "INTENSITY_FIELD": "classe_intensita",
            "OUTPUT": "TEMPORARY_OUTPUT",
        },
    )

    result_layer = result["OUTPUT"]

    with edit(layer_intensity):
        for feature in result_layer.getFeatures():
            feature["fid"] = None
            layer_intensity.addFeature(feature)
