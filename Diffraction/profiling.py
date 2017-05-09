from __future__ import division

import profile
from main import update, initialize
from numpy import pi, cos, sin
from bokeh.models import ColumnDataSource, Div
from bokeh.plotting import Figure
from bokeh.models.widgets import Slider, TextInput

from surface3d import Surface3d
from contour import Contour
from clickInteractor import ClickInteractor

from diffraction_grid import Grid

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
phi0_init = pi / 3.0  # angle of incident
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
phi0_slider = Slider(title="angle of incident", name='angle of incident', value=phi0_init, start=0, end=pi,
                     step=.1 * pi)
# slider for setting wavelength
wavelength_slider = Slider(title="wavelength", name='wavelength', value=wavelength_init, start=10, end=100, step=5)
# textbox for displaying dB value at proble location
textbox = TextInput(title="noise probe", name='noise probe')

# Generate a figure container for the field
plot = Figure(plot_height=300,
              plot_width=330,
              x_range=[x_min, x_max],
              y_range=[y_min, y_max],
              x_axis_label='x',
              y_axis_label='y',
              tools=["crosshair, save, tap"])

# create interactor that detects click location in plot
interactor = ClickInteractor(plot)

# create plots
surface = Surface3d(x="x", y="y", z="z", color="color", data_source=source_surf)  # wave surface
# contour plots of wave
contour_zero = Contour(plot, line_width=2, line_color='black', path_filter=10)  # zero level
contour_all = Contour(plot, line_width=1, path_filter=10)  # some other levels

initialize()

for i in range(10):
    update(i)