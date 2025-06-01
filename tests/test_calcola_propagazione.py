import pytest
from qgis.core import QgsProject
from qgis.testing import start_app
from qgis.testing.mocked import get_iface

from pzp.calculation import PropagationTool
from tests.utils import get_data_path

start_app()


@pytest.fixture(scope="module", autouse=True)
def initialize_processing():
    print("\nINFO: Setting up processing")
    from processing.core.Processing import Processing

    Processing.initialize()


@pytest.fixture(scope="module")
def qgis_projects_to_test():
    print("\nINFO: Get layer copy")
    return [
        str(get_data_path("caduta_sassi_semplice.qgz", "caduta_sassi")),
        str(get_data_path("caduta_sassi_vigne.qgz", "caduta_sassi")),
    ]


@pytest.fixture(scope="module")
def plugin_instance():
    print("\nINFO: Get plugin instance")
    from pzp import PZP

    plugin = PZP(get_iface())  # Initializes and registers processing provider
    yield plugin

    print(" [INFO] Tearing down plugin instance")
    plugin.unload_provider()


@pytest.mark.flusso_detrito
def test_calcola_propagazione(plugin_instance, qgis_projects_to_test):
    print(" [INFO] Validating calcola propagazione...")

    def clear_project():
        project.layerTreeRoot().clear()
        assert len(project.layerTreeRoot().children()) == 0

    # Test each project given
    for project_path in qgis_projects_to_test:
        print(f" [INFO] Testing project {project_path}...")
        project = QgsProject.instance()
        project.read(project_path)

        assert len(project.layerTreeRoot().children()) > 0
        main_group = project.layerTreeRoot().findGroup("Caduta sassi o blocchi")
        assert main_group
        subgroups = main_group.findGroups()

        tool = PropagationTool(get_iface(), main_group)
        tool.run(force=True)

        # There should be a new group for the intensity layers
        assert len(subgroups) == len(main_group.findGroups()) - 1

        intensity_group = main_group.findGroup("Intensità (con filtri x visualizzazione scenari)")
        assert intensity_group
        assert intensity_group.children()
        obtained_layer = intensity_group.children()[0]  # Get main intensity layer
        assert obtained_layer.layer().isValid()
        assert obtained_layer.layer().featureCount() > 0

        expected_layer = project.mapLayersByName("expected_intensity_layer")
        assert expected_layer
        expected_layer = expected_layer[0]
        assert expected_layer.isValid()
        assert expected_layer.featureCount() > 0

        # Compare obtained and expected layers
        obtained_periodo_di_ritorno = [feature["periodo_ritorno"] for feature in obtained_layer.layer().getFeatures()]
        expected_periodo_di_ritorno = [feature["periodo_ritorno"] for feature in expected_layer.getFeatures()]
        print(f" [INFO] Obtained periodo di retorno: {obtained_periodo_di_ritorno}")

        assert obtained_periodo_di_ritorno == expected_periodo_di_ritorno

        clear_project()
