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
    QgsFeature,
    QgsFeatureRequest,
    QgsFeatureSink,
    QgsGeometry,
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingUtils,
)

pluginPath = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]


class MergeByArea(QgisAlgorithm):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    MODE = "MODE"
    VALUE_FIELD = "VALUE_FIELD"

    MODE_LARGEST_AREA = 0
    MODE_SMALLEST_AREA = 1
    MODE_BOUNDARY = 2
    MODE_HIGHEST_VALUE = 3
    MODE_HIGHEST_MATRIX_VALUE = 4

    def group(self):
        return "Algoritmi"

    def groupId(self):
        return "algorithms"

    def __init__(self):
        super().__init__()

    def initAlgorithm(self, config=None):
        self.modes = [
            self.tr("Largest Area"),
            self.tr("Smallest Area"),
            self.tr("Largest Common Boundary")
        ]

        self.addParameter(
            QgsProcessingParameterFeatureSource(self.INPUT, self.tr("Input layer"), [QgsProcessing.TypeVectorPolygon])
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.MODE, self.tr("Merge selection with the neighbouring polygon with the"), options=self.modes
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Eliminated"), QgsProcessing.TypeVectorPolygon)
        )

    def name(self):
        return "merge_by_area"

    def displayName(self):
        return "Fondi per area"

    def processAlgorithm(self, parameters, context, feedback):
        inLayer = self.parameterAsSource(parameters, self.INPUT, context)
        mode = self.parameterAsEnum(parameters, self.MODE, context)
        valueField = self.parameterAsFields(parameters, self.VALUE_FIELD, context)

        featToEliminate = []

        (sink, dest_id) = self.parameterAsSink(
            parameters, self.OUTPUT, context, inLayer.fields(), inLayer.wkbType(), inLayer.sourceCrs()
        )
        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        for feature in inLayer.getFeatures():
            if feedback.isCanceled():
                break

            if feature.geometry().area() <= 1:
                featToEliminate.append(feature)
            else:
                # write the others to output
                sink.addFeature(feature, QgsFeatureSink.FastInsert)
        del sink

        # Delete all features to eliminate in processLayer
        processLayer = QgsProcessingUtils.mapLayerFromString(dest_id, context)
        processLayer.startEditing()

        # ANALYZE
        if len(featToEliminate) > 0:  # Prevent zero division
            start = 20.00
            add = 80.00 / len(featToEliminate)
        else:
            start = 100

        feedback.setProgress(start)
        madeProgress = True

        # We go through the list and see if we find any polygons we can
        # merge the selected with. If we have no success with some we
        # merge and then restart the whole story.
        while madeProgress:  # Check if we made any progress
            madeProgress = False
            featNotEliminated = []

            # Iterate over the polygons to eliminate
            for i in range(len(featToEliminate)):
                if feedback.isCanceled():
                    break

                feat = featToEliminate.pop()
                geom2Eliminate = feat.geometry()
                bbox = geom2Eliminate.boundingBox()
                fit = processLayer.getFeatures(QgsFeatureRequest().setFilterRect(bbox).setSubsetOfAttributes([]))
                mergeWithFid = None
                mergeWithGeom = None
                max = None
                selFeat = QgsFeature()

                # use prepared geometries for faster intersection tests
                engine = QgsGeometry.createGeometryEngine(geom2Eliminate.constGet())
                engine.prepareGeometry()

                while fit.nextFeature(selFeat):
                    if feedback.isCanceled():
                        break

                    selGeom = selFeat.geometry()

                    if engine.intersects(selGeom.constGet()):
                        # We have a candidate
                        iGeom = geom2Eliminate.intersection(selGeom)

                        # We need a common boundary in order to merge
                        if not iGeom:
                            continue

                        selValue = None
                        if mode == self.MODE_BOUNDARY:
                            selValue = iGeom.length()

                        elif mode == self.MODE_LARGEST_AREA:
                            selValue = selGeom.area()

                        elif mode == self.MODE_SMALLEST_AREA:
                            selValue = selGeom.area() * -1

                        else:
                            raise QgsProcessingException(
                                self.tr("Invalid value '{0}' for parameter '{1}'").format(mode, self.MODE)
                            )

                        if selValue is None:
                            # No candidate found
                            continue

                        useThis = False
                        if max is None:
                            max = selValue
                            useThis = True
                        elif selValue > max:
                            max = selValue
                            useThis = True

                        if useThis:
                            mergeWithFid = selFeat.id()
                            mergeWithGeom = QgsGeometry(selGeom)
                # End while fit

                if mergeWithFid is None:
                    featNotEliminated.append(feat)
                    continue

                # A successful candidate
                newGeom = mergeWithGeom.combine(geom2Eliminate)

                if processLayer.changeGeometry(mergeWithFid, newGeom):
                    madeProgress = True
                else:
                    raise QgsProcessingException(
                        self.tr("Could not replace geometry of feature with id {0}").format(mergeWithFid)
                    )

                start = start + add
                feedback.setProgress(start)

            # End for featToEliminate

            featToEliminate = featNotEliminated

        # End while
        if not processLayer.commitChanges():
            raise QgsProcessingException(self.tr("Could not commit changes"))

        for feature in featNotEliminated:
            if feedback.isCanceled():
                break

            print("Error: could not merge feature: {}".format(feature.id()))

            processLayer.dataProvider().addFeature(feature, QgsFeatureSink.FastInsert)

        return {self.OUTPUT: dest_id}
