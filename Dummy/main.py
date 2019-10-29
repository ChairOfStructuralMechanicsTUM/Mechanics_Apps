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
from bokeh.models import ColumnDataSource, Slider, Button, Select, CustomJS

# internal imports
from DY_ball import DY_ball

# latex integration
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv, LatexSlider


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
# also: arc grows when using the ywheel_zoom



#alpha_input = Slider(title="alpha [°]", value=0.0, start=0.0, end=90.0, step=0.5, width=400) # build the slider (without LaTeX)
alpha_input = LatexSlider(title="\\alpha [°]", value=0.0, start=0.0, end=90.0, step=0.5, width=400) # build the slider (with LaTeX supported)
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
    pp_ball.plot(pp_plot)




pp_plot = figure(title="Ping Pong", x_range=(-1,5), y_range=(-0.5,2.5), height=300, width=400, tools="")
pp_plot.line(x=[0,0], y=[0,2], line_width=20, color="black")
pp_plot.line(x=[4,4], y=[0,2], line_width=20, color="black")
#pp_plot.toolbar.logo = None    # we don't need this, if we hide the toolbar
pp_plot.toolbar_location = None # hide the toolbar
pp_plot.axis.visible = False    # do not show axis
pp_plot.grid.visible = False    # do not show grid

pp_ball.plot(pp_plot)



# play/pause button  (two in one for user convenience)
play_pause_button = Button(label="Play", button_type="success",width=100)
play_pause_button.on_click(play_pause) # calls the function play_plause() as soon as the button is clicked on

# reset button to return the plot/animation in its original state
reset_button = Button(label="Reset", button_type="success",width=100)
reset_button.on_click(reset) # calls the function play_plause() as soon as the button is clicked on



#---------------------------------------------------------------------#




                #################################            
                #          hide example         #
                #################################      


# CSS and JavaScript needed for this example
# more sophisticated 
# /templates/index.html and /templates/styles.css necessary, see description text
### UPDATE: also possible without JavaScript ###

# real app example: rolling test

# JavaScript callback function
# not needed anymore, but leaving it for the sake of completeness
hide_JS = """
// store the value of the callback object (in our case the Select)
choice = cb_obj.value;


// here we get all elements that containt "button" in their css_classes
// this is returned by an array
// since we only have one button with this feature in this example, we can just use the first index
// otherwise, we would need some more code and css_classes names to get the right index; see the Rolling Test App
button_in_question = document.getElementsByClassName("button")[0];


// if "show" is selected, show the button (get rid of "hidden")
if(choice.includes("show")){
    button_in_question.className = button_in_question.className.replace(" hidden", "");
}

// if "hide" is selected, hide the button (add "hidden" to the css_classes)
else if(choice.includes("hide")){
    button_in_question.className += " hidden";
}


// you can debug JavaScript code by printing it to the console via
//    console.log(variable);
// when using Firefox, pressing F12 and choosing the console or opening it via Ctrl+Shift+K, you can see the output
"""


# callback function for the selection
# the button tag is necessary, otherwise it will only work once (one hide, and one show)
# of course you can name the tag whatever you like, not necessarily "button", but some non-empty string is required
def change_css_attr(attr, old ,new):
    # add the tag "hidden" (or whatever word defined in styles.css) to hide the button
    if new == "hide":
        hide_button.css_classes = ["button", "hidden"]
        #hide_button.css_classes = ["hidden"] # only works once
    # remove the tag "hidden" to display the button; replacing instead of removing is also possible
    elif new == "show":
        hide_button.css_classes = ["button"]
        #hide_button.css_classes = [""] # only works once



# button to hide
hide_button = Button(label="hide", button_type="success",width=100, css_classes=["button"])

# selection/dropdown whether to display the button or hide it
hide_selection = Select(title="display mode:", value="show", name="hs", options=["show", "hide"])

# define the JavaScript code as its callback function
#hide_selection.callback = CustomJS(code=hide_JS)  # JavaScript callback
hide_selection.on_change('value', change_css_attr) # Python callback








#---------------------------------------------------------------------#








# add app description text
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)

description_filename_animation = join(dirname(__file__), "description_animation.html")
description_animation = LatexDiv(text=open(description_filename_animation).read(), render_as_text=False, width=1200)

description_filename_hide = join(dirname(__file__), "description_hide.html")
description_hide = LatexDiv(text=open(description_filename_hide).read(), render_as_text=False, width=1200)

description_filename_end = join(dirname(__file__), "description_end.html")
description_end = LatexDiv(text=open(description_filename_end).read(), render_as_text=False, width=1200)


# send to window
curdoc().add_root(column(description,
                         inclination_plot,
                         alpha_input,
                         description_animation,
                         row(pp_plot, column(play_pause_button,
                                              reset_button)),
                         description_hide,
                         row(hide_selection, hide_button),
                         description_end)) # place all objects at their desired position
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
