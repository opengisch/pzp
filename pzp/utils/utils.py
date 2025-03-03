import os
from functools import partial, wraps
from pathlib import Path

from qgis import processing
from qgis.core import (
    Qgis,
    QgsCoordinateReferenceSystem,
    QgsDefaultValue,
    QgsEditorWidgetSetup,
    QgsField,
    QgsFieldConstraints,
    QgsLayerDefinition,
    QgsMessageLog,
    QgsProject,
    QgsVectorLayer,
)
from qgis.PyQt.QtCore import Qt, QVariant
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


def check_inputs(tool_name: str, input: QgsVectorLayer, callback) -> bool:
    parameters = {
        "INPUT_LAYER": input.id(),
        "METHOD": 1,  # 1: QGIS, 2: GEOS
        "IGNORE_RING_SELF_INTERSECTION": False,
        "VALID_OUTPUT": "TEMPORARY_OUTPUT",
        "INVALID_OUTPUT": "TEMPORARY_OUTPUT",
        "ERROR_OUTPUT": "TEMPORARY_OUTPUT",
    }
    results = processing.run("qgis:checkvalidity", parameters)

    check_ok = results["ERROR_COUNT"] == 0

    if not check_ok:
        # Show message bar with two options:
        # 1) See errors
        # 2) Run with errors
        _push_input_error_report(tool_name, input.name(), results["ERROR_COUNT"], results["ERROR_OUTPUT"], callback)

    return check_ok


def _push_input_error_report(
    tool_name: str, input_layer_name: str, error_count: int, error_output: QgsVectorLayer, callback
):
    widget = iface.messageBar().createMessage(
        tool_name, f"{error_count} errori trovati nelle geometrie del layer '{input_layer_name}'!"
    )

    def _see_geometry_errors(error_layer: QgsVectorLayer, tool_name: str, input_name: str):
        # Style errors
        set_qml_style(error_layer, "point_error")

        # Add layer to ToC
        QgsProject.instance().addMapLayer(error_layer)

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


def add_field_to_layer(layer, name, alias="", variant=QVariant.Int):
    field = QgsField(name, variant)
    field.setAlias(alias)
    pr = layer.dataProvider()
    pr.addAttributes([field])
    layer.updateFields()


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


def set_qml_style(layer, qml_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    qml_file_path = os.path.join(current_dir, "../qml", f"{qml_name}.qml")
    layer.loadNamedStyle(qml_file_path)


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


def set_value_relation_field(layer, field_name, other_layer, key_field, value_field):
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
        },
    )

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
