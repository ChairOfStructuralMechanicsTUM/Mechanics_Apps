# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 00:28:16 2019

@author: Boulbrachene
"""

from os.path import dirname, split, join
import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt 
from math import exp
from bokeh.plotting import Figure, show
from bokeh.layouts import widgetbox, layout
from bokeh.models.widgets import Button, Select, Slider,TextInput
from sympy import sympify, lambdify, integrate
from bokeh.io import curdoc

# text input window for function f(t) to be transformed
f_input = TextInput(value="t*t", title="f(t):")
plot_transform_real= Figure(x_axis_label='b',
                            y_axis_label='a',
                            active_scroll="wheel_zoom",
                            title="Wavelet transform of function")

def extract_parameters():
    """
    etxracts the necessary parameters from the input widgets
    :return: float T_0, float N, lambda function f
    """
    f_function = string_to_function_parser(f_input.value, 't')  # function to be transformed

    return f_function

def string_to_function_parser(fun_str, args):
    """
    converts a string to a lambda function.
    :param fun_str: string representation of the function
    :param h: sampling width, needed for proper representation of dirac function
    :param args: symbolic arguments that will be turned into lambda function arguments
    :return:
    """

    # print (fun_str)
    fun_sym = sympify(fun_str)
    fun_lam = sym_to_function_parser(fun_sym + 0.0j, args)

    return fun_sym
###################################################################################

def sym_to_function_parser(fun_sym, args):
    """
    converts a symbolic expression to a lambda function. The function handles constant and zero symbolic input such that
    on numpy.array input a numpy.array with identical size is returned.
    :param fun_sym: symbolic expression
    :param h: sampling width, needed for proper representation of dirac function
    :param args: symbols turned into function input arguments
    :return:
    """

    if fun_sym.is_constant():
        fun_lam = lambda *x: np.ones_like(x[0]) * complex(fun_sym)
    else:
        fun_lam = lambdify(args, fun_sym, ['numpy'])

    return fun_lam

eval( "lambda x:x+1" )

s1 = lambdify('t',f_input.value)
quad(lambda t: evalf(s1), 1, 2)

# Extract parameters
x_function = 'x+1'
#c= str(x_function) + str(x_function)
#fun_sym = sympify(c)
#d=lambdify('t', fun_sym)

#print(d(2))
#def integrand1(x):
#    
#    return "x"
#output = "x"
#integraTion=quad(lambda x: eval(integrand1),0,1)[0]
