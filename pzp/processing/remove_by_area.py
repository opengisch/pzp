"""
Derived from:

***************************************************************************
    EliminateSelection.py
    ---------------------
    Date                 : January 2017
    Copyright         : (C) 2017 by Bernhard Ströbl
    Email                : bernhard.stroebl@jena.de
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""


import os

from processing.algs.qgis.QgisAlgorithm import QgisAlgorithm
from qgis.core import (
    QgsFeatureSink,
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
)

pluginPath = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]


class RemoveByArea(QgisAlgorithm):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    def group(self):
        return "Algoritmi"

    def groupId(self):
        return "algorithms"

    def __init__(self):
        super().__init__()

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(self.INPUT, self.tr("Input layer"), [QgsProcessing.TypeVectorPolygon])
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Eliminated"), QgsProcessing.TypeVectorPolygon)
        )

    def name(self):
        return "remove_by_area"

    def displayName(self):
        return "Rimuovi per area"

    def processAlgorithm(self, parameters, context, feedback):
        inLayer = self.parameterAsSource(parameters, self.INPUT, context)

        (sink, dest_id) = self.parameterAsSink(
            parameters, self.OUTPUT, context, inLayer.fields(), inLayer.wkbType(), inLayer.sourceCrs()
        )
        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        for feature in inLayer.getFeatures():
            if feedback.isCanceled():
                break

            if feature.geometry().area() <= 1:
                print(f"Remove feature: {feature.attributes()}")
                continue

            # write the others to output
            sink.addFeature(feature, QgsFeatureSink.FastInsert)

        del sink

        return {self.OUTPUT: dest_id}
