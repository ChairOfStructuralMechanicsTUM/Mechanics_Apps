"""
Created on Sat Jul 11 22:04:14 2015

@author: benjamin
"""

import logging
import numpy as np

from bokeh.models import ColumnDataSource, Slider, RadioButtonGroup
from bokeh.plotting import Figure
from bokeh.io import curdoc
from bokeh.layouts import row, column, widgetbox

import ode_functions as ode_fun
import ode_settings
import sys
import os.path
from os.path import dirname, split
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import my_bokeh_utils

logging.basicConfig(level=logging.DEBUG)


def compute_numerical_solution(ode_id, solver_id, x0, h):
    """
    solves a given ode numerically
    :param ode_id: identifier for the ode
    :param solver_id: identifier for the solver to be used
    :param x0: inital value for the ode
    :param h: stepwidth of the scheme
    :return: dict to be saved to bokeh.models.ColumnDataSource holding the discrete solution
    """
    # get solver to be used
    solver = ode_settings.solver_library[solver_id]
    # get ode function handle
    ode = ode_settings.ode_library[ode_id]

    if odes.active == ode_settings.oszillator_id:  # special treatment. Adding second component equal to zero.
        x0 = np.array([x0, 0])
    else:
        x0 = np.array([x0])

    t1 = source_view.data['x_end'][0]

    [t_num, x_num] = solver(ode, x0, h, t1)

    x_num = x_num[0, :]  # only take first line of solutions
    x_num = x_num.tolist()
    t_num = t_num.tolist()

    return dict(x_num=x_num, t_num=t_num)


def compute_reference_solution(ode_id, x0):
    """
    computes the reference resolution for a specific ode.
    :param ode_id: identifier for the ode, for which the reference solution is computed
    :param x0: initial value for the ode
    :return: dict to be saved to bokeh.models.ColumnDataSource holding samples of the reference solution
    """
    # get reference solution function handle
    ref = ode_settings.ref_library[ode_id]
    # get time interval to display
    t1 = source_view.data['x_end'][0]
    t0 = max([source_view.data['x_start'][0], 0])

    [t_ref, x_ref] = ode_fun.ref_sol(ref, x0, t_min=t0, t_max=t1, n_samples=ode_settings.x_res)

    x_ref = x_ref.tolist()
    t_ref = t_ref.tolist()

    return dict(x_ref=x_ref, t_ref=t_ref)


def update_ode_data(attr, old, new):
    """
    updates data for ode
    """
    source_num.data = compute_numerical_solution(odes.active, solvers.active, startvalue.value, stepsize.value)


def update_ref_data(attr, old, new):
    """
    updates data for reference solution
    """
    update_quiver_data()
    source_ref.data = compute_reference_solution(odes.active, startvalue.value)


def update_quiver_data():
    """
    updates the bokeh.models.ColumnDataSource_s holding the quiver data.
    """
    ode_id = odes.active

    ode = ode_settings.ode_library[ode_id]
    if ode_id == ode_settings.oszillator_id: # exceptional case, quiver field does not make sense!
        x_val = y_val = u_val = v_val = [0.0]
    else:
        # crating samples
        x_val, y_val, u_val, v_val, _ = get_samples(ode)

    # update quiver w.r.t. samples
    quiver.compute_quiver_data(x_val, y_val, u_val, v_val, normalize=True)


def get_samples(ode):
    """
    compute sample points where the ode is evaluated.
    :param ode: function handle, the ode
    :return: four matrices holding the x,y and the u,v grid
    """
    # create a grid of samples
    xx, hx = np.linspace(source_view.data['x_start'][0], source_view.data['x_end'][0], ode_settings.n_sample, retstep=True)
    yy, hy = np.linspace(source_view.data['y_start'][0], source_view.data['y_end'][0], ode_settings.n_sample, retstep=True)
    x_val, y_val = np.meshgrid(xx, yy)
    # evaluate ode
    v_val = ode(x_val, y_val)
    u_val = np.ones(v_val.shape)
    # detect nan values and eliminate them
    u_val[u_val != u_val] = 0
    v_val[v_val != v_val] = 0
    # detect inf values and make them finite
    u_val[u_val == np.inf] =  10**10
    v_val[v_val == np.inf] =  10**10
    u_val[u_val == -np.inf] = -10 ** 10
    v_val[v_val == -np.inf] = -10 ** 10

    return x_val, y_val, u_val, v_val, hx


def update_data(attr, old, new):
    """
    updates all data
    """
    # update ode and reference solution data
    update_ode_data(attr, old, new)
    update_ref_data(attr, old, new)
    update_quiver_data()


def init_data():
    """
    initializes data
    """
    update_data(None,None,None)


def refresh_user_view():
    """
    periodically called function that updates data with respect to the current user view, if the user view has changed.
    """
    user_view_has_changed = my_bokeh_utils.check_user_view(source_view.data, plot)
    if user_view_has_changed:
        source_view.data = my_bokeh_utils.get_user_view(plot)
        update_quiver_data()
        update_data(None, None, None)

# initialize data source
source_num = ColumnDataSource(data=dict(t_num=[], x_num=[]))
source_ref = ColumnDataSource(data=dict(t_ref=[], x_ref=[]))
source_view = ColumnDataSource(data=dict(x_start=[ode_settings.min_time],
                                         y_start=[ode_settings.min_y],
                                         x_end=[ode_settings.max_time],
                                         y_end=[ode_settings.max_y],
                                         ))

# initialize controls
# slider controlling stepsize of the solver
stepsize = Slider(title="stepsize", name='stepsize', value=ode_settings.step_init, start=ode_settings.step_min,
                  end=ode_settings.step_max, step=ode_settings.step_step)
stepsize.on_change('value', update_ode_data)
# slider controlling initial value of the ode
startvalue = Slider(title="startvalue", name='startvalue', value=ode_settings.x0_init,
                    start=ode_settings.x0_min,
                    end=ode_settings.x0_max, step=ode_settings.x0_step)
startvalue.on_change('value', update_data)
# gives the opportunity to choose from different solvers
solvers = RadioButtonGroup(labels=ode_settings.solver_labels, active=ode_settings.solver_init)
solvers.on_change('active', update_ode_data)
# gives the opportunity to choose from different odes
odes = RadioButtonGroup(labels=ode_settings.odetype_labels, active=ode_settings.odetype_init)
odes.on_change('active', update_data)

# initialize plot
toolset = "crosshair,pan,reset,resize,wheel_zoom,box_zoom"
# Generate a figure container
plot = Figure(plot_height=ode_settings.y_res,
              plot_width=ode_settings.x_res,
              tools=toolset,
              # title=text.value,
              title=ode_settings.title,
              x_range=[ode_settings.min_time, ode_settings.max_time],
              y_range=[ode_settings.min_y, ode_settings.max_y]
              )
# Plot the numerical solution by the x,t values in the source property
plot.line('t_num', 'x_num', source=source_num,
          line_width=2,
          line_alpha=0.6,
          color='black',
          line_dash=[7, 5]
          )
plot.circle('t_num', 'x_num', source=source_num,
            color='red',
            legend='numerical solution'
            )
# Plot the analytical solution by the x_ref,t values in the source property
plot.line('t_ref', 'x_ref', source=source_ref,
          color='green',
          line_width=3,
          line_alpha=0.6,
          legend='analytical solution'
          )
# Plot the direction field
quiver = my_bokeh_utils.Quiver(plot)

# calculate data
init_data()

# lists all the controls in our app
controls = widgetbox(stepsize, startvalue, solvers, odes, sizing_mode='stretch_both', width=400)

curdoc().add_periodic_callback(refresh_user_view, 100)
# make layout
curdoc().add_root(column(plot, controls))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
