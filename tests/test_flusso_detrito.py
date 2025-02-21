import pytest
from qgis.core import QgsExpressionContextUtils, QgsMapLayer, QgsProject, QgsVectorLayer
from qgis.testing import start_app
from qgis.testing.mocked import get_iface

from pzp.calculation import CalculationTool
from tests.utils import get_copy_path, get_data_path

start_app()
import processing


@pytest.fixture(scope="module", autouse=True)
def initialize_processing():
    print("\nINFO: Setting up processing")
    from processing.core.Processing import Processing

    Processing.initialize()


@pytest.fixture(scope="module")
def flusso_detrito_layer():
    print("\nINFO: Get layer copy")
    return QgsVectorLayer(
        str(get_copy_path(get_data_path("riali_gambarogno_intensities.gpkg", "flusso_detritico")))
        + "|layername=Intensità completa",
        "layer",
        "ogr",
    )


@pytest.fixture(scope="module")
def flusso_detrito_expected_layer():
    print("\nINFO: Get read-only expected layer")
    return QgsVectorLayer(
        str(get_data_path("riali_gambarogno_zone_pericolo_expected.gpkg", "flusso_detritico"))
        + "|layername=Pericolo 1200 20250204170251",
        "expected layer",
        "ogr",
    )


@pytest.fixture(scope="module")
def plugin_instance():
    print("\nINFO: Get plugin instance")
    from pzp import PZP

    plugin = PZP(get_iface())  # Initializes and registers processing provider
    yield plugin

    print(" [INFO] Tearing down plugin instance")
    plugin.unload_provider()


@pytest.mark.flusso_detrito
def test_flusso_detrito(plugin_instance, flusso_detrito_layer, flusso_detrito_expected_layer):
    print(" [INFO] Validating flusso di detrito...")
    process_type = 1200

    # Make sure we have valid input/expected data layers
    assert flusso_detrito_layer.isValid()
    assert flusso_detrito_layer.featureCount() == 268
    assert flusso_detrito_expected_layer.isValid()
    assert flusso_detrito_expected_layer.featureCount() == 101

    # Add layer to project so that Processing can find it and use it
    QgsProject.instance().addMapLayer(flusso_detrito_layer)

    dlg = CalculationTool(get_iface(), None)
    pericolo_layer = dlg.run_with_parameters(process_type, flusso_detrito_layer)

    assert isinstance(pericolo_layer, QgsMapLayer)
    assert pericolo_layer.featureCount() == 101

    # Check post layer configurations
    options = pericolo_layer.geometryOptions()
    assert options.geometryPrecision() == 0.001
    assert options.removeDuplicateNodes()
    assert options.geometryChecks() == ["QgsIsValidCheck"]

    assert QgsExpressionContextUtils.layerScope(pericolo_layer).variable("pzp_layer") == "danger_zones"
    assert QgsExpressionContextUtils.layerScope(pericolo_layer).variable("pzp_process") == "1200"

    # Compare features per category
    statistics = processing.run(
        "qgis:statisticsbycategories",
        {
            "INPUT": pericolo_layer,
            "VALUES_FIELD_NAME": "",
            "CATEGORIES_FIELD_NAME": ["grado_pericolo"],
            "OUTPUT": "TEMPORARY_OUTPUT",
        },
    )
    statistics_layer = statistics["OUTPUT"]
    assert isinstance(statistics_layer, QgsMapLayer)
    assert statistics_layer.isValid()

    expected_features_per_group = {
        1000: 19,  # non in pericolo
        1001: 8,  # residuo
        1002: 16,  # basso
        1003: 30,  # medio
        1004: 28,  # elevato
    }
    assert statistics_layer.featureCount() == 5
    for feature in statistics_layer.getFeatures():
        assert expected_features_per_group.get(feature["grado_pericolo"], -1) == feature["count"]

    # Compare geometries and attributes (expected layer vs obtained layer)
    layer_comparison = processing.run(
        "native:detectvectorchanges",
        {
            "ORIGINAL": flusso_detrito_expected_layer,
            "REVISED": pericolo_layer,
            "COMPARE_ATTRIBUTES": [  # To test only geometries, pass empty list here
                # 'fid',
                "commento",
                "periodo_ritorno",
                "classe_intensita",
                "proc_parz",
                "fonte_proc",
                "grado_pericolo",
                "matrice",
                # 'layer',
            ],
            "MATCH_TYPE": 1,  # 0: Exact match, 1: Tolerant match
            "UNCHANGED": "TEMPORARY_OUTPUT",
            "ADDED": "TEMPORARY_OUTPUT",
            "DELETED": "TEMPORARY_OUTPUT",
        },
    )
    assert isinstance(layer_comparison["UNCHANGED"], QgsMapLayer)
    assert isinstance(layer_comparison["ADDED"], QgsMapLayer)
    assert isinstance(layer_comparison["DELETED"], QgsMapLayer)

    assert layer_comparison["UNCHANGED"].featureCount() == 101  # THe obtained layer matches the expected one
    assert layer_comparison["ADDED"].featureCount() == 0
    assert layer_comparison["DELETED"].featureCount() == 0
