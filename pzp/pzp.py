import os
import webbrowser

from qgis import processing
from qgis.core import QgsApplication, QgsProject
from qgis.gui import QgsOptionsPageWidget, QgsOptionsWidgetFactory
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QHBoxLayout

from pzp import domains, project, utils
from pzp.processing_provider.provider import Provider
from pzp.ui.calculation_dialog import CalculationDialog
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
                "file.png", "Inizia nuovo progetto", self.do_start_project
            )
        )
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

    def do_start_project(self):
        # project = QgsProject.instance()
        # dir_path = os.path.dirname(os.path.realpath(__file__))
        # project.read(os.path.join(dir_path, "data", "PN_MandatoPZP_UCA_MN95+WMS.qgz"))
        project.add_layers()

    @utils.check_project()
    def do_check_geometries(self):
        pass

    @utils.check_project()
    def do_calculate_zones(self):
        # TODO: check the layers and the fields needed are present
        # TODO: run algo
        # TODO: apply valuemap and styles

        dlg = CalculationDialog(self.iface)
        for process in domains.PROCESS_TYPES.items():
            dlg.process_cbox.addItem(process[1], process)

        if dlg.exec_():
            selected_process = dlg.process_cbox.currentData()
            result = processing.run(
                "pzp:danger_zones",
                {
                    "INPUT": "Intensità",
                    "PROCESS_FIELD": "Processo",
                    "PROBABILITY_FIELD": "Probabilità",
                    "INTENSITY_FIELD": "Intensità",
                    "PROCESS_TYPE": dlg.process_cbox.currentIndex(),
                    "OUTPUT": "TEMPORARY_OUTPUT",
                },
            )

            layer = result["OUTPUT"]
            layer.setName(f"Pericolo {selected_process[1]}")
            QgsProject.instance().addMapLayer(layer, True)

            current_dir = os.path.dirname(os.path.abspath(__file__))
            qml_file_path = os.path.join(current_dir, "qml", "danger_level.qml")
            layer.loadNamedStyle(qml_file_path)

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
