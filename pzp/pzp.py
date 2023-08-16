import os
import webbrowser

from qgis.core import (
    QgsExpressionContextUtils,
    QgsIconUtils,
    QgsLayerDefinition,
    QgsLayerTreeGroup,
    QgsProject,
)
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QAction, QMenu, QToolButton

from pzp import a_b, no_impact, utils
from pzp.add_process import AddProcessDialog
from pzp.calculation import CalculationDialog, PropagationDialog
from pzp.check_dock import CheckResultsDock
from pzp.ui.resources import *  # noqa

PLUGIN_NAME = "PZP"


class PZP:
    def __init__(self, iface):
        self.iface = iface
        self.toolbar = None

    def initGui(self):
        self.toolbar = self.iface.addToolBar(PLUGIN_NAME)
        self.toolbar.setObjectName("PZPToolbar")
        self.toolbar.setToolTip(f"{PLUGIN_NAME} Toolbar")

        action = self.create_action("landslide.png", "Aggiungi processo", self.do_add_process)
        self.toolbar.addAction(action)
        self.iface.addPluginToMenu(PLUGIN_NAME, action)

        self.init_geodata_menu()

        action = self.create_action(
            "no_impact.png",
            "Aggiungi zone nessun impatto",
            self.do_calculate_no_impact,
        )
        self.toolbar.addAction(action)
        self.iface.addPluginToMenu(PLUGIN_NAME, action)

        action = self.create_action("propagation.png", "Calcola propagazione", self.do_calculate_propagation)
        self.toolbar.addAction(action)
        self.iface.addPluginToMenu(PLUGIN_NAME, action)

        action = self.create_action("process.png", "Calcola zone di pericolo", self.do_calculate_zones)
        self.toolbar.addAction(action)
        self.iface.addPluginToMenu(PLUGIN_NAME, action)

        a_b_menu = QMenu()
        a_b_action = self.create_action("a_b.png", "A->B", self.do_a_b)
        a_b_menu.addAction(a_b_action)
        self.iface.addPluginToMenu(PLUGIN_NAME, a_b_action)

        b_a_action = self.create_action("b_a.png", "B->A", self.do_b_a)
        a_b_menu.addAction(b_a_action)
        self.iface.addPluginToMenu(PLUGIN_NAME, b_a_action)

        toolButton = QToolButton()
        toolButton.setDefaultAction(a_b_action)
        toolButton.setMenu(a_b_menu)
        toolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.toolbar.addWidget(toolButton)

        action = self.create_action("help.png", "Aiuto", self.do_help)
        self.toolbar.addAction(action)
        self.iface.addPluginToMenu(PLUGIN_NAME, action)

        menu_pzp = self.iface.mainWindow().getPluginMenu(PLUGIN_NAME)
        menu_pzp.setIcon(utils.get_icon("landslide.png"))

    def init_geodata_menu(self):
        menuMappeBase = self.init_geodata_menu_qlr("mappe_base", "world.png")
        # self.init_geodata_menu_qlr("dati_base_wms", "ruler.png")
        # self.init_geodata_menu_qlr("dati_base_wfs", "ruler.png")

        add_basemaps_action = self.create_action("world.png", "Aggiungi mappe base", self.do_add_basemaps)
        add_basemaps_action.setMenu(menuMappeBase)

        geodata_menu = QMenu()
        geodata_menu.addAction(add_basemaps_action)
        geodata_menu.addAction(self.create_action("ruler.png", "Aggiungi dati base WMS", self.do_add_base_data_wms))
        geodata_menu.addAction(self.create_action("ruler.png", "Aggiungi dati base WFS", self.do_add_base_data_wfs))

        toolButton = QToolButton()
        toolButton.setDefaultAction(add_basemaps_action)
        toolButton.setMenu(geodata_menu)
        toolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.toolbar.addWidget(toolButton)

    def init_geodata_menu_qlr(self, qlr_filename, icon_name):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        qlr_file_path = os.path.join(current_dir, "qlr", f"{qlr_filename}.qlr")

        layersDefinitionProject = QgsProject()
        layerTreeRoot = layersDefinitionProject.layerTreeRoot()

        QgsLayerDefinition.loadLayerDefinition(qlr_file_path, layersDefinitionProject, layerTreeRoot)

        menu_pzp = self.iface.mainWindow().getPluginMenu(PLUGIN_NAME)

        for group in layerTreeRoot.findGroups():
            # Only one root group per .qlr is supported
            return self.walk_group(group, menu_pzp, icon_name)

    def walk_group(self, group, parent_menu, icon=None):
        print(f"Group: {group.name()}")

        if icon is None:
            icon = "group.svg"

        submenu = self.create_submenu(icon, group.name(), parent_menu)

        for subgroup in group.findGroups():
            self.walk_group(subgroup, submenu)

        for layer in group.findLayers():
            if layer.parent() == group:
                print(f"Layer: {layer.name()}")

                action = QAction(QgsIconUtils.iconForLayer(layer.layer()), layer.name(), self.iface.mainWindow())
                submenu.addAction(action)

        # Create action for add all in the group
        actionAddAll = self.create_action("group.svg", "Aggiungi tutto da questo gruppo", self.do_add_basemaps)
        font = actionAddAll.font()
        font.setBold(True)
        actionAddAll.setFont(font)
        submenu.addAction(actionAddAll)

        return submenu

    def create_action(self, icon, name, callback):
        action = QAction(utils.get_icon(icon), name, self.iface.mainWindow())
        action.triggered.connect(callback)
        return action

    def create_submenu(self, icon, name, parent_menu):
        submenu = parent_menu.addMenu(name)
        submenu.setIcon(utils.get_icon(icon))
        return submenu

    def unload(self):
        # Clear PZP menu
        menu_pzp = self.iface.mainWindow().getPluginMenu(PLUGIN_NAME)
        menu_pzp.clear()

        toolbar_actions = self.toolbar.actions()
        for action in toolbar_actions:
            self.toolbar.removeAction(action)
        del self.toolbar

    def do_add_process(self):
        dlg = AddProcessDialog(self.iface)
        with utils.OverrideCursor(Qt.WaitCursor):
            dlg.exec_()

    def do_add_basemaps(self):
        with utils.OverrideCursor(Qt.WaitCursor):
            utils.load_qlr_layer("mappe_base")

    def do_add_base_data_wms(self):
        with utils.OverrideCursor(Qt.WaitCursor):
            utils.load_qlr_layer("dati_base_wms")

    def do_add_base_data_wfs(self):
        with utils.OverrideCursor(Qt.WaitCursor):
            utils.load_qlr_layer("dati_base_wfs")

    def do_check_geometries(self):
        self.checks_dock = CheckResultsDock(self.iface)

        self.checks_dock.setObjectName("CheckResultsDock")
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.checks_dock)
        self.checks_dock.setVisible(True)
        self.checks_dock.show()

    def do_calculate_propagation(self):
        # Get selected group
        current_node = self.iface.layerTreeView().currentNode()
        if isinstance(current_node, QgsLayerTreeGroup):
            # TODO: Check we have all the layers in the group
            dlg = PropagationDialog(self.iface, current_node)
            with utils.OverrideCursor(Qt.WaitCursor):
                dlg.exec_()
        else:
            utils.push_error("Selezionare il gruppo che contiene il processo", 3)

    def do_calculate_zones(self):
        # Get selected group
        current_node = self.iface.layerTreeView().currentNode()
        if isinstance(current_node, QgsLayerTreeGroup):
            # TODO: Check we have all the layers in the group
            dlg = CalculationDialog(self.iface, current_node)
            with utils.OverrideCursor(Qt.WaitCursor):
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

    def do_a_b(self):
        layer = self.iface.activeLayer()
        if layer:
            if QgsExpressionContextUtils.layerScope(layer).variable("pzp_layer") == "danger_zones":
                a_b.a_b(layer)
                return

        utils.push_error("Selezionare il layer con le zone di pericolo", 3)

    def do_b_a(self):
        layer = self.iface.activeLayer()
        if layer:
            if QgsExpressionContextUtils.layerScope(layer).variable("pzp_layer") == "danger_zones":
                a_b.b_a(layer)
                return

        utils.push_error("Selezionare il layer con le zone di pericolo", 3)

    def do_help(self):
        webbrowser.open("https://opengisch.github.io/pzp/")
