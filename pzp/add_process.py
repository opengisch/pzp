import os
from datetime import datetime

from pzp_utils.processing import domains
from qgis.core import QgsExpressionContextUtils, QgsProject
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox

from pzp import utils

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

    timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
    gpkg_path = os.path.join(
        gpkg_directory_path, f"data_{process_type}_{timestamp}.gpkg"
    )
    group_name = domains.PROCESS_TYPES[process_type]

    project = QgsProject.instance()

    root = QgsProject.instance().layerTreeRoot()

    group = utils.create_group(group_name, root)

    area_layer = utils.create_layer("Area di studio")
    QgsExpressionContextUtils.setLayerVariable(area_layer, "pzp_layer", "area")
    QgsExpressionContextUtils.setLayerVariable(area_layer, "pzp_process", process_type)

    utils.add_field_to_layer(
        area_layer, "commento", "Osservazione o ev. commento", QVariant.String
    )

    utils.add_field_to_layer(
        area_layer, "proc_parz", "Processo rappresentato TI", QVariant.Int
    )
    utils.set_value_map_to_field(area_layer, "proc_parz", domains.PROCESS_TYPES)

    utils.add_field_to_layer(
        area_layer, "fonte_proc", "Fonte del processo (es. nome riale)", QVariant.String
    )

    utils.set_qml_style(area_layer, "area")
    utils.set_not_null_constraint_to_field(area_layer, "fonte_proc")
    utils.set_unique_constraint_to_field(area_layer, "fonte_proc")
    utils.set_default_value_to_field(area_layer, "proc_parz", "@pzp_process")
    utils.set_not_null_constraint_to_field(area_layer, "proc_parz")
    utils.add_layer_to_gpkg(area_layer, gpkg_path)
    area_gpkg_layer = utils.load_gpkg_layer(area_layer.name(), gpkg_path)
    project.addMapLayer(area_gpkg_layer, False)
    group.addLayer(area_gpkg_layer)
    options = area_gpkg_layer.geometryOptions()
    options.setGeometryPrecision(0.001)
    options.setRemoveDuplicateNodes(True)
    options.setGeometryChecks(["QgsIsValidCheck"])

    if process_type == 3000:  # Caduta sassi
        propagation_layer = utils.create_layer(
            "Probabilità di propagazione", "LineString"
        )
        QgsExpressionContextUtils.setLayerVariable(
            propagation_layer, "pzp_layer", "propagation"
        )
        QgsExpressionContextUtils.setLayerVariable(
            propagation_layer, "pzp_process", process_type
        )

        utils.add_field_to_layer(
            propagation_layer, "osservazioni", "Osservazioni", QVariant.String
        )
        utils.add_field_to_layer(
            propagation_layer,
            "prob_propagazione",
            "Probabilità propagazione",
            QVariant.Int,
        )
        utils.add_field_to_layer(
            propagation_layer,
            "fonte_proc",
            "Fonte del processo (es. nome riale)",
            QVariant.String,
        )
        utils.add_field_to_layer(
            propagation_layer, "prob_rottura", "Probabilità di rottura", QVariant.Int
        )
        utils.set_qml_style(propagation_layer, "propagation")
        utils.set_not_null_constraint_to_field(propagation_layer, "fonte_proc")
        # utils.set_unique_constraint_to_field(propagation_layer, "fonte_proc")
        # utils.set_value_relation_field(
        #     propagation_layer, "fonte_proc", area_gpkg_layer, "fonte_proc", "fonte_proc"
        # )
        utils.add_layer_to_gpkg(propagation_layer, gpkg_path)
        propagation_gpkg_layer = utils.load_gpkg_layer(
            propagation_layer.name(), gpkg_path
        )
        project.addMapLayer(propagation_gpkg_layer, False)
        group.addLayer(propagation_gpkg_layer)
        options = propagation_gpkg_layer.geometryOptions()
        options.setGeometryPrecision(0.001)
        options.setRemoveDuplicateNodes(True)
        options.setGeometryChecks(["QgsIsValidCheck"])

        breaking_layer = utils.create_layer("Probabilità di rottura")

        QgsExpressionContextUtils.setLayerVariable(
            breaking_layer, "pzp_layer", "breaking"
        )
        QgsExpressionContextUtils.setLayerVariable(
            breaking_layer, "pzp_process", process_type
        )

        utils.add_field_to_layer(
            breaking_layer, "osservazioni", "Osservazioni", QVariant.String
        )

        utils.add_field_to_layer(
            breaking_layer, "prob_rottura", "Probabilità di rottura", QVariant.Int
        )

        utils.add_field_to_layer(
            breaking_layer,
            "classe_intensita",
            "Intensità/impatto del processo",
            QVariant.Int,
        )

        utils.add_field_to_layer(
            breaking_layer,
            "fonte_proc",
            "Fonte del processo (es. nome riale)",
            QVariant.String,
        )

        utils.add_field_to_layer(
            breaking_layer, "proc_parz_ch", "Processo rappresentato CH", QVariant.Int
        )
        utils.add_field_to_layer(
            breaking_layer, "liv_dettaglio", "Precisione del lavoro", QVariant.Int
        )
        utils.add_field_to_layer(
            breaking_layer, "scala", "Scala di rappresentazione", QVariant.Int
        )

        utils.set_qml_style(breaking_layer, "breaking")
        utils.add_layer_to_gpkg(breaking_layer, gpkg_path)
        breaking_gpkg_layer = utils.load_gpkg_layer(breaking_layer.name(), gpkg_path)
        project.addMapLayer(breaking_gpkg_layer, False)
        group.addLayer(breaking_gpkg_layer)
        options = breaking_gpkg_layer.geometryOptions()
        options.setGeometryPrecision(0.001)
        options.setRemoveDuplicateNodes(True)
        options.setGeometryChecks(["QgsIsValidCheck"])

    else:

        intensity_layer = utils.create_layer("Intensità completa")
        QgsExpressionContextUtils.setLayerVariable(
            intensity_layer, "pzp_layer", "intensity"
        )
        QgsExpressionContextUtils.setLayerVariable(
            intensity_layer, "pzp_process", process_type
        )

        utils.add_field_to_layer(
            intensity_layer, "commento", "Osservazione o ev. commento", QVariant.String
        )
        utils.add_field_to_layer(
            intensity_layer,
            "periodo_ritorno",
            "Periodo di ritorno (es. 30, 100, 300, 99999)",
            QVariant.Int,
        )
        utils.add_field_to_layer(
            intensity_layer,
            "classe_intensita",
            "Intensità/impatto del processo",
            QVariant.Int,
        )
        utils.add_field_to_layer(
            intensity_layer, "proc_parz", "Processo rappresentato TI", QVariant.Int
        )
        utils.add_field_to_layer(
            intensity_layer,
            "fonte_proc",
            "Fonte del processo (es. nome riale)",
            QVariant.String,
        )
        utils.add_field_to_layer(
            intensity_layer, "proc_parz_ch", "Processo rappresentato CH", QVariant.Int
        )
        utils.add_field_to_layer(
            intensity_layer, "liv_dettaglio", "Precisione del lavoro", QVariant.Int
        )
        utils.add_field_to_layer(
            intensity_layer, "scala", "Scala di rappresentazione", QVariant.Int
        )
        # utils.add_field_to_layer(intensity_layer, "matrice", "No. casella matrice", QVariant.Int)
        # utils.add_field_to_layer(
        #     intensity_layer, "prob_propagazione", "Probabilità propagazione", QVariant.Int
        # )

        utils.set_qml_style(intensity_layer, "intensity")
        utils.set_expression_constraint_to_field(
            intensity_layer, "periodo_ritorno", '"periodo_ritorno" > 0'
        )
        utils.set_value_map_to_field(
            intensity_layer, "classe_intensita", domains.INTENSITIES
        )
        utils.set_not_null_constraint_to_field(intensity_layer, "classe_intensita")
        utils.set_value_map_to_field(
            intensity_layer, "proc_parz", domains.PROCESS_TYPES
        )
        utils.set_default_value_to_field(intensity_layer, "proc_parz", "@pzp_process")
        utils.set_not_null_constraint_to_field(intensity_layer, "fonte_proc")

        utils.set_value_relation_field(
            intensity_layer, "fonte_proc", area_gpkg_layer, "fonte_proc", "fonte_proc"
        )

        utils.add_layer_to_gpkg(intensity_layer, gpkg_path)
        gpkg_layer = utils.load_gpkg_layer(intensity_layer.name(), gpkg_path)
        project.addMapLayer(gpkg_layer, False)
        group.addLayer(gpkg_layer)
        options = gpkg_layer.geometryOptions()
        options.setGeometryPrecision(0.001)
        options.setRemoveDuplicateNodes(True)
        options.setGeometryChecks(["QgsIsValidCheck"])

        group_intensity_filtered = utils.create_group(
            "Intensità (con filtri x visualizzazione scenari)", group
        )
        group_intensity_filtered.setExpanded(True)

        gpkg_layer = utils.load_gpkg_layer(intensity_layer.name(), gpkg_path)
        gpkg_layer.setSubsetString("\"periodo_ritorno\"='30'")
        options = gpkg_layer.geometryOptions()
        options.setGeometryPrecision(0.001)
        options.setRemoveDuplicateNodes(True)
        options.setGeometryChecks(["QgsIsValidCheck"])
        gpkg_layer.setName("HQ 030")
        project.addMapLayer(gpkg_layer, False)
        group_intensity_filtered.addLayer(gpkg_layer)
        layer_node = group.findLayer(gpkg_layer.id())
        layer_node.setExpanded(False)
        layer_node.setItemVisibilityChecked(False)

        gpkg_layer = utils.load_gpkg_layer(intensity_layer.name(), gpkg_path)
        gpkg_layer.setSubsetString("\"periodo_ritorno\"='100'")
        options = gpkg_layer.geometryOptions()
        options.setGeometryPrecision(0.001)
        options.setRemoveDuplicateNodes(True)
        options.setGeometryChecks(["QgsIsValidCheck"])
        gpkg_layer.setName("HQ 100")
        project.addMapLayer(gpkg_layer, False)
        group_intensity_filtered.addLayer(gpkg_layer)
        layer_node = group.findLayer(gpkg_layer.id())
        layer_node.setExpanded(False)
        layer_node.setItemVisibilityChecked(False)

        gpkg_layer = utils.load_gpkg_layer(intensity_layer.name(), gpkg_path)
        gpkg_layer.setSubsetString("\"periodo_ritorno\"='300'")
        options = gpkg_layer.geometryOptions()
        options.setGeometryPrecision(0.001)
        options.setRemoveDuplicateNodes(True)
        options.setGeometryChecks(["QgsIsValidCheck"])

        gpkg_layer.setName("HQ 300")
        project.addMapLayer(gpkg_layer, False)
        group_intensity_filtered.addLayer(gpkg_layer)
        layer_node = group.findLayer(gpkg_layer.id())
        layer_node.setExpanded(False)
        layer_node.setItemVisibilityChecked(False)

        gpkg_layer = utils.load_gpkg_layer(intensity_layer.name(), gpkg_path)
        gpkg_layer.setSubsetString("\"periodo_ritorno\"='99999'")
        options = gpkg_layer.geometryOptions()
        options.setGeometryPrecision(0.001)
        options.setRemoveDuplicateNodes(True)
        options.setGeometryChecks(["QgsIsValidCheck"])
        gpkg_layer.setName("HQ >300")
        project.addMapLayer(gpkg_layer, False)
        group_intensity_filtered.addLayer(gpkg_layer)
        layer_node = group.findLayer(gpkg_layer.id())
        layer_node.setExpanded(False)
        layer_node.setItemVisibilityChecked(False)
