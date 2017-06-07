"""
Original from https://github.com/BenjaminRueth/Visualization/blob/master/ConvolutionApp/convolution_functions.py
Modified on Jun 06 2017

@author: benjamin
"""

from __future__ import division
import numpy as np
from sympy import sympify, lambdify


def window(x):
    """
    window function from -.5 to +.5
    :param x: ndarray
    :return: ndarray
    """
    return np.piecewise(x,
                        [x < -.5,
                         (-.5 <= x) * (x <= .5),
                         .5 < x],
                        [0,
                         1,
                         0])


def ramp(x):
    """
    ramp function
    :param x: ndarray
    :return: ndarray
    """
    return np.piecewise(x,
                        [x < 0,
                         (0 <= x) * (x <= 1.0),
                         1.0 < x],
                        [lambda arg: 0.0,
                         lambda arg: arg,
                         lambda arg: 0.0])


def saw(x):
    """
    saw tooth function
    :param x: ndarray
    :return: ndarray
    """
    w = 2.0  # intervall width
    n = 2  # number of oszillations
    return (((x + w * .5) % w) - w * .5) * npHeaviside(x + w * n * .5) * npHeaviside(w * n * .5 - x)


def npHeaviside(x):
    """
    numpy compatible implementation of heaviside function
    :param x: ndarraynp
    :return: ndarray
    """
    return np.piecewise(x,
                        [x < 0,
                         x == 0,
                         x > 0],
                        [lambda arg: 0.0,
                         lambda arg: 0.5,
                         lambda arg: 1.0])


def npDirac(x, h):
    """
    numpy compatible implementation of dirac delta. This implementation is representing a disrete version of dirac with
    width h and height 1/h. Area under dirac is equal to 1.
    :param x: ndarray, evaluation point
    :param h: width of dirac
    :return: ndarray
    """
    return npHeaviside(x + .5 * h) * npHeaviside(h * .5 - x) * 1.0


def string_to_function_parser(fun_str, h, args):
    """
    converts a string to a lambda function.
    :param fun_str: string representation of the function
    :param h: sampling width, needed for proper representation of dirac function
    :param args: symbolic arguments that will be turned into lambda function arguments
    :return:
    """

    print fun_str
    fun_sym = sympify(fun_str)
    fun_lam = sym_to_function_parser(fun_sym + 0.0j, h, args)

    return fun_lam, fun_sym


def sym_to_function_parser(fun_sym, h, args):
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
        fun_lam = lambdify(args, fun_sym, ['numpy',
                                    {"Heaviside": npHeaviside},
                                    {"DiracDelta": lambda x: npDirac(x, h)}])

    return fun_lam

"""
f,f_s = string_to_function_parser("sqrt(pi/2)*DiracDelta(f - 16*pi) + sqrt(pi/2)*DiracDelta(f + 16*pi)",.1,['f'])
f,f_s = string_to_function_parser("I*sqrt(pi/2)*DiracDelta(f - 8*pi) - I*sqrt(pi/2)*DiracDelta(f + 8*pi) + sqrt(pi/2)*DiracDelta(f + 4*pi) + sqrt(pi/2)*DiracDelta(f - 4*pi)",.1,['f'])
f,f_s = string_to_function_parser("1.0*DiracDelta(f - 8*pi)", .1, ['f'])
"""