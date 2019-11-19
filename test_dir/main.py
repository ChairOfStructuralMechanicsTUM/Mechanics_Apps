"""
Python Bokeh program which interactively changes two vectors and displays their sum

"""
from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider, Button
from bokeh.io import curdoc
from math import sin, cos, pi, radians



from os.path import dirname, join, abspath # no split required, managed in strings.json
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir  = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexLabel




# constants
length_incl_line = 10


# data for the inclination example
line_coordinates = ColumnDataSource(data = dict(x=[0,length_incl_line],y=[0,0]))


# callback function to update line coordinates when changing alpha
def change_alpha(attr,old,new):  # attr, old, new ALWAYS needed to be interpreted correctly as a callback function for sliders
    # update coordinates of the line to be displayed
    alpha_incl = radians(new)  # read the new value from the slider and transform it from deg to rad
                               # if one needs data from other sliders alpha_input.value would return the current value of the slider alpha_input
    line_coordinates.data['x'] = [0,cos(alpha_incl)*length_incl_line]
    line_coordinates.data['y'] = [0,sin(alpha_incl)*length_incl_line]


# inclination figure
inclination_plot = figure(title="Inclination", x_range=(-1,length_incl_line+1), y_range=(-1,length_incl_line+1), height=400, width=400, \
    toolbar_location="right", tools=["ywheel_zoom, pan, reset, save"], output_backend="svg") # build the basic skeleton of the figure
inclination_plot.line(x='x', y='y', source=line_coordinates, color="#a2ad00") # plot the line based on the coordinates of the ColumnDataSource line_coordinates
inclination_plot.arc(x=[0], y=[0], radius=[10], start_angle=[0], end_angle=[0.5*pi], line_dash="dashed", color="gray") # TODO: check why the arc is plotted wrong -> aspect ratio
inclination_plot.toolbar.logo = None # removes the bokeh logo
inclination_plot.match_aspect = True # does not work, arc is still wrong; # with title it is better -> title counts to hight
# also: arc grows when using the ywheel_zoom



alpha_input = Slider(title="alpha [°]", value=0.0, start=0.0, end=90.0, step=0.5, width=400) # build the slider (without LaTeX)
#alpha_input = LatexSlider(title="\\alpha [°]", value=0.0, start=0.0, end=90.0, step=0.5, width=400) # build the slider (with LaTeX supported)
alpha_input.on_change('value',change_alpha) # callback function called when alpha is changed in slider





latex = LatexLabel(text="f = \sum_{n=1}^\infty\\frac{-e^{i\pi}}{2^n}!",
                   x=6, y=6,
                   render_mode='css', text_font_size='10pt',
                   background_fill_alpha=0)
inclination_plot.add_layout(latex)





## Send to window
curdoc().add_root(column(inclination_plot, alpha_input))
#curdoc().title # managed in file "/static/strings.json"
