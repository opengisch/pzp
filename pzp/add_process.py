import os
from datetime import datetime

from qgis.core import QgsExpressionContextUtils, QgsProject
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox, QFileDialog, QMessageBox

from pzp.processing import domains
from pzp.utils import utils

FORM_CLASS = utils.get_ui_class(str(utils.get_plugin_path() / "ui" / "add_process.ui"))


class AddProcessDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.buttonBox.accepted.disconnect()
        self.buttonBox.clicked.connect(self.button_box_clicked)

        for process in domains.PROCESS_TYPES.items():
            self.process_cbox.addItem(process[1], process[0])

        self.directory_toolButton.clicked.connect(self.select_directory_clicked)

    def select_directory_clicked(self):
        directory = QFileDialog.getExistingDirectory(self, "Seleziona cartella")

        if directory:
            self.directory_lineEdit.setText(directory)

    def button_box_clicked(self, button):
        if self.buttonBox.buttonRole(button) == QDialogButtonBox.RejectRole:
            self.close()
            return

        selected_directory = self.directory_lineEdit.text()

        # check if selected dir exists
        if not selected_directory or not os.path.exists(selected_directory):
            QMessageBox.critical(
                self,
                "Errore",
                "Seleziona una cartella esistente per il processo.",
            )
            return

        process_type = self.process_cbox.currentData()
        try:
            self.add_process(process_type, selected_directory)
        except Exception as exception:
            QMessageBox.critical(
                self,
                "Errore",
                f"Si è verificato un errore durante l'aggiunta del processo: {exception}",
            )
            return

        if self.buttonBox.buttonRole(button) == QDialogButtonBox.ApplyRole:
            return

        self.close()

    @staticmethod
    def add_process(process_type, gpkg_directory_path):
        # TODO: docstring process_type is the process code
        # TODO: manage different process_types

        timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
        gpkg_path = os.path.join(gpkg_directory_path, f"data_{process_type}_{timestamp}.gpkg")
        group_name = domains.PROCESS_TYPES[process_type]

        project = QgsProject.instance()

        root = QgsProject.instance().layerTreeRoot()

        group = utils.create_group(group_name, root)

        area_layer = utils.create_layer("Area di studio")
        QgsExpressionContextUtils.setLayerVariable(area_layer, "pzp_layer", "area")
        QgsExpressionContextUtils.setLayerVariable(area_layer, "pzp_process", process_type)

        utils.add_field_to_layer(area_layer, "commento", "Nome", QVariant.String)
        utils.add_field_to_layer(area_layer, "proc_parz", "Processo", QVariant.Int)
        utils.set_value_map_to_field(area_layer, "proc_parz", domains.PROCESS_TYPES)
        utils.add_field_to_layer(area_layer, "fonte_proc", "Fonte processo", QVariant.String)

        if process_type == 3000:  # Caduta sassi
            utils.set_qml_style(area_layer, "area_caduta_sassi")
        else:
            utils.set_qml_style(area_layer, "area")

        utils.set_not_null_constraint_to_field(area_layer, "fonte_proc")
        utils.set_unique_constraint_to_field(area_layer, "fonte_proc")
        utils.set_default_value_to_field(area_layer, "proc_parz", "@pzp_process")
        utils.set_not_null_constraint_to_field(area_layer, "proc_parz")
        utils.remove_unique_constraint_to_field(area_layer, "proc_parz")

        utils.add_layer_to_gpkg(area_layer, gpkg_path)
        area_gpkg_layer = utils.load_gpkg_layer(area_layer.name(), gpkg_path)
        project.addMapLayer(area_gpkg_layer, False)
        group.addLayer(area_gpkg_layer)
        options = area_gpkg_layer.geometryOptions()
        options.setGeometryPrecision(0.001)
        options.setRemoveDuplicateNodes(True)
        options.setGeometryChecks(["QgsIsValidCheck"])

        if process_type == 3000:  # Caduta sassi
            AddProcessDialog.__add_process_caduta_sassi(gpkg_path, project, group, area_gpkg_layer)

        else:
            AddProcessDialog.__add_process_general(gpkg_path, project, group, area_gpkg_layer, process_type)

    @staticmethod
    def __add_process_general(gpkg_path, project, group, area_gpkg_layer, process_type):
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

        utils.set_value_relation_field(intensity_layer, "fonte_proc", area_gpkg_layer, "fonte_proc", "fonte_proc")

        utils.remove_unique_constraint_to_field(intensity_layer, "fonte_proc")
        utils.remove_unique_constraint_to_field(intensity_layer, "classe_intensita")
        utils.remove_unique_constraint_to_field(intensity_layer, "periodo_ritorno")

        utils.add_layer_to_gpkg(intensity_layer, gpkg_path)
        gpkg_layer = utils.load_gpkg_layer(intensity_layer.name(), gpkg_path)
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
                gpkg_path,
                param[0],
                param[1],
            )

            project.addMapLayer(gpkg_layer, False)
            group_intensity_filtered.addLayer(gpkg_layer)
            layer_node = group.findLayer(gpkg_layer.id())
            layer_node.setExpanded(False)
            layer_node.setItemVisibilityChecked(False)

    @staticmethod
    def __add_process_caduta_sassi(gpkg_path, project, group, area_gpkg_layer, process_type=3000):
        # Layer zone sorgente
        source_zones_layer = utils.create_layer("Zona sorgente (fonte processo)")
        QgsExpressionContextUtils.setLayerVariable(source_zones_layer, "pzp_layer", "source_zones")
        QgsExpressionContextUtils.setLayerVariable(source_zones_layer, "pzp_process", process_type)

        utils.add_field_to_layer(source_zones_layer, "commento", "Osservazioni", QVariant.String)
        utils.add_field_to_layer(source_zones_layer, "fonte_proc", "Settore/i (fonte processo)", QVariant.String)

        utils.add_field_to_layer(source_zones_layer, "scenario", "Scenario", QVariant.Int)
        utils.set_value_map_to_field(source_zones_layer, "scenario", domains.SOURCE_ZONES)

        utils.set_qml_style(source_zones_layer, "source_zones")
        utils.add_layer_to_gpkg(source_zones_layer, gpkg_path)
        source_zones_gpkg_layer = utils.load_gpkg_layer(source_zones_layer.name(), gpkg_path)
        project.addMapLayer(source_zones_gpkg_layer, False)
        group.addLayer(source_zones_gpkg_layer)

        # Link area layer with source zones layer
        utils.set_value_relation_field(
            area_gpkg_layer, "fonte_proc", source_zones_gpkg_layer, "fonte_proc", "fonte_proc"
        )

        # Propagation layer
        propagation_layer = utils.create_layer("Probabilità di propagazione (tutti gli scenari)", "LineString")

        utils.add_field_to_layer(
            propagation_layer,
            "prob_propagazione",
            "Limite probabilità di propagazione",
            QVariant.Int,
        )
        utils.set_value_map_to_field(propagation_layer, "prob_propagazione", domains.PROPAGATION_PROBABILITIES)

        utils.add_field_to_layer(
            propagation_layer,
            "fonte_proc",
            "Zona sorgente (fonte processo)",
            QVariant.String,
        )
        utils.add_field_to_layer(propagation_layer, "prob_rottura", "Probabilità di rottura (scenario)", QVariant.Int)
        utils.set_value_map_to_field(propagation_layer, "prob_rottura", domains.EVENT_PROBABILITIES)

        utils.add_field_to_layer(propagation_layer, "proc_parz", "Processo rappresentato TI", QVariant.Int)

        description = """Case
        when "scenario"  = 0 then 'Sconosciuto'
        when "scenario"  = 1001 then 'Scenario puntuale'
        when "scenario"  = 1000 then 'Scenario diffuso'
        else '_'
    End
            """
        utils.set_value_relation_field(
            propagation_layer, "fonte_proc", source_zones_gpkg_layer, "fonte_proc", "fonte_proc", description
        )

        utils.set_qml_style(propagation_layer, "propagation", True)
        utils.set_default_value_to_field(propagation_layer, "proc_parz", "@pzp_process")
        utils.set_not_null_constraint_to_field(propagation_layer, "fonte_proc")
        utils.remove_unique_constraint_to_field(propagation_layer, "fonte_proc")

        utils.add_layer_to_gpkg(propagation_layer, gpkg_path)
        propagation_gpkg_layer = utils.load_gpkg_layer(propagation_layer.name(), gpkg_path)
        project.addMapLayer(propagation_gpkg_layer, False)

        QgsExpressionContextUtils.setLayerVariable(propagation_gpkg_layer, "pzp_layer", "propagation")

        def post_configurations_propagation_layers(_layer):
            utils.set_field_alias(_layer, "Identificativo (automatico)", field_name="fid")

            # Virtual field should be set on the loaded layer from GPKG
            # (and the QML style should not contain the Fields category when exported,
            # otherwise the virtual field would be stored as a normal field in the GPKG)
            utils.add_virtual_field_to_layer(_layer, "lunghezza", "Lunghezza in metri", QVariant.Double, "$length")

            # Configure widget for virtual field (not included in the QML)
            _config = {
                "AllowNull": True,
                "Max": 1.7976931348623157e308,
                "Min": -1.7976931348623157e308,
                "Precision": 1,
                "Step": 1.0,
                "Style": "SpinBox",
            }
            utils.set_range_to_field(_layer, "lunghezza", _config)

            options = _layer.geometryOptions()
            options.setGeometryPrecision(0.001)
            options.setRemoveDuplicateNodes(True)
            options.setGeometryChecks([])

            QgsExpressionContextUtils.setLayerVariable(_layer, "pzp_process", process_type)

        post_configurations_propagation_layers(propagation_gpkg_layer)

        group_propagation_filtered = utils.create_group("Probabilità di propagazione", group)
        group_propagation_filtered.setExpanded(True)

        group_propagation_filtered.addLayer(propagation_gpkg_layer)

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
                propagation_layer.name(),
                gpkg_path,
                param[0],
                param[1],
            )

            project.addMapLayer(gpkg_layer, False)
            group_propagation_filtered.addLayer(gpkg_layer)
            post_configurations_propagation_layers(gpkg_layer)
            layer_node = group.findLayer(gpkg_layer.id())
            layer_node.setExpanded(False)
            layer_node.setItemVisibilityChecked(False)

        # Breaking layer
        breaking_layer = utils.create_layer("Probabilità di rottura (tutti gli scenari)")

        utils.add_field_to_layer(breaking_layer, "prob_rottura", "Probabilità di rottura", QVariant.Int)
        utils.set_value_map_to_field(breaking_layer, "prob_rottura", domains.EVENT_PROBABILITIES)

        utils.add_field_to_layer(breaking_layer, "classe_intensita", "Intensità", QVariant.Int)
        utils.set_value_map_to_field(breaking_layer, "classe_intensita", domains.INTENSITIES)

        utils.add_field_to_layer(
            breaking_layer,
            "fonte_proc",
            "Zona sorgente (fonte processo)",
            QVariant.String,
        )
        description = """Case
                when "scenario"  = 0 then 'Sconosciuto'
                when "scenario"  = 1001 then 'Scenario puntuale'
                when "scenario"  = 1000 then 'Scenario diffuso'
                else '_'
            End
                    """
        utils.set_value_relation_field(
            breaking_layer, "fonte_proc", source_zones_gpkg_layer, "fonte_proc", "fonte_proc", description
        )

        utils.add_field_to_layer(breaking_layer, "proc_parz", "Processo rappresentato TI", QVariant.Int)
        utils.add_field_to_layer(breaking_layer, "commento", "Osservazione o ev. commento", QVariant.String)

        utils.set_qml_style(breaking_layer, "breaking")
        utils.set_default_value_to_field(breaking_layer, "proc_parz", "@pzp_process")

        utils.add_layer_to_gpkg(breaking_layer, gpkg_path)
        breaking_gpkg_layer = utils.load_gpkg_layer(breaking_layer.name(), gpkg_path)
        project.addMapLayer(breaking_gpkg_layer, False)

        def post_configurations_breaking_layers(_layer):
            utils.set_field_alias(_layer, "No. identificativo", field_name="fid")

            # Virtual field should be set on the loaded layer from GPKG
            # (and the QML style should not contain the Fields category when exported,
            # otherwise the virtual field would be stored as a normal field in the GPKG)
            utils.add_virtual_field_to_layer(_layer, "area", "Area in m2", QVariant.Double, "$area")

            # Configure widget for virtual field (not included in the QML)
            _config = {
                "AllowNull": True,
                "Max": 1.7976931348623157e308,
                "Min": -1.7976931348623157e308,
                "Precision": 1,
                "Step": 1.0,
                "Style": "SpinBox",
            }
            utils.set_range_to_field(_layer, "area", _config)

            options = _layer.geometryOptions()
            options.setGeometryPrecision(0.001)
            options.setRemoveDuplicateNodes(True)
            options.setGeometryChecks([])

            QgsExpressionContextUtils.setLayerVariable(_layer, "pzp_process", process_type)

        post_configurations_breaking_layers(breaking_gpkg_layer)

        QgsExpressionContextUtils.setLayerVariable(breaking_gpkg_layer, "pzp_layer", "breaking")

        group_breaking_filtered = utils.create_group("Probabilità di rottura", group)
        group_breaking_filtered.setExpanded(True)

        group_breaking_filtered.addLayer(breaking_gpkg_layer)

        filter_params = [
            ("\"prob_rottura\"='1003'", "Probabilità di rottura alta (0-30)", True),
            ("\"prob_rottura\"='1002'", "Probabilità di rottura media (30-100)", True),
            ("\"prob_rottura\"='1001'", "Probabilità di rottura bassa (100-300)", True),
            ("\"prob_rottura\"='1000'", "Probabilità di rottura molto bassa (>300)", False),
        ]

        for param in filter_params:
            gpkg_layer = utils.create_filtered_layer_from_gpkg(
                breaking_layer.name(),
                gpkg_path,
                param[0],
                param[1],
            )
            added_layer = project.addMapLayer(gpkg_layer, False)
            if not param[2]:
                utils.set_qml_style(added_layer, "breaking_without_no_impact")

            group_breaking_filtered.addLayer(added_layer)
            post_configurations_breaking_layers(added_layer)
            layer_node = group.findLayer(added_layer.id())
            layer_node.setExpanded(False)
            layer_node.setItemVisibilityChecked(False)
