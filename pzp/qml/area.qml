<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.16.16-Hannover" styleCategories="Symbology|Fields|Forms">
  <renderer-v2 type="singleSymbol" symbollevels="0" enableorderby="0" forceraster="0">
    <symbols>
      <symbol type="fill" force_rhr="0" name="0" clip_to_extent="1" alpha="1">
        <layer locked="0" pass="0" class="SimpleFill" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="0,0,255,0"/>
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" pass="0" class="LinePatternFill" enabled="1">
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol type="line" force_rhr="0" name="@0@1" clip_to_extent="1" alpha="1">
            <layer locked="0" pass="0" class="SimpleLine" enabled="1">
              <prop k="align_dash_pattern" v="0"/>
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="MM"/>
              <prop k="dash_pattern_offset" v="0"/>
              <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="dash_pattern_offset_unit" v="MM"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="31,120,180,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="0.15"/>
              <prop k="line_width_unit" v="MM"/>
              <prop k="offset" v="0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="ring_filter" v="0"/>
              <prop k="tweak_dash_pattern_on_corners" v="0"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option type="QString" name="name" value=""/>
                  <Option name="properties"/>
                  <Option type="QString" name="type" value="collection"/>
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
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <fieldConfiguration>
    <field name="fid" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="commento" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="proc_parz" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="Alluvionamento corso d'acqua minore" value="1110"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Alluvionamento corso d'acqua principale" value="1120"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Colata detritica di versante" value="2002"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Flusso detrito" value="1200"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Ruscellamento superficiale" value="1400"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Scivolamento spontaneo" value="2001"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Caduta sassi o blocchi" value="3000"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Valanga radente" value="4100"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Valanga polverosa" value="4200"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="fonte_proc" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" index="0" field="fid"/>
    <alias name="Osservazione o ev. commento" index="1" field="commento"/>
    <alias name="Processo rappresentato TI" index="2" field="proc_parz"/>
    <alias name="Fonte del processo (es. nome riale)" index="3" field="fonte_proc"/>
  </aliases>
  <defaults>
    <default field="fid" expression="" applyOnUpdate="0"/>
    <default field="commento" expression="" applyOnUpdate="0"/>
    <default field="proc_parz" expression="@pzp_process" applyOnUpdate="0"/>
    <default field="fonte_proc" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" field="fid" exp_strength="0" unique_strength="1" constraints="3"/>
    <constraint notnull_strength="0" field="commento" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="1" field="proc_parz" exp_strength="1" unique_strength="1" constraints="7"/>
    <constraint notnull_strength="1" field="fonte_proc" exp_strength="1" unique_strength="1" constraints="7"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="fid"/>
    <constraint desc="" exp="" field="commento"/>
    <constraint desc="" exp="" field="proc_parz"/>
    <constraint desc="" exp="" field="fonte_proc"/>
  </constraintExpressions>
  <expressionfields/>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
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
    <attributeEditorField showLabel="1" name="proc_parz" index="2"/>
    <attributeEditorField showLabel="1" name="fonte_proc" index="3"/>
    <attributeEditorField showLabel="1" name="commento" index="1"/>
  </attributeEditorForm>
  <editable>
    <field name="commento" editable="1"/>
    <field name="fid" editable="1"/>
    <field name="fonte_proc" editable="1"/>
    <field name="proc_parz" editable="0"/>
  </editable>
  <labelOnTop>
    <field name="commento" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="fonte_proc" labelOnTop="0"/>
    <field name="proc_parz" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <layerGeometryType>2</layerGeometryType>
</qgis>
