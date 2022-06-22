from qgis.PyQt.QtWidgets import QDialog

from pzp.utils import get_ui_class

FORM_CLASS = get_ui_class("calculation_dialog.ui")


class CalculationDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
