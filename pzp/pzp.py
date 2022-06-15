import os

from qgis.core import QgsProject
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from pzp import utils


class PZP:
    def __init__(self, iface):
        self.iface = iface
        self.toolbar = None

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
        self.toolbar.addSeparator()
        self.toolbar.addAction(
            self.create_action("settings.png", "Impostazioni", self.do_open_settings)
        )

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

    def do_start_project(self):
        project = QgsProject.instance()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        project.read(os.path.join(dir_path, "data", "PN_MandatoPZP_UCA_MN95+WMS.qgz"))

    @utils.check_project()
    def do_check_geometries(self):
        pass

    @utils.check_project()
    def do_calculate_zones(self):
        pass

    def do_open_settings(self):
        pass
