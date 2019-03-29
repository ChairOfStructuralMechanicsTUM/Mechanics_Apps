############################ 
####     MAIN FILE      ####
############################
from bokeh.plotting import Figure, output_file , show
from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, Arrow
from bokeh.models.glyphs import ImageURL, Quadratic, Rect, Patch
from bokeh.models.layouts import Spacer
from bokeh.layouts import column, row, widgetbox, layout
from bokeh.io import curdoc
from bokeh.models.widgets import Button, CheckboxGroup, RadioButtonGroup, RadioGroup, Paragraph
import numpy as np
import math
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexDiv, LatexLabel, LatexLabelSet, LatexSlider, LatexLegend


#####################################
####   GLOBAL BEAM PROPERTIES    ####
#####################################
x0 = 0.0                # starting value of rod
xf = 10.0               # end value of rod



###############################
####       SOURCES         ####
###############################


###################################
####   SLIDERS AND BUTTONS     ####
###################################

### Sliders and Buttons:

# Button to choose type of load:
radio_button_group = RadioButtonGroup(labels=["Point Load", "Constant Load", "Triangular Load", "Temperature"], active=0, width = 600)

radio_group_left = RadioGroup(labels=["fixed", "sliding"], active=0, inline=True)
radio_group_right = RadioGroup(labels=["fixed", "sliding"], active=0, inline=True)
radio_group_cross = RadioGroup(labels=["constant", "tapered"], active=0, inline=True)

# Reset Button
Reset_button = Button(label="Reset", button_type="success")
dummy_button = Button(label="Dummy/Test", button_type="success")



#################################
####       FUNCTIONS         ####
#################################



########################################
#####           PLOTTING           #####
########################################


###### MAIN PLOT (SUPPORT AND LOAD):
# Define plot:
plot_main = Figure(title="Rod with Supports and Load", tools="", x_range=(x0-.5,xf+.5), y_range=(-2.5,2.5), height = 400)
# Set properties
plot_main.axis.visible = False
plot_main.outline_line_width = 2
plot_main.outline_line_color = "Black"
plot_main.title.text_font_size = "13pt"
plot_main.toolbar.logo = None

###### PLOT (NORMAL FORCE):
# Define plot
plot_normalF = Figure(title="Normal force N(x)", tools="", x_range=(x0-.5,xf+.5), y_range=(-11,11), height = 400)
# Set properties
plot_normalF.axis.visible = False
plot_normalF.outline_line_width = 2
plot_normalF.outline_line_color = "Black"
plot_normalF.title.text_font_size = "13pt"
plot_normalF.toolbar.logo = None

###### PLOT (DEFORMATION):
# Define plot
plot_deform = Figure(title="Deformation u(x)", tools="", x_range=(x0-.5,xf+.5), y_range=(-12,12), height = 400)
# Set properties
plot_deform.axis.visible = False
plot_deform.outline_line_width = 2
plot_deform.outline_line_color = "Black"
plot_deform.title.text_font_size = "13pt"
plot_deform.toolbar.logo = None


##### ADD DESCRIPTION FROM HTML FILE
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1000)

##### ARRANGE LAYOUT
#doc_layout = layout(children=[
#        column(description,
#               row(column(Spacer(height=20,width=350),widgetbox(radio_button_group), p_loc_slide, p_mag_slide, f2_loc_slide, widgetbox(Show_button), widgetbox(Reset_button)),
#                   column(plot_main,plot_normalF,plot_deform ) ) ) ] )

#radio_group = 

rt_filename = join(dirname(__file__), "radio_button_title.html")
rt = LatexDiv(text=open(rt_filename).read())

p_rt1 = Paragraph(text="""Left support:  """)
p_rt2 = Paragraph(text="""Right support: """)
p_rt3 = Paragraph(text="""Cross-section: """)
#width=200, height=100)

simple_button_group = widgetbox([Reset_button, dummy_button])

doc_layout = layout(children=[
        column(description,
               row(column(
                       Spacer(height=20,width=450),
                       widgetbox(radio_button_group),
                       #widgetbox(radio_group_left), 
                       #widgetbox(radio_group_right),
                       #widgetbox(radio_group_cross),
                       row(widgetbox(p_rt1, width=120), widgetbox(radio_group_left)),
                       row(widgetbox(p_rt2, width=120), widgetbox(radio_group_right)), 
                       row(widgetbox(p_rt3, width=120), widgetbox(radio_group_cross)), 
                       #row(rt, widgetbox(radio_group_left)),
                       #row(rt, widgetbox(radio_group_right)), 
                       #row(rt, widgetbox(radio_group_cross)), 
                       simple_button_group),
                   column(plot_main,plot_normalF,plot_deform ) ) ) ] )


# plots do not show...
#doc_layout = layout([
#        [description],
#        [widgetbox(radio_button_group)],
#        [rt, widgetbox(radio_group_left)],
#        [rt, widgetbox(radio_group_right), plot_main],
#        [rt, widgetbox(radio_group_cross)],
#        [simple_button_group]
#        ])
 
# wrong layout..
#doc_layout = layout([
#        [description],
#        [
#        [widgetbox(radio_button_group)],
#        [widgetbox(radio_group_left)],
#        [simple_button_group]
#        ],
#        [
#        [plot_main],
#        [plot_normalF],
#        [plot_deform]
#        ],
#        ])

curdoc().add_root(doc_layout)
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '