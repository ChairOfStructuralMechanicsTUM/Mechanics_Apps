__author__ = 'benjamin'

# list defining the dropdown menu.
# the tuples have the following meaning: (<name in dropdown menu>, <key for sample_system_functions>)
sample_system_names = [
    ("linear stable", "linear_stable"),
    ("linear unstable", "linear_unstable"),
    ("saddlepoint", "saddlepoint"),
    ("circular stable", "circular_stable"),
    ("circular critical", "circular_critical"),
    ("circular unstable", "circular_unstable"),
    ("non linear", "non_linear"),
    ("non linear orbit", "non_linear_orbit"),
    ("pendulum", "pendulum"),
    ("chaotic system (long computation!)","dixon")
]
# key value pairs holding the with the function pair (u,v) that defines the ode system
sample_system_functions = {
    "linear_stable": ("-x", "-y"),
    "linear_unstable": ("+x", "+y"),
    "saddlepoint": ("4*y", "x"),
    "circular_stable": ("-y", "x-y/10"),
    "circular_critical": ("-y", "x"),
    "circular_unstable": ("-y", "x+y/10"),
    "non_linear": ("(x-1)*(y-1)", "(x+1)*(y+1)*(y-1)"),
    "non_linear_orbit": ("y", "(1-x^2)*y -x"),
    "pendulum": ("y","-sin(x)"),
    "dixon": ("(x*(y+2.5))/(x^2+(y+2.5)^2)-x/5.0",
              "((y+2.5)^2)/(x^2+(y+2.5)^2)-(y+2.5)/5.0-0.1") # see dixon system
}

# defines initial ode system by key
init_fun_key = "saddlepoint"

# defines initial user perspective on plot
x_min = -5.0
x_max = +5.0
y_min = -5.0
y_max = +5.0

# number of evaluated points for quiver field in each dimension
n_sample = 21
# corresponding resolution
resolution = (x_max - x_min) / (n_sample-1)

# defines initial starting point of streamline
x0_input_init=-2.0
y0_input_init=-4.0
#maximum number of integration steps for streamline
streamline_integration_steps = 1000
