from __future__ import division
from sympy import sympify, lambdify
from scipy.integrate.quadpack import quad
from scipy.optimize import newton
import numpy as np


def sym_parser(fun_str):
    fun_sym = sympify(fun_str)
    return fun_sym

def parser(fun_str):
    from sympy.abc import t

    fun_sym = sym_parser(fun_str)
    fun_lam = lambdify(t, fun_sym,['numpy'])
    return fun_lam


def arclength(df_x, df_y, t):
    integrand = lambda tau: np.sqrt( df_x(tau)**2+df_y(tau)**2 )
    return quad(integrand,0,t)[0]


def s_inverse(df_x, df_y, t):
    s = lambda tau: arclength(df_x,df_y,tau)-t # objective function
    return newton(s,0)


def central_finite_difference(f,h,x0):
    return (f(x0+h)-f(x0-h)) / (2.0*h)


def calculate_tangent(f_x_str, f_y_str, t0):
    f_x_sym = sym_parser(f_x_str)
    f_y_sym = sym_parser(f_y_str)
    f_x = parser(f_x_str)
    f_y = parser(f_y_str)

    from sympy.core import diff
    from sympy.abc import t

    df_x_sym = diff(f_x_sym)
    df_y_sym = diff(f_y_sym)
    df_x = lambdify(t, df_x_sym, ['numpy'])
    df_y = lambdify(t, df_y_sym, ['numpy'])

    x = np.array([f_x(t0)],dtype=np.float64)
    y = np.array([f_y(t0)],dtype=np.float64)
    u = np.array([df_x(t0)],dtype=np.float64)
    v = np.array([df_y(t0)],dtype=np.float64)

    return x,y,u,v