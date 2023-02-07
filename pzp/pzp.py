import webbrowser

from qgis.core import QgsLayerTreeGroup
from qgis.gui import QgsOptionsPageWidget, QgsOptionsWidgetFactory
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QHBoxLayout, QMenu, QToolButton

from pzp import no_impact, utils
from pzp.add_process import AddProcessDialog
from pzp.calculation import CalculationDialog
from pzp.check_dock import CheckResultsDock
from pzp.ui.resources import *  # noqa


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
                "process.png", "Calcola zone di pericolo", self.do_calculate_zones
            )
        )

        self.toolbar.addAction(
            self.create_action(
                "process.png",
                "Aggiungi zone nessun impatto",
                self.do_calculate_no_impact,
            )
        )

        self.toolbar.addAction(self.create_action("help.png", "Aiuto", self.do_help))
        self.options_factory = PluginOptionsFactory()
        self.options_factory.setTitle("PZP")
        self.iface.registerOptionsWidgetFactory(self.options_factory)

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
        self.iface.unregisterOptionsWidgetFactory(self.options_factory)

    def do_add_process(self):
        dlg = AddProcessDialog(self.iface)
        dlg.exec_()

    def do_add_basemaps(self):
        utils.load_qlr_layer("mappe_base")

    def do_add_base_data(self):
        utils.load_qlr_layer("dati_base")

    def do_check_geometries(self):
        self.checks_dock = CheckResultsDock(self.iface)

        self.checks_dock.setObjectName("CheckResultsDock")
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.checks_dock)
        self.checks_dock.setVisible(True)
        self.checks_dock.show()

    def do_calculate_zones(self):
        # Get selected group
        current_node = self.iface.layerTreeView().currentNode()
        if isinstance(current_node, QgsLayerTreeGroup):
            # TODO: Check we have all the layers in the group
            dlg = CalculationDialog(self.iface, current_node)
            dlg.exec_()
        else:
            utils.push_error("Selezionare il gruppo che contiene il processo", 3)

    def do_calculate_no_impact(self):
        # Get selected group
        current_node = self.iface.layerTreeView().currentNode()
        if isinstance(current_node, QgsLayerTreeGroup):
            # TODO: Check we have all the layers in the group
            no_impact.calculate(*no_impact.guess_params(current_node))
        else:
            utils.push_error("Selezionare il gruppo che contiene il processo", 3)

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
