"""
Created on Sat Jul 11 22:04:14 2015

@author: benjamin
"""

from __future__ import division

import logging

logging.basicConfig(level=logging.DEBUG)

import numpy as np

from bokeh.models import ColumnDataSource, Slider, RadioButtonGroup, TextInput
from bokeh.layouts import widgetbox, row, column, Spacer
from bokeh.plotting import Figure
from bokeh.io import curdoc

import pde_settings
import pde_functions

from os.path import dirname, split

u_x = [None]

def get_numerical_solution_data(k, t):
    """
    computes the numerical solution for a given time.
    :param k; temporal meshwidth
    :param t: time
    :return: x values and corresponding solution values u
    """
    idx = int(round(t / k, 0))
    u_key = 'u' + str(idx)
    x = mesh_data.data['x']
    u = mesh_data.data[u_key]
    return x, u


def updata_analytical_solution():
    """
    updates the analytical solution
    """
    x = np.linspace(pde_settings.x_min, pde_settings.x_max, 200)
    u_ana_id = get_solver_id()
    f0 = pde_functions.parse(initial_condition.value)
    u_x[0] = pde_settings.analytical_solutions[u_ana_id](f0, x)


def get_analytical_solution_data(t):
    """
    computes the analytical solution for a given time.
    :param t: time
    :return: x values and corresponding solution values u
    """
    x = np.linspace(pde_settings.x_min, pde_settings.x_max, 200)
    u_ana_id = get_solver_id()
    if u_ana_id == 0 or u_ana_id == 1:
        t += .001
    u = u_x[0](t)
    return x, u


def update_plot(k, t):
    """
    updates the plot w.r.t new data by updating the corresponding bokeh.models.ColumnDataSource
    :param k: temporal meshwidth
    :param t: time
    :return:
    """
    x_num, u_num = get_numerical_solution_data(k, t)
    x_ana, u_ana = get_analytical_solution_data(t)
    plot_data_num.data = dict(x=x_num, u=u_num)
    plot_data_ana.data = dict(x=x_ana, u=u_ana)


def get_solver_id():
    """
    maps the tuple of active pde and active solver to the corresponding id
    """
    return pde_type.active * 2 + solver_type.active


def mesh_change(attrname, old, new):
    """
    called if the numerical discretization mesh changes
    :param attrname: not used
    :param old: not used
    :param new: not used
    :return:
    """
    # read discretization parameters
    h = h_slider.value  # spatial meshwidth
    k = k_slider.value  # temporal meshwidth
    update_mesh(h, k)


def pde_type_change(attrname, old, new):
    """
    called if the pde type is changed
    :param attrname: not used
    :param old: not used
    :param new: not used
    """
    updata_analytical_solution()
    mesh_change(attrname, old, new)


def time_change(attrname, old, new):
    """
    called if the active timestep changes.
    :param attrname: not used
    :param old: not used
    :param new: not used
    """
    # read values from sliders
    k = k_slider.value
    t = time_slider.value
    # plot current time
    update_plot(k, t)


def update_mesh(h, k):
    """
    called if the numerical discretization mesh changed. i.e. if temporal or spatial meshwidth changes. The whole
    problem is recomputed and each timestep is saved to the mesh_data. Finally the currently active timestep is plotted.
    :param h: spatial meshwidth
    :param k: temporal meshwidth
    """
    solver_id = get_solver_id()
    pde_specs.data = dict(h=[h], k=[k], solver_id=[solver_id])

    solver = pde_settings.solvers[solver_id]

    # spatial discretization
    x0 = pde_settings.x_min
    x1 = pde_settings.x_max
    x = np.arange(x0, x1+h, h)

    # get initial condition
    f0 = pde_functions.parse(initial_condition.value)
    u = f0(x)

    # this enforces neumann BC: u'(t=0)=0
    u_old = np.array(u)

    # number of timesteps
    n_temporal = int(round(pde_settings.t_max / k, 0)) + 1

    # setup datastructure for saving each timestep
    mesh_dict = dict(x=x)

    for i in range(n_temporal): # iterate over all timesteps
        key = 'u' + str(i)
        mesh_dict[key] = u.tolist() # save result to dict
        u_new = solver(u_old, u, k, h) # propagate in time
        u_old = u
        u = u_new

    mesh_data.data = mesh_dict
    t = time_slider.value
    update_plot(k, t)


def initial_condition_change(attrname, old, new):
    """
    callback function if the initial condition of the pde changes.
    :param attrname: not used
    :param old: not used
    :param new: not used
    """
    updata_analytical_solution()
    mesh_change(attrname, old, new)


def init_pde():
    """
    initialize data
    """
    h = h_slider.value
    k = k_slider.value
    updata_analytical_solution()
    update_mesh(h, k)


# initialize data source
plot_data_num = ColumnDataSource(data=dict(x=[], u=[]))
plot_data_ana = ColumnDataSource(data=dict(x=[],u=[]))
mesh_data = ColumnDataSource(data=dict())
pde_specs = ColumnDataSource(data=dict(h=[], k=[]))

# initialize controls
# slider for going though time
time_slider = Slider(title="time", name='time', value=pde_settings.t_init, start=pde_settings.t_min, end=pde_settings.t_max,
                     step=pde_settings.t_step)
time_slider.on_change('value', time_change)
# slider controlling spatial stepsize of the solver
h_slider = Slider(title="spatial meshwidth", name='spatial meshwidth', value=pde_settings.h_init, start=pde_settings.h_min,
                  end=pde_settings.h_max, step=pde_settings.h_step)
h_slider.on_change('value', mesh_change)
# slider controlling spatial stepsize of the solver
k_slider = Slider(title="temporal meshwidth", name='temporal meshwidth', value=pde_settings.k_init, start=pde_settings.k_min,
                  end=pde_settings.k_max, step=pde_settings.k_step)
k_slider.on_change('value', mesh_change)
# radiobuttons controlling pde type
pde_type = RadioButtonGroup(labels=['Heat', 'Wave'], active=0)
pde_type.on_change('active', pde_type_change)
# radiobuttons controlling solver type
solver_type = RadioButtonGroup(labels=['Explicit', 'Implicit'], active=0)
solver_type.on_change('active', mesh_change)
# text input for IC
initial_condition = TextInput(value=pde_settings.IC_init, title="initial condition")
initial_condition.on_change('value', initial_condition_change)

# initialize plot
toolset = "crosshair,pan,reset,wheel_zoom,box_zoom"
# Generate a figure container
plot = Figure(plot_height=400,
              plot_width=400,
              tools=toolset,
              title="Time dependent PDEs",
              x_range=[pde_settings.x_min, pde_settings.x_max],
              y_range=[-1, 1]
              )

# Plot the numerical solution at time=t by the x,u values in the source property
plot.line('x', 'u', source=plot_data_num,
          line_width=.5,
          line_alpha=.6,
          line_dash=[4, 4],
          color='red')
plot.line('x', 'u', source=plot_data_ana,
          line_width=.5,
          line_alpha=.6,
          color='blue',
          legend_label='analytical solution')
plot.circle('x', 'u', source=plot_data_num,
            color='red',
            legend_label='numerical solution')

# calculate data
init_pde()

# lists all the controls in our app
controls = widgetbox(initial_condition,time_slider,h_slider,k_slider,pde_type, solver_type,width=400)

# make layout
curdoc().add_root(row(plot,controls,width=800))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
