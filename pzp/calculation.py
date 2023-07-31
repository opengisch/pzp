import datetime
import os
import traceback

from pzp_utils.processing import domains
from pzp_utils.processing.merge_by_area import MergeByArea
from qgis import processing
from qgis.core import (
    QgsApplication,
    QgsExpressionContextUtils,
    QgsProcessingException,
    QgsProject,
    QgsVectorLayer,
)

from pzp import utils


class PropagationDialog:
    def __init__(self, iface, group, parent=None):
        self.group = group

    def exec_(self):
        guess_params_propagation(self.group)


def guess_params_propagation(group):
    # process and layers
    layer_nodes = group.findLayers()
    process_type = None
    layer_propagation = None
    layer_breaking = None

    for layer_node in layer_nodes:
        pzp_layer = QgsExpressionContextUtils.layerScope(layer_node.layer()).variable("pzp_layer")
        if pzp_layer == "propagation":
            layer_propagation = layer_node.layer()
            process_type = int(QgsExpressionContextUtils.layerScope(layer_propagation).variable("pzp_process"))
        elif pzp_layer == "breaking":
            layer_breaking = layer_node.layer()
            process_type = int(QgsExpressionContextUtils.layerScope(layer_breaking).variable("pzp_process"))

    if not layer_propagation:
        utils.push_error("Layer con le probabilità di propagazione non trovato", 3)
        return
    if not layer_breaking:
        utils.push_error("Layer con le probabilità di rottura non trovato", 3)
        return
    if not process_type:
        utils.push_error("Impossibile determinare il tipo di processo", 3)
        return

    calculate_propagation(process_type, layer_propagation, layer_breaking, group)


def calculate_propagation(process_type, layer_propagation, layer_breaking, group):
    print(f"{process_type=}")
    print(f"{layer_propagation=}")
    print(f"{layer_breaking=}")

    result = None
    data_provider = None
    data_provider = layer_breaking.dataProvider()
    result = processing.run(
        "pzp:propagation",
        {
            "BREAKING_LAYER": layer_breaking.id(),
            "BREAKING_FIELD": "prob_rottura",
            "SOURCE_FIELD": "fonte_proc",
            "PROPAGATION_LAYER": layer_propagation.id(),
            "PROPAGATION_FIELD": "prob_propagazione",
            "BREAKING_FIELD_PROP": "prob_rottura",
            "SOURCE_FIELD_PROP": "fonte_proc",
            "OUTPUT": "TEMPORARY_OUTPUT",
        },
    )
    result = processing.run(
        "native:extractbyexpression",
        {
            "INPUT": result["OUTPUT"],
            "EXPRESSION": f'"proc_parz" = {process_type}',
            "OUTPUT": "TEMPORARY_OUTPUT",
        },
    )

    # Clippa per periodo di ritorno
    result = processing.run(
        "pzp:remove_overlappings",
        {
            "INPUT": result["OUTPUT"],
            "INTENSITY_FIELD": "classe_intensita",
            "PERIOD_FIELD": "periodo_ritorno",
            "SOURCE_FIELD": "fonte_proc",
            "OUTPUT": "TEMPORARY_OUTPUT",
        },
    )

    # qgis:deletecolumn has been renamed native:deletecolumn after qgis 3.16
    deletecolumn_id = "qgis:deletecolumn"
    if "qgis:deletecolumn" not in [x.id() for x in QgsApplication.processingRegistry().algorithms()]:
        deletecolumn_id = "native:deletecolumn"

    result = processing.run(
        deletecolumn_id,
        {
            "INPUT": result["OUTPUT"],
            "COLUMN": ["fid"],
            "OUTPUT": "TEMPORARY_OUTPUT",
        },
    )

    layer = result["OUTPUT"]
    layer_name = "Intensità completa"
    layer.setName(layer_name)

    gpkg_path = data_provider.dataSourceUri().split("|")[0]

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
    new_layer = QgsVectorLayer(gpkg_path + "|layername=" + layer_name, "MultiPolygon", "ogr")
    new_layer.setName("Intensità completa")

    utils.set_qml_style(new_layer, "intensity")

    project = QgsProject.instance()
    project.addMapLayer(new_layer, False)

    group_intensity_filtered = utils.create_group("Intensità (con filtri x visualizzazione scenari)", group)
    group_intensity_filtered.setExpanded(True)

    group_intensity_filtered.addLayer(new_layer)

    options = new_layer.geometryOptions()
    options.setGeometryPrecision(0.001)
    options.setRemoveDuplicateNodes(True)
    options.setGeometryChecks(["QgsIsValidCheck"])

    QgsExpressionContextUtils.setLayerVariable(new_layer, "pzp_layer", "intensity")
    QgsExpressionContextUtils.setLayerVariable(new_layer, "pzp_process", process_type)

    filter_params = [
        ("\"periodo_ritorno\"='30'", "T 30"),
        ("\"periodo_ritorno\"='100'", "T 100"),
        ("\"periodo_ritorno\"='300'", "T 300"),
        ("\"periodo_ritorno\">'300'", "T >300"),
    ]

    for param in filter_params:
        gpkg_layer = utils.create_filtered_layer_from_gpkg(
            layer.name(),
            gpkg_path,
            param[0],
            param[1],
        )
        utils.set_qml_style(gpkg_layer, "intensity")

        project.addMapLayer(gpkg_layer, False)
        group_intensity_filtered.addLayer(gpkg_layer)
        layer_node = group.findLayer(gpkg_layer.id())
        layer_node.setExpanded(False)
        layer_node.setItemVisibilityChecked(False)


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
        pzp_layer = QgsExpressionContextUtils.layerScope(layer_node.layer()).variable("pzp_layer")
        if pzp_layer == "intensity":
            layer_intensity = layer_node.layer()
            process_type = int(QgsExpressionContextUtils.layerScope(layer_intensity).variable("pzp_process"))

    if not layer_intensity:
        utils.push_error("Layer con le intensità non trovato", 3)
        return

    if not process_type:
        utils.push_error("Impossibile determinare il tipo di processo", 3)
        return

    try:
        calculate(process_type, layer_intensity)

    except QgsProcessingException as processingException:
        utils.push_error("Errore di processing: {0}".format(str(processingException)), showMore=traceback.format_exc())

    except Exception as exception:
        utils.push_error("Errore sconosciuto: {0}".format(str(exception)), showMore=traceback.format_exc())


def calculate(process_type, layer_intensity):
    print(f"{process_type=}")
    print(f"{layer_intensity=}")

    result = None
    data_provider = None

    data_provider = layer_intensity.dataProvider()
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
            "PROCESS_SOURCE_FIELD": "fonte_proc",
            "OUTPUT": "TEMPORARY_OUTPUT",
        },
    )

    result = processing.run(
        "native:fixgeometries",
        {
            "INPUT": result["OUTPUT"],
            "OUTPUT": "TEMPORARY_OUTPUT",
        },
    )

    result = processing.run(
        "pzp:merge_by_area",
        {
            "INPUT": result["OUTPUT"],
            "MODE": MergeByArea.MODE_HIGHEST_VALUE,
            "VALUE_FIELD": "grado_pericolo",
            "OUTPUT": "TEMPORARY_OUTPUT",
        },
    )

    layer = result["OUTPUT"]
    layer_name = f"Pericolo {process_type} {datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    layer.setName(layer_name)

    gpkg_path = data_provider.dataSourceUri().split("|")[0]

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
    new_layer = QgsVectorLayer(gpkg_path + "|layername=" + layer_name, "MultiPolygon", "ogr")
    new_layer.setName(f"Pericolo {process_type} {datetime.datetime.now().strftime('%Y%m%d%H%M%S')}")

    QgsProject.instance().layerTreeRoot()

    QgsProject.instance().addMapLayer(new_layer, True)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    qml_file_path = os.path.join(current_dir, "qml", "danger_level.qml")
    new_layer.loadNamedStyle(qml_file_path)

    options = new_layer.geometryOptions()
    options.setGeometryPrecision(0.001)
    options.setRemoveDuplicateNodes(True)
    options.setGeometryChecks(["QgsIsValidCheck"])

    QgsExpressionContextUtils.setLayerVariable(new_layer, "pzp_layer", "danger_zones")
    QgsExpressionContextUtils.setLayerVariable(new_layer, "pzp_process", process_type)
