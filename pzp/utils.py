import os
from functools import wraps

from qgis.core import Qgis, QgsMessageLog, QgsProject
from qgis.PyQt.uic import loadUiType
from qgis.utils import iface


def push_info(message):
    _get_iface().messageBar().pushInfo("pzp", message)


def push_warning(message):
    _get_iface().messageBar().pushMessage("pzp", message, Qgis.Warning, 0)


def push_error(message):
    _get_iface().messageBar().pushMessage("pzp", message, Qgis.Critical, 0)


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
                if pzp_project_version in ["0", "1"]:  # TODO: actual version number
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
