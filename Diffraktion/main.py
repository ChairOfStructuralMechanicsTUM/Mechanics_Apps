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
from bokeh.models.widgets import Slider, TextInput

from surface3d import Surface3d
from contour import Contour
from quiver import Quiver
from clickInteractor import ClickInteractor


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
nx_surf = 20
ny_surf = 20
nx_contour = 50
ny_contour = 50
x_min, x_max = -50, 50
y_min, y_max = -50, 50

# Wave parameters
phi0_init = pi/3.0  # angle of incident
c = 1  # speed of sound
wavelength_init = 50  # wavelength

content_filename = join(dirname(__file__), "description.html")

description = Div(text=open(content_filename).read(),
                  render_as_text=False, width=600)

source_surf = ColumnDataSource()
source_fresnel_surf = ColumnDataSource()
source_fresnel_cont = ColumnDataSource()
source_checker = ColumnDataSource(data=dict(SliderHasChanged=[False]))
source_wavefront = ColumnDataSource(data=dict(x=[], y=[]))
source_wavelength = ColumnDataSource(data=dict(x=[], y=[]))
source_value_plotter = ColumnDataSource(data=dict(x=[], y=[]))

source_reflection = ColumnDataSource(data=dict(x=[], y=[]))
source_light = ColumnDataSource(data=dict(x=[], y=[]))
source_shadow = ColumnDataSource(data=dict(x=[], y=[]))

phi0_slider = Slider(title="angle of incident", name='angle of incident', value=phi0_init, start=0, end=pi, step=.1*pi)
wavelength_slider = Slider(title="wavelength", name='wavelength', value=wavelength_init, start=0, end=100, step=1)
textbox = TextInput(title="noise probe", name='noise probe')

toolset = ["crosshair, save, tap"]
# Generate a figure container for the field
plot = Figure(plot_height=300,
              plot_width=330,
              x_range=[x_min,x_max],
              y_range=[y_min,y_max],
              x_axis_label='x',
              y_axis_label='y',
              tools=toolset)

contour_zero = Contour(plot, line_width=2,line_color='black')
contour_all = Contour(plot, line_width=1)
kvector = Quiver(plot, fix_at_middle=False)
interactor = ClickInteractor(plot)


def eval_fresnel_at(x, y):
    phi, rho = cart2pol(x, y)
    phi[phi<0] += 2*pi  # make all angles positive
    phi0 = phi0_slider.value
    wavelength = wavelength_slider.value
    k = 2 * np.pi / wavelength  # wave number
    """
    Eq (3.4) Arguments of Fresnel Integrals are multiplied by sqrt(2 / pi) due to different definition of fresnels / c in matlab, use substitution to change between definitions...
    """
    fresnels, fresnelc = fresnel(sqrt(2.0 / pi) * sqrt(2 * k * rho) * cos((phi - phi0) / 2.0))
    phiplus = (1 - 1j) / 2.0 + fresnelc - 1j * fresnels
    fresnels, fresnelc = fresnel(sqrt(2.0 / pi) * sqrt(2 * k * rho) * cos((phi + phi0) / 2.0))
    phiminus = (1 - 1j) / 2.0 + fresnelc - 1j * fresnels

    return phiplus, phiminus, rho, phi


def set_parameter_visualization():
    phi0 = phi0_slider.value
    wavelength = wavelength_slider.value
    length = (x_max - x_min)
    x0, y0 = 0.0, 0.0
    u, v = wavelength * cos(phi0+pi), wavelength * sin(phi0+pi)

    kvector.compute_quiver_data(np.array([[x0]]), np.array([[y0]]), np.array([[u]]), np.array([[v]]), h=wavelength, scaling=1)
    source_wavefront.data = dict(x=[+0.5 * length * cos(phi0+.5*pi), -0.5 * length * cos(phi0+.5*pi)],
                                 y=[+0.5 * length * sin(phi0+.5*pi), -0.5 * length * sin(phi0+.5*pi)])
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
    return source_checker.data['SliderHasChanged'][0]


def on_click_change(attr,old,new):
    x,y = interactor.clicked_point()
    print "("+str(x)+","+str(y)+")"
    if x is not None:
        source_value_plotter.data = dict(x=[x], y=[y])


def compute_wave_amplitude(source_fresnel, t):
    phi0 = phi0_slider.value
    wavelength = wavelength_slider.value
    k = 2 * np.pi / wavelength  # wave number
    omega = 2 * np.pi * c / wavelength  # angular velocity

    rho = source_fresnel.data['Rho']
    phi = source_fresnel.data['Phi']
    phiplus = source_fresnel.data['PhiPlus']
    phiminus = source_fresnel.data['PhiMinus']
    p = (1 + 1j) / 2.0 * exp(1j * omega * t) * (exp(1j * k * rho * cos(phi - phi0)) * phiplus +
                                                exp(1j * k * rho * cos(phi + phi0)) * phiminus)

    return p.real


def update_fresnel_on_grids():
    # Surf Mesh
    x_surf_mesh, y_surf_mesh = np.meshgrid(np.linspace(x_min, x_max, num=nx_surf),
                                           np.linspace(y_min, y_max, num=ny_surf))

    phiplus_surf, phiminus_surf, rho_surf, phi_surf = eval_fresnel_at(x_surf_mesh, y_surf_mesh)
    source_fresnel_surf.data = dict(PhiPlus=phiplus_surf, PhiMinus=phiminus_surf, Rho=rho_surf, Phi=phi_surf)

    # Contour Mesh
    x_cont_mesh, y_cont_mesh = np.meshgrid(np.linspace(x_min, x_max, num=nx_contour),
                                           np.linspace(y_min, y_max, num=ny_contour))

    phiplus_cont, phiminus_cont, rho_cont, phi_cont = eval_fresnel_at(x_cont_mesh, y_cont_mesh)
    source_fresnel_cont.data = dict(PhiPlus=phiplus_cont, PhiMinus=phiminus_cont, Rho=rho_cont, Phi=phi_cont)


def compute(t):

    if slider_has_changed():
        update_fresnel_on_grids()
        source_checker.data = dict(SliderHasChanged=[False])

    # Surf Mesh
    x_surf_mesh, y_surf_mesh = np.meshgrid(np.linspace(x_min, x_max, num=nx_surf),
                                           np.linspace(y_min, y_max, num=ny_surf))

    p_surf = compute_wave_amplitude(source_fresnel_surf, t)

    source_surf.data = dict(x=x_surf_mesh.ravel(), y=y_surf_mesh.ravel(), z=p_surf.ravel(), color=p_surf.ravel())


    # Contour Mesh
    x_cont_mesh, y_cont_mesh = np.meshgrid(np.linspace(x_min, x_max, num=nx_contour),
                                           np.linspace(y_min, y_max, num=ny_contour))

    p_cont = compute_wave_amplitude(source_fresnel_cont, t)

    contour_zero.set_contour_data(x_cont_mesh,y_cont_mesh,p_cont,isovalue=[0])
    contour_all.set_contour_data(x_cont_mesh,y_cont_mesh,p_cont,isovalue=[-2,-1.5,-1,-.5]+[+.5,+1,+1.5,+2])


def compute_at(x, y, t):
    phi0 = phi0_slider.value
    wavelength = wavelength_slider.value
    k = 2 * np.pi / wavelength  # wave number
    omega = 2 * np.pi * c / wavelength  # angular velocity

    phiplus, phiminus, phi, rho = eval_fresnel_at(np.array([x]),np.array([y]))

    p = (1 + 1j) / 2.0 * exp(1j * omega * t) * (exp(1j * k * rho * cos(phi - phi0)) * phiplus +
                                                exp(1j * k * rho * cos(phi + phi0)) * phiminus)
    return p.real[0]


@count()
def update(t):
    compute(t)

    x, y = interactor.clicked_point()
    if x is not None:
        z_val = compute_at(x, y, t)
        textbox.value = str(z_val)+" dB"
    else:
        textbox.value = "pick a location for measurement"


def initialize():
    set_parameter_visualization()

    source_checker.data = dict(SliderHasChanged=[True])

    update(0)

initialize()

phi0_slider.on_change('value',set_slider_has_changed)
wavelength_slider.on_change('value',set_slider_has_changed)
interactor.on_click(on_click_change)

surface = Surface3d(x="x", y="y", z="z", color="color", data_source=source_surf)

plot.line(x=[x_min,0], y=[0,0], line_dash='dashed')
plot.line(x=[x_max,0], y=[0,0], line_width=10)
plot.line(x='x', y='y', source=source_wavefront)
plot.patch(x='x', y='y', color='yellow', source=source_light, alpha=.1)
plot.patch(x='x', y='y', color='red',source=source_reflection, alpha=.1)
plot.patch(x='x', y='y', color='blue', source=source_shadow, alpha=.1)
plot.scatter(x='x',y='y', source=source_value_plotter, size=10)


controls = Column(phi0_slider,wavelength_slider,textbox)
curdoc().add_root(Column(Row(Row(surface),Spacer(width=300),plot),controls))
curdoc().add_periodic_callback(update, 200)
curdoc().title = "Diffraktion"
