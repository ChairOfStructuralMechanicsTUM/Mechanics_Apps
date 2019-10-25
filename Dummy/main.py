"""
Dummy App - shows some common concepts used in this project

"""
# general imports
import numpy as np
from math import sin, cos, pi, radians

# bokeh imports
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.models import ColumnDataSource, Slider

# internal imports

# latex integration
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv


#---------------------------------------------------------------------#

# constants
length_incl_line = 10


# data for the inclination example
line_coordinates = ColumnDataSource(data = dict(x=[0,length_incl_line],y=[0,0]))


# callback function to update line coordinates when changing alpha
def change_alpha(attr,old,new):  # attr, old, new ALWAYS needed to be interpreted correctly as callback function
    # update coordinates of the line to be displayed
    alpha_incl = radians(new)  # read the new value from the slider and transform it from deg to rad
                               # if one needs data from other sliders alpha_input.value would return the current value of the slider alpha_input
    line_coordinates.data['x'] = [0,cos(alpha_incl)*length_incl_line]
    line_coordinates.data['y'] = [0,sin(alpha_incl)*length_incl_line]





# inclination figure
inclination_plot = figure(title="", x_range=(-1,length_incl_line+1), y_range=(-1,length_incl_line+1), height=400, width=400, \
    toolbar_location="right", tools=["ywheel_zoom, pan, reset"]) # build the basic skeleton of the figure
inclination_plot.line(x='x', y='y', source=line_coordinates, color="#a2ad00") # plot the line based on the coordinates of the ColumnDataSource line_coordinates
inclination_plot.arc(x=[0], y=[0], radius=[10], start_angle=[0], end_angle=[0.5*pi], line_dash="dashed", color="gray") # TODO: check why the arc is plotted wrong -> aspect ratio
inclination_plot.toolbar.logo = None # removes the bokeh logo



alpha_input = Slider(title="alpha [°]", value=0.0, start=0.0, end=90.0, step=0.5, width=400)
alpha_input.on_change('value',change_alpha) # callback function called when alpha is changed in slider











# add app description
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)


# send to window
curdoc().add_root(column(description,
                         inclination_plot,
                         alpha_input)) # place all object at their desired position
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
