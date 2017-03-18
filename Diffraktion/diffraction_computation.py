import numpy as np
from numpy import sqrt, pi, cos, sin, exp
from scipy.special import fresnel


def cart2pol(x, y):
    """
    helper function for coordinate conversion of Cartesian to polar coordinates. See cart2pol in Matlab. From http://stackoverflow.com/a/26757297
    :param x: x values
    :param y: y values
    :return: radius rho and angle phi
    """
    rho = np.sqrt(x ** 2 + y ** 2)  # radius
    phi = np.arctan2(y, x)  # angle
    phi[phi < 0] += 2 * pi  # make all angles positive
    return rho, phi


def compute_fresnel_at_polar(rho, phi, phi0, wavelength):
    k = 2 * np.pi / wavelength  # wave number
    # Eq (3.4) Arguments of Fresnel Integrals are multiplied by sqrt(2 / pi) due to different definition of fresnels / c in matlab, use substitution to change between definitions...
    fresnels, fresnelc = fresnel(sqrt(2.0 / pi) * sqrt(2 * k * rho) * cos((phi - phi0) / 2.0))
    phiplus = (1 - 1j) / 2.0 + fresnelc - 1j * fresnels
    fresnels, fresnelc = fresnel(sqrt(2.0 / pi) * sqrt(2 * k * rho) * cos((phi + phi0) / 2.0))
    phiminus = (1 - 1j) / 2.0 + fresnelc - 1j * fresnels

    return phiplus, phiminus


def compute_fresnel_at_cart(x, y, phi0, wavelength):
    """
    evauate fresnel integrals on grid. The resulting variables are wave parameter specific, but constant over time
    :param x: x locations
    :param y: y locations
    :return:
    """
    # convert to polar coordinates
    phi, rho = cart2pol(x, y)

    return compute_fresnel_at_polar(rho, phi, phi0, wavelength)


def compute_wave_amplitude_at_cart(x, y, wavelength, phi0, c, t):
    """
    compute wave amplitude at time t and position (x,y)
    :param x: position x
    :param y: position y
    :param t: time
    :return: wave amplitude
    """

    rho, phi = cart2pol(x,y)

    return compute_wave_amplitude_at_polar(rho, phi, wavelength, phi0, c, t)


def compute_wave_amplitude_at_polar(rho, phi, wavelength, phi0, c, t):

    # compute parameter specific quantities
    phiplus, phiminus = compute_fresnel_at_polar(rho, phi, wavelength, phi0)

    return compute_wave_amplitude(rho, phi, phiplus, phiminus, wavelength, phi0, c, t)


def compute_wave_amplitude(rho, phi, phiplus, phiminus, wavelength, phi0, c, t):

    k = 2 * np.pi / wavelength  # wave number
    omega = 2 * np.pi * c / wavelength  # angular velocity

    # compute amplitude at time t from specific quantities
    p = (1 + 1j) / 2.0 * exp(1j * omega * t) * (exp(1j * k * rho * cos(phi - phi0)) * phiplus +
                                                exp(1j * k * rho * cos(phi + phi0)) * phiminus)

    return p.real