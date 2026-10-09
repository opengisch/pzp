import pytest
from qgis.core import QgsExpressionContextUtils, QgsMapLayer, QgsProject, QgsVectorLayer
from qgis.testing import start_app
from qgis.testing.mocked import get_iface

from pzp.calculation import CalculationTool
from tests.utils import get_copy_path, get_data_path

start_app()
import processing

COMPARED_ATTRIBUTES = [
    # 'fid',
    "commento",
    "periodo_ritorno",
    "classe_intensita",
    "proc_parz",
    "fonte_proc",
    "grado_pericolo",
    "matrice",
    # 'layer',
]

# Same threshold under which the plugin considers geometries negligible (see merge_by_area)
MAX_AREA_DIFFERENCE = 1  # m2


def _match_changed_features(expected_layer, obtained_layer, attributes, max_area_difference):
    """
    Pairs each expected feature with an obtained feature having the same attributes and
    the smallest area of symmetric difference. Returns the list of area differences.
    """
    obtained_features = list(obtained_layer.getFeatures())
    assert len(obtained_features) == expected_layer.featureCount()

    differences = []
    for expected in expected_layer.getFeatures():
        candidates = [
            (expected.geometry().symDifference(obtained.geometry()).area(), i)
            for i, obtained in enumerate(obtained_features)
            if all(expected[attribute] == obtained[attribute] for attribute in attributes)
        ]
        assert candidates, f"No obtained feature with the attributes of expected feature {expected.attributes()}"

        difference, index = min(candidates)
        assert (
            difference <= max_area_difference
        ), f"Area difference of {difference} m2 for feature {expected.attributes()}"

        differences.append(round(difference, 6))
        obtained_features.pop(index)

    return differences


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


@pytest.fixture(scope="module")
def project():
    print("\nINFO: Make sure the project has no layers")
    project = QgsProject.instance()

    def clear_project():
        project.layerTreeRoot().clear()
        assert len(project.layerTreeRoot().children()) == 0

    clear_project()
    yield project
    clear_project()


@pytest.mark.flusso_detrito
def test_flusso_detrito(plugin_instance, flusso_detrito_layer, flusso_detrito_expected_layer, project):
    print(" [INFO] Validating flusso di detrito...")
    process_type = 1200

    # Make sure we have valid input/expected data layers
    assert flusso_detrito_layer.isValid()
    assert flusso_detrito_layer.featureCount() == 268
    assert flusso_detrito_expected_layer.isValid()
    assert flusso_detrito_expected_layer.featureCount() == 101

    # Add layer to project so that Processing can find it and use it
    project.addMapLayer(flusso_detrito_layer)

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
            "COMPARE_ATTRIBUTES": COMPARED_ATTRIBUTES,  # To test only geometries, pass empty list here
            "MATCH_TYPE": 1,  # 0: Exact match, 1: Tolerant match
            "UNCHANGED": "TEMPORARY_OUTPUT",
            "ADDED": "TEMPORARY_OUTPUT",
            "DELETED": "TEMPORARY_OUTPUT",
        },
    )
    assert isinstance(layer_comparison["UNCHANGED"], QgsMapLayer)
    assert isinstance(layer_comparison["ADDED"], QgsMapLayer)
    assert isinstance(layer_comparison["DELETED"], QgsMapLayer)

    unchanged = layer_comparison["UNCHANGED"].featureCount()
    differences = _match_changed_features(
        layer_comparison["DELETED"], layer_comparison["ADDED"], COMPARED_ATTRIBUTES, MAX_AREA_DIFFERENCE
    )
    print(f" [INFO] {unchanged} unchanged features, area differences of changed features: {differences}")
    assert unchanged + len(differences) == 101

    # Test expected groups
    assert len(project.layerTreeRoot().children()) == 2  # Group + layer intensity
    groups = project.layerTreeRoot().findGroups()
    assert len(groups) == 1
    group = groups[0]
    assert group.name().startswith("Pericolo 1200")
    assert len(group.children()) == 7

    # Test filtered layers are there
    # 'MAG-018', 'MAG-019', 'MAG-020', 'MAG-021', 'MAG-022', 'MAG-023'
    idx = pericolo_layer.fields().indexOf("fonte_proc")
    sources = pericolo_layer.uniqueValues(idx) if idx != -1 else []
    assert len(sources) == 6
    names = {layer.name() for layer in group.children()}
    filtered_names = names.intersection(sources)
    assert len(filtered_names) == 6
    assert "Pericolo" in names  # The unfiltered layer is there as well
