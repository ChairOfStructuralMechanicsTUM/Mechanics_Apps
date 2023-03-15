__author__ = 'benjamin'

# general settings
# visu
x_min_view = -1
x_max_view = 3
y_min_view = -2
y_max_view = 2

# control degree
t_value_min = 0
t_value_max = 1
t_value_step = .01
t_value_init = 0

resolution = 100

sample_curve_names = [
    ("circle", "circle"),
    ("shifted circle", "shift_circle"),
    ("cardioid", "cardioid"),
    ("cycloid", "cycloid")
]

sample_curves = {
    "circle": ("sin(2*pi*t)", "cos(2*pi*t)"),
    "shift_circle": ("1+sin(2*pi*t)", "1+cos(2*pi*t)"),
    "cardioid": ("cos(2*pi*t)*(1+cos(2*pi*t))", "sin(2*pi*t)*(1+cos(2*pi*t))"),
    "cycloid": ("1/5*(8*pi*t-sin(8*pi*t))", "1/5*(1-cos(8*pi*t))")
}

# function input
x_component_input_msg = sample_curves["cardioid"][0]
y_component_input_msg = sample_curves["cardioid"][1]
