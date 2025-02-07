import pytest
from qgis.core import QgsApplication
from qgis.testing import start_app
from qgis.testing.mocked import get_iface

start_app()


@pytest.fixture(scope="module")
def plugin_instance():
    print("\nINFO: Get plugin instance")
    from pzp import PZP

    plugin = PZP(get_iface())  # Initializes and registers processing provider
    yield plugin

    print(" [INFO] Tearing down plugin instance")
    plugin.unload_provider()


@pytest.mark.basic
def test_plugin_load(plugin_instance):
    print(" [INFO] Validating plugin load...")
    assert plugin_instance.iface is not None
    assert "PZP_UTILS" in [provider.name() for provider in QgsApplication.processingRegistry().providers()]
