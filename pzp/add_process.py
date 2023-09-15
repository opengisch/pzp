import os
from datetime import datetime

from pzp_utils.processing import domains
from qgis.core import QgsExpressionContextUtils, QgsProject
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox

from pzp.utils import utils

FORM_CLASS = utils.get_ui_class(os.path.join(os.path.dirname(__file__), "ui/add_process.ui"))


class AddProcessDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self._gpkg_path = str()
        self._area_gpkg_layer = None

        self.buttonBox.accepted.disconnect()
        self.buttonBox.clicked.connect(self.button_box_clicked)

        for process in domains.PROCESS_TYPES.items():
            self.process_cbox.addItem(process[1], process[0])

        self.file_widget.setFilter("*.gpkg;;*.GPKG")

    def button_box_clicked(self, button):
        if self.buttonBox.buttonRole(button) == QDialogButtonBox.AcceptRole:
            process_type = self.process_cbox.currentData()
            self._add_process(process_type, self.file_widget.filePath())

        self.close()

    def _add_process(self, process_type, gpkg_directory_path):
        # TODO: docstring process_type is the process code
        # TODO: manage different process_types

        timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
        self._gpkg_path = os.path.join(gpkg_directory_path, f"data_{process_type}_{timestamp}.gpkg")
        group_name = domains.PROCESS_TYPES[process_type]

        project = QgsProject.instance()

        root = QgsProject.instance().layerTreeRoot()

        group = utils.create_group(group_name, root)

        area_layer = utils.create_layer("Area di studio")
        QgsExpressionContextUtils.setLayerVariable(area_layer, "pzp_layer", "area")
        QgsExpressionContextUtils.setLayerVariable(area_layer, "pzp_process", process_type)

        utils.add_field_to_layer(area_layer, "commento", "Osservazione o ev. commento", QVariant.String)

        utils.add_field_to_layer(area_layer, "proc_parz", "Processo rappresentato TI", QVariant.Int)
        utils.set_value_map_to_field(area_layer, "proc_parz", domains.PROCESS_TYPES)

        utils.add_field_to_layer(area_layer, "fonte_proc", "Fonte del processo (es. nome riale)", QVariant.String)

        # For caduta sassi fonte_proc are multiple in separate layer
        if process_type != 3000:  # Caduta sassi
            utils.set_qml_style(area_layer, "area")

            utils.set_not_null_constraint_to_field(area_layer, "fonte_proc")
            utils.set_unique_constraint_to_field(area_layer, "fonte_proc")
        else:
            utils.set_qml_style(area_layer, "area_caduta_sassi")

        utils.set_default_value_to_field(area_layer, "proc_parz", "@pzp_process")
        utils.set_not_null_constraint_to_field(area_layer, "proc_parz")
        utils.remove_unique_constraint_to_field(area_layer, "proc_parz")
        utils.add_layer_to_gpkg(area_layer, self._gpkg_path)
        self._area_gpkg_layer = utils.load_gpkg_layer(area_layer.name(), self._gpkg_path)
        project.addMapLayer(self._area_gpkg_layer, False)
        group.addLayer(self._area_gpkg_layer)
        options = self._area_gpkg_layer.geometryOptions()
        options.setGeometryPrecision(0.001)
        options.setRemoveDuplicateNodes(True)
        options.setGeometryChecks(["QgsIsValidCheck"])

        if process_type == 3000:  # Caduta sassi
            self._add_process_caduta_sassi(process_type, group)

        else:
            intensity_layer = utils.create_layer("Intensità completa")

            utils.add_field_to_layer(intensity_layer, "commento", "Osservazione o ev. commento", QVariant.String)
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
            utils.add_field_to_layer(intensity_layer, "proc_parz", "Processo rappresentato TI", QVariant.Int)
            utils.add_field_to_layer(
                intensity_layer,
                "fonte_proc",
                "Fonte del processo (es. nome riale)",
                QVariant.String,
            )

            utils.set_qml_style(intensity_layer, "intensity")
            utils.set_expression_constraint_to_field(intensity_layer, "periodo_ritorno", '"periodo_ritorno" > 0')
            utils.set_value_map_to_field(intensity_layer, "classe_intensita", domains.INTENSITIES)
            utils.set_not_null_constraint_to_field(intensity_layer, "classe_intensita")
            utils.set_value_map_to_field(intensity_layer, "proc_parz", domains.PROCESS_TYPES)
            utils.set_default_value_to_field(intensity_layer, "proc_parz", "@pzp_process")
            utils.set_not_null_constraint_to_field(intensity_layer, "fonte_proc")

            utils.set_value_relation_field(
                intensity_layer, "fonte_proc", self._area_gpkg_layer, "fonte_proc", "fonte_proc"
            )

            utils.remove_unique_constraint_to_field(intensity_layer, "fonte_proc")
            utils.remove_unique_constraint_to_field(intensity_layer, "classe_intensita")
            utils.remove_unique_constraint_to_field(intensity_layer, "periodo_ritorno")

            utils.add_layer_to_gpkg(intensity_layer, self._gpkg_path)
            gpkg_layer = utils.load_gpkg_layer(intensity_layer.name(), self._gpkg_path)
            project.addMapLayer(gpkg_layer, False)

            QgsExpressionContextUtils.setLayerVariable(gpkg_layer, "pzp_layer", "intensity")
            QgsExpressionContextUtils.setLayerVariable(gpkg_layer, "pzp_process", process_type)

            group.addLayer(gpkg_layer)
            options = gpkg_layer.geometryOptions()
            options.setGeometryPrecision(0.001)
            options.setRemoveDuplicateNodes(True)
            options.setGeometryChecks(["QgsIsValidCheck"])

            group_intensity_filtered = utils.create_group("Intensità (con filtri x visualizzazione scenari)", group)
            group_intensity_filtered.setExpanded(True)

            if process_type in [2001, 2002, 3000, 4100, 4200]:
                filter_params = [
                    ("\"periodo_ritorno\"='30'", "T 30"),
                    ("\"periodo_ritorno\"='100'", "T 100"),
                    ("\"periodo_ritorno\"='300'", "T 300"),
                    ("\"periodo_ritorno\">'300'", "T >300"),
                ]
            else:
                filter_params = [
                    ("\"periodo_ritorno\"='30'", "HQ 030"),
                    ("\"periodo_ritorno\"='100'", "HQ 100"),
                    ("\"periodo_ritorno\"='300'", "HQ 300"),
                    ("\"periodo_ritorno\">'300'", "HQ >300"),
                ]

            for param in filter_params:
                gpkg_layer = utils.create_filtered_layer_from_gpkg(
                    intensity_layer.name(),
                    self._gpkg_path,
                    param[0],
                    param[1],
                )

                project.addMapLayer(gpkg_layer, False)
                group_intensity_filtered.addLayer(gpkg_layer)
                layer_node = group.findLayer(gpkg_layer.id())
                layer_node.setExpanded(False)
                layer_node.setItemVisibilityChecked(False)

    def _add_process_caduta_sassi(self, process_type, group):
        zone_di_stacco_gpkg_layer = self._add_process_caduta_sassi_zone_di_stacco()
        group.addLayer(zone_di_stacco_gpkg_layer)

        propagation_gpkg_layer = self._add_process_caduta_sassi_propagation(zone_di_stacco_gpkg_layer)

        QgsExpressionContextUtils.setLayerVariable(propagation_gpkg_layer, "pzp_layer", "propagation")
        QgsExpressionContextUtils.setLayerVariable(propagation_gpkg_layer, "pzp_process", process_type)

        group_propagation_filtered = utils.create_group("Probabilità di propagazione", group)
        group_propagation_filtered.setExpanded(True)

        group_propagation_filtered.addLayer(propagation_gpkg_layer)
        options = propagation_gpkg_layer.geometryOptions()
        options.setGeometryPrecision(0.001)
        options.setRemoveDuplicateNodes(True)
        options.setGeometryChecks(["QgsIsValidCheck"])

        filter_params = [
            ("\"prob_rottura\"='1003'", "Prob. propagazione (scenario rottura 0-30)"),
            ("\"prob_rottura\"='1002'", "Prob. propagazione (scenario rottura 30-100)"),
            (
                "\"prob_rottura\"='1001'",
                "Prob. propagazione (scenario rottura 100-300)",
            ),
            ("\"prob_rottura\"='1000'", "Prob. propagazione (scenario rottura >300)"),
        ]

        for param in filter_params:
            gpkg_layer = utils.create_filtered_layer_from_gpkg(
                propagation_gpkg_layer.name(),
                self._gpkg_path,
                param[0],
                param[1],
            )

            QgsProject.instance().addMapLayer(gpkg_layer, False)
            group_propagation_filtered.addLayer(gpkg_layer)
            layer_node = group.findLayer(gpkg_layer.id())
            layer_node.setExpanded(False)
            layer_node.setItemVisibilityChecked(False)

        breaking_gpkg_layer = self._add_process_caduta_sassi_breaking(zone_di_stacco_gpkg_layer)

        QgsExpressionContextUtils.setLayerVariable(breaking_gpkg_layer, "pzp_layer", "breaking")
        QgsExpressionContextUtils.setLayerVariable(breaking_gpkg_layer, "pzp_process", process_type)

        group_breaking_filtered = utils.create_group("Probabilità di rottura", group)
        group_breaking_filtered.setExpanded(True)

        group_breaking_filtered.addLayer(breaking_gpkg_layer)
        options = breaking_gpkg_layer.geometryOptions()
        options.setGeometryPrecision(0.001)
        options.setRemoveDuplicateNodes(True)
        options.setGeometryChecks(["QgsIsValidCheck"])

        filter_params = [
            ("\"prob_rottura\"='1003'", "Probabilità di rottura alta (0-30)", True),
            ("\"prob_rottura\"='1002'", "Probabilità di rottura media (30-100)", True),
            ("\"prob_rottura\"='1001'", "Probabilità di rottura bassa (100-300)", True),
            (
                "\"prob_rottura\"='1000'",
                "Probabilità di rottura molto bassa (>300)",
                False,
            ),
        ]

        for param in filter_params:
            gpkg_layer = utils.create_filtered_layer_from_gpkg(
                breaking_gpkg_layer.name(),
                self._gpkg_path,
                param[0],
                param[1],
            )

            added_layer = QgsProject.instance().addMapLayer(gpkg_layer, False)
            if param[2] is False:
                utils.set_qml_style(added_layer, "breaking_without_no_impact")
            group_breaking_filtered.addLayer(added_layer)
            layer_node = group.findLayer(added_layer.id())
            layer_node.setExpanded(False)
            layer_node.setItemVisibilityChecked(False)

    def _add_process_caduta_sassi_zone_di_stacco(self):
        zone_di_stacco_layer = utils.create_layer("Zone di stacco")

        utils.add_field_to_layer(zone_di_stacco_layer, "nome", "Nome", QVariant.String)
        utils.add_field_to_layer(zone_di_stacco_layer, "osservazioni", "Tipo di scenario", QVariant.String)

        utils.set_qml_style(zone_di_stacco_layer, "detachment_zone")

        utils.add_layer_to_gpkg(zone_di_stacco_layer, self._gpkg_path)
        zone_di_stacco_gpkg_layer = utils.load_gpkg_layer(zone_di_stacco_layer.name(), self._gpkg_path)

        QgsProject.instance().addMapLayer(zone_di_stacco_gpkg_layer, False)
        return zone_di_stacco_gpkg_layer

    def _add_process_caduta_sassi_propagation(self, zone_di_stacco_gpkg_layer):
        propagation_layer = utils.create_layer("Probabilità di propagazione (tutti gli scenari)", "LineString")

        utils.add_field_to_layer(propagation_layer, "osservazioni", "Osservazioni", QVariant.String)
        utils.add_field_to_layer(
            propagation_layer,
            "prob_propagazione",
            "Probabilità propagazione",
            QVariant.Int,
        )
        utils.add_field_to_layer(
            propagation_layer,
            "fonte_proc",
            "Zona di stacco",
            QVariant.String,
        )
        utils.add_field_to_layer(propagation_layer, "prob_rottura", "Probabilità di rottura", QVariant.Int)
        utils.set_qml_style(propagation_layer, "propagation_caduta_sassi")
        utils.set_not_null_constraint_to_field(propagation_layer, "fonte_proc")
        utils.remove_unique_constraint_to_field(propagation_layer, "fonte_proc")

        utils.add_layer_to_gpkg(propagation_layer, self._gpkg_path)
        propagation_gpkg_layer = utils.load_gpkg_layer(propagation_layer.name(), self._gpkg_path)

        QgsProject.instance().addMapLayer(propagation_gpkg_layer, False)
        return propagation_gpkg_layer

    def _add_process_caduta_sassi_breaking(self, zone_di_stacco_gpkg_layer):
        breaking_layer = utils.create_layer("Probabilità di rottura (tutti gli scenari)")

        utils.add_field_to_layer(breaking_layer, "osservazioni", "Osservazioni", QVariant.String)

        utils.add_field_to_layer(breaking_layer, "prob_rottura", "Probabilità di rottura", QVariant.Int)

        utils.add_field_to_layer(
            breaking_layer,
            "classe_intensita",
            "Intensità/impatto del processo",
            QVariant.Int,
        )

        utils.add_field_to_layer(
            breaking_layer,
            "fonte_proc",
            "Zone di stacco",
            QVariant.String,
        )

        utils.add_field_to_layer(breaking_layer, "proc_parz", "Processo rappresentato TI", QVariant.Int)

        utils.set_default_value_to_field(breaking_layer, "proc_parz", "@pzp_process")

        utils.set_qml_style(breaking_layer, "breaking_caduta_sassi")

        utils.add_layer_to_gpkg(breaking_layer, self._gpkg_path)
        breaking_gpkg_layer = utils.load_gpkg_layer(breaking_layer.name(), self._gpkg_path)

        QgsProject.instance().addMapLayer(breaking_gpkg_layer, False)
        return breaking_gpkg_layer
