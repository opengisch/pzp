<qgis labelsEnabled="0" styleCategories="Symbology|Labeling|Fields|Forms" version="3.16.12-Hannover">
  <renderer-v2 attr="classe_intensita" enableorderby="0" forceraster="0" symbollevels="1" type="categorizedSymbol">
    <categories>
      <category label="forte" render="true" symbol="0" value="1004"></category>
      <category label="medio" render="true" symbol="1" value="1003"></category>
      <category label="debole" render="true" symbol="2" value="1002"></category>
    </categories>
    <symbols>
      <symbol alpha="1" clip_to_extent="1" force_rhr="0" name="0" type="fill">
        <layer class="SimpleFill" enabled="1" locked="0" pass="5">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"></prop>
          <prop k="color" v="56,158,0,255"></prop>
          <prop k="joinstyle" v="bevel"></prop>
          <prop k="offset" v="0,0"></prop>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"></prop>
          <prop k="offset_unit" v="MM"></prop>
          <prop k="outline_color" v="35,35,35,255"></prop>
          <prop k="outline_style" v="solid"></prop>
          <prop k="outline_width" v="0.26"></prop>
          <prop k="outline_width_unit" v="MM"></prop>
          <prop k="style" v="solid"></prop>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""></Option>
              <Option name="properties"></Option>
              <Option name="type" type="QString" value="collection"></Option>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" force_rhr="0" name="1" type="fill">
        <layer class="SimpleFill" enabled="1" locked="0" pass="4">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"></prop>
          <prop k="color" v="83,212,0,255"></prop>
          <prop k="joinstyle" v="bevel"></prop>
          <prop k="offset" v="0,0"></prop>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"></prop>
          <prop k="offset_unit" v="MM"></prop>
          <prop k="outline_color" v="35,35,35,255"></prop>
          <prop k="outline_style" v="solid"></prop>
          <prop k="outline_width" v="0.26"></prop>
          <prop k="outline_width_unit" v="MM"></prop>
          <prop k="style" v="solid"></prop>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""></Option>
              <Option name="properties"></Option>
              <Option name="type" type="QString" value="collection"></Option>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" force_rhr="0" name="2" type="fill">
        <layer class="SimpleFill" enabled="1" locked="0" pass="3">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"></prop>
          <prop k="color" v="209,255,115,255"></prop>
          <prop k="joinstyle" v="bevel"></prop>
          <prop k="offset" v="0,0"></prop>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"></prop>
          <prop k="offset_unit" v="MM"></prop>
          <prop k="outline_color" v="35,35,35,255"></prop>
          <prop k="outline_style" v="solid"></prop>
          <prop k="outline_width" v="0.26"></prop>
          <prop k="outline_width_unit" v="MM"></prop>
          <prop k="style" v="solid"></prop>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""></Option>
              <Option name="properties"></Option>
              <Option name="type" type="QString" value="collection"></Option>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <source-symbol>
      <symbol alpha="1" clip_to_extent="1" force_rhr="0" name="0" type="fill">
        <layer class="SimpleFill" enabled="1" locked="0" pass="0">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"></prop>
          <prop k="color" v="0,0,255,255"></prop>
          <prop k="joinstyle" v="bevel"></prop>
          <prop k="offset" v="0,0"></prop>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"></prop>
          <prop k="offset_unit" v="MM"></prop>
          <prop k="outline_color" v="35,35,35,255"></prop>
          <prop k="outline_style" v="solid"></prop>
          <prop k="outline_width" v="0.26"></prop>
          <prop k="outline_width_unit" v="MM"></prop>
          <prop k="style" v="solid"></prop>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""></Option>
              <Option name="properties"></Option>
              <Option name="type" type="QString" value="collection"></Option>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </source-symbol>
    <rotation></rotation>
    <sizescale></sizescale>
  </renderer-v2>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <fieldConfiguration>
    <field configurationFlags="None" name="fid">
      <editWidget type="TextEdit">
        <config>
          <Option></Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="osservazioni">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"></Option>
            <Option name="UseHtml" type="bool" value="false"></Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="prob_rottura">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="Alta" type="QString" value="1003"></Option>
              </Option>
              <Option type="Map">
                <Option name="Media" type="QString" value="1002"></Option>
              </Option>
              <Option type="Map">
                <Option name="Bassa" type="QString" value="1001"></Option>
              </Option>
              <Option type="Map">
                <Option name="Molto bassa" type="QString" value="1000"></Option>
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
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="Debole" type="QString" value="1002"></Option>
              </Option>
              <Option type="Map">
                <Option name="Medio" type="QString" value="1003"></Option>
              </Option>
              <Option type="Map">
                <Option name="Forte" type="QString" value="1004"></Option>
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
            <Option name="IsMultiline" type="bool" value="false"></Option>
            <Option name="UseHtml" type="bool" value="false"></Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="proc_parz">
      <editWidget type="Range">
        <config>
          <Option></Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="proc_parz_ch">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option name="AllowMulti" type="bool" value="false"></Option>
            <Option name="AllowNull" type="bool" value="false"></Option>
            <Option name="Description" type="QString" value=""></Option>
            <Option name="FilterExpression" type="QString" value="CASE&#xA;WHEN current_value ( 'proc_parz' ) = 0 THEN &quot;code&quot; = 0&#xA;WHEN current_value ( 'proc_parz' ) = 1110 THEN &quot;code&quot; = 1100&#xA;WHEN current_value ( 'proc_parz' ) = 1120 THEN &quot;code&quot; = 1100 &#xA;WHEN current_value ( 'proc_parz' ) = 1130 THEN &quot;code&quot; = 1100 &#xA;WHEN current_value ( 'proc_parz' ) = 1200 THEN &quot;code&quot; = 1200 &#xA;WHEN current_value ( 'proc_parz' ) = 1300 THEN &quot;code&quot; = 1300 &#xA;WHEN current_value ( 'proc_parz' ) = 1400 THEN &quot;code&quot; = 0 &#xA;WHEN current_value ( 'proc_parz' ) = 2001 THEN &quot;code&quot; = 2210 &#xA;WHEN current_value ( 'proc_parz' ) = 2002 THEN &quot;code&quot; = 2220 &#xA;WHEN current_value ( 'proc_parz' ) = 2003 THEN &quot;code&quot; = 2100 &#xA;WHEN current_value ( 'proc_parz' ) = 2004 THEN &quot;code&quot; = 2210 &#xA;WHEN current_value ( 'proc_parz' ) = 3000 THEN &quot;code&quot; = 3100 &#xA;WHEN current_value ( 'proc_parz' ) = 3001 THEN &quot;code&quot; = 3200 &#xA;WHEN current_value ( 'proc_parz' ) = 3002 THEN &quot;code&quot; = 3200 &#xA;WHEN current_value ( 'proc_parz' ) = 4100 THEN &quot;code&quot; = 4100 &#xA;WHEN current_value ( 'proc_parz' ) = 4200 THEN &quot;code&quot; = 4200 &#xA;WHEN current_value ( 'proc_parz' ) = 4300 THEN &quot;code&quot; = 4300 &#xA;ELSE NULL&#xA;END"></Option>
            <Option name="Key" type="QString" value=""></Option>
            <Option name="Layer" type="QString" value=""></Option>
            <Option name="LayerName" type="QString" value=""></Option>
            <Option name="LayerProviderName" type="QString" value=""></Option>
            <Option name="LayerSource" type="QString" value=""></Option>
            <Option name="NofColumns" type="int" value="1"></Option>
            <Option name="OrderByValue" type="bool" value="false"></Option>
            <Option name="UseCompleter" type="bool" value="false"></Option>
            <Option name="Value" type="QString" value=""></Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="liv_dettaglio">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option name="AllowMulti" type="bool" value="false"></Option>
            <Option name="AllowNull" type="bool" value="true"></Option>
            <Option name="Description" type="QString" value=""></Option>
            <Option name="FilterExpression" type="QString" value=""></Option>
            <Option name="Key" type="QString" value=""></Option>
            <Option name="Layer" type="QString" value=""></Option>
            <Option name="LayerName" type="QString" value=""></Option>
            <Option name="LayerProviderName" type="QString" value=""></Option>
            <Option name="LayerSource" type="QString" value=""></Option>
            <Option name="NofColumns" type="int" value="1"></Option>
            <Option name="OrderByValue" type="bool" value="false"></Option>
            <Option name="UseCompleter" type="bool" value="false"></Option>
            <Option name="Value" type="QString" value=""></Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="scala">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option name="AllowMulti" type="bool" value="false"></Option>
            <Option name="AllowNull" type="bool" value="true"></Option>
            <Option name="Description" type="QString" value=""></Option>
            <Option name="FilterExpression" type="QString" value=""></Option>
            <Option name="Key" type="QString" value=""></Option>
            <Option name="Layer" type="QString" value=""></Option>
            <Option name="LayerName" type="QString" value=""></Option>
            <Option name="LayerProviderName" type="QString" value=""></Option>
            <Option name="LayerSource" type="QString" value=""></Option>
            <Option name="NofColumns" type="int" value="1"></Option>
            <Option name="OrderByValue" type="bool" value="false"></Option>
            <Option name="UseCompleter" type="bool" value="false"></Option>
            <Option name="Value" type="QString" value=""></Option>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="fid" index="0" name=""></alias>
    <alias field="osservazioni" index="1" name="Osservazioni"></alias>
    <alias field="prob_rottura" index="2" name="Probabilità di rottura"></alias>
    <alias field="classe_intensita" index="3" name="Intensità/impatto del processo"></alias>
    <alias field="fonte_proc" index="4" name="Fonte del processo (es. nome riale)"></alias>
    <alias field="proc_parz" index="5" name="Processo rappresentato TI"></alias>
    <alias field="proc_parz_ch" index="6" name="Processo rappresentato CH"></alias>
    <alias field="liv_dettaglio" index="7" name="Precisione del lavoro"></alias>
    <alias field="scala" index="8" name="Scala di rappresentazione"></alias>
  </aliases>
  <defaults>
    <default applyOnUpdate="0" expression="" field="fid"></default>
    <default applyOnUpdate="0" expression="" field="osservazioni"></default>
    <default applyOnUpdate="0" expression="" field="prob_rottura"></default>
    <default applyOnUpdate="0" expression="" field="classe_intensita"></default>
    <default applyOnUpdate="0" expression="" field="fonte_proc"></default>
    <default applyOnUpdate="0" expression="" field="proc_parz"></default>
    <default applyOnUpdate="0" expression="" field="proc_parz_ch"></default>
    <default applyOnUpdate="0" expression="" field="liv_dettaglio"></default>
    <default applyOnUpdate="0" expression="" field="scala"></default>
  </defaults>
  <constraints>
    <constraint constraints="3" exp_strength="0" field="fid" notnull_strength="1" unique_strength="1"></constraint>
    <constraint constraints="0" exp_strength="0" field="osservazioni" notnull_strength="0" unique_strength="0"></constraint>
    <constraint constraints="0" exp_strength="0" field="prob_rottura" notnull_strength="0" unique_strength="0"></constraint>
    <constraint constraints="0" exp_strength="0" field="classe_intensita" notnull_strength="0" unique_strength="0"></constraint>
    <constraint constraints="0" exp_strength="0" field="fonte_proc" notnull_strength="0" unique_strength="0"></constraint>
    <constraint constraints="0" exp_strength="0" field="proc_parz" notnull_strength="0" unique_strength="0"></constraint>
    <constraint constraints="0" exp_strength="0" field="proc_parz_ch" notnull_strength="0" unique_strength="0"></constraint>
    <constraint constraints="0" exp_strength="0" field="liv_dettaglio" notnull_strength="0" unique_strength="0"></constraint>
    <constraint constraints="0" exp_strength="0" field="scala" notnull_strength="0" unique_strength="0"></constraint>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="fid"></constraint>
    <constraint desc="" exp="" field="osservazioni"></constraint>
    <constraint desc="" exp="" field="prob_rottura"></constraint>
    <constraint desc="" exp="" field="classe_intensita"></constraint>
    <constraint desc="" exp="" field="fonte_proc"></constraint>
    <constraint desc="" exp="" field="proc_parz"></constraint>
    <constraint desc="" exp="" field="proc_parz_ch"></constraint>
    <constraint desc="" exp="" field="liv_dettaglio"></constraint>
    <constraint desc="" exp="" field="scala"></constraint>
  </constraintExpressions>
  <expressionfields></expressionfields>
  <editform tolerant="1"></editform>
  <editforminit></editforminit>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath>/home/01_GeologiaValanghe/02_PZP/Capriasca_PZP/06_Estraz_dati/Dati inviati/Qgs/00_Pericoli naturali</editforminitfilepath>
  <editforminitcode># -*- coding: utf-8 -*-
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
</editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer columnCount="1" groupBox="0" name="Dati principali" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0">
      <attributeEditorField index="5" name="proc_parz" showLabel="1"></attributeEditorField>
      <attributeEditorField index="2" name="prob_rottura" showLabel="1"></attributeEditorField>
      <attributeEditorField index="3" name="classe_intensita" showLabel="1"></attributeEditorField>
      <attributeEditorField index="4" name="fonte_proc" showLabel="1"></attributeEditorField>
      <attributeEditorField index="1" name="osservazioni" showLabel="1"></attributeEditorField>
    </attributeEditorContainer>
    <attributeEditorContainer columnCount="1" groupBox="0" name="Dati secondari" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0">
      <attributeEditorField index="6" name="proc_parz_ch" showLabel="1"></attributeEditorField>
      <attributeEditorField index="7" name="liv_dettaglio" showLabel="1"></attributeEditorField>
      <attributeEditorField index="8" name="scala" showLabel="1"></attributeEditorField>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="0" name="area"></field>
    <field editable="1" name="classe_intensita"></field>
    <field editable="1" name="commento"></field>
    <field editable="1" name="fid"></field>
    <field editable="1" name="fonte"></field>
    <field editable="1" name="fonte_proc"></field>
    <field editable="1" name="liv_dettaglio"></field>
    <field editable="1" name="matrice"></field>
    <field editable="1" name="osservazioni"></field>
    <field editable="1" name="periodo_ritorno"></field>
    <field editable="1" name="prob_accadimento"></field>
    <field editable="1" name="prob_propagazione"></field>
    <field editable="1" name="prob_rottura"></field>
    <field editable="0" name="proc_parz"></field>
    <field editable="1" name="proc_parz_ch"></field>
    <field editable="1" name="scala"></field>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="area"></field>
    <field labelOnTop="0" name="classe_intensita"></field>
    <field labelOnTop="1" name="commento"></field>
    <field labelOnTop="0" name="fid"></field>
    <field labelOnTop="0" name="fonte"></field>
    <field labelOnTop="0" name="fonte_proc"></field>
    <field labelOnTop="0" name="liv_dettaglio"></field>
    <field labelOnTop="0" name="matrice"></field>
    <field labelOnTop="0" name="osservazioni"></field>
    <field labelOnTop="0" name="periodo_ritorno"></field>
    <field labelOnTop="0" name="prob_accadimento"></field>
    <field labelOnTop="0" name="prob_propagazione"></field>
    <field labelOnTop="0" name="prob_rottura"></field>
    <field labelOnTop="0" name="proc_parz"></field>
    <field labelOnTop="0" name="proc_parz_ch"></field>
    <field labelOnTop="0" name="scala"></field>
  </labelOnTop>
  <dataDefinedFieldProperties></dataDefinedFieldProperties>
  <widgets></widgets>
  <layerGeometryType>2</layerGeometryType>
</qgis>
