from qgis.core import QgsFeature, QgsProject, QgsRelation, QgsVectorLayer
from qgis.gui import QgsAttributeEditorContext
from qgis.PyQt.QtCore import Qt
from qgis.testing import start_app, unittest

from pzp.calculation import CalculationDialog

start_app()


class TestCalculation(unittest.TestCase):

    def test_Calculation(self):
        
        self.assertTrue(False)

