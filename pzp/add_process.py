import os
from datetime import datetime

from qgis.core import QgsExpressionContextUtils, QgsProject
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox

from pzp import domains, utils

FORM_CLASS = utils.get_ui_class("add_process.ui")


class AddProcessDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.buttonBox.accepted.disconnect()
        self.buttonBox.clicked.connect(self.button_box_clicked)

        for process in domains.PROCESS_TYPES.items():
            self.process_cbox.addItem(process[1], process[0])

        self.file_widget.setFilter("*.gpkg;;*.GPKG")

    def button_box_clicked(self, button):
        if self.buttonBox.buttonRole(button) == QDialogButtonBox.ApplyRole:
            process_type = self.process_cbox.currentData()
            add_process(process_type, self.file_widget.filePath())
        elif self.buttonBox.buttonRole(button) == QDialogButtonBox.AcceptRole:
            process_type = self.process_cbox.currentData()
            add_process(process_type, self.file_widget.filePath())
            self.close()
        else:
            self.close()


def add_process(process_type, gpkg_directory_path):

    # TODO: docstring process_type is the process code
    # TODO: manage different process_types
    # TODO: set_layer_metadata (or variable?) and use process the set default

    timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
    gpkg_path = os.path.join(
        gpkg_directory_path, f"data_{process_type}_{timestamp}.gpkg"
    )
    group_name = domains.PROCESS_TYPES[process_type]

    project = QgsProject.instance()

    root = QgsProject.instance().layerTreeRoot()

    group = utils.create_group(group_name, root)

    layer = utils.create_layer("Area di studio")
    QgsExpressionContextUtils.setLayerVariable(layer, "pzp_layer", "area")
    QgsExpressionContextUtils.setLayerVariable(layer, "pzp_process", process_type)

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
    QgsExpressionContextUtils.setLayerVariable(layer, "pzp_layer", "intensity")
    QgsExpressionContextUtils.setLayerVariable(layer, "pzp_process", process_type)

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
    utils.add_field_to_layer(
        layer, "classe_intensita", "Intensità/impatto del processo", QVariant.Int
    )
    utils.add_field_to_layer(
        layer, "proc_parz", "Processo rappresentato TI", QVariant.Int
    )
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
    utils.set_value_map_to_field(layer, "periodo_ritorno", domains.EVENT_PROBABILITIES)
    utils.set_value_map_to_field(layer, "classe_intensita", domains.INTENSITIES)
    utils.set_value_map_to_field(layer, "proc_parz", domains.PROCESS_TYPES)
    utils.set_default_value_to_field(layer, "proc_parz", "@pzp_process")
    utils.set_not_null_constraint_to_field(layer, "fonte_proc")

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
