<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.16.12-Hannover" labelsEnabled="0" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms" readOnly="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 type="singleSymbol" symbollevels="0" enableorderby="0" forceraster="0">
    <symbols>
      <symbol type="fill" name="0" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer enabled="1" class="SimpleFill" locked="0" pass="0">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="0,0,255,0" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="31,120,250,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.46" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer enabled="1" class="LinePatternFill" locked="0" pass="0">
          <prop v="45" k="angle"/>
          <prop v="0,0,0,255" k="color"/>
          <prop v="2" k="distance"/>
          <prop v="3x:0,0,0,0,0,0" k="distance_map_unit_scale"/>
          <prop v="MM" k="distance_unit"/>
          <prop v="0.5" k="line_width"/>
          <prop v="3x:0,0,0,0,0,0" k="line_width_map_unit_scale"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol type="line" name="@0@1" clip_to_extent="1" alpha="1" force_rhr="0">
            <layer enabled="1" class="SimpleLine" locked="0" pass="0">
              <prop v="0" k="align_dash_pattern"/>
              <prop v="square" k="capstyle"/>
              <prop v="5;2" k="customdash"/>
              <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
              <prop v="MM" k="customdash_unit"/>
              <prop v="0" k="dash_pattern_offset"/>
              <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
              <prop v="MM" k="dash_pattern_offset_unit"/>
              <prop v="0" k="draw_inside_polygon"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="31,120,180,255" k="line_color"/>
              <prop v="solid" k="line_style"/>
              <prop v="0.15" k="line_width"/>
              <prop v="MM" k="line_width_unit"/>
              <prop v="0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="0" k="ring_filter"/>
              <prop v="0" k="tweak_dash_pattern_on_corners"/>
              <prop v="0" k="use_custom_dash"/>
              <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
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
    <alias index="0" name="" field="fid"/>
    <alias index="1" name="Commento" field="commento"/>
    <alias index="2" name="Processo" field="proc_parz"/>
    <alias index="3" name="Fonte processo" field="fonte_proc"/>
  </aliases>
  <defaults>
    <default field="fid" applyOnUpdate="0" expression=""/>
    <default field="commento" applyOnUpdate="0" expression=""/>
    <default field="proc_parz" applyOnUpdate="0" expression="@pzp_process"/>
    <default field="fonte_proc" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" exp_strength="0" field="fid" constraints="3" notnull_strength="1"/>
    <constraint unique_strength="0" exp_strength="0" field="commento" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" exp_strength="0" field="proc_parz" constraints="1" notnull_strength="1"/>
    <constraint unique_strength="1" exp_strength="0" field="fonte_proc" constraints="3" notnull_strength="1"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" exp="" desc=""/>
    <constraint field="commento" exp="" desc=""/>
    <constraint field="proc_parz" exp="" desc=""/>
    <constraint field="fonte_proc" exp="" desc=""/>
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
    <attributeEditorField index="2" showLabel="1" name="proc_parz"/>
    <attributeEditorField index="3" showLabel="1" name="fonte_proc"/>
    <attributeEditorField index="1" showLabel="1" name="commento"/>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="commento"/>
    <field editable="1" name="fid"/>
    <field editable="1" name="fonte_proc"/>
    <field editable="0" name="proc_parz"/>
  </editable>
  <labelOnTop>
    <field name="commento" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="fonte_proc" labelOnTop="0"/>
    <field name="proc_parz" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"commento"</previewExpression>
  <layerGeometryType>2</layerGeometryType>
</qgis>
