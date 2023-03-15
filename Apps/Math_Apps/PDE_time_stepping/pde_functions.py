import numpy as np
from sympy import sympify, lambdify
from sympy.abc import x


def npHeaviside(x):
    """
    numpy compatible implementation of heaviside function
    :param x: ndarray
    :return: ndarray
    """
    return np.select([x<0,x==0,x>0],[0.0,0.5,1.0])


def parse(fun_str):
    fun_sym = sympify(fun_str)
    fun_lam = lambdify(x, fun_sym,['numpy',{"Heaviside": npHeaviside,
                                            "heaviside": npHeaviside}])
    return fun_lam