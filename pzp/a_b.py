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
                if matrice == 1008:
                    feature["grado_pericolo"] = 1003
                elif matrice == 1006:
                    feature["grado_pericolo"] = 1003
                elif matrice == 1004:
                    feature["grado_pericolo"] = 1004

            elif process_type in [2001, 2002]:  # Sciv. spontaneo and colata detritica
                if matrice == 1007:
                    feature["grado_pericolo"] = 1003
                elif matrice == 1005:
                    feature["grado_pericolo"] = 1003
            elif process_type == 3000:  # Caduta sassi
                if matrice == 1004:
                    feature["grado_pericolo"] = 1004
                elif matrice == 1006:
                    feature["grado_pericolo"] = 1003
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
                if matrice == 1008:
                    feature["grado_pericolo"] = 1002
                elif matrice == 1006:
                    feature["grado_pericolo"] = 1002
                elif matrice == 1004:
                    feature["grado_pericolo"] = 1003

            elif process_type in [2001, 2002]:  # Sciv. spontaneo and colata detritica
                if matrice == 1007:
                    feature["grado_pericolo"] = 1002
                elif matrice == 1005:
                    feature["grado_pericolo"] = 1002
            elif process_type == 3000:  # Caduta sassi
                if matrice == 1004:
                    feature["grado_pericolo"] = 1003
                elif matrice == 1006:
                    feature["grado_pericolo"] = 1002
            else:
                pass

            layer.updateFeature(feature)
