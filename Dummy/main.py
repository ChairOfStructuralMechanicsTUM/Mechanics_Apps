"""
Dummy App - shows some common concepts used in this project

"""
# general imports
import numpy as np
from math import sin, cos, pi, radians
import sys

# bokeh imports
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.models import ColumnDataSource, Slider, Button

# internal imports
from DY_ball import DY_ball

# latex integration
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv


#---------------------------------------------------------------------#


                ##################################            
                #    inclination plot example    #
                ##################################      


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
    toolbar_location="right", tools=["ywheel_zoom, pan, reset"]) # build the basic skeleton of the figure
inclination_plot.line(x='x', y='y', source=line_coordinates, color="#a2ad00") # plot the line based on the coordinates of the ColumnDataSource line_coordinates
inclination_plot.arc(x=[0], y=[0], radius=[10], start_angle=[0], end_angle=[0.5*pi], line_dash="dashed", color="gray") # TODO: check why the arc is plotted wrong -> aspect ratio
inclination_plot.toolbar.logo = None # removes the bokeh logo
inclination_plot.match_aspect = True # does not work, arc is still wrong; # with title it is better -> title counts to hight



alpha_input = Slider(title="alpha [°]", value=0.0, start=0.0, end=90.0, step=0.5, width=400) # build the slider
alpha_input.on_change('value',change_alpha) # callback function called when alpha is changed in slider


#---------------------------------------------------------------------#




                #####################################            
                #    ping pong animation example    #
                #####################################      


# ping pong animation with changing color

#with class
#TODO: Why does the plot keep slowing down? CDS is only updated, but it stays the same in terms of memory.
#   already checked: memory size of pp_ball or its CDS does NOT grow
#   RAM does not grow
#   speed again after refreshing the window; reset button does not have any effect

# global variables, that are not needed for direct plotting, can be created by dicts (or lists or other Python global scope objects)
# do not use the keyword global! 
# global variables for plots (indicated by source="..." in figure/plot objects) should be of the type ColumnDataSource
global_vars = dict(callback_id = None)


# data for the ping pong animation
#pp_ball = ColumnDataSource(data = dict(x=[], y=[], c=[]))
pp_ball = DY_ball(2,1)


# function called by periodic callback
def ping_pong():
    [x,_] = pp_ball.get_coords()
    if x>3.6:
        pp_ball.change_direction()
        #print(pp_ball) # Debug info
    elif x<0.4:
        pp_ball.change_direction()

    pp_ball.add_disp(0.1)
    new_color = tuple(np.random.random_integers(0,255,(1,3)).flatten()) # random new RGB color
    pp_ball.set_color(new_color)
    pp_ball.plot(pp_plot)
    #print(sys.getsizeof(pp_ball))


# function called, if the play/pause button is pressed
def play_pause():
    # if Play button is pressed
    if play_pause_button.label == "Play":
        # set the callback id
        global_vars["callback_id"] = curdoc().add_periodic_callback(ping_pong,100)  # calls ping_pong() every 100 milliseconds
        # change the displayed button label
        play_pause_button.label = "Pause"
        # disable the reset button as long as the animation runs
        reset_button.disabled = True
    # if Pause button is pressed
    elif play_pause_button.label == "Pause":
        # remove the callback such that the function ping_pong() won't be called as long as Pause is active
        curdoc().remove_periodic_callback(global_vars["callback_id"])
        # change the displayed button label
        play_pause_button.label = "Play"
        # enable the reset button again
        reset_button.disabled = False


def reset():
    pp_ball.set_coords(2,1)
    pp_ball.plot(pp_plot)




pp_plot = figure(title="Ping Pong", x_range=(-1,5), y_range=(-0.5,2.5), height=300, width=400)
pp_plot.line(x=[0,0], y=[0,2], line_width=20, color="black")
pp_plot.line(x=[4,4], y=[0,2], line_width=20, color="black")
#pp_plot.toolbar.logo = None
pp_plot.toolbar_location = None
pp_plot.axis.visible = False # do not show axis
pp_plot.grid.visible = False # do not show grid

pp_ball.plot(pp_plot)



# play/pause button  (two in one for user convenience)
play_pause_button = Button(label="Play", button_type="success",width=100)
play_pause_button.on_click(play_pause) # calls the function play_plause() as soon as the button is clicked on

# reset button to return the plot/animation in its original state
reset_button = Button(label="Reset", button_type="success",width=100)
reset_button.on_click(reset) # calls the function play_plause() as soon as the button is clicked on









# add app description
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)

description_filename_animation = join(dirname(__file__), "description_animation.html")
description_animation = LatexDiv(text=open(description_filename_animation).read(), render_as_text=False, width=1200)

description_filename_end = join(dirname(__file__), "description_end.html")
description_end = LatexDiv(text=open(description_filename_end).read(), render_as_text=False, width=1200)


# send to window
curdoc().add_root(column(description,
                         inclination_plot,
                         alpha_input,
                         description_animation,
                         row(pp_plot, column(play_pause_button,
                                              reset_button)),
                         description_end)) # place all objects at their desired position
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
