<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis minScale="1e+08" simplifyDrawingHints="1" hasScaleBasedVisibilityFlag="0" readOnly="0" labelsEnabled="0" maxScale="0" version="3.4.1-Madeira" simplifyDrawingTol="1" styleCategories="AllStyleCategories" simplifyLocal="1" simplifyAlgorithm="0" simplifyMaxScale="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" enableorderby="0" type="singleSymbol" symbollevels="0">
    <symbols>
      <symbol name="0" type="fill" alpha="1" clip_to_extent="1">
        <layer class="SimpleFill" pass="0" enabled="1" locked="0">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="236,245,57,0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="31,120,250,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.46"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="LinePatternFill" pass="0" enabled="1" locked="0">
          <prop k="angle" v="45"/>
          <prop k="color" v="0,0,0,255"/>
          <prop k="distance" v="2"/>
          <prop k="distance_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="distance_unit" v="MM"/>
          <prop k="line_width" v="0.5"/>
          <prop k="line_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@0@1" type="line" alpha="1" clip_to_extent="1">
            <layer class="SimpleLine" pass="0" enabled="1" locked="0">
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="MM"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="31,120,180,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="0.15"/>
              <prop k="line_width_unit" v="MM"/>
              <prop k="offset" v="0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties"/>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property key="dualview/previewExpressions">
      <value>COALESCE( "fid", '&lt;NULL>' )</value>
      <value>COALESCE( "fid", '&lt;NULL>' )</value>
      <value>COALESCE( "fid", '&lt;NULL>' )</value>
      <value>COALESCE( "fid", '&lt;NULL>' )</value>
    </property>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory scaleBasedVisibility="0" lineSizeScale="3x:0,0,0,0,0,0" labelPlacementMethod="XHeight" enabled="0" lineSizeType="MM" diagramOrientation="Up" penWidth="0" minScaleDenominator="0" minimumSize="0" sizeScale="3x:0,0,0,0,0,0" width="15" scaleDependency="Area" height="15" rotationOffset="270" backgroundColor="#ffffff" penAlpha="255" barWidth="5" penColor="#000000" opacity="1" backgroundAlpha="255" maxScaleDenominator="1e+08" sizeType="MM">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute color="#000000" label="" field=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings obstacle="0" linePlacementFlags="18" placement="1" priority="0" showAll="1" zIndex="0" dist="0">
    <properties>
      <Option type="Map">
        <Option name="name" value="" type="QString"/>
        <Option name="properties"/>
        <Option name="type" value="collection" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="fid">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="commento">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="proc_parz">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option name="AllowMulti" value="false" type="bool"/>
            <Option name="AllowNull" value="false" type="bool"/>
            <Option name="FilterExpression" value="" type="QString"/>
            <Option name="Key" value="code" type="QString"/>
            <Option name="Layer" value="pns_proc_dettagliato_42d5083d_9481_4c15_82e1_40c16db8ddbe" type="QString"/>
            <Option name="NofColumns" value="1" type="int"/>
            <Option name="OrderByValue" value="false" type="bool"/>
            <Option name="UseCompleter" value="false" type="bool"/>
            <Option name="Value" value="description_i" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="fonte_proc">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="No. identificativo" field="fid"/>
    <alias index="1" name="Osservazioni o ev. commento" field="commento"/>
    <alias index="2" name="Processo rappresentato TI" field="proc_parz"/>
    <alias index="3" name="Fonte del processo (es. nome riale, nome valle, nome località)" field="fonte_proc"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" applyOnUpdate="0" field="fid"/>
    <default expression="" applyOnUpdate="0" field="commento"/>
    <default expression="" applyOnUpdate="0" field="proc_parz"/>
    <default expression="" applyOnUpdate="0" field="fonte_proc"/>
  </defaults>
  <constraints>
    <constraint constraints="3" exp_strength="0" unique_strength="1" field="fid" notnull_strength="1"/>
    <constraint constraints="0" exp_strength="0" unique_strength="0" field="commento" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" unique_strength="0" field="proc_parz" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" unique_strength="0" field="fonte_proc" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="fid" desc=""/>
    <constraint exp="" field="commento" desc=""/>
    <constraint exp="" field="proc_parz" desc=""/>
    <constraint exp="" field="fonte_proc" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="">
    <columns>
      <column hidden="0" name="fid" type="field" width="-1"/>
      <column hidden="0" name="proc_parz" type="field" width="-1"/>
      <column hidden="0" name="fonte_proc" type="field" width="-1"/>
      <column hidden="0" name="commento" type="field" width="-1"/>
      <column hidden="1" type="actions" width="-1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath>F:/UPIP/06_StrumentiGis/02_Progetti base/02_Qgis/Qgs/00_Pericoli naturali</editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer showLabel="1" visibilityExpressionEnabled="0" name="Dati principali" groupBox="0" visibilityExpression="" columnCount="1">
      <attributeEditorField index="2" showLabel="1" name="proc_parz"/>
      <attributeEditorField index="3" showLabel="1" name="fonte_proc"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" visibilityExpressionEnabled="0" name="Dati secondari" groupBox="0" visibilityExpression="" columnCount="1">
      <attributeEditorField index="0" showLabel="1" name="fid"/>
      <attributeEditorField index="1" showLabel="1" name="commento"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="commento" editable="1"/>
    <field name="fid" editable="1"/>
    <field name="fonte_proc" editable="1"/>
    <field name="proc_parz" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="commento" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="fonte_proc" labelOnTop="0"/>
    <field name="proc_parz" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>COALESCE( "fid", '&lt;NULL>' )</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
