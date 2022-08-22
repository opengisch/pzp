import os
import shutil
from datetime import datetime

import qgis
from qgis.core import QgsProject
from qgis.PyQt.QtCore import QVariant

from pzp import domains, utils

# Layers:
# - Area di studio
# - Gradi di pericolo (questo viene generato dall'algoritmo)
# - Intensità completa
# - Intensità con filtri (gruppo)
#   - HQ 030
#   - HQ 100
#   - HQ 300
#   - EHQ >300
# - Zone di propagazione (solo per caduta sassi)
# - Dati di base (gruppo con geoservizi)
# - Mappe base (gruppo con geoservizi)


def create_project(name, working_dir, process):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    empty_gpkg_file_path = os.path.join(current_dir, "data", "empty.gpkg")

    gpkg_path = os.path.join(working_dir, f"{name}.gpkg")
    project_path = os.path.join(working_dir, f"{name}.qgs")
    shutil.copy(empty_gpkg_file_path, gpkg_path)

    add_layers(gpkg_path)

    # Read the version of the plugin
    version = qgis.utils.plugins_metadata_parser["pzp"].get("general", "version")
    utils.write_project_metadata("project_version", version)
    utils.write_project_metadata("created_at", str(datetime.now()))
    process_type_id, process_type = list(domains.PROCESS_TYPES.items())[process]
    utils.write_project_metadata("process_type_id", str(process_type_id))
    utils.write_project_metadata("process_type", process_type)

    QgsProject.instance().write(project_path)

    # TODO: different layers depending on process
    # TODO: layers metadata


def add_layers(gpkg_path):
    project = QgsProject.instance()
    group = create_group("Pericoli naturali mandato PZP")

    layer = create_layer("Area di studio")
    add_field_to_layer(layer, "fid", "No. identificativo", QVariant.LongLong)
    add_field_to_layer(
        layer, "commento", "Osservazione o ev. commento", QVariant.String
    )
    add_field_to_layer(layer, "proc_parz", "Processo rappresentato TI", QVariant.Int)
    set_value_map_to_field(layer, "proc_parz", domains.PROCESS_TYPES)
    add_field_to_layer(
        layer, "fonte_proc", "Fonte del processo (es. nome riale)", QVariant.String
    )

    set_qml_style(layer, "area")
    add_layer_to_gpkg(layer, gpkg_path)
    gpkg_layer = load_gpkg_layer(layer.name(), gpkg_path)
    project.addMapLayer(gpkg_layer, False)
    group.addLayer(gpkg_layer)

    layer = create_layer("Intensità completa")
    add_field_to_layer(layer, "fid", "No. identificativo", QVariant.LongLong)
    add_field_to_layer(
        layer, "commento", "Osservazione o ev. commento", QVariant.String
    )
    add_field_to_layer(
        layer,
        "periodo_ritorno",
        "Periodo di ritorno (es. 30, 100, 300, 99999)",
        QVariant.Int,
    )
    set_value_map_to_field(layer, "periodo_ritorno", domains.EVENT_PROBABILITIES)
    add_field_to_layer(
        layer, "classe_intensita", "Intensità/impatto del processo", QVariant.Int
    )
    set_value_map_to_field(layer, "classe_intensita", domains.INTENSITIES)
    add_field_to_layer(layer, "proc_parz", "Processo rappresentato TI", QVariant.Int)
    set_value_map_to_field(layer, "proc_parz", domains.PROCESS_TYPES)
    add_field_to_layer(
        layer, "fonte_proc", "Fonte del processo (es. nome riale)", QVariant.String
    )
    add_field_to_layer(layer, "proc_parz_ch", "Processo rappresentato CH", QVariant.Int)
    add_field_to_layer(layer, "liv_dettaglio", "Precisione del lavoro", QVariant.Int)
    add_field_to_layer(layer, "scala", "Scala di rappresentazione", QVariant.Int)
    add_field_to_layer(layer, "matrice", "No. casella matrice", QVariant.Int)
    add_field_to_layer(
        layer, "prob_propagazione", "Probabilità propagazione", QVariant.Int
    )

    set_qml_style(layer, "intensity")
    add_layer_to_gpkg(layer, gpkg_path)
    gpkg_layer = load_gpkg_layer(layer.name(), gpkg_path)
    project.addMapLayer(gpkg_layer, False)
    group.addLayer(gpkg_layer)

    group_intensity_filtered = create_group(
        "Intensità (con filtri x visualizzazione scenari)", group
    )
    group_intensity_filtered.setExpanded(True)

    gpkg_layer = load_gpkg_layer(layer.name(), gpkg_path)
    gpkg_layer.setSubsetString("\"periodo_ritorno\"='30'")
    gpkg_layer.setReadOnly(True)
    gpkg_layer.setName("HQ 030")
    project.addMapLayer(gpkg_layer, False)
    group_intensity_filtered.addLayer(gpkg_layer)
    layer_node = group.findLayer(gpkg_layer.id())
    layer_node.setExpanded(False)
    layer_node.setItemVisibilityChecked(False)

    gpkg_layer = load_gpkg_layer(layer.name(), gpkg_path)
    gpkg_layer.setSubsetString("\"periodo_ritorno\"='100'")
    gpkg_layer.setReadOnly(True)
    gpkg_layer.setName("HQ 100")
    project.addMapLayer(gpkg_layer, False)
    group_intensity_filtered.addLayer(gpkg_layer)
    layer_node = group.findLayer(gpkg_layer.id())
    layer_node.setExpanded(False)
    layer_node.setItemVisibilityChecked(False)

    gpkg_layer = load_gpkg_layer(layer.name(), gpkg_path)
    gpkg_layer.setSubsetString("\"periodo_ritorno\"='300'")
    gpkg_layer.setReadOnly(True)
    gpkg_layer.setName("HQ 300")
    project.addMapLayer(gpkg_layer, False)
    group_intensity_filtered.addLayer(gpkg_layer)
    layer_node = group.findLayer(gpkg_layer.id())
    layer_node.setExpanded(False)
    layer_node.setItemVisibilityChecked(False)

    gpkg_layer = load_gpkg_layer(layer.name(), gpkg_path)
    gpkg_layer.setSubsetString("\"periodo_ritorno\"='99999'")
    gpkg_layer.setReadOnly(True)
    gpkg_layer.setName("HQ >300")
    project.addMapLayer(gpkg_layer, False)
    group_intensity_filtered.addLayer(gpkg_layer)
    layer_node = group.findLayer(gpkg_layer.id())
    layer_node.setExpanded(False)
    layer_node.setItemVisibilityChecked(False)

    # Raster layers
    load_qlr_layer("dati_base", group)
    load_qlr_layer("mappe_base", group)
