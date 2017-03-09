from __future__ import division

from os.path import dirname, join

import numpy as np
from numpy import sqrt, pi, cos, sin, exp
from scipy.special import fresnel


from bokeh.driving import count
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Div
from bokeh.models.layouts import Column, Row, Spacer
from bokeh.plotting import Figure

from surface3d import Surface3d
from contour import Contour

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
nx = 20
ny = 20
# Mesh parameters

x = np.linspace(-50,50,num=nx)
y = -1 * np.linspace(-50,50,num=nx)
xx, yy = np.meshgrid(x, y)
phi, R = cart2pol(xx, yy)
xx_lin = xx.ravel()
yy_lin = yy.ravel()

phi[phi < 0] += 2 * np.pi # map negative angle to positive angles

# Wave parameters
phi0 = pi/3.0
k = .1
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

content_filename = join(dirname(__file__), "description.html")

description = Div(text=open(content_filename).read(),
                  render_as_text=False, width=600)

source = ColumnDataSource()

surface = Surface3d(x="x", y="y", z="z", color="color", data_source=source)

# Generate a figure container for the field
plot = Figure(plot_height=300,
              plot_width=300,
              x_range=[-50,50],
              y_range=[-50,50])

contour = Contour(plot, line_width=1)

def compute(t):
    P = (1 + 1j) / 2.0 * (exp(1j * k * R * cos(phi - phi0)) * PHIPLUS + exp(1j * k * R * cos(phi + phi0)) * PHIMINUS) * exp(1j * omega * t)
    return P.real

@count()
def update(t):
    zz = compute(t)	
    source.data = dict(x=xx_lin, y=yy_lin, z=zz, color=zz)
    contour.set_contour_data(xx,yy,zz,isovalue=np.arange(-2,2,.1).tolist())	 


update(0)

curdoc().add_root(Row(Row(surface),Spacer(width=300),plot))
curdoc().add_periodic_callback(update, 100)
curdoc().title = "Surface3d"
