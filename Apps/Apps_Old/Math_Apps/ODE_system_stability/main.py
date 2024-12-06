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

from bokeh.models import ColumnDataSource, TextInput, Dropdown
from bokeh.layouts import widgetbox, row, column
from bokeh.plotting import Figure
from bokeh.io import curdoc

import numpy as np

import odesystem_settings
import odesystem_helpers
import sys
#import os.path
#from os.path import dirname, split
#sys.path.append(
#    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import pathlib
app_base_path = pathlib.Path(__file__).resolve().parents[0]
sys.path.append(
    pathlib.Path(__file__).resolve().parents[1])
import my_bokeh_utils

global update_callback
update_callback = True

# initialize data source
source_streamline = ColumnDataSource(data=dict(x=[], y=[]))  # streamline data
source_initialvalue = ColumnDataSource(data=dict(x0=[], y0=[]))  # initial value data (only one point)
source_critical_pts = ColumnDataSource(data=dict(x=[], y=[]))  # critical point data (multiple points)
source_critical_lines = ColumnDataSource(data=dict(x_ls=[[]], y_ls=[[]]))  # critical line data (multiple sets of points connecting to lines)
source_view = ColumnDataSource(data=dict(x_start=[odesystem_settings.x_min],
                                         x_end=[odesystem_settings.x_max],
                                         y_start=[odesystem_settings.y_min],
                                         y_end=[odesystem_settings.y_max]))  # user view information


def init_data():
    """
    initializes the data.
    1. get the ode function components u and v
    2. get the initial value for the streamline
    3. compute quiver and streamline
    :return:
    """
    u_str = u_input.value
    v_str = v_input.value
    x0 = odesystem_settings.x0_input_init
    y0 = odesystem_settings.y0_input_init
    update_quiver_data(u_str, v_str)
    update_streamline_data(u_str, v_str, x0, y0)
    interactor.update_to_user_view()


def ode_change(attrname, old, new):
    """
    called, if the ode changes, i.e. one of the function u or v is modified. If the ode changes the quiver field as well
    as the streamline change. Additionally the global boolean value update_callback has to be set (this value is used
    for preventing unnecessary computation if both u and v are changed at the same time).
    :param attrname:
    :param old:
    :param new:
    :return:
    """
    global update_callback
    if update_callback:
        u_str = u_input.value
        v_str = v_input.value
        x0 = source_initialvalue.data['x0'][0]
        y0 = source_initialvalue.data['y0'][0]
        update_quiver_data(u_str, v_str)
        update_streamline_data(u_str, v_str, x0, y0)


def initial_value_change(attrname, old, new):
    """
    called, if the initial value for the streamline changes. The streamline has to by recomputed.
    :param attrname:
    :param old:
    :param new:
    :return:
    """
    u_str = u_input.value
    v_str = v_input.value
    x0, y0 = interactor.clicked_point()
    update_streamline_data(u_str, v_str, x0, y0)


def get_plot_bounds(plot):
    """
    helper function returning the bounds of the plot in a dict.
    :param plot: handle to the bokeh.plotting.Figure
    :return:
    """
    x_min = plot.x_range.start
    x_max = plot.x_range.end
    y_min = plot.y_range.start
    y_max = plot.y_range.end
    return {'x_min':x_min,
            'x_max':x_max,
            'y_min':y_min,
            'y_max':y_max}


def update_streamline_data(u_str, v_str, x0, y0):
    """
    updates the bokeh.models.ColumnDataSource holding the streamline data.
    :param u_str: string, first component of the ode
    :param v_str: string, second component of the ode
    :param x0: initial value x for the streamline
    :param y0: initial value y for the streamline
    :return:
    """
    # string parsing
    u_fun, u_sym = my_bokeh_utils.string_to_function_parser(u_str,['x','y'])
    v_fun, v_sym = my_bokeh_utils.string_to_function_parser(v_str,['x','y'])
    # numerical integration
    chaotic = (sample_fun_input.value == "dixon") # for the dixon system a special treatment is necessary
    x_val, y_val = odesystem_helpers.do_integration(x0, y0, u_fun, v_fun, get_plot_bounds(plot), chaotic)
    # update sources
    streamline_to_data(x_val, y_val, x0, y0) # save data to ColumnDataSource
    print("streamline was calculated for initial value (x0,y0)=({:f},{:f})".format(x0, y0))


def update_quiver_data(u_str, v_str):
    """
    updates the bokeh.models.ColumnDataSource_s holding the quiver data and the ciritical points and lines of the ode.
    :param u_str: string, first component of the ode
    :param v_str: string, second component of the ode
    :return:
    """
    # string parsing
    u_fun, u_sym = my_bokeh_utils.string_to_function_parser(u_str,['x','y'])
    v_fun, v_sym = my_bokeh_utils.string_to_function_parser(v_str,['x','y'])
    # compute critical points
    x_c, y_c, x_lines, y_lines = odesystem_helpers.critical_points(u_sym, v_sym, get_plot_bounds(plot))
    # crating samples
    x_val, y_val, u_val, v_val, h = get_samples(u_fun, v_fun)
    # update quiver w.r.t. samples
    quiver.compute_quiver_data(x_val, y_val, u_val, v_val, normalize=True)
    # save critical point data
    critical_to_data(x_c, y_c, x_lines, y_lines)

    print("quiver data was updated for u(x,y) = {}, v(x,y) = {}".format(u_str, v_str))


def get_samples(u_fun, v_fun):
    """
    compute sample points where the ode is evaluated.
    :param u_fun: function handle, first component of the ode
    :param v_fun: function handle, second component of the ode
    :return:
    """
    # create a grid of samples
    xx, hx = np.linspace(source_view.data['x_start'][0], source_view.data['x_end'][0], odesystem_settings.n_sample, retstep=True)
    yy, hy = np.linspace(source_view.data['y_start'][0], source_view.data['y_end'][0], odesystem_settings.n_sample, retstep=True)
    x_val, y_val = np.meshgrid(xx, yy)
    # evaluate ode
    u_val = u_fun(x_val, y_val)
    v_val = v_fun(x_val, y_val)
    # detect nan values and eliminate them
    u_val[u_val != u_val] = 0
    v_val[v_val != v_val] = 0
    # detect inf values and make them finite
    u_val[u_val == np.inf] =  10**10
    v_val[v_val == np.inf] =  10**10
    u_val[u_val == -np.inf] = -10 ** 10
    v_val[v_val == -np.inf] = -10 ** 10

    return x_val, y_val, u_val, v_val, hx


def streamline_to_data(x_val, y_val, x0, y0):
    """
    save streamline to bokeh.models.ColumnDataSource
    :param x_val: streamline data x
    :param y_val: streamline data y
    :param x0: initial value x of streamline
    :param y0: initial value y of streamline
    :return:
    """
    source_initialvalue.data = dict(x0=[x0], y0=[y0])
    source_streamline.data = dict(x=x_val, y=y_val)


def critical_to_data(x_c, y_c, x_lines, y_lines):
    """
    save critical points and lines to bokeh.models.ColumnDataSource
    :param x_c: critical points x
    :param y_c: critical points y
    :param x_lines: set of lines (multiple points x)
    :param y_lines: set of lines (multiple points y)
    :return:
    """
    source_critical_pts.data = dict(x=x_c, y=y_c)
    source_critical_lines.data = dict(x_ls=x_lines, y_ls=y_lines)


def sample_fun_change(attr, old, new):
    """
    called if the sample function is changed. The global variable update_callback is used to prevent triggering the
    callback function ode_change twice, once for change in u with old v, then for change in v with new u.
    :param self:
    :return:
    """
    global update_callback
    # get sample function pair (first & second component of ode)
    sample_fun_key = new #sample_fun_input.value
    sample_fun_u, sample_fun_v = odesystem_settings.sample_system_functions[sample_fun_key]
    # write new functions to u_input and v_input
    update_callback = False  # prevent callback
    u_input.value = sample_fun_u
    update_callback = True  # allow callback
    v_input.value = sample_fun_v


def refresh_user_view():
    """
    periodically called function that updates data with respect to the current user view, if the user view has changed.
    :return:
    """
    user_view_has_changed = my_bokeh_utils.check_user_view(source_view.data, plot)
    if user_view_has_changed:
        u_str = u_input.value
        v_str = v_input.value
        x_mark = source_initialvalue.data['x0'][0]
        y_mark = source_initialvalue.data['y0'][0]
        update_quiver_data(u_str, v_str)
        update_streamline_data(u_str, v_str, x_mark, y_mark)
        source_view.data = my_bokeh_utils.get_user_view(plot)
        interactor.update_to_user_view()


# initialize plot
toolset = "crosshair,pan,reset,save,wheel_zoom,tap"
# Generate a figure container
plot = Figure(plot_height=400,
              plot_width=400,
              tools=toolset,
              title="2D ODE System",
              x_range=[odesystem_settings.x_min, odesystem_settings.x_max],
              y_range=[odesystem_settings.y_min, odesystem_settings.y_max]
              )
# remove grid from plot
plot.grid[0].grid_line_alpha = 0.0
plot.grid[1].grid_line_alpha = 0.0

# Plot the direction field
quiver = my_bokeh_utils.Quiver(plot)
# Plot initial values
plot.scatter('x0', 'y0', source=source_initialvalue, color='black', legend_label='(x0,y0)')
# Plot streamline
plot.line('x', 'y', source=source_streamline, color='black', legend_label='streamline')
# Plot critical points and lines
plot.scatter('x', 'y', source=source_critical_pts, color='red', legend_label='critical pts')
plot.multi_line('x_ls', 'y_ls', source=source_critical_lines, color='red', legend_label='critical lines')

# initialize controls
# text input for input of the ode system [u,v] = [x',y']
u_input = TextInput(value=odesystem_settings.sample_system_functions[odesystem_settings.init_fun_key][0], title="u(x,y):")
v_input = TextInput(value=odesystem_settings.sample_system_functions[odesystem_settings.init_fun_key][1], title="v(x,y):")

# dropdown menu for selecting one of the sample functions
sample_fun_input = Dropdown(label="choose a sample function pair or enter one below",
                            menu=odesystem_settings.sample_system_names)

# Interactor for entering starting point of initial condition
interactor = my_bokeh_utils.Interactor(plot)

# initialize callback behaviour
sample_fun_input.on_change('value', sample_fun_change)
u_input.on_change('value', ode_change)
v_input.on_change('value', ode_change)
interactor.on_click(initial_value_change)

# calculate data
init_data()

# lists all the controls in our app associated with the default_funs panel
function_controls = widgetbox(sample_fun_input, u_input, v_input,width=400)

# refresh quiver field and streamline all 100ms
curdoc().add_periodic_callback(refresh_user_view, 100)
# make layout
curdoc().add_root(row(function_controls, plot))
curdoc().title = str(app_base_path.relative_to(app_base_path.parent)).replace("_"," ").replace("-"," ")  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
