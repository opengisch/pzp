from qgis.core import QgsExpressionContextUtils, edit


def a_b(layer):
    process_type = int(
        QgsExpressionContextUtils.layerScope(layer).variable("pzp_process")
    )
    selection = layer.selectedFeatures()

    if not selection:
        selection = layer.getFeatures()

    with edit(layer):
        for feature in selection:
            matrice = feature["matrice"]
            if process_type == 1200:  # Flusso detrito
                if matrice == 2:
                    feature["grado_pericolo"] = 1003
                elif matrice == 4:
                    feature["grado_pericolo"] = 1003
                elif matrice == 6:
                    feature["grado_pericolo"] = 1004

            elif process_type in [2001, 2002]:  # Sciv. spontaneo and colata detritica
                if matrice == 3:
                    feature["grado_pericolo"] = 1003
                elif matrice == 5:
                    feature["grado_pericolo"] = 1003
            elif process_type == 3000:  # Caduta sassi
                if matrice == 6:
                    feature["grado_pericolo"] = 1004
            else:
                pass

            layer.updateFeature(feature)


def b_a(layer):
    process_type = int(
        QgsExpressionContextUtils.layerScope(layer).variable("pzp_process")
    )
    selection = layer.selectedFeatures()

    if not selection:
        selection = layer.getFeatures()

    with edit(layer):
        for feature in selection:
            matrice = feature["matrice"]
            if process_type == 1200:  # Flusso detrito
                if matrice == 2:
                    feature["grado_pericolo"] = 1002
                elif matrice == 4:
                    feature["grado_pericolo"] = 1002
                elif matrice == 6:
                    feature["grado_pericolo"] = 1003

            elif process_type in [2001, 2002]:  # Sciv. spontaneo and colata detritica
                if matrice == 3:
                    feature["grado_pericolo"] = 1002
                elif matrice == 5:
                    feature["grado_pericolo"] = 1002
            elif process_type == 3000:  # Caduta sassi
                if matrice == 6:
                    feature["grado_pericolo"] = 1003
            else:
                pass

            layer.updateFeature(feature)
