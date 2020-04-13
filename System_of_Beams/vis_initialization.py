from functools import partial
import numpy as np
from os.path import dirname, join, abspath, split
import sys
import inspect

# import bokeh modules
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models.glyphs import Line
from bokeh.models.ranges import Range1d
from bokeh.layouts import column, row
from bokeh.models.widgets import Button, Div, TextInput, Dropdown, CheckboxGroup, RadioGroup
from bokeh.models.tickers import AdaptiveTicker
from bokeh.events import Tap, MouseMove

# import local files
import vis_callbacks as vis_cbs
from Classes import ElementSupportEnum as eLnum
from Libs import HtmlColors as coL

# import local latex_support
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0, parentdir)
# from latex_support import LatexDiv, LatexLabel, LatexSlider, LatexLabelSet, LatexLegend
# TODO update Latex support

# input plot, the user can add elements to it and combine them to a mechanical system
plot_input = figure()

# dict containing all element bokeh buttons and their corresponding ElementSupportEnum as key
buttons = {}

# dict containing all element-info-box inputs
input_element_info = {}
# dict containing some element-info-box Divs
div_element_info = {}
# dict containing some element-info-box radio- or checkbox-groups
group_element_info = {}
# dict containing children of layout_element_info
children_element_info = {}
# layout of the element-info-box
layout_element_info = row()

# bokeh Div for showing messages to the user like warnings and errors and initial text string that gets expanded
div_msg = 0
msg2user = ""

# bokeh Div for showing messages concerning the input plot to the user
div_input = 0

# output plots used after calculations
plot_list = []
plot_normal_f = figure()
plot_normal_disp = figure()
plot_shear_f = figure()
plot_moment = figure()
plot_shear_disp = figure()
plot_shear_angle = figure()


def configure_input_plot(p, div_xy, max_indep_elements):
    """
    The input plot is used to allow the user to connect mechanical elements.
    This function configures the style of the input plot, creates a ColumnDataSource for it and adds five callbacks.
    :param p: input plot (figure)
    :param div_xy: Div object to show the x and y position of the cursor (Div)
    :param max_indep_elements: maximum number of node independent elements accepted in the input plot (int)
    :return: none
    """
    global div_input

    # style of the grid of the input plot
    p_ticker = AdaptiveTicker(base=10, mantissas=[1, 2], min_interval=1)
    p.xaxis.ticker = p_ticker
    p.yaxis.ticker = p_ticker
    p.xgrid.minor_grid_line_color = coL.HtmlColors.LIGHTGRAY.value
    p.xgrid.minor_grid_line_alpha = 0.2
    p.ygrid.minor_grid_line_color = coL.HtmlColors.LIGHTGRAY.value
    p.ygrid.minor_grid_line_alpha = 0.2

    # add darker lines to be able to distinguish the x and y axis clearly after moving the plot
    axis_line = np.linspace(-100, 100, 2)
    axis_zero = axis_line * 0
    ds_x_axis = ColumnDataSource(dict(x=axis_line, y=axis_zero))
    ds_y_axis = ColumnDataSource(dict(x=axis_zero, y=axis_line))
    x_axis_line = Line(x="x", y="y", line_color=coL.HtmlColors.BLACK.value, line_width=1, line_alpha=0.8)
    y_axis_line = Line(x="x", y="y", line_color=coL.HtmlColors.BLACK.value, line_width=1, line_alpha=0.8)
    p.add_glyph(ds_x_axis, x_axis_line)
    p.add_glyph(ds_y_axis, y_axis_line)

    # create glyphs with datasources
    # tooltips info of independent elements
    p.circle('x', 'y', source=vis_cbs.ds_input, radius=vis_cbs.catch_radius, alpha=0.0,
             color=coL.HtmlColors.BLUE_TUM.value, nonselection_alpha=0.0)
    # tooltips info of nodedependent image glyph elements
    p.circle(x='glyph_x', y='glyph_y', source=vis_cbs.ds_glyph_springsPointMomentTemp,
             radius=vis_cbs.catch_radius, alpha=0.0, color=coL.HtmlColors.GREEN.value, nonselection_alpha=0.0)
    # show the fist chosen node for a nodedependent element needing two existing nodes
    p.circle(x='node_x', y='node_y', source=vis_cbs.ds_1st_chosen, radius=vis_cbs.catch_radius,
             color=coL.HtmlColors.RED.value, fill_alpha=0.3, line_alpha=1.0)
    # glyphs for beams/ rods and tooltips info about them
    p.rect(x='x', y='y', source=vis_cbs.ds_glyph_beam, angle="angle", width="width", height=0.1,
           fill_color=coL.HtmlColors.LIGHTGRAY.value, line_color=coL.HtmlColors.BLACK.value, fill_alpha=0.7,
           line_alpha=1.0, width_units="data", height_units="data", nonselection_alpha=0.3)
    # patch glyphs for line loads
    col_lineloads = coL.HtmlColors.ORANGE.value
    p.patches(xs='patch_x', ys='patch_y', source=vis_cbs.ds_glyph_lineload, fill_alpha=0.3, line_alpha=1.0,
              color=col_lineloads, nonselection_alpha=0.3)  # NaN values to plot multiple polygons in one patch
    # arrows for line loads
    p.multi_line(xs='xs', ys='ys', source=vis_cbs.ds_arrow_lineload, color=col_lineloads, line_alpha=1.0, line_width=3)

    # JavaScript callback to create an element when mouse tap in plot is detected and a button element is activated
    p.js_on_event(Tap, vis_cbs.cb_plot_tap(div_input, max_indep_elements))
    p.js_on_event(Tap, vis_cbs.cb_plot_xy(div_xy))

    # callback to react when the data source of the input plot has changed
    vis_cbs.ds_input.on_change('data', vis_cbs.cb_adapt_plot_indep)

    # callback to react when the data source for node-dependent elements has changed
    vis_cbs.ds_chosen_node.on_change('data', vis_cbs.cb_adapt_plot_nodedep)

    # callback to react when the data source for showing element info has changed
    vis_cbs.ds_element_info.on_change('data', vis_cbs.cb_show_element_info)

    # JavaScript callback to react when objects of the plot datasource change their 'selected' status
    vis_cbs.ds_input.selected.js_on_change('indices', vis_cbs.cb_get_selected(div_input))
    vis_cbs.ds_input_selected.on_change('data', vis_cbs.cb_show_selected)

    # JavaScript callback to show the x and y position of the cursor in the input plot
    # p.js_on_event(MouseMove, vis_cbs.cb_plot_xy(div_xy))


def expand_msg2user(msg, bg_color="white"):
    """
    Expands string used for the bokeh Div div_msg that shows information, warnings and errors to the user.
    Sets background-color of div_msg to orange or red if defined.
    :param msg: new message to be added (string)
    :param bg_color: background color of the message box (string), possible colors: white (default), red, orange
    :return: complete string of div_msg (string)
    """
    global div_msg, msg2user

    if bg_color == "red":
        div_msg.css_classes = ["MSG_BOX_RED"]
    elif bg_color == "orange":
        div_msg.css_classes = ["MSG_BOX_ORANGE"]
    else:
        div_msg.css_classes = ["MSG_BOX"]

    msg2user += "<br/>"
    msg2user += msg
    div_msg.text = "<ul>" + msg2user + "</ul>"
    return msg2user


def initialize(max_indep_elements=20, catch_radius=0.15):
    """
    Creates and configures all bokeh objects and starts the web app.
    :param max_indep_elements: maximum number of node independent elements accepted in the input plot (int)
    :param catch_radius: radius in which to select an element in input plot (double)
    :return: none
    """
    global plot_input, buttons, div_msg, div_input, \
        input_element_info, div_element_info, group_element_info, children_element_info, layout_element_info, \
        plot_list, plot_normal_f, plot_normal_disp, plot_shear_f, plot_moment, plot_shear_disp, plot_shear_angle

    vis_cbs.catch_radius = catch_radius

    '''
    ###############################
    # TEXT BOXES
    ###############################
    '''
    # Div object showing x and y position of the cursor in the input plot
    div_xy = Div(width=75, height=25)

    # Div object showing hints for the graphical input into the input plot through the element buttons
    div_input_width = plot_input.plot_width - div_xy.width - 10
    div_input       = Div(width=div_input_width, height=div_xy.height)

    # Div object showing general text messages to the user
    div_msg = Div(css_classes=["MSG_BOX"], text=" ", width=plot_input.plot_width, height=100)

    '''
    ###############################
    # INPUT PLOT
    ###############################
    '''
    # style and configuration of the input plot
    # this plot is used to allow the user to connect mechanical elements
    tooltips = [("name", "@name_user"), ("(x, y)", "(@x{0.0}, @y{0.0})")]
    plot_input = figure(
        # plot_width=600, plot_height=300,
        tools="pan,wheel_zoom,reset,lasso_select,hover,save",
        toolbar_location="above",
        # x_axis_label='x', y_axis_label='y',
        x_minor_ticks=10, y_minor_ticks=10,
        x_range=Range1d(start=0, end=5), y_range=Range1d(start=0, end=5),
        match_aspect=True, aspect_scale=1.0,
        tooltips=tooltips,
    )
    configure_input_plot(plot_input, div_xy, max_indep_elements)

    '''
    ###############################
    # OUTPUT PLOTS
    ###############################
    '''
    # initialize plots for the output after calculations
    plot_output_width   = 800
    plot_output_height  = 250
    plot_normal_f       = figure(plot_width=plot_output_width, plot_height=plot_output_height, active_scroll="wheel_zoom")
    plot_normal_f.title.text = 'Normal force'
    plot_normal_disp    = figure(plot_width=plot_output_width, plot_height=plot_output_height, active_scroll="wheel_zoom")
    plot_normal_disp.title.text = 'Normal displacement'
    plot_shear_f        = figure(plot_width=plot_output_width, plot_height=plot_output_height, active_scroll="wheel_zoom")
    plot_shear_f.title.text = 'Shear force'
    plot_moment         = figure(plot_width=plot_output_width, plot_height=plot_output_height, active_scroll="wheel_zoom")
    plot_moment.title.text = 'Bending moment'
    plot_shear_disp     = figure(plot_width=plot_output_width, plot_height=plot_output_height, active_scroll="wheel_zoom")
    plot_shear_disp.title.text = 'Shear displacement'
    plot_shear_angle    = figure(plot_width=plot_output_width, plot_height=plot_output_height, active_scroll="wheel_zoom")
    plot_shear_angle.title.text = 'Rotation angle'
    plot_list = [plot_normal_f, plot_normal_disp, plot_shear_f, plot_moment, plot_shear_angle, plot_shear_disp]

    # add plot renderer
    ds = ColumnDataSource(data=dict(x=[], y=[]))
    plot_normal_f.      circle('x', 'y', source=ds)
    plot_normal_disp.   circle('x', 'y', source=ds)
    plot_shear_f.       circle('x', 'y', source=ds)
    plot_moment.        circle('x', 'y', source=ds)
    plot_shear_disp.    circle('x', 'y', source=ds)
    plot_normal_f.      circle('x', 'y', source=ds)
    plot_shear_angle.   circle('x', 'y', source=ds)

    '''
    ###############################
    # TEST CASES
    ###############################
    '''
    menu_tc = [("Single beam load", "single_beam_load"), ("Two beam lineload", "two_beam_lineload"),
               ("Final structure Software Lab", "fin_struc_soft_lab")]
    dropdown_tc = Dropdown(label="Show test case", menu=menu_tc, width=150)
    dropdown_tc.on_change('value', vis_cbs.cb_plot_testcase)

    '''
    ###############################
    # CALCULATE AND DELETE BUTTONS
    ###############################
    '''
    # add and configure a button to start calculations
    button_calc = Button(label="Calculate", width=240)
    button_calc.on_click(partial(vis_cbs.cb_button_calculation, button_calc))

    # add and configure a button to delete selected elements of the input graph
    b_del_w = int((button_calc.width-10) / 2)
    button_del_selected = Button(label="Delete selected", width=b_del_w)
    button_del_selected.on_click(partial(vis_cbs.cb_button_delete, all_selected=False))

    # add and configure a button to delete selected elements of the input graph
    button_del_all = Button(label="Delete all", width=b_del_w)
    button_del_all.on_click(partial(vis_cbs.cb_button_delete, all_selected=True))

    '''
    ###############################
    # BOX OF ELEMENTS TO SELECT FOR INPUT PLOT
    ###############################
    '''
    # titles for groups of mechanical elements
    text_supports   = Div(text="Supports:", width=100, height=20)
    text_springs    = Div(text="Springs:", width=100, height=20)
    text_node       = Div(text="Node:", width=100, height=20)
    text_joints     = Div(text="Joints:", width=100, height=20)
    text_elements   = Div(text="Line elements:", width=100, height=20)
    text_loads      = Div(text="Loads:", width=100, height=20)

    b_height = 50
    b_line_width = 72

    # configure buttons for mechanical supports
    button_support_clamped = Button(label="", css_classes=[eLnum.ElSupEnum.SUPPORT_CLAMPED.name], width=b_height,
                                    height=b_height)
    buttons[eLnum.ElSupEnum.SUPPORT_CLAMPED.value] = button_support_clamped
    button_support_clamped.on_click(partial(vis_cbs.cb_button_element_click,
                                            button_enum=eLnum.ElSupEnum.SUPPORT_CLAMPED))

    button_support_normal = Button(label="", css_classes=[eLnum.ElSupEnum.SUPPORT_NORMAL_FORCE.name], width=b_height,
                                   height=b_height)
    buttons[eLnum.ElSupEnum.SUPPORT_NORMAL_FORCE.value] = button_support_normal
    button_support_normal.on_click(partial(vis_cbs.cb_button_element_click,
                                           button_enum=eLnum.ElSupEnum.SUPPORT_NORMAL_FORCE))

    button_support_transverse = Button(label="", css_classes=[eLnum.ElSupEnum.SUPPORT_TRANSVERSE_FORCE.name],
                                       width=b_height, height=b_height)
    buttons[eLnum.ElSupEnum.SUPPORT_TRANSVERSE_FORCE.value] = button_support_transverse
    button_support_transverse.on_click(partial(vis_cbs.cb_button_element_click,
                                               button_enum=eLnum.ElSupEnum.SUPPORT_TRANSVERSE_FORCE))

    button_support_fixed_conti = Button(label="", css_classes=[eLnum.ElSupEnum.SUPPORT_FIXED_CONTINUOUS.name],
                                        width=b_height, height=b_height)
    buttons[eLnum.ElSupEnum.SUPPORT_FIXED_CONTINUOUS.value] = button_support_fixed_conti
    button_support_fixed_conti.on_click(
        partial(vis_cbs.cb_button_element_click, button_enum=eLnum.ElSupEnum.SUPPORT_FIXED_CONTINUOUS))

    button_support_fixed_joint = Button(label="", css_classes=[eLnum.ElSupEnum.SUPPORT_FIXED_JOINT.name],
                                        width=b_height,
                                        height=b_height)
    buttons[eLnum.ElSupEnum.SUPPORT_FIXED_JOINT.value] = button_support_fixed_joint
    button_support_fixed_joint.on_click(
        partial(vis_cbs.cb_button_element_click, button_enum=eLnum.ElSupEnum.SUPPORT_FIXED_JOINT))

    button_support_roller_conti = Button(label="", css_classes=[eLnum.ElSupEnum.SUPPORT_ROLLER_CONTINUOUS.name],
                                         width=b_height, height=b_height)
    buttons[eLnum.ElSupEnum.SUPPORT_ROLLER_CONTINUOUS.value] = button_support_roller_conti
    button_support_roller_conti.on_click(partial(vis_cbs.cb_button_element_click,
                                                 button_enum=eLnum.ElSupEnum.SUPPORT_ROLLER_CONTINUOUS))

    button_support_roller_joint = Button(label="", css_classes=[eLnum.ElSupEnum.SUPPORT_ROLLER_JOINT.name],
                                         width=b_height,
                                         height=b_height)
    buttons[eLnum.ElSupEnum.SUPPORT_ROLLER_JOINT.value] = button_support_roller_joint
    button_support_roller_joint.on_click(partial(vis_cbs.cb_button_element_click,
                                                 button_enum=eLnum.ElSupEnum.SUPPORT_ROLLER_JOINT))

    button_spring_support = Button(label="", css_classes=[eLnum.ElSupEnum.SPRING_SUPPORT.name], width=b_height,
                                   height=b_height)
    buttons[eLnum.ElSupEnum.SPRING_SUPPORT.value] = button_spring_support
    button_spring_support.on_click(partial(vis_cbs.cb_button_element_click,
                                           button_enum=eLnum.ElSupEnum.SPRING_SUPPORT))

    button_spring_moment_support = Button(label="", css_classes=[eLnum.ElSupEnum.SPRING_MOMENT_SUPPORT.name],
                                          width=b_height,
                                          height=b_height)
    buttons[eLnum.ElSupEnum.SPRING_MOMENT_SUPPORT.value] = button_spring_moment_support
    button_spring_moment_support.on_click(partial(vis_cbs.cb_button_element_click,
                                                  button_enum=eLnum.ElSupEnum.SPRING_MOMENT_SUPPORT))

    # configure buttons for connectors
    button_node = Button(label="", css_classes=[eLnum.ElSupEnum.NODE.name], width=b_height, height=b_height)
    buttons[eLnum.ElSupEnum.NODE.value] = button_node
    button_node.on_click(partial(vis_cbs.cb_button_element_click, button_enum=eLnum.ElSupEnum.NODE))

    button_joint = Button(label="", css_classes=[eLnum.ElSupEnum.JOINT.name], width=b_height, height=b_height)
    buttons[eLnum.ElSupEnum.JOINT.value] = button_joint
    button_joint.on_click(partial(vis_cbs.cb_button_element_click, button_enum=eLnum.ElSupEnum.JOINT))

    button_joint_normal = Button(label="", css_classes=[eLnum.ElSupEnum.JOINT_NORMAL_FORCE.name], width=b_height,
                                 height=b_height)
    buttons[eLnum.ElSupEnum.JOINT_NORMAL_FORCE.value] = button_joint_normal
    button_joint_normal.on_click(
        partial(vis_cbs.cb_button_element_click, button_enum=eLnum.ElSupEnum.JOINT_NORMAL_FORCE))

    button_joint_transverse = Button(label="", css_classes=[eLnum.ElSupEnum.JOINT_TRANSVERSE_FORCE.name],
                                     width=b_height, height=b_height)
    buttons[eLnum.ElSupEnum.JOINT_TRANSVERSE_FORCE.value] = button_joint_transverse
    button_joint_transverse.on_click(
        partial(vis_cbs.cb_button_element_click, button_enum=eLnum.ElSupEnum.JOINT_TRANSVERSE_FORCE))

    button_spring = Button(label="", css_classes=[eLnum.ElSupEnum.SPRING.name], width=b_line_width, height=b_height)
    buttons[eLnum.ElSupEnum.SPRING.value] = button_spring
    button_spring.on_click(partial(vis_cbs.cb_button_element_click, button_enum=eLnum.ElSupEnum.SPRING))

    # configure buttons for mechanical 1D or 2D elements
    # button_rod = Button(label="", css_classes=[eLnum.ElSupEnum.ROD.name], width=b_line_width, height=b_height)
    # buttons[eLnum.ElSupEnum.ROD.value] = button_rod
    # button_rod.on_click(partial(vis_cbs.cb_button_element_click, button_enum=eLnum.ElSupEnum.ROD))

    button_beam = Button(label="", css_classes=[eLnum.ElSupEnum.BEAM.name], width=b_line_width, height=b_height)
    buttons[eLnum.ElSupEnum.BEAM.value] = button_beam
    button_beam.on_click(partial(vis_cbs.cb_button_element_click, button_enum=eLnum.ElSupEnum.BEAM))

    # configure buttons for mechanical loads
    button_load_point = Button(label="", css_classes=[eLnum.ElSupEnum.LOAD_POINT.name], width=b_height, height=b_height)
    buttons[eLnum.ElSupEnum.LOAD_POINT.value] = button_load_point
    button_load_point.on_click(partial(vis_cbs.cb_button_element_click, button_enum=eLnum.ElSupEnum.LOAD_POINT))

    button_load_moment = Button(label="", css_classes=[eLnum.ElSupEnum.LOAD_MOMENT.name], width=b_height,
                                height=b_height)
    buttons[eLnum.ElSupEnum.LOAD_MOMENT.value] = button_load_moment
    button_load_moment.on_click(partial(vis_cbs.cb_button_element_click, button_enum=eLnum.ElSupEnum.LOAD_MOMENT))

    button_load_random = Button(label="", css_classes=[eLnum.ElSupEnum.LOAD_LINE.name], width=b_line_width,
                                height=b_height)
    buttons[eLnum.ElSupEnum.LOAD_LINE.value] = button_load_random
    button_load_random.on_click(partial(vis_cbs.cb_button_element_click, button_enum=eLnum.ElSupEnum.LOAD_LINE))

    button_load_temp = Button(label="", css_classes=[eLnum.ElSupEnum.LOAD_TEMP.name], width=b_height, height=b_height)
    buttons[eLnum.ElSupEnum.LOAD_TEMP.value] = button_load_temp
    button_load_temp.on_click(partial(vis_cbs.cb_button_element_click, button_enum=eLnum.ElSupEnum.LOAD_TEMP))

    '''
    ###############################
    # ELEMENT INFO BOX
    ###############################
    '''
    elinfo_object_height = 26
    elinfo_label_width1 = 60
    elinfo_label_width2 = 40
    elinfo_input_width = 60

    # labels for values of an element of the input plot
    text_elinfo_name    = Div(text="name:", width=elinfo_label_width1, height=elinfo_object_height)
    text_elinfo_x       = Div(text="x:", width=elinfo_label_width1, height=elinfo_object_height)
    div_element_info["x"] = text_elinfo_x
    text_elinfo_y       = Div(text="y:", width=elinfo_label_width1, height=elinfo_object_height)
    div_element_info["y"] = text_elinfo_y
    text_elinfo_angle1  = Div(text="angle:", width=elinfo_label_width1, height=elinfo_object_height)
    text_elinfo_angle2  = Div(text="°", width=elinfo_label_width2-20, height=elinfo_object_height)
    spacer_y_a          = Div(text="", width=text_elinfo_angle2.width, height=elinfo_object_height)
    text_elinfo_k1      = Div(text="spring:", width=elinfo_label_width1, height=elinfo_object_height)
    text_elinfo_k2      = Div(text="* k", width=elinfo_label_width2, height=elinfo_object_height)
    text_elinfo_length1 = Div(text="length:", width=elinfo_label_width1, height=elinfo_object_height)
    text_elinfo_length2 = Div(text="* l", width=elinfo_label_width2, height=elinfo_object_height)
    text_elinfo_force1  = Div(text="force:", width=elinfo_label_width1, height=elinfo_object_height)
    text_elinfo_force2  = Div(text="* F", width=elinfo_label_width2, height=elinfo_object_height)
    text_elinfo_moment1 = Div(text="moment:", width=elinfo_label_width1, height=elinfo_object_height)
    text_elinfo_moment2 = Div(text="* M", width=elinfo_label_width2, height=elinfo_object_height)
    text_elinfo_beam    = Div(text="BEAM", width=elinfo_object_height, height=elinfo_label_width1,
                           css_classes=["ELINFO_VERTICAL_TEXT"])
    text_elinfo_h       = Div(text="* h", width=elinfo_label_width2, height=elinfo_object_height)
    text_elinfo_ei      = Div(text="* EI", width=elinfo_label_width2, height=elinfo_object_height)
    text_elinfo_ea      = Div(text="* EA", width=elinfo_label_width2, height=elinfo_object_height)
    text_elinfo_lineload= Div(text="LINE LOAD", width=elinfo_object_height, height=elinfo_label_width1,
                               css_classes=["ELINFO_VERTICAL_TEXT"])
    text_elinfo_xn      = Div(text="* n", width=elinfo_label_width2-10, height=elinfo_object_height)
    div_element_info["xn"] = text_elinfo_xn
    text_elinfo_yq      = Div(text="* q", width=elinfo_label_width2-10, height=elinfo_object_height)
    div_element_info["yq"] = text_elinfo_yq
    text_elinfo_temp = Div(text="TEMP.", width=elinfo_object_height, height=elinfo_label_width1,
                           css_classes=["ELINFO_VERTICAL_TEXT"])
    text_elinfo_dt      = Div(text="* dT", width=elinfo_label_width2, height=elinfo_object_height)
    text_elinfo_tt      = Div(text="* T", width=elinfo_label_width2, height=elinfo_object_height)
    text_elinfo_at      = Div(text="* &alpha;T", width=elinfo_label_width2, height=elinfo_object_height)

    # text inputs showing the current value of an input plot element and taking input for a value change
    # name
    input_elinfo_name = TextInput(value="-", width=elinfo_input_width, height=elinfo_object_height, disabled=True)
    key_elinfo_n = "name"
    input_element_info[key_elinfo_n] = input_elinfo_name
    input_elinfo_name.on_change('value', partial(vis_cbs.cb_get_textinput, key=key_elinfo_n))

    # xy
    input_elinfo_x = TextInput(value="-", width=elinfo_input_width, height=elinfo_object_height, disabled=True)
    key_elinfo_x = "x"
    input_element_info[key_elinfo_x] = input_elinfo_x
    input_elinfo_x.on_change('value', partial(vis_cbs.cb_get_textinput, key=key_elinfo_x))

    input_elinfo_y = TextInput(value="-", width=elinfo_input_width, height=elinfo_object_height, disabled=True)
    key_elinfo_y = "y"
    input_element_info[key_elinfo_y] = input_elinfo_y
    input_elinfo_y.on_change('value', partial(vis_cbs.cb_get_textinput, key=key_elinfo_y))

    # angle
    input_elinfo_angle = TextInput(value="-", width=elinfo_input_width, height=elinfo_object_height, disabled=True)
    key_elinfo_angle = "angle"
    input_element_info[key_elinfo_angle] = input_elinfo_angle
    input_elinfo_angle.on_change('value', partial(vis_cbs.cb_get_textinput, key=key_elinfo_angle))

    # spring constant
    input_elinfo_k = TextInput(value="-", width=elinfo_input_width, height=elinfo_object_height, disabled=True)
    key_elinfo_k = "k"
    input_element_info[key_elinfo_k] = input_elinfo_k
    input_elinfo_k.on_change('value', partial(vis_cbs.cb_get_textinput, key=key_elinfo_k))

    # length
    input_elinfo_length = TextInput(value="-", width=elinfo_input_width, height=elinfo_object_height, disabled=True)
    key_elinfo_length = "length"
    input_element_info[key_elinfo_length] = input_elinfo_length
    input_elinfo_k.on_change('value', partial(vis_cbs.cb_get_textinput, key=key_elinfo_length))

    # point load
    input_elinfo_force = TextInput(value="-", width=elinfo_input_width, height=elinfo_object_height, disabled=True)
    key_elinfo_f = "force"
    input_element_info[key_elinfo_f] = input_elinfo_force
    input_elinfo_force.on_change('value', partial(vis_cbs.cb_get_textinput, key=key_elinfo_f))

    # moment
    input_elinfo_moment = TextInput(value="-", width=elinfo_input_width, height=elinfo_object_height, disabled=True)
    key_elinfo_m = "moment"
    input_element_info[key_elinfo_m] = input_elinfo_moment
    input_elinfo_moment.on_change('value', partial(vis_cbs.cb_get_textinput, key=key_elinfo_m))

    # beam
    input_elinfo_h = TextInput(value="-", width=elinfo_input_width, height=elinfo_object_height, disabled=True)
    key_elinfo_h = "h"
    input_element_info[key_elinfo_h] = input_elinfo_h
    input_elinfo_h.on_change('value', partial(vis_cbs.cb_get_textinput, key=key_elinfo_h))

    check_elinfo_beam = CheckboxGroup(labels=["EA -> inf.", "EI -> inf."], active=[], disabled=True,
                                      width=elinfo_input_width+elinfo_label_width1)
    group_element_info["beam"] = check_elinfo_beam
    check_elinfo_beam.on_change('active', vis_cbs.cb_elinfo_beam)

    input_elinfo_ea = TextInput(value="-", width=elinfo_input_width, height=elinfo_object_height, disabled=True)
    key_elinfo_ea = "ea"
    input_element_info[key_elinfo_ea] = input_elinfo_ea
    input_elinfo_ea.on_change('value', partial(vis_cbs.cb_get_textinput, key=key_elinfo_ea))

    input_elinfo_ei = TextInput(value="-", width=elinfo_input_width, height=elinfo_object_height, disabled=True)
    key_elinfo_ei = "ei"
    input_element_info[key_elinfo_ei] = input_elinfo_ei
    input_elinfo_ei.on_change('value', partial(vis_cbs.cb_get_textinput, key=key_elinfo_ei))

    # line load
    radio_elinfo_ll = RadioGroup(labels=["local", "global"], active=0, disabled=True,  # "angle"
                                 width=elinfo_input_width+elinfo_label_width1)
    group_element_info["ll"] = radio_elinfo_ll
    radio_elinfo_ll.on_change('active', vis_cbs.cb_elinfo_lineload)

    input_elinfo_xns = TextInput(value="-", width=elinfo_input_width, height=elinfo_object_height+20, disabled=True,
                                 title="start")
    key_elinfo_xns = "xn_start"
    input_element_info[key_elinfo_xns] = input_elinfo_xns
    input_elinfo_xns.on_change('value', partial(vis_cbs.cb_get_textinput, key=key_elinfo_xns))

    input_elinfo_xne = TextInput(value="-", width=elinfo_input_width, height=elinfo_object_height+20, disabled=True,
                                 title="end")
    key_elinfo_xne = "xn_end"
    input_element_info[key_elinfo_xne] = input_elinfo_xne
    input_elinfo_xne.on_change('value', partial(vis_cbs.cb_get_textinput, key=key_elinfo_xne))

    input_elinfo_yqs = TextInput(value="-", width=elinfo_input_width, height=elinfo_object_height, disabled=True)
    key_elinfo_yqs = "yq_start"
    input_element_info[key_elinfo_yqs] = input_elinfo_yqs
    input_elinfo_yqs.on_change('value', partial(vis_cbs.cb_get_textinput, key=key_elinfo_yqs))

    input_elinfo_yqe = TextInput(value="-", width=elinfo_input_width, height=elinfo_object_height, disabled=True)
    key_elinfo_yqe = "yq_end"
    input_element_info[key_elinfo_yqe] = input_elinfo_yqe
    input_elinfo_yqe.on_change('value', partial(vis_cbs.cb_get_textinput, key=key_elinfo_yqe))

    # temperature load
    input_elinfo_dt = TextInput(value="-", width=elinfo_input_width, height=elinfo_object_height, disabled=True)
    key_elinfo_dt = "dT"
    input_element_info[key_elinfo_dt] = input_elinfo_dt
    input_elinfo_dt.on_change('value', partial(vis_cbs.cb_get_textinput, key=key_elinfo_dt))

    input_elinfo_tt = TextInput(value="-", width=elinfo_input_width, height=elinfo_object_height, disabled=True)
    key_elinfo_tt = "T"
    input_element_info[key_elinfo_tt] = input_elinfo_tt
    input_elinfo_tt.on_change('value', partial(vis_cbs.cb_get_textinput, key=key_elinfo_tt))

    input_elinfo_at = TextInput(value="-", width=elinfo_input_width, height=elinfo_object_height, disabled=True)
    key_elinfo_at = "aT"
    input_element_info[key_elinfo_at] = input_elinfo_at
    input_elinfo_at.on_change('value', partial(vis_cbs.cb_get_textinput, key=key_elinfo_at))

    # button for deleting an input plot element
    button_elinfo_del = Button(label="Delete element", width=elinfo_label_width1+elinfo_input_width+elinfo_label_width2,
                               height=elinfo_object_height+10, disabled=False)
    button_elinfo_del.on_click(partial(vis_cbs.cb_button_delete, single=True))

    '''
    ###############################
    # CHECKBOXES FOR OUTPUT PLOTS
    ###############################
    '''
    check_labels = ["Min/ max values", "Start/ end values", "Zero points"]
    check_init_active = [1]

    check_plot_nf = CheckboxGroup(labels=check_labels, active=check_init_active)  # inline=False
    text_plot_nf = Div(text="", width=100, height=10)
    check_plot_nf.on_change('active', partial(vis_cbs.cb_toggle_characteristic_values, output_plot=plot_normal_f,
                                              div=text_plot_nf))

    check_plot_nd = CheckboxGroup(labels=check_labels, active=check_init_active)
    text_plot_nd = Div(text="", width=100, height=10)
    check_plot_nd.on_change('active', partial(vis_cbs.cb_toggle_characteristic_values, output_plot=plot_normal_disp,
                                              div=text_plot_nd))

    check_plot_sf = CheckboxGroup(labels=check_labels, active=check_init_active)
    text_plot_sf = Div(text="", width=100, height=10)
    check_plot_sf.on_change('active', partial(vis_cbs.cb_toggle_characteristic_values, output_plot=plot_shear_f,
                                              div=text_plot_sf))

    check_plot_mo = CheckboxGroup(labels=check_labels, active=check_init_active)
    text_plot_mo = Div(text="", width=100, height=10)
    check_plot_mo.on_change('active', partial(vis_cbs.cb_toggle_characteristic_values, output_plot=plot_moment,
                                              div=text_plot_mo))

    check_plot_sa = CheckboxGroup(labels=check_labels, active=check_init_active)
    text_plot_sa = Div(text="", width=100, height=10)
    check_plot_sa.on_change('active', partial(vis_cbs.cb_toggle_characteristic_values, output_plot=plot_shear_angle,
                                              div=text_plot_sa))

    check_plot_sd = CheckboxGroup(labels=check_labels, active=check_init_active)
    text_plot_sd = Div(text="", width=100, height=10)
    check_plot_sd.on_change('active', partial(vis_cbs.cb_toggle_characteristic_values, output_plot=plot_shear_disp,
                                              div=text_plot_sf))

    '''
    ###############################
    # HTML  LATEX DESCRIPTION
    ###############################
    '''
    # latex packages not working with updated bokeh!
    # description_filename = join(dirname(__file__), "description.html")
    # description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=910)

    '''
    ###############################
    # CREATE LAYOUT AND START DOCUMENT
    ###############################
    '''
    spacer = Div(text="", width=20, height=20)
    minispacer = Div(text="", width=0, height=0)

    # element buttons
    layout_supports_1 = row(button_support_clamped, button_support_normal, button_support_transverse)
    layout_supports_2 = row(button_support_fixed_joint, button_support_fixed_conti, button_support_roller_joint,
                            button_support_roller_conti)
    layout_springs = row(button_spring_support, button_spring_moment_support)
    layout_node = row(button_node)
    layout_joints = row(button_joint, button_joint_normal, button_joint_transverse, button_spring)
    layout_elements = row(button_beam)  # button_rod,
    layout_loads = row(button_load_point, button_load_moment, button_load_random, button_load_temp)
    layout_input_elements = column(spacer, text_supports, layout_supports_1, layout_supports_2,
                                   row(column(text_springs, layout_springs), spacer, minispacer,
                                       column(text_node, layout_node)),
                                   text_joints, layout_joints,
                                   text_elements, layout_elements,
                                   text_loads, layout_loads)

    # element info box
    elinfo_name = row(text_elinfo_name, input_elinfo_name)
    children_element_info[key_elinfo_n] = elinfo_name
    elinfo_xy = row(text_elinfo_x, input_elinfo_x, spacer_y_a, text_elinfo_y, input_elinfo_y)
    children_element_info[key_elinfo_x] = elinfo_xy
    elinfo_angle_length = row(text_elinfo_angle1, input_elinfo_angle, text_elinfo_angle2,
                              text_elinfo_length1, input_elinfo_length, text_elinfo_length2)
    children_element_info[key_elinfo_angle] = elinfo_angle_length
    elinfo_k = row(text_elinfo_k1, input_elinfo_k, text_elinfo_k2)
    children_element_info[key_elinfo_k] = elinfo_k
    elinfo_force = row(text_elinfo_force1, input_elinfo_force, text_elinfo_force2)
    children_element_info[key_elinfo_f] = elinfo_force
    elinfo_moment = row(text_elinfo_moment1, input_elinfo_moment, text_elinfo_moment2)
    children_element_info[key_elinfo_m] = elinfo_moment
    elinfo_beam = row(minispacer, column(minispacer, text_elinfo_beam),
                      column(check_elinfo_beam, row(input_elinfo_h, text_elinfo_h)),
                      column(row(input_elinfo_ea, text_elinfo_ea), row(input_elinfo_ei, text_elinfo_ei)))
    children_element_info[key_elinfo_h] = elinfo_beam
    elinfo_lineload = row(minispacer, column(spacer, text_elinfo_lineload), column(spacer, radio_elinfo_ll),
                          column(row(input_elinfo_xns, input_elinfo_xne),
                                 row(input_elinfo_yqs, input_elinfo_yqe)),
                          column(spacer, text_elinfo_xn, text_elinfo_yq))
    children_element_info[key_elinfo_ei] = elinfo_lineload
    elinfo_dt = row(minispacer, column(minispacer, text_elinfo_temp), column(
        row(input_elinfo_dt, text_elinfo_dt, minispacer, input_elinfo_at, text_elinfo_at),
        row(input_elinfo_tt, text_elinfo_tt)))
    children_element_info[key_elinfo_dt] = elinfo_dt
    layout_element_info = row(minispacer, column(minispacer, elinfo_name, elinfo_xy, elinfo_angle_length, spacer,
                                                 elinfo_k, elinfo_force, elinfo_moment, spacer,
                                                 elinfo_beam, spacer, elinfo_lineload, spacer, elinfo_dt, spacer,
                                                 button_elinfo_del, minispacer), minispacer,
                              css_classes=["ELEMENT_INFO_BOX"], margin=(20, 0, 0, 20), visible=True)

    # input plot with element buttons, delete and calculation buttons and divs
    user_input = row(plot_input, spacer, layout_input_elements)
    user_input_info = row(div_input, div_xy, spacer, button_del_selected, button_del_all)
    user_msg = row(div_msg, spacer, button_calc)

    # output plots and check boxes for characteristic values
    user_output = column(
        row(plot_normal_f, spacer, column(spacer, check_plot_nf, text_plot_nf)),
        row(plot_normal_disp, spacer, column(spacer, check_plot_nd, text_plot_nd)),
        row(plot_shear_f, spacer, column(spacer, check_plot_sf, text_plot_sf)),
        row(plot_moment, spacer, column(spacer, check_plot_mo, text_plot_mo)),
        row(plot_shear_angle, spacer, column(spacer, check_plot_sa, text_plot_sa)),
        row(plot_shear_disp, spacer, column(spacer, check_plot_sd, text_plot_sd)))

    # assemble complete layout
    doc_layout = column(spacer, row(spacer, spacer, dropdown_tc),
                        row(column(user_input, user_input_info, user_msg), minispacer, layout_element_info), spacer,
                        user_output)

    # add layout
    curdoc().add_root(doc_layout)
    # set title of browser tab
    curdoc().title = split(dirname(__file__))[-1].replace('_', ' ').replace('-', ' ')
