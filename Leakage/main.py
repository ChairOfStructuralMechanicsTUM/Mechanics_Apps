from __future__ import division

from os.path import dirname, split

import numpy as np
from numpy.fft import fft, fftshift

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, VBox
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
f_sampled_source = ColumnDataSource(data=dict(t=[],f=[]))
f_analytical_source = ColumnDataSource(data=dict(t=[],f=[]))
# source for transformed function F
F_sampled_source = ColumnDataSource(data=dict(omega=[], F_real=[], F_imag=[]))
F_analytical_source = ColumnDataSource(data=dict(omega=[], F_real=[], F_imag=[]))
source_interval_patch = ColumnDataSource(data=dict(x_patch=[], y_patch=[]))
source_interval_bound = ColumnDataSource(data=dict(x_min=[], x_max=[], y_minmax=[]))

#######################
# INTERACTIVE WIDGETS #
#######################
# text input window for function f(x,y) to be transformed
f_input = TextInput(value='exp(-t)',
                    title="f(t):",
                    sizing_mode='stretch_both')

# dropdown menu for selecting one of the sample functions
sample_fun_input_f = Dropdown(label="choose a sample function f(t) or enter one below",
                              menu=sample_f_names,
                              sizing_mode='stretch_both')
# text input window for T0 (Sampling interval length)
t0_input = TextInput(value='1',
                     title=u"T\u2080 (Interval)",
                     sizing_mode='stretch_both')
# text input window for N (Number of sample points)
N_input = TextInput(value='2^6',
                    title=u"N (Number of sample points, max = 10\u2075)",
                    sizing_mode='stretch_both')

###########
# FIGURES #
###########
toolset=["crosshair, pan, wheel_zoom"]
# Generate a figure container for the original function
plot_original = Figure(x_axis_label='t',
                       y_axis_label='f(t)',
                       tools=toolset,active_scroll="wheel_zoom")

# Generate a figure container for the real part of the transformed function
plot_transform_real= Figure(x_axis_label=u'\u03C9',
                            y_axis_label=u'Re[F(\u03C9)]',
                            tools=toolset,active_scroll="wheel_zoom")

# Generate a figure container for the imaginary part of the transformed function
plot_transform_imag= Figure(x_axis_label=u'\u03C9',
                            y_axis_label=u'Im[F(\u03C9)]',
                            x_range=plot_transform_real.x_range, y_range=plot_transform_real.y_range,  # this line links the displayed region in the imaginary and the real part.
                            tools=toolset,active_scroll="wheel_zoom")

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
    T_0, N, f_function = extract_parameters()

    # computation of discrete FT
    F_samples, omega_samples, f_samples, t_samples = approximate_fourier_transform(T_0, N, f_function)

    # faking the analytical FT by using a high resolution discrete FT
    N_high = 10**5
    F_analytical, omega_analytical, f_analytical, t_analytical = approximate_fourier_transform(T_0, N_high, f_function)
    # we only use the part of the "analytical" solution that matched the discrete FT region, otherwise the interesting regions shrink too much
    decider = (omega_analytical >= omega_samples.min()) & (omega_analytical <= omega_samples.max())
    F_analytical = F_analytical[decider]  # truncuate F values
    omega_analytical = omega_analytical[decider]  # truncuate omega region

    # save to data source
    f_sampled_source.data = dict(t=t_samples, f=f_samples)
    F_sampled_source.data = dict(omega=omega_samples, F_real=F_samples.real, F_imag=F_samples.imag)
    f_analytical_source.data = dict(t=t_analytical, f=f_analytical)
    F_analytical_source.data = dict(omega=omega_analytical, F_real=F_analytical.real, F_imag=F_analytical.imag)

    t_start = 0 - N / T_0 / 2.0
    t_end = 0 + N / T_0 / 2.0

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

    plot_original.scatter('t', 'f', source=f_sampled_source, legend='samples')
    plot_original.line('t', 'f', source=f_analytical_source, line_width=.5, legend='f(t)')
    plot_transform_imag.scatter('omega', 'F_imag', source=F_sampled_source, legend='Im[DFT(f(t))]')
    plot_transform_imag.line('omega', 'F_imag', source=F_analytical_source, line_width=.5, legend=u'Im[F[\u03C9)]')
    plot_transform_real.scatter('omega', 'F_real', source=F_sampled_source, legend='Re[DFT(f(t)]')
    plot_transform_real.line('omega', 'F_real', source=F_analytical_source, line_width=.5, legend=u'Re[F(\u03C9)]')
    plot_transform_real.patch('x_patch', 'y_patch', source=source_interval_patch, alpha=.2)
    plot_transform_imag.patch('x_patch', 'y_patch', source=source_interval_patch, alpha=.2)
    plot_transform_real.line('x_min', 'y_minmax', source=source_interval_bound)
    plot_transform_real.line('x_max', 'y_minmax', source=source_interval_bound)
    plot_transform_imag.line('x_min', 'y_minmax', source=source_interval_bound)
    plot_transform_imag.line('x_max', 'y_minmax', source=source_interval_bound)


def on_parameters_changed(attr, old, new):
    update()


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


# create plots
initialize()

# add callback behaviour
f_input.on_change('value', on_function_changed)
sample_fun_input_f.on_click(sample_fun_input_changed)
t0_input.on_change('value',on_parameters_changed)
N_input.on_change('value',on_parameters_changed)

# create layout
controls = [f_input, sample_fun_input_f, t0_input, N_input]
controls_box = widgetbox(*controls,
                	 sizing_mode='fixed')  # all controls
curdoc().add_root(layout([[plot_original, plot_transform_real],
                          [controls_box, plot_transform_imag]],
                         sizing_mode='stretch_both')) # add plots and controls to root
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
