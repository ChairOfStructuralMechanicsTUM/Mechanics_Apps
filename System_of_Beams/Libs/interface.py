import math as m
from sympy import Symbol, N

import vis_initialization as vis_init
from Element_Calculation import ElementCalculation
from Element_Initialising import CalculationElement
from Classes.Knot import Knot
from Classes.TempProps import TempProps
from Classes import ElementSupportEnum as ElSupEnum
from Libs import outputvisualization as outvis
from Libs import symbolictoolbox as symbbox
from Libs import print_function_helpers as prhlp
from Libs import geometriccalc as gc


def get_indices(variable, x):  # x = list
    """
    Finds all indices of a given value in a list
    :param variable: value to search in the list
    :param x: the list to search in
    :return: list of indices
    """
    get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y]
    return get_indexes(variable, x)


def get_related_knots_for_elements(element, indice, node_list):
    """
    extracts the knots from a given element
    :param element: the related element the knots need to be searched in
    :param indice: indice of this element in the data source
    :param node_list: list of all existing nodes
    :return: knot_1, knot_2
    """
    knot_1 = next((knot for knot in node_list if knot.id == element.data["name_node1"][indice]), None)
    knot_2 = next((knot for knot in node_list if knot.id == element.data["name_node2"][indice]), None)
    return knot_1, knot_2


def get_all_node_from_indep(ds_indep):
    """
    Extracts all nodes from a ColumnDataSource.
    Extracts only the raw data, some information (e.g. spring/ point forces) need to be added later
    :param ds_indep:
    :return:
    """
    node_list = []
    for i in range(len(ds_indep.data["type"])):
        _, el_type, num = ElSupEnum.value_in_enum(ElSupEnum.ElSupEnum, ds_indep.data["type"][i])
        # print("Knot" + str(i) + ": " + str(ds_indep.data["name"][i]) + " type: " + str(el_type))
        kn = Knot(ds_indep.data["name"][i], ds_indep.data["x"][i], ds_indep.data["y"][i], ds_indep.data["type"][i], ds_indep.data["angle"][i])
        node_list.append(kn)
        # print("Successful created: ")
        # print(kn)

    return node_list


def extract_beams_and_rods(ds_nodedep, indice, node_list, beam_id):
    line_load_init = [0, 0]
    temp_load_init = TempProps(0, 0, 0)
    knot_1, knot_2 = get_related_knots_for_elements(ds_nodedep, indice, node_list)
    h = symbbox.get_func_from_string(str(ds_nodedep.data["h"][indice]) + "*h")
    ea = ds_nodedep.data["ea"][indice]
    if str(ea) == "inf":
        ea = float('inf')
    else:
        ea = ea * Symbol("EA")
    ei = ds_nodedep.data["ei"][indice]
    if ei == float("inf"):
        ei = float('inf')
    else:
        ei = ei * Symbol("EI")
    len_symb = symbbox.get_func_from_string(str(ds_nodedep.data["length"][indice]) + "*l")
    ele = ElementCalculation(beam_id, knot_1, knot_2, len_symb, line_load_init, temp_load_init, ei=ei, ea=ea, h=h)
    knot_1.add_coupled_el(beam_id)
    knot_2.add_coupled_el(beam_id)
    return ele


def extract_line_spring(ds_nodedep, indice, node_list, beam_id):
    # print("Get spring")
    line_load_init = [0, 0]
    temp_load_init = TempProps(0, 0, 0)
    knot_1, knot_2 = get_related_knots_for_elements(ds_nodedep, indice, node_list)
    k = symbbox.get_func_from_string(str(ds_nodedep.data["k"][indice]) + "k")
    # h = symbbox.get_func_from_string(str(ds_nodedep.data["h"][indice]) + "*h")
    len_symb = symbbox.get_func_from_string(str(ds_nodedep.data["length"][indice]) + "*l")
    ele = ElementCalculation(beam_id, knot_1, knot_2, len_symb, line_load_init, temp_load_init, k_spring=k)
    knot_1.add_coupled_el(beam_id)
    knot_2.add_coupled_el(beam_id)
    return ele


def extract_point_spring(ds_nodedep, indice, node_list):
    """
    Extracts a point spring. k is defined in negative y-direction
    """
    knot_1, _ = get_related_knots_for_elements(ds_nodedep, indice, node_list)
    k_x = k_y = k_mom = 0
    k = float(ds_nodedep.data["k"][indice]) * Symbol("k")
    angle = float(ds_nodedep.data["angle"][indice]) * m.pi / 180  # convert from degree to radian
    if ds_nodedep.data["type"][indice] == ElSupEnum.ElSupEnum.SPRING_SUPPORT.value:
        k_x = symbbox.round_expr(k * -m.sin(angle), 5)
        k_y = symbbox.round_expr(k * m.cos(angle), 5)
    else:
        k_mom = float(ds_nodedep.data["k"][indice]) * Symbol("k")
    knot_1.add_spring_stiffness(k_x, k_y, k_mom)
    return k_x, k_y, k_mom


def extract_point_load(ds_nodedep, indice, node_list):
    """
    Extracts the pointload. F is defined in negative y-direction
    """
    knot_1, _ = get_related_knots_for_elements(ds_nodedep, indice, node_list)
    F = float(ds_nodedep.data["f"][indice]) * Symbol("F")
    mom = float(ds_nodedep.data["moment"][indice]) * Symbol("M")
    angle = float(ds_nodedep.data["angle"][indice])
    F_x = symbbox.round_expr(F * m.sin(angle), 5)
    F_y = symbbox.round_expr(F * m.cos(angle), 5)
    knot_1.set_pointload(F_x, F_y, mom)
    return F_x, F_y, mom


def extract_user_defined_load(ds_nodedep, indice, node_list):
    knot_1, knot_2 = get_related_knots_for_elements(ds_nodedep, indice, node_list)
    # TODO q_inp_str, n_inp_str, len_str needs to be set to correct user input
    q_inp_str = "2*q*x^2"
    n_inp_str = "1/2+n*x"
    len_str = "x"
    x_symb = Symbol('x')

    q_inp_str = symbbox.validate_input_string(q_inp_str)
    n_inp_str = symbbox.validate_input_string(n_inp_str)
    len_str = symbbox.validate_input_string(len_str)
    q = symbbox.get_func_from_string(q_inp_str)
    n = symbbox.get_func_from_string(n_inp_str)
    len_symb = symbbox.get_func_from_string(len_str)
    if len_symb != x_symb:
        q.subs(len_symb, x_symb)
        n.subs(len_symb, x_symb)
    return [n, q]


def extract_line_load(ds_nodedep, indice, node_list):
    knot_1, knot_2 = get_related_knots_for_elements(ds_nodedep, indice, node_list)
    ll_local = ds_nodedep.data["ll_local"][indice]
    ll_x_n = ds_nodedep.data["ll_x_n"][indice]
    ll_y_q = ds_nodedep.data["ll_y_q"][indice]
    angle = ds_nodedep.data["angle"][indice]

    len_symb = Symbol('x')
    x_2 = gc.knot_dist(knot_1, knot_2)
    n, q = calc_line_load(ll_local, ll_x_n, ll_y_q, 0, x_2, len_symb, angle)
    return [n, q]


def extract_temp_loads(ds_nodedep, indice, node_list):
    dT_T = ds_nodedep.data["dT_T"][indice]
    T  = Symbol("T")
    dT = Symbol("dT")
    aT = Symbol("aT")
    return TempProps(dT_T[1] * T, dT_T[0] * dT, dT_T[2] * aT)


def calc_line_load(ll_local, ll_x_n, ll_y_q, x_1, x_2, len_symb, angle_glob=0, round_prec=6):
    """
    User linear interpolation to create linear symbolic functions for the normal & shear forces
    :param ll_local: Boolean, if the function adds local or global
    :param ll_x_n: set of the normal force (start_n, end_n)
    :param ll_y_q: set of the shear force (start_q, end_q)
    :param len_symb: Symbol, the function shell run over
    :param angle_glob: angle of the global element, necessary if ll_local == True
    :param round_prec:
    :return: symbolic function of n, q
    """
    n = Symbol('n')
    q = Symbol('q')
    l = Symbol('l')
    n_func = N((ll_x_n[1] - ll_x_n[0]) / ( l * (x_2 - x_1)) * len_symb + ll_x_n[0] - (ll_x_n[1] - ll_x_n[0]) / ( l * (x_2 - x_1)) * x_1)
    q_func = N((ll_y_q[1] - ll_y_q[0]) / ( l * (x_2 - x_1)) * len_symb + ll_y_q[0] - (ll_y_q[1] - ll_y_q[0]) / ( l * (x_2 - x_1)) * x_1)
    if not ll_local:
        print("line_load transferred to local coordinate system")
        n_func_loc =   N(n_func * m.cos(angle_glob) + q_func * m.sin(angle_glob))
        q_func_loc = - N(n_func * m.sin(angle_glob) + q_func * m.cos(angle_glob))
    else:
        n_func_loc = n_func
        q_func_loc = q_func
    n_func_loc = n_func_loc * n
    q_func_loc = q_func_loc * q
    print(n_func)
    return symbbox.round_expr(n_func_loc, round_prec), symbbox.round_expr(-q_func_loc, round_prec)


def adjust_nodes_for_calc(node_list):
    """
    Changes the id of the nodes to get a consistent numbering from 0 to n
    Some node types look the same in the visualisation but are handeled differently in the calculation
    To satisfy this, the types are adapted here
    :return:
    """
    i = 0
    for node in node_list:
        node.id = i
        i += 1
        if node.type == ElSupEnum.ElSupEnum.SUPPORT_FIXED_JOINT.value and len(node.coupled_el) <= 1:
            node.type = ElSupEnum.ElSupEnum.SUPPORT_FIXED_END.value
            # print("Fixed changed to end element")
        elif node.type == ElSupEnum.ElSupEnum.SUPPORT_FIXED_CONTINUOUS.value and len(node.coupled_el) <= 1:
            node.type = ElSupEnum.ElSupEnum.SUPPORT_FIXED_END.value
            # print("Fixed continuous changed to end element")
        elif node.type == ElSupEnum.ElSupEnum.SUPPORT_ROLLER_JOINT.value and len(node.coupled_el) <= 1:
            node.type = ElSupEnum.ElSupEnum.SUPPORT_ROLLER_END.value
            # print("Roller changed to end load_type")
        elif node.type == ElSupEnum.ElSupEnum.SUPPORT_ROLLER_CONTINUOUS.value and len(node.coupled_el) <= 1:
            node.type = ElSupEnum.ElSupEnum.SUPPORT_ROLLER_END.value
            # print("Roller continuous changed to end load_type")
        elif node.type == ElSupEnum.ElSupEnum.NODE.value:
            if len(node.coupled_el) <= 1:
                node.type = ElSupEnum.ElSupEnum.FREE_END.value
                # print("Changed node to end node")
            else:
                node.type = ElSupEnum.ElSupEnum.THROUGH_ELEMENT.value
                # print("Changed node to middle node")


def add_loads_to_elements(curr_doc, beam_dict, load_dict, load_type="lineload"):
    """
    Adds distributed loads to a element. Can handle lineloads or temploads
    The loads and beams can be put together based on the same key in the dictionaries.
    The key is created out of a combination of the start/ end knot
    :param beam_dict: dict of all existing beams
    :param load_dict: dict of all loads that need to be added
    :param load_type: which types do the loads from the dict have. One type for complete dict
    """
    for key, load in load_dict.items():
        try:
            el_to_add = beam_dict[key]
            if load_type.lower() == "lineload":
                el_to_add.set_lineload(load)
                # print("line load succesfully added")
            elif load_type.lower() == "tempload":
                el_to_add.set_temp_props(load)
                # print("temp load succesfully added")
        except:
            vis_init.expand_msg2user(curr_doc, "WARNING: No beam element was found!", bg_color="orange")


def interface(curr_doc, ds_indep, ds_nodedep):
    """
    Gets the input from the graph and sorts this input into several list due to the properties
    Calls the ElementCalculation class with the correct input
    Calls the plot functions to visualise the calculated results
    :param ds_indep: all elements which can exist independently in the plot (supports, connectors)
    :param ds_nodedep: all elements, which are related to the independent elements (elements, loads, springs)
    :return:
    """
    print('Start calc interface')
    vis_init.expand_msg2user(curr_doc, "Start data conversion")

    # get all knots
    node_list = get_all_node_from_indep(ds_indep)
    '''
    Noetige Unterscheidungen:
    DONE SUPPORT_FIXED_END vs. SUPPORT_FIXED_JOINT: Kein weiteres Element, len(coupled_el) <= 1
    DONE SUPPORT_ROLLER_END vs. SUPPORT_ROLLER_JOINT: Alle in SUPPORT_ROLLER_JOINT angelegt, dann anpassen
    DONE Node in FREE_END or THROUGH_ELEMENT: Unterscheidung siehe oben
    DONE Rod, vs. Beam: ROD (EA unendlich), BEAM (EI unendlich) (wird ueber Nutzereingabe gelöst)
    DONE Federn muessen in Konstante k eingespeichert werden. Federkonstante muss relativ zum Auflagerwinkel angegeben werden
    DONE Spring anlegen
    '''

    # print("Node list: " + str(node_list))
    element_list = []
    load_line_dict = {}
    load_temp_dict = {}
    beam_id = 0
    beam_dict = dict()
    # print("len Node dependent" + str(len(ds_nodedep.data["type"])))
    for i in range(len(ds_nodedep.data["type"])):
        # print("i: " + str(i))
        el_type = ds_nodedep.data["type"][i]
        # print(ds_nodedep.data["type"][i])
        # get beams and rods
        if ElSupEnum.check_beams_and_rods(el_type):
            ele = extract_beams_and_rods(ds_nodedep, i, node_list, beam_id)
            element_list.append(ele)
            beam_dict.update({prhlp.get_id_from_knots(ele.start_knot, ele.end_knot): ele})
            # print("Beam created: " + str(prhlp.get_id_from_knots(ele.start_knot, ele.end_knot)))
            # print(element_list[-1])
            beam_id += 1

        # get springs in structure
        elif ElSupEnum.check_line_spring(el_type):
            ele = extract_line_spring(ds_nodedep, i, node_list, beam_id)
            element_list.append(ele)
            beam_dict.update({prhlp.get_id_from_knots(ele.start_knot, ele.end_knot): ele})
            # print("Spring created: " + str(prhlp.get_id_from_knots(ele.start_knot, ele.end_knot)))
            # print(element_list[-1])
            beam_id += 1

        # get line loads
        elif ElSupEnum.check_line_load(el_type):
            # print("Line load found")
            load = extract_line_load(ds_nodedep, i, node_list)
            knot_1, knot_2 = get_related_knots_for_elements(ds_nodedep, i, node_list)
            load_line_dict.update({prhlp.get_id_from_knots(knot_1, knot_2): load})
            # print("Lineload successfully created: " + str(prhlp.get_id_from_knots(knot_1, knot_2)))

        # get point springs
        elif ElSupEnum.check_point_spring(el_type):
            # print("Point spring found")
            k_x, k_y, k_mom = extract_point_spring(ds_nodedep, i, node_list)
            # print("Point spring successfully added [{}, {}, {}]".format(str(k_x), str(k_y), str(k_mom)))

        # get point loads and add them to element
        elif ElSupEnum.check_point_load(el_type):
            # print("Pointload found")
            f_x, f_y, mom = extract_point_load(ds_nodedep, i, node_list)
            # print("Point load successfully added [{}, {}, {}]".format(str(f_x), str(f_y), str(mom)))

        # get Temperatur loads
        elif ElSupEnum.check_temp_load(el_type):
            load = extract_temp_loads(ds_nodedep, i, node_list)
            knot_1, knot_2 = get_related_knots_for_elements(ds_nodedep, i, node_list)
            load_temp_dict.update({prhlp.get_id_from_knots(knot_1, knot_2): load})
            # print("TempLoad successfully created: " + str(prhlp.get_id_from_knots(knot_1, knot_2)))
            # print(load)

        elif ElSupEnum.check_user_defined_load(el_type):
            load = extract_user_defined_load(ds_nodedep, i, node_list)
            knot_1, knot_2 = get_related_knots_for_elements(ds_nodedep, i, node_list)
            load_temp_dict.update({prhlp.get_id_from_knots(knot_1, knot_2): load})
            # print("User defined load successfully created: " + str(prhlp.get_id_from_knots(knot_1, knot_2)))
            # print(load)

    # Add loads to the Beams and rods
    add_loads_to_elements(curr_doc, beam_dict, load_line_dict, load_type="lineload")
    add_loads_to_elements(curr_doc, beam_dict, load_temp_dict, load_type="tempload")

    # Refactor knot ids and change supports to calc supports
    adjust_nodes_for_calc(node_list)

    node_list_to_plot = []
    vis_init.expand_msg2user(curr_doc, "Data conversion successful")
    for el in element_list:
        el.start_calculation()
        node_list_to_plot.append([el.start_knot, el.end_knot])
    for el in element_list:
        el.set_start_end_knot_correctly()
        el.start_calculation()
    prhlp.print_knot_and_element_list(prhlp.list_with_every_knot_only_once(node_list), element_list)
    func_list, val, l_list = CalculationElement(curr_doc, element_list)
    vis_init.expand_msg2user(curr_doc, "Start visualisation of results")
    outvis.plot_output_functions(curr_doc, func_list, node_list_to_plot, val, l_list)
    vis_init.expand_msg2user(curr_doc, "Visualisation successful")

