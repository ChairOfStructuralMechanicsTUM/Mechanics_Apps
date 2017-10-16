import numpy as np
import logging

from astropy.convolution.tests.test_convolve_kernels import width

logging.basicConfig(level=logging.DEBUG)

from bokeh.models.widgets import Slider, RadioButtonGroup, TextInput, Panel, Tabs
from bokeh.models import ColumnDataSource
from bokeh.layouts import widgetbox, column, row
from bokeh.plotting import Figure
from bokeh.io import curdoc

import fourier_functions as ff
import fourier_settings as fs
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import my_bokeh_utils


def update_fourier_coeffs(f, N, t_start, t_end):
    """
    updates the fourier coefficients. Therefore the fourier coefficients are computed for a function f, that covers
    one period on the interval [t_start, t_end]. The final output is saved to a bokeh.models.ColumnDataSource
    :param f: function handle
    :param N: maximum degree of fourier coefficients
    :param t_start: start of one period
    :param t_end: end of one period
    """
    # compute fourier coefficients
    a, b = ff.coeff(f, t_start, t_end, N)  # calculate coefficients

    # save coefficients to data source
    source_coeff.data = dict(a=a, b=b)

    print "fourier coefficients have been updated for new function up to maximum degree N = %d" % (N)


def update_plot(f, N, t_start, t_end):
    """
    updates the plot data from given resources. The resulting plot data fits to the current user view window.

    The following plots are updated:
    - Line plot of the original function
    - Line plot of the fourier series from given coefficients a,b
    - Patch plot marking one period
    - Line plot of the borders of the period

    All the updated data is saved to the corresponding bokeh.models.ColumnDataSource_s
    :param f: function handle
    :param N: maximum degree for the fourier series that is plotted
    :param t_start: starting point of the period
    :param t_end: end point of the period
    """
    # interval length
    T = t_end - t_start

    # function f(x) which will be approximated
    t = np.linspace(plot.x_range.start,
                    plot.x_range.end,
                    2 * fs.resolution)
    periodic_t = (t - t_start) % T + t_start
    x_orig = f(periodic_t)

    # Generate Fourier series
    x_fourier = ff.fourier_series(source_coeff.data['a'],
                                  source_coeff.data['b'],
                                  N,
                                  T,
                                  t - t_start)

    # saving data to plot
    # data with evaluation of original function
    source_orig.data = dict(t=t,
                            x_orig=x_orig)
    # data with evaluation of fourier series
    source_fourier.data = dict(t=t,
                               x_fourier=x_fourier)
    # data for patch denoting the size of one interval
    source_interval_patch.data = dict(x_patch=[t_start,
                                               t_end,
                                               t_end,
                                               t_start],
                                      y_patch=[plot.y_range.start,
                                               plot.y_range.start,
                                               plot.y_range.end,
                                               plot.y_range.end])
    # data for patch border lines
    source_interval_bound.data = dict(x_min=[t_start,
                                             t_start],
                                      x_max=[t_end,
                                             t_end],
                                      y_minmax=[plot.y_range.start,
                                                plot.y_range.start])


def type_input_change(attrname, old, new):
    """
    Callback function for controls that affect the fourier coefficients and therefore require an updated of the
    coefficients.
    :param attrname:
    :param old:
    :param new:
    """
    function_change()


def degree_change(attrname, old_N, new_N):
    """
    Callback function that handles a change of the degree. This does not affect the (precomputed) fourier
    coefficients, but only the plotting.
    :param attrname:
    :param old_N:
    :param new_N:
    :return:
    """
    # read control varoables
    f = source_f.data['f'][0]
    t_start = source_periodicity.data['t_start'][0]
    t_end = source_periodicity.data['t_end'][0]

    update_plot(f, new_N, t_start, t_end)


def function_change():
    """
    function that handles a change in the control variables that cause a change in the fourier coefficients. The
    updated control variables are parsed and saved and from this information the fourier coefficients are updated.
    """
    N = int(round(degree.value))  # Get the current slider values

    # parse function from text input
    if fun_tabs.active == 0:
        f = fs.function_library[sample_function_type.active]
        timeinterval_start_str = fs.timeinterval_start_init
        timeinterval_end_str = fs.timeinterval_end_init
    elif fun_tabs.active == 1:
        fun_str = default_function_input.value
        f = ff.parser(fun_str)
        timeinterval_start_str = default_function_period_start.value
        timeinterval_end_str = default_function_period_end.value

    # parse time interval data
    t_start = ff.number_parser(timeinterval_start_str)
    t_end = ff.number_parser(timeinterval_end_str)

    # save updated control variables to data sources.
    source_f.data = dict(f=[f])
    source_periodicity.data = dict(t_start=[t_start], t_end=[t_end])

    update_fourier_coeffs(f, fs.degree_max, t_start, t_end)
    update_plot(f, N, t_start, t_end)


def automatic_update():
    """
    Function that is regularly called by the periodic callback. Updates the plots to the current user view.
    """
    user_view_has_changed = my_bokeh_utils.check_user_view(source_view.data, plot)
    if user_view_has_changed:

        source_view.data = my_bokeh_utils.get_user_view(plot)

        # read control variables
        N = int(round(degree.value))  # Get the current slider values
        f = source_f.data['f'][0]
        t_start = source_periodicity.data['t_start'][0]
        t_end = source_periodicity.data['t_end'][0]

        print "updating plot"
        update_plot(f, N, t_start, t_end)


# initialize data source
source_fourier = ColumnDataSource(data=dict(t=[], x_fourier=[]))
source_orig = ColumnDataSource(data=dict(t=[], x_orig=[]))
source_interval_patch = ColumnDataSource(data=dict(x_patch=[], y_patch=[]))
source_interval_bound = ColumnDataSource(data=dict(x_min=[], x_max=[], y_minmax=[]))
source_coeff = ColumnDataSource(data=dict(a=[], b=[]))
source_f = ColumnDataSource(data=dict(f=[None]))
source_periodicity = ColumnDataSource(data=dict(t_start=[None], t_end=[None]))
source_view = ColumnDataSource(data=dict(x_start=[None], x_end=[None], y_start=[None], y_end=[None]))

# initialize controls
# buttons for choosing a sample function
sample_function_type = RadioButtonGroup(labels=fs.function_names, active=fs.function_init)

# here one can choose arbitrary input function
default_function_input = TextInput(value=fs.function_input_init)
default_function_period_start = TextInput(title='period start', value=fs.timeinterval_start_init)
default_function_period_end = TextInput(title='period end', value=fs.timeinterval_end_init)

# slider controlling degree of the fourier series
degree = Slider(title="degree", name='degree', value=fs.degree_init, start=fs.degree_min,
                end=fs.degree_max, step=fs.degree_step)

# initialize callback behaviour
degree.on_change('value', degree_change)
default_function_input.on_change('value',
                                 type_input_change)  # todo write default functions for any callback, like above
default_function_period_start.on_change('value', type_input_change)
default_function_period_end.on_change('value', type_input_change)
sample_function_type.on_change('active', type_input_change)

# initialize plot
toolset = "crosshair,pan,reset,resize,save,wheel_zoom"
# Generate a figure container
plot = Figure(plot_height=fs.resolution,
              plot_width=fs.resolution,
              tools=toolset,
              title="Fourier Series Approximation",
              x_range=[fs.x_min, fs.x_max],
              y_range=[fs.y_min, fs.y_max]
              )
# Plot the line by the x,y values in the source property
plot.line('t', 'x_orig', source=source_orig,
          line_width=3,
          line_alpha=0.6,
          color='red',
          legend='original function'
          )
plot.line('t', 'x_fourier', source=source_fourier,
          color='green',
          line_width=3,
          line_alpha=0.6,
          legend='fourier series'
          )

plot.patch('x_patch', 'y_patch', source=source_interval_patch, alpha=.2)
plot.line('x_min', 'y_minmax', source=source_interval_bound)
plot.line('x_max', 'y_minmax', source=source_interval_bound)

sample_controls = widgetbox(sample_function_type)

default_controls = column(default_function_input,default_function_period_start,default_function_period_end)

# Panels for sample functions or default functions
sample_funs = Panel(child=sample_controls, title='sample function')
default_funs = Panel(child=default_controls, title='default function')
# Add panels to tabs
fun_tabs = Tabs(tabs=[sample_funs, default_funs])
fun_tabs.on_change('active', type_input_change)  # add callback for panel tabs

# lists all the controls in our app
controls = column(degree,fun_tabs)

# initialize data
function_change()

# regularly update user view
curdoc().add_periodic_callback(automatic_update, 100)
# make layout
curdoc().add_root(row(plot, controls, height=600, width=800))
