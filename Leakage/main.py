from __future__ import division

from os.path import dirname, split

import numpy as np
from numpy.fft import fft, fftshift

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, VBox
from bokeh.layouts import widgetbox, layout, column
from bokeh.plotting import Figure
from bokeh.models.widgets import TextInput, Dropdown, CheckboxButtonGroup

from sympy import sympify

from my_bokeh_utils import string_to_function_parser

sample_f_names = [
    ("cos", "cos(2*pi*8*t)"),
    ("cos and sin", "cos(2*pi*2*t)+sin(2*pi*4*t)"),
    ("exp", "exp(-t)")
]

####################
# General Settings #
####################

color_interval = False  # here we can decide if we want to color the transformed interval

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
f_input = TextInput(value='exp(-t)',
                    title="x(t):")
# dropdown menu for selecting one of the sample functions
sample_fun_input_f = Dropdown(label="choose a sample function x(t) or enter one above",
                              menu=sample_f_names)
# text input window for T0 (Sampling interval length)
t0_input = TextInput(value='1',
                     title=u"T\u2080 (Interval)")
# text input window for N (Number of sample points)
N_input = TextInput(value='2^6',
                    title=u"N (Number of sample points, max = 10\u2075)")
# button to show the solution
nyquist_label_default = "Show sampling- and Nyquist-frequency"
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
    T_0 = float(sympify(t0_input.value))  # Interval
    N = float(sympify(N_input.value))  # Number of sampled values

    if N > 10**5:  # we do not accept more than 10**5 sampling points!
        N = 10**5
        N_input.value = '10^5'

    print f_input.value
    f_function, _ = string_to_function_parser(f_input.value, ['t'])  # function to be transformed

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
    omega_samples = np.arange(-N / 2 / T_0, N / 2 / T_0, 1 / T_0)  # Grid in the Frequency Domain

    # Function sampling
    f_samples = f_function(t_samples)

    # Fast Fourier Transform (FFT)
    F_samples = fft(f_samples)

    # Modifications in order to approximate the Continuous FT
    F_samples *= T_S  # FFT and scaling with T_S
    F_samples = fftshift(F_samples)  # Shift of the results

    # ignore very small values and set them equal to zero
    a = F_samples.real
    b = F_samples.imag
    a[abs(a) < 10 ** -10] = 0
    b[abs(b) < 10 ** -10] = 0
    F_samples = a+1j*b

    return F_samples, omega_samples, f_samples, t_samples


def update():
    """
    Compute data depending on input parameters. We compute the fft and the analytical fourier transform

    WARNING!
    Currently we fake the computation of the transform by just computing a high resolution fft, sympy allows us to do
    an analytical fourier transform but there are some bugs: https://github.com/sympy/sympy/issues/12591 (18.5.2017)
    """

    # Extract parameters
    T_0, N, x_function = extract_parameters()

    # computation of discrete FT
    X_samples, f_samples, x_samples, t_samples = approximate_fourier_transform(T_0, N, x_function)

    # faking the analytical FT by using a high resolution discrete FT
    N_high = 10**5
    X_analytical, f_analytical, x_analytical, t_analytical = approximate_fourier_transform(T_0, N_high, x_function)
    # we only use the part of the "analytical" solution that matched the discrete FT region, otherwise the interesting regions shrink too much
    decider = (f_analytical >= 2 * f_samples.min()) & (f_analytical <= 2 * f_samples.max())
    X_analytical = X_analytical[decider]  # truncuate F values
    f_analytical = f_analytical[decider]  # truncuate omega region

    # save to data source
    x_sampled_source.data = dict(t=t_samples, x=x_samples)
    X_sampled_source.data = dict(frequency=f_samples, X_real=X_samples.real, X_imag=X_samples.imag)
    x_analytical_source.data = dict(t=t_analytical, x=x_analytical)
    X_analytical_source.data = dict(frequency=f_analytical, X_real=X_analytical.real, X_imag=X_analytical.imag)

    t_start = 0 - N / T_0 / 2.0
    t_end = 0 + N / T_0 / 2.0

    if color_interval:
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
    nyquist_button.labels = ["sampling: %.2f, nyquist: %.2f" % (sampling_frequency, nyquist_frequency)]
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


def on_function_changed(attr, old, new):
    update()
    # reset the views of all three plots
    plot_original.x_range.start = min(f_sampled_source.data['t'])
    plot_original.x_range.end = max(f_sampled_source.data['t'])
    plot_original.y_range.start = min(f_sampled_source.data['f'])
    plot_original.y_range.end = max(f_sampled_source.data['f'])
    plot_transform_imag.x_range.start = min(F_sampled_source.data['omega'])
    plot_transform_imag.x_range.end = max(F_sampled_source.data['omega'])
    plot_transform_imag.y_range.start = min(min(F_sampled_source.data['F_real']),min(F_sampled_source.data['F_imag']))
    plot_transform_imag.y_range.end = max(max(F_sampled_source.data['F_real']),max(F_sampled_source.data['F_imag']))
    plot_transform_real.x_range.start = min(F_sampled_source.data['omega'])
    plot_transform_real.x_range.end = max(F_sampled_source.data['omega'])
    plot_transform_real.y_range.start = min(min(F_sampled_source.data['F_real']),min(F_sampled_source.data['F_imag']))
    plot_transform_real.y_range.end = max(max(F_sampled_source.data['F_real']),max(F_sampled_source.data['F_imag']))


def sample_fun_input_changed(self):
    """
    called if the sample function is changed.
    :param self:
    :return:
    """
    f_input.value = sample_fun_input_f.value
    update()


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

# create layout
controls = [f_input, sample_fun_input_f, t0_input, N_input, nyquist_button]
controls_box = widgetbox(controls, responsive=True)  # all controls
curdoc().add_root(layout([[plot_original, plot_transform_real],
                          [controls_box, plot_transform_imag]],
                         sizing_mode='stretch_both')) # add plots and controls to root
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
