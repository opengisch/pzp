from qgis.core import QgsProcessingProvider

from pzp.processing.apply_matrix import ApplyMatrix
from pzp.processing.danger_zones import DangerZones
from pzp.processing.fix_geometries import FixGeometries
from pzp.processing.merge_by_area import MergeByArea
from pzp.processing.merge_intensity_layers import MergeIntensityLayers
from pzp.processing.no_impact import NoImpact
from pzp.processing.propagation import Propagation
from pzp.processing.remove_by_area import RemoveByArea
from pzp.processing.remove_overlappings import RemoveOverlappings
from pzp.processing.simplify_intensity import SimplifyIntensity


class Provider(QgsProcessingProvider):
    def loadAlgorithms(self, *args, **kwargs):
        self.addAlgorithm(DangerZones())
        self.addAlgorithm(ApplyMatrix())
        self.addAlgorithm(SimplifyIntensity())
        self.addAlgorithm(MergeIntensityLayers())
        self.addAlgorithm(FixGeometries())
        self.addAlgorithm(NoImpact())
        self.addAlgorithm(Propagation())
        self.addAlgorithm(RemoveOverlappings())
        self.addAlgorithm(MergeByArea())
        self.addAlgorithm(RemoveByArea())

    def id(self, *args, **kwargs):
        return "pzp_utils"

    def name(self, *args, **kwargs):
        return self.tr("PZP_UTILS")

    def icon(self):
        return QgsProcessingProvider.icon(self)
