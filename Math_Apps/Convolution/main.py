# ==============================================================================
# This file demonstrates a bokeh applet. The applet has been designed at TUM
# for educational purposes. The structure of the following code bases to large
# part on the work published on
# https://github.com/bokeh/bokeh/tree/master/examples
# ==============================================================================

import logging

logging.basicConfig(level=logging.DEBUG)

from bokeh.models import ColumnDataSource, Slider, Dropdown, TextInput
from bokeh.layouts import widgetbox, row
from bokeh.plotting import Figure
from bokeh.io import curdoc

from os.path import dirname, split

import numpy as np

import convolution_settings
import convolution_functions

global update_is_enabled


def update_data():
    """
    updates the data w.r.t. updated input.
    1. f1 and f2 are evaluated in the interval
    2. convolution f1*f2 is computed
    3. everyting, that is important for plotting is saved and plots are updated
    """
    # Get the current slider values
    x_value = x_value_input.value

    x = np.linspace(convolution_settings.x_min, convolution_settings.x_max,
                    convolution_settings.resolution)  # evaluation interval
    width = convolution_settings.x_max - convolution_settings.x_min  # width of the interval
    h = float(width) / float(convolution_settings.resolution)  # stepwidth for discrete convolution

    fun1_str = function1_input.value
    fun2_str = function2_input.value
    f1 = convolution_functions.parser(fun1_str, h)
    f2 = convolution_functions.parser(fun2_str, h)

    y1 = f1(x)  # evaluate first function
    y2 = f2(x)  # evaluate second function
    y2shift = f2(x_value - x)  # evaluate shifted function2
    y3 = np.convolve(y1, y2, mode='same') / x.size * width  # evaluate discrete convolution

    save_data(x, y1, y2shift, y3)


def save_data(x, y1, y2, y3):
    """
    saves the data to the corresponding data sources
    :param x: x values
    :param y1: y vector of the evaluations of f1
    :param y2: y vector of the evaluations of f2, shift and mirrored
    :param y3: y vector of the convolution f1*f2
    """
    # computes overlays of f1 and f2.
    y_positive, y_negative = convolution_functions.compute_overlay_vector(y1, y2)

    # saving data to plot
    source_overlay.data = dict(x=np.concatenate([x, x[-1::-1]]), y_pos=y_positive, y_neg=y_negative)
    source_function1.data = dict(x=x, y=y1)
    source_function2.data = dict(x=x, y=y2)
    source_result.data = dict(x=x, y=y3)

    y_value = convolution_functions.find_value(x, y3, x_value_input.value)
    source_xmarker.data = dict(x=[x_value_input.value, x_value_input.value], y=[y_value, 0])


def input_change(attrname, old, new):
    """
    called if function1, function2 or the x value changes
    :param attrname: not used
    :param old: not used
    :param new: not used
    """
    global update_is_enabled
    if update_is_enabled:
        update_data()


def function_pair_input_change(attr, old, new):
    """
    called if the sample function changes
    :param self:
    """
    function_key = new #function_type.value
    function1, function2 = convolution_settings.sample_functions[function_key]
    global update_is_enabled
    update_is_enabled = False  # disable update, that update is not committed again
    function1_input.value = function1
    function2_input.value = function2
    update_is_enabled = True

    update_data()


# initialize data source
source_function1 = ColumnDataSource(data=dict(x=[], y=[]))
source_function2 = ColumnDataSource(data=dict(x=[], y=[]))
source_result = ColumnDataSource(data=dict(x=[], y=[]))
source_convolution = ColumnDataSource(data=dict(x=[], y=[]))
source_xmarker = ColumnDataSource(data=dict(x=[], y=[]))
source_overlay = ColumnDataSource(data=dict(x=[], y=[], y_neg=[], y_pos=[]))

# initialize properties
update_is_enabled = True

# initialize controls
# dropdown menu for sample functions
function_type = Dropdown(label="choose a sample function pair or enter one below",
                         menu=convolution_settings.sample_function_names)
function_type.on_change('value', function_pair_input_change)

# slider controlling the evaluated x value of the convolved function
x_value_input = Slider(title="x value", name='x value', value=convolution_settings.x_value_init,
                       start=convolution_settings.x_value_min, end=convolution_settings.x_value_max,
                       step=convolution_settings.x_value_step)
x_value_input.on_change('value', input_change)
# text input for the first function to be convolved
function1_input = TextInput(value=convolution_settings.function1_input_init, title="my first function:")
function1_input.on_change('value', input_change)
# text input for the second function to be convolved
function2_input = TextInput(value=convolution_settings.function1_input_init, title="my second function:")
function2_input.on_change('value', input_change)

# initialize plot
toolset = "crosshair,pan,reset,save,wheel_zoom"
# Generate a figure container
plot = Figure(plot_height=400, plot_width=400, tools=toolset,
              title="Convolution of two functions",
              x_range=[convolution_settings.x_min_view, convolution_settings.x_max_view],
              y_range=[convolution_settings.y_min_view, convolution_settings.y_max_view])

# Plot the line by the x,y values in the source property
plot.line('x', 'y', source=source_function1, line_width=3, line_alpha=0.6, color='red', legend_label='function 1')
plot.line('x', 'y', source=source_function2, color='green', line_width=3, line_alpha=0.6, legend_label='function 2')
plot.line('x', 'y', source=source_result, color='blue', line_width=3, line_alpha=0.6, legend_label='convolution')
plot.scatter('x', 'y', source=source_xmarker, color='black')
plot.line('x', 'y', source=source_xmarker, color='black', line_width=3)
plot.patch('x', 'y_pos', source=source_overlay, fill_color='blue', fill_alpha=.2)
plot.patch('x', 'y_neg', source=source_overlay, fill_color='red', fill_alpha=.2)

# calculate data
update_data()

# lists all the controls in our app
controls = widgetbox(x_value_input, function_type, function1_input, function2_input, width=400)

# make layout
curdoc().add_root(row(plot, controls, width=800))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
