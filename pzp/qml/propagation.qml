<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="1" styleCategories="LayerConfiguration|Symbology|Labeling|Forms" readOnly="0" version="3.43.0-Master">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <renderer-v2 enableorderby="0" referencescale="-1" type="categorizedSymbol" symbollevels="0" forceraster="0" attr="prob_propagazione">
    <categories>
      <category render="true" uuid="0" value="1003" symbol="0" type="string" label="alta"/>
      <category render="true" uuid="1" value="1002" symbol="1" type="string" label="media"/>
      <category render="true" uuid="2" value="1001" symbol="2" type="string" label="bassa"/>
      <category render="false" uuid="3" value="" symbol="3" type="string" label=""/>
    </categories>
    <symbols>
      <symbol force_rhr="0" type="line" frame_rate="10" alpha="1" is_animated="0" clip_to_extent="1" name="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer id="{a2791384-74e0-4a62-868a-88575f8e3b9b}" pass="0" class="SimpleLine" enabled="1" locked="0">
          <Option type="Map">
            <Option value="0" type="QString" name="align_dash_pattern"/>
            <Option value="square" type="QString" name="capstyle"/>
            <Option value="5;2" type="QString" name="customdash"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="customdash_map_unit_scale"/>
            <Option value="MM" type="QString" name="customdash_unit"/>
            <Option value="0" type="QString" name="dash_pattern_offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="dash_pattern_offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="dash_pattern_offset_unit"/>
            <Option value="0" type="QString" name="draw_inside_polygon"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="227,26,28,255,rgb:0.8901960784313725,0.10196078431372549,0.10980392156862745,1" type="QString" name="line_color"/>
            <Option value="solid" type="QString" name="line_style"/>
            <Option value="0.26" type="QString" name="line_width"/>
            <Option value="MM" type="QString" name="line_width_unit"/>
            <Option value="0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="0" type="QString" name="ring_filter"/>
            <Option value="0" type="QString" name="trim_distance_end"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="trim_distance_end_map_unit_scale"/>
            <Option value="MM" type="QString" name="trim_distance_end_unit"/>
            <Option value="0" type="QString" name="trim_distance_start"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="trim_distance_start_map_unit_scale"/>
            <Option value="MM" type="QString" name="trim_distance_start_unit"/>
            <Option value="0" type="QString" name="tweak_dash_pattern_on_corners"/>
            <Option value="0" type="QString" name="use_custom_dash"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="width_map_unit_scale"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer id="{0780e612-1b38-4295-b40e-d59c11913cca}" pass="0" class="MarkerLine" enabled="1" locked="0">
          <Option type="Map">
            <Option value="4" type="QString" name="average_angle_length"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="average_angle_map_unit_scale"/>
            <Option value="MM" type="QString" name="average_angle_unit"/>
            <Option value="20" type="QString" name="interval"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="interval_map_unit_scale"/>
            <Option value="Point" type="QString" name="interval_unit"/>
            <Option value="-0.6" type="QString" name="offset"/>
            <Option value="0.5" type="QString" name="offset_along_line"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_along_line_map_unit_scale"/>
            <Option value="Point" type="QString" name="offset_along_line_unit"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="true" type="bool" name="place_on_every_part"/>
            <Option value="Interval" type="QString" name="placements"/>
            <Option value="0" type="QString" name="ring_filter"/>
            <Option value="1" type="QString" name="rotate"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
          <symbol force_rhr="0" type="marker" frame_rate="10" alpha="1" is_animated="0" clip_to_extent="1" name="@0@1">
            <data_defined_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name"/>
                <Option name="properties"/>
                <Option value="collection" type="QString" name="type"/>
              </Option>
            </data_defined_properties>
            <layer id="{2d747dd0-d5d1-422d-8d8d-bce1270a9abd}" pass="0" class="SimpleMarker" enabled="1" locked="0">
              <Option type="Map">
                <Option value="0" type="QString" name="angle"/>
                <Option value="square" type="QString" name="cap_style"/>
                <Option value="0,0,0,255,rgb:0,0,0,1" type="QString" name="color"/>
                <Option value="1" type="QString" name="horizontal_anchor_point"/>
                <Option value="bevel" type="QString" name="joinstyle"/>
                <Option value="equilateral_triangle" type="QString" name="name"/>
                <Option value="4.40000000000000036,4.40000000000000036" type="QString" name="offset"/>
                <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
                <Option value="Point" type="QString" name="offset_unit"/>
                <Option value="255,255,255,255,rgb:1,1,1,1" type="QString" name="outline_color"/>
                <Option value="solid" type="QString" name="outline_style"/>
                <Option value="0" type="QString" name="outline_width"/>
                <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
                <Option value="MM" type="QString" name="outline_width_unit"/>
                <Option value="area" type="QString" name="scale_method"/>
                <Option value="10" type="QString" name="size"/>
                <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
                <Option value="Pixel" type="QString" name="size_unit"/>
                <Option value="1" type="QString" name="vertical_anchor_point"/>
              </Option>
              <effect type="effectStack" enabled="0">
                <effect type="drawSource">
                  <Option type="Map">
                    <Option value="0" type="QString" name="blend_mode"/>
                    <Option value="2" type="QString" name="draw_mode"/>
                    <Option value="1" type="QString" name="enabled"/>
                    <Option value="1" type="QString" name="opacity"/>
                  </Option>
                </effect>
              </effect>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" type="QString" name="name"/>
                  <Option name="properties"/>
                  <Option value="collection" type="QString" name="type"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="line" frame_rate="10" alpha="1" is_animated="0" clip_to_extent="1" name="1">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer id="{1570a05b-798d-4f86-84ee-299d3e67dbce}" pass="0" class="SimpleLine" enabled="1" locked="0">
          <Option type="Map">
            <Option value="0" type="QString" name="align_dash_pattern"/>
            <Option value="square" type="QString" name="capstyle"/>
            <Option value="5;2" type="QString" name="customdash"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="customdash_map_unit_scale"/>
            <Option value="MM" type="QString" name="customdash_unit"/>
            <Option value="0" type="QString" name="dash_pattern_offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="dash_pattern_offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="dash_pattern_offset_unit"/>
            <Option value="0" type="QString" name="draw_inside_polygon"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="255,127,0,255,rgb:1,0.49803921568627452,0,1" type="QString" name="line_color"/>
            <Option value="dash" type="QString" name="line_style"/>
            <Option value="1.08" type="QString" name="line_width"/>
            <Option value="Point" type="QString" name="line_width_unit"/>
            <Option value="0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="Point" type="QString" name="offset_unit"/>
            <Option value="0" type="QString" name="ring_filter"/>
            <Option value="0" type="QString" name="trim_distance_end"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="trim_distance_end_map_unit_scale"/>
            <Option value="MM" type="QString" name="trim_distance_end_unit"/>
            <Option value="0" type="QString" name="trim_distance_start"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="trim_distance_start_map_unit_scale"/>
            <Option value="MM" type="QString" name="trim_distance_start_unit"/>
            <Option value="0" type="QString" name="tweak_dash_pattern_on_corners"/>
            <Option value="0" type="QString" name="use_custom_dash"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="width_map_unit_scale"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer id="{46ebdb28-028d-406d-8ca8-032d55f1045e}" pass="0" class="MarkerLine" enabled="1" locked="0">
          <Option type="Map">
            <Option value="4" type="QString" name="average_angle_length"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="average_angle_map_unit_scale"/>
            <Option value="MM" type="QString" name="average_angle_unit"/>
            <Option value="20" type="QString" name="interval"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="interval_map_unit_scale"/>
            <Option value="Point" type="QString" name="interval_unit"/>
            <Option value="-0.6" type="QString" name="offset"/>
            <Option value="0.5" type="QString" name="offset_along_line"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_along_line_map_unit_scale"/>
            <Option value="Point" type="QString" name="offset_along_line_unit"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="Point" type="QString" name="offset_unit"/>
            <Option value="true" type="bool" name="place_on_every_part"/>
            <Option value="Interval" type="QString" name="placements"/>
            <Option value="0" type="QString" name="ring_filter"/>
            <Option value="1" type="QString" name="rotate"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
          <symbol force_rhr="0" type="marker" frame_rate="10" alpha="1" is_animated="0" clip_to_extent="1" name="@1@1">
            <data_defined_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name"/>
                <Option name="properties"/>
                <Option value="collection" type="QString" name="type"/>
              </Option>
            </data_defined_properties>
            <layer id="{11d2cf12-bb1d-4943-9f61-cdea4c34c49a}" pass="0" class="SimpleMarker" enabled="1" locked="0">
              <Option type="Map">
                <Option value="0" type="QString" name="angle"/>
                <Option value="square" type="QString" name="cap_style"/>
                <Option value="0,0,0,255,rgb:0,0,0,1" type="QString" name="color"/>
                <Option value="1" type="QString" name="horizontal_anchor_point"/>
                <Option value="bevel" type="QString" name="joinstyle"/>
                <Option value="equilateral_triangle" type="QString" name="name"/>
                <Option value="4.40000000000000036,4.40000000000000036" type="QString" name="offset"/>
                <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
                <Option value="Point" type="QString" name="offset_unit"/>
                <Option value="255,255,255,255,rgb:1,1,1,1" type="QString" name="outline_color"/>
                <Option value="solid" type="QString" name="outline_style"/>
                <Option value="0" type="QString" name="outline_width"/>
                <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
                <Option value="MM" type="QString" name="outline_width_unit"/>
                <Option value="diameter" type="QString" name="scale_method"/>
                <Option value="10" type="QString" name="size"/>
                <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
                <Option value="Pixel" type="QString" name="size_unit"/>
                <Option value="1" type="QString" name="vertical_anchor_point"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" type="QString" name="name"/>
                  <Option name="properties"/>
                  <Option value="collection" type="QString" name="type"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="line" frame_rate="10" alpha="1" is_animated="0" clip_to_extent="1" name="2">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer id="{a1c724e9-0289-481e-ac21-f3fc86225f70}" pass="0" class="SimpleLine" enabled="1" locked="0">
          <Option type="Map">
            <Option value="0" type="QString" name="align_dash_pattern"/>
            <Option value="square" type="QString" name="capstyle"/>
            <Option value="5;2" type="QString" name="customdash"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="customdash_map_unit_scale"/>
            <Option value="MM" type="QString" name="customdash_unit"/>
            <Option value="0" type="QString" name="dash_pattern_offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="dash_pattern_offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="dash_pattern_offset_unit"/>
            <Option value="0" type="QString" name="draw_inside_polygon"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="line_color"/>
            <Option value="dot" type="QString" name="line_style"/>
            <Option value="1.08" type="QString" name="line_width"/>
            <Option value="Point" type="QString" name="line_width_unit"/>
            <Option value="0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="0" type="QString" name="ring_filter"/>
            <Option value="0" type="QString" name="trim_distance_end"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="trim_distance_end_map_unit_scale"/>
            <Option value="MM" type="QString" name="trim_distance_end_unit"/>
            <Option value="0" type="QString" name="trim_distance_start"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="trim_distance_start_map_unit_scale"/>
            <Option value="MM" type="QString" name="trim_distance_start_unit"/>
            <Option value="0" type="QString" name="tweak_dash_pattern_on_corners"/>
            <Option value="0" type="QString" name="use_custom_dash"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="width_map_unit_scale"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer id="{71305106-e631-4c6e-b111-8a6b4780542d}" pass="0" class="MarkerLine" enabled="1" locked="0">
          <Option type="Map">
            <Option value="4" type="QString" name="average_angle_length"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="average_angle_map_unit_scale"/>
            <Option value="MM" type="QString" name="average_angle_unit"/>
            <Option value="20" type="QString" name="interval"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="interval_map_unit_scale"/>
            <Option value="Point" type="QString" name="interval_unit"/>
            <Option value="-0.6" type="QString" name="offset"/>
            <Option value="0.5" type="QString" name="offset_along_line"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_along_line_map_unit_scale"/>
            <Option value="Point" type="QString" name="offset_along_line_unit"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="Point" type="QString" name="offset_unit"/>
            <Option value="true" type="bool" name="place_on_every_part"/>
            <Option value="Interval" type="QString" name="placements"/>
            <Option value="0" type="QString" name="ring_filter"/>
            <Option value="1" type="QString" name="rotate"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
          <symbol force_rhr="0" type="marker" frame_rate="10" alpha="1" is_animated="0" clip_to_extent="1" name="@2@1">
            <data_defined_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name"/>
                <Option name="properties"/>
                <Option value="collection" type="QString" name="type"/>
              </Option>
            </data_defined_properties>
            <layer id="{16f6e03c-63c4-4eb2-9ea8-3b448ef38d88}" pass="0" class="SimpleMarker" enabled="1" locked="0">
              <Option type="Map">
                <Option value="0" type="QString" name="angle"/>
                <Option value="square" type="QString" name="cap_style"/>
                <Option value="0,0,0,255,rgb:0,0,0,1" type="QString" name="color"/>
                <Option value="1" type="QString" name="horizontal_anchor_point"/>
                <Option value="bevel" type="QString" name="joinstyle"/>
                <Option value="equilateral_triangle" type="QString" name="name"/>
                <Option value="4.40000000000000036,4.40000000000000036" type="QString" name="offset"/>
                <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
                <Option value="Point" type="QString" name="offset_unit"/>
                <Option value="255,255,255,255,rgb:1,1,1,1" type="QString" name="outline_color"/>
                <Option value="solid" type="QString" name="outline_style"/>
                <Option value="0" type="QString" name="outline_width"/>
                <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
                <Option value="MM" type="QString" name="outline_width_unit"/>
                <Option value="diameter" type="QString" name="scale_method"/>
                <Option value="10" type="QString" name="size"/>
                <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
                <Option value="Point" type="QString" name="size_unit"/>
                <Option value="1" type="QString" name="vertical_anchor_point"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" type="QString" name="name"/>
                  <Option name="properties"/>
                  <Option value="collection" type="QString" name="type"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="line" frame_rate="10" alpha="1" is_animated="0" clip_to_extent="1" name="3">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer id="{48d18e69-644a-468d-894a-16eca28a21de}" pass="0" class="SimpleLine" enabled="1" locked="0">
          <Option type="Map">
            <Option value="0" type="QString" name="align_dash_pattern"/>
            <Option value="square" type="QString" name="capstyle"/>
            <Option value="5;2" type="QString" name="customdash"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="customdash_map_unit_scale"/>
            <Option value="MM" type="QString" name="customdash_unit"/>
            <Option value="0" type="QString" name="dash_pattern_offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="dash_pattern_offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="dash_pattern_offset_unit"/>
            <Option value="0" type="QString" name="draw_inside_polygon"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="63,52,215,255,rgb:0.24705882352941178,0.20392156862745098,0.84313725490196079,1" type="QString" name="line_color"/>
            <Option value="solid" type="QString" name="line_style"/>
            <Option value="0.26" type="QString" name="line_width"/>
            <Option value="MM" type="QString" name="line_width_unit"/>
            <Option value="0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="0" type="QString" name="ring_filter"/>
            <Option value="0" type="QString" name="trim_distance_end"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="trim_distance_end_map_unit_scale"/>
            <Option value="MM" type="QString" name="trim_distance_end_unit"/>
            <Option value="0" type="QString" name="trim_distance_start"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="trim_distance_start_map_unit_scale"/>
            <Option value="MM" type="QString" name="trim_distance_start_unit"/>
            <Option value="0" type="QString" name="tweak_dash_pattern_on_corners"/>
            <Option value="0" type="QString" name="use_custom_dash"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="width_map_unit_scale"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <source-symbol>
      <symbol force_rhr="0" type="line" frame_rate="10" alpha="1" is_animated="0" clip_to_extent="1" name="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer id="{9ae01466-4608-4766-94c0-b24ba15276f7}" pass="0" class="SimpleLine" enabled="1" locked="0">
          <Option type="Map">
            <Option value="0" type="QString" name="align_dash_pattern"/>
            <Option value="square" type="QString" name="capstyle"/>
            <Option value="5;2" type="QString" name="customdash"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="customdash_map_unit_scale"/>
            <Option value="MM" type="QString" name="customdash_unit"/>
            <Option value="0" type="QString" name="dash_pattern_offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="dash_pattern_offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="dash_pattern_offset_unit"/>
            <Option value="0" type="QString" name="draw_inside_polygon"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="line_color"/>
            <Option value="solid" type="QString" name="line_style"/>
            <Option value="0.26" type="QString" name="line_width"/>
            <Option value="MM" type="QString" name="line_width_unit"/>
            <Option value="0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="0" type="QString" name="ring_filter"/>
            <Option value="0" type="QString" name="trim_distance_end"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="trim_distance_end_map_unit_scale"/>
            <Option value="MM" type="QString" name="trim_distance_end_unit"/>
            <Option value="0" type="QString" name="trim_distance_start"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="trim_distance_start_map_unit_scale"/>
            <Option value="MM" type="QString" name="trim_distance_start_unit"/>
            <Option value="0" type="QString" name="tweak_dash_pattern_on_corners"/>
            <Option value="0" type="QString" name="use_custom_dash"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="width_map_unit_scale"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </source-symbol>
    <rotation/>
    <sizescale/>
    <data-defined-properties>
      <Option type="Map">
        <Option value="" type="QString" name="name"/>
        <Option name="properties"/>
        <Option value="collection" type="QString" name="type"/>
      </Option>
    </data-defined-properties>
  </renderer-v2>
  <selection mode="Default">
    <selectionColor invalid="1"/>
    <selectionSymbol>
      <symbol force_rhr="0" type="line" frame_rate="10" alpha="1" is_animated="0" clip_to_extent="1" name="">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer id="{d5117ecb-cdb1-45f7-a06f-c78c342e2626}" pass="0" class="SimpleLine" enabled="1" locked="0">
          <Option type="Map">
            <Option value="0" type="QString" name="align_dash_pattern"/>
            <Option value="square" type="QString" name="capstyle"/>
            <Option value="5;2" type="QString" name="customdash"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="customdash_map_unit_scale"/>
            <Option value="MM" type="QString" name="customdash_unit"/>
            <Option value="0" type="QString" name="dash_pattern_offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="dash_pattern_offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="dash_pattern_offset_unit"/>
            <Option value="0" type="QString" name="draw_inside_polygon"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="line_color"/>
            <Option value="solid" type="QString" name="line_style"/>
            <Option value="0.26" type="QString" name="line_width"/>
            <Option value="MM" type="QString" name="line_width_unit"/>
            <Option value="0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="0" type="QString" name="ring_filter"/>
            <Option value="0" type="QString" name="trim_distance_end"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="trim_distance_end_map_unit_scale"/>
            <Option value="MM" type="QString" name="trim_distance_end_unit"/>
            <Option value="0" type="QString" name="trim_distance_start"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="trim_distance_start_map_unit_scale"/>
            <Option value="MM" type="QString" name="trim_distance_start_unit"/>
            <Option value="0" type="QString" name="tweak_dash_pattern_on_corners"/>
            <Option value="0" type="QString" name="use_custom_dash"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="width_map_unit_scale"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </selectionSymbol>
  </selection>
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style multilineHeightUnit="Percentage" fontKerning="1" tabStopDistanceMapUnitScale="3x:0,0,0,0,0,0" blendMode="0" legendString="Aa" forcedItalic="0" allowHtml="0" fontSize="10" fontLetterSpacing="0" fieldName="prob_propagazione" forcedBold="0" tabStopDistanceUnit="Point" fontWeight="50" fontFamily="Open Sans" fontItalic="0" multilineHeight="1" textOpacity="1" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontSizeUnit="Point" tabStopDistance="80" isExpression="0" namedStyle="Regular" fontWordSpacing="0" previewBkgrdColor="255,255,255,255,rgb:1,1,1,1" textColor="50,50,50,255,rgb:0.19607843137254902,0.19607843137254902,0.19607843137254902,1" fontStrikeout="0" fontUnderline="0" capitalization="0" useSubstitutions="1" textOrientation="horizontal">
        <families/>
        <text-buffer bufferSizeUnits="MM" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferOpacity="1" bufferColor="250,250,250,255,rgb:0.98039215686274506,0.98039215686274506,0.98039215686274506,1" bufferNoFill="1" bufferBlendMode="0" bufferSize="1" bufferDraw="0" bufferJoinStyle="128"/>
        <text-mask maskOpacity="1" maskType="0" maskEnabled="0" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskSize="1.5" maskSize2="1.5" maskedSymbolLayers="" maskSizeUnits="MM" maskJoinStyle="128"/>
        <background shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthUnit="Point" shapeFillColor="255,255,255,255,rgb:1,1,1,1" shapeOffsetUnit="Point" shapeRotation="0" shapeSizeType="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeSizeUnit="Point" shapeOffsetY="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeJoinStyle="64" shapeOffsetX="0" shapeType="0" shapeRadiiUnit="Point" shapeBorderWidth="0" shapeRadiiY="0" shapeBorderColor="128,128,128,255,rgb:0.50196078431372548,0.50196078431372548,0.50196078431372548,1" shapeSizeY="0" shapeSizeX="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeSVGFile="" shapeDraw="0" shapeBlendMode="0" shapeOpacity="1" shapeRotationType="0" shapeRadiiX="0">
          <symbol force_rhr="0" type="marker" frame_rate="10" alpha="1" is_animated="0" clip_to_extent="1" name="markerSymbol">
            <data_defined_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name"/>
                <Option name="properties"/>
                <Option value="collection" type="QString" name="type"/>
              </Option>
            </data_defined_properties>
            <layer id="" pass="0" class="SimpleMarker" enabled="1" locked="0">
              <Option type="Map">
                <Option value="0" type="QString" name="angle"/>
                <Option value="square" type="QString" name="cap_style"/>
                <Option value="152,125,183,255,rgb:0.59607843137254901,0.49019607843137253,0.71764705882352942,1" type="QString" name="color"/>
                <Option value="1" type="QString" name="horizontal_anchor_point"/>
                <Option value="bevel" type="QString" name="joinstyle"/>
                <Option value="circle" type="QString" name="name"/>
                <Option value="0,0" type="QString" name="offset"/>
                <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
                <Option value="MM" type="QString" name="offset_unit"/>
                <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
                <Option value="solid" type="QString" name="outline_style"/>
                <Option value="0" type="QString" name="outline_width"/>
                <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
                <Option value="MM" type="QString" name="outline_width_unit"/>
                <Option value="diameter" type="QString" name="scale_method"/>
                <Option value="2" type="QString" name="size"/>
                <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
                <Option value="MM" type="QString" name="size_unit"/>
                <Option value="1" type="QString" name="vertical_anchor_point"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" type="QString" name="name"/>
                  <Option name="properties"/>
                  <Option value="collection" type="QString" name="type"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
          <symbol force_rhr="0" type="fill" frame_rate="10" alpha="1" is_animated="0" clip_to_extent="1" name="fillSymbol">
            <data_defined_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name"/>
                <Option name="properties"/>
                <Option value="collection" type="QString" name="type"/>
              </Option>
            </data_defined_properties>
            <layer id="" pass="0" class="SimpleFill" enabled="1" locked="0">
              <Option type="Map">
                <Option value="3x:0,0,0,0,0,0" type="QString" name="border_width_map_unit_scale"/>
                <Option value="255,255,255,255,rgb:1,1,1,1" type="QString" name="color"/>
                <Option value="bevel" type="QString" name="joinstyle"/>
                <Option value="0,0" type="QString" name="offset"/>
                <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
                <Option value="MM" type="QString" name="offset_unit"/>
                <Option value="128,128,128,255,rgb:0.50196078431372548,0.50196078431372548,0.50196078431372548,1" type="QString" name="outline_color"/>
                <Option value="no" type="QString" name="outline_style"/>
                <Option value="0" type="QString" name="outline_width"/>
                <Option value="Point" type="QString" name="outline_width_unit"/>
                <Option value="solid" type="QString" name="style"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" type="QString" name="name"/>
                  <Option name="properties"/>
                  <Option value="collection" type="QString" name="type"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </background>
        <shadow shadowDraw="0" shadowOffsetGlobal="1" shadowRadiusUnit="MM" shadowUnder="0" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.69999999999999996" shadowBlendMode="6" shadowOffsetUnit="MM" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetDist="1" shadowColor="0,0,0,255,rgb:0,0,0,1" shadowRadiusAlphaOnly="0" shadowScale="100" shadowOffsetAngle="135" shadowRadius="1.5"/>
        <dd_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </dd_properties>
        <substitutions>
          <replacement replace="bassa" caseSensitive="0" wholeWord="1" match="1001"/>
          <replacement replace="media" caseSensitive="0" wholeWord="1" match="1002"/>
          <replacement replace="alta" caseSensitive="0" wholeWord="1" match="1003"/>
        </substitutions>
      </text-style>
      <text-format formatNumbers="0" addDirectionSymbol="0" placeDirectionSymbol="0" autoWrapLength="0" rightDirectionSymbol=">" useMaxLineLengthForAutoWrap="1" leftDirectionSymbol="&lt;" wrapChar="" reverseDirectionSymbol="0" decimals="3" plussign="0" multilineAlign="0"/>
      <placement overlapHandling="PreventOverlap" offsetType="0" repeatDistanceUnits="MM" yOffset="0" lineAnchorPercent="0.5" layerType="LineGeometry" geometryGenerator="" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" maxCurvedCharAngleIn="25" overrunDistance="0" distMapUnitScale="3x:0,0,0,0,0,0" centroidInside="0" prioritization="PreferCloser" lineAnchorType="0" maximumDistance="0" fitInPolygonOnly="0" maximumDistanceUnit="MM" quadOffset="4" lineAnchorClipping="0" repeatDistance="0" maxCurvedCharAngleOut="-25" xOffset="0" polygonPlacementFlags="2" dist="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" placement="2" lineAnchorTextPoint="FollowPlacement" centroidWhole="0" geometryGeneratorEnabled="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorType="PointGeometry" rotationAngle="0" preserveRotation="1" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" rotationUnit="AngleDegrees" offsetUnits="MM" priority="5" distUnits="MM" allowDegraded="0" overrunDistanceUnit="MM" maximumDistanceMapUnitScale="3x:0,0,0,0,0,0" placementFlags="10"/>
      <rendering minFeatureSize="0" fontLimitPixelSize="0" labelPerPart="0" zIndex="0" mergeLines="0" obstacleFactor="1" scaleMax="0" maxNumLabels="2000" fontMinPixelSize="3" scaleVisibility="0" scaleMin="0" obstacle="1" drawLabels="1" fontMaxPixelSize="10000" obstacleType="1" unplacedVisibility="0" upsidedownLabels="0" limitNumLabels="0"/>
      <dd_properties>
        <Option type="Map">
          <Option value="" type="QString" name="name"/>
          <Option name="properties"/>
          <Option value="collection" type="QString" name="type"/>
        </Option>
      </dd_properties>
      <callout type="simple">
        <Option type="Map">
          <Option value="pole_of_inaccessibility" type="QString" name="anchorPoint"/>
          <Option value="0" type="int" name="blendMode"/>
          <Option type="Map" name="ddProperties">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
          <Option value="false" type="bool" name="drawToAllParts"/>
          <Option value="0" type="QString" name="enabled"/>
          <Option value="point_on_exterior" type="QString" name="labelAnchorPoint"/>
          <Option value="&lt;symbol force_rhr=&quot;0&quot; type=&quot;line&quot; frame_rate=&quot;10&quot; alpha=&quot;1&quot; is_animated=&quot;0&quot; clip_to_extent=&quot;1&quot; name=&quot;symbol&quot;>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; type=&quot;QString&quot; name=&quot;name&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; type=&quot;QString&quot; name=&quot;type&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;layer id=&quot;{a5e7a18b-ef3c-456c-87d8-06764edc77c8}&quot; pass=&quot;0&quot; class=&quot;SimpleLine&quot; enabled=&quot;1&quot; locked=&quot;0&quot;>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;align_dash_pattern&quot;/>&lt;Option value=&quot;square&quot; type=&quot;QString&quot; name=&quot;capstyle&quot;/>&lt;Option value=&quot;5;2&quot; type=&quot;QString&quot; name=&quot;customdash&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;customdash_map_unit_scale&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;customdash_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;dash_pattern_offset&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;dash_pattern_offset_map_unit_scale&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;dash_pattern_offset_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;draw_inside_polygon&quot;/>&lt;Option value=&quot;bevel&quot; type=&quot;QString&quot; name=&quot;joinstyle&quot;/>&lt;Option value=&quot;60,60,60,255,rgb:0.23529411764705882,0.23529411764705882,0.23529411764705882,1&quot; type=&quot;QString&quot; name=&quot;line_color&quot;/>&lt;Option value=&quot;solid&quot; type=&quot;QString&quot; name=&quot;line_style&quot;/>&lt;Option value=&quot;0.3&quot; type=&quot;QString&quot; name=&quot;line_width&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;line_width_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;offset&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;offset_map_unit_scale&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;offset_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;ring_filter&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;trim_distance_end&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;trim_distance_end_map_unit_scale&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;trim_distance_end_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;trim_distance_start&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;trim_distance_start_map_unit_scale&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;trim_distance_start_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;tweak_dash_pattern_on_corners&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;use_custom_dash&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;width_map_unit_scale&quot;/>&lt;/Option>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; type=&quot;QString&quot; name=&quot;name&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; type=&quot;QString&quot; name=&quot;type&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString" name="lineSymbol"/>
          <Option value="0" type="double" name="minLength"/>
          <Option value="3x:0,0,0,0,0,0" type="QString" name="minLengthMapUnitScale"/>
          <Option value="MM" type="QString" name="minLengthUnit"/>
          <Option value="0" type="double" name="offsetFromAnchor"/>
          <Option value="3x:0,0,0,0,0,0" type="QString" name="offsetFromAnchorMapUnitScale"/>
          <Option value="MM" type="QString" name="offsetFromAnchorUnit"/>
          <Option value="0" type="double" name="offsetFromLabel"/>
          <Option value="3x:0,0,0,0,0,0" type="QString" name="offsetFromLabelMapUnitScale"/>
          <Option value="MM" type="QString" name="offsetFromLabelUnit"/>
        </Option>
      </callout>
    </settings>
  </labeling>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <fieldConfiguration>
    <field name="fid">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="prob_propagazione">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="1001" type="QString" name="bassa"/>
              </Option>
              <Option type="Map">
                <Option value="1002" type="QString" name="media"/>
              </Option>
              <Option type="Map">
                <Option value="1003" type="QString" name="alta"/>
              </Option>
              <Option type="Map">
                <Option value="{2839923C-8B7D-419E-B84B-CA2FE9B80EC7}" type="QString" name="&lt;NULL>"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="fonte_proc">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="AllowMulti"/>
            <Option value="false" type="bool" name="AllowNull"/>
            <Option value="Case&#xd;&#xa;&#x9;when &quot;scenario&quot;  = 0 then 'Sconosciuto'&#xd;&#xa;&#x9;when &quot;scenario&quot;  = 1001 then 'Scenario puntuale'&#xd;&#xa;&#x9;when &quot;scenario&quot;  = 1000 then 'Scenario diffuso'&#xd;&#xa;&#x9;else '_'&#xd;&#xa;End" type="QString" name="Description"/>
            <Option type="invalid" name="FilterExpression"/>
            <Option value="fonte_proc" type="QString" name="Key"/>
            <Option value="Zone_instabilita_1ed06e0b_ac25_48cb_a1ae_d42c8a2f4097" type="QString" name="Layer"/>
            <Option value="Zona sorgente (fonte processo)" type="QString" name="LayerName"/>
            <Option value="ogr" type="QString" name="LayerProviderName"/>
            <Option value="F:/UPIP/06_StrumentiGis/02_Progetti base/09_Plugin QGIS/01_Test QGIS/Mod.proc.CadutaSassi2024/data_3000_19092023_145610.gpkg|layername=Zone_instabilita" type="QString" name="LayerSource"/>
            <Option value="1" type="int" name="NofColumns"/>
            <Option value="false" type="bool" name="OrderByValue"/>
            <Option value="false" type="bool" name="UseCompleter"/>
            <Option value="fonte_proc" type="QString" name="Value"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="prob_rottura">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="1000" type="QString" name="molto bassa"/>
              </Option>
              <Option type="Map">
                <Option value="1001" type="QString" name="bassa"/>
              </Option>
              <Option type="Map">
                <Option value="1002" type="QString" name="media"/>
              </Option>
              <Option type="Map">
                <Option value="1003" type="QString" name="alta"/>
              </Option>
              <Option type="Map">
                <Option value="{2839923C-8B7D-419E-B84B-CA2FE9B80EC7}" type="QString" name="&lt;NULL>"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="proc_parz">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="3000" type="QString" name="caduta sassi o blocchi"/>
              </Option>
              <Option type="Map">
                <Option value="3001" type="QString" name="crollo di roccia o frana"/>
              </Option>
              <Option type="Map">
                <Option value="{2839923C-8B7D-419E-B84B-CA2FE9B80EC7}" type="QString" name="&lt;NULL>"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="lunghezza">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull"/>
            <Option value="1.7976931348623157e+308" type="double" name="Max"/>
            <Option value="-1.7976931348623157e+308" type="double" name="Min"/>
            <Option value="1" type="int" name="Precision"/>
            <Option value="1" type="double" name="Step"/>
            <Option value="SpinBox" type="QString" name="Style"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
I moduli QGIS possono avere una funzione Python che può essere chiamata quando viene aperto un modulo.

Usa questa funzione per aggiungere logica extra ai tuoi moduli.

Inserisci il nome della funzione nel campo "Funzione Python di avvio".

Segue un esempio:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>2</featformsuppress>
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <labelStyle overrideLabelColor="0" overrideLabelFont="0" labelColor="">
      <labelFont description="Ubuntu Sans,11,-1,5,50,0,0,0,0,0" style="" underline="0" italic="0" bold="0" strikethrough="0"/>
    </labelStyle>
    <attributeEditorContainer columnCount="1" collapsed="0" collapsedExpression="" collapsedExpressionEnabled="0" visibilityExpressionEnabled="0" horizontalStretch="0" verticalStretch="0" type="Tab" visibilityExpression="" groupBox="0" showLabel="1" name="Attributi">
      <labelStyle overrideLabelColor="0" overrideLabelFont="0" labelColor="0,0,0,255,rgb:0,0,0,1">
        <labelFont description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style="" underline="0" italic="0" bold="0" strikethrough="0"/>
      </labelStyle>
      <attributeEditorField horizontalStretch="0" verticalStretch="0" index="1" showLabel="1" name="prob_propagazione">
        <labelStyle overrideLabelColor="0" overrideLabelFont="0" labelColor="0,0,0,255,rgb:0,0,0,1">
          <labelFont description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style="" underline="0" italic="0" bold="0" strikethrough="0"/>
        </labelStyle>
      </attributeEditorField>
      <attributeEditorField horizontalStretch="0" verticalStretch="0" index="3" showLabel="1" name="prob_rottura">
        <labelStyle overrideLabelColor="0" overrideLabelFont="0" labelColor="0,0,0,255,rgb:0,0,0,1">
          <labelFont description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style="" underline="0" italic="0" bold="0" strikethrough="0"/>
        </labelStyle>
      </attributeEditorField>
      <attributeEditorField horizontalStretch="0" verticalStretch="0" index="2" showLabel="1" name="fonte_proc">
        <labelStyle overrideLabelColor="0" overrideLabelFont="0" labelColor="0,0,0,255,rgb:0,0,0,1">
          <labelFont description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style="" underline="0" italic="0" bold="0" strikethrough="0"/>
        </labelStyle>
      </attributeEditorField>
      <attributeEditorContainer columnCount="1" collapsed="0" collapsedExpression="" collapsedExpressionEnabled="0" visibilityExpressionEnabled="0" horizontalStretch="0" verticalStretch="0" type="GroupBox" visibilityExpression="" groupBox="1" showLabel="1" name="Automatici">
        <labelStyle overrideLabelColor="0" overrideLabelFont="0" labelColor="0,0,0,255,rgb:0,0,0,1">
          <labelFont description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style="" underline="0" italic="0" bold="0" strikethrough="0"/>
        </labelStyle>
        <attributeEditorField horizontalStretch="0" verticalStretch="0" index="4" showLabel="1" name="proc_parz">
          <labelStyle overrideLabelColor="0" overrideLabelFont="0" labelColor="0,0,0,255,rgb:0,0,0,1">
            <labelFont description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style="" underline="0" italic="0" bold="0" strikethrough="0"/>
          </labelStyle>
        </attributeEditorField>
        <attributeEditorField horizontalStretch="0" verticalStretch="0" index="0" showLabel="1" name="fid">
          <labelStyle overrideLabelColor="0" overrideLabelFont="0" labelColor="0,0,0,255,rgb:0,0,0,1">
            <labelFont description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style="" underline="0" italic="0" bold="0" strikethrough="0"/>
          </labelStyle>
        </attributeEditorField>
        <attributeEditorField horizontalStretch="0" verticalStretch="0" index="5" showLabel="1" name="lunghezza">
          <labelStyle overrideLabelColor="0" overrideLabelFont="0" labelColor="0,0,0,255,rgb:0,0,0,1">
            <labelFont description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style="" underline="0" italic="0" bold="0" strikethrough="0"/>
          </labelStyle>
        </attributeEditorField>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="fid"/>
    <field editable="1" name="fonte_proc"/>
    <field editable="0" name="lunghezza"/>
    <field editable="1" name="osservazioni"/>
    <field editable="1" name="periodo_ritorno"/>
    <field editable="1" name="prob_propagazione"/>
    <field editable="1" name="prob_rottura"/>
    <field editable="1" name="proc_parz"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="fid"/>
    <field labelOnTop="0" name="fonte_proc"/>
    <field labelOnTop="0" name="lunghezza"/>
    <field labelOnTop="1" name="osservazioni"/>
    <field labelOnTop="0" name="periodo_ritorno"/>
    <field labelOnTop="0" name="prob_propagazione"/>
    <field labelOnTop="0" name="prob_rottura"/>
    <field labelOnTop="0" name="proc_parz"/>
  </labelOnTop>
  <reuseLastValue>
    <field name="fid" reuseLastValue="0"/>
    <field name="fonte_proc" reuseLastValue="0"/>
    <field name="lunghezza" reuseLastValue="0"/>
    <field name="osservazioni" reuseLastValue="0"/>
    <field name="prob_propagazione" reuseLastValue="0"/>
    <field name="prob_rottura" reuseLastValue="0"/>
    <field name="proc_parz" reuseLastValue="0"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"fid"</previewExpression>
  <layerGeometryType>1</layerGeometryType>
</qgis>
