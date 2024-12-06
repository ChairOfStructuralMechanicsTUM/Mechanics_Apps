from sympy import Symbol, Eq, sin, cos
import math

from Libs import geometriccalc as gc
from Classes import Knot, TempProps
from Classes.ElementSupportEnum import ElSupEnum
from Element_Calculation import ElementCalculation
from testing_collection import testingtoolbox as testbox
from Classes.CurrentDocument import CurrentDoc


"""
HOW TO: ADD NEW TEST CASE TO DROPDOWN MENU
1.) Create new structure, that needs to be visualised in this script
2.) Go to file: vis_initialization.py and add new test case to the variable menu_tc in the following style:
    Needs sets, for every test case: ("name shown by the dropdown menu", "internal_handled_name")
3.) Go to file: vis_callbacks.py, function: cb_plot_testcase(attr, old, new, curr_doc: CurrentDoc)
    add new testcase to by creating a new if statement, that tests for the internal_handled_name
"""


def single_beam_lineload_visu(curr_doc: CurrentDoc):
    start_knot = Knot.Knot(0, 1, 1, ElSupEnum.SUPPORT_FIXED_END.value, 0, [0, 0, 0], [0, 0, 0])
    end_knot = Knot.Knot(1, 3, 1, ElSupEnum.SUPPORT_ROLLER_END.value,  0, [0, 0, 0], [0, 0, 0])
    q = Symbol('p')
    l = gc.knot_dist(start_knot, end_knot) * Symbol('l')
    lineload = [0, q]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = [[start_knot, end_knot]]
    elementlist = []
    ele = ElementCalculation(0, start_knot, end_knot, l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    start_knot.add_coupled_el(0)
    end_knot.add_coupled_el(0)
    elementlist.append(ele)
    testbox.vis_structure_from_input(curr_doc, knot_list, elementlist)


def two_beam_lineload_visu(curr_doc: CurrentDoc):
    start_knot = Knot.Knot(0, 1, 1, ElSupEnum.SUPPORT_ROLLER_END.value, 0)
    middle_knot = Knot.Knot(1, 2, 1, ElSupEnum.SUPPORT_FIXED_CONTINUOUS.value, 0)
    end_knot = Knot.Knot(2, 3, 1, ElSupEnum.SUPPORT_ROLLER_END.value, 0)
    q = Symbol('p')
    l = Symbol('l')
    lineload = [0, q]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = []
    elementlist = []
    ele = ElementCalculation(0, start_knot, middle_knot, l, lineload, temp_prop, Symbol('EI'), Symbol('EA'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([start_knot, middle_knot])
    ele = ElementCalculation(1, middle_knot, end_knot, l, lineload, temp_prop, Symbol('EI'), Symbol('EA'), Symbol('h'))
    elementlist.append(ele)
    start_knot.add_coupled_el(0)
    middle_knot.add_coupled_el([0, 1])
    end_knot.add_coupled_el(1)
    knot_list.append([middle_knot, end_knot])
    testbox.vis_structure_from_input(curr_doc, knot_list, elementlist)


def final_structure_software_lab(curr_doc: CurrentDoc):
    f = Symbol('F')
    k = Symbol('k')
    start_knot = Knot.Knot(0, 1, 3, ElSupEnum.SUPPORT_CLAMPED.value, 0)
    middle_knot = Knot.Knot(1, 2, 3, ElSupEnum.JOINT.value, 0, [0, 0, 0], [0, f, 0])
    end_knot = Knot.Knot(2, 3, 2, ElSupEnum.SUPPORT_ROLLER_END.value, 0, [0, 0, k])
    q = Symbol('q')
    l = Symbol('l')
    h = Symbol('h')
    x = Symbol('x')
    at = Symbol('at')
    ei = Symbol('EI')
    line_load_0 = [0, q * x]
    temp_load_0 = TempProps.TempProps(0, 0, 0)
    knot_list = []
    elementlist = []

    # ELEMENT 0
    l0 = gc.knot_dist(start_knot, middle_knot) * l
    ele0 = ElementCalculation(0, start_knot, middle_knot, l0, line_load_0, temp_load_0, ei=ei, ea=float('inf'), h=h)
    elementlist.append(ele0)
    knot_list.append([start_knot, middle_knot])

    # ELEMENT 1
    line_load_1 = [0, 0]
    temp_load_1 = TempProps.TempProps(0, Symbol('dT'), at)
    l1 = gc.knot_dist(middle_knot, end_knot) * l
    ele1 = ElementCalculation(1, middle_knot, end_knot, l1, line_load_1, temp_load_1, ei=ei, ea=float('inf'), h=h)
    elementlist.append(ele1)
    knot_list.append([middle_knot, end_knot])

    # VIS STRUCTURE
    testbox.vis_structure_from_input(curr_doc, knot_list, elementlist)


def example_unterlagen_visu(curr_doc: CurrentDoc):
    q = Symbol('q')
    l = Symbol('l')
    start_knot = Knot.Knot(0, 0.5, 2, ElSupEnum.SUPPORT_ROLLER_END.value, 0, [0, 0, 0], [0, 0, 0])
    middle_knot1 = Knot.Knot(1, 2.5, 2, ElSupEnum.JOINT.value, 0, [0, 0, 0], [0, 0, 0])
    middle_knot2 = Knot.Knot(2, 2.5, 1, ElSupEnum.THROUGH_ELEMENT.value, 0, [0, 0, 0], [0, 0, - 2 * q * l**2])
    end_knot = Knot.Knot(3, 4.5, 1, ElSupEnum.SUPPORT_CLAMPED.value, 0)
    lineload = [0, q]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = []
    elementlist = []
    l0 = gc.knot_dist(start_knot, middle_knot1)
    l1 = gc.knot_dist(middle_knot1, middle_knot2)
    l2 = gc.knot_dist(middle_knot2, end_knot)
    ele = ElementCalculation(0, start_knot, middle_knot1, l0 * l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([start_knot, middle_knot1])
    ele = ElementCalculation(1, middle_knot1, middle_knot2, l1 * l, [0, 0], temp_prop, float('inf'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([middle_knot1, middle_knot2])
    ele = ElementCalculation(2, middle_knot2, end_knot, l2 * l, [0, 0], temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([middle_knot2, end_knot])
    start_knot.add_coupled_el(0)
    middle_knot1.add_coupled_el([0, 1])
    middle_knot2.add_coupled_el([1, 2])
    end_knot.add_coupled_el(2)

    # VIS STRUCTURE
    testbox.vis_structure_from_input(curr_doc, knot_list, elementlist)


def vis_all_possible_nodedep_ele(curr_doc: CurrentDoc):
    # Visualises: beam, lineload, spring, spring_support, spring_moment, temp_prop
    f = Symbol('f')
    start_knot = Knot.Knot(0, 1.2, 1.7, ElSupEnum.SUPPORT_FIXED_END.value, k=[0, 0, 0], pointload=[0, 0, 0], angleSupport=-30)
    middle_knot = Knot.Knot(1, 2, 1, ElSupEnum.THROUGH_ELEMENT.value, k=[0, 0, 0], pointload=[0, 2*f, f])
    end_knot = Knot.Knot(2, 3, 1, ElSupEnum.SUPPORT_ROLLER_END.value, k=[0, 0, 0], pointload=[0, 0, 0], angleSupport=0)
    q = Symbol('q')
    n = Symbol('n')
    l = Symbol('l')
    l1 = gc.knot_dist(start_knot, middle_knot) * l
    l2 = gc.knot_dist(middle_knot, end_knot) * l
    k = Symbol('k')
    ei = Symbol('EI')
    ea = Symbol('EA')
    h = Symbol('h')
    lineload = [0.5 * n * l, q]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = []
    elementlist = []
    # BEAM
    ele = ElementCalculation(0, start_knot, middle_knot, l1, lineload, temp_prop, ei=ei, ea=ea, h=h)
    elementlist.append(ele)
    knot_list.append([start_knot, middle_knot])

    # SPRING
    ele = ElementCalculation(1, middle_knot, end_knot, l2, [0, 0, 0], temp_prop, ei=ei, ea=ea, h=h, k_spring=k)
    elementlist.append(ele)
    knot_list.append([middle_knot, end_knot])

    # SPRING SUPPORT
    spring_sup = Knot.Knot(4, 2, 2, ElSupEnum.FREE_END.value, k=[2*k, 0, 0], pointload=[0, 0, 0], angleSupport=-90)
    spring_mom = Knot.Knot(5, 4, 2, ElSupEnum.FREE_END.value, k=[0, 0, 3*k], pointload=[0, 0, 0], angleSupport=0)
    temp_prop = TempProps.TempProps(10, 0, 0)
    ele = ElementCalculation(2, spring_sup, spring_mom, l1, [0, 0, 0], temp_prop, ei=ei, ea=ea, h=h)
    elementlist.append(ele)
    knot_list.append([spring_sup, spring_mom])
    testbox.vis_structure_from_input(curr_doc, knot_list, elementlist)

