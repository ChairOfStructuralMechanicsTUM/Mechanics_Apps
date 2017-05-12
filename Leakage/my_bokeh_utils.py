from __future__ import division
import bokeh
from sympy import sympify, lambdify, diff
import numpy as np


def check_user_view(view_data, plot):
    """
    checks for a change in the user view that affects the plotting
    :param view_data: dict containing the current view data
    :param plot: handle to the plot
    :return: bool that states if any relevant parameter has been changed
    """
    assert type(view_data) is bokeh.core.property_containers.PropertyValueDict

    user_view_has_changed = (view_data['x_start'][0] != plot.x_range.start) or \
                            (view_data['x_end'][0] != plot.x_range.end) or \
                            (view_data['y_start'][0] != plot.y_range.start) or \
                            (view_data['y_end'][0] != plot.y_range.end)

    return user_view_has_changed


def get_user_view(plot):
    """
    returns the current user view of the plot
    :param plot: a bokeh.plotting.Figure
    :return: a dict that can be used for a bokeh.models.ColumnDataSource
    """
    x_start = plot.x_range.start  # origin x
    y_start = plot.y_range.start  # origin y
    x_end = plot.x_range.end  # final x
    y_end = plot.y_range.end  # final y

    return dict(x_start=[x_start], y_start=[y_start], x_end=[x_end], y_end=[y_end])


def string_to_function_parser(fun_str, args):
    """
    converts a string to a lambda function.
    :param fun_str: string representation of the function
    :param args: symbolic arguments that will be turned into lambda function arguments
    :return:
    """

    fun_sym = sympify(fun_str)
    fun_lam = sym_to_function_parser(fun_sym, args)

    return fun_lam, fun_sym


def sym_to_function_parser(fun_sym, args):
    """
    converts a symbolic expression to a lambda function. The function handles constant and zero symbolic input such that
    on numpy.array input a numpy.array with identical size is returned.
    :param fun_sym: symbolic expression
    :param args: symbols turned into function input arguments
    :return:
    """

    if fun_sym.is_constant():
        fun_lam = lambda *x: np.ones_like(x[0]) * float(fun_sym)
    else:
        fun_lam = lambdify(args, fun_sym, modules=['numpy'])

    return fun_lam


def compute_gradient(fun_sym, args):
    """
    computes the gradient of fun_sym w.r.t. every symbol in args
    :param fun_sym: scalar function
    :param args: arguments to build derivatives
    :return:
    """
    df_sym = []
    for s in args:
        dfds_sym = diff(fun_sym, s)
        df_sym.append(sym_to_function_parser(dfds_sym, args))
    df = lambda x, y: [_(x, y) for _ in df_sym]

    return df, df_sym