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
from quiver import Quiver

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
x_min, x_max = -50, 50
y_min, y_max = -50, 50
# Mesh parameters

x = np.linspace(x_min,x_max,num=nx)
y = np.linspace(y_min,y_max,num=ny)
xx, yy = np.meshgrid(x, y)
phi, R = cart2pol(xx, yy)

phi[phi < 0] += 2 * np.pi # map negative angle to positive angles

# Wave parameters
phi0_init = pi/3.0 # angle of incident
c = 1 # speed of sound
wavelength_init = 50 # wavelength

content_filename = join(dirname(__file__), "description.html")

description = Div(text=open(content_filename).read(),
                  render_as_text=False, width=600)

source = ColumnDataSource()
source_fresnel = ColumnDataSource()
source_checker = ColumnDataSource(data=dict(SliderHasChanged=[False]))
source_wavefront = ColumnDataSource()
source_wavelength = ColumnDataSource()
source_incoming_wave = ColumnDataSource()

source_reflection = ColumnDataSource()
source_light = ColumnDataSource()
source_shadow = ColumnDataSource()

phi0_slider = Slider(title="angle of incident", name='angle of incident', value=phi0_init, start=0, end=pi, step = .1*pi)
wavelength_slider = Slider(title="wavelength", name='wavelength', value=wavelength_init, start=0, end=100, step=1)

toolset = []
# Generate a figure container for the field
plot = Figure(plot_height=300,
              plot_width=330,
              x_range=[x_min,x_max],
              y_range=[y_min,y_max],
              x_axis_label='x',
              y_axis_label='y',
              tools=toolset)

contour = Contour(plot, line_width=1)
kvector = Quiver(plot, fix_at_middle=False)

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

def set_parameter_visualization():

    phi0 = phi0_slider.value
    wavelength = wavelength_slider.value
    length = (x_max - x_min)
    x0, y0 = 0.0, 0.0
    u, v = wavelength * cos(phi0+pi), wavelength * sin(phi0+pi)

    kvector.compute_quiver_data(np.array([[x0]]), np.array([[y0]]), np.array([[u]]), np.array([[v]]), h=wavelength, scaling=1)
    source_wavefront.data = dict(x=[+0.5 * length * cos(phi0+.5*pi), -0.5 * length * cos(phi0+.5*pi)],
                                 y=[+0.5 * length * sin(phi0+.5*pi), -0.5 * length * sin(phi0+.5*pi)])

    x_incoming = np.linspace(0,wavelength) * cos(phi0 + pi) + .2 * length * sin(phi0+pi) * np.sin(2.0*pi/wavelength * np.linspace(0,wavelength))
    y_incoming = np.linspace(0,wavelength) * sin(phi0 + pi) - .2 * length * cos(phi0+pi) * np.sin(2.0*pi/wavelength * np.linspace(0,wavelength))
    source_incoming_wave.data = dict(x=x_incoming,
                                     y=y_incoming)

    source_light.data = dict(x=[0, 2 * x_max*cos(phi0+pi), 2 * x_min, 2 * x_min, 2 * x_max*cos(phi0+pi)],
                             y=[0, 2 * y_max*sin(phi0), 10 * y_max, 10 * y_min, 2 * y_min*sin(phi0)])
    source_reflection.data = dict(x=[0, 2 * x_max, 2 * x_max, 2*x_min, 2 * x_max*cos(phi0+pi)],
                                  y=[0, 0, 10 * y_max, 10 * y_max, 2 * y_max*sin(phi0)])
    source_shadow.data = dict(x=[0, 2 * x_max * cos(phi0+pi), 2*x_min, 2*x_max, 2*x_max],
                              y=[0, 2 * y_min * sin(phi0), 10 * y_min, 10 * y_min, 0])

def set_slider_has_changed(attr, old, new):
    set_parameter_visualization()
    source_checker.data = dict(SliderHasChanged=[True])

def slider_has_changed():
    return source_checker.data['SliderHasChanged']

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
    contour.set_contour_data(xx,yy,zz,isovalue=[-2,-1,0,1,2])


def initialize():
    set_parameter_visualization()
    eval_fresnel()
    update(0)

initialize()

phi0_slider.on_change('value',set_slider_has_changed)
wavelength_slider.on_change('value',set_slider_has_changed)

surface = Surface3d(x="x", y="y", z="z", color="color", data_source=source)

plot.line(x=[x_min,0], y=[0,0], line_dash='dashed')
plot.line(x=[x_max,0], y=[0,0], line_width=10)
plot.line(x='x', y='y', source=source_wavefront)
plot.line(x='x', y='y', source=source_incoming_wave, line_dash='dashed')
plot.patch(x='x', y='y', color='yellow', source=source_light, alpha=.1)
plot.patch(x='x', y='y', color='red',source=source_reflection, alpha=.1)
plot.patch(x='x', y='y', color='blue', source=source_shadow, alpha=.1)


controls = Column(phi0_slider,wavelength_slider)
curdoc().add_root(Column(Row(Row(surface),Spacer(width=300),plot),controls))
curdoc().add_periodic_callback(update, 200)
curdoc().title = "Surface3d"