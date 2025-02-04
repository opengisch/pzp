import pytest
from qgis.core import QgsMapLayer, QgsProject, QgsVectorLayer
from qgis.testing import start_app
from qgis.testing.mocked import get_iface

from pzp.calculation import CalculationDialog
from tests.utils import get_copy_path

start_app()


@pytest.fixture(scope="module", autouse=True)
def initialize_processing():
    print("\nINFO: Setting up processing")
    from processing.core.Processing import Processing

    Processing.initialize()


@pytest.fixture(scope="module")
def flusso_detrito_layer():
    print("\nINFO: Get layer copy")
    yield QgsVectorLayer(
        str(get_copy_path("riali_gambarogno_1200.gpkg")) + "|layername=Intensità completa", "layer", "ogr"
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
def test_flusso_detrito(plugin_instance, flusso_detrito_layer):
    print(" [INFO] Validating flusso detrito...")
    process_type = 1200

    assert flusso_detrito_layer.isValid()

    # Add layer to project so that Processing can find it and use it
    QgsProject.instance().addMapLayer(flusso_detrito_layer)

    dlg = CalculationDialog(get_iface(), None)
    pericolo_layer = dlg.do_exec(process_type, flusso_detrito_layer)

    assert isinstance(pericolo_layer, QgsMapLayer)
    assert pericolo_layer.featureCount() == 101

    # TODO: Compare features per category

    # TODO: Compare geometries
