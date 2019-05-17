__author__ = 'benjamin'

import numpy as np

# general settings
# visu
x_min_view=-2
x_max_view=2
y_min_view=-1
y_max_view=3

# sampling
x_min=-10
x_max=10
y_min=-10
y_max=10
resolution=2000.0

#function input
sample_function_names = [
    ("Window&Window", "Window&Window"),
    ("Ramp&Ramp","Ramp&Ramp"),
    ("Cosine&Heaviside", "Cosine&Heaviside"),
    ("Cosine&Ramp", "Cosine&Ramp"),
    ("Sine&Heaviside", "Sine&Heaviside"),
    ("Sine&Ramp", "Sine&Ramp")
]

sample_functions = {
    "Window&Window":("Heaviside(x+1) * Heaviside(1-x)","Heaviside(x+1) * Heaviside(1-x)"),
    "Ramp&Ramp":("x*Heaviside(x+1) * Heaviside(1-x)","x*Heaviside(x+1) * Heaviside(1-x)"),
    "Cosine&Heaviside": ("cos(x*pi/2) * Heaviside(x+1) * Heaviside(1-x)", "Heaviside(x)"),
    "Cosine&Ramp": ("cos(x*pi/2) * Heaviside(x+1) * Heaviside(1-x)", "x*Heaviside(x)"),
    "Sine&Heaviside": ("sin(x*pi/2) * Heaviside(x+1) * Heaviside(1-x)", "Heaviside(x)"),
    "Sine&Ramp": ("sin(x*pi/2) * Heaviside(x+1) * Heaviside(1-x)", "x*Heaviside(x)")
}
function1_input_init = "sin(x*pi) * Heaviside( x+1 ) * Heaviside(1-x)"
function2_input_init = "sin(x*pi) * Heaviside( x+1 ) * Heaviside(1-x)"

#fourierseries
timeinterval_start = -np.pi
timeinterval_end = +np.pi
timeinterval_length = timeinterval_end-timeinterval_start

# control degree
x_value_min=x_min
x_value_max=x_max
x_value_step=.1
x_value_init=0


