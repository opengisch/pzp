import os

from qgis import processing
from qgis.core import QgsExpressionContextUtils, QgsProject

from pzp import domains, utils

FORM_CLASS = utils.get_ui_class("calculation.ui")

# TODO: check for needed layers and show only groups with correct layers


# class CalculationDialog(QDialog, FORM_CLASS):
#     def __init__(self, iface, group, parent=None):
#         QDialog.__init__(self, parent)
# self.setupUi(self)
# self.buttonBox.accepted.disconnect()
# self.buttonBox.clicked.connect(self.button_box_clicked)

# for process in domains.PROCESS_TYPES.items():
#     self.process_cbox.addItem(process[1], process[0])

# root = QgsProject.instance().layerTreeRoot()
# if isinstance(root, QgsLayerTreeGroup):
#     for group in root.findGroups(recursive=True):
#         self.group_cbox.addItem(group.name(), group)

# def button_box_clicked(self, button):
#     if self.buttonBox.buttonRole(button) == QDialogButtonBox.AcceptRole:
#         process_type = self.process_cbox.currentData()
#         calculate(process_type, None)
#         self.close()
#     else:
#         self.close()


class CalculationDialog:
    def __init__(self, iface, group, parent=None):
        self.group = group

    def exec_(self):
        guess_params(self.group)


def guess_params(group):
    # process and layers
    layer_nodes = group.findLayers()
    layer_intensity = None
    process_type = None

    for layer_node in layer_nodes:
        if layer_node.name() == "Intensità completa":
            layer_intensity = layer_node.layer()
            process_type = int(
                QgsExpressionContextUtils.layerScope(layer_intensity).variable(
                    "pzp_process"
                )
            )

            calculate(process_type, layer_intensity)


def calculate(process_type, layer_intensity):

    # TODO: find group and layers

    # Processing algorithm wants the index of the process type in the combobox
    process_type_idx = list(domains.PROCESS_TYPES).index(process_type)

    result = processing.run(
        "pzp:danger_zones",
        {
            "INPUT": layer_intensity.id(),
            "PROCESS_FIELD": "proc_parz",
            "PERIOD_FIELD": "periodo_ritorno",
            "INTENSITY_FIELD": "classe_intensita",
            "PROCESS_TYPE": process_type_idx,
            "OUTPUT": "TEMPORARY_OUTPUT",
        },
    )

    layer = result["OUTPUT"]
    layer.setName(f"Pericolo ...")
    root = QgsProject.instance().layerTreeRoot()

    tree_layer = root.findLayer(
        QgsProject.instance().mapLayersByName("Intensità completa")[0]
    )
    tree_layer.parent()

    QgsProject.instance().addMapLayer(layer, True)
    # layer_parent.insertLayer(0, layer)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    qml_file_path = os.path.join(current_dir, "qml", "danger_level.qml")
    layer.loadNamedStyle(qml_file_path)

    # # TODO: disambiguity dialog
    # dlg = AmbiguityDialog(self.iface)
    # ambiguous_features = []

    # for feature in layer.getFeatures():
    #     # TODO: depending on the matrix of the process!!
    #     if feature["Tipo di pericolo"] in [1004]:
    #         print("AMBIGUO")
    #         ambiguous_features.append(feature)

    #     if dlg.exec_():
    #         pass

    # # Cycle all features in danger layer
    # # by process, create a list of the ambiguous ones with featureid
    # # populate list where to select the danger_type
