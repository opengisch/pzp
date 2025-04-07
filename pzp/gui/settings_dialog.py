from qgis.PyQt.QtWidgets import QDialog

from pzp.utils import utils
from pzp.utils.settings import Settings

FORM_CLASS = utils.get_ui_class(str(utils.get_plugin_path() / "ui" / "settings_dialog.ui"))


class SettingsDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.mergeFormFactorSpinBox.setToolTip(self.mergeFormFactorLabel.toolTip())
        self.mergeFormFactorSpinBox.setValue(Settings().merge_form_factor.value())

    def accept(self):
        Settings().merge_form_factor.setValue(self.mergeFormFactorSpinBox.value())
        super(SettingsDialog, self).accept()
