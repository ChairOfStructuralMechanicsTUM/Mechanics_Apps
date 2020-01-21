from sympy import Symbol
from numpy import array, append
from Libs.print_function_helpers import print_arr, print_results
from sympy import solve, integrate, Eq
import vis_initialization as vis_init
import time


def CalculationElement(elementlist):
    """
    :param elementlist: list of all elements
    :return:
        all_functions: [[functions of elements 1][functions of element 2]...[functions of element n]]
            --> order of functions: N, u, Q, M, w, phi
        x: Symbol to plot over
        l_list: list of length of all elements
    """
    i = 0
    rb = array([])
    eq = array([])
    functions = array([])
    all_functions = []
    x = Symbol('x')
    l_list = array([])

    for el in elementlist:
        # print(el)
        [eqN, equ, eqQ, eqM, eqphi, eqw] = el.compute_eqns_int()
        l_list = append(l_list, el.length_)
        eq = append(eq, eqN)
        eq = append(eq, equ)
        eq = append(eq, eqQ)
        eq = append(eq, eqM)
        eq = append(eq, eqphi)
        eq = append(eq, eqw)

        if el.k_spring_ != 0:
            """ If the element is a spring, further equations are needed, which are added here to the equation system"""
            eq = append(eq, Eq(Symbol('phi_0' + str(el.id_el_)), 0))
            eq = append(eq, Eq(Symbol('M_0' + str(el.id_el_)), 0))
            eq = append(eq, Eq(Symbol('N_1' + str(el.id_el_)) + el.k_spring_ * (Symbol('u_0' + str(el.id_el_)) - Symbol('u_1' + str(el.id_el_))), 0))


        """ Boundary conditions for each element are set"""
        startcondition = el.set_eqnsstart(el.type1_, elementlist)
        eq = append(eq, startcondition)
        endcondition = el.set_eqnsend(el.type2_, elementlist)
        eq = append(eq, endcondition)

        """The variables to solve for a defined --> they contain the start and end forces/displacements of each element"""
        if i == 0:
            rb = [Symbol('N_0' + str(i)), Symbol('u_0' + str(i)), Symbol('Q_0' + str(i)), Symbol('M_0' + str(i)),\
                  Symbol('phi_0' + str(i)), Symbol('w_0' + str(i)), Symbol('N_1' + str(i)), Symbol('u_1' + str(i)),\
                   Symbol('Q_1' + str(i)), Symbol('M_1' + str(i)), Symbol('phi_1' + str(i)), Symbol('w_1' + str(i))]
        else:
            rb.extend([Symbol('N_0' + str(i)), Symbol('u_0' + str(i)), Symbol('Q_0' + str(i)), Symbol('M_0' + str(i)),\
                  Symbol('phi_0' + str(i)), Symbol('w_0' + str(i)), Symbol('N_1' + str(i)), Symbol('u_1' + str(i)),\
                  Symbol('Q_1' + str(i)), Symbol('M_1' + str(i)), Symbol('phi_1' + str(i)), Symbol('w_1' + str(i))])
        i = i+1
    # print_arr(rb)
    # print_arr(eq)
    try:
        """The matrix is solved"""
        result = solve(eq, rb)
        # print('These are the results:')
        # print(result)
    except:
        """Calculation failed, error message to user and None values for plotting"""
        vis_init.expand_msg2user('The calculation failed, the most likely error is a movable system', "orange")
        for el in elementlist:
            for ind in range(0, 6):
                functions = append(functions, None)
            all_functions.append(functions)
        return all_functions, x, l_list

    if result == []:
        """Calculation failed, error message to user and None values for plotting"""
        vis_init.expand_msg2user('The calculation failed, the most likely error is a movable system', "orange")
        for el in elementlist:
            for ind in range(0, 6):
                functions = append(functions, None)
            all_functions.append(functions)
        return all_functions, x, l_list

    elif result == 0:
        """Calculation failed, error message to user and None values for plotting"""
        vis_init.expand_msg2user('The load function can not be handeled', "orange")
        for el in elementlist:
            all_functions = append(all_functions, [None, None, None, None, None, None])
        return all_functions, x, l_list

    else:
        for el in elementlist:
            functions = array([])
            if el.k_spring_ != 0:
                """ If the element is a spring, nothing should be plottet, therefore only None values are returned"""
                for ind in range(0, 6):
                    functions = append(functions, None)
                all_functions.append(functions)
            else:
                """ sets up final equations for plotting"""
                [eq_n_final, eq_u_final, eq_q_final, eq_m_final, eq_phi_final, eq_w_final] = get_sym_func_for_element(el.id_el_, el.n_, el.q_, el.ei_, el.ea_, result, x, [el.temp_, el.temp_coeff_, el.temp_diff_, el.h_])

                functions = append(functions, eq_n_final)
                functions = append(functions, eq_u_final)
                functions = append(functions, eq_q_final)
                functions = append(functions, (-1) * eq_m_final)
                functions = append(functions, (-1) * eq_w_final)
                functions = append(functions, eq_phi_final)
                all_functions.append(functions)
        print('These are the functions:')
        print_arr(all_functions)
        if len(rb) <= 0:
            rb.clear()
        vis_init.expand_msg2user("Calculation was successful")

        return all_functions, x, l_list


def get_sym_func_for_element(i, n_lineload, q_lineload, ei, ea,  result, x, temprops):
    """Integrates over line loads, adds temperature load and calculated values from solve of matrix"""
    eq_n_final = integrate_function_with_constant((-1) * n_lineload, x, result[Symbol('N_0'+str(i))])
    eq_u_final = integrate_function_with_constant(eq_n_final/ea + temprops[1] * temprops[0], x, result[Symbol('u_0'+str(i))])
    eq_q_final = integrate_function_with_constant((-1) * q_lineload, x, result[Symbol('Q_0'+str(i))])
    eq_m_final = integrate_function_with_constant(eq_q_final, x, result[Symbol('M_0'+str(i))])
    eq_phi_final = integrate_function_with_constant((-1) * eq_m_final/ei - temprops[1] * temprops[2]/(temprops[3]), x, result[Symbol('phi_0'+str(i))])
    eq_w_final = integrate_function_with_constant(eq_phi_final, x, result[Symbol('w_0'+str(i))])

    return [eq_n_final, eq_u_final, eq_q_final, eq_m_final, eq_phi_final, eq_w_final]


def integrate_function_with_constant(func, sym, constant=0):
    return integrate(func, sym) + constant
