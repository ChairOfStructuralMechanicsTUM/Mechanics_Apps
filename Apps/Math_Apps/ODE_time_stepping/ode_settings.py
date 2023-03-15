__author__ = 'benjamin'

import ode_functions as ode_fun

#some constants used in the ode_app
#general
max_time = 5        # max time for ode scheme
min_time = 0 # DONT CHANGE THIS!
max_y = 3.5
min_y = -1.5

# number of evaluated points for quiver field in each dimension
n_sample = 21

#plot settings
title = "Numerical ODE Solving"
x_res = 400
y_res = 400

#constants for dahlquist test equation
dahlquist_lambda = -5   # parameter y'=lambda*y

#constants for logistic equation
logistic_k = 5      #
logistic_g = .5     #

#constants for oscillator
oscillator_omega = 4 # parameter y''+omega**2*y=0

#available odes
ode_library = [lambda t, x: ode_fun.dahlquist(t, x, dahlquist_lambda),
               lambda t, x: ode_fun.logistic_equation(t, x, logistic_k, logistic_g),
               lambda t, x: ode_fun.definition_area(t, x),
               lambda t, x: ode_fun.oscillator_equation(t, x, oscillator_omega)]
ref_library = [lambda t, x0: ode_fun.dahlquist_ref(t, x0, dahlquist_lambda),
               lambda t, x0: ode_fun.logistic_equation_ref(t, x0, logistic_k, logistic_g),
               lambda t, x0: ode_fun.definition_area_ref(t, x0),
               lambda t, x0: ode_fun.oscillator_equation_ref(t,x0, oscillator_omega)]

oszillator_id = 3

#available solvers
solver_library = [lambda f, x0, h, timespan: ode_fun.expl_euler(f, x0, h, timespan),
                  lambda f, x0, h, timespan: ode_fun.impl_euler(f, x0, h, timespan),
                  lambda f, x0, h, timespan: ode_fun.impl_midpoint(f, x0, h, timespan)]

#settings for controls
#stepsize
step_max = 1.0
step_min = 0.1
step_step = 0.05
step_init = 1
#initial value
x0_max = 2.0
x0_min = 0.0
x0_step = 0.1
x0_init = 1.0
#ode solver
solver_labels = ["ExplicitEuler", "ImplicitEuler", "MidpointRule"]
solver_init = 0
#ode type
odetype_labels = ["Dahlquist", "Logistic","Def Area","Oscillator"]
odetype_init = 0


