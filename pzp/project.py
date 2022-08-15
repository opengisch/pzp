import os
import shutil

from qgis import processing
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsEditorWidgetSetup,
    QgsField,
    QgsLayerDefinition,
    QgsProject,
    QgsVectorLayer,
)
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
    QgsProject.instance().write(project_path)

    # TODO: different layers depending on process
    # TODO: metadata


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

    gpkg_layer = load_gpkg_layer(layer.name(), gpkg_path)
    gpkg_layer.setSubsetString("\"periodo_ritorno\"='30'")
    gpkg_layer.setReadOnly(True)
    gpkg_layer.setName("HQ 030")
    project.addMapLayer(gpkg_layer, False)
    group_intensity_filtered.addLayer(gpkg_layer)

    gpkg_layer = load_gpkg_layer(layer.name(), gpkg_path)
    gpkg_layer.setSubsetString("\"periodo_ritorno\"='100'")
    gpkg_layer.setReadOnly(True)
    gpkg_layer.setName("HQ 100")
    project.addMapLayer(gpkg_layer, False)
    group_intensity_filtered.addLayer(gpkg_layer)

    gpkg_layer = load_gpkg_layer(layer.name(), gpkg_path)
    gpkg_layer.setSubsetString("\"periodo_ritorno\"='300'")
    gpkg_layer.setReadOnly(True)
    gpkg_layer.setName("HQ 300")
    project.addMapLayer(gpkg_layer, False)
    group_intensity_filtered.addLayer(gpkg_layer)

    gpkg_layer = load_gpkg_layer(layer.name(), gpkg_path)
    gpkg_layer.setSubsetString("\"periodo_ritorno\"='99999'")
    gpkg_layer.setReadOnly(True)
    gpkg_layer.setName("HQ >300")
    project.addMapLayer(gpkg_layer, False)
    group_intensity_filtered.addLayer(gpkg_layer)

    group_geodati = create_group("Geodati", group)
    load_qlr_layer("carte_nazionali_colori", group_geodati)
    load_qlr_layer("carte_nazionali_grigio", group_geodati)


def old_add_layers():
    utils.write_project_metadata("project_version", "0")  # TODO: project version


def create_layer(name, path="Polygon"):
    layer = QgsVectorLayer(
        path=path,
        baseName=name,
        providerLib="memory",
    )
    layer.setCrs(QgsCoordinateReferenceSystem("EPSG:2056"))
    return layer


def add_field_to_layer(layer, name, alias="", variant=QVariant.Int):
    field = QgsField(name, variant)
    field.setAlias(alias)
    pr = layer.dataProvider()
    pr.addAttributes([field])
    layer.updateFields()


def set_value_map_to_field(layer, field_name, domain_map):

    index = layer.fields().indexOf(field_name)
    setup = QgsEditorWidgetSetup(
        "ValueMap",
        {"map": {y: x for x, y in domain_map.items()}},
    )
    layer.setEditorWidgetSetup(index, setup)


def set_qml_style(layer, qml_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    qml_file_path = os.path.join(current_dir, "qml", f"{qml_name}.qml")
    layer.loadNamedStyle(qml_file_path)


def load_qlr_layer(qlr_name, group):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    qlr_file_path = os.path.join(current_dir, "qlr", f"{qlr_name}.qlr")
    QgsLayerDefinition().loadLayerDefinition(
        qlr_file_path, QgsProject.instance(), group
    )


def create_group(name, root=None):
    if not root:
        root = QgsProject.instance().layerTreeRoot()
    group = root.addGroup(name)

    return group


def add_layer_to_gpkg(layer, gpkg_path):
    params = {
        "LAYERS": [layer],
        "OUTPUT": gpkg_path,
        "OVERWRITE": False,  # Important!
        "SAVE_STYLES": True,
        "SAVE_METADATA": True,
        "SELECTED_FEATURES_ONLY": False,
    }
    processing.run("native:package", params)


def load_gpkg_layer(layer_name, gpkg_path):
    source_path = f"{gpkg_path}|layername={layer_name}"
    layer = QgsVectorLayer(source_path, layer_name, "ogr")
    return layer
