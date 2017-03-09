"""
Visualization of Diffraction with Python Bokeh
9.3.2017
Author: Benjamin Rüth
HiWi LST Baumechanik, TU München

Incident plane wave upon sound barrier. Solution from eq. (3.3) and (3.4) Technical Acoustics II

Code adopted from original Matlab file:

diffraction_anim.m
25.11.2014
Author: Christian Weineisen
LST Baumechanik, TU Muenchen
"""

import numpy as np
from numpy import sqrt, pi, linspace, meshgrid, cos, sin, exp
from scipy.special import fresnel
from __future__ import division

def cart2pol(x, y):
    """
    helper function for coordinate conversion of Cartesian to polar coordinates. See cart2pol in Matlab. From http://stackoverflow.com/a/26757297
    :param x: x values
    :param y: y values
    :return: angle and radius
    """
    rho = np.sqrt(x**2 + y**2) # radius
    phi = np.arctan2(y, x) # angle
    return phi, rho

# number of gridpoints in x and y direction
nx = 100
ny = 100
# Mesh parameters
x = linspace(-50,50,num=nx)
y = -1 * linspace(-50,50,num=nx)

X,Y = meshgrid(x,y)
phi, R = cart2pol(X, Y)

phi[phi < 0] += 2 * np.pi # map negative angle to positive angles

# Wave parameters
phi0 = pi/3.0
k = .4
c = 1

l = 2.0 * np.pi / k # wavelength
T = l / c # period
omega = 2 * np.pi * c / l # angular velocity

"""
Eq (3.4) Arguments of Fresnel Integrals are multiplied by sqrt(2 / pi) due to different definition of fresnels / c in matlab, use substitution to change between definitions...
"""

fresnels, fresnelc = fresnel(sqrt(2.0/pi) * sqrt(2 * k * R) * cos((phi - phi0) / 2.0))
PHIPLUS = (1 - 1j) / 2.0 + fresnelc - 1j * fresnels
fresnels, fresnelc = fresnel(sqrt(2.0/pi) * sqrt(2 * k * R) * cos((phi + phi0) / 2.0))
PHIMINUS = (1 - 1j) / 2.0 + fresnelc - 1j * fresnels

# create plot

# TODO MISSING!!!
Ylim = (min(y), max(y))
Xlim = (min(x), max(x))

# timesteps
nT = 100
trange = linspace(0, T, nT)

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as plt3d

# pre
fig = plt.figure()
plt.ion()

# loop timesteps
for t in trange:
    # EQ(3.3)
    P = (1 + 1j) / 2.0 * (exp(1j * k * R * cos(phi - phi0)) * PHIPLUS + exp(1j * k * R * cos(phi + phi0)) * PHIMINUS) * exp(1j * omega * t)

    # simple plotting with matplotlib
    contourlevels = np.arange(-3, 3, 0.1)
    plt.contour(X, Y, P.real, levels=contourlevels)
    """
    # 3d plotting with mplot3d
    ax = fig.add_subplot(111, projection='3d')
    #ax.scatter(X,Y,P.real,marker='.')
    ax.plot_surface(X, Y, P.real)
    ax.set_zlim(-3, 3)
    """
    # post
    plt.pause(0.01)
    plt.clf()