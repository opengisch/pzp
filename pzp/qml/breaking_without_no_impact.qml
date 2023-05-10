<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.16.12-Hannover" styleCategories="Symbology|Labeling|Fields|Forms" labelsEnabled="0">
  <renderer-v2 forceraster="0" symbollevels="1" attr="classe_intensita" enableorderby="0" type="categorizedSymbol">
    <categories>
      <category symbol="0" value="1004" label="forte" render="true"/>
      <category symbol="1" value="1003" label="medio" render="true"/>
      <category symbol="2" value="1002" label="debole" render="true"/>
    </categories>
    <symbols>
      <symbol clip_to_extent="1" alpha="1" type="fill" name="0" force_rhr="0">
        <layer pass="5" class="SimpleFill" locked="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="56,158,0,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="35,35,35,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.26"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" alpha="1" type="fill" name="1" force_rhr="0">
        <layer pass="4" class="SimpleFill" locked="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="83,212,0,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="35,35,35,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.26"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" alpha="1" type="fill" name="2" force_rhr="0">
        <layer pass="3" class="SimpleFill" locked="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="209,255,115,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="35,35,35,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.26"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <source-symbol>
      <symbol clip_to_extent="1" alpha="1" type="fill" name="0" force_rhr="0">
        <layer pass="0" class="SimpleFill" locked="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="0,0,255,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="35,35,35,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.26"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </source-symbol>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <fieldConfiguration>
    <field configurationFlags="None" name="fid">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="osservazioni">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="prob_rottura">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" value="1003" name="Alta"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="1002" name="Media"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="1001" name="Bassa"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="1000" name="Molto bassa"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="classe_intensita">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" value="1002" name="Debole"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="1003" name="Medio"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="1004" name="Forte"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="fonte_proc">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="proc_parz">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="proc_parz_ch">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="AllowMulti"/>
            <Option type="bool" value="false" name="AllowNull"/>
            <Option type="QString" value="" name="Description"/>
            <Option type="QString" value="CASE&#xa;WHEN current_value ( 'proc_parz' ) = 0 THEN &quot;code&quot; = 0&#xa;WHEN current_value ( 'proc_parz' ) = 1110 THEN &quot;code&quot; = 1100&#xa;WHEN current_value ( 'proc_parz' ) = 1120 THEN &quot;code&quot; = 1100 &#xa;WHEN current_value ( 'proc_parz' ) = 1130 THEN &quot;code&quot; = 1100 &#xa;WHEN current_value ( 'proc_parz' ) = 1200 THEN &quot;code&quot; = 1200 &#xa;WHEN current_value ( 'proc_parz' ) = 1300 THEN &quot;code&quot; = 1300 &#xa;WHEN current_value ( 'proc_parz' ) = 1400 THEN &quot;code&quot; = 0 &#xa;WHEN current_value ( 'proc_parz' ) = 2001 THEN &quot;code&quot; = 2210 &#xa;WHEN current_value ( 'proc_parz' ) = 2002 THEN &quot;code&quot; = 2220 &#xa;WHEN current_value ( 'proc_parz' ) = 2003 THEN &quot;code&quot; = 2100 &#xa;WHEN current_value ( 'proc_parz' ) = 2004 THEN &quot;code&quot; = 2210 &#xa;WHEN current_value ( 'proc_parz' ) = 3000 THEN &quot;code&quot; = 3100 &#xa;WHEN current_value ( 'proc_parz' ) = 3001 THEN &quot;code&quot; = 3200 &#xa;WHEN current_value ( 'proc_parz' ) = 3002 THEN &quot;code&quot; = 3200 &#xa;WHEN current_value ( 'proc_parz' ) = 4100 THEN &quot;code&quot; = 4100 &#xa;WHEN current_value ( 'proc_parz' ) = 4200 THEN &quot;code&quot; = 4200 &#xa;WHEN current_value ( 'proc_parz' ) = 4300 THEN &quot;code&quot; = 4300 &#xa;ELSE NULL&#xa;END" name="FilterExpression"/>
            <Option type="QString" value="" name="Key"/>
            <Option type="QString" value="" name="Layer"/>
            <Option type="QString" value="" name="LayerName"/>
            <Option type="QString" value="" name="LayerProviderName"/>
            <Option type="QString" value="" name="LayerSource"/>
            <Option type="int" value="1" name="NofColumns"/>
            <Option type="bool" value="false" name="OrderByValue"/>
            <Option type="bool" value="false" name="UseCompleter"/>
            <Option type="QString" value="" name="Value"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="liv_dettaglio">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="AllowMulti"/>
            <Option type="bool" value="true" name="AllowNull"/>
            <Option type="QString" value="" name="Description"/>
            <Option type="QString" value="" name="FilterExpression"/>
            <Option type="QString" value="" name="Key"/>
            <Option type="QString" value="" name="Layer"/>
            <Option type="QString" value="" name="LayerName"/>
            <Option type="QString" value="" name="LayerProviderName"/>
            <Option type="QString" value="" name="LayerSource"/>
            <Option type="int" value="1" name="NofColumns"/>
            <Option type="bool" value="false" name="OrderByValue"/>
            <Option type="bool" value="false" name="UseCompleter"/>
            <Option type="QString" value="" name="Value"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="scala">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="AllowMulti"/>
            <Option type="bool" value="true" name="AllowNull"/>
            <Option type="QString" value="" name="Description"/>
            <Option type="QString" value="" name="FilterExpression"/>
            <Option type="QString" value="" name="Key"/>
            <Option type="QString" value="" name="Layer"/>
            <Option type="QString" value="" name="LayerName"/>
            <Option type="QString" value="" name="LayerProviderName"/>
            <Option type="QString" value="" name="LayerSource"/>
            <Option type="int" value="1" name="NofColumns"/>
            <Option type="bool" value="false" name="OrderByValue"/>
            <Option type="bool" value="false" name="UseCompleter"/>
            <Option type="QString" value="" name="Value"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="" field="fid"/>
    <alias index="1" name="Osservazioni" field="osservazioni"/>
    <alias index="2" name="Probabilità di rottura" field="prob_rottura"/>
    <alias index="3" name="Intensità/impatto del processo" field="classe_intensita"/>
    <alias index="4" name="Fonte del processo (es. nome riale)" field="fonte_proc"/>
    <alias index="5" name="Processo rappresentato TI" field="proc_parz"/>
    <alias index="6" name="Processo rappresentato CH" field="proc_parz_ch"/>
    <alias index="7" name="Precisione del lavoro" field="liv_dettaglio"/>
    <alias index="8" name="Scala di rappresentazione" field="scala"/>
  </aliases>
  <defaults>
    <default expression="" applyOnUpdate="0" field="fid"/>
    <default expression="" applyOnUpdate="0" field="osservazioni"/>
    <default expression="" applyOnUpdate="0" field="prob_rottura"/>
    <default expression="" applyOnUpdate="0" field="classe_intensita"/>
    <default expression="" applyOnUpdate="0" field="fonte_proc"/>
    <default expression="" applyOnUpdate="0" field="proc_parz"/>
    <default expression="" applyOnUpdate="0" field="proc_parz_ch"/>
    <default expression="" applyOnUpdate="0" field="liv_dettaglio"/>
    <default expression="" applyOnUpdate="0" field="scala"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" exp_strength="0" unique_strength="1" constraints="3" field="fid"/>
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" constraints="0" field="osservazioni"/>
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" constraints="0" field="prob_rottura"/>
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" constraints="0" field="classe_intensita"/>
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" constraints="0" field="fonte_proc"/>
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" constraints="0" field="proc_parz"/>
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" constraints="0" field="proc_parz_ch"/>
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" constraints="0" field="liv_dettaglio"/>
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" constraints="0" field="scala"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="fid"/>
    <constraint exp="" desc="" field="osservazioni"/>
    <constraint exp="" desc="" field="prob_rottura"/>
    <constraint exp="" desc="" field="classe_intensita"/>
    <constraint exp="" desc="" field="fonte_proc"/>
    <constraint exp="" desc="" field="proc_parz"/>
    <constraint exp="" desc="" field="proc_parz_ch"/>
    <constraint exp="" desc="" field="liv_dettaglio"/>
    <constraint exp="" desc="" field="scala"/>
  </constraintExpressions>
  <expressionfields/>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath>/home/01_GeologiaValanghe/02_PZP/Capriasca_PZP/06_Estraz_dati/Dati inviati/Qgs/00_Pericoli naturali</editforminitfilepath>
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
    <attributeEditorContainer visibilityExpressionEnabled="0" columnCount="1" groupBox="0" visibilityExpression="" name="Dati principali" showLabel="1">
      <attributeEditorField index="5" name="proc_parz" showLabel="1"/>
      <attributeEditorField index="2" name="prob_rottura" showLabel="1"/>
      <attributeEditorField index="3" name="classe_intensita" showLabel="1"/>
      <attributeEditorField index="4" name="fonte_proc" showLabel="1"/>
      <attributeEditorField index="1" name="osservazioni" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer visibilityExpressionEnabled="0" columnCount="1" groupBox="0" visibilityExpression="" name="Dati secondari" showLabel="1">
      <attributeEditorField index="6" name="proc_parz_ch" showLabel="1"/>
      <attributeEditorField index="7" name="liv_dettaglio" showLabel="1"/>
      <attributeEditorField index="8" name="scala" showLabel="1"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="0" name="area"/>
    <field editable="1" name="classe_intensita"/>
    <field editable="1" name="commento"/>
    <field editable="1" name="fid"/>
    <field editable="1" name="fonte"/>
    <field editable="1" name="fonte_proc"/>
    <field editable="1" name="liv_dettaglio"/>
    <field editable="1" name="matrice"/>
    <field editable="1" name="osservazioni"/>
    <field editable="1" name="periodo_ritorno"/>
    <field editable="1" name="prob_accadimento"/>
    <field editable="1" name="prob_propagazione"/>
    <field editable="1" name="prob_rottura"/>
    <field editable="0" name="proc_parz"/>
    <field editable="1" name="proc_parz_ch"/>
    <field editable="1" name="scala"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="area"/>
    <field labelOnTop="0" name="classe_intensita"/>
    <field labelOnTop="1" name="commento"/>
    <field labelOnTop="0" name="fid"/>
    <field labelOnTop="0" name="fonte"/>
    <field labelOnTop="0" name="fonte_proc"/>
    <field labelOnTop="0" name="liv_dettaglio"/>
    <field labelOnTop="0" name="matrice"/>
    <field labelOnTop="0" name="osservazioni"/>
    <field labelOnTop="0" name="periodo_ritorno"/>
    <field labelOnTop="0" name="prob_accadimento"/>
    <field labelOnTop="0" name="prob_propagazione"/>
    <field labelOnTop="0" name="prob_rottura"/>
    <field labelOnTop="0" name="proc_parz"/>
    <field labelOnTop="0" name="proc_parz_ch"/>
    <field labelOnTop="0" name="scala"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <layerGeometryType>2</layerGeometryType>
</qgis>
