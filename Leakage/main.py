from __future__ import division

from os.path import dirname, split

import numpy as np
from numpy.fft import fft, fftshift

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.layouts import widgetbox, layout
from bokeh.plotting import Figure
from bokeh.models.widgets import TextInput, Dropdown

from sympy import sympify

from my_bokeh_utils import string_to_function_parser

sample_f_names = [
    ("cos", "cos(2*pi*8*t)"),
    ("cos and sin", "cos(2*pi*2*t)+sin(2*pi*4*t)"),
    ("exp", "exp(-t)")
]

################
# Data Sources #
################
# source for original function f
f_source = ColumnDataSource(data=dict(t=[],f=[]))
# source for transformed function F
F_source = ColumnDataSource(data=dict(omega=[], F_real=[], F_imag=[]))

#######################
# INTERACTIVE WIDGETS #
#######################
# text input window for function f(x,y) to be transformed
f_input = TextInput(value='exp(-t)', title="f(x):")
# dropdown menu for selecting one of the sample functions
sample_fun_input_f = Dropdown(label="choose a sample function f(x,y) or enter one below",
                              menu=sample_f_names)
# text input window for T0 (Sampling interval length)
t0_input = TextInput(value='1', title="T0 (Interval)")
# text input window for N (Number of sample points)
N_input = TextInput(value='2^6', title="N (Number of sample points, max = 10^5)")

###########
# FIGURES #
###########
# Generate a figure container for the original function
plot_original = Figure(x_axis_label='t',
                       y_axis_label='f(t)',
                       tools=["crosshair, save, tap"])

# Generate a figure container for the real part of the transformed function
plot_transform_real= Figure(x_axis_label='omega',
                            y_axis_label='real(F(omega))',
                            tools=["crosshair, save, tap"])

# Generate a figure container for the imaginary part of the transformed function
plot_transform_imag= Figure(x_axis_label='omega',
                            y_axis_label='imag(F(omega))',
                            tools=["crosshair, save, tap"])


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
    ## Extract parameters
    T_0, N, f_function = extract_parameters()

    F_samples, omega_samples, f_samples, t_samples = approximate_fourier_transform(T_0, N, f_function)

    # save to data source
    f_source.data = dict(t=t_samples, f=f_samples)
    F_source.data = dict(omega=omega_samples, F_real=F_samples.real, F_imag=F_samples.imag)


def initialize():
    """
    initialize app
    :return:
    """

    update()

    plot_original.line('t', 'f', source=f_source)
    plot_transform_imag.line('omega', 'F_imag', source=F_source)
    plot_transform_real.line('omega', 'F_real', source=F_source)


def widged_changed(attr, old, new):
    update()


def sample_fun_input_changed(self):
    """
    called if the sample function is changed.
    :param self:
    :return:
    """
    f_input.value = sample_fun_input_f.value
    update()


# create plots
initialize()

# add callback behaviour
f_input.on_change('value', widged_changed)
sample_fun_input_f.on_click(sample_fun_input_changed)
t0_input.on_change('value',widged_changed)
N_input.on_change('value',widged_changed)

# create layout
controls = widgetbox(f_input, sample_fun_input_f, t0_input, N_input)  # all controls
curdoc().add_root(layout([[plot_original, plot_transform_real],
                          [controls, plot_transform_imag]],
                         sizing_mode='stretch_both')) # add plots and controls to root
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '