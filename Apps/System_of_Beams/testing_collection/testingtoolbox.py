import math
import copy
from sympy import Symbol

from Libs import symbolictoolbox as symbbox
from Libs import outputvisualization as out_vis
from Libs import print_function_helpers as prhlp
import vis_elementToPlot as vis_el
from Classes import ElementSupportEnum as ElSupEnum
from Element_Calculation import ElementCalculation
from Classes.CurrentDocument import CurrentDoc


def print_graphs(curr_doc: CurrentDoc, functions, x, l_list, knot_list):
    """
    Visualises a given calculation results in the output
    :param functions: List of lists of resulting function. See comment plot_output_functions for structure
    :param x: symbol the functions shell be plotted over
    :param l_list: list of all length values for every element
    :param knot_list: list of knots [[start_knot_1, end_knot_1], ... , [start_knot_n, end_knot_n]]
    """
    out_vis.plot_output_functions(curr_doc, functions, knot_list, x, l_list)


def vis_structure_from_input(curr_doc: CurrentDoc, nodeindep_list, nodedep_list):
    """
    Visualises a structure being defined by nodeindep_list & nodedep_list
    :param nodeindep_list: all node independent elements
    :param nodedep_list: all node dependent elements
    """
    nodedep_to_plot = copy.deepcopy(nodedep_list)
    nodeindep_to_plot = prhlp.list_with_every_knot_only_once(nodeindep_list)
    nodedep_list.sort(key=lambda ele: ele.id_el_)
    prhlp.print_knot_and_element_list(nodeindep_to_plot, nodedep_list)
    vis_nodeindep_elements(curr_doc, nodeindep_to_plot)
    vis_nodedep_elements(curr_doc, nodedep_to_plot)
    print("VIS DONE")


def get_knot_name_from_nodeindep_list(nodeindep_list, x, y, tol=10e-3):
    """
    Gets the name of a knot by the x and y position
    :param nodeindep_list: list of knots to search in
    :param x: x-position of searched knot
    :param y: y-position of searched knot
    :param tol: accuracy the knot shell be searched
    :return: name of the knot if found, else None
    """
    x_ind = []
    y_ind = []
    for i in range(len(nodeindep_list.data['type'])):
        if abs(nodeindep_list.data['x'][i] - x) <= tol:
            x_ind.append(i)
    if x_ind:
        for i in range(len(nodeindep_list.data['type'])):
            if abs(nodeindep_list.data['y'][i] - y) <= tol:
                y_ind.append(i)
    ind = [el for el in x_ind if el in y_ind]
    if len(ind) >= 1:
        # print("Node found: " + str(nodeindep_list.data['name'][ind[0]]))
        return nodeindep_list.data['name'][ind[0]]
    else:
        return None


def add_nodeindep_single_el(curr_doc: CurrentDoc, x, y, el_type, name, angle):
    """
    Adds a nodeindep element to the data sources
    """
    curr_doc.test_case_angle.append(angle)
    curr_doc.data_sources.ds_input.data['x'].append(round(x, 1))
    curr_doc.data_sources.ds_input.data['y'].append(round(y, 1))
    curr_doc.data_sources.ds_input.data['type'].append(el_type)
    curr_doc.data_sources.ds_input.data['name_user'].append(name)
    curr_doc.data_sources.ds_input.trigger('data', curr_doc.data_sources.ds_input.data, curr_doc.data_sources.ds_input.data)


def symb2float(el):
    """
    Converts a symbolic expression to float
    """
    if isinstance(el, float) or isinstance(el, int):
        return el
    return float(symbbox.remove_free_symbols(el, None))


def convert_lineload_to_input(n, q, n_symb, q_symb, length):
    """
    Converts symbolic lineloads to necessary input structure of start and end point
    """
    if isinstance(n, float) or isinstance(n, int):
        n_start = n
        n_end = n
    else:
        n_start = symb2float(n.subs(n_symb, 0))
        n_end = symb2float(n.subs(n_symb, length))

    if isinstance(q, float) or isinstance(q, int):
        q_start = q
        q_end = q
    else:
        q_start = symb2float(q.subs(q_symb, 0))
        q_end = symb2float(q.subs(q_symb, length))
    return n_start, n_end, q_start, q_end


def add_knots_to_visu(curr_doc: CurrentDoc, knot1, knot2):
    """
    Adds two knots to the nodedep data source
    :return:
    """
    curr_doc.data_sources.ds_nodedep_elements.data['name_node1'].append(knot1)
    curr_doc.data_sources.ds_nodedep_elements.data['name_node2'].append(knot2)


def add_nodedep_two_knots(curr_doc: CurrentDoc, el, el_type):
    """
    Visualises all beams, lineloads and springs
    :param el: Element to visualise type(el) = ElementCalculation
    :param el_type: type of the element
    :return:
    """
    left_node, right_node, (x_middle, y_middle), length, angle = \
        vis_el.get_1st2nd_center_length_angle(el.x1_, el.y1_, el.x2_, el.y2_)
    knot1 = get_knot_name_from_nodeindep_list(curr_doc.data_sources.ds_indep_elements, left_node[0], left_node[1])
    knot2 = get_knot_name_from_nodeindep_list(curr_doc.data_sources.ds_indep_elements, right_node[0], right_node[1])
    # print("knot1: " + str(knot1))
    # print("el_type: {}\t x_middle: {}\t y_middle: {}".format(el_type, x_middle, y_middle))
    if ElSupEnum.check_beams_and_rods(el_type):
        add_knots_to_visu(curr_doc, knot1, knot2)
        vis_el.add_nodedep(curr_doc, el_type, x_middle, y_middle, length=length, angle=angle, h=symb2float(el.h_),
                           ei=symb2float(el.ei_), ea=symb2float(el.ea_))
        if el.lineloads[0] != 0 or el.lineloads[1] != 0:
            n_run_var = symbbox.get_free_symbols(el.lineloads[0], Symbol('n'))
            q_run_var = symbbox.get_free_symbols(el.lineloads[1], Symbol('q'))
            if len(n_run_var) >= 1:
                n_run_var = n_run_var[0]
            elif len(n_run_var) == 0:
                n_run_var = 0
            if len(q_run_var) >= 1:
                q_run_var = q_run_var[0]
            elif len(q_run_var) == 0:
                q_run_var = 0
            n_start, n_end, q_start, q_end = convert_lineload_to_input(el.lineloads[0], el.lineloads[1], n_run_var, q_run_var, el.length_)
            # print("Forces: n_s: {}\t n_e: {}\t q_s: {}\t q_e: {}".format(n_start, n_end, q_start, q_end))
            add_knots_to_visu(curr_doc, knot1, knot2)
            vis_el.add_nodedep(curr_doc, ElSupEnum.ElSupEnum.LOAD_LINE.value, x_middle, y_middle, length=length, angle=angle,
                               ll_local=True, ll_x_n=(n_start, n_end), ll_y_q=(-q_start, -q_end))   # minus q, due to the different axes
        if not el.temp_props.is_empty():
            add_knots_to_visu(curr_doc, knot1, knot2)
            start_temp = symb2float(symbbox.remove_free_symbols(el.temp_props.start_temp, None))
            grad_temp = symb2float(symbbox.remove_free_symbols(el.temp_props.grad_temp, None))
            temp_coeff = symb2float(symbbox.remove_free_symbols(el.temp_props.temp_coeff, None))
            vis_el.add_nodedep(curr_doc, ElSupEnum.ElSupEnum.LOAD_TEMP.value, x_middle, y_middle, length=length, angle=angle,
                               dt_t=(grad_temp, start_temp, temp_coeff))
    elif ElSupEnum.check_line_spring(el_type):
        add_knots_to_visu(curr_doc, knot1, knot2)
        vis_el.add_nodedep(curr_doc, el_type, x_middle, y_middle, length=length, angle=angle, k=symb2float(el.k_spring_),
                           ei=symb2float(el.ei_), ea=symb2float(el.ea_))

    return


def add_nodedep_single_knot(curr_doc: CurrentDoc, el):
    """
    Adds all point forces and point springs to the visualisation plot
    :param el: needs a knot as input
    """
    if not (el.has_pointload() or el.is_spring()):
        return
    knot1 = get_knot_name_from_nodeindep_list(curr_doc.data_sources.ds_indep_elements, el.x_, el.y_)
    # print("knot1: " + str(knot1))
    if el.has_pointload():
        n = q = 0
        if el.pointLoad_[0] != 0:
            q = float(symbbox.remove_free_symbols(el.pointLoad_[0], None))
        if el.pointLoad_[1] != 0:
            n = float(symbbox.remove_free_symbols(el.pointLoad_[1], None))
        if n != 0 or q != 0:
            angle = float(math.atan2(q, n))
            f = math.sqrt(n**2 + q**2)
            add_knots_to_visu(curr_doc, knot1, None)
            vis_el.add_nodedep(curr_doc, ElSupEnum.ElSupEnum.LOAD_POINT.value, el.x_, el.y_, angle=angle, f=f)
        if el.pointLoad_[2] != 0:
            mom = float(symbbox.remove_free_symbols(el.pointLoad_[2], None))
            add_knots_to_visu(curr_doc, knot1, None)
            vis_el.add_nodedep(curr_doc, ElSupEnum.ElSupEnum.LOAD_MOMENT.value, el.x_, el.y_, moment=mom)
    if el.is_spring():
        k_x = k_y = 0
        angle = el.angle * math.pi/180
        if el.k[0] != 0:
            k_x = float(symbbox.remove_free_symbols(el.k[0], None))
        if el.k[1] != 0:
            k_y = float(symbbox.remove_free_symbols(el.k[1], None))
        if k_x != 0 or k_y != 0:
            angle = float(math.atan2(k_x, k_y))
            k = math.sqrt(k_x ** 2 + k_y ** 2)
            add_knots_to_visu(curr_doc, knot1, None)
            vis_el.add_nodedep(curr_doc, ElSupEnum.ElSupEnum.SPRING_SUPPORT.value, el.x_, el.y_, angle=angle, k=k)
        if el.k[2] != 0:
            k_mom = float(symbbox.remove_free_symbols(el.k[2], None))
            add_knots_to_visu(curr_doc, knot1, None)
            vis_el.add_nodedep(curr_doc, ElSupEnum.ElSupEnum.SPRING_MOMENT_SUPPORT.value, el.x_, el.y_, angle=angle, k=k_mom)


def vis_nodeindep_elements(curr_doc: CurrentDoc, el_list):
    """
    Takes a list of nodes as input and can visualize them in the input plot
    :param el_list: [knot1, knot2, ... knot_n]
    """
    i = 0
    for el in el_list:
        el_to_plot = convert_node_indep_type(el)
        name = "name_str_" + str(i)
        el_type = el_to_plot.type
        if el_type == ElSupEnum.ElSupEnum.SUPPORT_FIXED_END.value:
            el_type = ElSupEnum.ElSupEnum.SUPPORT_FIXED_CONTINUOUS.value
        elif el_type == ElSupEnum.ElSupEnum.SUPPORT_ROLLER_END.value:
            el_type = ElSupEnum.ElSupEnum.SUPPORT_ROLLER_CONTINUOUS.value
        # name = str(el_type) + '-' + str(i)
        add_nodeindep_single_el(curr_doc, el_to_plot.x_, el_to_plot.y_, el_type, name, el.angle * math.pi/180)
        add_nodedep_single_knot(curr_doc, el_to_plot)
        i += 1


def vis_nodedep_elements(curr_doc: CurrentDoc, nodedep_list):
    """
    Takes a list of nodedependent elements as input and visualizes them in the input plot
    """
    # TODO Correct force management
    i = 0
    for el in nodedep_list:
        if isinstance(el, ElementCalculation):
            if el.k_spring_ != 0:
                el_type = ElSupEnum.ElSupEnum.SPRING.value
            else:
                # Is beam or rod
                el_type = ElSupEnum.ElSupEnum.BEAM.value
            add_nodedep_two_knots(curr_doc, el, el_type)


def convert_node_indep_type(node):
    """
    Converts the knot type from calc types to vis types
    :param node: node to check
    :return: changed knot
    """
    knot = node
    if knot.type == ElSupEnum.ElSupEnum.SUPPORT_FIXED_END.value:
        knot.type = ElSupEnum.ElSupEnum.SUPPORT_FIXED_JOINT.value
    if knot.type == ElSupEnum.ElSupEnum.SUPPORT_ROLLER_END.value:
        knot.type = ElSupEnum.ElSupEnum.SUPPORT_ROLLER_JOINT.value
    if knot.type == ElSupEnum.ElSupEnum.FREE_END.value:
        knot.type = ElSupEnum.ElSupEnum.NODE.value
    if knot.type == ElSupEnum.ElSupEnum.THROUGH_ELEMENT.value:
        knot.type = ElSupEnum.ElSupEnum.NODE.value
    return knot
