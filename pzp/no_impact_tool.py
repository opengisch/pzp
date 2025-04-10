import traceback

from qgis import processing
from qgis.core import QgsExpressionContextUtils, QgsProcessingException, edit

from pzp.processing import domains
from pzp.utils import utils


class ToolNessunImpatto:
    def __init__(self, group):
        self._group = group
        self._tool_name = "Aggiungi zone nessun impatto"

    def _guess_params(self):
        # process and layers
        layer_nodes = self._group.findLayers()
        layer_intensity = None
        layer_area = None
        process_type = None

        for layer_node in layer_nodes:
            pzp_layer = QgsExpressionContextUtils.layerScope(layer_node.layer()).variable("pzp_layer")
            if pzp_layer == "intensity":
                layer_intensity = layer_node.layer()
                var_process = QgsExpressionContextUtils.layerScope(layer_intensity).variable("pzp_process")
                process_type = int(var_process) if var_process else None
            elif pzp_layer == "area":
                layer_area = layer_node.layer()

        if not layer_intensity:
            utils.push_error("Layer con le intensità non trovato", 3)
            return (False,)
        if not layer_area:
            utils.push_error("Layer con le area di studio non trovato", 3)
            return (False,)
        if not process_type:
            utils.push_error("Impossibile determinare il tipo di processo", 3)
            return (False,)

        return True, process_type, layer_intensity, layer_area

    def run(self, force=False):
        result = self._guess_params()
        if not result[0]:
            return

        ok, process_type, layer_intensity, layer_area = result

        check_ok = False
        if not force:
            check_ok = utils.check_inputs(self._tool_name, layer_intensity, self.run)

        if force or check_ok:
            self.run_with_params(process_type, layer_intensity, layer_area)

    def run_with_params(self, process_type, layer_intensity, layer_area):
        try:
            self._calculate(process_type, layer_intensity, layer_area)
        except (QgsProcessingException, Exception) as exc:
            utils.push_error_report(
                self._tool_name,
                "Process: {}".format(domains.PROCESS_TYPES.get(process_type, "Unknown process!")),
                f"Description: \n{exc}" if "traceback" not in str(exc).lower() else "",
                traceback.format_exc(),
            )
            return False

        utils.push_info(f"The tool '{self._tool_name}' has finished successfully!", 5)
        return True

    def _calculate(self, process_type, layer_intensity, layer_area):
        result_01 = processing.run(
            "pzp_utils:no_impact",
            {
                "AREA_LAYER": layer_area.id(),
                "AREA_PROCESS_SOURCE_FIELD": "fonte_proc",
                "INTENSITY_PROCESS_SOURCE_FIELD": "fonte_proc",
                "INTENSITY_LAYER": layer_intensity.id(),
                "PERIOD_FIELD": "periodo_ritorno",
                "INTENSITY_FIELD": "classe_intensita",
                "OUTPUT": "TEMPORARY_OUTPUT",
            },
        )

        result = processing.run(
            "pzp_utils:fix_geometries",
            {
                "INPUT": result_01["OUTPUT"],
                "OUTPUT": "TEMPORARY_OUTPUT",
            },
        )

        result_layer = result["OUTPUT"]

        with edit(layer_intensity):
            for feature in result_layer.getFeatures():
                feature["fid"] = None
                layer_intensity.addFeature(feature)
