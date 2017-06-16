from __future__ import division

from os.path import dirname, split, join

import numpy as np
from numpy.fft import ifft, fft, fftshift

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, VBox, Div
from bokeh.layouts import widgetbox, layout, column
from bokeh.plotting import Figure
from bokeh.models.widgets import TextInput, Dropdown, CheckboxButtonGroup

from sympy import sympify

from sym_functions import string_to_function_parser

# sample functions with corresponding id
sample_f_names = [
    ("cos", "cos"),
    ("cos and sin", "cos and sin"),
   #("exp", "exp")
]

# function and corresponding FT
sample_functions = {
    "cos":("cos(2*pi*8*t)", "(1/2)*DiracDelta(f - 8) + (1/2)*DiracDelta(f + 8)"),
    "cos and sin":("cos(2*pi*2*t)+sin(2*pi*4*t)", "-I*(1/2)*DiracDelta(f - 4) + I*(1/2)*DiracDelta(f + 4) + (1/2)*DiracDelta(f + 2) + (1/2)*DiracDelta(f - 2)"),
    #"exp":("exp(-t)", "1/(1+4*(pi)^2 * f^2) - I*2*pi*f/(1+4*(pi)^2 * f^2)") # FT does not exist!
}

####################
# General Settings #
####################

color_interval = False  # here we can decide if we want to color the transformed interval
show_analytical_solution = True  # here we can decide if we want to show the analytical solution for sample functions
sample_function_id = "cos"  # here we set the sample function that initially activated
sample_function_used = True  # global bool that states whether a sample function is currently used


################
# Data Sources #
################
# source for original function f
x_sampled_source = ColumnDataSource(data=dict(t=[],x=[]))
x_analytical_source = ColumnDataSource(data=dict(t=[],x=[]))
# source for transformed function F
X_sampled_source = ColumnDataSource(data=dict(frequency=[], X_real=[], X_imag=[]))
X_analytical_source = ColumnDataSource(data=dict(frequency=[], X_real=[], X_imag=[]))

if color_interval:
    source_interval_patch = ColumnDataSource(data=dict(x_patch=[], y_patch=[]))
    source_interval_bound = ColumnDataSource(data=dict(x_min=[], x_max=[], y_minmax=[]))

#######################
# INTERACTIVE WIDGETS #
#######################
# text input window for function f(x,y) to be transformed
f_input = TextInput(value=sample_functions[sample_function_id][0],
                    title="x(t):")
# dropdown menu for selecting one of the sample functions
sample_fun_input_f = Dropdown(label="choose a sample function x(t) or enter one above",
                              menu=sample_f_names,
                              width=200)
# text input window for T0 (Sampling interval length)
t0_input = TextInput(value='1',
                     title=u"T\u2080 (Interval)")
# text input window for N (Number of sample points)
N_input = TextInput(value='2^6',
                    title=u"N (Number of sample points, max = 10\u2075)")
# button to show the solution
nyquist_label_default = "show sampling- and Nyquist-frequency"
nyquist_button = CheckboxButtonGroup(labels=[nyquist_label_default],
                                     active=[],
                                     sizing_mode="stretch_both")

###########
# FIGURES #
###########
toolset=["crosshair, pan, wheel_zoom"]
# Generate a figure container for the original function
plot_original = Figure(x_axis_label='t',
                       y_axis_label='x(t)',
                       tools=toolset,
                       active_scroll="wheel_zoom",
                       title="Function in Original Domain")

# Generate a figure container for the real part of the transformed function
plot_transform_real= Figure(x_axis_label='f',
                            y_axis_label='Re[X(f)]',
                            tools=toolset,
                            active_scroll="wheel_zoom",
                            title="Fourier transform of function - Real part")

# Generate a figure container for the imaginary part of the transformed function
plot_transform_imag= Figure(x_axis_label='f',
                            y_axis_label='Re[X(f)]',
                            x_range=plot_transform_real.x_range, y_range=plot_transform_real.y_range,  # this line links the displayed region in the imaginary and the real part.
                            tools=toolset,
                            active_scroll="wheel_zoom",
                            title="Fourier transform of function - Imaginary part")

def extract_parameters():
    """
    etxracts the necessary parameters from the input widgets
    :return: float T_0, float N, lambda function f
    """
    T_0 = float(sympify(t0_input.value.replace(',','.')))  # Interval
    t0_input.value = str(T_0)
    N = float(sympify(N_input.value.replace(',','.')))  # Number of sampled values

    if N > 10**5:  # we do not accept more than 10**5 sampling points!
        N = 10**5
        N_input.value = '10^5'

    h = T_0 / N
    print f_input.value
    f_function, _ = string_to_function_parser(f_input.value, h, ['t'])  # function to be transformed

    return T_0, N, f_function


def approximate_fourier_transform(T_0, N, f_function):
    """
    computes a discretized approximation of the continuous fouriertransform using fft
    :param T_0: interval length
    :param N: number of samples
    :param f_function: original function
    :return: samples values of FT, sample omega, sample values of f, sample time
    """
    T_S = T_0 / N  # Length of one sampling interval

    t_samples = np.arange(0, T_0, T_S)  # Grid in the Time Domain
    f_samples = np.arange(-(N/2) / T_0, (N/2 - 1) / T_0, 1/ T_0)  # Grid in the Frequency Domain

    # Function sampling
    x_samples = f_function(t_samples)

    # Fast Fourier Transform (FFT)
    X_samples = fft(x_samples)

    # Modifications in order to approximate the Continuous FT
    # X_samples /= N  # FFT and scaling with T_S
    X_samples = (1/N) * fftshift(X_samples)  # Shift of the results

    # ignore very small values and set them equal to zero
    a = X_samples.real
    b = X_samples.imag
    a[abs(a) < 10 ** -10] = 0
    b[abs(b) < 10 ** -10] = 0
    X_samples = a+1j*b

    return X_samples, f_samples, x_samples, t_samples


def sample_fourier_transform(T_0, N):
    """
    returns samples of the fourier transform
    :return:
    """
    assert sample_function_used

    sample_functions_transform = sample_functions[sample_function_id][1]

    N_samples = 1000
    f_analytical, h = np.linspace(-(N/2) / T_0, (N/2 - 1) / T_0, N_samples, retstep=True)  # Grid in the Frequency Domain
    X_function_analytical, _ = string_to_function_parser(sample_functions_transform, h, ['f'])  # function to be transformed
    X_analytical = X_function_analytical(f_analytical)

    return X_analytical, f_analytical


def update():
    """
    Compute data depending on input parameters. We compute the fft and the analytical fourier transform
    """

    # Extract parameters
    T_0, N, x_function = extract_parameters()

    # computation of discrete FT
    X_samples, f_samples, x_samples, t_samples = approximate_fourier_transform(T_0, N, x_function)
    x_sampled_source.data = dict(t=t_samples, x=x_samples)
    X_sampled_source.data = dict(frequency=f_samples, X_real=X_samples.real, X_imag=X_samples.imag)

    if sample_function_used and show_analytical_solution: # we only provide the analytical solution, if a sample function is used.
        X_analytical, f_analytical = sample_fourier_transform(T_0, N)
        X_analytical_source.data = dict(frequency=f_analytical.tolist(), X_real=X_analytical.real, X_imag=X_analytical.imag)

    else:  # otherwise we provide empty arrays
        X_analytical_source.data = dict(frequency=[], X_real=[], X_imag=[])

    N_samples = 1000
    t_analytical, h = np.linspace(0, T_0, N_samples, retstep=True)
    x_function_analytical, _ = string_to_function_parser(f_input.value, h, ['t'])  # function to be transformed
    x_analytical = x_function_analytical(t_analytical)
    x_analytical_source.data = dict(t=t_analytical.tolist(), x=x_analytical.tolist())

    if color_interval:
        t_start = - N / T_0 / 2.0
        t_end = + N / T_0 / 2.0
        # data for patch denoting the size of one interval
        source_interval_patch.data = dict(x_patch=[t_start,t_end,t_end,t_start],
                                          y_patch=[-10**3,-10**3,+10**3,+10**3])
        # data for patch border lines
        source_interval_bound.data = dict(x_min=[t_start,t_start],
                                          x_max=[t_end,t_end],
                                          y_minmax=[-10**3,-10**3])


def initialize():
    """
    initialize app
    :return:
    """

    update()

    plot_original.scatter('t', 'x', source=x_sampled_source, legend='samples')
    plot_original.line('t', 'x', color='red', source=x_analytical_source, line_width=.5, legend='x(t)')
    plot_transform_imag.scatter('frequency', 'X_imag', source=X_sampled_source, legend='Im[X(f)] - DFT')
    plot_transform_imag.line('frequency', 'X_imag', color='red', source=X_analytical_source, line_width=.5, legend='Im[X(f)]')
    plot_transform_real.scatter('frequency', 'X_real', source=X_sampled_source, legend='Re[X(f)] - DFT')
    plot_transform_real.line('frequency', 'X_real', color='red', source=X_analytical_source, line_width=.5, legend='Re[X(f)]')

    if color_interval:
        plot_transform_real.patch('x_patch', 'y_patch', source=source_interval_patch, alpha=.2)
        plot_transform_imag.patch('x_patch', 'y_patch', source=source_interval_patch, alpha=.2)
        plot_transform_real.line('x_min', 'y_minmax', source=source_interval_bound)
        plot_transform_real.line('x_max', 'y_minmax', source=source_interval_bound)
        plot_transform_imag.line('x_min', 'y_minmax', source=source_interval_bound)
        plot_transform_imag.line('x_max', 'y_minmax', source=source_interval_bound)


def reveal_solution():
    """
    reveals sampling and nyquist frequency for current setting
    :return:
    """
    T_0, N, _ = extract_parameters()
    sampling_frequency = N/T_0
    nyquist_frequency = sampling_frequency/2.0
    nyquist_button.labels = ["f_s: %.2f, f_Nyquist: %.2f" % (sampling_frequency, nyquist_frequency)]
    nyquist_button.active = [0]


def hide_solution():
    """
    hides sampling and nyquist frequency for current setting and replaces it with default text
    :return:
    """
    nyquist_button.labels = [nyquist_label_default]
    nyquist_button.active = []


def on_parameters_changed(attr, old, new):
    update()
    hide_solution()


def reset_views():
    """
    resets all views with respect to the currently plotted function. Should be called after a new function is eneterd.
    :return:
    """
    # reset the views of all three plots
    plot_original.x_range.start = min(x_sampled_source.data['t'])
    plot_original.x_range.end = max(x_sampled_source.data['t'])
    plot_original.y_range.start = min(x_sampled_source.data['x'])
    plot_original.y_range.end = max(x_sampled_source.data['x'])
    plot_transform_imag.x_range.start = min(X_sampled_source.data['frequency'])
    plot_transform_imag.x_range.end = max(X_sampled_source.data['frequency'])
    plot_transform_imag.y_range.start = min(min(X_sampled_source.data['X_real']), min(X_sampled_source.data['X_imag']))
    plot_transform_imag.y_range.end = max(max(X_sampled_source.data['X_real']), max(X_sampled_source.data['X_imag']))
    plot_transform_real.x_range.start = min(X_sampled_source.data['frequency'])
    plot_transform_real.x_range.end = max(X_sampled_source.data['frequency'])
    plot_transform_real.y_range.start = min(min(X_sampled_source.data['X_real']), min(X_sampled_source.data['X_imag']))
    plot_transform_real.y_range.end = max(max(X_sampled_source.data['X_real']), max(X_sampled_source.data['X_imag']))


def on_function_changed(attr, old, new):
    """
    Called if the function is changed by providing text input
    :param attr:
    :param old:
    :param new:
    :return:
    """
    # we set the bool false, because we use an arbitrary function that is input by the user
    global sample_function_used
    sample_function_used = False

    update()
    reset_views()


def sample_fun_input_changed(self):
    """
    Called if the sample function is changed.
    :param self:
    :return:
    """

    # we set the bool true, because we use a sample function for which we know the analytical solution
    global sample_function_used, sample_function_id
    sample_function_used = True

    # get the id
    sample_function_id = sample_fun_input_f.value
    # get the corresponding sample function
    sample_function = sample_functions[sample_function_id][0]
    # write the sample function into the textbox
    f_input.value = sample_function
    sample_function_used = True
    update()
    reset_views()


def on_nyquist_button_changed(attr, old, new):
    """
    called if the nyquist button is
    :return:
    """
    if 0 in nyquist_button.active:
        reveal_solution()
    else:
        hide_solution()


# create plots
initialize()

# add callback behaviour
f_input.on_change('value', on_function_changed)
sample_fun_input_f.on_click(sample_fun_input_changed)
t0_input.on_change('value', on_parameters_changed)
N_input.on_change('value', on_parameters_changed)
nyquist_button.on_change('active', on_nyquist_button_changed)

#Description
description_filename = join(dirname(__file__), "description.html")

description = Div(text=open(description_filename).read(), render_as_text=False)


# create layout
controls = [f_input, sample_fun_input_f, t0_input, N_input, nyquist_button]
controls_box = widgetbox(controls, responsive=True)  # all controls
curdoc().add_root(layout([[description],[plot_original, plot_transform_real],
                          [controls_box, plot_transform_imag]],
                         sizing_mode='stretch_both')) # add plots and controls to root
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
