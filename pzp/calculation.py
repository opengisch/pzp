import datetime
import os

from pzp_utils.processing import domains
from qgis import processing
from qgis.core import QgsExpressionContextUtils, QgsProject, QgsVectorLayer

from pzp import utils

FORM_CLASS = utils.get_ui_class("calculation.ui")


class CalculationDialog:
    def __init__(self, iface, group, parent=None):
        self.group = group

    def exec_(self):
        guess_params(self.group)


def guess_params(group):
    # process and layers
    layer_nodes = group.findLayers()
    layer_intensity = None
    process_type = None

    for layer_node in layer_nodes:
        if layer_node.name() == "Intensità completa":
            layer_intensity = layer_node.layer()
            process_type = int(
                QgsExpressionContextUtils.layerScope(layer_intensity).variable(
                    "pzp_process"
                )
            )
            calculate(process_type, layer_intensity)


def calculate(process_type, layer_intensity):

    # TODO: calculate separately by "fonte processo" from area di studio and then group them in the end in the same layer!

    # TODO: Get list of "area di studio" as param

    result = processing.run(
        "native:extractbyexpression",
        {
            "INPUT": layer_intensity.id(),
            "EXPRESSION": f'"proc_parz" = {process_type}',
            "OUTPUT": "TEMPORARY_OUTPUT",
        },
    )

    result = processing.run(
        "pzp:fix_geometries",
        {
            "INPUT": result["OUTPUT"],
            "OUTPUT": "TEMPORARY_OUTPUT",
        },
    )

    result = processing.run(
        "pzp:apply_matrix",
        {
            "INPUT": result["OUTPUT"],
            "PERIOD_FIELD": "periodo_ritorno",
            "INTENSITY_FIELD": "classe_intensita",
            "MATRIX": domains.MATRICES[process_type],
            "OUTPUT": "TEMPORARY_OUTPUT",
        },
    )

    result = processing.run(
        "pzp:danger_zones",
        {
            "INPUT": result["OUTPUT"],
            "MATRIX_FIELD": "matrice",
            "OUTPUT": "TEMPORARY_OUTPUT",
        },
    )

    result = processing.run(
        "pzp:fix_geometries",
        {
            "INPUT": result["OUTPUT"],
            "OUTPUT": "TEMPORARY_OUTPUT",
        },
    )

    layer = result["OUTPUT"]
    layer_name = (
        f"Pericolo {process_type} {datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    )
    layer.setName(layer_name)

    gpkg_path = layer_intensity.dataProvider().dataSourceUri().split("|")[0]

    # Save output layer to gpkg
    params = {
        "LAYERS": [layer],
        "OUTPUT": gpkg_path,
        "OVERWRITE": False,  # Important!
        "SAVE_STYLES": False,
        "SAVE_METADATA": False,
        "SELECTED_FEATURES_ONLY": False,
    }
    processing.run("native:package", params)

    # Load layer from gpkg
    new_layer = QgsVectorLayer(
        gpkg_path + "|layername=" + layer_name, "MultiPolygon", "ogr"
    )
    new_layer.setName(
        f"Pericolo {process_type} {datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    )

    QgsProject.instance().layerTreeRoot()

    QgsProject.instance().addMapLayer(new_layer, True)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    qml_file_path = os.path.join(current_dir, "qml", "danger_level.qml")
    new_layer.loadNamedStyle(qml_file_path)

    # # TODO: disambiguity dialog
    # dlg = AmbiguityDialog(self.iface)
    # ambiguous_features = []

    # for feature in layer.getFeatures():
    #     # TODO: depending on the matrix of the process!!
    #     if feature["Tipo di pericolo"] in [1004]:
    #         print("AMBIGUO")
    #         ambiguous_features.append(feature)

    #     if dlg.exec_():
    #         pass

    # # Cycle all features in danger layer
    # # by process, create a list of the ambiguous ones with featureid
    # # populate list where to select the danger_type
