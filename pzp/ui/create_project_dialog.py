from qgis.PyQt.QtWidgets import QDialog

from pzp import domains
from pzp.utils import get_ui_class

FORM_CLASS = get_ui_class("create_project.ui")


class CreateProjectDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        for process in domains.PROCESS_TYPES.items():
            self.process_cbox.addItem(process[1], process)
