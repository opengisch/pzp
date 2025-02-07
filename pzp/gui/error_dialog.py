from qgis.core import QgsApplication
from qgis.PyQt.QtWidgets import QApplication, QDialog

from pzp.utils import utils

FORM_CLASS = utils.get_ui_class(str(utils.get_plugin_path() / "ui" / "error_dialog.ui"))


class ErrorDialog(QDialog, FORM_CLASS):
    def __init__(self, title, subtitle="", description="", traceback="", parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self._title = title
        self._subtitle = subtitle
        self._description = description
        self._traceback = traceback

        self.lbl_title.setText(title)
        self.lbl_subtitle.setText(subtitle)
        self.lbl_description.setText(description)
        self.txt_traceback.setText(traceback)

        self.btn_copy.setIcon(QgsApplication.getThemeIcon("/mActionEditCopy.svg"))
        self.btn_copy.clicked.connect(self._copy_to_clipboard)

    def _copy_to_clipboard(self):
        QApplication.clipboard().setText(
            f"{self._title}\n{self._subtitle}\n\n{self._description}\n\n\n{self._traceback}"
        )
