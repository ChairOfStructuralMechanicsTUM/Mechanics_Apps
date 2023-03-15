from __future__ import division

import pde_solvers
import pde_solutions

solvers = [pde_solvers.heat_do_explicit_step,
           pde_solvers.heat_do_implicit_step,
           pde_solvers.wave_do_explicit_step,
           pde_solvers.wave_do_implicit_step]

analytical_solutions = [pde_solutions.heat_analytical,
                        pde_solutions.heat_analytical,
                        pde_solutions.wave_analytical,
                        pde_solutions.wave_analytical]

t_init = 0.0
t_min = 0.0
t_max = 2.0
t_step = .01

h_init = .1
h_min = .005
h_max = .1
h_step = .005

k_init = .1
k_min = .005
k_max = .1
k_step = .005

x_min = 0.0
x_max = 1.0

IC_init = 'sin(x * 2 * pi)'

svg_palette_jet = ['#00008f', '#00009f', '#0000af', '#0000bf', '#0000cf', '#0000df', '#0000ef', '#0000ff', '#000fff',
                   '#001fff', '#002fff', '#003fff', '#004fff', '#005fff', '#006fff', '#007fff', '#008fff', '#009fff',
                   '#00afff', '#00bfff', '#00cfff', '#00dfff', '#00efff', '#00ffff', '#0fffef', '#1fffdf', '#2fffcf',
                   '#3fffbf', '#4fffaf', '#5fff9f', '#6fff8f', '#7fff7f', '#8fff6f', '#9fff5f', '#afff4f', '#bfff3f',
                   '#cfff2f', '#dfff1f', '#efff0f', '#ffff00', '#ffef00', '#ffdf00', '#ffcf00', '#ffbf00', '#ffaf00',
                   '#ff9f00', '#ff8f00', '#ff7f00', '#ff6f00', '#ff5f00', '#ff4f00', '#ff3f00', '#ff2f00', '#ff1f00',
                   '#ff0f00', '#ff0000', '#ef0000', '#df0000', '#cf0000', '#bf0000', '#af0000', '#9f0000', '#8f0000',
                   '#7f0000']
