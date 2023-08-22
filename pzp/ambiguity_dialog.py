from qgis.core import QgsProject
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QComboBox, QDialog, QTableWidgetItem
from qgis.utils import iface

from pzp.utils.utils import get_ui_class

FORM_CLASS = get_ui_class("ambiguity.ui")


class AmbiguityDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        columns = ["Geometria", "Varianti"]
        self.table.setHorizontalHeaderLabels(columns)
        self.table.setColumnCount(len(columns))

        for i in range(3):
            self.table.insertRow(i)

            item = QTableWidgetItem(f"Geometria {i+1}")
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.table.setItem(i, 0, QTableWidgetItem(item))

            combo = QComboBox()
            for t in ["4a", "4b"]:
                combo.addItem(t)
            self.table.setCellWidget(i, 1, combo)

        self.table.cellClicked.connect(self.poldo)

    def poldo(self, a, b):
        print(a, b)

        layers = QgsProject.instance().mapLayersByName("Intensità completa")

        layers[0].selectByIds([a + 1])
        iface.actionZoomToSelected().trigger()
