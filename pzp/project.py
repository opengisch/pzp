import os

from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsEditorWidgetSetup,
    QgsField,
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
)
from qgis.PyQt.QtCore import QVariant

from pzp import domains, utils


def add_layers():
    root = QgsProject.instance().layerTreeRoot()
    group_pzp = root.addGroup("Pericoli naturali mandato PZP")

    layer = QgsVectorLayer(
        path="Polygon",
        baseName="Intensità",
        providerLib="memory",
    )
    layer.setCrs(QgsCoordinateReferenceSystem("EPSG:2056"))

    pr = layer.dataProvider()
    pr.addAttributes(
        [
            QgsField("Processo", QVariant.Int),
            QgsField("Probabilità", QVariant.Int),
            QgsField("Intensità", QVariant.Int),
        ]
    )
    layer.updateFields()

    setup = QgsEditorWidgetSetup(
        "ValueMap",
        {"map": {y: x for x, y in domains.PROCESS_TYPES.items()}},
    )
    layer.setEditorWidgetSetup(0, setup)

    setup = QgsEditorWidgetSetup(
        "ValueMap",
        {"map": {y: x for x, y in domains.EVENT_PROBABILITIES.items()}},
    )
    layer.setEditorWidgetSetup(1, setup)

    setup = QgsEditorWidgetSetup(
        "ValueMap",
        {"map": {y: x for x, y in domains.INTENSITIES.items()}},
    )
    layer.setEditorWidgetSetup(2, setup)

    QgsProject.instance().addMapLayer(layer, False)
    group_pzp.addLayer(layer)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    qml_file_path = os.path.join(current_dir, "qml", "intensity.qml")
    layer.loadNamedStyle(qml_file_path)

    utils.write_project_metadata("project_version", "0")  # TODO: project version

    group_basemaps = root.addGroup("Mappe base")

    urlWithParams = "contextualWMSLegend=0&crs=EPSG:2056&dpiMode=1&featureCount=10&format=image/jpeg&layers=ch.swisstopo.pixelkarte-farbe&styles=ch.swisstopo.pixelkarte-farbe&tileDimensions=Time%3Dcurrent&tileMatrixSet=2056_27&url=https://wmts.geo.admin.ch/EPSG/2056/1.0.0/WMTSCapabilities.xml?lang%3Dit"
    layer = QgsRasterLayer(urlWithParams, "Carte nazionali (colori)", "wms")

    QgsProject.instance().addMapLayer(layer, False)
    group_basemaps.addLayer(layer)
