"""
Tamplate App - provides a template for new apps
"""
# general imports
import numpy as np

# bokeh imports
from bokeh.io             import curdoc
from bokeh.plotting       import figure
from bokeh.models         import ColumnDataSource, Arrow, OpenHead, NormalHead
from bokeh.models.glyphs  import ImageURL
from bokeh.models.widgets import Button, RadioButtonGroup, RadioGroup
from bokeh.layouts        import column, row, Spacer

# internal imports
from TA_surface3d import TA_Surface3d
from TA_custom_class import TA_example_class
from TA_constants import (
    slide_support_img, fixed_support_img,  # support images
    xsl, ysl, xsr, ysr,                    # support coordinates
    support_width, support_height,         # support scale
    initial_value, start_value, end_value, # slider settings
    button_width,                          # button settings
    c_orange                               # colors used
)
from TA_Spring  import TA_Spring
from TA_Mass    import TA_CircularMass
from TA_Dashpot import TA_Dashpot
from TA_Coord   import TA_Coord

# latex integration
#from os.path import dirname, join, split, abspath
#import sys, inspect
#currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
#parentdir = join(dirname(currentdir), "shared/")
#sys.path.insert(0,parentdir)
#from latex_support import LatexDiv, LatexLabel, LatexLabelSet, LatexSlider, LatexLegend

# Using pathlib
import pathlib
import sys, inspect
shareddir = str(pathlib.Path(__file__).parent.parent.resolve() / "shared" ) + "/"
sys.path.insert(0,shareddir)
from latex_support import LatexDiv, LatexLabel, LatexLabelSet, LatexSlider, LatexLegend

app_base_path = pathlib.Path(__file__).resolve().parents[0]

# ----------------------------------------------------------------- #

###################################
#            Constants            #
###################################
# you may also define constants directly in main if they are only used here
# though defining them in an extra file is recommended for possible extensions
max_x = 5


###################################
#         Global Variables        #
###################################
# file-global variables (only "global" in this file!)
# see mutable objections in Python (e.g. lists and dictionaries)
global_vars = dict(callback_id=None)


###################################
#        ColumnDataSources        #
###################################
# define your ColumnDataSources here for a better overview of which data influences plots
# they don't have to be filled but at least defined (and later filled in callback or helper functions)
cds_support_left  = ColumnDataSource(data=dict(sp_img=[fixed_support_img], x=[xsl] , y=[ysl]))
cds_support_right = ColumnDataSource(data=dict(sp_img=[slide_support_img], x=[xsr] , y=[ysr]))

cds_arrow = ColumnDataSource(data=dict(xS=[1], xE=[3], yS=[1], yE=[1]))
plot_3D_source = ColumnDataSource(data=dict(x=[], y=[], z=[]))

##################################
#       Callback Functions       #
##################################


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


def radio_cb_fun(attr,old,new):
    if new==0: # slider without background color
        example_slider.css_classes = ["slider"]
    elif new==1: # change the background of the slider
        example_slider.css_classes = ["slider", "bgcol"]
        # NOTE: this just serves as an example
        # Bokeh provides an easy python access via   example_slider.background = "red"
        # Use css_classes only in case if there is no attribute which provides your desired functionality!


# a more detailed example of hiding models can be found in the Dummy App
def radio_cb_fun_2(attr,old,new):
    if new==0: # show slider
        example_slider.visible = True
    elif new==1: # hide slider
        example_slider.visible = False



##################################
#        Helper Functions        #
##################################
# if a callback function might get to large or if several callback functions partly do the same
# outsource it to helper functions

def some_helper_fun():
    print("hello, I'm here to help")



###################################
#             Figures             #
###################################

### define the figure ###
# the shown attributes should always be set
# if no tool is needed, set tools="" or toolbar_location=None
# for more attributes have a look at the bokeh documentation
figure_name = figure(title="Example Figure", x_range=(-1,max_x), y_range=(-0.5,2.5), height=300, width=400, tools="pan, wheel_zoom, reset")
figure_name.toolbar.logo = None # do not display the bokeh logo


### add the support images ###
# urls and coordinates are provided by a ColumnDataSource
# anchor specifies at which position of the image the x and y coordinates are referring to
# width and height could also be set using constants defined in TA_constants.py and imported here in main.py
figure_name.add_glyph(cds_support_left,  ImageURL(url="sp_img", x='x', y='y', w=0.66, h=0.4, anchor="center"))
figure_name.add_glyph(cds_support_right, ImageURL(url="sp_img", x='x', y='y', w=support_width, h=support_height, anchor="center"))


### add arrows to the figure ###
# use either Normalheads or Openheads and orange color by default
#arrow_glyph = Arrow(end=NormalHead(line_color=c_orange, fill_color=c_orange), x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_color=c_orange, source=cds_arrow)
arrow_glyph = Arrow(end=OpenHead(line_color=c_orange), x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_color=c_orange, source=cds_arrow)
figure_name.add_layout(arrow_glyph)

### define the 3D plot ###
x = np.arange(0, 300, 10)
y = np.arange(0, 300, 10)
xx, yy = np.meshgrid(x, y)
xx = xx.ravel()
yy = yy.ravel()
value = np.sin(xx / 50) * np.cos(yy / 50) * 50 + 50

plot_3D_source.data=dict(x=xx, y=yy, z=value)

surface = TA_Surface3d(x="x", y="y", z="z", data_source=plot_3D_source)



###################################
#       Buttons and Sliders       #
###################################
# or in general widgets
# you may also separate the definitions and calls depending on your setting


play_pause_button = Button(label="Play", button_type="success", width=button_width)
play_pause_button.on_click(play_pause) 


# the attribute "value_unit" only exists in the costum LatexSlider class
# for a default bokeh slider use Slider
# use the css_classes to reference this object in /templates/styles.css
example_slider = LatexSlider(title="\\text{example}=", value_unit="\\frac{Sv}{m \\cdot kg}", value=initial_value, start=start_value, end=end_value, step=0.5, width=400, css_classes=["slider"])
example_slider.on_change('value',slider_cb_fun) # callback function is called when value changes


# radio button: round and only one active selection per group allowed
# active=0 to select the the first button by default
# inline=True to place the buttons horizontally
radio_group_01  = RadioGroup(labels=["1", "2"], active=0, inline=True)
radio_group_02  = RadioGroup(labels=["3", "4"])
radio_group_01.on_change("active", radio_cb_fun)
radio_group_02.on_change("active", radio_cb_fun_2)


# radio button group: buttons that are merged next to each other, only one active selection per group allowed
radio_button_group = RadioButtonGroup(labels=["Item 1", "Item 2", "Item 3"], active=0, width = 200)


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



### building an SDOF system ###
# see SDOF app for an application
# separate linking lines that would also need ColumnDataSource in real applications
figure_name.line(x=[0,4], y=[1.5,1.5], color="black", line_width=2)
figure_name.line(x=[2,2], y=[1.5,2.0], color="black", line_width=2)
figure_name.line(x=[0,4], y=[0.3,0.3], color="black", line_width=3)
# replace numbers by constants in real app
mass   = TA_CircularMass(8,2,2,0.8,0.5)
spring = TA_Spring((0,.3),(0,1.5),1,1,50,0.25)
damper = TA_Dashpot((4,.3),(4,1.5),0.5,1.5)
mass.plot(figure_name)
spring.plot(figure_name)
damper.plot(figure_name)

# for other real application classes browse through existing apps



###################################
#           Page Layout           #
###################################

description_filename = str(app_base_path / "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1000)

# to keep track of the final page layout it is suggested to more or less use the same layout in your curdoc code
# add additional spacers to move your objects to the desired locations
curdoc().add_root(column(
    description,
    row(figure_name, Spacer(width=100), column(play_pause_button, 
                                               example_slider,
                                               radio_group_01,
                                               radio_group_02,
                                               radio_button_group)),
    surface
))
curdoc().title = str(app_base_path.relative_to(app_base_path.parent)).replace("_"," ").replace("-"," ")  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '


