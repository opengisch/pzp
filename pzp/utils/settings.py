from qgis.core import QgsSettingsEntryDouble, QgsSettingsTree

PLUGIN_NAME = "PZP"


class Settings:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(Settings, cls).__new__(cls)

            settings_node = QgsSettingsTree.createPluginTreeNode(pluginName=PLUGIN_NAME)

            cls.merge_form_factor = QgsSettingsEntryDouble("merge_form_factor", settings_node, 0.0)

        return cls.instance

    @staticmethod
    def unload():
        QgsSettingsTree.unregisterPluginTreeNode(PLUGIN_NAME)
