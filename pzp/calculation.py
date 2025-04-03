import datetime
import traceback

from qgis import processing
from qgis.core import (
    QgsExpressionContextUtils,
    QgsProcessingException,
    QgsProject,
    QgsVectorLayer,
)

from pzp.processing import domains
from pzp.utils import utils
from pzp.utils.settings import Settings


class PropagationTool:
    def __init__(self, iface, group, parent=None):
        self._group = group or QgsProject.instance().layerTreeRoot()
        self._tool_name = "Calcolo propagazione"

    def _guess_params(self):
        # process and layers
        layer_nodes = self._group.findLayers()
        process_type = None
        layer_propagation = None
        layer_breaking = None

        for layer_node in layer_nodes:
            pzp_layer = QgsExpressionContextUtils.layerScope(layer_node.layer()).variable("pzp_layer")
            if pzp_layer == "propagation":
                layer_propagation = layer_node.layer()
                process_type = int(QgsExpressionContextUtils.layerScope(layer_propagation).variable("pzp_process"))
            elif pzp_layer == "breaking":
                layer_breaking = layer_node.layer()
                process_type = int(QgsExpressionContextUtils.layerScope(layer_breaking).variable("pzp_process"))

        if not layer_propagation:
            utils.push_error("Layer con le probabilità di propagazione non trovato", 3)
            return (False,)
        if not layer_breaking:
            utils.push_error("Layer con le probabilità di rottura non trovato", 3)
            return (False,)
        if not process_type:
            utils.push_error("Impossibile determinare il tipo di processo", 3)
            return (False,)

        return True, process_type, layer_propagation, layer_breaking

    def run(self, force=False):
        result = self._guess_params()
        if not result[0]:
            return

        ok, process_type, layer_propagation, layer_breaking = result

        check_ok = False
        if not force:
            check_ok = utils.check_inputs(self._tool_name, layer_breaking, self.run)

        if force or check_ok:
            self.run_with_parameters(process_type, layer_propagation, layer_breaking)

    def run_with_parameters(self, process_type, layer_propagation, layer_breaking):
        try:
            layer_intensity = self._calculate(process_type, layer_propagation, layer_breaking)
        except (QgsProcessingException, Exception) as exc:
            utils.push_error_report(
                self._tool_name,
                "Process: {}".format(domains.PROCESS_TYPES.get(process_type, "Unknown process!")),
                f"Description: \n{exc}" if "traceback" not in str(exc).lower() else "",
                traceback.format_exc(),
            )
            return None

        gpkg_path = layer_breaking.dataProvider().dataSourceUri().split("|")[0]
        layer_name = "Intensità completa"
        self._save_layer(layer_intensity, layer_name, gpkg_path)

        new_layer = self._load_layer_to_project(process_type, gpkg_path, layer_name, layer_propagation)
        self._post_layer_configuration(process_type, new_layer)

        utils.push_info(f"The tool '{self._tool_name}' has finished successfully!", 5)

        return new_layer

    def _calculate(self, process_type, layer_propagation, layer_breaking):
        print(f"{process_type=}")
        print(f"{layer_propagation=}")
        print(f"{layer_breaking=}")

        result_01 = processing.run(
            "pzp_utils:propagation",
            {
                "BREAKING_LAYER": layer_breaking.id(),
                "BREAKING_FIELD": "prob_rottura",
                "SOURCE_FIELD": "fonte_proc",
                "PROPAGATION_LAYER": layer_propagation.id(),
                "PROPAGATION_FIELD": "prob_propagazione",
                "BREAKING_FIELD_PROP": "prob_rottura",
                "SOURCE_FIELD_PROP": "fonte_proc",
                "OUTPUT": "TEMPORARY_OUTPUT",
            },
        )
        result_02 = processing.run(
            "native:extractbyexpression",
            {
                "INPUT": result_01["OUTPUT"],
                "EXPRESSION": f'"proc_parz" = {process_type}',
                "OUTPUT": "TEMPORARY_OUTPUT",
            },
        )

        # Clippa per periodo di ritorno
        result_03 = processing.run(
            "pzp_utils:remove_overlappings",
            {
                "INPUT": result_02["OUTPUT"],
                "INTENSITY_FIELD": "classe_intensita",
                "PERIOD_FIELD": "periodo_ritorno",
                "SOURCE_FIELD": "fonte_proc",
                "OUTPUT": "TEMPORARY_OUTPUT",
            },
        )

        result = processing.run(
            "native:deletecolumn",
            {
                "INPUT": result_03["OUTPUT"],
                "COLUMN": ["fid"],
                "OUTPUT": "TEMPORARY_OUTPUT",
            },
        )

        return result["OUTPUT"]

    def _save_layer(self, layer, layer_name, gpkg_path):
        layer.setName(layer_name)

        # Save output layer to gpkg
        params = {
            "LAYERS": [layer],
            "OUTPUT": gpkg_path,
            "OVERWRITE": False,  # Important!
            "SAVE_STYLES": False,
            "SAVE_METADATA": False,
            "SELECTED_FEATURES_ONLY": False,
        }
        processing.run("native:package", params)

    def _load_layer_to_project(self, process_type, gpkg_path, layer_name, base_layer):
        # Load layer from gpkg
        new_layer = QgsVectorLayer(gpkg_path + "|layername=" + layer_name, "MultiPolygon", "ogr")
        new_layer.setName(layer_name)

        utils.set_qml_style(new_layer, "intensity")

        project = QgsProject.instance()
        project.addMapLayer(new_layer, False)

        def _set_common_post_configurations(_layer, _base_layer):
            _idx = _base_layer.fields().indexOf("fonte_proc")
            _widget = _base_layer.editorWidgetSetup(_idx)
            _idx = _layer.fields().indexOf("fonte_proc")
            _layer.setEditorWidgetSetup(_idx, _widget)

            QgsExpressionContextUtils.setLayerVariable(_layer, "pzp_process", process_type)

        _set_common_post_configurations(new_layer, base_layer)

        group_intensity_filtered = utils.create_group("Intensità (con filtri x visualizzazione scenari)", self._group)
        group_intensity_filtered.setExpanded(True)

        group_intensity_filtered.addLayer(new_layer)

        filter_params = [
            ("\"periodo_ritorno\"='30'", "T 30", True),
            ("\"periodo_ritorno\"='100'", "T 100", True),
            ("\"periodo_ritorno\"='300'", "T 300", True),
            ("\"periodo_ritorno\">'300'", "T >300", False),
        ]

        for param in filter_params:
            gpkg_layer = utils.create_filtered_layer_from_gpkg(
                new_layer.name(),
                gpkg_path,
                param[0],
                param[1],
            )
            utils.set_qml_style(gpkg_layer, "intensity")

            if param[2]:  # Remove 'impatto presente' category
                utils.remove_renderer_category(gpkg_layer, "1001")

            project.addMapLayer(gpkg_layer, False)
            group_intensity_filtered.addLayer(gpkg_layer)
            _set_common_post_configurations(gpkg_layer, base_layer)
            layer_node = self._group.findLayer(gpkg_layer.id())
            layer_node.setExpanded(False)
            layer_node.setItemVisibilityChecked(False)

        return new_layer

    def _post_layer_configuration(self, process_type, new_layer):
        options = new_layer.geometryOptions()
        options.setGeometryPrecision(0.001)
        options.setRemoveDuplicateNodes(True)
        options.setGeometryChecks(["QgsIsValidCheck"])

        QgsExpressionContextUtils.setLayerVariable(new_layer, "pzp_layer", "intensity")


class CalculationTool:
    def __init__(self, iface, group, parent=None):
        self._group = group
        self._tool_name = "Calcolo zone di pericolo"

    def run(self, force=False):
        process_type, layer_intensity = self._guess_params()

        if process_type is None or layer_intensity is None:
            return

        check_ok = False
        if not force:
            check_ok = utils.check_inputs(self._tool_name, layer_intensity, self.run)

        if force or check_ok:
            self.run_with_parameters(process_type, layer_intensity)

    def run_with_parameters(self, process_type, layer_intensity):
        try:
            layer_pericolo = self._calculate(process_type, layer_intensity)
        except (QgsProcessingException, Exception) as exc:
            utils.push_error_report(
                self._tool_name,
                "Process: {}".format(domains.PROCESS_TYPES.get(process_type, "Unknown process!")),
                f"Description: \n{exc}" if "traceback" not in str(exc).lower() else "",
                traceback.format_exc(),
            )
            return None

        gpkg_path = layer_intensity.dataProvider().dataSourceUri().split("|")[0]
        layer_name = f"Pericolo {process_type} {datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        self._save_layer(layer_pericolo, layer_name, gpkg_path)

        new_layer = self._load_layer_to_project(process_type, gpkg_path, layer_name)
        self._post_layer_configuration(process_type, new_layer)

        utils.push_info(f"The tool '{self._tool_name}' has finished successfully!", 5)

        return new_layer

    def _guess_params(self):
        # process and layers
        layer_nodes = self._group.findLayers()
        layer_intensity = None
        process_type = None

        for layer_node in layer_nodes:
            pzp_layer = QgsExpressionContextUtils.layerScope(layer_node.layer()).variable("pzp_layer")
            if pzp_layer == "intensity":
                layer_intensity = layer_node.layer()
                process_type = int(QgsExpressionContextUtils.layerScope(layer_intensity).variable("pzp_process"))
                break

        if not layer_intensity:
            utils.push_error("Layer con le intensità non trovato", 3)
            return None, None

        if not process_type:
            utils.push_error("Impossibile determinare il tipo di processo", 3)
            return None, None

        return process_type, layer_intensity

    def _calculate(self, process_type, layer_intensity):
        print(f"{process_type=}")
        print(f"{layer_intensity=}")

        result_01 = processing.run(
            "native:extractbyexpression",
            {
                "INPUT": layer_intensity.id(),
                "EXPRESSION": f'"proc_parz" = {process_type}',
                "OUTPUT": "TEMPORARY_OUTPUT",
            },
        )

        result_02 = processing.run(
            "pzp_utils:fix_geometries",
            {
                "INPUT": result_01["OUTPUT"],
                "OUTPUT": "TEMPORARY_OUTPUT",
            },
        )

        try:
            result_03 = processing.run(
                "pzp_utils:apply_matrix",
                {
                    "INPUT": result_02["OUTPUT"],
                    "PERIOD_FIELD": "periodo_ritorno",
                    "INTENSITY_FIELD": "classe_intensita",
                    "MATRIX": domains.MATRICES[process_type],
                    "OUTPUT": "TEMPORARY_OUTPUT",
                },
            )
        except (QgsProcessingException, Exception) as e:
            # Sample on how to add more context to a processing error
            raise QgsProcessingException("The algorithm 'pzp_utils:apply_matrix' failed! " + str(e))

        result_04 = processing.run(
            "native:dissolve",
            {
                "INPUT": result_03["OUTPUT"],
                "FIELD": "matrice;fonte_proc",
                "SEPARATE_DISJOINT": False,
                "OUTPUT": "TEMPORARY_OUTPUT",
            },
        )

        result_05 = processing.run(
            "pzp_utils:danger_zones",
            {
                "INPUT": result_04["OUTPUT"],
                "MATRIX_FIELD": "matrice",
                "PROCESS_SOURCE_FIELD": "fonte_proc",
                "MERGE_FORM_FACTOR": Settings().merge_form_factor.value(),
                "OUTPUT": "TEMPORARY_OUTPUT",
            },
        )

        result_06 = processing.run(
            "native:fixgeometries",
            {
                "INPUT": result_05["OUTPUT"],
                "OUTPUT": "TEMPORARY_OUTPUT",
            },
        )

        return result_06["OUTPUT"]

    def _save_layer(self, layer, layer_name, gpkg_path):
        layer.setName(layer_name)

        # Save output layer to gpkg
        params = {
            "LAYERS": [layer],
            "OUTPUT": gpkg_path,
            "OVERWRITE": False,  # Important!
            "SAVE_STYLES": False,
            "SAVE_METADATA": False,
            "SELECTED_FEATURES_ONLY": False,
        }
        processing.run("native:package", params)

    def _load_layer_to_project(self, process_type, gpkg_path, layer_name):
        # Load layer from gpkg
        new_layer = QgsVectorLayer(gpkg_path + "|layername=" + layer_name, "MultiPolygon", "ogr")

        utils.set_qml_style(new_layer, "danger_level")

        project = QgsProject.instance()

        # Get unique values from fonte processo
        idx = new_layer.fields().indexOf("fonte_proc")
        sources = new_layer.uniqueValues(idx) if idx != -1 else []

        if len(sources) <= 1:
            new_layer.setName(layer_name)
            project.addMapLayer(new_layer, True)
        else:
            # Add layer inside a group and add filtered layers below
            new_layer.setName("Pericolo")
            project.addMapLayer(new_layer, False)

            group_danger_filtered = utils.create_group(layer_name, self._group, to_the_top=True)
            group_danger_filtered.setExpanded(True)

            group_danger_filtered.addLayer(new_layer)

            sources = sorted(sources)
            filter_params = [(f"\"fonte_proc\"='{source}'", f"{source}") for source in sources]

            for param in filter_params:
                gpkg_layer = utils.create_filtered_layer_from_gpkg(
                    layer_name,
                    gpkg_path,
                    param[0],
                    param[1],
                )
                utils.set_qml_style(gpkg_layer, "danger_level")

                project.addMapLayer(gpkg_layer, False)
                group_danger_filtered.addLayer(gpkg_layer)
                layer_node = group_danger_filtered.findLayer(gpkg_layer.id())
                layer_node.setExpanded(False)
                layer_node.setItemVisibilityChecked(False)

        return new_layer

    def _post_layer_configuration(self, process_type, new_layer):
        # Set geometry options and layer variables
        options = new_layer.geometryOptions()
        options.setGeometryPrecision(0.001)
        options.setRemoveDuplicateNodes(True)
        options.setGeometryChecks(["QgsIsValidCheck"])

        QgsExpressionContextUtils.setLayerVariable(new_layer, "pzp_layer", "danger_zones")
        QgsExpressionContextUtils.setLayerVariable(new_layer, "pzp_process", process_type)
