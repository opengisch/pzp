from .pzp import PZP


def classFactory(iface):
    return PZP(iface)
