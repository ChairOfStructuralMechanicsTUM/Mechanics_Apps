############################ 
####     MAIN FILE      ####
############################
from bokeh.plotting import Figure#, output_file , show
#from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, Arrow
from bokeh.models.glyphs import ImageURL#, Quadratic, Rect, Patch
from bokeh.models.layouts import Spacer
from bokeh.models.widgets import Paragraph
from bokeh.layouts import column, row, widgetbox, layout
from bokeh.io import curdoc
import numpy as np
#import math
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexDiv#, LatexLabel, LatexLabelSet, LatexSlider, LatexLegend



## inner app imports
from NFR_constants import (
        fig_height, fig_width, x_range
        )
from NFR_data_sources import (
        rod_source,
        support_source_left, support_source_right,
        aux_line
        )
from NFR_buttons import (
        load_position_slide, load_magnitude_slide, right_support_position_slide,
        radio_button_group, radio_group_left, radio_group_right, radio_group_cross,
        reset_button, dummy_button
        )







## file description (put -also- in Readme)
# NFR_constants             global constants, default values, images (ext. source)
# NFR_data_sources          ColumnDataSources needed for this program
# NFR_buttons               Buttons, Sliders, Radio Buttons (baically input widgets)
# NFR_callback_functions    inner parts, buttons, sliders (etc.) functionality




######################################
#####   GLOBAL BEAM PROPERTIES    ####
######################################
#x0 = 0.0                # starting value of rod
#xf = 10.0               # end value of rod
#
#
#
################################
#####       SOURCES         ####
################################
## Support Source:
#slide_support_img = "Normal_Force_Rod/static/images/auflager01.svg"
#fixed_support_img = "Normal_Force_Rod/static/images/auflager02.svg"
#
#support_source1 = ColumnDataSource(data=dict(sp_img=[], x=[] , y=[]))
#support_source2 = ColumnDataSource(data=dict(sp_img=[], x=[] , y=[]))
#
#
####################################
#####   SLIDERS AND BUTTONS     ####
####################################
#
#### Sliders and Buttons:
#
#p_loc_slide= LatexSlider(title="\\mathrm{Load \ Position}", value_unit='\\frac{\\mathrm{L}}{\\mathrm{10}}', value= 5,start = 0, end = 10, step = 1.0)
#p_mag_slide = LatexSlider(title="\\mathrm{Load \ Amplitude}", value = 1.0, start=-1.0, end=1.0, step=2.0)
#sup2_loc_slide = LatexSlider(title="\\mathrm{Support \ Position}", value_unit='\\frac{\\mathrm{L}}{\\mathrm{10}}', value=10,start = 0, end = 10, step = 1.0)
#
#
#
## Button to choose type of load:
#radio_button_group = RadioButtonGroup(labels=["Point Load", "Constant Load", "Triangular Load", "Temperature"], active=0, width = 600)
#
#radio_group_left = RadioGroup(labels=["fixed", "sliding"], active=0, inline=True)
#radio_group_right = RadioGroup(labels=["fixed", "sliding"], active=0, inline=True)
#radio_group_cross = RadioGroup(labels=["constant", "tapered"], active=0, inline=True)
#
## Reset Button
#Reset_button = Button(label="Reset", button_type="success")
#dummy_button = Button(label="Dummy/Test", button_type="success")
#


#################################
####       FUNCTIONS         ####
#################################



########################################
#####           PLOTTING           #####
########################################


###### MAIN PLOT (SUPPORT AND LOAD):
# Define plot:
plot_main = Figure(title="Rod with Supports and Load", tools="", x_range=x_range, y_range=(-2.5,2.5), height=fig_height)
# Set properties
plot_main.axis.visible = False
plot_main.outline_line_width = 2
plot_main.outline_line_color = "Black"
plot_main.title.text_font_size = "13pt"
plot_main.toolbar.logo = None





#######################
##########  TESTS #
###################################

#support_source1 = ColumnDataSource(data=dict(sp1=[], x=[] , y=[]))
#support_source2 = ColumnDataSource(data=dict(sp2=[], x=[] , y=[]))
#
#support_source1.data = dict(sp_img=[fixed_support_img], x= [-0.325], y= [-0.1]) 
#support_source2.data = dict(sp_img=[slide_support_img], x = [10-0.33] , y = [-0.1])
#

plot_main.add_glyph(support_source_left,ImageURL(url="sp_img", x='x', y='y', w=0.66, h=0.4))
plot_main.add_glyph(support_source_right,ImageURL(url="sp_img", x='x', y='y', w=0.66, h=0.4))

#rod_source = ColumnDataSource(data=dict(x = np.linspace(0,10,100), y = np.ones(100) * 0 ))

plot_main.line(x='x', y='y', source=rod_source, color='#0065BD',line_width=15)









###### PLOT (NORMAL FORCE):
# Define plot
plot_normalF = Figure(title="Normal force N(x)", tools="", x_range=x_range, y_range=(-11,11), height=fig_height)
# Set properties
plot_normalF.axis.visible = False
plot_normalF.outline_line_width = 2
plot_normalF.outline_line_color = "Black"
plot_normalF.title.text_font_size = "13pt"
plot_normalF.toolbar.logo = None


## const p=2     -2x
#x = np.linspace(0,10,1000)
#y = np.ones(1000)*-2*x
#normalF_source = ColumnDataSource(data=dict(x=[] , y=[]))
#normalF_source.data = dict(x=x, y=y)
#
#plot_normalF.line(x='x', y='y', source=normalF_source, color="#A2AD00",line_width=2)

# evtl. gleichmit scipy und integration rules für beliebiges p

###### PLOT (DEFORMATION):
# Define plot
plot_deform = Figure(title="Deformation u(x)", tools="", x_range=x_range, y_range=(-12,12), height=fig_height)
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

#slider_group = widgetbox(p_loc_slide,p_mag_slide,sup2_loc_slide) # together to close....
simple_button_group = widgetbox([reset_button, dummy_button])

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
                       load_position_slide,
                       load_magnitude_slide,
                       right_support_position_slide,
                       #slider_group,
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