import math
from functools  import partial

# import bokeh modules
from bokeh.models.callbacks import CustomJS
from bokeh.models import ColumnDataSource

# import local files
import vis_initialization   as vis_init
import vis_elementToPlot    as vis_elToP
import vis_editElement      as vis_editEl
from Libs               import interface
from Classes            import ElementSupportEnum as eLnum
from Libs               import outputvisualization as vis_output
from testing_collection import test_cases, visualisation_tests
from ColumnDataSources  import ColumnDataSources

ds_input                         = ColumnDataSources.ds_input
ds_glyph_images                  = ColumnDataSources.ds_glyph_images
ds_glyph_beam                    = ColumnDataSources.ds_glyph_beam
ds_glyph_lineload                = ColumnDataSources.ds_glyph_lineload
ds_arrow_lineload                = ColumnDataSources.ds_arrow_lineload
ds_glyph_springsPointMomentTemp  = ColumnDataSources.ds_glyph_springsPointMomentTemp
ds_input_selected                = ColumnDataSources.ds_input_selected
ds_active_button                 = ColumnDataSources.ds_active_button
ds_element_count                 = ColumnDataSources.ds_element_count
ds_chosen_node                   = ColumnDataSources.ds_chosen_node
ds_1st_chosen                    = ColumnDataSources.ds_1st_chosen
ds_element_info                  = ColumnDataSources.ds_element_info
ds_indep_elements                = ColumnDataSources.ds_indep_elements
ds_nodedep_elements              = ColumnDataSources.ds_nodedep_elements

# variable for the currently activated element button for the input plot
button_activated = -1

# radius to select specific element in input plot
catch_radius = 0.15

# used for automatic naming of the elements in the plot using a consecutive number
object_id = 0

# current element in the element info box, used to be able to delte the single element - Tupel(name, indep, index)
elinfo_current_element = (False, False, False)
# whether user input of element info box is blocked
elinfo_input_blocked = False

# whether currently a test case is plotted - independent element should get angle and elinfo shouldn't react
plotting_test_case = False
test_case_angle = []
test_case_count_indep = 0

# used to adapt plot elements when entries in ds_input were deleted
len_ds_input = 0


# node dependent enum element values of the plot to distinguish in the java script callback cb_plot_tap()
nodedep_element_values = [eLnum.ElSupEnum.SPRING_SUPPORT.value, eLnum.ElSupEnum.SPRING_MOMENT_SUPPORT.value,
                          eLnum.ElSupEnum.SPRING.value, eLnum.ElSupEnum.BEAM.value, eLnum.ElSupEnum.LOAD_POINT.value,
                          eLnum.ElSupEnum.LOAD_MOMENT.value, eLnum.ElSupEnum.LOAD_LINE.value,
                          eLnum.ElSupEnum.LOAD_TEMP.value]


def cb_plot_tap(div_input, max_indep_elements):
    """
    JavaScript callback to create an element when mouse tap in input plot is detected and a button element is activated.
    :param div_input: bokeh Div for messages concerning the input plot (Div)
    :param max_indep_elements: maximum number of node independent elements accepted in the input plot (int)
    :return: none
    """
    global ds_chosen_node, ds_input, ds_active_button, ds_element_count, ds_element_info, indep_element_values
    cb_plot_tap_ = ColumnDataSources.cb_plot_tap_
    cb_plot_tap_.args['div']                 = div_input
    cb_plot_tap_.args['ds']                  = ds_input
    cb_plot_tap_.args['activated']           = ds_active_button
    cb_plot_tap_.args['element_count']       = ds_element_count
    cb_plot_tap_.args['max_number_elements'] = max_indep_elements
    cb_plot_tap_.args['ds_c_n']              = ds_chosen_node
    cb_plot_tap_.args['ds_e_i']              = ds_element_info
    cb_plot_tap_.args['nodedep']             = nodedep_element_values

    return cb_plot_tap_


def cb_adapt_plot_indep(attr, old, new):
    """
    Callback to react when the data source of the input plot has changed through cb_plot_tab.
    :param attr: not used
    :param old: not used, because doesn't show correct values after cb_button_delete run (dict)
    :param new: updated ds_input.data (dict)
    :return: none
    """
    global ds_indep_elements, object_id, ds_input, len_ds_input, \
        plotting_test_case, test_case_angle, test_case_count_indep

    # check if element was added or deleted or just edited
    if not len(new['x']) == len_ds_input:
        len_ds_input = len(new['x'])

        # reset "same" of plot elements, used to check which entries of ds_input still exist and are plotted
        ds_indep_elements.data['same'] = [False] * len(ds_indep_elements.data['same'])

        ds_input_x = new['x']
        ds_input_y = new['y']
        ds_input_t = new['type']
        ds_indep_x = ds_indep_elements.data['x']
        ds_indep_y = ds_indep_elements.data['y']
        ds_indep_t = ds_indep_elements.data['type']
        ds_indep_n = ds_indep_elements.data['name']
        ds_indep_s = ds_indep_elements.data['same']

        # get image glyphs that were already there before ds_input changed
        same = [False] * len(ds_input_x)
        for i in range(len(ds_input_x)):
            for j in range(len(ds_indep_x)):
                # let it get first fitting object several times - prevents new creation of same object in input plot
                if ds_input_x[i] == ds_indep_x[j] and ds_input_y[i] == ds_indep_y[j]:
                    if ds_input_t[i] == ds_indep_t[j]:
                        ds_indep_s[j] = True
                        same[i] = True
                    else:
                        same[i] = True
                        vis_init.div_input.text = "An object already exists at this position. " \
                                                  "New object wasn't created!"
                    break

        # delete image glyphs if their corresponding entries in d_input were deleted (cb_button_delete)
        # adaptive while condition necessary because length of ds_indep_x changes through deletion!
        i = 0
        while True:
            if i == len(ds_indep_x):
                break
            if not ds_indep_s[i]:
                vis_elToP.delete_indep(name=ds_indep_n[i], index=i)
            else:
                i += 1

        # create new image glyphs for elements that were added to ds_input
        for i in range(len(ds_input_x)):
            if not same[i]:
                # configure name and increse object id
                name = str(ds_input_t[i]) + "-" + str(object_id)
                object_id += 1

                # adapt name in ds_input
                ds_input_data = ds_input.data.copy()
                ds_input_data['name_user'][i] = name
                ds_input.data = ds_input_data
                # ds_input.trigger('data', ds_input.data, ds_input_data)

                if plotting_test_case:
                    try:
                        angle = test_case_angle[test_case_count_indep]
                    except:
                        angle = 0.0
                    test_case_count_indep += 1
                else:
                    angle = 0.0
                # add node independent element
                vis_elToP.add_indep(x=ds_input_x[i], y=ds_input_y[i], enum_type=ds_input_t[i], name=name, angle=angle)


def check_for_similar(enum_type, node1, node2=None):
    """
    Check if elements of same or similiar type already exist at that node/ between the nodes.
    :param enum_type: type of element for the input plot (double - ElementSupportEnum)
    :param node1: name of node, first node of line element (string)
    :param node2: name of second node of line element (string)
    :return: True if similiar object already exists (bool)
    """
    global ds_nodedep_elements
    similiar = []

    plot_n1 = ds_nodedep_elements.data["name_node1"]
    plot_n2 = ds_nodedep_elements.data["name_node2"]
    plot_t = ds_nodedep_elements.data["type"]

    # get enum_types of elements that have the same two nodes
    for i in range(len(plot_n1)):
        if(node1 == plot_n1[i] and node2 == plot_n2[i]) or (node2 == plot_n1[i] and node1 == plot_n2[i]):
            similiar.append(plot_t[i])

    if not len(similiar) == 0:
        # allow only one point load, one moment, one temperature, one spring_moment_support, one spring_support
        # per node/ edge
        if enum_type == eLnum.ElSupEnum.LOAD_POINT.value or enum_type == eLnum.ElSupEnum.LOAD_MOMENT.value \
                or enum_type == eLnum.ElSupEnum.LOAD_TEMP.value \
                or enum_type == eLnum.ElSupEnum.SPRING_MOMENT_SUPPORT.value \
                or enum_type == eLnum.ElSupEnum.SPRING_SUPPORT.value:
            for t in similiar:
                if t == enum_type:
                    return True
        # allow only one beam OR spring between two nodes
        elif enum_type == eLnum.ElSupEnum.BEAM.value or enum_type == eLnum.ElSupEnum.SPRING.value:
            for t in similiar:
                if t == eLnum.ElSupEnum.BEAM.value or t == eLnum.ElSupEnum.SPRING.value:
                    return True
        # allow only one line load between two nodes
        else:
            for t in similiar:
                if t == eLnum.ElSupEnum.LOAD_LINE.value:
                    return True

    return False


def cb_adapt_plot_nodedep(attr, old, new):
    """
    Callback to react when ds_chosen_node has changed because a node dependent element is active and a tab in the
    input plot was caught.
    :param attr: not used
    :param old: not used
    :param new: updated ds_chosen_node.data (dict)
    :return: none
    """
    global ds_indep_elements, ds_1st_chosen, ds_nodedep_elements, catch_radius

    enum_type = new['type'][0]
    new_x = new['tap_x'][0]
    new_y = new['tap_y'][0]
    node_x = 0.0
    node_y = 0.0

    ds_indep_x = ds_indep_elements.data['x']
    ds_indep_y = ds_indep_elements.data['y']
    ds_indep_n = ds_indep_elements.data['name']

    ds_1st_t = ds_1st_chosen.data['type']
    ds_1st_x = ds_1st_chosen.data['node_x']
    ds_1st_y = ds_1st_chosen.data['node_y']
    ds_1st_n = ds_1st_chosen.data['name_node1']

    ds_dep_n1 = ds_nodedep_elements.data['name_node1']
    ds_dep_n2 = ds_nodedep_elements.data['name_node2']

    # look for the clicked point for an existing x, y in the plotted independent node elements (ds_indep_elements)
    new_name = None
    for i in range(0, len(ds_indep_x)):
        if abs(ds_indep_x[i] - new_x) < catch_radius and abs(ds_indep_y[i] - new_y) < catch_radius:
            new_name = ds_indep_n[i]
            node_x = ds_indep_x[i]
            node_y = ds_indep_y[i]
            break

    # check if a node was clicked or tell user to choose one
    if new_name is not None:
        # add element if it needs only one independent node
        if enum_type == eLnum.ElSupEnum.LOAD_POINT.value or enum_type == eLnum.ElSupEnum.LOAD_MOMENT.value \
                or enum_type == eLnum.ElSupEnum.SPRING_SUPPORT.value \
                or enum_type == eLnum.ElSupEnum.SPRING_MOMENT_SUPPORT.value:
            if check_for_similar(enum_type, new_name):
                vis_init.div_input.text = "Element of this category already exists at this node. " \
                                          "Please choose another node."
            else:
                ds_dep_n1.append(new_name)
                ds_dep_n2.append(None)
                vis_elToP.add_nodedep(enum_type, node_x, node_y)
        elif not len(ds_1st_t) == 0:
            # check if first node was already chosen for that element type
            if enum_type == ds_1st_t[0]:
                # tell user to choose another node if same node was chosen twice for one element
                if node_x == ds_1st_x[0] and node_y == ds_1st_y[0]:
                    vis_init.div_input.text = "Node already chosen. Please choose second node."
                # tell user to choose another node if same/similiar object already exists between nodes
                elif check_for_similar(enum_type, new_name, ds_1st_n[0]):
                    vis_init.div_input.text = "Element of this category already exists between these two nodes. " \
                                          "Please choose another node."
                # add nodedependent element
                else:
                    # get the left/lower and the right/upper node of the two and get their distance and angle to x axis
                    # give position of left/lower (if dx=0) chosen node and save this node as node1 for the interface
                    left_lower, right_upper, center, length, angle = \
                        vis_elToP.get_1st2nd_center_length_angle(ds_1st_x[0], ds_1st_y[0], node_x, node_y)
                    # add names to data source and call method to add more values and a glyph to input plot
                    if left_lower[0] == node_x and left_lower[1] == node_y:
                        ds_dep_n1.append(new_name)
                        ds_dep_n2.append(ds_1st_n[0])
                    else:
                        ds_dep_n1.append(ds_1st_n[0])
                        ds_dep_n2.append(new_name)
                    vis_elToP.add_nodedep(enum_type, center[0], center[1], length, angle)
                    # reset first chosen node
                    data = dict(type=[], node_x=[], node_y=[], name_node1=[])
                    ds_1st_chosen.data = data
        else:
            # remember chosen node as fist one
            data = dict(type=[enum_type], node_x=[node_x], node_y=[node_y], name_node1=[new_name])
            ds_1st_chosen.data = data
            # tell user to choose a second node
            vis_init.div_input.text = "First node chosen. Please choose second one."
    else:
        vis_init.div_input.text = "Please choose an existing node in the plot."


def cb_plot_xy(div_xy, style='float:left;clear:left;font_size=10pt'):
    """
    JavaScript callback to show the x and y position of the cursor in the input plot.
    :param div_xy: bokeh Div to show the position of the cursor (Div)
    :param style: style of the message for div_xy (string)
    :return:
    """
    cb_plot_xy_ = ColumnDataSources.cb_plot_xy_
    cb_plot_xy_.args['div'] = div_xy
    return cb_plot_xy_


def cb_show_selected(attr, old, new):
    """
    Get the selected glyph elements of the input plot and make all other opaque.
    :param attr: not used
    :param old: not used
    :param new: changed ds_input_selected.data with selected independent elements of the input plot (dict)
    :return: none
    """
    global ds_indep_elements

    selected_x = new['x']
    selected_y = new['y']

    ds_indep_x = ds_indep_elements.data['x']
    ds_indep_y = ds_indep_elements.data['y']
    ds_indep_n = ds_indep_elements.data['name']

    # get selected elements from the datasource of the independent elements
    for i in range(len(ds_indep_x)):
        # if no element is selected make all elements opaque
        if len(selected_x) == 0:
            vis_editEl.set_glyph_opacity(ds_indep_n[i], 1.0)
        else:
            for j in range(len(selected_x)):
                # if element is selected make it opaque
                if selected_x[j] == ds_indep_x[i] and selected_y[j] == ds_indep_y[i]:
                    vis_editEl.set_glyph_opacity(ds_indep_n[i], 1.0)
                    break
            # if element is not selected make it transparent
            else:
                vis_editEl.set_glyph_opacity(ds_indep_n[i], 0.3)


def cb_get_selected(div_input):
    """
    JavaScript callback to react when objects of the input plot datasource change their 'selected' status.
    :param div_input: bokeh Div for messages concerning the input plot (Div)
    :return: none
    """
    global ds_input, ds_input_selected
    cb_get_selected_ = ColumnDataSources.cb_get_selected_
    cb_get_selected_.args['div'] = div_input
    cb_get_selected_.args['ds'] = ds_input
    cb_get_selected_.args['selected'] = ds_input_selected
    return cb_get_selected_ 


def cb_button_calculation(button_calc):
    """
    Callback for the "Calculate" button.
    Collects the information from the plot and passes them to the interface function to start calculations and plot the
    results in the output plots.
    :return: none
    """
    # feedback to user that calculations are initialized
    button_calc.label = "Calculating..."
    vis_init.expand_msg2user("Starting calculation...")

    # convert databases from the input plot to mechanical elements for calculations
    interface.interface(ds_indep_elements, ds_nodedep_elements)

    # show user that button action stopped
    button_calc.label = "Calculate"


def cb_button_delete(all_selected=False, single=False):
    """
    Callback for both delete buttons of the input plot and the "delete element" button of the element info box.
    :param all_selected: bool, if True button "delete all" was clicked and method deletes all plot elements,
    if False method deletes only selected elements in the plot (bool)
    :param single: Tuple of a single element displayed in the element info box that shall be deleted of the form
    (name (string), indep (bool), index (int))
    :return: none
    """
    global button_activated, object_id, ds_input, ds_1st_chosen, elinfo_current_element

    if all_selected:
        object_id = 0
        # delete all entries of the ColumnDataSource corresponding to the input plot and update the plot
        data = dict(x=[], y=[], type=[], name_user=[])
        ds_input.data = data
        ds_input.trigger('data', ds_input.data, ds_input.data)
        # deactivate currently activated button element
        if not button_activated == -1:
            found, button_enum = eLnum.get_enum_of_value(eLnum.ElSupEnum, button_activated)
            cb_button_element_click(button_enum)
    elif single:
        if elinfo_current_element[1]:
            del ds_input.data['x'][elinfo_current_element[2]]
            del ds_input.data['y'][elinfo_current_element[2]]
            del ds_input.data['type'][elinfo_current_element[2]]
            del ds_input.data['name_user'][elinfo_current_element[2]]
            ds_input.trigger('data', ds_input.data, ds_input.data)
        else:
            vis_elToP.delete_nodedep(name_nodedep=elinfo_current_element[0], index_nodedep=elinfo_current_element[2])
    else:
        s_x = ds_input_selected.data['x']
        s_y = ds_input_selected.data['y']
        len_s = len(s_x)
        len_ds = len(ds_input.data['x'])

        # delete selected elements from the datasource of the input plot (ds_input) and update
        for i in range(len_s):
            for j in range(len_ds):
                if s_x[i] == ds_input.data['x'][j] and s_y[i] == ds_input.data['y'][j]:
                    del ds_input.data['x'][j]
                    del ds_input.data['y'][j]
                    del ds_input.data['type'][j]
                    del ds_input.data['name_user'][j]
                    len_ds -= 1
                    break
        ds_input.trigger('data', ds_input.data, ds_input.data)

        # reset datasource for selected element
        ds_input_selected.data = dict(x=[], y=[])

    # reset datasource for first node for line elements
    data = dict(type=[], node_x=[], node_y=[], name_node1=[])
    ds_1st_chosen.data = data


def cb_button_element_click(button_enum):
    """
    Callback for all element buttons:
    - deselects previous button and select new button or deselect selected button if it already was selected before
    - saves selected one as Enum in 'button_activated' and change it's background color
    :param button_enum: Enum that corresponds to the button that was clicked (ElementSupportEnum)
    :return: none
    """
    global button_activated

    # unselect button if same button is selected again
    if not button_activated == -1 and button_activated == button_enum.value:
        button_style = button_enum.name
        vis_init.buttons[button_activated].css_classes = [button_style]

        # update the currently activated button to none
        button_activated = -1
        ds_active_button.data['type'] = [-1]
        ds_active_button.trigger('data', ds_active_button.data, ds_active_button.data)

        # reset datasource for first node for line elements
        data = dict(type=[], node_x=[], node_y=[], name_node1=[])
        ds_1st_chosen.data = data
        return

    # unselect previously selected button, if one was selected before at all
    if not button_activated == -1:
        found, button_style, value = eLnum.value_in_enum(eLnum.ElSupEnum, button_activated)
        vis_init.buttons[button_activated].css_classes = [button_style]
    else:
        reset_element_info()

    # change background color of newly selected element button
    button_style = button_enum.name + '_selected'
    vis_init.buttons[button_enum.value].css_classes = [button_style]

    # update the currently activated button
    button_activated = button_enum.value
    ds_active_button.data['type'] = [button_activated]
    ds_active_button.trigger('data', ds_active_button.data, ds_active_button.data)

    # reset datasource for first node for line elements
    data = dict(type=[], node_x=[], node_y=[], name_node1=[])
    ds_1st_chosen.data = data


def cb_toggle_characteristic_values(attr, old, new, output_plot, div):
    """
    Check which checkboxes to corresponding output plot are active. For active ones show the characteristic values.
    :param attr: not used
    :param old: attribute 'active' of the bokeh CheckboxGroup how it was before it changed (list)
    :param new: changed attribute 'active' of the bokeh CheckboxGroup (list)
    :param output_plot: the specific output plot (bokeh figure)
    :param div: bokeh Div below the checkbox (Div)
    :return: none
    """
    # activation of max/ min values has changed
    if 0 in new and 0 not in old:
        vis_output.toggle_extreme_values(output_plot, True)
    elif 0 not in new and 0 in old:
        vis_output.toggle_extreme_values(output_plot, False)

    # activation of start/ end values has changed
    if 1 in new and 1 not in old:
        vis_output.toggle_bound_vals(output_plot, True)
    elif 1 not in new and 1 in old:
        vis_output.toggle_bound_vals(output_plot, False)

    # activation of zero points has changed
    if 2 in new and 2 not in old:
        vis_output.toggle_zero_crossing(output_plot, True)
    elif 2 not in new and 2 in old:
        vis_output.toggle_zero_crossing(output_plot, False)


def get_indep_name_from_position(x, y):
    """
    Get the name of a node independent element at the given position.
    :param x: x position of the element (double)
    :param y: y position of the element (double)
    :return: name of the element or None if no element was found at that position (string or None)
    """
    global ds_indep_elements
    ds_indep_x = ds_indep_elements.data['x']
    ds_indep_y = ds_indep_elements.data['y']
    ds_indep_n = ds_indep_elements.data['name']

    x = round(x, 1)
    y = round(y, 1)

    indep_name = None
    for i in range(len(ds_indep_x)):
        if ds_indep_x[i] == x and ds_indep_y[i] == y:
            indep_name = ds_indep_n[i]
            break
    return indep_name


def cb_plot_testcase(attr, old, new):
    """
    Plot given test case to the input plot and show results in the output plots.
    :param attr: not used
    :param old: not used
    :param new: changed attribute 'value' of the dropdown menu testcases (string)
    :return: none
    """
    global plotting_test_case

    # bool to show callbacks that a testcase is being plotted
    plotting_test_case = True

    # clear input plot
    cb_button_delete(all_selected=True)

    # start plotting of specific test case
    if new == "single_beam_load":
        vis_init.expand_msg2user("Single beam lineload test")
        visualisation_tests.single_beam_lineload_visu()
    elif new == "two_beam_lineload":
        vis_init.expand_msg2user("Two beam lineload test")
        visualisation_tests.two_beam_lineload_visu()
    elif new == "fin_struc_soft_lab":
        vis_init.expand_msg2user("Final structure software lab")
        visualisation_tests.example_unterlagen_visu()

    # testcase plotting done
    plotting_test_case = False


def reset_element_info():
    """
    Hide and reset the element info box: clear all values and disable all text inputs and the groups.
    :return: none
    """
    # hide element info box
    # vis_init.layout_element_info.visible = False
    # reset widgets in element info box (WARNING: too slow!)
    # vis_init.layout_element_info.children[1].children = []

    elinfo = vis_init.input_element_info
    for key in elinfo:
        elinfo[key].disabled = True
        elinfo[key].value = "-"
    vis_init.group_element_info["beam"].disabled = True
    vis_init.group_element_info["ll"].disabled = True


# TODO: idea - add button "adapt angle to beam" for independent elements like a clamped support
def cb_show_element_info(attr, old, new, indep=False, nodedep=False):
    """
    Callback to show information about an element in the input plot when ds_element_info was changed. ds_element_info
    gets changed by cb_plot_tap when a tap in the input plot was caught without an element button being active.
    Also called when an element was just added to the plot and it was not an element of a test case.
    :param attr: not used
    :param old: not used
    :param new: changed ds_element_info.data when no button element is active and a tap in the plot was caught (dict)
    :param indep: True if just added element is a node independent one (bool)
    :param nodedep: True if just added element is a node independent one (bool)
    :return: none
    """
    global catch_radius, ds_indep_elements, ds_nodedep_elements, \
        ds_glyph_springsPointMomentTemp, ds_glyph_beam, ds_glyph_lineload, \
        elinfo_current_element, elinfo_input_blocked

    # block user input while element info box gets changed (because of cb_get_textinput)
    elinfo_input_blocked = True

    reset_element_info()
    elinfo = vis_init.input_element_info

    indep_x = ds_indep_elements.data['x']
    indep_y = ds_indep_elements.data['y']
    indep_t = ds_indep_elements.data['type']
    indep_n = ds_indep_elements.data['name']
    indep_a = ds_indep_elements.data['angle']

    nodedep_n1 = ds_nodedep_elements.data['name_node1']
    nodedep_n2 = ds_nodedep_elements.data['name_node2']
    nodedep_t = ds_nodedep_elements.data['type']
    nodedep_n = ds_nodedep_elements.data['name']
    nodedep_x = ds_nodedep_elements.data['x']
    nodedep_y = ds_nodedep_elements.data['y']
    nodedep_l = ds_nodedep_elements.data['length']
    nodedep_dt = ds_nodedep_elements.data['dT_T']
    nodedep_k = ds_nodedep_elements.data['k']
    nodedep_h = ds_nodedep_elements.data['h']
    nodedep_ei = ds_nodedep_elements.data['ei']
    nodedep_ea = ds_nodedep_elements.data['ea']
    nodedep_m = ds_nodedep_elements.data['moment']
    nodedep_f = ds_nodedep_elements.data['f']
    nodedep_lll = ds_nodedep_elements.data['ll_local']
    nodedep_llxn = ds_nodedep_elements.data['ll_x_n']
    nodedep_llyq = ds_nodedep_elements.data['ll_y_q']
    nodedep_a = ds_nodedep_elements.data['angle']

    # check if element was just added
    if indep:
        index = len(indep_x) - 1
        name = indep_n[index]
    elif nodedep:
        index = len(ds_nodedep_elements.data['x']) - 1
        name = nodedep_n[index]
    # search for element in data sources if it was not just added
    else:
        # initialize for element search
        index = -1
        name = False
        tap_x = new['tap_x'][0]
        tap_y = new['tap_y'][0]
        # check if tap was on an node independent element in the input plot
        for i in range(0, len(indep_x)):
            if abs(indep_x[i] - tap_x) < catch_radius and abs(indep_y[i] - tap_y) < catch_radius:
                index = i
                name = indep_n[index]
                indep = True
                break
        # check if tap was on a node dependent element
        else:
            # search in glyph data source of type spring, load_point, load_moment or temp
            ds_glyph = ds_glyph_springsPointMomentTemp
            ds_glyph_x = ds_glyph.data['glyph_x']
            ds_glyph_y = ds_glyph.data['glyph_y']
            for j in range(len(ds_glyph_x)):
                if abs(ds_glyph_x[j] - tap_x) < catch_radius and abs(ds_glyph_y[j] - tap_y) < catch_radius:
                    name = ds_glyph.data['name_user'][j]
                    break
            # search in glyph data source of beams
            else:
                ds_glyph = ds_glyph_beam
                ds_glyph_x = ds_glyph.data['x']
                ds_glyph_y = ds_glyph.data['y']
                for j in range(len(ds_glyph_x)):
                    if abs(ds_glyph_x[j] - tap_x) < catch_radius and abs(ds_glyph_y[j] - tap_y) < catch_radius:
                        name = ds_glyph.data['name_user'][j]
                        break
                # search in glyph data source of line loads
                else:
                    ds_glyph = ds_glyph_lineload
                    ds_glyph_x = ds_glyph.data['glyph_x']
                    ds_glyph_y = ds_glyph.data['glyph_y']
                    for j in range(len(ds_glyph_x)):
                        if abs(ds_glyph_x[j] - tap_x) < catch_radius and abs(ds_glyph_y[j] - tap_y) < catch_radius:
                            name = ds_glyph.data['name_user'][j]
                            break
            # get index of element in data source of node dependent elements
            if name:
                for i in range(len(nodedep_n)):
                    if name == nodedep_n[i]:
                        index = i
                        break

    # reaction if no element was found for that tap
    if index == -1:
        vis_init.div_input.text = "No button element active and no element of graph clicked."
        return

    # make information about current element global for the callbacks and get enum_type
    if indep:
        elinfo_current_element = (name, True, index)
        enum_type = indep_t[index]
    else:
        elinfo_current_element = (name, False, index)
        enum_type = nodedep_t[index]

    # adapt element info box
    elinfo["name"].value = name
    if indep:
        # set values
        elinfo["x"].value = "%3.1f" % indep_x[index]
        vis_init.div_element_info["x"].text = "x:"
        elinfo["y"].value = "%3.1f" % indep_y[index]
        vis_init.div_element_info["y"].text = "y:"
        # enable input
        if not enum_type == eLnum.ElSupEnum.NODE.value and not enum_type == eLnum.ElSupEnum.JOINT.value:
            elinfo["angle"].disabled = False
            elinfo["angle"].value = "%3.1f" % math.degrees(indep_a[index])
    elif enum_type == eLnum.ElSupEnum.SPRING_SUPPORT.value or enum_type == eLnum.ElSupEnum.SPRING_MOMENT_SUPPORT.value:
        # set values
        elinfo["x"].value = "%3.1f" % nodedep_x[index]
        vis_init.div_element_info["x"].text = "x:"
        elinfo["y"].value = "%3.1f" % nodedep_y[index]
        vis_init.div_element_info["y"].text = "y:"
        elinfo["angle"].value = "%3.1f" % math.degrees(nodedep_a[index])
        elinfo["k"].value = "%3.1f" % nodedep_k[index]
        # enable input
        elinfo["angle"].disabled = False
        elinfo["k"].disabled = False
    elif enum_type == eLnum.ElSupEnum.SPRING.value:
        # set values
        elinfo["x"].value = nodedep_n1[index]
        vis_init.div_element_info["x"].text = "node 1:"
        elinfo["y"].value = nodedep_n2[index]
        vis_init.div_element_info["y"].text = "node 2:"
        elinfo["angle"].value = "%3.1f" % math.degrees(nodedep_a[index])
        elinfo["k"].value = "%3.1f" % nodedep_k[index]
        # enable input
        elinfo["k"].disabled = False
    elif enum_type == eLnum.ElSupEnum.LOAD_POINT.value:
        # set values
        elinfo["x"].value = "%3.1f" % nodedep_x[index]
        vis_init.div_element_info["x"].text = "x:"
        elinfo["y"].value = "%3.1f" % nodedep_y[index]
        vis_init.div_element_info["y"].text = "y:"
        elinfo["angle"].value = "%3.1f" % math.degrees(nodedep_a[index])
        elinfo["force"].value = "%3.1f" % nodedep_f[index]
        # enable input
        elinfo["angle"].disabled = False
        elinfo["force"].disabled = False
    elif enum_type == eLnum.ElSupEnum.LOAD_MOMENT.value:
        # set values
        elinfo["x"].value = "%3.1f" % nodedep_x[index]
        vis_init.div_element_info["x"].text = "x:"
        elinfo["y"].value = "%3.1f" % nodedep_y[index]
        vis_init.div_element_info["y"].text = "y:"
        elinfo["moment"].value = "%3.1f" % nodedep_m[index]
        # enable input
        elinfo["moment"].disabled = False
    elif enum_type == eLnum.ElSupEnum.LOAD_TEMP.value:
        # set values
        elinfo["x"].value = nodedep_n1[index]
        vis_init.div_element_info["x"].text = "node 1:"
        elinfo["y"].value = nodedep_n2[index]
        vis_init.div_element_info["y"].text = "node 2:"
        elinfo["dT"].value = "%3.1f" % nodedep_dt[index][0]
        elinfo["T"].value = "%3.1f" % nodedep_dt[index][1]
        elinfo["aT"].value = "%3.1f" % nodedep_dt[index][2]
        # enable input
        elinfo["dT"].disabled = False
        elinfo["T"].disabled = False
        elinfo["aT"].disabled = False
    elif enum_type == eLnum.ElSupEnum.BEAM.value:
        # set values
        elinfo["x"].value = nodedep_n1[index]
        vis_init.div_element_info["x"].text = "node 1:"
        elinfo["y"].value = nodedep_n2[index]
        vis_init.div_element_info["y"].text = "node 2:"
        elinfo["angle"].value = "%3.1f" % math.degrees(nodedep_a[index])
        elinfo["length"].value = "%3.1f" % nodedep_l[index]
        elinfo["h"].value = "%3.1f" % nodedep_h[index]
        ea = nodedep_ea[index]
        ei = nodedep_ei[index]
        active = []
        if ea == float("inf"):
            active.append(0)
        else:
            elinfo["ea"].value = "%3.1f" % ea
            elinfo["ea"].disabled = False

        if ei == float("inf"):
            active.append(1)
        else:
            elinfo["ei"].value = "%3.1f" % ei
            elinfo["ei"].disabled = False
        vis_init.group_element_info["beam"].active = active
        # enable input
        vis_init.group_element_info["beam"].disabled = False
        elinfo["h"].disabled = False
    elif enum_type == eLnum.ElSupEnum.LOAD_LINE.value:
        # set values
        elinfo["x"].value = nodedep_n1[index]
        vis_init.div_element_info["x"].text = "node 1:"
        elinfo["y"].value = nodedep_n2[index]
        vis_init.div_element_info["y"].text = "node 2:"
        elinfo["length"].value = "%3.1f" % nodedep_l[index]
        elinfo["xn_start"].value = "%3.1f" % nodedep_llxn[index][0]
        elinfo["xn_end"].value = "%3.1f" % nodedep_llxn[index][1]
        elinfo["yq_start"].value = "%3.1f" % nodedep_llyq[index][0]
        elinfo["yq_end"].value = "%3.1f" % nodedep_llyq[index][1]
        local = nodedep_lll[index]
        if local:
            vis_init.group_element_info["ll"].active = 0
            vis_init.div_element_info["xn"].text = "* n"
            vis_init.div_element_info["yq"].text = "* q"
        else:
            vis_init.group_element_info["ll"].active = 1
            vis_init.div_element_info["xn"].text = "* p<sub>x</sub>"
            vis_init.div_element_info["yq"].text = "* p<sub>y</sub>"
        # enable input
        vis_init.group_element_info["ll"].disabled = False
        elinfo["xn_start"].disabled = False
        elinfo["xn_end"].disabled = False
        elinfo["yq_start"].disabled = False
        elinfo["yq_end"].disabled = False

    # resize element info box to children truly containing information (WARNING: too slow!)
    # vis_init.layout_element_info.children[1].children.insert(0, vis_init.children_element_info["del"])
    # vis_init.layout_element_info.children[1].children.insert(0, vis_init.children_element_info["name"])
    # for key in elinfo:
    #     if not key == "name" and not key == "del":
    #         if not elinfo[key].value == "":
    #             child = vis_init.children_element_info[key]
    #             child_index = len(vis_init.layout_element_info.children[1].children) - 1
    #             vis_init.layout_element_info.children[1].children.insert(child_index, child)
    # show element info box
    # vis_init.layout_element_info.visible = True

    # release for user input
    elinfo_input_blocked = False


# TODO: idea - input of different symbols, e.g. also allow "F*l" not only "M" for a moment
def cb_get_textinput(attr, old, new, key):
    """
    Callback for the TextInputs of the element info box.
    :param attr: not used
    :param old: previous attribute 'value' of the TextInput (string)
    :param new: changed attribute 'value' of the TextInput (string)
    :param key: key of the specific TextInput (string)
    :return: none
    """
    global elinfo_current_element, elinfo_input_blocked, ds_indep_elements, ds_nodedep_elements

    # check whether user input is blocked
    if elinfo_input_blocked:
        return

    element_name = elinfo_current_element[0]
    element_indep = elinfo_current_element[1]
    element_index = elinfo_current_element[2]

    try:
        value = float(new)
    except ValueError:
        vis_init.div_input.text = "Error: Please enter a number!"
        return

    # TODO: idea - don't accept zeros as TextInput for some keys?
    # if not(key == "angle" or key == "xn_start" or key == "xn_end" or key == "yq_start" or key == "yq_end") \
    #         and value == 0:
    #     vis_init.div_input.text = "Error: Please enter a non-zero number!"
    #     return

    # change data sources and glyphs in plot according to text input
    if key == "angle":
        # convert angle to radians and call method to adapt the angle in the input plot
        angle = math.radians(value)
        if element_indep:
            ds_indep_elements.data['angle'][element_index] = angle
            vis_editEl.change_angle_indep(element_name, angle, element_index)
        else:
            ds_nodedep_elements.data['angle'][element_index] = angle
            vis_editEl.change_angle_nodedep(element_name, angle, element_index)
    elif key == "k":
        k = ds_nodedep_elements.data['k'][element_index]
        ds_nodedep_elements.data['k'][element_index] = value
        if value < 0 <= k:
            vis_editEl.draw_moment_negative(element_name, element_index, negative=True)
        elif value > 0 >= k:
            vis_editEl.draw_moment_negative(element_name, element_index, negative=False)
    elif key == "force":
        ds_nodedep_elements.data['f'][element_index] = value
    elif key == "moment":
        moment = ds_nodedep_elements.data['moment'][element_index]
        ds_nodedep_elements.data['moment'][element_index] = value
        if value < 0 <= moment:
            vis_editEl.draw_moment_negative(element_name, element_index, negative=True)
        elif value > 0 >= moment:
            vis_editEl.draw_moment_negative(element_name, element_index, negative=False)
    elif key == "h":
        ds_nodedep_elements.data['h'][element_index] = value
    elif key == "ea":
        ds_nodedep_elements.data['ea'][element_index] = value
    elif key == "ei":
        ds_nodedep_elements.data['ei'][element_index] = value
    elif key == "xn_start" or key == "xn_end" or key == "yq_start" or key == "yq_end":
        nodedep_llxn = ds_nodedep_elements.data['ll_x_n']
        nodedep_llyq = ds_nodedep_elements.data['ll_y_q']
        elinfo = vis_init.input_element_info
        elinfo_input_blocked = True
        if key == "xn_start":
            xn_start = value
            xn_end = nodedep_llxn[element_index][1]
            yq_start = nodedep_llyq[element_index][0]
            yq_end = nodedep_llyq[element_index][1]
            if (xn_start == 0 and xn_end == 0 and yq_start == 0 and yq_end == 0):
                yq_start, yq_end = -1, -1
                elinfo["yq_start"].value = "%3.1f" % yq_start
                elinfo["yq_end"].value = "%3.1f" % yq_end  
            elif (xn_start > 0 and xn_end <= 0) or (xn_start < 0 and xn_end >= 0):
                xn_end = 0
                elinfo["xn_end"].value = "%3.1f" % xn_end
        elif key == "xn_end":
            xn_start = nodedep_llxn[element_index][0]
            xn_end = value
            yq_start = nodedep_llyq[element_index][0]
            yq_end = nodedep_llyq[element_index][1]
            if (xn_end == 0 and xn_start == 0 and yq_start == 0 and yq_end == 0):
                yq_start, yq_end = -1, -1
                elinfo["yq_start"].value = "%3.1f" % yq_start
                elinfo["yq_end"].value = "%3.1f" % yq_end
            elif (xn_end > 0 and xn_start <= 0) or (xn_end < 0 and xn_start >= 0):
                xn_start = 0
                elinfo["xn_start"].value = "%3.1f" % xn_start
        elif key == "yq_start":
            xn_start = nodedep_llxn[element_index][0]
            xn_end = nodedep_llxn[element_index][1]
            yq_start = value
            yq_end = nodedep_llyq[element_index][1]
            if (yq_start == 0 and yq_end == 0 and xn_end == 0 and xn_start == 0):
                xn_start, xn_end = 1, 1
                elinfo["xn_start"].value = "%3.1f" % xn_start
                elinfo["xn_end"].value = "%3.1f" % xn_end
            elif (yq_start > 0 and yq_end <= 0) or (yq_start < 0 and yq_end >= 0):
                yq_end = 0
                elinfo["yq_end"].value = "%3.1f" % yq_end
        else:
            xn_start = nodedep_llxn[element_index][0]
            xn_end = nodedep_llxn[element_index][1]
            yq_start = nodedep_llyq[element_index][0]
            yq_end = value
            if (yq_end == 0 and yq_start == 0 and xn_end == 0 and xn_start == 0):
                xn_start, xn_end = 1, 1
                elinfo["xn_start"].value = "%3.1f" % xn_start
                elinfo["xn_end"].value = "%3.1f" % xn_end
            elif (yq_end > 0 and yq_start <= 0) or (yq_end < 0 and yq_start >= 0):
                yq_start = 0
                elinfo["yq_start"].value = "%3.1f" % yq_start
        elinfo_input_blocked = False
        # check lineload before change
        # one value has to be non-zero and start end are either >=0 or <=0
        # TODO (Done): idea - change acceptance of line load values? the way it is right now, one value needs to be zero before
        #  load direction can be changed
        if not(xn_start == 0 and xn_end == 0 and yq_start == 0 and yq_end == 0):
            load_x_n = (xn_start, xn_end)
            load_y_q = (yq_start, yq_end)
            # change data source
            nodedep_llxn[element_index] = load_x_n
            nodedep_llyq[element_index] = load_y_q
            # draw adapted line load
            local = ds_nodedep_elements.data['ll_local'][element_index]
            vis_editEl.draw_lineload(element_name, load_x_n, load_y_q, local, element_index)
        else:
            vis_init.div_input.text = "Error: Invalid line load values, one value has to be non-zero!"
            return
    elif key == "dT":
        tt = ds_nodedep_elements.data['dT_T'][element_index][1]
        at = ds_nodedep_elements.data['dT_T'][element_index][2]
        ds_nodedep_elements.data['dT_T'][element_index] = (value, tt, at)
    elif key == "T":
        dt = ds_nodedep_elements.data['dT_T'][element_index][0]
        at = ds_nodedep_elements.data['dT_T'][element_index][2]
        ds_nodedep_elements.data['dT_T'][element_index] = (dt, value, at)
    elif key == "aT":
        dt = ds_nodedep_elements.data['dT_T'][element_index][0]
        tt = ds_nodedep_elements.data['dT_T'][element_index][1]
        ds_nodedep_elements.data['dT_T'][element_index] = (dt, tt, value)

    # tell user about changed value
    vis_init.div_input.text = "New value accepted!"


def cb_elinfo_beam(attr, old, new):
    """
    Callback for the beam CheckboxGroup.
    Set EI and/ or EA to be infinite.
    :param attr: not used
    :param old: not used
    :param new: changed attribute 'active' of the beam CheckboxGroup (list)
    :return: none
    """
    global elinfo_current_element, elinfo_input_blocked, ds_nodedep_elements

    # block user input while element info box gets changed (because of cb_get_textinput)
    elinfo_input_blocked = True

    elinfo = vis_init.input_element_info
    element_index = elinfo_current_element[2]

    # get current state of EA and EI
    ea_infinite = False
    ei_infinite = False
    if ds_nodedep_elements.data['ea'][element_index] == float("inf"):
        ea_infinite = True
    if ds_nodedep_elements.data['ei'][element_index] == float("inf"):
        ei_infinite = True

    # EA was changed to infinite
    if 0 in new and not ea_infinite:
        ds_nodedep_elements.data['ea'][element_index] = float("inf")
        elinfo["ea"].disabled = True
    # EA was changed to finite
    elif 0 not in new and ea_infinite:
        ds_nodedep_elements.data['ea'][element_index] = 1.0
        elinfo["ei"].value = "%3.1f" % 1.0
        elinfo["ea"].disabled = False

    # EI was changed to infinite
    if 1 in new and not ei_infinite:
        ds_nodedep_elements.data['ei'][element_index] = float("inf")
        elinfo["ei"].disabled = True
    # EI was changed to finite
    elif 1 not in new and ei_infinite:
        ds_nodedep_elements.data['ei'][element_index] = 1.0
        elinfo["ei"].value = "%3.1f" % 1.0
        elinfo["ei"].disabled = False

    # release for user input
    elinfo_input_blocked = False


def cb_elinfo_lineload(attr, old, new):
    """
    Callback for the line load RadioGroup.
    Change from local to global coordinates and the other way round.
    :param attr: not used
    :param old: not used
    :param new: changed attribute 'active' of the line load radio group (int)
    :return: none
    """
    global elinfo_current_element, ds_nodedep_elements

    element_name = elinfo_current_element[0]
    element_index = elinfo_current_element[2]
    load_x_n = ds_nodedep_elements.data['ll_x_n'][element_index]
    load_y_q = ds_nodedep_elements.data['ll_y_q'][element_index]

    # load is locally defined
    if new == 0:
        vis_init.div_element_info["xn"].text = "* n"
        vis_init.div_element_info["yq"].text = "* q"
        ds_nodedep_elements.data['ll_local'][element_index] = True
        vis_editEl.draw_lineload(element_name, load_x_n, load_y_q, True, element_index)
    # load is globally defined
    elif new == 1:
        vis_init.div_element_info["xn"].text = "* p<sub>x</sub>"
        vis_init.div_element_info["yq"].text = "* p<sub>y</sub>"
        ds_nodedep_elements.data['ll_local'][element_index] = False
        vis_editEl.draw_lineload(element_name, load_x_n, load_y_q, False, element_index)
