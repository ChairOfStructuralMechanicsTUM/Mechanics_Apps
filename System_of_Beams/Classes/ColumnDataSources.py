import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.models.callbacks import CustomJS


class ColumnDataSources:
    # datasource for the node independent elements of the input plot
    ds_input = ColumnDataSource(data=dict(x=[], y=[], type=[], name_user=[]))

    # data source for all image glyphs plotted in the input plot
    ds_glyph_images = ColumnDataSource(data=dict())

    # data source for beam glyphs plotted in the input plot
    ds_glyph_beam = ColumnDataSource(data=dict(x=[], y=[], width=[], angle=[], name_user=[]))

    # data source for line load patch glyphs of the input plot
    ds_glyph_lineload = ColumnDataSource(data=dict(patch_x=[], patch_y=[], glyph_x=[], glyph_y=[],
                                                   x=[], y=[], name_user=[]))
    # data source for line load arrows
    ds_arrow_lineload = ColumnDataSource(data=dict(xs=[], ys=[], name_user=[]))

    # # data source for line load arrows
    # ds_arrow_lineload = ColumnDataSource(data=dict(xs=[], ys=[], name_user=[]))

    # data source for info about image glyphs of nodedependent elements for tooltips and element info box
    ds_glyph_springsPointMomentTemp = ColumnDataSource(data=dict(glyph_x=[], glyph_y=[], x=[], y=[],
                                                                 name_user=[]))

    # data source for the selected node independent elements of the input plot
    ds_input_selected = ColumnDataSource(data=dict(x=[], y=[]))

    # ColumnDataSource necessary for the JavaScript callbacks
    # data source for the activated element button
    ds_active_button = ColumnDataSource(data=dict(type=[-1]))
    # data source for the current number of elements in the plot
    ds_element_count = ColumnDataSource(data=dict(count=[0]))

    # data source for tap in input plot for node dependend glyphs (transfer)
    ds_chosen_node = ColumnDataSource(data=dict(type=[-1], tap_x=[0.0], tap_y=[0.0]))
    # data source for taps on existing nodes in input plot to create a new node dependent glyph
    ds_1st_chosen = ColumnDataSource(data=dict(type=[], node_x=[], node_y=[], name_node1=[]))

    # data source for tap in input plot for showing element info when no button is activated (transfer)
    ds_element_info = ColumnDataSource(data=dict(tap_x=[0.0], tap_y=[0.0]))

    # data source for image glyphs of node independent elements, that need to be plotted (collection)
    ds_indep_elements = ColumnDataSource(data=dict(x=[], y=[], type=[], name=[], same=[], angle=[]))

    # data source for image glyphs of node dependent elements, that need to be plotted (collection)
    ds_nodedep_elements = ColumnDataSource(
        data=dict(name_node1=[], name_node2=[], type=[], name=[], x=[], y=[], length=[],
                  dT_T=[], k=[], h=[], ei=[], ea=[], moment=[], f=[],
                  ll_local=[], ll_x_n=[], ll_y_q=[], angle=[]))

    cb_get_selected_ = CustomJS(args=dict(div=None, ds=None, selected=None), code="""
        //JavaScript code:
        var inds = cb_obj.indices;
        var ds_x = ds.data['x'];
        var ds_y = ds.data['y'];

        //get selected elements of plot and add them to the datasource for the selected input plot elements
        s = {'x': [], 'y': []}
        for (var i = 0; i < inds.length; i++) {
            s['x'].push(ds_x[inds[i]])
            s['y'].push(ds_y[inds[i]])
        }
        selected.data = s
        """)

    cb_plot_tap_ = CustomJS(args=dict(div=None, ds=None, activated=None, element_count=None,
                                      max_number_elements=None, ds_c_n=None, ds_e_i=None,
                                      nodedep=None), code="""
        //JavaScript code:
        var div = div;
        var nodedep = nodedep;
        var active = activated.data['type'][0];
        var count = element_count.data['count'][0];
        var str_count = count.toFixed(0);
        var count_data = element_count.data;
        var max_element = max_number_elements;
        var ds_data = ds.data;
        var ds_c_n_data = ds_c_n.data;
        var ds_e_i_data = ds_e_i.data;
        var active_is_independent = true;

        // get x and y position of tap in plot, restricted to one decimal
        var x = Math.round(Number(cb_obj['x']) * 10) / 10;
        var y = Math.round(Number(cb_obj['y']) * 10) / 10;

        // check if active element belongs to the node dependent ones (springs, loads, beam)
        for (i = 0; i < nodedep.length; i++) {
           if (nodedep[i] == active) {
              active_is_independent = false;
              break;
           }
        }

        // tell user if no element button is active and add tap to datasource of element info 
        if (active == -1) { 
            ds_e_i_data['tap_x'] = [x];
            ds_e_i_data['tap_y'] = [y];
            ds_e_i.data = ds_e_i_data;
        // add element to datasource of input plot and element info if element is node independent 
        // and maximum amount of elements is not already reached
        } else if (active_is_independent == true) {  
            if (count == max_element) {
                div.text = "<span style=%r>You already reached the maximum number of nodes (" + str_count + ")!</span>";
            } else {   
               ds_data['x'].push(x);
               ds_data['y'].push(y);
               ds_data['type'].push(active);
               ds_data['name_user'].push(0);
               ds.data = ds_data;

               ds_e_i_data['tap_x'] = [x];
               ds_e_i_data['tap_y'] = [y];
               ds_e_i.data = ds_e_i_data;

               count_data['count'] = [count + 1];
               element_count.data = count_data;
            }
        // add element to datasource of chosen node if element is node dependent
        } else {
            ds_c_n_data['type'] = [active];
            ds_c_n_data['tap_x'] = [x];
            ds_c_n_data['tap_y'] = [y];
            ds_c_n.data = ds_c_n_data;
        }
        ds.change.emit();
        """)

    style = 'float:left;clear:left;font_size=10pt'
    cb_plot_xy_ = CustomJS(args=dict(div=None), code="""
        //JavaScript code:
        //get x and y of plot when mouse hovers in plot and show it
        var text = Number(cb_obj['x']).toFixed(1) + ',' + Number(cb_obj['y']).toFixed(1);        
        div.text = "<span style=%r>(" + text + ")</span>";
        """ % style)

    # -> ColumnDataSources for vis_elementToPlot
    ############################################

    # mapping of enum_type to position in ds_images used for image url, sizes and offsets of bokeh image glyphs
    url = "System_of_Beams/static/images/"
    ds_images = ColumnDataSource(dict(
        url=[url + "support_clamped_p.png", url + "support_normal_p.png", url + "support_transverse_p.png",
             url + "support_fixed_conti_p.png", url + "support_fixed_joint_p.png", url + "support_roller_conti_p.png",
             url + "support_roller_joint_p.png", url + "spring_support_p.png", url + "spring_moment_p.png",
             url + "spring_moment_neg_p.png", url + "node_p.png", url + "joint_p.png", url + "joint_normal_p.png",
             url + "joint_transverse_p.png", url + "spring_p.png", url + "load_point_p.png", url + "moment_p.png",
             url + "moment_neg_p.png", url + "load_temp_p.png"],
        x_mod=[+0.03, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2],
        y_mod=[0, 0, 0, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, 0, 0, 0, 0, 0, 0.2, 0.2, 0.2, -0.2],
        w=[0.30, 0.50, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.024, 0.11, 0.25, 0.25, 1.0, 0.16, 0.4, 0.4,
           0.18],
        h=[0.37, 0.30, 0.37, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.11, 0.11, 0.08, 0.15, 0.24, 0.4, 0.16, 0.16, 0.25],
    ))  # supports                            # springs         # node, joints           # sp   # point, moment  # temp

    # -> ColumnDataSources for vis_initalization
    ############################################

    # add darker lines to be able to distinguish the x and y axis clearly after moving the plot
    axis_line = np.linspace(-100, 100, 2)
    axis_zero = axis_line * 0
    ds_x_axis = ColumnDataSource(dict(x=axis_line, y=axis_zero))
    ds_y_axis = ColumnDataSource(dict(x=axis_zero, y=axis_line))

