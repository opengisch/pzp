import pytest
from qgis.core import QgsApplication
from qgis.testing import start_app

from pzp.processing.provider import Provider

start_app()


@pytest.fixture(scope="module")
def processing_provider():
    print("\n [INFO] Setting up test_provider_load")
    _provider = Provider()  # Processing provider
    QgsApplication.processingRegistry().addProvider(_provider)
    yield _provider

    print(" [INFO] Tearing down test_provider_load")
    QgsApplication.processingRegistry().removeProvider(_provider)


@pytest.mark.basic
def test_provider_load(processing_provider):
    print(" [INFO] Validating provider load...")
    assert "PZP_UTILS" in [provider.name() for provider in QgsApplication.processingRegistry().providers()]
