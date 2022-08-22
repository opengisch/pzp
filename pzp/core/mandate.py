from qgis.core import QgsProject
from qgis.PyQt.QtCore import QVariant

from pzp import domains, utils


def add_mandate(name):
    # TODO: In the ui Check if one already exists in the current QGIS project and inform the user
    group = utils.create_group(f"Pericoli naturali mandato PZP - {name}")

    # Raster layers
    utils.load_qlr_layer("dati_base", group)
    utils.load_qlr_layer("mappe_base", group)


def add_process(process_type, gpkg_path, group_name):
    # In the ui, we'll try to find the mandate group, if not we ask to the user
    # If the gpkg already exists, we append the layer.
    # TODO: inform user

    project = QgsProject.instance()

    root = QgsProject.instance().layerTreeRoot()
    if group_name:
        root = root.findGroup(group_name)

    group = utils.create_group(process_type, root)

    layer = utils.create_layer("Area di studio")
    utils.add_field_to_layer(layer, "fid", "No. identificativo", QVariant.LongLong)
    utils.add_field_to_layer(
        layer, "commento", "Osservazione o ev. commento", QVariant.String
    )
    utils.add_field_to_layer(
        layer, "proc_parz", "Processo rappresentato TI", QVariant.Int
    )
    utils.set_value_map_to_field(layer, "proc_parz", domains.PROCESS_TYPES)
    utils.add_field_to_layer(
        layer, "fonte_proc", "Fonte del processo (es. nome riale)", QVariant.String
    )

    utils.set_qml_style(layer, "area")
    utils.add_layer_to_gpkg(layer, gpkg_path)
    gpkg_layer = utils.load_gpkg_layer(layer.name(), gpkg_path)
    project.addMapLayer(gpkg_layer, False)
    group.addLayer(gpkg_layer)

    layer = utils.create_layer("Intensità completa")
    utils.add_field_to_layer(layer, "fid", "No. identificativo", QVariant.LongLong)
    utils.add_field_to_layer(
        layer, "commento", "Osservazione o ev. commento", QVariant.String
    )
    utils.add_field_to_layer(
        layer,
        "periodo_ritorno",
        "Periodo di ritorno (es. 30, 100, 300, 99999)",
        QVariant.Int,
    )
    utils.set_value_map_to_field(layer, "periodo_ritorno", domains.EVENT_PROBABILITIES)
    utils.add_field_to_layer(
        layer, "classe_intensita", "Intensità/impatto del processo", QVariant.Int
    )
    utils.set_value_map_to_field(layer, "classe_intensita", domains.INTENSITIES)
    utils.add_field_to_layer(
        layer, "proc_parz", "Processo rappresentato TI", QVariant.Int
    )
    utils.set_value_map_to_field(layer, "proc_parz", domains.PROCESS_TYPES)
    utils.add_field_to_layer(
        layer, "fonte_proc", "Fonte del processo (es. nome riale)", QVariant.String
    )
    utils.add_field_to_layer(
        layer, "proc_parz_ch", "Processo rappresentato CH", QVariant.Int
    )
    utils.add_field_to_layer(
        layer, "liv_dettaglio", "Precisione del lavoro", QVariant.Int
    )
    utils.add_field_to_layer(layer, "scala", "Scala di rappresentazione", QVariant.Int)
    utils.add_field_to_layer(layer, "matrice", "No. casella matrice", QVariant.Int)
    utils.add_field_to_layer(
        layer, "prob_propagazione", "Probabilità propagazione", QVariant.Int
    )

    utils.set_qml_style(layer, "intensity")
    utils.add_layer_to_gpkg(layer, gpkg_path)
    gpkg_layer = utils.load_gpkg_layer(layer.name(), gpkg_path)
    project.addMapLayer(gpkg_layer, False)
    group.addLayer(gpkg_layer)

    group_intensity_filtered = utils.create_group(
        "Intensità (con filtri x visualizzazione scenari)", group
    )
    group_intensity_filtered.setExpanded(True)

    gpkg_layer = utils.load_gpkg_layer(layer.name(), gpkg_path)
    gpkg_layer.setSubsetString("\"periodo_ritorno\"='30'")
    gpkg_layer.setReadOnly(True)
    gpkg_layer.setName("HQ 030")
    project.addMapLayer(gpkg_layer, False)
    group_intensity_filtered.addLayer(gpkg_layer)
    layer_node = group.findLayer(gpkg_layer.id())
    layer_node.setExpanded(False)
    layer_node.setItemVisibilityChecked(False)

    gpkg_layer = utils.load_gpkg_layer(layer.name(), gpkg_path)
    gpkg_layer.setSubsetString("\"periodo_ritorno\"='100'")
    gpkg_layer.setReadOnly(True)
    gpkg_layer.setName("HQ 100")
    project.addMapLayer(gpkg_layer, False)
    group_intensity_filtered.addLayer(gpkg_layer)
    layer_node = group.findLayer(gpkg_layer.id())
    layer_node.setExpanded(False)
    layer_node.setItemVisibilityChecked(False)

    gpkg_layer = utils.load_gpkg_layer(layer.name(), gpkg_path)
    gpkg_layer.setSubsetString("\"periodo_ritorno\"='300'")
    gpkg_layer.setReadOnly(True)
    gpkg_layer.setName("HQ 300")
    project.addMapLayer(gpkg_layer, False)
    group_intensity_filtered.addLayer(gpkg_layer)
    layer_node = group.findLayer(gpkg_layer.id())
    layer_node.setExpanded(False)
    layer_node.setItemVisibilityChecked(False)

    gpkg_layer = utils.load_gpkg_layer(layer.name(), gpkg_path)
    gpkg_layer.setSubsetString("\"periodo_ritorno\"='99999'")
    gpkg_layer.setReadOnly(True)
    gpkg_layer.setName("HQ >300")
    project.addMapLayer(gpkg_layer, False)
    group_intensity_filtered.addLayer(gpkg_layer)
    layer_node = group.findLayer(gpkg_layer.id())
    layer_node.setExpanded(False)
    layer_node.setItemVisibilityChecked(False)
