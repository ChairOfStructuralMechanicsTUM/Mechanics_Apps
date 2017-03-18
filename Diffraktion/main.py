from __future__ import division

from os.path import dirname, join

import numpy as np
from numpy import pi, cos, sin
import time

from bokeh.driving import count
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Div
from bokeh.layouts import widgetbox, row, column
from bokeh.models.layouts import Spacer
from bokeh.plotting import Figure
from bokeh.models.widgets import Slider, TextInput

from surface3d import Surface3d
from contour import Contour
from quiver import Quiver
from clickInteractor import ClickInteractor

from diffraction_grid import Grid
from diffraction_computation import compute_wave_amplitude_at_cart

# number of gridpoints in x and y direction
nx_surface = 20  # resolution surface plot
ny_surface = 20
nx_contour = 50  # resolution contour plot
ny_contour = 50
x_min, x_max = -50, 50  # x extend of domain
y_min, y_max = -50, 50  # y extend of domain

# initialize diffraction grids
contour_grid = Grid(x_min, x_max, nx_contour, y_min, y_max, ny_contour)
surface_grid = Grid(x_min, x_max, nx_surface, y_min, y_max, ny_surface)

# Wave parameters
phi0_init = pi/3.0  # angle of incident
c = 4  # speed of sound
wavelength_init = 50  # wavelength

# data sources
# data source for surface plot
source_surf = ColumnDataSource(data=dict(x=[], y=[], z=[], color=[]))
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
wavelength_slider = Slider(title="wavelength", name='wavelength', value=wavelength_init, start=10, end=100, step=5)
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


def update_fresnel_on_grids():
    """
    called, if wave parameters are changed. Specific quantities have to be updated for the grids corresponding to the
    contour and the surface plot.
    :return:
    """

    # read wave parameters
    phi0 = phi0_slider.value
    wavelength = wavelength_slider.value
    # if wave parameters have changed, we have to recompute the specific quantities
    contour_grid.set_wave_parameters(phi0, wavelength, c)
    surface_grid.set_wave_parameters(phi0, wavelength, c)


def update_wave_amplitude_on_grids(t):
    """
    Compute wave amplitude for time t on surface plot and contour plot grid. Wave parameter specific quantities are
    reused, if the wave parameters are unchanged.
    :param t: time
    :return:
    """
    if slider_has_changed():
        update_fresnel_on_grids()
        source_checker.data = dict(SliderHasChanged=[False])

    # Surf Mesh
    p_surf = surface_grid.compute_wave_amplitude(t)
    source_surf.data = dict(x=surface_grid._x.ravel(), y=surface_grid._y.ravel(), z=p_surf.ravel(), color=p_surf.ravel())

    # Contour Mesh
    p_cont = contour_grid.compute_wave_amplitude(t)
    contour_zero.set_contour_data(contour_grid._x, contour_grid._y, p_cont, isovalue=[0])
    contour_all.set_contour_data(contour_grid._x, contour_grid._y, p_cont, isovalue=[-2,-1.5,-1,-.5]+[+.5,+1,+1.5,+2])


def update_wave_amplitude_at_probe(x,y,t):
    # read wave parameters
    phi0 = phi0_slider.value
    wavelength = wavelength_slider.value
    x = np.array([[x]])
    y = np.array([[y]])
    z_val = compute_wave_amplitude_at_cart(x, y, wavelength, phi0, c, t)
    textbox.value = str(z_val[0,0]) + " dB"  # write measured value to textbox


target_frame_time = 200  # we update the app after x milliseconds. If computation takes longer than this time, the app lags.
frame_end_time = 0
lagcount = 0


def do_time_measurement(frame_no, computation_time):
    global lagcount, frame_end_time

    this_frame_end_time = time.time() * 1000  # in ms
    frame_duration = (this_frame_end_time - frame_end_time)

    if (frame_duration > 1.5 * target_frame_time) or (computation_time > target_frame_time):
        print " "
        print "high lag observed for frame %s. Frame Target: %s ms, Frame Real: %s ms, Computation: %s ms" % (
        frame_no, target_frame_time, frame_duration, computation_time)
        lagcount += 1
        lagfraction = lagcount / (frame_no + 1)
        if lagfraction > 0.1 and frame_no > 100:
            print "WARNING! more than 10% of the frames are lost. Consider increasing TARGET_FRAME_TIME to avoid lags!"
    if (computation_time < .5 * target_frame_time) and (target_frame_time > 40):
        print " "
        print "Frame Target: %s ms, Frame Real: %s ms, Computation: %s ms" % (
        target_frame_time, frame_duration, computation_time)
        print "Computation time is much lower than frame time and framerate is below 25Hz. Consider decreasing TARGET_FRAME_TIME to improve user experience!"

    frame_end_time = this_frame_end_time


@count()
def update(frame_no):
    """
    called regularly by periodic update
    :param t: time
    :return:
    """   
    t = frame_no * target_frame_time / 1000.0
    computation_start_time = time.time()

    ######## computation kernel

    update_wave_amplitude_on_grids(t)

    x, y = interactor.clicked_point()
    if x is not None:  # valid position has been clicked
        update_wave_amplitude_at_probe(x,y,t)
    else:
        textbox.value = "pick a location for measurement"

    ########

    computation_time = (time.time() - computation_start_time) * 1000

    do_time_measurement(frame_no, computation_time)

   
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
contour_zero = Contour(plot, line_width=2,line_color='black', path_filter = 10)  # zero level
contour_all = Contour(plot, line_width=1, path_filter = 10)  # some other levels

kvector = Quiver(plot, fix_at_middle=False) # visualization of wave k vector
plot.line(x=[x_min,0], y=[0,0], line_dash='dashed')
plot.line(x=[x_max,0], y=[0,0], line_width=10)  # the wall
plot.line(x='x', y='y', source=source_wavefront)  # wavefront visualization
plot.patch(x='x', y='y', color='yellow', source=source_light, alpha=.1)  # light area
plot.patch(x='x', y='y', color='red',source=source_reflection, alpha=.1)  # reflection area
plot.patch(x='x', y='y', color='blue', source=source_shadow, alpha=.1)  # shadow area
plot.scatter(x='x',y='y', source=source_value_plotter, size=10)  # value probing

initialize()

# add app description
description_filename = join(dirname(__file__), "description.html")

description = Div(text=open(description_filename).read(), render_as_text=False, width=700)

# add area image
area_image = Div(text="""
<p>
<img src="/Diffraktion/static/images/Diffraktion_areas.jpg" width=250>
</p>
<p>
Characteristic regions and wave parameters
</p>""", render_as_text=False, width=350)

# create layout
controls = widgetbox(phi0_slider,wavelength_slider,textbox,width=300)  # all controls
curdoc().add_root(column(description,row(row(Spacer(width=25),surface,Spacer(width=325)),plot),row(Spacer(width=25),controls,Spacer(width=65),area_image)))  # add plots and controls to root
curdoc().add_periodic_callback(update, target_frame_time)  # update function
curdoc().title = "Diffraktion"
