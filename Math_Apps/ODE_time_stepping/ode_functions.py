from __future__ import division

import numpy as np
from scipy.optimize import fsolve


def dahlquist(_, x, lam):
    """
    dahlquist test equation ode.
    :param _: place holder for time, not used
    :param x: x value
    :param lam: lambda
    :return: slope dx/dt
    """
    dx = lam * x
    return dx


def dahlquist_ref(t, x0, lam):
    """
    reference solution for dahlquist test equation ode. x' = lam*x -> y = x0 * exp(lam*t)
    :param t: time
    :param x0: initial value
    :param lam: lambda
    :return: samples of reference solution for time t
    """
    x_ref = np.exp(lam * t) * x0  # analytical solution of the dahlquist test equation
    return x_ref


def definition_area(t, x):
    """
    for the initial value x0 = 1 this ODE only has a solution for x in (-sqrt(2),sqrt(2)). Therefore the ode is only
    defined in a certain area.
    :param t: time
    :param x: x value
    :return: slope dx/dt
    """
    dx = t * x ** 2
    return dx


def definition_area_ref(t, x0):
    """
    reference solution for ode with respricted definition area.
    :param t: time
    :param x0: initial value
    :return: samples of reference solution for time t
    """
    x_ref = 1. / (1. / x0 - 1. / 2. * (t ** 2))  # analytical solution of this ODE
    return x_ref


def logistic_equation(_, x, k, g):
    """
    ode for the logistic equation
    :param _: place holder for time, not used
    :param x: x value
    :param k: slope of logistic equation
    :param g: upper bound of logistic equation
    :return: slope dx/dt
    """
    dx = k * x * (g - x)
    return dx


def logistic_equation_ref(t, x0, k, g):
    """
    reference solution for logistic equation ode
    :param t: time
    :param x0: initial value
    :param k: slope of logistic equation
    :param g: upper bound of logistic equation
    :return: samples of reference solution for time t
    """
    if 0 != x0:
        x_ref = g * 1 / (1 + np.exp(-k * g * t) * (g / x0 - 1))
    else:
        x_ref = 0
    return x_ref


def oscillator_equation(_, x, omega):
    """
    two dimensionaly ode describing the harmonic oszillator
    :param _: place holder for time, not used
    :param x: x value
    :param omega: frequency of oszillation
    :return: slope dx/dt
    """
    A = np.array([[0, 1], [-omega ** 2, 0]])
    dx = np.dot(A, x)
    return dx


def oscillator_equation_ref(t, x0, omega, v0=0):
    """
    reference solution for two dimensional ode describing the harmonic oszillator
    :param t: time
    :param x0: initial displacements
    :param omega: frequency of oszillation
    :param v0: initial velocity
    :return: samples of reference solution (only displacement) for time t
    """
    x = x0 * np.exp(1j * omega * t) + v0 * np.exp(-1j * omega * t)
    return np.real(x)


def ref_sol(f_ref, x0, t_min = 0, t_max = 1, n_samples = 1000):
    """
    computes samples of the reference solution for a given timespan
    :param f_ref: reference solution function handle
    :param x0: initial value of ode
    :param t_min: starting time
    :param t_max: end time
    :param n_samples: number of samples to be produced
    :return: tuple of time and x value samples of the reference solution
    """
    t_ref = np.linspace(t_min, t_max, n_samples)
    x_ref = f_ref(t_ref, x0)
    return t_ref, x_ref


def expl_euler(f, x0, h, timespan):
    """
    explicit euler solver. Computes the solution for a given ode using explicit euler scheme.
    :param f: function handle for ode
    :param x0: initial value
    :param h: constant step size
    :param timespan: integration time
    :return: numerical solution in time and x
    """
    n = int(np.ceil(timespan / h))
    t = np.empty(n + 1)
    x = np.empty([x0.shape[0], n + 1])

    t[0] = 0
    x[:, 0] = x0
    for k in range(n):
        dx = f(t[k], x[:, k])
        t[k + 1] = (k + 1) * h
        x[:, k + 1] = x[:, k] + dx * h

    return t, x


def impl_euler(f, x0, h, timespan):
    """
    implicit euler solver. Computes the solution for a given ode using implicit euler scheme.
    :param f: function handle for ode
    :param x0: initial value
    :param h: constant step size
    :param timespan: integration time
    :return: numerical solution in time and x
    """
    n = int(np.ceil(timespan / h))
    t = np.empty(n + 1)
    x = np.empty([x0.shape[0], n + 1])

    t[0] = 0
    x[:, 0] = x0
    for k in range(n):
        t[k + 1] = (k + 1) * h
        try:
            x[:, k + 1] = fsolve(lambda arg: x[:, k] - arg + h * f(t[k + 1], arg), x[:, k])
        except RuntimeError:
            print "newton did not converge!"
            for k in range(k, n):
                t[k + 1] = (k + 1) * h
            break
    return t, x


def impl_midpoint(f, x0, h, timespan):
    """
    implicit midpoint rule solver. Computes the solution for a given ode using the implicit midpoint rule scheme.
    :param f: function handle for ode
    :param x0: initial value
    :param h: constant step size
    :param timespan: integration time
    :return: numerical solution in time and x
    """
    n = int(np.ceil(timespan / h))
    t = np.empty(n + 1)
    x = np.empty([x0.shape[0], n + 1])

    t[0] = 0
    x[:, 0] = x0
    for k in range(n):
        t[k + 1] = (k + 1) * h
        try:
            dx_left = f(t[k], x[:, k])
            x[:, k + 1] = fsolve(lambda arg: x[:, k] - arg + h / 2 * (f(t[k + 1], arg) + dx_left), x[:, k])
        except RuntimeError:
            print "newton did not converge!"
            for k in range(k, n):
                t[k + 1] = (k + 1) * h
            break
    return t, x
