from qgis.core import QgsApplication
from qgis.testing import unittest, start_app
from pzp.processing.provider import Provider

start_app()


class TestProviderLoad(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\nINFO: Set up test_provider_load')
        cls.provider = Provider()  # Processing provider
        QgsApplication.processingRegistry().addProvider(cls.provider)

    def test_provider_load(self):
        print('INFO: Validating provider load...')
        self.assertIn("PZP_UTILS", [provider.name() for provider in QgsApplication.processingRegistry().providers()])

    @classmethod
    def tearDownClass(cls):
        print('INFO: Tear down test_provider_load')
        QgsApplication.processingRegistry().removeProvider(cls.provider)
