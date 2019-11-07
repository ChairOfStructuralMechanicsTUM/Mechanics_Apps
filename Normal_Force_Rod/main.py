from __future__ import division # float division only, like in python 3

from bokeh.plotting import Figure#, output_file , show
#from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, Arrow
from bokeh.models import ColumnDataSource, Arrow, OpenHead, LabelSet
from bokeh.models.glyphs import ImageURL, Patch, MultiLine, Rect #, Quadratic, Rect, Patch
from bokeh.models.layouts import Spacer
from bokeh.models.widgets import Paragraph, Button, CheckboxGroup, RadioButtonGroup, RadioGroup
from bokeh.layouts import column, row, widgetbox, layout
from bokeh.io import curdoc
#import numpy as np
#import math
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexDiv, LatexLabel, LatexLabelSet, LatexSlider, LatexLegend



from NFR_constants import (
        xr_start, xr_end,
        x_range, fig_height,
        lb, ub
        )


from NFR_beam import NFR_beam

from NFR_equations import calcNU


# ----------------------------------------------------------------- #



def change_load(attr, old, new):
    # TODO: change graphics
    
    compute_new_scenario()



def change_left_support(attr, old, new):
    print(new)
    #beam.set_left_support(5)
    beam.set_left_support(new)
    compute_new_scenario()

def change_right_support(attr, old, new):
    beam.set_right_support(new)
    compute_new_scenario()


def change_amplitude(attr, old, new):
    # TODO: change force arrows

    compute_new_scenario()



def change_load_position(attr, old, new):
    beam.move_load(new)
    #beam.plot_label(plot_main)
    #compute_new_scenario(new)
    compute_new_scenario()




#def compute_new_scenario(ls_type, rs_type, load_type, load_position, amplitude):
def compute_new_scenario():
    ls_tpye = radio_group_left.active
    rs_type = radio_group_right.active
    load_type = radio_button_group.active
    load_position = load_position_slider.value
    ampl    = -1 + 2*radio_group_ampl.active  # ampl=-1 if active=0, ampl=1 if active=1
    samples = calcNU(ls_tpye, rs_type, load_type, load_position, ampl)
    graph_N.data = dict(x=samples['x'], y=samples['yN'])
    graph_U.data = dict(x=samples['x'], y=samples['yU'])




radio_button_group = RadioButtonGroup(labels=["Point Load", "Constant Load", "Triangular Load", "Temperature"], active=0, width = 600)



radio_group_left  = RadioGroup(labels=["fixed", "sliding"], active=0, inline=True)
radio_group_right = RadioGroup(labels=["fixed", "sliding"], active=1, inline=True)
#radio_group_cross = RadioGroup(labels=["constant", "tapered"], active=0, inline=True) # cross-section
radio_group_ampl  = RadioGroup(labels=["-1", "+1"], active=1, inline=True) # amplitude

# Reset Button
reset_button = Button(label="Reset", button_type="success")
line_button  = Button(label="Show line", button_type="success")



radio_button_group.on_change('active',change_load)


radio_group_left.on_change('active', change_left_support)
radio_group_right.on_change('active', change_right_support)
radio_group_ampl.on_change('active',change_amplitude)

load_position_slider  = LatexSlider(title="\\mathrm{Load  Position}", value_unit='\\frac{\\mathrm{L}}{\\mathrm{10}}', value=(xr_end-xr_start)/2, start=xr_start, end=xr_end, step=1.0)
load_position_slider.on_change('value', change_load_position)







###### MAIN PLOT (SUPPORT AND LOAD):
# Define plot:
plot_main = Figure(title="Rod with Supports and Load", tools="", x_range=x_range, y_range=(-2.5,2.5), height=fig_height)
# Set properties
plot_main.axis.visible = False
plot_main.outline_line_width = 2
plot_main.outline_line_color = "Black"
plot_main.title.text_font_size = "13pt"
plot_main.toolbar.logo = None




###### PLOT (NORMAL FORCE):
# Define plot
plot_normalF = Figure(title="Normal force N(x)", tools="yzoom_in,yzoom_out,reset", x_range=x_range, y_range=(-11,11), height=fig_height)
# Set properties
plot_normalF.axis.visible = False
plot_normalF.outline_line_width = 2
plot_normalF.outline_line_color = "Black"
plot_normalF.title.text_font_size = "13pt"
plot_normalF.toolbar.logo = None





###### PLOT (DEFORMATION):
# Define plot
plot_deform = Figure(title="Deformation u(x)", tools="yzoom_in,yzoom_out,reset", x_range=x_range, y_range=(-12,12), height=fig_height)
# Set properties
plot_deform.axis.visible = False
plot_deform.outline_line_width = 2
plot_deform.outline_line_color = "Black"
plot_deform.title.text_font_size = "13pt"
plot_deform.toolbar.logo = None



beam = NFR_beam(0.0, 10.0, 0.0) # x_start, x_end, y_offset, constant shape
beam.plot_all(plot_main)

## move support if necessary
# beam.set_rs_coords(5.0, -0.08)
# beam.plot_supports(plot_main)

# beam.move_load(5.0)
# beam.plot_label(plot_main)

beam.plot_beam_shadow(plot_normalF)
beam.plot_beam_shadow(plot_deform)


graph_N = ColumnDataSource(data=dict(x=[0], y=[0]))
graph_U = ColumnDataSource(data=dict(x=[0], y=[0]))




plot_normalF.line(x='x', y='y', source=graph_N, color="#A2AD00",line_width=2)

plot_deform.line(x='x', y='y', source=graph_U, color="#A2AD00",line_width=2)





##### ADD DESCRIPTION FROM HTML FILE
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1000)

rt_filename = join(dirname(__file__), "radio_button_title.html")
rt = LatexDiv(text=open(rt_filename).read())

p_rt1 = Paragraph(text="""Left support:  """)
p_rt2 = Paragraph(text="""Right support: """)
#p_rt3 = Paragraph(text="""Cross-section: """)
p_rt4 = Paragraph(text="""Load Amplitude:""")


doc_layout = layout(children=[
        column(description,
               row(column(
                       Spacer(height=20,width=450),
                       widgetbox(radio_button_group),
                       row(widgetbox(p_rt1, width=120), widgetbox(radio_group_left)),
                       row(widgetbox(p_rt2, width=120), widgetbox(radio_group_right)), 
                       ##row(widgetbox(p_rt3, width=120), widgetbox(radio_group_cross)), 
                       row(widgetbox(p_rt4, width=120), widgetbox(radio_group_ampl)), 
                       load_position_slider,
                       ##load_magnitude_slide,
                       ##slider_group,
                       #simple_button_group
                       reset_button,
                       line_button),
                   column(plot_main,plot_normalF,plot_deform ) ) ) ] )



curdoc().add_root(doc_layout)
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '