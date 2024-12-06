__author__ = 'benjamin'

# defines initial user perspective on plot
x_min = -5.0
x_max = +5.0
y_min = -5.0
y_max = +5.0

sample_functions = {
    "circular": ("y", "x")
}

sample_curves = {
    "circle": ("cos(t)", "sin(t)")
}

# defines initial function by key
init_fun_key = "circular"
# defines initial curve by key
init_curve_key = "circle"

# number of evaluated points for quiver field in each dimension
n_sample = 21
# corresponding resolution
resolution = (x_max - x_min) / (n_sample-1)

# defines slider control for parameter
parameter_input_init = 0
parameter_min = 0
parameter_max = 1
parameter_step = .01
