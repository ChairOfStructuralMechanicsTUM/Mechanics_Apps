"""
Normal Force Rod - presents the influence of different loads on force and deformation

"""
# general imports
from __future__ import division # float division only, like in python 3

# bokeh imports
from bokeh.io             import curdoc
from bokeh.plotting       import Figure
from bokeh.models         import ColumnDataSource, LabelSet #Arrow, OpenHead
from bokeh.models.glyphs  import MultiLine, Rect ,ImageURL #, Patch, 
from bokeh.models.layouts import Spacer
from bokeh.models.widgets import Paragraph, Button, RadioButtonGroup, RadioGroup #CheckboxGroup
from bokeh.layouts        import column, row, widgetbox, layout

# internal imports
from NFR_beam      import NFR_beam
from NFR_equations import calcNU
from NFR_constants import (
        xr_start, xr_end,
        x_range, fig_height,
        #lb, ub, 
        initial_load, initial_load_position
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
#      ColumnDataSources      #
###############################
aux_line        = ColumnDataSource(data=dict(x=[], y=[]))         # auxiliary / helper line
error_msg_frame = ColumnDataSource(data=dict(x=[],y=[]))          # error message frame
error_msg       = ColumnDataSource(data=dict(x=[],y=[],name=[]))  # error message position
graph_N         = ColumnDataSource(data=dict(x=[0], y=[0]))       # data for force plot
graph_U         = ColumnDataSource(data=dict(x=[0], y=[0]))       # data for deformation plot




################################
#      Callback Functions      #
################################

def change_load(attr, old, new):
    beam.set_load(new)
    compute_new_scenario()

def change_left_support(attr, old, new):
    beam.set_left_support(new)

    if radio_group_right.active==1 and new==1: # both slide
        show_error(True)
    else:
        show_error(False)
        compute_new_scenario()

    #compute_new_scenario()

def change_right_support(attr, old, new):
    beam.set_right_support(new)

    if radio_group_left.active==1 and new==1: # both slide
        show_error(True)
    else:
        show_error(False)
        compute_new_scenario()


def change_amplitude(attr, old, new):
    beam.set_load_direction(new)
    compute_new_scenario()


def change_load_position(attr, old, new):
    beam.move_load(new)
    compute_new_scenario()


def reset():
    radio_button_group.active  = initial_load
    radio_group_left.active    = 0
    radio_group_right.active   = 1
    radio_group_ampl.active    = 1
    load_position_slider.value = initial_load_position
    # possibly set the values in beam correspondingly - # ok no, happens automatically
    # setting the values via their attributes seems to call the callback functions as well
    compute_new_scenario()


def change_line_visibility():
    if line_button.label == "Show line":
        move_aux_line()
        line_button.label = "Hide line"
    elif line_button.label == "Hide line":
        aux_line.data = dict(x=[], y=[])
        line_button.label = "Show line"




################################
#       Helper Functions       #
################################

def compute_new_scenario():
    ls_tpye       = radio_group_left.active
    rs_type       = radio_group_right.active
    load_type     = radio_button_group.active
    load_position = load_position_slider.value
    ampl          = -1 + 2*radio_group_ampl.active  # ampl=-1 if active=0, ampl=1 if active=1
    #print(beam)
    samples = calcNU(ls_tpye, rs_type, load_type, load_position, ampl)
    graph_N.data = dict(x=samples['x'], y=samples['yN'])
    graph_U.data = dict(x=samples['x'], y=samples['yU'])

    # if the auxiliary line should be shown, the line button shows "Hide line"
    if line_button.label == "Hide line":
        move_aux_line()


def move_aux_line():
    x_samples = graph_N.data['x']
    y_samples = graph_N.data['y']
    roots     = []

    for i in range(0,len(y_samples)-1):
        if y_samples[i]*y_samples[i+1] < 0: # sign changes => root
            r = 0.5*(x_samples[i+1]-x_samples[i]) + x_samples[i]
            roots.append([r,r])

    aux_line.data = dict(x=roots, y=[[15,-15]]*len(roots))


def show_error(show=True):
    if show:
        error_msg.data       = dict(x=[2],y=[1.35],name=["Warning! - Kinematic, rod slides away!"])
        error_msg_frame.data = dict(x=[5], y=[1.5])
    else:
        error_msg.data       = dict(x=[], y=[], name=[])
        error_msg_frame.data = dict(x=[], y=[])



###################################
#             Figures             #
###################################

# helper line glyph for every plot
aux_line_glyph = MultiLine(xs='x', ys='y', line_width=2, line_dash=[1,2], line_color='gray')


###### MAIN PLOT (beam, supports, load) ######
# define plot:
plot_main = Figure(title="Rod with Supports and Load", tools="", x_range=x_range, y_range=(-1.5,2.5), height=fig_height)
# set properties
plot_main.axis.visible = False
plot_main.outline_line_width = 2
plot_main.outline_line_color = "Black"
plot_main.title.text_font_size = "13pt"
plot_main.toolbar.logo = None

# plot error message if both supports are set to sliding
error_label = LabelSet(x='x', y='y', text='name', source=error_msg)
plot_main.add_layout(error_label)
plot_main.add_glyph(error_msg_frame,Rect(x="x", y="y", width=8, height=1, angle=0, fill_color='red', fill_alpha=0.2))

# plot helper line
plot_main.add_glyph(aux_line, aux_line_glyph)



###### FORCE PLOT (normal force) ######
# define plot
plot_normalF = Figure(title="Normal force N(x)", tools="yzoom_in,yzoom_out,reset", x_range=x_range, y_range=(-11,11), height=fig_height)
# set properties
plot_normalF.axis.visible = False
plot_normalF.outline_line_width = 2
plot_normalF.outline_line_color = "Black"
plot_normalF.title.text_font_size = "13pt"
plot_normalF.toolbar.logo = None

# plot data
plot_normalF.line(x='x', y='y', source=graph_N, color="#A2AD00",line_width=2)

# plot helper line
plot_normalF.add_glyph(aux_line, aux_line_glyph)



###### DEFORMATION PLOT ######
# define plot
plot_deform = Figure(title="Deformation u(x)", tools="yzoom_in,yzoom_out,reset", x_range=x_range, y_range=(-12,12), height=fig_height)
# set properties
plot_deform.axis.visible = False
plot_deform.outline_line_width = 2
plot_deform.outline_line_color = "Black"
plot_deform.title.text_font_size = "13pt"
plot_deform.toolbar.logo = None

# plot data
plot_deform.line(x='x', y='y', source=graph_U, color="#A2AD00",line_width=2)

# plot helper line
plot_deform.add_glyph(aux_line, aux_line_glyph)



###################################
#       Buttons and Sliders       #
###################################
radio_button_group = RadioButtonGroup(labels=["Point Load", "Constant Load", "Triangular Load", "Temperature"], active=initial_load, width = 600)

radio_group_left  = RadioGroup(labels=["fixed", "sliding"], active=0, inline=True)
radio_group_right = RadioGroup(labels=["fixed", "sliding"], active=1, inline=True)
#radio_group_cross = RadioGroup(labels=["constant", "tapered"], active=0, inline=True) # cross-section not yet
radio_group_ampl  = RadioGroup(labels=["-1", "+1"], active=1, inline=True) # amplitude

load_position_slider  = LatexSlider(title="\\mathrm{Load \ Position:}", value_unit='\\frac{\\mathrm{L}}{\\mathrm{10}}', value=initial_load_position, start=xr_start, end=xr_end, step=1.0)

reset_button = Button(label="Reset", button_type="success")
line_button  = Button(label="Show line", button_type="success")


## call their corresponding callback functions

radio_button_group.on_change('active',change_load)

radio_group_left.on_change('active', change_left_support)
radio_group_right.on_change('active', change_right_support)
radio_group_ampl.on_change('active',change_amplitude)

load_position_slider.on_change('value', change_load_position)

reset_button.on_click(reset)
line_button.on_click(change_line_visibility)





sf1 = "Normal_Force_Rod/static/images/snowflake01.svg"
sf2 = "Normal_Force_Rod/static/images/snowflake02.svg"
sf3 = "Normal_Force_Rod/static/images/snowflake03.svg"

cds_t1 = ColumnDataSource(data=dict(x=[0.4],y=[1.1], img=[sf1]))
cds_t2 = ColumnDataSource(data=dict(x=[3.4],y=[1.2], img=[sf2]))
cds_t3 = ColumnDataSource(data=dict(x=[7.4],y=[-0.7], img=[sf3]))




plot_main.add_glyph(cds_t1, ImageURL(url='img', x='x', y='y', w=0.66, h=0.4))
plot_main.add_glyph(cds_t2, ImageURL(url='img', x='x', y='y', w=0.66, h=0.4))
plot_main.add_glyph(cds_t3, ImageURL(url='img', x='x', y='y', w=0.66, h=0.4))



##################################
#           Build beam           #
##################################

# build the beam object
beam = NFR_beam()

# plot beam, supports and its labels in the main plot
beam.plot_all(plot_main)

# plot its shadows into the other plots to have a reference for the data output
beam.plot_beam_shadow(plot_normalF)
beam.plot_beam_shadow(plot_deform)

# calculate the output for the inital setting
compute_new_scenario()





###################################
#           Page Layout           #
###################################

description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1000)

# rt_filename = join(dirname(__file__), "radio_button_title.html")
# rt = LatexDiv(text=open(rt_filename).read())

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
                       reset_button,
                       line_button),
                   column(plot_main,plot_normalF,plot_deform ) ) ) ] )



curdoc().add_root(doc_layout)
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '