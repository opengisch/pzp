import pytest
from qgis.core import (
    Qgis,
    QgsApplication,
    QgsFeature,
    QgsFeatureRequest,
    QgsGeometry,
    QgsProcessingContext,
    QgsVectorLayer,
    QgsWkbTypes,
)
from qgis.testing import start_app

from pzp.processing.merge_by_area import MergeByArea
from pzp.processing.merge_by_form_factor import MergeByFormFactor
from pzp.processing.provider import Provider
from pzp.utils.utils import keep_polygonal_parts

start_app()
import processing

SQUARE = "POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))"
SMALL = "POLYGON((10 0, 10.5 0, 10.5 1, 10 1, 10 0))"  # 0.5 m2, to be merged into SQUARE
COLLAPSED = "POLYGON((0 0, 0 -10, 0 0))"  # Zero-area polygon touching SQUARE

if Qgis.QGIS_VERSION_INT >= 33000:
    POLYGON_TYPE = Qgis.GeometryType.Polygon
else:
    POLYGON_TYPE = QgsWkbTypes.GeometryType.PolygonGeometry

if Qgis.QGIS_VERSION_INT >= 33600:
    NO_GEOMETRY_CHECK = Qgis.InvalidGeometryCheck.NoCheck
else:
    NO_GEOMETRY_CHECK = QgsFeatureRequest.InvalidGeometryCheck.GeometryNoCheck


@pytest.fixture(scope="module", autouse=True)
def initialize_processing():
    from processing.core.Processing import Processing

    Processing.initialize()


@pytest.fixture(scope="module")
def processing_provider():
    _provider = Provider()
    QgsApplication.processingRegistry().addProvider(_provider)
    yield _provider
    QgsApplication.processingRegistry().removeProvider(_provider)


def _create_layer(wkts):
    layer = QgsVectorLayer("Polygon?crs=EPSG:2056&field=value:integer", "input", "memory")
    features = []
    for i, wkt in enumerate(wkts):
        feature = QgsFeature(layer.fields())
        feature.setGeometry(QgsGeometry.fromWkt(wkt))
        feature["value"] = i
        features.append(feature)
    layer.dataProvider().addFeatures(features)
    return layer


def _context():
    # The collapsed input geometry is invalid on purpose
    context = QgsProcessingContext()
    context.setInvalidGeometryCheck(NO_GEOMETRY_CHECK)
    return context


def _assert_only_polygons(layer):
    for feature in layer.getFeatures():
        assert feature.geometry().type() == POLYGON_TYPE
        assert feature.geometry().area() > 0


@pytest.mark.basic
def test_keep_polygonal_parts():
    square = QgsGeometry.fromWkt(SQUARE)

    # With GEOS >= 3.15 this is a GeometryCollection containing a LineString
    combined = square.combine(QgsGeometry.fromWkt(COLLAPSED))

    result = keep_polygonal_parts(combined)
    assert result.type() == POLYGON_TYPE
    assert result.area() == pytest.approx(100)

    # Non-collections are returned untouched
    assert keep_polygonal_parts(square).equals(square)


@pytest.mark.basic
@pytest.mark.parametrize(
    "algorithm, parameters",
    [
        ("pzp_utils:merge_by_area", {"MODE": MergeByArea.MODE_BOUNDARY}),
        (
            "pzp_utils:merge_by_form_factor",
            {"MODE": MergeByFormFactor.MODE_BOUNDARY, "FORM_FACTOR": 0.6, "AREA_THRESHOLD": 10},
        ),
    ],
)
def test_merge_with_collapsed_geometry(processing_provider, algorithm, parameters):
    layer = _create_layer([SQUARE, SMALL, COLLAPSED])

    context = _context()
    result = processing.run(algorithm, {"INPUT": layer, "OUTPUT": "memory:", **parameters}, context=context)
    _assert_only_polygons(result["OUTPUT"])

    # Used to fail with "Could not add feature with geometry type LineString to layer of type Polygon"
    result = processing.run("native:multiparttosingleparts", {"INPUT": result["OUTPUT"], "OUTPUT": "memory:"})
    output = result["OUTPUT"]

    _assert_only_polygons(output)
    assert output.featureCount() == 1  # SMALL merged into SQUARE, COLLAPSED removed
    assert next(output.getFeatures()).geometry().area() == pytest.approx(100.5)
