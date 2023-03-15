"""
Created on Thu Jul 30 18:03:09 2015

@author: benjamin
"""

from sympy import lambdify
from sympy.core import diff
from scipy.integrate.quadpack import quad

def calc_area(f_x_sym, f_y_sym, t_val):
    from sympy.abc import t

    f_x = lambdify(t, f_x_sym,['numpy'])
    f_y = lambdify(t, f_y_sym, ['numpy'])
    df_x = lambdify(t, diff(f_x_sym), ['numpy'])
    df_y = lambdify(t, diff(f_y_sym), ['numpy'])

    integrand = lambda tau: f_x(tau)*df_y(tau)-df_x(tau)*f_y(tau)
    return abs(0.5 * quad(integrand, 0, t_val)[0])
