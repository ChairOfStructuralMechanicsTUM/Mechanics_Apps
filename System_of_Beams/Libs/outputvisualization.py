# EXTERNAL LIBS
import numpy as np
from sympy import lambdify,  pprint, Symbol, diff
import math as m
import time
import traceback

# CUSTOM LIBS
from Libs import HtmlColors as htmlcol
from Classes import LinePlot
from Libs import geometriccalc as gc
from Libs import symbolictoolbox as symbbox
from Libs import print_function_helpers as prhlp
from Classes.CurrentDocument import CurrentDoc


def add_el_to_dict(dict_to_add, key, value):
    """
    Adds a new value to an existing dictionary. If the key already exists,
    the the value gets inserted into a list of related values to this one key
    :param dict_to_add: dictionary, getting updated
    :param key: key to search for in the dictionary
    :param value: new value that needs to be added
    """
    if key in dict_to_add:
        dict_to_add[key].append(value)
    else:
        if isinstance(value, list):
            dict_to_add.update({key: value})
        else:
            dict_to_add.update({key: [value]})


def print_call_stack():
    """
    Prints the current call stack. Can be used for debugging
    """
    for line in traceback.format_stack():
        print(line.strip())


def toggle_extreme_values(curr_doc: CurrentDoc, plot, vals_active=True):
    """
    Toggles the visualisation of the extreme values in a chosen plot
    :param plot: plot to visualise the extreme values in
    :param vals_active: Boolean to define if values shell be plotted or not
    :return:
    """
    # toggle extreme values
    toggle_visibility_of_glyphs(plot, curr_doc.plot_data.extreme_vals_dict, "text", vals_active)
    toggle_visibility_of_glyphs(plot, curr_doc.plot_data.extreme_vals_cross_dict, "line", vals_active)


def toggle_bound_vals(curr_doc: CurrentDoc, plot, vals_active=True):
    # toggle boundary values
    toggle_visibility_of_glyphs(plot, curr_doc.plot_data.bound_vals_dict, "text", vals_active)


def toggle_zero_crossing(curr_doc: CurrentDoc, plot, vals_active=True):
    # toggle zero_crossing
    toggle_visibility_of_glyphs(plot, curr_doc.plot_data.zero_cross_dict, "text", vals_active)
    toggle_visibility_of_glyphs(plot, curr_doc.plot_data.zero_cross_cross_dict, "line", vals_active)


def toggle_visibility_of_glyphs(plot, dict_to_search, glyph_type, vals_active):
    """
    Toggles the visibility of a glyph. For the related plot, a list of values is taken out of the dict_to_search
    This list contains all values that need to be toggled
    :param plot: The plot the visibility is changed in
    :param dict_to_search: Dict of all plots, for specified values
    :param glyph_type: defines, which type of glyph needs to be accessed. supports: "text" or "line"
    :param vals_active: Defines if switched on or off
    :return:
    """
    # toggle zero crossing values
    if plot in dict_to_search:
        search_name_list = dict_to_search[plot]
        for el in search_name_list:
            search_glyph = plot.select(name=el)
            if vals_active:
                if glyph_type.lower() == "text":
                    search_glyph[0].glyph.update(text_alpha=1)
                elif glyph_type.lower() == "line":
                    search_glyph[0].glyph.update(line_alpha=1)
            else:
                if glyph_type.lower() == "text":
                    search_glyph[0].glyph.update(text_alpha=0)
                elif glyph_type.lower() == "line":
                    search_glyph[0].glyph.update(line_alpha=0)


def plot_structure_from_knots(plot, knot_list, plot_list, line_width=6):
    """
    plots the beam structure from a knot list being inputted
    :param plot: plot to add the structure to
    :param knot_list: knots that need to be plotted [[start_knot_1, end_knot_1], ... , [start_knot_n, end_knot_n]]
    :param plot_list: collects all elements that exist in this plot (needed to delete everything)
    """
    i = 0
    for knots in knot_list:
        col = htmlcol.plot_cols[i].value
        x_vals = [knots[0].x_, knots[1].x_]
        y_vals = [knots[0].y_, knots[1].y_]
        name = str(knots[0].id) + str(knots[1].id) + str(time.time())
        plot.line(x_vals, y_vals, line_color=col, line_width=line_width, name=name)
        plot_list.append(name)
        i += 1
        if i >= len(htmlcol.plot_cols):
            i = 0
    return


def calc_xy(symb_func, symb_to_plot_over, l_val, start_knot, end_knot):
    """
    Calculate the x- and y-coordinates for the plot
    :param symb_func: function that needs to be plotted
    :param symb_to_plot_over: running variable from 0 to 1, type(symb_to_plot_over) == type(sympy.Symbol())
    :param l_val: Defines length of the complete element
    :param start_knot: start knot for the function
    :param end_knot: end knot of the function
    """
    if symb_func is None:
        return None, None, False
    free_symbs = symb_func.free_symbols
    len_el = gc.knot_dist(start_knot, end_knot)
    prec_plot = 50

    x_length = float(symbbox.remove_free_symbols(l_val, None))
    x_vals = np.linspace(0, x_length, round(prec_plot*len_el))
    symb_func = symbbox.remove_free_symbols(symb_func, symb_to_plot_over)
    if symb_func == 0:
        return None, None, False
    if symb_to_plot_over in free_symbs:
        # evaluate function from zero to one with symb_to_plot_over
        func_lambdified = lambdify(symb_to_plot_over, symb_func, "numpy")
        y_vals = func_lambdified(x_vals)
    else:
        y_vals = np.full(len(x_vals), float(symb_func))
    return x_vals, y_vals, True


def scale_y_values(y_data, y_reference, y_max):
    """
    Scale the plot in y direction, to prevent extreme values.
    :param y_data:      the y data of the plot
    :param y_reference: the maximum value of the plot series (e.g. Normal force), which will be scaled to y_max
    :param y_max:       the maximum y value for the plot (e.g. if y_max=1, no y value in the plot will be greater than 1)
    """
    multipl_factor = y_max / y_reference
    for i in range(len(y_data)):
        y_data[i] = y_data[i] * multipl_factor
    return y_data, multipl_factor


'''
########################### WARNING ###########################
The lambdify uses the eval statement
make sure, this function only gets sanitized input
'''
def plot_symbolic_func(plot, symb_func, symb_to_plot_over, l_val, start_knot, end_knot, xy_data, y_reference, plot_list, line_color="#f46d43",line_width=4):
    """
    Gets a symbolic function and plots it for a running symbol from 0 to 1 and moves it to the position between two knots
    :param plot: plot to print the function to
    :param symb_func: function that needs to be plotted
    :param symb_to_plot_over: running variable from 0 to 1, type(symb_to_plot_over) == type(sympy.Symbol())
    :param l_val: Defines length of the complete element
    :param start_knot: start knot for the function
    :param end_knot: end knot of the function
    :param xy_data: x- and y-coordinates for the plot
    :param y_reference: the maximum value of the plot series (e.g. Normal force), which will be scaled to y_max
    :param plot_list: collects all elements that exist in this plot (needed to delete everything)
    """
    y_max = 1 # the maximum y value for the plot (e.g. if y_max=1, no y value in the plot will be greater than 1)
    if symb_func is None:
        return None, None, 0
    len_el = gc.knot_dist(start_knot, end_knot)
    prec_plot = 50
    tol = 1e-15

    # Plot a zero in the middle of the structure, if function is zero
    if symb_func == 0:
        x_val = start_knot.x_ + (end_knot.x_-start_knot.x_)/2
        y_val = start_knot.y_ + (end_knot.y_-start_knot.y_)/2
        name = str(start_knot.id) + str(end_knot.id) + str(time.time())
        plot.text([x_val], [y_val], ["0"], text_color=line_color, name=name,
                  text_font_size='4em', text_align='center', text_alpha=1, text_baseline='middle')
        plot_list.append(name)
        return None, None, 0

    x_vals, y_vals = xy_data[0], xy_data[1]
    if y_vals is None:
        return None, None, 0
        
    # Rotate, translate and scale function to beam to plot over
    y_vals, multipl_factor = scale_y_values(y_vals, y_reference, y_max)
    x_vals = np.linspace(start_knot.x_, start_knot.x_+len_el, round(prec_plot*len_el))
    y_vals += start_knot.y_
    x_vals, y_vals = gc.rotate_x_y_values(x_vals, y_vals, start_knot, end_knot, tol)
    
    x_vals = np.concatenate([[start_knot.x_], x_vals, [end_knot.x_]])
    y_vals = np.concatenate([[start_knot.y_], y_vals, [end_knot.y_]])
    name = str(start_knot.id) + str(end_knot.id) + str(time.time())
    plot.line(x_vals, y_vals, line_color=line_color, line_width=line_width, line_alpha=0.6, name=name)
    plot_list.append(name)

    return x_vals, y_vals, multipl_factor


def func_is_const(func, symb_to_plot_over):
    """
    Tests, if a function is constant for a given variable
    :param func: function to test
    :param symb_to_plot_over: dimension the function should be tested in
    :return: boolean
    """
    test_symb = Symbol('tEst_sYmbol')
    if func == func.subs(symb_to_plot_over, test_symb):
        return True
    else:
        return False


def plot_bound_val(curr_doc: CurrentDoc, x_val, y_val, text, plot, bound_val_name, color, rel_tol, abs_tol):
    """
    Plot the boundary values to a given plot and adds them to the reated dictionaries
    :param text: Text, that gets shown in the plot
    :param plot: plot to visualise in
    :param bound_val_name: internal name of the plot
    :param rel_tol: tolerance to check if already a element exists in the plot at this position
    :param abs_tol: see rel_tol
    """
    if plot in curr_doc.plot_data.char_vals_dict:
        points_to_check = curr_doc.plot_data.char_vals_dict[plot]
        # if gc.is_close_position(x_val, y_val, points_to_check, rel_tol, abs_tol):
        #     return

    plot.text([x_val], [y_val], [" " + str(text)], text_color=color,
              text_font_size='1.3em', text_align='left', text_alpha=0.6, name=bound_val_name)
    add_el_to_dict(curr_doc.plot_data.char_vals_dict, plot, LinePlot.PointCol(x_val, y_val))
    add_el_to_dict(curr_doc.plot_data.bound_vals_dict, plot, bound_val_name)


def print_charac_val_to_console(name, x, y):
    print("Name: {}\t x: {}\t y: {}".format(name, x, y))


def plot_characteristic_vals(curr_doc: CurrentDoc, plot, func, symb_to_plot_over, l_val, start_knot, end_knot, x_vals, y_vals, multipl_factor, plot_list, mirror_y_values=False, line_color="#f46d43"):
    """
    Calculates all characteristic values for a given function and visualises them
    Visibility of Start/ end values is by default 1
    Visibility of Extrema and zero crossing is by default 0
    :param plot: plot the values need to be added to
    :param func: func the values are based on
    :param symb_to_plot_over: the running variable
    :param l_val: length variable of the element
    :param x_vals: array of all x values of the function
    :param y_vals: array of all y_values rotated to the end configuration
    :param multipl_factor: scaling of y coordinates
    :param plot_list: collects all elements that exist in this plot (needed to delete everything)
    :param mirror_y_values: If True, changes the sign of the text value
    :return:
    """
    if func is None or x_vals is None or y_vals is None:
        return

    sign = 1
    if mirror_y_values:
        sign = -1

    func_without_free_symbs = symbbox.remove_free_symbols(func, symb_to_plot_over)
    len_symbol = next(iter(l_val.free_symbols))
    kn_dist = gc.knot_dist(start_knot, end_knot)
    rel_tol = 1e-1
    abs_tol = 1e-1

    # BOUNDARY VALUES
    start_text = symbbox.get_str_from_func(sign * symbbox.round_expr(func.subs(symb_to_plot_over, 0), 2))
    x_point_start = x_vals[1]
    y_point_start = y_vals[1]
    start_bound_name = "bound_start_" + prhlp.get_id_from_knots(start_knot, end_knot)
    plot_bound_val(curr_doc, x_point_start, y_point_start, start_text, plot, start_bound_name, line_color, rel_tol, abs_tol)
    plot_list.append(start_bound_name)

    end_text = symbbox.get_str_from_func(sign * symbbox.round_expr(func.subs(symb_to_plot_over, l_val), 2))
    x_point_end = x_vals[-2]
    y_point_end = y_vals[-2]
    end_bound_name = "bound_end_" + prhlp.get_id_from_knots(start_knot, end_knot)
    plot_bound_val(curr_doc, x_point_end, y_point_end, end_text, plot, end_bound_name, line_color, rel_tol, abs_tol)
    plot_list.append(end_bound_name)

    # EXTREMA VALUES
    if not func_is_const(func, symb_to_plot_over):
        # print("EXTREME VALUES")
        diff_func_without_symbs = diff(func_without_free_symbs, symb_to_plot_over)
        roots = gc.get_real_roots(diff_func_without_symbs, symb_to_plot_over)
        i = 0
        for root in roots:
            if 0 < root < kn_dist:
                diff_text = symbbox.get_str_from_func(sign * symbbox.round_expr(func.subs(symb_to_plot_over, root * len_symbol), 2))
                x_point = x_vals[0] + float(root)
                y_point = float(func_without_free_symbs.subs(symb_to_plot_over, root))*multipl_factor + y_vals[0]
                x_point, y_point = gc.rotate_x_y_values(x_point, y_point, start_knot, end_knot)
                # print_charac_val_to_console(diff_text, x_point, y_point)
                if plot in curr_doc.plot_data.char_vals_dict:
                    points_to_check = curr_doc.plot_data.char_vals_dict[plot]
                    # if gc.is_close_position(x_point, y_point, points_to_check, rel_tol, abs_tol):
                    #     continue
                diff_name = "extreme_val_" + prhlp.get_id_from_knots(start_knot, end_knot) + str(i)
                plot.text([x_point], [y_point], [" " + str(diff_text)], text_color=line_color,
                          text_font_size='1.3em', text_align='left', text_alpha=0, name=diff_name)
                add_el_to_dict(curr_doc.plot_data.char_vals_dict, plot, LinePlot.PointCol(x_point, y_point))
                add_el_to_dict(curr_doc.plot_data.extreme_vals_dict, plot, diff_name)
                plot_list.append(diff_name)

                ex_cross_name = "cross_ex_" + prhlp.get_id_from_knots(start_knot, end_knot) + str(i)
                plot.cross([x_point], [y_point], angle=1/m.sqrt(2), size=15, color=line_color,
                           line_width=3, line_alpha=0, name=ex_cross_name)
                add_el_to_dict(curr_doc.plot_data.extreme_vals_cross_dict, plot, ex_cross_name)
                plot_list.append(ex_cross_name)
                i += 1

    # ZERO CROSSING VALUES
    i = 0
    if not func_is_const(func, symb_to_plot_over):
        roots = gc.get_real_roots(func_without_free_symbs, symb_to_plot_over)
        for root in roots:
            if 0 < root < kn_dist:
                zero_cross_text = symbbox.get_str_from_func(root * kn_dist * len_symbol)
                x_point = x_vals[0] + root
                y_point = y_vals[0] + 0
                x_point, y_point = gc.rotate_x_y_values(x_point, y_point, start_knot, end_knot)
                # print_charac_val_to_console(zero_cross_text, x_point, y_point)
                if plot in curr_doc.plot_data.char_vals_dict:
                    points_to_check = curr_doc.plot_data.char_vals_dict[plot]
                    # if gc.is_close_position(x_point, y_point, points_to_check, rel_tol, abs_tol):
                    #     continue
                zero_cross_name = "zero_cross_val_" + prhlp.get_id_from_knots(start_knot, end_knot) + str(i)
                plot.text([x_point], [y_point], ["(" + str(zero_cross_text) + ", 0)"],
                          text_color=line_color, text_font_size='1.3em', text_align='left', text_alpha=0, name=zero_cross_name)
                add_el_to_dict(curr_doc.plot_data.char_vals_dict, plot, LinePlot.PointCol(x_point, y_point))
                add_el_to_dict(curr_doc.plot_data.zero_cross_dict, plot, zero_cross_name)
                plot_list.append(zero_cross_name)

                zero_cross_cross_name = "cross_zero_cross_" + prhlp.get_id_from_knots(start_knot, end_knot) + str(i)
                plot.cross([x_point], [y_point], angle=1 / m.sqrt(2), size=15, color=line_color,
                           line_width=3, line_alpha=0, name=zero_cross_cross_name)
                add_el_to_dict(curr_doc.plot_data.zero_cross_cross_dict, plot, zero_cross_cross_name)
                plot_list.append(zero_cross_cross_name)
                i += 1


def plot_output_functions(curr_doc: CurrentDoc, function_list, knot_list, symb_to_plot_over, l_list):
    """
    Plots all functions to the related plots and calculates the characteristic values
    :param plot_list: list of plots the function shell be added to
    :param function_list: list of list of all resulting functions
            [[norm_f_beam1, norm_d_beam1, ...], ... , [norm_f_beam_n, norm_d_beam_n, ...]]
    :param knot_list: list of knots being used in the system
    :param symb_to_plot_over: running variable
    :param l_list: list of all length values for the given element
    :return:
    """
    plot_list = curr_doc.plot_list
    num_plots = 6
    norm_f_funcs = []
    norm_disp_func = []
    shear_f_funcs = []
    moment_funcs = []
    shear_disp_funcs = []
    shear_angle_funcs = []
    for funcs in function_list:
        norm_f_funcs.append(funcs[0])
        norm_disp_func.append(funcs[1])
        shear_f_funcs.append(funcs[2])
        moment_funcs.append(funcs[3])
        shear_angle_funcs.append(funcs[4])
        shear_disp_funcs.append(funcs[5])
    
    # RESET PLOTS
    for i in range(num_plots):
        curr_doc.plot_data.reset_plot(plot_list[i], curr_doc.plot_data.plot_el_lists[i])
    
    # PLOT STRUCTURES
    print("Plot structure")
    for i in range(num_plots):
        plot_structure_from_knots(plot_list[i], knot_list, curr_doc.plot_data.plot_el_lists[i])

    xy_data = []
    y_max = []
    for i in range(0, num_plots):
        xy_data.extend([[]])
        y_max.extend([[]])

    for i in range(0, len(function_list)):
        l_val = l_list[i]
        x_vals, y_vals, res = calc_xy(norm_f_funcs[i],      symb_to_plot_over, l_val, knot_list[i][0], knot_list[i][1])
        xy_data[0].extend([[x_vals, y_vals]])
        if res:
            y_max[0].append(max(abs(y_vals)))

        x_vals, y_vals, res = calc_xy(norm_disp_func[i],    symb_to_plot_over, l_val, knot_list[i][0], knot_list[i][1])
        xy_data[1].extend([[x_vals, y_vals]])
        if res:
            y_max[1].append(max(abs(y_vals)))
        
        x_vals, y_vals, res = calc_xy(shear_f_funcs[i],     symb_to_plot_over, l_val, knot_list[i][0], knot_list[i][1])
        xy_data[2].extend([[x_vals, y_vals]])
        if res:
            y_max[2].append(max(abs(y_vals)))
        
        x_vals, y_vals, res = calc_xy(moment_funcs[i],      symb_to_plot_over, l_val, knot_list[i][0], knot_list[i][1])
        xy_data[3].extend([[x_vals, y_vals]])
        if res:
            y_max[3].append(max(abs(y_vals)))
        
        x_vals, y_vals, res = calc_xy(shear_disp_funcs[i],  symb_to_plot_over, l_val, knot_list[i][0], knot_list[i][1])
        xy_data[4].extend([[x_vals, y_vals]])
        if res:
            y_max[4].append(max(abs(y_vals)))
        
        x_vals, y_vals, res = calc_xy(shear_angle_funcs[i], symb_to_plot_over, l_val, knot_list[i][0], knot_list[i][1])
        xy_data[5].extend([[x_vals, y_vals]])
        if res:
            y_max[5].append(max(abs(y_vals)))

    for i in range(0, num_plots):
        if len(y_max[i]) != 0:
            y_max[i] = max(y_max[i])
        else:
            y_max[i] = 0

    plot_ind = 0
    for i in range(0, len(function_list)):
        l_val = l_list[i]
        col = htmlcol.plot_cols[plot_ind].value
        x_vals, y_vals, multipl_factor = plot_symbolic_func(plot_list[0], norm_f_funcs[i],      symb_to_plot_over, l_val, knot_list[i][0], knot_list[i][1], xy_data[0][i] , y_max[0], curr_doc.plot_data.plot_el_lists[0], line_color=col)
        plot_characteristic_vals(curr_doc, plot_list[0], norm_f_funcs[i],      symb_to_plot_over, l_val, knot_list[i][0], knot_list[i][1], x_vals, y_vals, multipl_factor, curr_doc.plot_data.plot_el_lists[0], line_color=col)

        x_vals, y_vals, multipl_factor = plot_symbolic_func(plot_list[1], norm_disp_func[i],    symb_to_plot_over, l_val, knot_list[i][0], knot_list[i][1], xy_data[1][i] , y_max[1], curr_doc.plot_data.plot_el_lists[1], line_color=col)
        plot_characteristic_vals(curr_doc, plot_list[1], norm_disp_func[i],    symb_to_plot_over, l_val, knot_list[i][0], knot_list[i][1], x_vals, y_vals, multipl_factor, curr_doc.plot_data.plot_el_lists[1], line_color=col)

        x_vals, y_vals, multipl_factor = plot_symbolic_func(plot_list[2], shear_f_funcs[i],     symb_to_plot_over, l_val, knot_list[i][0], knot_list[i][1], xy_data[2][i] , y_max[2], curr_doc.plot_data.plot_el_lists[2], line_color=col)
        plot_characteristic_vals(curr_doc, plot_list[2], shear_f_funcs[i],     symb_to_plot_over, l_val, knot_list[i][0], knot_list[i][1], x_vals, y_vals, multipl_factor, curr_doc.plot_data.plot_el_lists[2], line_color=col)

        x_vals, y_vals, multipl_factor = plot_symbolic_func(plot_list[3], moment_funcs[i],      symb_to_plot_over, l_val, knot_list[i][0], knot_list[i][1], xy_data[3][i] , y_max[3], curr_doc.plot_data.plot_el_lists[3], line_color=col)
        plot_characteristic_vals(curr_doc, plot_list[3], moment_funcs[i],      symb_to_plot_over, l_val, knot_list[i][0], knot_list[i][1], x_vals, y_vals, multipl_factor, curr_doc.plot_data.plot_el_lists[3], mirror_y_values=True, line_color=col)

        x_vals, y_vals, multipl_factor = plot_symbolic_func(plot_list[4], shear_disp_funcs[i],  symb_to_plot_over, l_val, knot_list[i][0], knot_list[i][1], xy_data[4][i] , y_max[4], curr_doc.plot_data.plot_el_lists[4], line_color=col)
        plot_characteristic_vals(curr_doc, plot_list[4], shear_disp_funcs[i],  symb_to_plot_over, l_val, knot_list[i][0], knot_list[i][1], x_vals, y_vals, multipl_factor, curr_doc.plot_data.plot_el_lists[4], line_color=col)

        x_vals, y_vals, multipl_factor = plot_symbolic_func(plot_list[5], shear_angle_funcs[i], symb_to_plot_over, l_val, knot_list[i][0], knot_list[i][1], xy_data[5][i] , y_max[5], curr_doc.plot_data.plot_el_lists[5], line_color=col)
        plot_characteristic_vals(curr_doc, plot_list[5], shear_angle_funcs[i], symb_to_plot_over, l_val, knot_list[i][0], knot_list[i][1], x_vals, y_vals, multipl_factor, curr_doc.plot_data.plot_el_lists[5], mirror_y_values=True, line_color=col)
        plot_ind += 1
        if plot_ind >= len(htmlcol.plot_cols):
            plot_ind = 0


if __name__ == '__main__':
    x = Symbol('x')
    y = Symbol('y')
    n1 = Symbol('N_1')
    func = 2*x**2 + x*y + 2*n1**(3*x)
    func2 = 2*y
    if func_is_const(func2, x):
        print("Const in x direction")
    if func_is_const(func2, y):
        print("Const in y direction")

    print("Function before substitution")
    pprint(func)
    func_small = symbbox.remove_free_symbols(func, x)
    print("Function after substitution")
    pprint(func_small)
    # TODO function subs works not properly (see Term 2*n1**(3*x), should be 2^x (for further refactoring)
