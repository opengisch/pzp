from pzp import utils


def add_mandate(name):
    # TODO: In the ui Check if one already exists in the current QGIS project and inform the user
    group = utils.create_group(f"Pericoli naturali mandato PZP - {name}")

    # Raster layers
    utils.load_qlr_layer("dati_base", group)
    utils.load_qlr_layer("mappe_base", group)
