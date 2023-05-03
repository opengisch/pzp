import os
from functools import wraps

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
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.uic import loadUiType
from qgis.utils import iface


def push_info(message):
    _get_iface().messageBar().pushInfo("pzp", message)


def push_warning(message, time=0):
    _get_iface().messageBar().pushMessage("pzp", message, Qgis.Warning, time)


def push_error(message, time=0):
    _get_iface().messageBar().pushMessage("pzp", message, Qgis.Critical, time)


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
                    return func(
                        *args[:-1], **kwargs
                    )  # TODO: Why there is a False as last argument?

            push_error(
                f"Il progetto corrente non è compatibile con questa versione del plugin:"
            )
            return

        return wrapper

    return decorate


def get_ui_class(ui_file):
    """Get UI Python class from .ui file.
       Can be filename.ui or subdirectory/filename.ui
    :param ui_file: The file of the ui in svir.ui
    :type ui_file: str
    """
    os.path.sep.join(ui_file.split("/"))
    ui_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "ui", ui_file)
    )
    return loadUiType(ui_file_path)[0]


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
    qml_file_path = os.path.join(current_dir, "qml", f"{qml_name}.qml")
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
    QgsLayerDefinition().loadLayerDefinition(
        qlr_file_path, QgsProject.instance(), group
    )


def create_group(name, root=None):
    if not root:
        root = QgsProject.instance().layerTreeRoot()
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


def create_filtered_layers_from_gpkg(gpkg_layer_name, gpkg_path, substring, name):
    gpkg_layer = load_gpkg_layer(gpkg_layer_name, gpkg_path)
    gpkg_layer.setSubsetString(substring)
    options = gpkg_layer.geometryOptions()
    options.setGeometryPrecision(0.001)
    options.setRemoveDuplicateNodes(True)
    options.setGeometryChecks(["QgsIsValidCheck"])
    gpkg_layer.setName(name)
    return gpkg_layer
