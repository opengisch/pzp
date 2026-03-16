import os
from functools import partial, wraps
from pathlib import Path

from qgis import processing
from qgis.core import (
    Qgis,
    QgsCategorizedSymbolRenderer,
    QgsCoordinateReferenceSystem,
    QgsDefaultValue,
    QgsEditorWidgetSetup,
    QgsExpression,
    QgsFeature,
    QgsFeatureRequest,
    QgsField,
    QgsFieldConstraints,
    QgsLayerDefinition,
    QgsMessageLog,
    QgsProcessingException,
    QgsProject,
    QgsVectorLayer,
)
from qgis.PyQt.QtCore import QMetaType, Qt, QVariant
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QPushButton
from qgis.PyQt.uic import loadUiType
from qgis.utils import iface

from pzp.utils.override_cursor import OverrideCursor


def push_info(message, time=0, showMore=""):
    args = [message, showMore, Qgis.Info, time] if showMore else [message, Qgis.Info, time]
    _get_iface().messageBar().pushMessage("pzp", *args)


def push_warning(message, time=0, showMore=""):
    args = [message, showMore, Qgis.Warning, time] if showMore else [message, Qgis.Warning, time]
    _get_iface().messageBar().pushMessage("pzp", *args)


def push_error(message, time=0, showMore=""):
    args = [message, showMore, Qgis.Critical, time] if showMore else [message, Qgis.Critical, time]
    _get_iface().messageBar().pushMessage("pzp", *args)


def push_error_report(title, subtitle="", description="", traceback=""):
    widget = iface.messageBar().createMessage("PZP", f"There was a problem running the <b>'{title}'</b> tool.")

    button = QPushButton(widget)
    button.setText("Show more...")
    button.pressed.connect(partial(_show_error_dialog, title, subtitle, description, traceback))
    widget.layout().addWidget(button)

    iface.messageBar().pushWidget(widget, Qgis.Critical, 0)


def _show_error_dialog(title, subtitle="", description="", traceback=""):
    from pzp.gui.error_dialog import ErrorDialog

    dlg = ErrorDialog(title, subtitle, description, traceback)
    dlg.exec_()


def check_inputs(
    tool_name: str, input: QgsVectorLayer, callback, check_overlaps: bool = False, show_error_message: bool = True
) -> bool:
    pks_idxs = input.primaryKeyAttributes()
    pk_idx = pks_idxs[0] if len(pks_idxs) == 1 else -1
    pk_name = input.fields().field(pk_idx).name() if len(pks_idxs) == 1 else ""

    def _add_fields(layer: QgsVectorLayer, fields: list[QgsField]):
        layer.dataProvider().addAttributes(fields)
        layer.updateFields()

    parameters = {
        "INPUT_LAYER": input.id(),
        "METHOD": 1,  # 1: QGIS, 2: GEOS
        "IGNORE_RING_SELF_INTERSECTION": False,
        "VALID_OUTPUT": "TEMPORARY_OUTPUT",
        "INVALID_OUTPUT": "TEMPORARY_OUTPUT",
        "ERROR_OUTPUT": "TEMPORARY_OUTPUT",
    }
    results = processing.run("qgis:checkvalidity", parameters)

    def _clean_error_outputs(error_layer: QgsVectorLayer) -> QgsVectorLayer:
        # Remove 'Duplicate nodes' error, since it will be fixed
        # by pzp_utils:fix_geometries alg.
        parameters = {
            # Filter by searching 'duplicate nodes'. 0 means not found.
            "EXPRESSION": "strpos(\"message\",'duplicate nodes') = 0",
            "INPUT": error_layer,
            "OUTPUT": "TEMPORARY_OUTPUT",
        }
        result = processing.run("native:extractbyexpression", parameters)
        return result["OUTPUT"]

    error_output = _clean_error_outputs(results["ERROR_OUTPUT"])
    check_ok = error_output.featureCount() == 0

    if not check_ok:
        # Add feature id to each error in the Error Output layer

        if pk_idx != -1:
            # Get mappings from input and error layers, so that we can then
            # perform a join to bring input's pk into error output layer.
            # Note that _errors from a single feature in input layer are separated by '\n'.
            # Note also that PKs are in the Invalid output layer, we need to get them
            # from there and then complete data in Error Output layer (point layer).
            request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
            mapping_pk_msgs = {
                feature[pk_idx]: feature["_errors"].split("\n")
                for feature in results["INVALID_OUTPUT"].getFeatures(request)
            }
            mapping_error_msg = {feature["message"]: feature.id() for feature in error_output.getFeatures(request)}

            # Add field to output_layer
            _add_fields(error_output, [input.fields().field(pk_idx)])
            error_pk_idx = error_output.fields().indexOf(pk_name)
            attrs = {}  # fid: {error_pk_idx: pk}

            for pk, msgs in mapping_pk_msgs.items():
                for msg in msgs:
                    fid = mapping_error_msg.get(msg, -1)
                    if fid != -1:
                        attrs[fid] = {error_pk_idx: pk}

            if attrs:
                error_output.dataProvider().changeAttributeValues(attrs)

    # Check for overlaps
    check_overlaps_ok = True
    if check_overlaps and Qgis.QGIS_VERSION_INT >= 34400:
        if not pk_name:
            log_error(f"Unable to check overlaps in layer '{input.name()}'. The layer has no unique field!")
        else:
            overlap_ran_with_exceptions = False
            parameters = {
                "INPUT": input.id(),
                "UNIQUE_ID": pk_name,  # fid
                "ERRORS": "TEMPORARY_OUTPUT",  # Point layer
                "OUTPUT": "TEMPORARY_OUTPUT",  # Polygon layer
                "MIN_OVERLAP_AREA": 0,
                "TOLERANCE": 8,
            }
            try:
                results_overlaps = processing.run("native:checkgeometryoverlap", parameters)
            except (QgsProcessingException, Exception) as e:
                # There is an exception here, which means some nasty geometry issues
                # were detected in the qgis:checkvalidity alg. and will be shown to users.
                # We leave the overlap check out, log the issue, and continue, so
                # that original geometry issues can still be shown to users.
                log_error("Checking overlaps failed! First fix the next issue(s), and then run again. " + str(e))
                overlap_ran_with_exceptions = True
            else:
                error_overlaps_output = results_overlaps["ERRORS"]
                check_overlaps_ok = error_overlaps_output.featureCount() == 0

            if not overlap_ran_with_exceptions and not check_overlaps_ok:
                # Get pairs of overlapping feature pks (fids)
                request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
                overlapping_feature_field = f"gc_overlap_feature_{pk_name}"
                overlapping_pk_pairs = [
                    (feature[pk_name], feature[overlapping_feature_field])
                    for feature in error_overlaps_output.getFeatures(request)
                ]
                overlapping_pk_pairs = set(overlapping_pk_pairs)  # Get rid of duplicate pairs

                # Prepare cached data from input layer
                mapping_pk_data = {
                    feature[pk_idx]: {"source": feature["fonte_proc"], "scenario": feature["periodo_ritorno"]}
                    for feature in input.getFeatures(request)
                }

                # Filter overlap errors between the same source/scenario
                overlapping_errors = []
                for pk_1, pk_2 in overlapping_pk_pairs:
                    data_1 = mapping_pk_data[pk_1]
                    data_2 = mapping_pk_data[pk_2]
                    if data_1["source"] != data_2["source"]:
                        # Polygons from different source may overlap
                        continue

                    if data_1["scenario"] != data_2["scenario"]:
                        # Polygons from different scenarios may overlap
                        continue

                    overlapping_errors.append((pk_1, pk_2))

                # And finally, copy filtered overlap errors to the main error_output layer
                check_overlaps_ok = len(overlapping_errors) == 0
                if overlapping_errors:
                    new_fields = [
                        error_overlaps_output.fields().field(overlapping_feature_field),
                        QgsField("fonte_proc", QMetaType.Type.QString),
                        QgsField("periodo_ritorno", QMetaType.Type.QString),
                        QgsField("overlapped_area", QMetaType.Type.Double),
                    ]
                    if error_output.fields().indexOf(pk_name) == -1:
                        new_fields = [input.fields().field(pk_idx)] + new_fields
                    _add_fields(error_output, new_fields)

                    new_features = []
                    for pk_1, pk_2 in overlapping_errors:
                        expression = QgsExpression(f"{pk_name} = {pk_1} and {overlapping_feature_field} = {pk_2}")
                        request = QgsFeatureRequest(expression)
                        for feature in error_overlaps_output.getFeatures(request):
                            geometry = feature.geometry()
                            new_feature = QgsFeature(error_output.fields())
                            new_feature.setGeometry(geometry)
                            new_feature["message"] = "Overlapping features"
                            new_feature[pk_name] = pk_1
                            new_feature[overlapping_feature_field] = pk_2
                            new_feature["fonte_proc"] = mapping_pk_data[pk_1]["source"]
                            new_feature["periodo_ritorno"] = mapping_pk_data[pk_1]["scenario"]
                            new_feature["overlapped_area"] = feature["gc_error"]

                            new_features.append(new_feature)

                    if new_features:
                        error_output.dataProvider().addFeatures(new_features)

    if not (check_ok and check_overlaps_ok):
        if len(pks_idxs) > 1:
            log_warning(
                f"Feature ids won't be shown in Error Output layer: multiple PK fields found in layer '{input.name()}'!"
            )
        elif len(pks_idxs) == 0:
            log_warning(
                f"Feature ids won't be shown in Error Output layer: PK field not found in layer '{input.name()}'!"
            )

        # Show message bar with two options:
        # 1) See errors
        # 2) Run with errors
        if show_error_message:
            _push_input_error_report(tool_name, input.name(), error_output.featureCount(), error_output, callback)

    return check_ok and check_overlaps_ok, error_output


def _push_input_error_report(
    tool_name: str, input_layer_name: str, error_count: int, error_output: QgsVectorLayer, callback
):
    widget = iface.messageBar().createMessage(
        tool_name, f"{error_count} errori trovati nelle geometrie del layer '{input_layer_name}'!"
    )

    def _see_geometry_errors(error_layer: QgsVectorLayer, tool_name: str, input_name: str):
        # Style errors
        set_qml_style(error_layer, "point_error")
        error_layer.setName("Errori Geometrici")

        # Add layer to ToC, in its own group
        QgsProject.instance().addMapLayer(error_layer, False)
        group = create_group("Errori", to_the_top=True)
        group.setExpanded(True)
        group.addLayer(error_layer)

        # Show attribute table
        iface.showAttributeTable(error_layer)

        # Inform users about what just happened to QGIS GUI
        iface.messageBar().clearWidgets()
        iface.messageBar().pushMessage(tool_name, f"Showing errors in input layer '{input_name}'", Qgis.Info, 0)

    button = QPushButton(widget)
    button.setText("Ispeziona gli errori...")
    button.pressed.connect(partial(_see_geometry_errors, error_output, tool_name, input_layer_name))
    widget.layout().addWidget(button)

    def _run_with_errors(callback, tool_name, input_name, count):
        log_warning(
            "'{}' is running with {} geometry errors in its input layer ('{}')...".format(tool_name, count, input_name)
        )
        iface.messageBar().clearWidgets()
        # QCoreApplication.processEvents()  # Uncomment to see the messagebar closed
        with OverrideCursor(Qt.WaitCursor):
            callback(True)  # force=True

    button = QPushButton(widget)
    button.setText("Ignora e continua...")
    button.pressed.connect(partial(_run_with_errors, callback, tool_name, input_layer_name, error_count))
    widget.layout().addWidget(button)

    iface.messageBar().pushWidget(widget, Qgis.Critical, 0)


def _get_iface():
    """In case of iface doesn't exist i.e. unit test, return a mocked one"""
    if iface:
        return iface
    else:
        from qgis.testing.mocked import get_iface

        return get_iface()


def log_info(message):
    QgsMessageLog.logMessage(message, "pzp", Qgis.Info)


def log_warning(message):
    QgsMessageLog.logMessage(message, "pzp", Qgis.Warning)


def log_error(message):
    QgsMessageLog.logMessage(message, "pzp", Qgis.Critical)


def write_project_metadata(keyword, value):
    project = QgsProject.instance()
    metadata = project.metadata()
    metadata.addKeywords("pzp:{}".format(keyword), [value])
    project.setMetadata(metadata)


def read_project_metadata(keyword):
    project = QgsProject.instance()
    metadata = project.metadata()
    keywords = metadata.keywords("pzp:{}".format(keyword))
    if keywords:
        return keywords[0]
    return None


def check_project():
    """Decorator to check the current project before running the function."""

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            pzp_project_version = read_project_metadata("project_version")

            if pzp_project_version:
                if pzp_project_version in [
                    "0.0.2",
                ]:  # TODO: actual version number
                    return func(*args[:-1], **kwargs)  # TODO: Why there is a False as last argument?

            push_error(
                f"Il progetto corrente ({pzp_project_version}) non è compatibile con questa versione del plugin."
            )
            return

        return wrapper

    return decorate


def get_ui_class(ui_file):
    """Get UI Python class from .ui file.
    :param ui_file: The file of the u
    :type ui_file: str
    """
    return loadUiType(ui_file)[0]


def add_field_to_layer(layer: QgsVectorLayer, name: str, alias: str = "", variant: QVariant = QVariant.Int) -> None:
    field = QgsField(name, variant)
    field.setAlias(alias)
    pr = layer.dataProvider()
    pr.addAttributes([field])
    layer.updateFields()


def add_virtual_field_to_layer(
    layer: QgsVectorLayer, name: str, alias: str = "", variant: QVariant = QVariant.Int, expression: str = ""
) -> None:
    field = QgsField(name, variant)
    layer.addExpressionField(expression, field)
    set_field_alias(layer, alias, field_name=name)


def set_field_alias(layer: QgsVectorLayer, field_alias: str, field_index: int = -1, field_name: str = "") -> None:
    if field_index == -1 and not field_name.strip():
        return

    if field_index == -1:
        field_index = layer.fields().indexOf(field_name)

    if field_index != -1:
        layer.setFieldAlias(field_index, field_alias)


def set_value_map_to_field(layer, field_name, domain_map):
    index = layer.fields().indexOf(field_name)
    setup = QgsEditorWidgetSetup(
        "ValueMap",
        {"map": {y: x for x, y in domain_map.items()}},
    )
    layer.setEditorWidgetSetup(index, setup)


def set_default_value_to_field(layer, field_name, expression):
    index = layer.fields().indexOf(field_name)
    default_value = QgsDefaultValue()
    default_value.setExpression(expression)
    layer.setDefaultValueDefinition(index, default_value)


def set_not_null_constraint_to_field(layer, field_name, enforce=True):
    index = layer.fields().indexOf(field_name)

    constraint = QgsFieldConstraints.ConstraintNotNull
    strength = QgsFieldConstraints.ConstraintStrengthHard
    if not enforce:
        strength = QgsFieldConstraints.ConstraintStrengthSoft
    layer.setFieldConstraint(index, constraint, strength)


def remove_not_null_constraint_to_field(layer, field_name):
    index = layer.fields().indexOf(field_name)

    constraint = QgsFieldConstraints.ConstraintNotNull
    layer.removeFieldConstraint(index, constraint)


def set_unique_constraint_to_field(layer, field_name, enforce=True):
    index = layer.fields().indexOf(field_name)

    constraint = QgsFieldConstraints.ConstraintUnique
    strength = QgsFieldConstraints.ConstraintStrengthHard
    if not enforce:
        strength = QgsFieldConstraints.ConstraintStrengthSoft
    layer.setFieldConstraint(index, constraint, strength)


def remove_unique_constraint_to_field(layer, field_name):
    index = layer.fields().indexOf(field_name)

    constraint = QgsFieldConstraints.ConstraintUnique
    layer.removeFieldConstraint(index, constraint)


def set_expression_constraint_to_field(layer, field_name, expression, description=""):
    index = layer.fields().indexOf(field_name)
    layer.setConstraintExpression(index, expression, description)


def set_qml_style(layer, qml_name, load_from_local_db=False):
    # load_from_local_db=True forces to load from the given QML, regardless of the GPKG style
    current_dir = os.path.dirname(os.path.abspath(__file__))
    qml_file_path = os.path.join(current_dir, "../qml", f"{qml_name}.qml")
    layer.loadNamedStyle(qml_file_path, load_from_local_db)


def remove_renderer_category(layer: QgsVectorLayer, category_value: str) -> bool:
    renderer = layer.renderer()
    res = False

    if isinstance(layer.renderer(), QgsCategorizedSymbolRenderer):
        index = renderer.categoryIndexForValue(category_value)

        if index != -1:
            res = renderer.deleteCategory(index)
            layer.triggerRepaint()
            _get_iface().layerTreeView().refreshLayerSymbology(layer.id())
            layer.emitStyleChanged()  # Update symbology in layer styling panel

    return res


def create_layer(name, path="MultiPolygon"):
    layer = QgsVectorLayer(
        path=path,
        baseName=name,
        providerLib="memory",
    )
    layer.setCrs(QgsCoordinateReferenceSystem("EPSG:2056"))
    return layer


def load_qlr_layer(qlr_name, group=None):
    if not group:
        group = QgsProject.instance().layerTreeRoot()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    qlr_file_path = os.path.join(current_dir, "qlr", f"{qlr_name}.qlr")

    QgsLayerDefinition.loadLayerDefinition(qlr_file_path, QgsProject.instance(), group)


def create_group(name, root=None, to_the_top=False):
    if not root:
        root = QgsProject.instance().layerTreeRoot()

    if to_the_top:
        group = root.insertGroup(0, name)
    else:
        group = root.addGroup(name)

    return group


def add_layer_to_gpkg(layer, gpkg_path):
    params = {
        "LAYERS": [layer],
        "OUTPUT": gpkg_path,
        "OVERWRITE": False,  # Important!
        "SAVE_STYLES": True,
        "SAVE_METADATA": True,
        "SELECTED_FEATURES_ONLY": False,
    }
    processing.run("native:package", params)


def load_gpkg_layer(layer_name, gpkg_path):
    source_path = f"{gpkg_path}|layername={layer_name}"
    layer = QgsVectorLayer(source_path, layer_name, "ogr")
    return layer


def set_value_relation_field(layer, field_name, other_layer, key_field, value_field, description=""):
    widget = QgsEditorWidgetSetup(
        "ValueRelation",
        {
            "AllowMulti": False,
            "AllowNull": False,
            "FilterExpression": "",
            "Key": key_field,
            "Layer": other_layer.id(),
            "OrderByValue": False,
            "UseCompleter": False,
            "Value": value_field,
            "Description": description,
        },
    )

    index = layer.fields().indexOf(field_name)
    layer.setEditorWidgetSetup(index, widget)


def set_range_to_field(layer: QgsVectorLayer, field_name: str, config: dict) -> None:
    widget = QgsEditorWidgetSetup("Range", config)
    index = layer.fields().indexOf(field_name)
    layer.setEditorWidgetSetup(index, widget)


def create_filtered_layer_from_gpkg(gpkg_layer_name, gpkg_path, substring, name):
    gpkg_layer = load_gpkg_layer(gpkg_layer_name, gpkg_path)
    gpkg_layer.setSubsetString(substring)
    options = gpkg_layer.geometryOptions()
    options.setGeometryPrecision(0.001)
    options.setRemoveDuplicateNodes(True)
    options.setGeometryChecks(["QgsIsValidCheck"])
    gpkg_layer.setName(name)
    return gpkg_layer


def get_icon(filename):
    return QIcon(str(get_plugin_path() / "icons" / filename))


def get_plugin_path() -> Path:
    return Path(__file__).parent.parent


def set_layer_opacity(layer: QgsVectorLayer, opacity: int) -> None:
    layer.setOpacity(opacity / 100.0)  # Convert percentage to a value between 0 and 1
