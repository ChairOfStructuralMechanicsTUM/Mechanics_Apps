# ==============================================================================
# This file demonstrates a bokeh applet. The applet has been designed at TUM
# for educational purposes. The structure of the following code bases to large
# part on the work published on
# https://github.com/bokeh/bokeh/tree/master/examples
# ==============================================================================

import logging

logging.basicConfig(level=logging.DEBUG)

from bokeh.models.widgets import Slider, Dropdown, TextInput
from bokeh.models import ColumnDataSource
from bokeh.layouts import widgetbox, row, column
from bokeh.plotting import Figure
from bokeh.io import curdoc

import numpy as np

from os.path import dirname, split

import leibnitz_settings
import leibnitz_functions as lf
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import my_bokeh_utils


global update_callback
update_callback = True

def update_curve():
    # parse x and y component
    f_x, _ = my_bokeh_utils.string_to_function_parser(x_component_input.value, ['t'])
    f_y, _ = my_bokeh_utils.string_to_function_parser(y_component_input.value, ['t'])

    t = np.linspace(leibnitz_settings.t_value_min, leibnitz_settings.t_value_max,
                    leibnitz_settings.resolution)  # evaluation interval

    x = f_x(t)
    y = f_y(t)

    # saving data to plot
    source_curve.data = dict(x=x, y=y)


def update_point():
    # Get the current slider value
    t0 = t_value_input.value
    f_x, f_x_sym = my_bokeh_utils.string_to_function_parser(x_component_input.value, ['t'])
    f_y, f_y_sym = my_bokeh_utils.string_to_function_parser(y_component_input.value, ['t'])

    t_min = leibnitz_settings.t_value_min

    t = np.linspace(t_min, t0,
                    leibnitz_settings.resolution)  # evaluation interval

    x = f_x(t)
    y = f_y(t)

    x = np.array([0] + x.tolist() + [0])
    y = np.array([0] + y.tolist() + [0])

    x0 = f_x(t0)
    y0 = f_y(t0)

    area = lf.calc_area(f_x_sym, f_y_sym, t0)

    # saving data to plot
    source_point.data = dict(x=[x0], y=[y0])
    source_sector.data = dict(x=x, y=y)
    source_lines.data = dict(x_start=[0, f_x(t_min)], y_start=[0, f_y(t_min)],
                             x_end=[0, f_x(t0)], y_end=[0, f_y(t0)])
    source_text.data = dict(x=[f_x(t0)], y=[f_y(t0)],
                            text=[str(round(area, 2))], text_color=['blue'])


def curve_change(attrname, old, new):
    global update_callback
    if update_callback:
        update_curve()
        update_point()


def sample_curve_change(attr, old, new):
    global update_callback
    # get sample function pair (first & second component of ode)
    sample_curve_key = new #sample_curve_input.value
    sample_curve_x_component, sample_curve_y_component = leibnitz_settings.sample_curves[sample_curve_key]
    # write new functions to u_input and v_input
    update_callback = False  # prevent callback
    x_component_input.value = sample_curve_x_component
    update_callback = True  # allow callback
    y_component_input.value = sample_curve_y_component


def t_value_change(attrname, old, new):
    update_point()


# initialize data source
source_curve = ColumnDataSource(data=dict(x=[], y=[]))
source_point = ColumnDataSource(data=dict(x=[], y=[]))
source_sector = ColumnDataSource(data=dict(x=[], y=[]))
source_lines = ColumnDataSource(data=dict(x_start=[], y_start=[], x_end=[], y_end=[]))
source_text = ColumnDataSource(data=dict(area=[]))

# initialize controls
# slider controlling the current parameter t
t_value_input = Slider(title="parameter t", name='parameter t', value=leibnitz_settings.t_value_init,
                       start=leibnitz_settings.t_value_min, end=leibnitz_settings.t_value_max,
                       step=leibnitz_settings.t_value_step)
t_value_input.on_change('value', t_value_change)
# text input for the x component of the curve
x_component_input = TextInput(value=leibnitz_settings.x_component_input_msg, title="curve x")
x_component_input.on_change('value', curve_change)
# text input for the y component of the curve
y_component_input = TextInput(value=leibnitz_settings.y_component_input_msg, title="curve y")
y_component_input.on_change('value', curve_change)
# dropdown menu for selecting one of the sample curves
sample_curve_input = Dropdown(label="choose a sample function pair or enter one below",
                              menu=leibnitz_settings.sample_curve_names)
sample_curve_input.on_change('value', sample_curve_change)

# initialize plot
toolset = "crosshair,pan,reset,save,wheel_zoom"
# Generate a figure container
plot = Figure(plot_height=400, plot_width=400, tools=toolset,
              title="Leibnitz sector formula",
              x_range=[leibnitz_settings.x_min_view, leibnitz_settings.x_max_view],
              y_range=[leibnitz_settings.y_min_view, leibnitz_settings.y_max_view])

# Plot the line by the x,y values in the source property
plot.line('x', 'y', source=source_curve, line_width=3, line_alpha=1, color='black', legend_label='curve')
plot.scatter('x', 'y', source=source_point, color='blue', legend_label='point at t')
plot.scatter([0], [0], color='black', marker='x')
pat = plot.patch('x', 'y', source=source_sector, fill_color='blue', fill_alpha=.2, legend_label='area')
plot.line('x_start', 'y_start', source=source_lines, line_width=1, line_alpha=1, color='blue')
plot.line('x_end', 'y_end', source=source_lines, line_width=1, line_alpha=1, color='blue')
plot.text('x', 'y', text='text', text_color='text_color', source=source_text)

# calculate data
update_curve()
update_point()

# lists all the controls in our app
controls = widgetbox(t_value_input, sample_curve_input, x_component_input, y_component_input)

# make layout
curdoc().add_root(row(plot, controls))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
