from sympy import Symbol, Eq, sin, cos
import math
from numpy import array, append

from Libs import geometriccalc as gc
from Classes import Knot, TempProps
from Classes.ElementSupportEnum import ElSupEnum
from Element_Initialising import CalculationElement
from Element_Calculation import ElementCalculation
from testing_collection import testingtoolbox as testbox


def single_beam_lineload_test():
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_FIXED_END.value, [0, 0, 0], [0, 0, 0], 0)
    end_knot = Knot.Knot(1, 1, 0, ElSupEnum.SUPPORT_ROLLER_END.value, [0, 0, 0], [0, 0, 0], 0)
    q = Symbol('p')
    l = Symbol('l')
    lineload = [0, q]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = [[start_knot, end_knot]]
    elementlist = []
    ele = ElementCalculation(0, start_knot, end_knot, l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    start_knot.add_coupled_el(0)
    end_knot.add_coupled_el(0)
    elementlist.append(ele)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)
    testbox.vis_structure_from_input(knot_list, elementlist)

# def single_beam_lineload_test_infinity():
#     tim = []
#     for count in range(3, 50):
#         knots = array([])
#         knot_list = []
#         lo_nr = count
#         Kn = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_FIXED_END.value, [0, 0, 0], [0, 0, 0], 0)
#         knots = append(knots, Kn)
#         for i in range(1, lo_nr-1):
#             Kn = Knot.Knot(i, i, 0, ElSupEnum.SUPPORT_ROLLER_JOINT.value)
#             knots = append(knots, Kn)
#         end_knot = Knot.Knot(lo_nr-1, lo_nr-1, 0, ElSupEnum.SUPPORT_ROLLER_END.value, [0, 0, 0], [0, 0, 0], 0)
#         knots = append(knots, end_knot)
#         q = Symbol('p')
#         l = Symbol('l')
#         lineload = [0, q]
#         temp_prop = TempProps.TempProps(0, 0, 0)
#         elementlist = array([])
#         knots[0].add_coupled_el(0)
#         for j in range(1, lo_nr - 1):
#             knots[j].add_coupled_el([j - 1, j])
#         knots[lo_nr-1].add_coupled_el(lo_nr - 2)
#         for j in range(0, lo_nr-1):
#             ele = ElementCalculation(j, knots[j], knots[j+1], l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
#             knot_list.append([knots[j], knots[j+1]])
#             elementlist = append(elementlist, ele)
#
#         functions, x, l_list, elapsed_time = CalculationElement(elementlist)
#         print(elapsed_time)
#         tim.append(elapsed_time)
    # print(tim)


def single_beam_normal_lineload_test():
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_FIXED_END.value, [0, 0, 0], [0, 0, 0], 0)
    end_knot = Knot.Knot(1, 1, 0, ElSupEnum.SUPPORT_ROLLER_END.value, [0, 0, 0], [0, 0, 0], 0)
    q = Symbol('n')
    l = Symbol('l')
    x = Symbol('x')
    lineload = [- q * x, 0]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = [[start_knot, end_knot]]
    elementlist = []
    ele = ElementCalculation(0, start_knot, end_knot, l, lineload, temp_prop, Symbol('EI'), Symbol('EA'), Symbol('h'))
    start_knot.add_coupled_el(0)
    end_knot.add_coupled_el(0)
    elementlist.append(ele)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def single_beam_lineload_vertical_test():
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_FIXED_END.value)
    end_knot = Knot.Knot(1, 0, 1, ElSupEnum.SUPPORT_ROLLER_END.value, [0, 0, 0], [0, 0, 0], 90)
    q = Symbol('p')
    l = Symbol('l')
    lineload = [0, q]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = [[start_knot, end_knot]]
    elementlist = []
    ele = ElementCalculation(0, start_knot, end_knot, l, lineload, temp_prop)
    start_knot.add_coupled_el(0)
    end_knot.add_coupled_el(0)
    elementlist.append(ele)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)
    testbox.vis_structure_from_input(knot_list, elementlist)


def single_beam_single_load_vertical_test():
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_FIXED_END.value, [0, 0, 0], [0, 0, 0], 90)
    end_knot = Knot.Knot(1, 0, 1, ElSupEnum.SUPPORT_ROLLER_END.value, [0, 0, 0], [0, Symbol('F'), 0], 90)        # in globalen Koordinaten
    q = Symbol('p')
    l = Symbol('l')
    lineload = [0, 0]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = [[start_knot, end_knot]]
    elementlist = []
    ele = ElementCalculation(0, start_knot, end_knot, l, lineload, temp_prop)
    start_knot.add_coupled_el(0)
    end_knot.add_coupled_el(0)
    elementlist.append(ele)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def single_beam_trapezload_test():
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_FIXED_END.value)
    end_knot = Knot.Knot(1, 1, 0, ElSupEnum.SUPPORT_ROLLER_END.value)
    q = Symbol('p')
    x = Symbol('x')
    l = Symbol('l')
    lineload = [0, q * x]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = [[start_knot, end_knot]]
    elementlist = []
    ele = ElementCalculation(0, start_knot, end_knot, l, lineload, temp_prop)
    start_knot.add_coupled_el(0)
    end_knot.add_coupled_el(0)
    elementlist.append(ele)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def single_beam_temperature_test():
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_FIXED_END.value)
    end_knot = Knot.Knot(1, 1, 0, ElSupEnum.SUPPORT_FIXED_END.value)
    q = Symbol('p')
    l = Symbol('l')
    lineload = [0, 0]
    temp_prop = TempProps.TempProps(Symbol('dT'), 0, Symbol('aT'))
    knot_list = [[start_knot, end_knot]]
    elementlist = []
    ele = ElementCalculation(0, start_knot, end_knot, l, lineload, temp_prop)
    start_knot.add_coupled_el(0)
    end_knot.add_coupled_el(0)
    elementlist.append(ele)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def single_clamping_left_side_temperature():
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_CLAMPED.value)
    end_knot = Knot.Knot(1, 1, 0, ElSupEnum.FREE_END.value)
    q = Symbol('p')
    l = Symbol('l')
    lineload = [0, 0]
    temp_prop = TempProps.TempProps(Symbol('Tstart'), Symbol('To_Tu'), Symbol('aT'))
    knot_list = [[start_knot, end_knot]]
    elementlist = []
    ele = ElementCalculation(0, start_knot, end_knot, l, lineload, temp_prop, Symbol('EI'), Symbol('EA'), Symbol('h'))
    start_knot.add_coupled_el(0)
    end_knot.add_coupled_el(0)
    elementlist.append(ele)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def single_beam_lineload_test_overdefined():
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_FIXED_END.value)
    end_knot = Knot.Knot(1, 1, 0, ElSupEnum.SUPPORT_FIXED_END.value)
    q = Symbol('p')
    l = Symbol('l')
    lineload = [0, q]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = [[start_knot, end_knot]]
    elementlist = []
    ele = ElementCalculation(0, start_knot, end_knot, l, lineload, temp_prop)
    start_knot.add_coupled_el(0)
    end_knot.add_coupled_el(0)
    elementlist.append(ele)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def single_beam_lineload_test_underdefined():
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_ROLLER_END.value)
    end_knot = Knot.Knot(1, 1, 0, ElSupEnum.SUPPORT_ROLLER_END.value, [0, 0, 0], [0, 0, 0])
    q = Symbol('p')
    l = Symbol('l')
    lineload = [0, q]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = [[start_knot, end_knot]]
    elementlist = []
    ele = ElementCalculation(0, start_knot, end_knot, l, lineload, temp_prop)
    start_knot.add_coupled_el(0)
    end_knot.add_coupled_el(0)
    elementlist.append(ele)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def two_beam_lineload_test():
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_ROLLER_END.value)
    middle_knot = Knot.Knot(1, 1, 0, ElSupEnum.SUPPORT_FIXED_CONTINUOUS.value)
    end_knot = Knot.Knot(2, 2, 0, ElSupEnum.SUPPORT_ROLLER_END.value)
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
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)
    testbox.vis_structure_from_input(knot_list, elementlist)


def two_beam_combined_to_one_complete_lineload_test():
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_FIXED_END.value)
    middle_knot = Knot.Knot(1, 0.5, 0, ElSupEnum.THROUGH_ELEMENT.value)
    end_knot = Knot.Knot(2, 1, 0, ElSupEnum.SUPPORT_ROLLER_END.value)
    q = Symbol('p')
    l = Symbol('l')
    lineload = [0, q]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = []
    elementlist = []
    ele = ElementCalculation(0, start_knot, middle_knot, 0.5 * l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    ele.start_calculation()
    elementlist.append(ele)
    knot_list.append([start_knot, middle_knot])
    ele = ElementCalculation(1, middle_knot, end_knot, 0.5 * l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    start_knot.add_coupled_el(0)
    middle_knot.add_coupled_el([0, 1])
    end_knot.add_coupled_el(1)
    knot_list.append([middle_knot, end_knot])
    elementlist.append(ele)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def two_beam_combined_to_one_complete_lineload_test_2l():
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_FIXED_END.value)
    middle_knot = Knot.Knot(1, 0.5, 0, ElSupEnum.THROUGH_ELEMENT.value)
    end_knot = Knot.Knot(2, 1, 0, ElSupEnum.SUPPORT_ROLLER_END.value)
    q = Symbol('p')
    l = Symbol('l')
    lineload = [0, q]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = []
    elementlist = []
    ele = ElementCalculation(0, start_knot, middle_knot, l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([start_knot, middle_knot])
    ele = ElementCalculation(1, middle_knot, end_knot, l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    start_knot.add_coupled_el(0)
    middle_knot.add_coupled_el([0, 1])
    end_knot.add_coupled_el(1)
    knot_list.append([middle_knot, end_knot])
    elementlist.append(ele)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def two_beam_combined_to_one_single_load_middle():
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_FIXED_END.value)
    middle_knot = Knot.Knot(1, 0.5, 0, ElSupEnum.THROUGH_ELEMENT.value, [0, 0, 0], [0, Symbol('F'), 0])
    end_knot = Knot.Knot(2, 1, 0, ElSupEnum.SUPPORT_ROLLER_END.value)
    q = Symbol('p')
    l = Symbol('l')
    lineload = [0, 0]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = []
    elementlist = []
    ele = ElementCalculation(0, start_knot, middle_knot, l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([start_knot, middle_knot])
    ele = ElementCalculation(1, middle_knot, end_knot, l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    knot_list.append([middle_knot, end_knot])
    start_knot.add_coupled_el(0)
    middle_knot.add_coupled_el([0, 1])
    end_knot.add_coupled_el(1)
    elementlist.append(ele)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def single_clamping_left_side():                # TODO:  Aufpassen mit den Richtungen, spinnt, wenn mann die Koordinaten vertauscht
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_CLAMPED.value)
    end_knot = Knot.Knot(1, 1, 0, ElSupEnum.FREE_END.value, [0, 0, 0], [0, Symbol('F'), 0])
    q = Symbol('p')
    l = Symbol('l')
    lineload = [0, q]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = [[start_knot, end_knot]]
    elementlist = []
    ele = ElementCalculation(0, start_knot, end_knot, l, lineload, temp_prop)
    start_knot.add_coupled_el(0)
    end_knot.add_coupled_el(0)
    elementlist.append(ele)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def single_clamping_left_side_single_load():
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_CLAMPED.value)
    end_knot = Knot.Knot(1, 1, 0, ElSupEnum.FREE_END.value, [0, 0, 0], [0, Symbol('F'), 0])
    q = Symbol('p')
    l = Symbol('l')
    lineload = [0, 0]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = [[start_knot, end_knot]]
    elementlist = []
    ele = ElementCalculation(0, start_knot, end_knot, l, lineload, temp_prop)
    start_knot.add_coupled_el(0)
    end_knot.add_coupled_el(0)
    elementlist.append(ele)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def single_beam_lineload_test_seperated_elements():
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_FIXED_END.value)
    end_knot = Knot.Knot(1, 1, 0, ElSupEnum.SUPPORT_ROLLER_END.value)
    start_knot2 = Knot.Knot(3, 0, 1, ElSupEnum.SUPPORT_FIXED_END.value)
    end_knot2 = Knot.Knot(4, 1, 1, ElSupEnum.SUPPORT_ROLLER_END.value)
    knot_list = []
    knot_list.append([start_knot, end_knot])
    knot_list.append([start_knot2, end_knot2])
    q = Symbol('p')
    l1 = Symbol('l1')
    l2= Symbol('l2')
    lineload = [0, q]
    temp_prop = TempProps.TempProps(0, 0, 0)
    elementlist = []
    ele = ElementCalculation(0, start_knot, end_knot, l1, lineload, temp_prop)
    elementlist.append(ele)
    ele = ElementCalculation(1, start_knot2, end_knot2, l2, lineload, temp_prop)
    start_knot.add_coupled_el(0)
    end_knot.add_coupled_el(0)
    start_knot2.add_coupled_el(1)
    end_knot2.add_coupled_el(1)
    elementlist.append(ele)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def two_beam_combined_to_one_single_load_middle_joint():
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_CLAMPED.value)
    middle_knot = Knot.Knot(1, 0.5, 0, ElSupEnum.JOINT.value)  #, [0, 0, 0], [0, Symbol('F'), 0]
    end_knot = Knot.Knot(2, 1, 0, ElSupEnum.SUPPORT_ROLLER_END.value)
    q = Symbol('p')
    l = Symbol('l')
    lineload1 = [0, 0]
    lineload2 = [0, q]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = []
    elementlist = []
    ele = ElementCalculation(0, start_knot, middle_knot, l, lineload1, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([start_knot, middle_knot])
    ele = ElementCalculation(1, middle_knot, end_knot, l, lineload2, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    knot_list.append([middle_knot, end_knot])
    start_knot.add_coupled_el(0)
    middle_knot.add_coupled_el([0, 1])
    end_knot.add_coupled_el(1)
    elementlist.append(ele)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)

def example_from_sheet_2_4():
    l = Symbol('l')
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_FIXED_END.value)
    middle_knot = Knot.Knot(1, 1, 0, ElSupEnum.THROUGH_ELEMENT.value, [2 * Symbol('EA')/l, 0, 0])
    end_knot = Knot.Knot(2, 2, 0, ElSupEnum.SUPPORT_ROLLER_END.value, [0, 0, 0], [Symbol('F'), 0, 0])
    q = Symbol('p')
    lineload = [0, 0]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = []
    elementlist = []
    ele = ElementCalculation(0, start_knot, middle_knot, l, lineload, temp_prop, Symbol('EI'), Symbol('EA'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([start_knot, middle_knot])
    ele = ElementCalculation(1, middle_knot, end_knot, l, lineload, temp_prop, Symbol('EI'), Symbol('EA'), Symbol('h'))
    knot_list.append([middle_knot, end_knot])
    start_knot.add_coupled_el(0)
    middle_knot.add_coupled_el([0, 1])
    end_knot.add_coupled_el(1)
    elementlist.append(ele)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def two_beam_triangle_load_middle():
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_FIXED_END.value)
    middle_knot = Knot.Knot(1, math.sqrt(0.5), math.sqrt(0.5), ElSupEnum.JOINT.value, [0, 0, 0], [0, Symbol('F'), 0])
    end_knot = Knot.Knot(2, 2 * math.sqrt(0.5), 0, ElSupEnum.SUPPORT_FIXED_END.value)
    q = Symbol('p')
    l = Symbol('l')
    lineload = [0, 0]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = []
    elementlist = []
    ele = ElementCalculation(0, start_knot, middle_knot, l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([start_knot, middle_knot])
    ele = ElementCalculation(1, middle_knot, end_knot, l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    knot_list.append([middle_knot, end_knot])
    start_knot.add_coupled_el(0)
    middle_knot.add_coupled_el([0, 1])
    end_knot.add_coupled_el(1)
    elementlist.append(ele)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def two_beam_triangle_load_middle_not_symmetrical():
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_FIXED_END.value)
    middle_knot = Knot.Knot(1, 2, 1, ElSupEnum.JOINT.value, [0, 0, 0], [0, Symbol('F'), 0], 0)
    end_knot = Knot.Knot(2, 3, 0, ElSupEnum.SUPPORT_FIXED_END.value, [0, 0, 0], [0, 0, 0], 0)
    q = Symbol('p')
    l = Symbol('l')
    lineload = [0, 0]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = []
    elementlist = []
    ele = ElementCalculation(0, start_knot, middle_knot, math.sqrt(5) * l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([start_knot, middle_knot])
    ele = ElementCalculation(1, middle_knot, end_knot, math.sqrt(2) * l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    knot_list.append([middle_knot, end_knot])
    start_knot.add_coupled_el(0)
    middle_knot.add_coupled_el([0, 1])
    end_knot.add_coupled_el(1)
    elementlist.append(ele)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def two_beam_corner_line_load():
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_FIXED_END.value)
    middle_knot = Knot.Knot(1, 0, 1, ElSupEnum.JOINT.value, [0, 0, 0], [0, 0, 0])
    end_knot = Knot.Knot(2, 1, 1, ElSupEnum.SUPPORT_FIXED_END.value)
    q = Symbol('p')
    l = Symbol('l')
    lineload = [0, q]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = []
    elementlist = []
    ele = ElementCalculation(0, start_knot, middle_knot, l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([start_knot, middle_knot])
    ele = ElementCalculation(1, middle_knot, end_knot, l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    knot_list.append([middle_knot, end_knot])
    start_knot.add_coupled_el(0)
    middle_knot.add_coupled_el([0, 1])
    end_knot.add_coupled_el(1)
    elementlist.append(ele)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)
    testbox.vis_structure_from_input(knot_list, elementlist)


def single_beam_schraeg():
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_FIXED_END.value, [0, 0, 0], [0, 0, 0], 45)
    end_knot = Knot.Knot(1, math.sqrt(0.5), math.sqrt(0.5), ElSupEnum.SUPPORT_ROLLER_END.value, [0, 0, 0], [0, Symbol('F'), 0], 45)
    q = Symbol('p')
    l = Symbol('l')
    lineload = [0, 0]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = [[start_knot, end_knot]]
    elementlist = []
    ele = ElementCalculation(0, start_knot, end_knot, l, lineload, temp_prop, Symbol('EI'), Symbol('EA'), Symbol('h'))
    start_knot.add_coupled_el(0)
    end_knot.add_coupled_el(0)
    elementlist.append(ele)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def example_ss13():
    q = Symbol('p')
    l = Symbol('l')
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_TRANSVERSE_FORCE.value, [0, 0, 0], [0, 2 * q * l, (-1) * 2 * q * l**2], 0)
    middle_knot1 = Knot.Knot(1, 1, 0, ElSupEnum.JOINT.value)
    middle_knot2 = Knot.Knot(2, 1.5, 0, ElSupEnum.SUPPORT_ROLLER_CONTINUOUS.value, [0, 0, 0], [0, 0, q * l**2], 0)
    end_knot = Knot.Knot(3, 2.5, 0, ElSupEnum.SUPPORT_ROLLER_END.value)
    lineload = [0, q]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = []
    elementlist = []
    ele = ElementCalculation(0, start_knot, middle_knot1, l, [0, 0], temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([start_knot, middle_knot1])
    ele = ElementCalculation(1, middle_knot1, middle_knot2, 0.5 * l, [0, 0], temp_prop, float('inf'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([middle_knot1, middle_knot2])
    ele = ElementCalculation(2, middle_knot2, end_knot, l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    start_knot.add_coupled_el(0)
    middle_knot1.add_coupled_el([0, 1])
    middle_knot2.add_coupled_el([1, 2])
    end_knot.add_coupled_el(2)
    knot_list.append([middle_knot2, end_knot])
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def example_ss12():
    q = Symbol('p')
    l = Symbol('l')
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_CLAMPED.value)
    middle_knot1 = Knot.Knot(1, 1, 0, ElSupEnum.JOINT.value)
    middle_knot2 = Knot.Knot(2, 2, 0, ElSupEnum.SUPPORT_ROLLER_CONTINUOUS.value, [0, 0, 0], [0, 0, (-1) * q * l**2], 0)
    end_knot = Knot.Knot(3, 3, 0, ElSupEnum.FREE_END.value, [0, 0, 0], [0, q * l, 0], 0)
    lineload = [0, q]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = []
    elementlist = []
    ele = ElementCalculation(0, start_knot, middle_knot1, l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([start_knot, middle_knot1])
    ele = ElementCalculation(1, middle_knot1, middle_knot2, l, [0, 0], temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([middle_knot1, middle_knot2])
    ele = ElementCalculation(2, middle_knot2, end_knot, l, [0, 0], temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    start_knot.add_coupled_el(0)
    middle_knot1.add_coupled_el([0, 1])
    middle_knot2.add_coupled_el([1, 2])
    end_knot.add_coupled_el(2)
    knot_list.append([middle_knot2, end_knot])
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def example_ss12_vereinfacht():
    q = Symbol('p')
    l = Symbol('l')
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_CLAMPED.value)
    middle_knot1 = Knot.Knot(1, 1, 0, ElSupEnum.JOINT.value)
    middle_knot2 = Knot.Knot(2, 2, 0, ElSupEnum.SUPPORT_ROLLER_END.value, [0, 0, 0], [0, q * l, (-1) * 2 * q * l**2], 0)
    lineload = [0, q]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = []
    elementlist = []
    ele = ElementCalculation(0, start_knot, middle_knot1, l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([start_knot, middle_knot1])
    ele = ElementCalculation(1, middle_knot1, middle_knot2, l, [0, 0], temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([middle_knot1, middle_knot2])
    start_knot.add_coupled_el(0)
    middle_knot1.add_coupled_el([0, 1])
    middle_knot2.add_coupled_el(1)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def example_ss11():
    q = Symbol('p')
    l = Symbol('l')
    x = Symbol('x')
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.FREE_END.value)
    middle_knot1 = Knot.Knot(1, 1, 0, ElSupEnum.SUPPORT_FIXED_CONTINUOUS.value, [0, 0, 0], [0, 0, 1 / 3 * q * l ** 2], 0)
    middle_knot2 = Knot.Knot(2, 2, 0, ElSupEnum.SUPPORT_ROLLER_END.value)
    lineload = [0, q * x]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = []
    elementlist = []
    ele = ElementCalculation(0, start_knot, middle_knot1, l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([start_knot, middle_knot1])
    ele = ElementCalculation(1, middle_knot1, middle_knot2, l, [0, 0], temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([middle_knot1, middle_knot2])
    start_knot.add_coupled_el(0)
    middle_knot1.add_coupled_el([0, 1])
    middle_knot2.add_coupled_el(1)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def example_ss14():
    q = Symbol('p')
    l = Symbol('l')
    k = Symbol('k')
    h = Symbol('h')
    at = Symbol('at')
    ei = Symbol('EI')
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.FREE_END.value, [0, k, 0], [0, 0, 0], 0)
    middle_knot1 = Knot.Knot(1, 2, 0, ElSupEnum.SUPPORT_ROLLER_CONTINUOUS.value, [0, 0, 0], [0, 0, - 2 * q * l**2], 0)
    middle_knot2 = Knot.Knot(2, 3, 0, ElSupEnum.JOINT.value)
    end_knot = Knot.Knot(3, 4, 0, ElSupEnum.SUPPORT_CLAMPED.value)
    lineload = [0, 2 * q]
    temp_prop = TempProps.TempProps(0, at, (2 * h * q * l**2)/(ei * at))
    temp_prop1 = TempProps.TempProps(0, 0, 0)
    knot_list = []
    elementlist = []
    ele = ElementCalculation(0, start_knot, middle_knot1, 2 * l, lineload, temp_prop1, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([start_knot, middle_knot1])
    ele = ElementCalculation(1, middle_knot1, middle_knot2, l, [0, 0], temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([middle_knot1, middle_knot2])
    ele = ElementCalculation(2, middle_knot2, end_knot, l, [0, 0], temp_prop1, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([middle_knot2, end_knot])
    start_knot.add_coupled_el(0)
    middle_knot1.add_coupled_el([0, 1])
    middle_knot2.add_coupled_el([1, 2])
    end_knot.add_coupled_el(2)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def example_unterlagen_test():
    q = Symbol('q')
    l = Symbol('l')
    m = Symbol('M')
    start_knot = Knot.Knot(0, 0.5, 2, ElSupEnum.SUPPORT_ROLLER_END.value, [0, 0, 0], [0, 0, 0], 0)
    middle_knot1 = Knot.Knot(1, 2.5, 2, ElSupEnum.JOINT.value, [0, 0, 0], [0, 0, 0], 0)
    middle_knot2 = Knot.Knot(2, 2.5, 1, ElSupEnum.THROUGH_ELEMENT.value, [0, 0, 0], [0, 0, - 2 * m], 0)
    end_knot = Knot.Knot(3, 4.5, 1, ElSupEnum.SUPPORT_CLAMPED.value)
    lineload = [0, q]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = []
    elementlist = []
    ele = ElementCalculation(0, start_knot, middle_knot1, 2 * l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([start_knot, middle_knot1])
    ele = ElementCalculation(1, middle_knot1, middle_knot2, l, [0, 0], temp_prop, float('inf'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([middle_knot1, middle_knot2])
    ele = ElementCalculation(2, middle_knot2, end_knot, 2 * l, [0, 0], temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([middle_knot2, end_knot])
    start_knot.add_coupled_el(0)
    middle_knot1.add_coupled_el([0, 1])
    middle_knot2.add_coupled_el([1, 2])
    end_knot.add_coupled_el(2)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)
    testbox.vis_structure_from_input(knot_list, elementlist)


def example_unterlagen_test_vereinfacht():
    q = Symbol('p')
    l = Symbol('l')
    middle_knot1 = Knot.Knot(1, 2, 1, ElSupEnum.FREE_END.value, [0, 0, 0], [0, q * l, 0], 0)
    middle_knot2 = Knot.Knot(2, 2, 0, ElSupEnum.THROUGH_ELEMENT.value, [0, 0, 0], [0, 0, - 2 * q * l**2], 0)
    end_knot = Knot.Knot(3, 4, 0, ElSupEnum.SUPPORT_CLAMPED.value)
    lineload = [0, q]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = []
    elementlist = []
    ele = ElementCalculation(0, middle_knot1, middle_knot2, l, [0, 0], temp_prop, float('inf'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([middle_knot1, middle_knot2])
    ele = ElementCalculation(1, middle_knot2, end_knot, 2 * l, [0, 0], temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([middle_knot2, end_knot])
    middle_knot1.add_coupled_el(0)
    middle_knot2.add_coupled_el([0, 1])
    end_knot.add_coupled_el(1)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def single_beam_cos_test():
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_ROLLER_END.value)
    end_knot = Knot.Knot(1, 1, 0, ElSupEnum.SUPPORT_FIXED_END.value)
    q = Symbol('p')
    l = Symbol('l')
    x = Symbol('x')
    lineload = [0, q * sin(2 * math.pi * x)]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = [[start_knot, end_knot]]
    elementlist = []
    ele = ElementCalculation(0, start_knot, end_knot, l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    start_knot.add_coupled_el(0)
    end_knot.add_coupled_el(0)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def multiple_elements():
    l = Symbol('l')
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_FIXED_END.value, [0, 0, 0], [0, 0, 0], 0)
    middle_knot = Knot.Knot(1, 1, 0, ElSupEnum.THROUGH_ELEMENT.value)
    end_knot1 = Knot.Knot(2, 2, 0, ElSupEnum.FREE_END.value, [0, 0, 0], [0, Symbol('F'), 0], 0)
    end_knot2 = Knot.Knot(2, 1, 2, ElSupEnum.SUPPORT_ROLLER_END.value, [0, 0, 0], [0, 0, 0], 180)
    knot_list = []
    elementlist = []
    temp_prop = TempProps.TempProps(0, 0, 0)
    lineload = [0, 0]
    knot_list.append([start_knot, middle_knot])
    ele0 = ElementCalculation(0, start_knot, middle_knot, l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele0)
    ele1 = ElementCalculation(1, middle_knot, end_knot1, l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele1)
    knot_list.append([middle_knot, end_knot1])
    ele2 = ElementCalculation(2, middle_knot, end_knot2, l, lineload, temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele2)
    knot_list.append([middle_knot, end_knot2])
    start_knot.add_coupled_el(0)
    middle_knot.add_coupled_el([0, 1, 2])
    end_knot1.add_coupled_el(1)
    end_knot2.add_coupled_el(2)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)
    testbox.vis_structure_from_input(knot_list, elementlist)



def example_2_23():
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_ROLLER_END.value, [Symbol('k'), 0, 0], [0, 0, 0], 0)
    middle_knot = Knot.Knot(1, 1, 0, ElSupEnum.THROUGH_ELEMENT.value)
    end_knot = Knot.Knot(2, 2, 0, ElSupEnum.SUPPORT_ROLLER_END.value, [2 * Symbol('k'), 0, 0], [0, 0, 0], 0)
    q = Symbol('p')
    x = Symbol('x')
    l = Symbol('l')
    knot_list = []
    elementlist = []
    lineload = [- q * cos(math.pi * x / 2), 0]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list.append([start_knot, middle_knot])
    ele1 = ElementCalculation(0, start_knot, middle_knot, l, [0, 0], temp_prop, Symbol('EI'), float('inf'),
                              Symbol('h'))
    elementlist.append(ele1)
    ele2 = ElementCalculation(1, middle_knot, end_knot, l, lineload, temp_prop, Symbol('EI'), Symbol('EA'),
                              Symbol('h'))
    elementlist.append(ele2)
    knot_list.append([middle_knot, end_knot])
    start_knot.add_coupled_el(0)
    middle_knot.add_coupled_el([0, 1])
    end_knot.add_coupled_el(1)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def example_2_3_neu():
    l = Symbol('l')
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_FIXED_END.value, [0, 0, 0], [0, 0, 0], 0)
    middle_knot1 = Knot.Knot(1, 1, 0, ElSupEnum.SUPPORT_ROLLER_JOINT.value, [0, 0, 0], [0, 0, 0])
    middle_knot2 = Knot.Knot(2, 2, 0, ElSupEnum.SUPPORT_ROLLER_JOINT.value, [0, 0, 0], [Symbol('F'), 0, 0])
    end_knot = Knot.Knot(3, 3, 0, ElSupEnum.SUPPORT_FIXED_END.value, [0, 0, 0], [0, 0, 0], 0)
    knot_list = []
    elementlist = []
    lineload = [- Symbol('p'), 0]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list.append([start_knot, middle_knot1])
    ele1 = ElementCalculation(0, start_knot, middle_knot1, l, lineload, temp_prop, float('inf'), Symbol('EA'), Symbol('h'))
    elementlist.append(ele1)
    knot_list.append([middle_knot1, middle_knot2])
    ele2 = ElementCalculation(1, middle_knot1, middle_knot2, l, [0, 0], temp_prop, 0, 0, Symbol('h'),2 * Symbol('EA')/l)
    elementlist.append(ele2)
    knot_list.append([middle_knot2, end_knot])
    ele3 = ElementCalculation(2, middle_knot2, end_knot, l, [0, 0], temp_prop, float('inf'), Symbol('EA'), Symbol('h'))
    elementlist.append(ele3)
    start_knot.add_coupled_el(0)
    middle_knot1.add_coupled_el([0, 1])
    middle_knot2.add_coupled_el([1, 2])
    end_knot.add_coupled_el(2)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)
    testbox.vis_structure_from_input(knot_list, elementlist)


def example_ss15():
    q = Symbol('p')
    l = Symbol('l')
    x = Symbol('x')
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_FIXED_END.value)
    middle_knot1 = Knot.Knot(1, 2, 0, ElSupEnum.JOINT.value, [0, 0, 3 * Symbol('EI')/l], [0, - 8 * q * l, 0])
    middle_knot2 = Knot.Knot(2, 4, 0, ElSupEnum.SUPPORT_ROLLER_CONTINUOUS.value, [0, 0, 0], [0, 0, 6 * q * l**2], 0)
    end_knot = Knot.Knot(3, 5, 0, ElSupEnum.FREE_END.value, [0, Symbol('EI')/(l**3), 0])
    lineload = [0, 7.5 * q * x]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list = []
    elementlist = []
    ele = ElementCalculation(0, start_knot, middle_knot1, 2 * l, lineload, temp_prop, 2 * Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([start_knot, middle_knot1])
    ele = ElementCalculation(1, middle_knot1, middle_knot2, 2 * l, [0, 0], temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    knot_list.append([middle_knot1, middle_knot2])
    ele = ElementCalculation(2, middle_knot2, end_knot, l, [0, 0], temp_prop, Symbol('EI'), float('inf'), Symbol('h'))
    elementlist.append(ele)
    start_knot.add_coupled_el(0)
    middle_knot1.add_coupled_el([0, 1])
    middle_knot2.add_coupled_el([1, 2])
    end_knot.add_coupled_el(2)
    knot_list.append([middle_knot2, end_knot])
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)
    testbox.vis_structure_from_input(knot_list, elementlist)


def example_SS_16():
    q = Symbol('p')
    x = Symbol('x')
    l = Symbol('l')
    start_knot = Knot.Knot(0, 0, 0, ElSupEnum.SUPPORT_TRANSVERSE_FORCE.value, [0, 0, 0], [0, - 3 * q * l, 0], 0)
    middle_knot = Knot.Knot(1, 1, 0, ElSupEnum.JOINT.value, [0, 3 * Symbol('EI')/l**3, 0])
    end_knot = Knot.Knot(2, 2, 0, ElSupEnum.FREE_END.value, [0, - 6 * Symbol('EI')/l**3, 0], [0, 0, 2 * q * l**2], 0)
    knot_list = []
    elementlist = []
    lineload = [0, 12 * q]
    temp_prop = TempProps.TempProps(0, 0, 0)
    knot_list.append([start_knot, middle_knot])
    ele1 = ElementCalculation(0, start_knot, middle_knot, l, [0, 0], temp_prop, float('inf'), float('inf'),
                              Symbol('h'))
    elementlist.append(ele1)
    ele2 = ElementCalculation(1, middle_knot, end_knot, l, lineload, temp_prop, Symbol('EI'), float('inf'),
                              Symbol('h'))
    elementlist.append(ele2)
    knot_list.append([middle_knot, end_knot])
    start_knot.add_coupled_el(0)
    middle_knot.add_coupled_el([0, 1])
    end_knot.add_coupled_el(1)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)


def final_structure_software_lab():
    f = Symbol('F')
    k = Symbol('k')
    start_knot = Knot.Knot(0, 1, 3, ElSupEnum.SUPPORT_CLAMPED.value)
    middle_knot = Knot.Knot(1, 2, 3, ElSupEnum.JOINT.value, [0, 0, 0], [0, f, 0])
    end_knot = Knot.Knot(2, 3, 2, ElSupEnum.SUPPORT_ROLLER_END.value, [0, 0, k])
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
    print(l0)
    ele0 = ElementCalculation(0, start_knot, middle_knot, l0, line_load_0, temp_load_0, ei=ei, ea=float('inf'), h=h)
    elementlist.append(ele0)
    knot_list.append([start_knot, middle_knot])

    # ELEMENT 1
    line_load_1 = [0, 0]
    temp_load_1 = TempProps.TempProps(0, Symbol('dT'), at)
    l1 = gc.knot_dist(middle_knot, end_knot) * l
    print(l1)
    ele1 = ElementCalculation(1, middle_knot, end_knot, l1, line_load_1, temp_load_1, ei=ei, ea=float('inf'), h=h)
    elementlist.append(ele1)
    knot_list.append([middle_knot, end_knot])

    start_knot.add_coupled_el(0)
    middle_knot.add_coupled_el([0, 1])
    end_knot.add_coupled_el(1)
    functions, x, l_list = CalculationElement(elementlist)
    testbox.print_graphs(functions, x, l_list, knot_list)

    # VIS STRUCTURE
    testbox.vis_structure_from_input(knot_list, elementlist)


