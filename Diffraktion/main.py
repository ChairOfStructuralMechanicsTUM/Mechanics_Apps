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
nx_surf = 20  # resolution surface plot
ny_surf = 20
nx_contour = 50  # resolution contour plot
ny_contour = 50
x_min, x_max = -50, 50  # x extend of domain
y_min, y_max = -50, 50  # y extend of domain

# Wave parameters
phi0_init = pi/3.0  # angle of incident
c = 1  # speed of sound
wavelength_init = 50  # wavelength

# data sources
# data source for surface plot
source_surf = ColumnDataSource(data=dict(x=[], y=[], z=[], color=[]))
# static variables for of wave amplitude (surface plot)
source_fresnel_surf = ColumnDataSource(data=dict(PhiPlus=[], PhiMinus=[], Rho=[], Phi=[]))
# static variables for of wave amplitude (contour plot)
source_fresnel_cont = ColumnDataSource(data=dict(PhiPlus=[], PhiMinus=[], Rho=[], Phi=[]))
# global variable that is set if a slider is changed
source_checker = ColumnDataSource(data=dict(SliderHasChanged=[False]))
# defines wavefront of plane wave
source_wavefront = ColumnDataSource(data=dict(x=[], y=[]))
# visualization of click location
source_value_plotter = ColumnDataSource(data=dict(x=[], y=[]))

# sources for the different areas
# reflection area
source_reflection = ColumnDataSource(data=dict(x=[], y=[]))
# light area
source_light = ColumnDataSource(data=dict(x=[], y=[]))
# shadow area
source_shadow = ColumnDataSource(data=dict(x=[], y=[]))

# interactive widgets
# slider for setting angle of incident
phi0_slider = Slider(title="angle of incident", name='angle of incident', value=phi0_init, start=0, end=pi, step=.1*pi)
# slider for setting wavelength
wavelength_slider = Slider(title="wavelength", name='wavelength', value=wavelength_init, start=0, end=100, step=1)
# textbox for displaying dB value at proble location
textbox = TextInput(title="noise probe", name='noise probe')

# Generate a figure container for the field
plot = Figure(plot_height=300,
              plot_width=330,
              x_range=[x_min,x_max],
              y_range=[y_min,y_max],
              x_axis_label='x',
              y_axis_label='y',
              tools=["crosshair, save, tap"])

# create interactor that detects click location in plot
interactor = ClickInteractor(plot)

def eval_fresnel_at(x, y):
    """
    evauate fresnel integrals on grid. The resulting variables are wave parameter specific, but constant over time
    :param x: x locations
    :param y: y locations
    :return:
    """
    # convert to polar coordinates
    phi, rho = cart2pol(x, y)
    phi[phi<0] += 2*pi  # make all angles positive

    # read wave parameters
    phi0 = phi0_slider.value
    wavelength = wavelength_slider.value
    k = 2 * np.pi / wavelength  # wave number

    # Eq (3.4) Arguments of Fresnel Integrals are multiplied by sqrt(2 / pi) due to different definition of fresnels / c in matlab, use substitution to change between definitions...
    fresnels, fresnelc = fresnel(sqrt(2.0 / pi) * sqrt(2 * k * rho) * cos((phi - phi0) / 2.0))
    phiplus = (1 - 1j) / 2.0 + fresnelc - 1j * fresnels
    fresnels, fresnelc = fresnel(sqrt(2.0 / pi) * sqrt(2 * k * rho) * cos((phi + phi0) / 2.0))
    phiminus = (1 - 1j) / 2.0 + fresnelc - 1j * fresnels

    return phiplus, phiminus, rho, phi


def set_parameter_visualization():
    """
    compute visualization of input parameters and update corresponding data sources. We visualize the following:
    * k vector of the wave with a quiver plot
    * wave front orientation with a line
    * different areas (reflection, light, shadow) through colored patches
    :return:
    """

    # get wave parameters
    phi0 = phi0_slider.value
    wavelength = wavelength_slider.value
    length = (x_max - x_min)

    # visualization of k vector
    x0, y0 = 0.0, 0.0  # origin of k-vector
    u, v = wavelength * cos(phi0+pi), wavelength * sin(phi0+pi)  # length and direction of k vector
    kvector.compute_quiver_data(np.array([[x0]]), np.array([[y0]]), np.array([[u]]), np.array([[v]]), h=wavelength, scaling=1)

    # visualization of wavefront
    x0_wavefront, y0_wavefront = 0.0, 0.0  # center of wavefront
    source_wavefront.data = dict(x=[x0_wavefront+0.5 * length * cos(phi0+.5*pi), x0_wavefront-0.5 * length * cos(phi0+.5*pi)],
                                 y=[y0_wavefront+0.5 * length * sin(phi0+.5*pi), y0_wavefront-0.5 * length * sin(phi0+.5*pi)])

    # visualization of areas
    source_light.data = dict(x=[0, 2 * x_max*cos(phi0+pi), 2 * x_min, 2 * x_min, 2 * x_max*cos(phi0+pi)],
                             y=[0, 2 * y_max*sin(phi0), 10 * y_max, 10 * y_min, 2 * y_min*sin(phi0)])
    source_reflection.data = dict(x=[0, 2 * x_max, 2 * x_max, 2*x_min, 2 * x_max*cos(phi0+pi)],
                                  y=[0, 0, 10 * y_max, 10 * y_max, 2 * y_max*sin(phi0)])
    source_shadow.data = dict(x=[0, 2 * x_max * cos(phi0+pi), 2*x_min, 2*x_max, 2*x_max],
                              y=[0, 2 * y_min * sin(phi0), 10 * y_min, 10 * y_min, 0])


def set_slider_has_changed(attr, old, new):
    """
    if slider has changed, this function is called
    :param attr:
    :param old:
    :param new:
    :return:
    """
    set_parameter_visualization()
    source_checker.data = dict(SliderHasChanged=[True])


def slider_has_changed():
    """
    returns true, if any slider has been changed since the last call of update(t)
    :return: bool
    """
    return source_checker.data['SliderHasChanged'][0]


def on_click_change(attr,old,new):
    """
    called, if user clicks in plot
    :param attr:
    :param old:
    :param new:
    :return:
    """
    x, y = interactor.clicked_point()  # clicked point location
    if x is not None:
        source_value_plotter.data = dict(x=[x], y=[y])  # update visualization of clicked point


def compute_wave_amplitude(source_fresnel, t):
    """
    computes wave amplitude at time t from wave parameter specific quantities saved in source_fresnel
    :param source_fresnel: data source holding wave parameter specific quantities
    :param t: time
    :return: wave amplitude
    """

    # wave parameters
    phi0 = phi0_slider.value
    wavelength = wavelength_slider.value
    k = 2 * np.pi / wavelength  # wave number
    omega = 2 * np.pi * c / wavelength  # angular velocity

    # load static grid parameters
    rho = source_fresnel.data['Rho']
    phi = source_fresnel.data['Phi']
    phiplus = source_fresnel.data['PhiPlus']
    phiminus = source_fresnel.data['PhiMinus']

    # amplitude at time t
    p = (1 + 1j) / 2.0 * exp(1j * omega * t) * (exp(1j * k * rho * cos(phi - phi0)) * phiplus +
                                                exp(1j * k * rho * cos(phi + phi0)) * phiminus)

    return p.real


def update_fresnel_on_grids():
    """
    called, if wave parameters are changed. Specific quantities have to be updated for the grids corresponding to the
    contour and the surface plot.
    :return:
    """
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


def compute_wave_amplitude_on_grids(t):
    """
    Compute wave amplitude for time t on surface plot and contour plot grid. Wave parameter specific quantities are
    reused, if the wave parameters are unchanged.
    :param t: time
    :return:
    """

    if slider_has_changed():
        # if wave parameters have changed, we have to recompute the specific quantities
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


def compute_wave_amplitude_at(x, y, t):
    """
    compute wave amplitude at time t and position (x,y)
    :param x: position x
    :param y: position y
    :param t: time
    :return: wave amplitude
    """

    # get wave parameters
    phi0 = phi0_slider.value
    wavelength = wavelength_slider.value
    k = 2 * np.pi / wavelength  # wave number
    omega = 2 * np.pi * c / wavelength  # angular velocity

    # compute parameter specific quantities
    phiplus, phiminus, phi, rho = eval_fresnel_at(np.array([x]),np.array([y]))

    # compute amplitude at time t from specific quantities
    p = (1 + 1j) / 2.0 * exp(1j * omega * t) * (exp(1j * k * rho * cos(phi - phi0)) * phiplus +
                                                exp(1j * k * rho * cos(phi + phi0)) * phiminus)
    return p.real[0]


@count()
def update(t):
    """
    called regularly by periodic update
    :param t: time
    :return:
    """
    compute_wave_amplitude_on_grids(t)

    x, y = interactor.clicked_point()
    if x is not None:  # valid position has been clicked
        z_val = compute_wave_amplitude_at(x, y, t)
        textbox.value = str(z_val)+" dB"  # write measured value to textbox
    else:
        textbox.value = "pick a location for measurement"


def initialize():
    """
    initialize app
    :return:
    """
    set_parameter_visualization()
    source_checker.data = dict(SliderHasChanged=[True])
    update(0)


# add callback beahviour
phi0_slider.on_change('value',set_slider_has_changed)
wavelength_slider.on_change('value',set_slider_has_changed)
interactor.on_click(on_click_change)

# create plots
surface = Surface3d(x="x", y="y", z="z", color="color", data_source=source_surf)  # wave surface
# contour plots of wave
contour_zero = Contour(plot, line_width=2,line_color='black')  # zero level
contour_all = Contour(plot, line_width=1)  # some other levels

kvector = Quiver(plot, fix_at_middle=False) # visualization of wave k vector
plot.line(x=[x_min,0], y=[0,0], line_dash='dashed')
plot.line(x=[x_max,0], y=[0,0], line_width=10)  # the wall
plot.line(x='x', y='y', source=source_wavefront)  # wavefront visualization
plot.patch(x='x', y='y', color='yellow', source=source_light, alpha=.1)  # light area
plot.patch(x='x', y='y', color='red',source=source_reflection, alpha=.1)  # reflection area
plot.patch(x='x', y='y', color='blue', source=source_shadow, alpha=.1)  # shadow area
plot.scatter(x='x',y='y', source=source_value_plotter, size=10)  # value probing

initialize()

# create layout
controls = Column(phi0_slider,wavelength_slider,textbox)  # all controls
curdoc().add_root(Column(Row(Row(surface),Spacer(width=300),plot),controls))  # add plots and controls to root
curdoc().add_periodic_callback(update, 200)  # update function
curdoc().title = "Diffraktion"
