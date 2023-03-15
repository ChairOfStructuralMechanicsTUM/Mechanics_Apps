"""
Dummy App - shows some common concepts used in this project

"""
# general imports
import numpy as np
from math import sin, cos, pi, radians
import time

# bokeh imports
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.models import ColumnDataSource, Slider, Button, Select, CustomJS, RadioGroup, Div

# internal imports
from DY_ball import DY_ball

# latex integration
#from os.path import dirname, join, split, abspath
#import sys, inspect
#currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
#parentdir = join(dirname(currentdir), "shared/")
#sys.path.insert(0,parentdir) 
#from latex_support import LatexDiv, LatexSlider

# latex integration via pathlilb
import pathlib
import sys, inspect
shareddir = str(pathlib.Path(__file__).parent.parent.resolve() / "shared" ) + "/"
sys.path.insert(0,shareddir)
from latex_support import LatexDiv, LatexLabelSet, LatexSlider, LatexLegend

app_base_path = pathlib.Path(__file__).resolve().parents[0]

#---------------------------------------------------------------------#
div_width = 1000

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
    toolbar_location="right", tools=["ywheel_zoom, pan, reset, save"], output_backend="svg") # build the basic skeleton of the figure
inclination_plot.line(x='x', y='y', source=line_coordinates, color="#a2ad00") # plot the line based on the coordinates of the ColumnDataSource line_coordinates
inclination_plot.arc(x=[0], y=[0], radius=[10], start_angle=[0], end_angle=[0.5*pi], line_dash="dashed", color="gray") # TODO: check why the arc is plotted wrong -> aspect ratio
inclination_plot.toolbar.logo = None # removes the bokeh logo
inclination_plot.match_aspect = True # does not work, arc is still wrong; # with title it is better -> title counts to hight
# also: arc grows when using the ywheel_zoom



#alpha_input = Slider(title="alpha [°]", value=0.0, start=0.0, end=90.0, step=0.5, width=400) # build the slider (without LaTeX)
#alpha_input = LatexSlider(title="\\alpha [°]:", value=0.0, start=0.0, end=90.0, step=0.5, width=400) # build the slider (with LaTeX supported) # colons have to be written explicitly into the string
alpha_input = LatexSlider(title="\\alpha = ", value_unit="°", value=0.0, start=0.0, end=90.0, step=0.5, width=400) # build the slider (with LaTeX supported) # use the custom value_unit attribute if you use symbols
alpha_input.on_change('value',change_alpha) # callback function called when alpha is changed in slider


#---------------------------------------------------------------------#




                #####################################            
                #    ping pong animation example    #
                #####################################      


# ping pong animation with changing color and a class

# IMPORTANT NOTE: Only plot objects ONCE and then update them via the ColumnDataSources - otherwise the animation would slow down drastically
#                 if the object would be plotted completely at each callback


# global variables, that are not needed for direct plotting, can be created by dicts (or lists or other Python global scope objects)
# do not use the keyword global! 
# global variables for plots (indicated by source="..." in figure/plot objects) should be of the type ColumnDataSource
global_vars = dict(callback_id = None)


# data for the ping pong animation
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
    #pp_ball.plot(pp_plot)  # Do NOT plot the ball completely new! Updates only via ColumnDataSources.


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


# reset functionality
def reset():
    pp_ball.set_coords(2,1)
    pp_ball.set_color((0,0,0))
    #pp_ball.plot(pp_plot)  # Do NOT plot the ball completely new! Updates only via ColumnDataSources.




pp_plot = figure(title="Ping Pong", x_range=(-1,5), y_range=(-0.5,2.5), height=300, width=400, tools="")
pp_plot.line(x=[0,0], y=[0,2], line_width=20, color="black")
pp_plot.line(x=[4,4], y=[0,2], line_width=20, color="black")
#pp_plot.toolbar.logo = None    # we don't need this, if we hide the toolbar
pp_plot.toolbar_location = None # hide the toolbar
pp_plot.axis.visible = False    # do not show axis
pp_plot.grid.visible = False    # do not show grid

pp_ball.plot(pp_plot) # plot the ball ONCE at this place - updates only via ColumnDataSources



# play/pause button  (two in one for user convenience)
play_pause_button = Button(label="Play", button_type="success", width=100)
play_pause_button.on_click(play_pause) # calls the function play_plause() as soon as the button is clicked on

# reset button to return the plot/animation in its original state
reset_button = Button(label="Reset", button_type="success", width=100)
reset_button.on_click(reset) # calls the function play_plause() as soon as the button is clicked on



#---------------------------------------------------------------------#




                #################################            
                #          hide example         #
                #################################      


# hiding objects can be handy 
# in the new bokeh version the visibility of objects can be set easily

# callback function for the selection
def change_display_mode(attr, old ,new):
    if new == "hide":
        hide_button.visible = False   # hides the button and adjusts the spacing of objects around it
        #hide_button.disabled = True  # this would still show the button but block it from being used
    if new == "show":
        hide_button.visible = True    # shows the button
        #hide_button.disabled = False # enables the button such that one can click on it again


# button to hide
hide_button = Button(label="now you see me", button_type="success", width=100)

# selection/dropdown whether to display the button or hide it
# value sets the initial choice
# options sets the list of available options
hide_selection = Select(title="display mode:", value="show", options=["show", "hide"])
hide_selection.on_change('value', change_display_mode) # Python callback





#---------------------------------------------------------------------#




                #################################            
                #          style example        #
                #################################      


# in very rare cases custom styles might be needed

# requires the folder /templates with /templates/styles.css and /templates/index.html



def change_background_color(attr,old,new):
    if new==0: # slider without background color
        radio_group.css_classes = ["radios"]
    elif new==1: # change the background of the slider
        radio_group.css_classes = ["radios", "bgcol"]
        # NOTE: this just serves as an example
        # Bokeh provides an easy python access via   radio_group.background = "red"
        # Use css_classes only in case if there is no attribute which provides your desired functionality!


# define the class names you need in your templates/styles.css in css_classes
radio_group = RadioGroup(labels=["no background", "aqua background"], width=300, css_classes=["radios"])
radio_group.on_change('active', change_background_color)





#---------------------------------------------------------------------#




                #################################            
                #        loading example        #
                #################################      


# for exhaustive computations we need to display a loading symbol to inform the user


def intensive_computational_work():
    # the actual work to be done

    # model the long computations with sleep for x seconds
    time.sleep(3)

    # set back the loading sign    # actually it is still there in this case, just invisible
                                   # to see the approach of manipulating the page layout directly, see the Wavelet App
    loading_sign.visible = False
    # also enable the button again
    heavy_comp_button.disabled = False


def start_work():
    # callback function for the button which initiates the computations

    # show the loading sign to tell the user, that s/he has to wait
    loading_sign.visible = True
    # also disable the button such that the user is not able to start new computations while the first one hasn't finished
    heavy_comp_button.disabled = True

    # add the next tick such this callback finishes to show the changes, but the actual work can start
    curdoc().add_next_tick_callback(intensive_computational_work)


# define the button which is used to start the desired computation
heavy_comp_button = Button(label="start intensive computation", button_type="success", width=150, height=80) # also add a height to avoid resizing when the loading sign is displayed # in general buttons can stay with their default height
heavy_comp_button.on_click(start_work)  # callback to apply the layout changes and start the computational work



# loading the html which provides the style definition of the loading symbol
# this can of course also be done where the other descriptions are loaded, however we keep important code together in each example section
description_filename_loading = str(app_base_path / "description_loading.html")
description_loading = LatexDiv(text=open(description_filename_loading).read(), render_as_text=False, width=div_width)

# create the div container which holds the loading sign
loading_sign = Div(text="<div class=\"lds-dual-ring\"></div>", width=650, visible=False)  # initially visible is false since it only should be seen during calculations




#---------------------------------------------------------------------#




# add app description text
description_filename = str(app_base_path / "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=div_width)

description_filename_animation = str(app_base_path / "description_animation.html")
description_animation = LatexDiv(text=open(description_filename_animation).read(), render_as_text=False, width=div_width)

description_filename_hide = str(app_base_path / "description_hide.html")
description_hide = LatexDiv(text=open(description_filename_hide).read(), render_as_text=False, width=div_width)

description_filename_style = str(app_base_path / "description_style.html")
description_style = LatexDiv(text=open(description_filename_style).read(), render_as_text=False, width=div_width)

description_filename_encoding = str(app_base_path / "description_encoding.html")
description_encoding = LatexDiv(text=open(description_filename_encoding).read(), render_as_text=False, width=div_width)

description_filename_end = str(app_base_path / "description_end.html")
description_end = LatexDiv(text=open(description_filename_end).read(), render_as_text=False, width=div_width)


# send to window
curdoc().add_root(column(description,
                         inclination_plot,
                         alpha_input,
                         description_animation,
                         row(pp_plot, column(play_pause_button,
                                              reset_button)),
                         description_hide,
                         row(hide_selection, hide_button),
                         description_style,
                         radio_group,
                         description_loading,
                         row(heavy_comp_button, loading_sign),
                         description_encoding,
                         description_end)) # place all objects at their desired position
curdoc().title = str(app_base_path.relative_to(app_base_path.parent)).replace("_"," ").replace("-"," ")  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '


