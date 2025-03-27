import tempfile

import pytest
from qgis.core import QgsExpressionContextUtils, QgsLayerTreeLayer, QgsProject
from qgis.testing import start_app
from qgis.testing.mocked import get_iface

from pzp.add_process import add_process

start_app()


@pytest.fixture(scope="module", autouse=True)
def initialize_processing():
    print("\nINFO: Setting up processing")
    from processing.core.Processing import Processing

    Processing.initialize()


@pytest.fixture(scope="module")
def gpkg_dir_path():
    print("\nINFO: Get GPKG dir path")
    # The dir wil lbe created in next line, the GPKG does not exist yet
    dir_path = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
    yield dir_path.name
    dir_path.cleanup()


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
def test_add_process_caduta_sassi(plugin_instance, gpkg_dir_path, project):
    print(" [INFO] Validating add process Caduta sassi...")
    process_type = 3000

    add_process(process_type, gpkg_dir_path)

    # Test expected root group
    assert len(project.layerTreeRoot().children()) == 1  # Root group
    groups = project.layerTreeRoot().findGroups()
    assert len(groups) == 1
    group = groups[0]
    assert group.name() == "Caduta sassi o blocchi"
    assert len(group.children()) == 4  # 2 layers, 2 groups

    # Test expected children layers and groups
    count = 0
    for child in group.children():
        if isinstance(child, QgsLayerTreeLayer):
            layer = child.layer()

            if layer.name() == "Area di studio":
                count += 1
                assert QgsExpressionContextUtils.layerScope(layer).variable("pzp_layer") == "area"
                assert QgsExpressionContextUtils.layerScope(layer).variable("pzp_process") == str(process_type)
                index = layer.fields().indexOf("fonte_proc")
                assert index != -1
                ews = layer.editorWidgetSetup(index)
                assert ews.type() == "ValueRelation"
                config = ews.config()
                assert "Layer" in config
                value_relation_layer = config["Layer"]
                assert isinstance(group.findLayer(value_relation_layer), QgsLayerTreeLayer)
            elif layer.name() == "Zona sorgente (fonte processo)":
                count += 1
                assert QgsExpressionContextUtils.layerScope(layer).variable("pzp_layer") == "source_zones"
                assert QgsExpressionContextUtils.layerScope(layer).variable("pzp_process") == str(process_type)

    assert count == 2

    groups = group.findGroups()
    assert len(groups) == 2  # Propagazione, rottura
    count = 0
    for subgroup in groups:
        if subgroup.name() == "Probabilità di propagazione":
            count += 1
            assert len(subgroup.children()) == 5  # 4 filtered layers
        elif subgroup.name() == "Probabilità di rottura":
            count += 1
            assert len(subgroup.children()) == 5  # 4 filtered layers

    assert count == 2
