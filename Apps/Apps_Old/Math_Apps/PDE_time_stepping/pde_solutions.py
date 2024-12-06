from __future__ import division
import numpy as np

import pde_constants


def heat_analytical(f0, x, c_heat = pde_constants.heat_conductivity):
    """
    computes the analytical solution for the heat transport equation in 1D using fourier series ansatz. The fourier
    series approximation of the initial condition is computed using fast fourier transform.
    ASSUMPTION: left and right boundary are dirichlet boundary conditions!
    :param f0: analytical, functional expression for the initial condition, that can be evaluated for arbitrary x
    :param c_heat: heat transport coefficient
    :param x: spatial x values for evaluation (equally spaced!)
    :return u_x: functional expression of the solution of the heat transport equation at positions x for arbitrary times t
    """

    #todo also support Neumann boundary conditions!

    u0 = f0(x)

    u_lin = u0[0] * (np.max(x) - x) / (np.max(x) - np.min(x)) + u0[-1] * (x - np.min(x)) / (np.max(x) - np.min(x))
    u_hom = u0 - u_lin
    u_hom = np.concatenate([u_hom, -u_hom[-2:0:-1]])  # periodically extend function

    K = u_hom.__len__()

    c = np.fft.fft(u_hom)

    b = -2 * np.imag(c) / K
    a = 2 * np.real(c) / K
    K = int(K / 2) + 1
    b = b[:K]
    a = a[:K]

    w = np.max(x) - np.min(x)

    # numpy matrix version of code below
    """
    for k in range(K):
        kk = k * np.pi / w
        u += np.exp(-(kk**2)*(c_heat ** 2)*t) * (b[k] * np.sin(kk*x) + a[k] * np.cos(kk*x))
    """
    k = np.arange(K)
    kk = k * np.pi / w

    u_x = lambda t: u_lin - a[0] / 2 + \
                      np.sum(np.exp(-(kk ** 2) * (c_heat ** 2) * t) *
                             (b * np.sin(np.outer(x, kk)) + a * np.cos(np.outer(x, kk))),axis=1)
    return u_x


def wave_analytical(f0, x):
    """
    wrapper function for calling the appropriate analytical solution scheme.
    :param f0: analytical, functional expression for the initial condition, that can be evaluated for arbitrary x
    :param x: spatial x values for evaluation
    :return u_x: functional expression of the solution of the wave equation at positions x for arbitrary times t
    """
    c_wave = pde_constants.wave_number
    u_x = wave_dAlembert(f0, c_wave, x)
    return u_x


def wave_fourier(f0, c_wave, x):
    """
    computes the analytical solution for the wave equation in 1D using fourier series ansatz. The fourier
    series approximation of the initial condition is computed using fast fourier transform. The initial condition f0' is
    assumed to be equal to zero. For theory see 'Karpfinger: Rezepte'
	ASSUMPTION: left and right boundary are dirichlet boundary conditions!
    :param f0: analytical, functional expression for the initial condition, that can be evaluated for arbitrary x
    :param c_wave: wave travelling speed
    :param x: spatial x values for evaluation (equally spaced!)
    :return u_x: functional expression of the solution of the wave equation at positions x for arbitrary times t
    """
	
    #todo also support Neumann boundary conditions!	

    u0 = f0(x)

    u_lin = u0[0] * (np.max(x) - x) / (np.max(x) - np.min(x)) + u0[-1] * (x - np.min(x)) / (np.max(x) - np.min(x))
    u_hom = u0 - u_lin
    u_hom = np.concatenate([u_hom, -u_hom[-2:0:-1]])  # periodically extend function

    K = u_hom.__len__()

    c = np.fft.fft(u0)

    b = -2 * np.imag(c) / K
    a = 2 * np.real(c) / K
    K = int(K / 2) + 1
    b = b[:K]
    a = a[:K]

    w = np.max(x) - np.min(x)

    # numpy matrix version of code below
    """
    for k in range(K):
        kk = k * np.pi / w
        u += np.cos(kk * t  * c_wave) * (b[k] * np.sin(kk*x) + a[k] * np.cos(kk*x))
    """
    k = np.arange(K)
    kk = k * np.pi / w
    u_x = lambda t: u_lin + np.sum(np.cos(kk * t * c_wave) * (b * np.sin(np.outer(x, kk)) + a * np.cos(np.outer(x, kk))), axis=1)
    return u_x


def wave_dAlembert(f0, c_wave, x):
    """
    computes the analytical solution for the wave equation in 1D using d'Alemberts ansatz. The initial condition f0' is
    assumed to be equal to zero.
    http://www.jirka.org/diffyqs/htmlver/diffyqsse32.html
    :param f0: analytical, functional expression for the initial condition, that can be evaluated for arbitrary x
    :param c_wave: wave travelling speed
    :param x: spatial x values for evaluation
    :return u_x: functional expression of the solution of the wave equation at positions x for arbitrary times t
    """
    w = np.max(x) - np.min(x)

    f_lin = lambda arg: (f0(np.min(x)) * (np.max(x)-arg)/w) + (f0(np.max(x)) * (arg - np.min(x))/w)
    f_hom = lambda arg: f0(arg) - f_lin(arg)

    def u_x(t):
        x_r = (x - c_wave * t) % (2 * w)
        x_l = (x + c_wave * t) % (2 * w)
        sign_r = np.where((x_r > w), -1, 1)
        sign_l = np.where((x_l > w), -1, 1)
        x_r[x_r > w] = 2 * w - x_r[x_r > w]
        x_l[x_l > w] = 2 * w - x_l[x_l > w]

        u_r = (sign_r * f_hom(x_r))
        u_l = (sign_l * f_hom(x_l))
        return (u_r + u_l)*.5 + f_lin(x)

    return u_x


