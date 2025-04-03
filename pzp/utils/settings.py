from qgis.core import QgsSettingsEntryDouble

# Remove this when dropping QGIS 3.28 compatibility
qgsSettingsTreeAvailable = True
try:
    from qgis.core import QgsSettingsTree
except ImportError:
    qgsSettingsTreeAvailable = False

PLUGIN_NAME = "PZP"


class Settings:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(Settings, cls).__new__(cls)

            if qgsSettingsTreeAvailable:
                settings_node = QgsSettingsTree.createPluginTreeNode(pluginName=PLUGIN_NAME)
                cls.merge_form_factor = QgsSettingsEntryDouble("merge_form_factor", settings_node, 0.0)
            else:
                cls.merge_form_factor = QgsSettingsEntryDouble(f"plugins/{PLUGIN_NAME}/merge_form_factor", None, 0.0)

        return cls.instance

    @staticmethod
    def unload():
        if not qgsSettingsTreeAvailable:
            return

        QgsSettingsTree.unregisterPluginTreeNode(PLUGIN_NAME)
