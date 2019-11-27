"""
Tamplate App - provides a template for new apps
"""
# general imports
import numpy as np

# bokeh imports
from bokeh.io             import curdoc
from bokeh.plotting       import figure
from bokeh.models         import ColumnDataSource, LabelSet, Arrow, OpenHead
from bokeh.models.glyphs  import MultiLine, Rect, ImageURL #, Patch, 
from bokeh.models.widgets import Paragraph, Button, RadioButtonGroup, RadioGroup #CheckboxGroup
from bokeh.layouts        import column, row, widgetbox, layout, Spacer

# internal imports
from TA_costum_class import TA_example_class
from TA_constants import (
    slide_support_img, fixed_support_img,  # support images
    xsl, ysl, xsr, ysr,                    # support coordinates
    support_width, support_height,         # support scale
    initial_value, start_value, end_value, # slider settings
    button_width                           # button settings
)

# latex integration
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexDiv, LatexLabel, LatexLabelSet, LatexSlider, LatexLegend

# ----------------------------------------------------------------- #

###############################
#          Constants          #
###############################
# you may also define constants directly in main if they are only used here
# though defining them in an extra file is recommended for possible extensions
max_x = 5


###############################
#       Global Variables      #
###############################
# file-global variables (only "global" in this file!)
# see mutable objections in Python (e.g. lists and dictionaries)
global_vars = dict(callback_id=None)


###############################
#      ColumnDataSources      #
###############################
# define your ColumnDataSources here for a better overview of which data influences plots
# they don't have to be filled but at least defined (and later filled in callback or helper functions)
cds_support_left  = ColumnDataSource(data=dict(sp_img=[fixed_support_img], x=[xsl] , y=[ysl]))
cds_support_right = ColumnDataSource(data=dict(sp_img=[slide_support_img], x=[xsr] , y=[ysr]))



################################
#      Callback Functions      #
################################


def pp_button_cb_fun():
    # define functionality
    pass


def play_pause():
    if play_pause_button.label == "Play":
        global_vars["callback_id"] = curdoc().add_periodic_callback(pp_button_cb_fun,100)
        play_pause_button.label = "Pause"
    elif play_pause_button.label == "Pause":
        curdoc().remove_periodic_callback(global_vars["callback_id"])
        play_pause_button.label = "Play"



def slider_cb_fun(attr,old,new):
    # define functionality
    if(new == end_value):
        some_helper_fun() # call helper function


################################
#       Helper Functions       #
################################
# if a callback function might get to large or if several callback functions partly do the same
# outsource it to helper functions

def some_helper_fun():
    print("hello, I'm here to help")




###################################
#             Figures             #
###################################

### define the figure ###
# the shown attributes should always be set
# if no tool is needed set tools="" or toolbar_location=None
# for more attributes have a look at the bokeh documentation
figure_name = figure(title="Example Figure", x_range=(-1,max_x), y_range=(-0.5,2.5), height=300, width=400, tools="pan, wheel_zoom, reset")
figure_name.toolbar.logo = None # do not display the bokeh logo


### add the support images ###
# urls and coordinates are provided by a ColumnDataSource
# anchor specifies at which position of the image the x and y coordinates are referring to
# width and height could also be set using constants defined in TA_constants.py and imported here in main.py
figure_name.add_glyph(cds_support_left,  ImageURL(url="sp_img", x='x', y='y', w=0.66, h=0.4, anchor="center"))
figure_name.add_glyph(cds_support_right, ImageURL(url="sp_img", x='x', y='y', w=support_width, h=support_height, anchor="center"))





###################################
#       Buttons and Sliders       #
###################################
# or in general widgets
# you may also sepperate the definitions and calls depending on you setting


play_pause_button = Button(label="Play", button_type="success", width=button_width)
play_pause_button.on_click(play_pause) 



# the attribute "value_unit" only exists in the costum LatexSlider class
# for a default bokeh slider use Slider
example_slider = LatexSlider(title="\\text{example}=", value_unit="\\frac{Sv}{m \\cdot kg}", value=initial_value, start=start_value, end=end_value, step=0.5, width=400)
example_slider.on_change('value',slider_cb_fun) # callback function is called when value changes



##################################
#         Costum Objects         #
##################################

# build a new object
my_object = TA_example_class(42)

# printing the objects yields the output defined in the __str__ function
print(my_object)

# changing the string
my_object.set_string("This is cool!")

# check if the new string has been set correctly
print(my_object)

# plot a line in the test figure
my_object.plot_line(figure_name)

# you can also use this object in above callback/helper functions
# since it is mutable and therefore file global


# for other real application classes see 


###################################
#           Page Layout           #
###################################

description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1000)


curdoc().add_root(column(
    description,
    row(figure_name, column(play_pause_button, 
                            example_slider))
))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '


