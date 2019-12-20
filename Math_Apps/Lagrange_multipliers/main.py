"""
Created on Sat Jul 11 22:04:14 2015

@author: benjamin
"""
# ==============================================================================
# This file demonstrates a bokeh applet. The applet has been designed at TUM
# for educational purposes. The structure of the following code bases to large
# part on the work published on
# https://github.com/bokeh/bokeh/tree/master/examples
# ==============================================================================

import logging

logging.basicConfig(level=logging.DEBUG)

from bokeh.models.widgets import TextInput, Dropdown
from bokeh.models import ColumnDataSource
from bokeh.layouts import widgetbox, row
from bokeh.plotting import Figure
from bokeh.io import curdoc

from os.path import dirname, split

import numpy as np

import lagrange_settings
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import my_bokeh_utils


# initialize data source
source_mark = ColumnDataSource(data=dict(x=[], y=[]))
source_view = ColumnDataSource(data=dict(x_start=[lagrange_settings.x_min],
                                         x_end=[lagrange_settings.x_max],
                                         y_start=[lagrange_settings.y_min],
                                         y_end=[lagrange_settings.y_max]))  # user view information


def init_data():
    """
    initializes the plots and interactor
    """
    f, _ = my_bokeh_utils.string_to_function_parser(f_input.value, ['x', 'y'])
    contour_f.compute_contour_data(f)
    g, _ = my_bokeh_utils.string_to_function_parser(g_input.value, ['x', 'y'])
    contour_g.compute_contour_data(g, isovalue=[0])
    interactor.update_to_user_view()


def get_samples(df, x0, y0):
    """
    compues the relevant data for the gradient plot
    :param df: function to be evaluated
    :param x0: base point x
    :param y0: base point y
    :return: samples of df on x0, y0
    """
    dfx_val, dfy_val = df(x0, y0)
    return np.array(x0), np.array(y0), np.array(dfx_val), np.array(dfy_val)


def on_selection_change(attr, old, new):
    """
    called if the by click selected point changes
    """
    # detect clicked point
    x_coor, y_coor = interactor.clicked_point()

    if x_coor is not None:
        # get constraint function
        g, _ = my_bokeh_utils.string_to_function_parser(g_input.value, ['x', 'y'])
        # project point onto constraint
        x_close, y_close = my_bokeh_utils.find_closest_on_iso(x_coor, y_coor, g)
        # save to mark
        source_mark.data = dict(x=[x_close], y=[y_close])
        # update influenced data
        compute_click_data()


def compute_click_data():
    """
    computes relevant data for the position clicked on:
    1. gradients of objective function f(x,y) and constraint function g(x,y)
    2. contour lines running through click location
    """
    # get objective function and constraint function
    f, f_sym = my_bokeh_utils.string_to_function_parser(f_input.value, ['x', 'y'])
    g, g_sym = my_bokeh_utils.string_to_function_parser(g_input.value, ['x', 'y'])
    # compute gradients
    df, _ = my_bokeh_utils.compute_gradient(f_sym, ['x', 'y'])
    dg, _ = my_bokeh_utils.compute_gradient(g_sym, ['x', 'y'])
    # compute isovalue on click location
    x_mark = source_mark.data['x'][0]
    y_mark = source_mark.data['y'][0]
    isovalue = f(x_mark, y_mark)
    # update contour running through isovalue
    contour_f0.compute_contour_data(f, [isovalue])
    # save gradient data
    h = (source_view.data['x_end'][0] - source_view.data['x_start'][0]) / 5.0
    x, y, u, v = get_samples(df, x_mark, y_mark)
    quiver_isolevel.compute_quiver_data(x, y, u, v, h=h, scaling=1)
    x, y, u, v = get_samples(dg, x_mark, y_mark)
    quiver_constraint.compute_quiver_data(x, y, u, v, h=h, scaling=1)


def sample_fun_input_f_changed(attr, old, new):
    """
    called if the sample function is changed.
    :param self:
    :return:
    """
    sample_fun_key = new #sample_fun_input_f.value
    sample_fun_f = lagrange_settings.sample_functions_f[sample_fun_key]
    # write new functions to f_input, this triggers the callback of f_input
    f_input.value = sample_fun_f


def sample_fun_input_g_changed(attr, old, new):
    """
    called if the sample function is changed.
    :param self:
    :return:
    """
    sample_fun_key = new #sample_fun_input_g.value
    sample_fun_g = lagrange_settings.sample_functions_g[sample_fun_key]
    # write new functions to g_input, this triggers the callback of f_input
    g_input.value = sample_fun_g


def f_changed(attr, old, new):
    """
    called if f input function changes
    """
    # get new functions
    f, _ = my_bokeh_utils.string_to_function_parser(f_input.value, ['x', 'y'])
    # has any point been marked?
    if len(source_mark.data['x']) > 0: # projected point does not change, just recompute isocontour on f
        compute_click_data()
    # update contour data
    contour_f.compute_contour_data(f)


def g_changed(attr, old, new):
    """
    called if g input function changes
    """
    # get new functions
    g, _ = my_bokeh_utils.string_to_function_parser(g_input.value, ['x', 'y'])
    # has any point been marked?
    if len(source_mark.data['x']) > 0: # use clicked on point to recompute projection and recompute isocontour on f
        on_selection_change(None,None,None)
    # update contour data
    contour_g.compute_contour_data(g, isovalue=[0])


def refresh_contour():
    """
    periodically called function that updates data with respect to the current user view, if the user view has changed.
    """
    user_view_has_changed = my_bokeh_utils.check_user_view(source_view.data, plot)
    if user_view_has_changed:
        f, _ = my_bokeh_utils.string_to_function_parser(f_input.value, ['x', 'y'])
        g, _ = my_bokeh_utils.string_to_function_parser(g_input.value, ['x', 'y'])

        if len(source_mark.data['x']) > 0:  # has any point been marked?
            compute_click_data()

        contour_f.compute_contour_data(f)
        contour_g.compute_contour_data(g, [0])
        interactor.update_to_user_view()
        source_view.data = my_bokeh_utils.get_user_view(plot)


# initialize plot
toolset = ["crosshair,pan,save,wheel_zoom,tap"]
# Generate a figure container for the field
plot = Figure(plot_height=lagrange_settings.res_x,
              plot_width=lagrange_settings.res_y,
              tools=toolset,
              title="Optimization with side condition",
              x_range=[lagrange_settings.x_min, lagrange_settings.x_max],
              y_range=[lagrange_settings.y_min, lagrange_settings.y_max])

# Plot contour of f(x,y)
contour_f = my_bokeh_utils.Contour(plot, line_color='grey', line_width=1)
# Plot active isolevel f(x,y)=v
contour_f0 = my_bokeh_utils.Contour(plot, add_label=True, line_color='black', line_width=2, legend_label='f(x,y) = v')
# Plot constraint function contour g(x,y)=0
contour_g = my_bokeh_utils.Contour(plot, line_color='red', line_width=2, legend_label='g(x,y) = 0')
# Plot corresponding tangent vector
quiver_isolevel = my_bokeh_utils.Quiver(plot, fix_at_middle=False, line_width=2, color='black')
# Plot corresponding tangent vector
quiver_constraint = my_bokeh_utils.Quiver(plot, fix_at_middle=False, line_width=2, color='red')
# Plot mark at position on constraint function
plot.cross(x='x', y='y', color='red', size=10, line_width=2, source=source_mark)

# object that detects, if a position in the plot is clicked on
interactor = my_bokeh_utils.Interactor(plot)
# adds callback function to interactor, if position in plot is clicked, call on_selection_change
interactor.on_click(on_selection_change)

# text input window for objective function f(x,y) to be optimized
f_input = TextInput(value=lagrange_settings.f_init, title="f(x,y):")
f_input.on_change('value', f_changed)

# dropdown menu for selecting one of the sample functions
sample_fun_input_f = Dropdown(label="choose a sample function f(x,y) or enter one below",
                              menu=lagrange_settings.sample_f_names)
sample_fun_input_f.on_change('value', sample_fun_input_f_changed)

# text input window for side condition g(x,y)=0
g_input = TextInput(value=lagrange_settings.g_init, title="g(x,y):")
g_input.on_change('value', g_changed)

# dropdown menu for selecting one of the sample functions
sample_fun_input_g = Dropdown(label="choose a sample function g(x,y) or enter one below",
                              menu=lagrange_settings.sample_g_names)
sample_fun_input_g.on_change('value', sample_fun_input_g_changed)

# calculate data
init_data()

# refresh quiver field all 100ms
curdoc().add_periodic_callback(refresh_contour, 100)
# make layout
curdoc().add_root(row(plot,widgetbox(sample_fun_input_f,f_input,sample_fun_input_g,g_input)))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
