import pytest
from qgis.core import Qgis

# Skip as early as possible if QGIS doesn't have the overlaps alg.
pytestmark = pytest.mark.skipif(Qgis.QGIS_VERSION_INT < 34400, reason="Tests for QGIS >= 3.44.0")

from qgis.core import (
    QgsFeatureRequest,
    QgsMapLayer,
    QgsProcessingException,
    QgsProject,
    QgsVectorLayer,
)
from qgis.testing import start_app

from pzp.utils.utils import check_inputs
from tests.utils import get_copy_path, get_data_path

start_app()
import processing


@pytest.fixture(scope="module", autouse=True)
def initialize_processing():
    print("\nINFO: Setting up processing")
    from processing.core.Processing import Processing

    Processing.initialize()


@pytest.fixture(scope="module")
def layers_to_test():
    print("\nINFO: Get intensity layers to test")
    return [
        {
            "layer": QgsVectorLayer(
                str(get_copy_path(get_data_path("riali_gambarogno_intensities.gpkg", "flusso_detritico")))
                + "|layername=Intensità completa",
                "layer",
                "ogr",
            ),
            "expected_data": {
                "check_ok": False,
                "overlap_count": 1069,
                "error_count": 2,
                "pzp_overlap_count": 2,
                "pzp_overlapping_fids": ((1317, 1316), (488, 487)),
            },
        }
    ]


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
def test_overlaps(layers_to_test, project):
    print(" [INFO] Validating overlaps in intensity layers...")

    # Make sure we have valid input/expected data layers
    assert len(layers_to_test) > 0

    count = 0
    for layer_to_test in layers_to_test:
        layer = layer_to_test["layer"]
        expected = layer_to_test["expected_data"]

        # Add layer to project so that Processing can find it and use it
        project.addMapLayer(layer)

        assert layer.isValid()
        assert layer.featureCount() > 0

        # Check that the input layer has the expected overlaps
        # (this is a general overlap count, still not refined for PZP)
        pks_idxs = layer.primaryKeyAttributes()
        pk_idx = pks_idxs[0] if len(pks_idxs) == 1 else -1
        pk_name = layer.fields().field(pk_idx).name() if len(pks_idxs) == 1 else ""

        if pk_idx != -1:
            parameters = {
                "INPUT": layer.id(),
                "UNIQUE_ID": pk_name,  # fid
                "ERRORS": "TEMPORARY_OUTPUT",  # Point layer
                "OUTPUT": "TEMPORARY_OUTPUT",  # Polygon layer
                "MIN_OVERLAP_AREA": 0,
                "TOLERANCE": 8,
            }
            try:
                results_overlaps = processing.run("native:checkgeometryoverlap", parameters)
            except (QgsProcessingException, Exception) as e:
                # May be expected if the input geometries are invalid
                print("Checking overlaps failed! Details: " + str(e))
            else:
                error_overlaps_output = results_overlaps["ERRORS"]
                assert error_overlaps_output.featureCount() == expected["overlap_count"]

        res, error_output = check_inputs("test_overlaps", layer, None, check_overlaps=True, show_error_message=False)

        # Check if we have general errors and its number
        assert res == expected["check_ok"]
        assert isinstance(error_output, QgsMapLayer)
        assert error_output.featureCount() == expected["error_count"]

        # Check that overlap error count is the same as expected
        error_output.selectByExpression("message = 'Overlapping features'")
        assert error_output.selectedFeatureCount() == expected["pzp_overlap_count"]
        error_output.removeSelection()

        # Check pairs of fids that overlap
        if pk_idx != -1:
            list_pairs = []
            overlapping_fid_field_name = f"gc_overlap_feature_{pk_name}"
            request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
            for feature in error_output.getFeatures(request):
                fid_field = feature[pk_name]
                overlapping_fid_field = feature[overlapping_fid_field_name]
                list_pairs.append((fid_field, overlapping_fid_field))

            assert set(expected["pzp_overlapping_fids"]) == set(list_pairs)

        count += 1

    assert count == len(layers_to_test)
