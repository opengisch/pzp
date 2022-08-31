import os
import webbrowser
from datetime import datetime

from qgis import processing
from qgis.core import QgsApplication, QgsProject
from qgis.gui import QgsOptionsPageWidget, QgsOptionsWidgetFactory
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QHBoxLayout, QMenu, QToolButton

from pzp import domains, utils
from pzp.processing_provider.provider import Provider
from pzp.ui.add_process import AddProcessDialog
from pzp.ui.ambiguity_dialog import AmbiguityDialog
from pzp.ui.calculation_dialog import CalculationDialog
from pzp.ui.check_dock import CheckResultsDock
from pzp.ui.resources import *  # noqa


class PZP:
    def __init__(self, iface):
        self.iface = iface
        self.toolbar = None
        self.provider = None

    def initGui(self):
        self.toolbar = self.iface.addToolBar("PZP")
        self.toolbar.setObjectName("PZPToolbar")
        self.toolbar.setToolTip("PZP Toolbar")

        self.toolbar.addAction(
            self.create_action(
                "landslide.png", "Aggiungi processo", self.do_add_process
            )
        )

        geodata_menu = QMenu()
        add_basemaps_action = self.create_action(
            "world.png", "Aggiungi mappe base", self.do_add_basemaps
        )

        geodata_menu.addAction(add_basemaps_action)
        geodata_menu.addAction(
            self.create_action("ruler.png", "Aggiungi dati base", self.do_add_base_data)
        )

        toolButton = QToolButton()
        toolButton.setDefaultAction(add_basemaps_action)
        toolButton.setMenu(geodata_menu)
        toolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.toolbar.addWidget(toolButton)

        self.toolbar.addAction(
            self.create_action(
                "check.png", "Verifica geometrie", self.do_check_geometries
            )
        )
        self.toolbar.addAction(
            self.create_action(
                "danger.png", "Calcola zone di pericolo", self.do_calculate_zones
            )
        )
        self.toolbar.addAction(self.create_action("help.png", "Aiuto", self.do_help))
        self.initProcessing()
        self.options_factory = PluginOptionsFactory()
        self.options_factory.setTitle("PZP")
        self.iface.registerOptionsWidgetFactory(self.options_factory)

    def initProcessing(self):
        self.provider = Provider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def create_action(self, icon, name, callback):
        action = QAction(
            QIcon(f":/plugins/pzp/icons/{icon}"), name, self.iface.mainWindow()
        )
        action.triggered.connect(callback)
        self.iface.addPluginToMenu("PZP", action)
        return action

    def unload(self):
        for action in self.toolbar.actions():
            self.iface.removePluginMenu("PZP", action)
            del action

        del self.toolbar
        QgsApplication.processingRegistry().removeProvider(self.provider)
        self.iface.unregisterOptionsWidgetFactory(self.options_factory)

    def do_add_process(self):
        dlg = AddProcessDialog(self.iface)
        dlg.exec_()

    def do_add_basemaps(self):
        utils.load_qlr_layer("mappe_base")

    def do_add_base_data(self):
        utils.load_qlr_layer("dati_base")

    @utils.check_project()
    def do_check_geometries(self):
        self.checks_dock = CheckResultsDock(self.iface)

        self.checks_dock.setObjectName("CheckResultsDock")
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.checks_dock)
        self.checks_dock.setVisible(True)
        self.checks_dock.show()

    # @utils.check_project()
    def do_calculate_zones(self):
        # TODO: check the layers and the fields needed are present

        # TODO: run the algo for the process defined in the project instead of asking

        dlg = CalculationDialog(self.iface)
        for process in domains.PROCESS_TYPES.items():
            dlg.process_cbox.addItem(process[1], process)

        if dlg.exec_():
            selected_process = dlg.process_cbox.currentData()
            result = processing.run(
                "pzp:danger_zones",
                {
                    "INPUT": "Intensità completa",
                    "PROCESS_FIELD": "proc_parz",
                    "PROBABILITY_FIELD": "periodo_ritorno",
                    "INTENSITY_FIELD": "classe_intensita",
                    "PROCESS_TYPE": dlg.process_cbox.currentIndex(),
                    "OUTPUT": "TEMPORARY_OUTPUT",
                },
            )

            layer = result["OUTPUT"]
            layer.setName(f"Pericolo {selected_process[1]} {datetime.now()}")
            root = QgsProject.instance().layerTreeRoot()

            tree_layer = root.findLayer(
                QgsProject.instance().mapLayersByName("Intensità completa")[0]
            )
            layer_parent = tree_layer.parent()

            QgsProject.instance().addMapLayer(layer, False)
            layer_parent.insertLayer(0, layer)
            # layer_parent.addLayer(layer)

            current_dir = os.path.dirname(os.path.abspath(__file__))
            qml_file_path = os.path.join(current_dir, "qml", "danger_level.qml")
            layer.loadNamedStyle(qml_file_path)

            # TODO: disambiguity dialog
            dlg = AmbiguityDialog(self.iface)
            ambiguous_features = []

            for feature in layer.getFeatures():
                # TODO: depending on the matrix of the process!!
                if feature["Tipo di pericolo"] in [1004]:
                    print("AMBIGUO")
                    ambiguous_features.append(feature)

            if dlg.exec_():
                pass

        # Cycle all features in danger layer
        # by process, create a list of the ambiguous ones with featureid
        # populate list where to select the danger_type

    def do_help(self):
        webbrowser.open("https://opengisch.github.io/pzp/")


class PluginOptionsFactory(QgsOptionsWidgetFactory):
    def __init__(self):
        super().__init__()

    def icon(self):
        return QIcon("icons/my_plugin_icon.svg")

    def createWidget(self, parent):
        return ConfigOptionsPage(parent)


class ConfigOptionsPage(QgsOptionsPageWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
