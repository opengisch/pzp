from functools import partial

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QDockWidget, QHeaderView, QPushButton, QTableWidgetItem

from pzp.utils import utils

FORM_CLASS = utils.get_ui_class(str(utils.get_plugin_path() / "ui" / "checker.ui"))


class CheckResultsDock(QDockWidget, FORM_CLASS):
    """Creates a DockWidget where show the results of the checks."""

    result_parent = None

    def __init__(self, iface, parent=None):
        QDockWidget.__init__(self, parent)

        self.setupUi(self)
        self.iface = iface
        self.message_bar = self.iface.messageBar()

        self.create_columns()

        self.checks = {}
        self.populate_table()
        self.run_all_checks_button.clicked.connect(self.run_all_checks)

    def create_columns(self):
        self.table.setColumnCount(4)
        headers = ["Nome", "Descrizione", "Esegui", "Risultato"]
        self.table.setHorizontalHeaderLabels(headers)

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

    def populate_table(self):
        for name in ["Poligoni dupplicati", "Sovrapposizioni"]:
            check = name
            self._append_row((name, "descrizione"))
            self.table.resizeColumnsToContents()

            self.checks[name] = check

    def _append_row(self, row):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        item = QTableWidgetItem(row[0])
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.table.setItem(row_position, 0, item)
        item = QTableWidgetItem(row[1])
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.table.setItem(row_position, 1, item)
        button = QPushButton(QIcon(utils.get_icon("play.png")), "")
        button.setObjectName(row[0])
        button.clicked.connect(partial(self.on_button_clicked, row[0]))
        self.table.setCellWidget(row_position, 2, button)
        item = QTableWidgetItem("")
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.table.setItem(row_position, 3, item)

    def run_all_checks(self):
        # Clean result column
        for i in range(self.table.rowCount()):
            self.table.item(i, 3).setText("")
            self.table.item(i, 3).setIcon(QIcon())

        for i, name in enumerate(["Poligoni dupplicati", "Sovrapposizioni"]):
            self.run_check(name)

    def on_button_clicked(self, name):
        self.run_check(name, True)

    def run_check(self, name, do_select=False):
        self.add_result(name, True, 0)

    def add_result(self, name, is_correct, message):
        """Add a parent result"""
        found_item = self.table.findItems(name, Qt.MatchExactly)[0]
        result_item = self.table.item(found_item.row(), 3)
        if is_correct:
            result_item.setText("OK")
            result_item.setIcon(QIcon(utils.get_icon("green_check.png")))
        else:
            result_item.setText("NO ({})".format(message))
            result_item.setIcon(QIcon(utils.get_icon("red_cross.png")))

    def select_features(self, id_list):
        pass
