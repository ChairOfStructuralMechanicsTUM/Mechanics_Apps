from __future__ import division
import numpy as np

#==============================================================================
# The hat function    
#==============================================================================
def hat(x):
    return -npHeaviside(x) * (-np.pi+x)/np.pi + npHeaviside(-x) * (np.pi+x)/np.pi

#==============================================================================
# The step function
#==============================================================================
def step(x):
    return npHeaviside(x) - npHeaviside(-1*x)

#==============================================================================
# The sawtooth function    
#==============================================================================
def saw(x):
    return x/np.pi


def npHeaviside(x):
    """
    numpy compatible implementation of heaviside function
    :param x: ndarray
    :return: ndarray
    """
    return np.piecewise(x,
                        [x<0,
                         x==0,
                         x>0],
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
    return npHeaviside(x)*npHeaviside(h-x)*1.0/h


def parser(fun_str):
    from sympy import sympify, lambdify
    from sympy.abc import x

    fun_sym = sympify(fun_str)
    fun_lam = lambdify(x, fun_sym,['numpy',
                                   {"Heaviside": npHeaviside},
                                   {"Dirac": npDirac}])
    return fun_lam


def number_parser(number_str):
    from sympy import sympify
    number_sym = sympify(number_str)
    return float(number_sym)


def coeff(f, start, end, N):
    """
    This function computes the coefficients of the fourier series representation
    of the function f, which is periodic on the interval [start,end] up to the
    degree N.
    """
    return coeff_fft(f, start, end, N)


def coeff_fft(f, start, end, N):
    """
    computes the fourier coefficients using fft
    :param f:
    :param start:
    :param end:
    :param N:
    :return:
    """
    M = 4*N+1000+1
    x = np.linspace(start, end, M, endpoint=False)
    u0 = f(x)

    c = np.fft.rfft(u0) / M

    a = 2 * np.real(c)
    b = -2 * np.imag(c)

    a[0] /= 2

    return [a[0:N+1], b[0:N+1]]


def fourier_series(a, b, N, T, x):
    """
    This function evaluates the fourier series of degree N with the coefficient
    vectors a and b and the period length T at the points in the array x.
    :param a: even coefficients
    :param b: uneven coefficients
    :param N: degree of fourier series
    :param T: period length
    :param x: sample points
    :return: fourier series evaluated at sample points
    """
    # numpy matrix version of code below
    a = a[:N+1]
    b = b[:N+1]

    """
    y = np.zeros(x.shape)
    for k in range(N+1):
        kk = k * 2 * np.pi / T
        y += (b[k] * np.sin(kk*x) + a[k] * np.cos(kk*x))
    """
    k = np.arange(N+1)
    kk = k * 2 * np.pi / T
    y = np.sum(b * np.sin(np.outer(x, kk)) + a * np.cos(np.outer(x, kk)), axis=1)
    return y