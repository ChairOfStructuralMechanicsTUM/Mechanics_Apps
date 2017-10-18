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

from bokeh.models.widgets import Slider, TextInput, Panel, Tabs, Dropdown
from bokeh.models import ColumnDataSource
from bokeh.layouts import row, column, widgetbox
from bokeh.plotting import Figure
from bokeh.io import curdoc

import numpy as np

import curveintegral_settings
import sys
import os.path
from os.path import dirname, split
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import my_bokeh_utils

# initialize data source
source_patches = ColumnDataSource(data=dict(xs=[], ys=[]))  # patches defining the arrow tips of the quiver plot
source_segments = ColumnDataSource(
    data=dict(x0=[], y0=[], x1=[], y1=[]))  # segments defining the arrow lines of the quiver plot
source_basept = ColumnDataSource(
    data=dict(x=[], y=[]))  # points lying in the middle of each arrow defining the point the arrow is referring to
source_curve = ColumnDataSource(data=dict(x=[], y=[]))  # curve
source_param = ColumnDataSource(data=dict(x=[], y=[], t=[], x0=[], y0=[], x1=[], y1=[], xs=[], ys=[]))
source_integral = ColumnDataSource(data=dict(t=[], integral=[], integrand=[]))  # integrand and integral value w.r.t. parameter t
source_view = ColumnDataSource(data=dict(x_start=[curveintegral_settings.x_min],
                                         x_end=[curveintegral_settings.x_max],
                                         y_start=[curveintegral_settings.y_min],
                                         y_end=[curveintegral_settings.y_max]))  # user view information


def init_data():
    u_str = u_input.value
    v_str = v_input.value
    cx_str = cx_input.value
    cy_str = cy_input.value
    t = parameter_input.value
    update_quiver_data(u_str, v_str)
    update_curve_data(cx_str, cy_str)
    update_parameter_data(cx_str, cy_str, t)
    update_integral_data(u_str, v_str, cx_str, cy_str)


def update_curve_data(cx_str, cy_str):
    # string parsing
    cx_fun, _ = my_bokeh_utils.string_to_function_parser(cx_str, ['t'])
    cy_fun, _ = my_bokeh_utils.string_to_function_parser(cy_str, ['t'])
    # crating samples
    t_range = np.linspace(0, 1)
    x_val = cx_fun(t_range)
    y_val = cy_fun(t_range)
    # save data
    source_curve.data = dict(x=x_val, y=y_val)

    print "curve data was updated with c(t)=[%s,%s]" % (cx_str, cy_str)


def update_parameter_data(cx_str, cy_str, t):
    # string parsing
    cx_fun, cx_sym = my_bokeh_utils.string_to_function_parser(cx_str, ['t'])
    cy_fun, cy_sym = my_bokeh_utils.string_to_function_parser(cy_str, ['t'])

    from sympy import diff

    dcx_sym = diff(cx_sym, 't')
    dcy_sym = diff(cy_sym, 't')

    dcx_fun = my_bokeh_utils.sym_to_function_parser(dcx_sym, 't')
    dcy_fun = my_bokeh_utils.sym_to_function_parser(dcy_sym, 't')

    # crating sample
    x_val = cx_fun(t)
    y_val = cy_fun(t)

    dx_val = dcx_fun(t)
    dy_val = dcy_fun(t)
    xx, hx = np.linspace(source_view.data['x_start'][0], source_view.data['x_end'][0], curveintegral_settings.n_sample,
                         retstep=True)
    ssdict, spdict, _ = my_bokeh_utils.quiver_to_data(x=np.array(x_val), y=np.array(y_val), u=np.array(dx_val), v=np.array(dy_val), h=2*hx,
                                                           do_normalization=True, fix_at_middle=False)

    # save data
    source_param.data = dict(x=[x_val], y=[y_val], t=[t], x0=ssdict['x0'], y0=ssdict['y0'],
                             x1=ssdict['x1'], y1=ssdict['y1'], xs=spdict['xs'], ys=spdict['ys'])

    print "curve point was updated with t=%f" % (t)


def update_quiver_data(u_str, v_str):
    """
    updates the bokeh.models.ColumnDataSource_s holding the quiver data
    :param u_str: string, first component of the vector values function
    :param v_str: string, second component of the vector values function
    :return:
    """
    # string parsing
    u_fun, _ = my_bokeh_utils.string_to_function_parser(u_str, ['x', 'y'])
    v_fun, _ = my_bokeh_utils.string_to_function_parser(v_str, ['x', 'y'])
    # crating samples
    x_val, y_val, u_val, v_val, h = get_samples(u_fun, v_fun)
    # generating quiver data and updating sources
    ssdict, spdict, sbdict = my_bokeh_utils.quiver_to_data(x=x_val, y=y_val, u=u_val, v=v_val, h=h,
                                                           do_normalization=False)
    # save quiver data to respective ColumnDataSource_s
    source_segments.data = ssdict
    source_patches.data = spdict
    source_basept.data = sbdict

    print "quiver data was updated for u(x,y) = %s, v(x,y) = %s" % (u_str, v_str)


def update_integral_data(u_str, v_str, cx_str, cy_str):
    #string parsing
    u_fun, _ = my_bokeh_utils.string_to_function_parser(u_str, ['x', 'y'])
    v_fun, _ = my_bokeh_utils.string_to_function_parser(v_str, ['x', 'y'])
    cx_fun, cx_sym = my_bokeh_utils.string_to_function_parser(cx_str, ['t'])
    cy_fun, cy_sym = my_bokeh_utils.string_to_function_parser(cy_str, ['t'])

    from sympy import diff

    dcx_sym = diff(cx_sym,'t')
    dcy_sym = diff(cy_sym,'t')

    dcx_fun = my_bokeh_utils.sym_to_function_parser(dcx_sym, 't')
    dcy_fun = my_bokeh_utils.sym_to_function_parser(dcy_sym, 't')

    t = np.linspace(curveintegral_settings.parameter_min,curveintegral_settings.parameter_max)

    f_I = lambda xx, tt: (u_fun(cx_fun(tt),cy_fun(tt)) * dcx_fun(tt) + v_fun(cx_fun(tt),cy_fun(tt)) * dcy_fun(tt))

    integrand = f_I(None,t)

    from scipy.integrate import odeint

    integral = odeint(f_I,0,t)

    source_integral.data = dict(t=t.tolist(),
                                integral=integral.tolist(),
                                integrand=integrand.tolist())


def function_change(attr, old, new):
    u_str = u_input.value
    v_str = v_input.value
    cx_str = cx_input.value
    cy_str = cy_input.value
    update_quiver_data(u_str, v_str)
    update_integral_data(u_str, v_str, cx_str, cy_str)


def curve_change(attr, old, new):
    u_str = u_input.value
    v_str = v_input.value
    cx_str = cx_input.value
    cy_str = cy_input.value
    t = parameter_input.value
    update_curve_data(cx_str, cy_str)
    update_parameter_data(cx_str, cy_str, t)
    update_integral_data(u_str, v_str, cx_str, cy_str)


def parameter_change(attr, old, new):
    cx_str = cx_input.value
    cy_str = cy_input.value
    t = parameter_input.value
    update_parameter_data(cx_str, cy_str, t)


def get_samples(u_fun, v_fun):
    """
    compute sample points where the vector function is evaluated.
    :param u_fun: function handle, first component of the function
    :param v_fun: function handle, second component of the function
    :return:
    """
    # create a grid of samples
    xx, hx = np.linspace(source_view.data['x_start'][0], source_view.data['x_end'][0], curveintegral_settings.n_sample,
                         retstep=True)
    yy, hy = np.linspace(source_view.data['y_start'][0], source_view.data['y_end'][0], curveintegral_settings.n_sample,
                         retstep=True)
    x_val, y_val = np.meshgrid(xx, yy)
    # evaluate function at sample points
    u_val = u_fun(x_val, y_val)
    v_val = v_fun(x_val, y_val)

    return x_val, y_val, u_val, v_val, hx


# initialize controls
# text input for input of the vector function [fx(x,y),fy(x,y)]
u_input = TextInput(value=curveintegral_settings.sample_functions[curveintegral_settings.init_fun_key][0],
                    title="fx(x,y):")
v_input = TextInput(value=curveintegral_settings.sample_functions[curveintegral_settings.init_fun_key][1],
                    title="fy(x,y):")

u_input.on_change('value', function_change)
v_input.on_change('value', function_change)

# text input for input of the parametrized curve [cx(t),cy(t)]
cx_input = TextInput(value=curveintegral_settings.sample_curves[curveintegral_settings.init_curve_key][0],
                     title="cx(t):")
cy_input = TextInput(value=curveintegral_settings.sample_curves[curveintegral_settings.init_curve_key][1],
                     title="cy(t):")
# slider controlling the parameter t
parameter_input = Slider(title="t",
                         value=curveintegral_settings.parameter_input_init,
                         start=curveintegral_settings.parameter_min,
                         end=curveintegral_settings.parameter_max,
                         step=curveintegral_settings.parameter_step)

cx_input.on_change('value', curve_change)
cy_input.on_change('value', curve_change)
parameter_input.on_change('value', parameter_change)

# initialize plot
toolset = "crosshair,pan,reset,resize,save,wheel_zoom"
# Generate a figure container for the field
plot_field = Figure(plot_height=400,
                    plot_width=400,
                    tools=toolset,
                    title="Vector valued function",
                    x_range=[curveintegral_settings.x_min, curveintegral_settings.x_max],
                    y_range=[curveintegral_settings.y_min, curveintegral_settings.y_max]
                    )

# remove grid from plot
plot_field.grid[0].grid_line_alpha = 0.0
plot_field.grid[1].grid_line_alpha = 0.0

# Plot the direction field
plot_field.segment('x0', 'y0', 'x1', 'y1', source=source_segments)
plot_field.patches('xs', 'ys', source=source_patches)
plot_field.circle('x', 'y', source=source_basept, color='blue', size=1.5)
# Plot curve
plot_field.line('x', 'y', source=source_curve, color='black', legend='curve')
# Plot parameter point
plot_field.scatter('x', 'y', source=source_param, color='black', legend='c(t)')
# Plot corresponding tangent vector
plot_field.segment('x0', 'y0', 'x1', 'y1', source=source_param, color='black')
plot_field.patches('xs', 'ys', source=source_param, color='black')

# Generate a figure container for the integral value
plot_integral = Figure(plot_height=200,
                       plot_width=400,
                       title="Integral along curve",
                       x_range=[curveintegral_settings.parameter_min, curveintegral_settings.parameter_max],
                       y_range=[-10,10]
                       )
plot_integral.scatter('t',0, source=source_param, color='black')
plot_integral.line('t','integrand',source=source_integral, color='black')
plot_integral.line('t','integral',source=source_integral, color='red')


def refresh_quiver():
    """
    periodically called function that updates data with respect to the current user view, if the user view has changed.
    :return:
    """
    user_view_has_changed = my_bokeh_utils.check_user_view(source_view.data, plot_field)
    if user_view_has_changed:
        u_str = u_input.value
        v_str = v_input.value
        update_quiver_data(u_str, v_str)
        source_view.data = my_bokeh_utils.get_user_view(plot_field)


# calculate data
init_data()

# lists all the controls in our app associated with the default_funs panel
ww = 400
function_controls = widgetbox(u_input, v_input)
curve_controls = widgetbox(cx_input, cy_input, parameter_input)

# Panels for sample functions or default functions
function_panel = Panel(child=function_controls, title='choose function')
curve_panel = Panel(child=curve_controls, title='choose curve')
# Add panels to tabs
tabs = Tabs(tabs=[function_panel, curve_panel])

# refresh quiver field all 100ms
curdoc().add_periodic_callback(refresh_quiver, 100)
# make layout
curdoc().add_root(row(row(column(plot_field, plot_integral),
                          tabs)))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
