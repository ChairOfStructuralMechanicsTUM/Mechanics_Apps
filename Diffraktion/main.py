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
from bokeh.models.widgets import Slider

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

phi[phi < 0] += 2 * np.pi # map negative angle to positive angles

# Wave parameters
phi0_init = pi/3.0 # angle of incident
c = 1 # speed of sound
wavelength_init = 100 # wavelength

content_filename = join(dirname(__file__), "description.html")

description = Div(text=open(content_filename).read(),
                  render_as_text=False, width=600)

source = ColumnDataSource()
source_fresnel = ColumnDataSource()
source_checker = ColumnDataSource(data=dict(SliderHasChanged=[False]))

phi0_slider = Slider(title="angle of incident", name='angle of incident', value=phi0_init, start=0, end=pi, step = .1*pi)
wavelength_slider = Slider(title="wavelength", name='wavelength', value=wavelength_init, start=0, end=100, step=1)

def eval_fresnel():
    phi0 = phi0_slider.value
    wavelength = wavelength_slider.value
    k = 2 * np.pi / wavelength  # wave number
    """
    Eq (3.4) Arguments of Fresnel Integrals are multiplied by sqrt(2 / pi) due to different definition of fresnels / c in matlab, use substitution to change between definitions...
    """
    fresnels, fresnelc = fresnel(sqrt(2.0 / pi) * sqrt(2 * k * R) * cos((phi - phi0) / 2.0))
    phiplus = (1 - 1j) / 2.0 + fresnelc - 1j * fresnels
    fresnels, fresnelc = fresnel(sqrt(2.0 / pi) * sqrt(2 * k * R) * cos((phi + phi0) / 2.0))
    phiminus = (1 - 1j) / 2.0 + fresnelc - 1j * fresnels

    source_fresnel.data = dict(PhiPlus=phiplus, PhiMinus=phiminus)

def set_slider_has_changed(attr, old, new):
    source_checker.data = dict(SliderHasChanged=[True])

def slider_has_changed():
    return source_checker.data['SliderHasChanged']

phi0_slider.on_change('value',set_slider_has_changed)
wavelength_slider.on_change('value',set_slider_has_changed)

surface = Surface3d(x="x", y="y", z="z", color="color", data_source=source)

toolset = []
# Generate a figure container for the field
plot = Figure(plot_height=300,
              plot_width=300,
              x_range=[-50,50],
              y_range=[-50,50],
              tools=toolset)

contour = Contour(plot, line_width=1)


def compute(t):
    phi0 = phi0_slider.value
    wavelength = wavelength_slider.value
    k = 2 * np.pi / wavelength  # wave number
    omega = 2 * np.pi * c / wavelength  # angular velocity

    if slider_has_changed():
        eval_fresnel()

    phiplus = source_fresnel.data['PhiPlus']
    phiname = source_fresnel.data['PhiMinus']

    p = (1 + 1j) / 2.0 * (exp(1j * k * R * cos(phi - phi0)) * phiplus + exp(1j * k * R * cos(phi + phi0)) * phiname) * exp(1j * omega * t)
    return p.real

@count()
def update(t):
    zz = compute(t)	
    source.data = dict(x=xx.ravel(), y=yy.ravel(), z=zz.ravel(), color=zz.ravel())
    contour.set_contour_data(xx,yy,zz,isovalue=np.arange(-2,2,.1).tolist())	 


def initialize():
    eval_fresnel()
    update(0)

initialize()
controls = Column(phi0_slider,wavelength_slider)
curdoc().add_root(Column(Row(Row(surface),Spacer(width=300),plot),controls))
curdoc().add_periodic_callback(update, 500)
curdoc().title = "Surface3d"