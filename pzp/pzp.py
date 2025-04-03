import os
import webbrowser

from qgis.core import (
    QgsApplication,
    QgsExpressionContextUtils,
    QgsIconUtils,
    QgsLayerDefinition,
    QgsLayerTreeGroup,
    QgsLayerTreeNode,
    QgsProject,
)
from qgis.PyQt.QtCore import QObject, Qt
from qgis.PyQt.QtWidgets import QAction, QMenu, QMessageBox, QToolButton

from pzp import a_b
from pzp.add_process import AddProcessDialog
from pzp.calculation import CalculationTool, PropagationTool
from pzp.check_dock import CheckResultsDock
from pzp.gui.settings_dialog import SettingsDialog
from pzp.no_impact import ToolNessunImpatto
from pzp.processing.provider import Provider
from pzp.utils import utils
from pzp.utils.override_cursor import OverrideCursor
from pzp.utils.settings import PLUGIN_NAME, Settings


class PZP(QObject):
    PROPERTY_LAYER_NODE = "layer_node"
    PROPERTY_QLR_FILENAME = "qlr_filename"

    QLR_FILENAME_MAPPE_BASE = "mappe_base"
    QLR_FILENAME_DATI_BASE_WMS = "dati_base_wms"
    QLR_FILENAME_DATI_BASE_WFS = "dati_base_wfs"

    def __init__(self, iface):
        super().__init__(None)
        self.iface = iface
        self.toolbar = None

        self._provider = Provider()  # Processing provider

        self.layerDefinitionProjectMappeBase = None
        self.layerDefinitionProjectDatiBaseWMF = None
        self.layerDefinitionProjectDatiBaseWFS = None
        self.initProcessing()

    def initGui(self):
        self.toolbar = self.iface.addToolBar(PLUGIN_NAME)
        self.toolbar.setObjectName("PZPToolbar")
        self.toolbar.setToolTip(f"{PLUGIN_NAME} Toolbar")

        landslide_action = self.create_action("landslide.png", "Aggiungi processo", self.do_add_process)
        self.toolbar.addAction(landslide_action)
        self.iface.addPluginToMenu(PLUGIN_NAME, landslide_action)

        self.init_geodata_menu()

        no_impact_action = self.create_action(
            "no_impact.png",
            "Aggiungi zone nessun impatto",
            self.do_calculate_no_impact,
        )
        self.toolbar.addAction(no_impact_action)
        self.iface.addPluginToMenu(PLUGIN_NAME, no_impact_action)

        propagation_action = self.create_action(
            "propagation.png", "Calcola propagazione", self.do_calculate_propagation
        )
        self.toolbar.addAction(propagation_action)
        self.iface.addPluginToMenu(PLUGIN_NAME, propagation_action)

        calculate_zones_action = self.create_action("process.png", "Calcola zone di pericolo", self.do_calculate_zones)
        self.toolbar.addAction(calculate_zones_action)
        self.iface.addPluginToMenu(PLUGIN_NAME, calculate_zones_action)

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

        settings_action = self.create_action("gear.png", "Ipostazioni", self.do_settings)
        self.toolbar.addAction(settings_action)
        self.iface.addPluginToMenu(PLUGIN_NAME, settings_action)

        help_action = self.create_action("help.png", "Aiuto", self.do_help)
        self.toolbar.addAction(help_action)
        self.iface.addPluginToMenu(PLUGIN_NAME, help_action)

        menu_pzp = self.iface.mainWindow().getPluginMenu(PLUGIN_NAME)
        menu_pzp.setIcon(utils.get_icon("landslide.png"))

    def initProcessing(self):
        """Create the Processing provider"""
        QgsApplication.processingRegistry().addProvider(self._provider)

    def init_geodata_menu(self):
        menuMappeBase = self.init_geodata_menu_qlr(self.QLR_FILENAME_MAPPE_BASE, "world.png", "Aggiungi mappe base")
        menuDatiBaseWMS = self.init_geodata_menu_qlr(
            self.QLR_FILENAME_DATI_BASE_WMS, "ruler.png", "Aggiungi dati base WMS"
        )
        menuDatiBaseWFS = self.init_geodata_menu_qlr(
            self.QLR_FILENAME_DATI_BASE_WFS, "ruler.png", "Aggiungi dati base WFS"
        )

        add_basemaps_action = self.create_action("world.png", "Aggiungi mappe base", self.do_add_basemaps)
        add_basemaps_action.setMenu(menuMappeBase)

        add_basedatawms_action = self.create_action("ruler.png", "Aggiungi dati base WMS", self.do_add_base_data_wms)
        add_basedatawms_action.setMenu(menuDatiBaseWMS)

        add_basedatawfs_action = self.create_action("ruler.png", "Aggiungi dati base WFS", self.do_add_base_data_wfs)
        add_basedatawfs_action.setMenu(menuDatiBaseWFS)

        geodata_menu = QMenu()
        geodata_menu.addAction(add_basemaps_action)
        geodata_menu.addAction(add_basedatawms_action)
        geodata_menu.addAction(add_basedatawfs_action)

        toolButton = QToolButton()
        toolButton.setDefaultAction(add_basemaps_action)
        toolButton.setMenu(geodata_menu)
        toolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.toolbar.addWidget(toolButton)

    def init_geodata_menu_qlr(self, qlr_filename, icon_name, menu_name):
        menu_pzp = self.iface.mainWindow().getPluginMenu(PLUGIN_NAME)
        placeholderMenu = self.create_submenu(icon_name, menu_name, menu_pzp)
        placeholderMenu.setProperty(self.PROPERTY_QLR_FILENAME, qlr_filename)
        placeholderMenu.aboutToShow.connect(self.placeholderMenuAboutToShow)
        return placeholderMenu

    def walk_group(self, group, parent_menu, icon=None):
        if icon is None:
            icon = "group.svg"

        for subgroup in group.findGroups():
            submenu = self.create_submenu(icon, subgroup.name(), parent_menu)
            self.walk_group(subgroup, submenu)

        for layer in group.findLayers():
            if layer.parent() == group:
                action = QAction(QgsIconUtils.iconForLayer(layer.layer()), layer.name(), self.iface.mainWindow())
                action.triggered.connect(self.do_add_layer_node)
                action.setProperty(self.PROPERTY_LAYER_NODE, layer)
                parent_menu.addAction(action)

        # Create action for add all in the group
        actionAddAll = self.create_action("group.svg", "Aggiungi tutto da questo gruppo", self.do_add_layer_node)
        actionAddAll.setProperty(self.PROPERTY_LAYER_NODE, group)
        font = actionAddAll.font()
        font.setBold(True)
        actionAddAll.setFont(font)
        parent_menu.addAction(actionAddAll)

        return parent_menu

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

        self.unload_provider()

        Settings.unload()

    def unload_provider(self):
        QgsApplication.processingRegistry().removeProvider(self._provider)

    def do_add_process(self):
        dlg = AddProcessDialog(self.iface)
        dlg.exec_()

    def do_add_basemaps(self):
        with OverrideCursor(Qt.WaitCursor):
            utils.load_qlr_layer(self.QLR_FILENAME_MAPPE_BASE)

    def do_add_base_data_wms(self):
        with OverrideCursor(Qt.WaitCursor):
            utils.load_qlr_layer(self.QLR_FILENAME_DATI_BASE_WMS)

    def do_add_base_data_wfs(self):
        with OverrideCursor(Qt.WaitCursor):
            utils.load_qlr_layer(self.QLR_FILENAME_DATI_BASE_WFS)

    def do_add_layer_node(self):
        with OverrideCursor(Qt.WaitCursor):
            action = self.sender()
            layerNode = action.property(self.PROPERTY_LAYER_NODE)

            parentGroups = []
            parentGroup = layerNode.parent()
            while parentGroup and parentGroup.parent():
                parentGroups.insert(0, parentGroup)
                parentGroup = parentGroup.parent()

            if layerNode.nodeType() == QgsLayerTreeNode.NodeGroup:
                parentGroups.append(layerNode)

            projectParentGroup = QgsProject.instance().layerTreeRoot()
            for newParentGroup in parentGroups:
                groupAlreadyExists = False
                for children in projectParentGroup.children():
                    if children.name() == newParentGroup.name():
                        projectParentGroup = children
                        groupAlreadyExists = True
                        break

                if not groupAlreadyExists:
                    projectParentGroup = projectParentGroup.addGroup(newParentGroup.name())
                    projectParentGroup.setItemVisibilityChecked(newParentGroup.itemVisibilityChecked())
                    projectParentGroup.setExpanded(newParentGroup.isExpanded())

            # We reached the inserting group -> add all subgroups and layers
            # For group types...
            if layerNode.nodeType() == QgsLayerTreeNode.NodeGroup:
                self.do_add_group_recursive(projectParentGroup, layerNode)

            # ... and for layer types
            else:
                for children in projectParentGroup.children():
                    if children.name() == layerNode.name():
                        # Already existing
                        return

                # Sublayer
                newLayer = layerNode.layer().clone()
                newLayerNode = projectParentGroup.addLayer(newLayer)
                newLayerNode.setItemVisibilityChecked(layerNode.itemVisibilityChecked())
                newLayerNode.setExpanded(layerNode.isExpanded())
                QgsProject.instance().layerStore().addMapLayer(newLayer)

    def do_add_group_recursive(self, projectParentGroup, group):
        for layerNode in group.children():
            existingTreeElement = None
            for children in projectParentGroup.children():
                if children.name() == layerNode.name():
                    existingTreeElement = children
                    break

            # Sublayer
            if layerNode.nodeType() == QgsLayerTreeNode.NodeLayer and existingTreeElement is None:
                newLayer = layerNode.layer().clone()
                newLayerNode = projectParentGroup.addLayer(newLayer)
                newLayerNode.setItemVisibilityChecked(layerNode.itemVisibilityChecked())
                newLayerNode.setExpanded(layerNode.isExpanded())
                QgsProject.instance().layerStore().addMapLayer(newLayer)
                continue

            # Subgroup
            if existingTreeElement is None:
                existingTreeElement = projectParentGroup.addGroup(layerNode.name())
                projectParentGroup.setItemVisibilityChecked(layerNode.itemVisibilityChecked())
                existingTreeElement.setExpanded(layerNode.isExpanded())
            self.do_add_group_recursive(existingTreeElement, layerNode)

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
            tool = PropagationTool(self.iface, current_node)
            with OverrideCursor(Qt.WaitCursor):
                tool.run()
        else:
            utils.push_error("Selezionare il gruppo che contiene il processo", 3)

    def do_calculate_zones(self):
        # Get selected group
        current_node = self.iface.layerTreeView().currentNode()
        if isinstance(current_node, QgsLayerTreeGroup):
            tool = CalculationTool(self.iface, current_node)
            with OverrideCursor(Qt.WaitCursor):
                tool.run()
        else:
            utils.push_error("Selezionare il gruppo che contiene il processo", 3)

    def do_calculate_no_impact(self):
        # Get selected group
        current_node = self.iface.layerTreeView().currentNode()
        if isinstance(current_node, QgsLayerTreeGroup):
            tool = ToolNessunImpatto(current_node)
            with OverrideCursor(Qt.WaitCursor):
                tool.run()
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

    def do_settings(self):
        settingsDialog = SettingsDialog()
        settingsDialog.exec_()

    def do_help(self):
        webbrowser.open("https://opengisch.github.io/pzp/")

    def placeholderMenuAboutToShow(self):
        placeholderMenu = self.sender()
        qlr_filename = placeholderMenu.property(self.PROPERTY_QLR_FILENAME)

        project = None
        if self.QLR_FILENAME_MAPPE_BASE == qlr_filename:
            project = self.layerDefinitionProjectMappeBase
        elif self.QLR_FILENAME_DATI_BASE_WMS == qlr_filename:
            project = self.layerDefinitionProjectDatiBaseWMF
        elif self.QLR_FILENAME_DATI_BASE_WFS == qlr_filename:
            project = self.layerDefinitionProjectDatiBaseWFS
        else:
            QMessageBox.critical(self, "Unknown qlr filename", f"Unknown qlr filename {qlr_filename}")

        # Project already loaded
        if project is not None:
            return

        with OverrideCursor(Qt.WaitCursor):
            current_dir = os.path.dirname(os.path.abspath(__file__))
            qlr_file_path = os.path.join(current_dir, "qlr", f"{qlr_filename}.qlr")

            project = QgsProject()
            layerTreeRoot = project.layerTreeRoot()

            QgsLayerDefinition.loadLayerDefinition(qlr_file_path, project, layerTreeRoot)

            if self.QLR_FILENAME_MAPPE_BASE == qlr_filename:
                self.layerDefinitionProjectMappeBase = project
            elif self.QLR_FILENAME_DATI_BASE_WMS == qlr_filename:
                self.layerDefinitionProjectDatiBaseWMF = project
            elif self.QLR_FILENAME_DATI_BASE_WFS == qlr_filename:
                self.layerDefinitionProjectDatiBaseWFS = project

            for group in layerTreeRoot.findGroups():
                # Only one root group per .qlr is supported (thus return)
                return self.walk_group(group, placeholderMenu)
