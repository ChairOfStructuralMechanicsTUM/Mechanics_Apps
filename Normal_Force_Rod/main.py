"""
Normal Force Rod - presents the influence of different loads on force and deformation

"""
# general imports
from __future__ import division # float division only, like in python 3
from math import ceil
import numpy as np

# bokeh imports
from bokeh.io             import curdoc
from bokeh.plotting       import Figure
from bokeh.models         import ColumnDataSource, LabelSet, Arrow, OpenHead, NormalHead
from bokeh.models.glyphs  import MultiLine, Rect ,ImageURL
from bokeh.models.layouts import Spacer
from bokeh.models.widgets import Paragraph, Button, RadioButtonGroup, RadioGroup
from bokeh.layouts        import column, row, widgetbox, layout

# internal imports
from NFR_beam      import NFR_beam
from NFR_equations import calcNU
from NFR_constants import (
        xr_start, xr_end,
        color_rod, num_symbols,
        color_nf, color_def, c_black, c_gray,
        x_range, fig_height,
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

beam_measure_label_source = ColumnDataSource(data=dict(x=[], y=[], text=[])) # position and text for measure labels in the main plot
zero_label_source         = ColumnDataSource(data=dict(x=[], y=[], text=[])) # position and text for the labels in force plot
extrem_val_label_source   = ColumnDataSource(data=dict(x=[], y=[], text=[])) # position and text for the labels in deformation plot



################################
#      Callback Functions      #
################################

def change_load(attr, old, new):
    beam.set_load(new)
    
    # if the temperature load is selected, display either fire or snow symbols
    # based on the selected amplitude
    if new == 3: # temperature load
        if radio_group_ampl.active==0: # -1
            snow_glyphs.visible = True
            fire_glyphs.visible = False
        elif radio_group_ampl.active==1: #1
            snow_glyphs.visible = False
            fire_glyphs.visible = True
    # if another load is selected, do not display any symbols
    else:
        snow_glyphs.visible = False
        fire_glyphs.visible = False

    compute_new_scenario()

def change_left_support(attr, old, new):
    beam.set_left_support(new)

    if radio_group_right.active==1 and new==1: # both slide
        show_error(True)
    else:
        show_error(False)
        compute_new_scenario()


def change_right_support(attr, old, new):
    beam.set_right_support(new)

    if radio_group_left.active==1 and new==1: # both slide
        show_error(True)
    else:
        show_error(False)
        compute_new_scenario()


def change_amplitude(attr, old, new):
    beam.set_load_direction(new)

    if radio_button_group.active == 3: # temperature
        if new == 0: #-1
            snow_glyphs.visible = True
            fire_glyphs.visible = False
        else:
            snow_glyphs.visible = False
            fire_glyphs.visible = True

    compute_new_scenario()


def change_load_position(attr, old, new):
    beam.move_load(new)
    compute_new_scenario()


def reset():
    radio_button_group.active    = initial_load
    radio_group_left.active      = 0
    radio_group_right.active     = 1
    radio_group_ampl.active      = 1
    load_position_slider.value   = initial_load_position
    # possibly set the values in beam correspondingly - # ok no, happens automatically
    # setting the values via their attributes seems to call the callback functions as well
    aux_line.data                = dict(x=[], y=[])
    zero_label_source.data       = dict(x=[], y=[], text=[])
    extrem_val_label_source.data = dict(x=[], y=[], text=[])
    line_button.label            = "Show line"
    compute_new_scenario()


def change_line_visibility():
    if line_button.label == "Show line":
        move_aux_line()
        line_button.label = "Hide line"
    elif line_button.label == "Hide line":
        aux_line.data                = dict(x=[], y=[])
        zero_label_source.data       = dict(x=[], y=[], text=[])
        extrem_val_label_source.data = dict(x=[], y=[], text=[])
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


def n2str(number, n=4):
    # costum number to string function
    # rounds up to n decimals and crops zeros 
    # e.g.  0.210000  --> 0.21
    #       0.1654486 --> 0.1654
    return str(round(number,n))


def move_aux_line():
    # only for fixed supports on both sides, but would work in general

    # fetch data
    x_samples = graph_N.data['x']
    y_samples = graph_N.data['y']
    #y_value   = graph_U.data['y']
    roots     = []

    # find the zero crossings
    for i in range(0,len(y_samples)-1):
        if y_samples[i]*y_samples[i+1] < 0: # sign changes => root
            r = 0.5*(x_samples[i+1]-x_samples[i]) + x_samples[i]
            #print(r, 0.5*abs((y_value[i+1]-y_value[i]))+np.sign(y_value[i])*max(abs(y_value[i]), abs(y_value[i+1])) )
            roots.append([r,r])

    if roots!=[] and radio_group_left.active==0 and radio_group_right.active==0: # fixed/fixed
        a = -1 if radio_group_ampl.active==0 else 1 # set the sign
        k = load_position_slider.value
        ## point load labels
        if radio_button_group.active==0:
            new_data_zero    = dict(x=[0], y=[-2*a], text=["x_0="+n2str(k/10)+"L"])
            new_data_extreme = dict(x=[0], y=[-2*a], text=["u(x_0)="+n2str( -k*(k/10 - 1)/10 )+"\\frac{F L}{EA}"])
        ## constant load labels
        elif radio_button_group.active==1:
            new_data_zero    = dict(x=[0], y=[-2*a], text=["x_0="+n2str((20*k-k**2)/200)+"L"])
            new_data_extreme = dict(x=[0], y=[-2*a], text=["u(x_0)="+n2str(a*(k**2 * (k/20-1)**2)/200)+"\\frac{p L^2}{EA}"])
        ## triangular load labels
        elif radio_button_group.active==2:
            new_data_zero    = dict(x=[0], y=[-2*a], text=["x_0="+n2str(-k*((k/30)**(1/2) - 1)/10)+"L"])
            new_data_extreme = dict(x=[0], y=[-2*a], text=["u(x_0)="+n2str( a*(k**2*((30**(1/2)*k**(3/2))/15 - 3*k + 30))/18000 )+"\\frac{p L^2}{EA}"])
        else:
            new_data_zero    = dict(x=[], y=[], text=[])
            new_data_extreme = dict(x=[], y=[], text=[])
    else:
        new_data_zero    = dict(x=[], y=[], text=[])
        new_data_extreme = dict(x=[], y=[], text=[])

    zero_label_source.data = new_data_zero
    extrem_val_label_source.data = new_data_extreme

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
plot_main = Figure(title="Rod with Supports and Load", tools="", x_range=x_range, y_range=(-2.0,2.5), height=fig_height)
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

# measures
beam_measure_doublearrow_glyph = Arrow(start=OpenHead(line_color=c_black, line_width=2, size=8), end=OpenHead(line_color='black',line_width= 2, size=8),
    x_start=xr_start, y_start=-1.2, x_end=xr_end, y_end=-1.2, line_width=5, line_color=c_black)
beam_measure_singlearrow_glyph = Arrow(end=NormalHead(fill_color=c_gray, line_width=1, size=6),
    x_start=xr_start-0.1, y_start=-0.8, x_end=xr_start+0.8, y_end=-0.8, line_width=1, line_color=c_black)

beam_measure_label_source.data = dict(x=[xr_start+0.25, 0.5*(xr_end-xr_start)], y=[-0.7,-1.6], text=["x","L"])
beam_measure_label = LatexLabelSet(x='x', y='y', text='text', source=beam_measure_label_source, level='glyph')#, x_offset=3, y_offset=-15)
plot_main.line(x=[xr_start, xr_start], y=[-0.7,-0.9], line_color=c_black) # vertical line for single x-arrow
plot_main.add_layout(beam_measure_singlearrow_glyph)
plot_main.add_layout(beam_measure_doublearrow_glyph)
plot_main.add_layout(beam_measure_label)


# graphics for a cold beam
snow_images = ["Normal_Force_Rod/static/images/snowflake01.svg",
               "Normal_Force_Rod/static/images/snowflake02.svg",
               "Normal_Force_Rod/static/images/snowflake03.svg"]

cds_snow = ColumnDataSource(data=dict(x=np.linspace(xr_start+0.5, xr_end-0.5,num_symbols),
                                      y=np.zeros((num_symbols,1)).flatten(),
                                      # copy the image list often enough and select the first num_symbols images
                                      # this way the symbols will be repeated in order
                                      img=(snow_images*ceil(num_symbols/len(snow_images)))[:num_symbols]
                                      ))

snow_glyphs = plot_main.add_glyph(cds_snow, ImageURL(url='img', x='x', y='y', w=0.66, h=0.4, anchor="center"))
snow_glyphs.visible = False
snow_glyphs.level = "overlay"


# graphics for a hot beam
fire_images = ["Normal_Force_Rod/static/images/fire01.svg",
               "Normal_Force_Rod/static/images/fire02.svg",
               "Normal_Force_Rod/static/images/fire03.svg"]

cds_fire = ColumnDataSource(data=dict(x=np.linspace(xr_start+0.5, xr_end-0.5,num_symbols),
                                      y=np.zeros((num_symbols,1)).flatten(),
                                      # copy the image list often enough and select the first num_symbols images
                                      # this way the symbols will be repeated in order
                                      img=(fire_images*ceil(num_symbols/len(fire_images)))[:num_symbols]
                                      ))

fire_glyphs = plot_main.add_glyph(cds_fire, ImageURL(url='img', x='x', y='y', w=0.66, h=0.4, anchor="bottom_center"))
fire_glyphs.visible = False
fire_glyphs.level = "overlay"




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
plot_normalF.line(x='x', y='y', source=graph_N, color=color_nf ,line_width=2)

# plot helper line
plot_normalF.add_glyph(aux_line, aux_line_glyph)

# zero crossing label
zero_label = LatexLabelSet(x='x', y='y', text='text', source=zero_label_source, level='glyph')
plot_normalF.add_layout(zero_label)




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
plot_deform.line(x='x', y='y', source=graph_U, color=color_def, line_width=2)

# plot helper line
plot_deform.add_glyph(aux_line, aux_line_glyph)

# extremum label
extrem_val_label = LatexLabelSet(x='x', y='y', text='text', source=extrem_val_label_source, level='glyph')
plot_deform.add_layout(extrem_val_label)



###################################
#       Buttons and Sliders       #
###################################
radio_button_group = RadioButtonGroup(labels=["Point Load", "Constant Load", "Triangular Load", "Temperature"], active=initial_load, width=400)

radio_group_left  = RadioGroup(labels=["fixed", "sliding"], active=0, inline=True)
radio_group_right = RadioGroup(labels=["fixed", "sliding"], active=1, inline=True)
#radio_group_cross = RadioGroup(labels=["constant", "tapered"], active=0, inline=True) # cross-section not yet
radio_group_ampl  = RadioGroup(labels=["-1", "+1"], active=1, inline=True) # amplitude

load_position_slider  = LatexSlider(title="\\mathrm{Load \ Position:}", value_unit='\\frac{\\mathrm{L}}{\\mathrm{10}}', value=initial_load_position, start=xr_start, end=xr_end, step=1.0, width=400)

reset_button = Button(label="Reset", button_type="success", width=400)
line_button  = Button(label="Show line", button_type="success", width=400)


## call their corresponding callback functions

radio_button_group.on_change('active',change_load)

radio_group_left.on_change('active', change_left_support)
radio_group_right.on_change('active', change_right_support)
radio_group_ampl.on_change('active',change_amplitude)

load_position_slider.on_change('value', change_load_position)

reset_button.on_click(reset)
line_button.on_click(change_line_visibility)



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

p_rt1 = Paragraph(text="""Left support:  """)
p_rt2 = Paragraph(text="""Right support: """)
#p_rt3 = Paragraph(text="""Cross-section: """)
p_rt4 = Paragraph(text="""Load Amplitude:""")


doc_layout = layout(children=[
        column(description,
               row(column(
                       Spacer(height=20,width=400),
                       widgetbox(radio_button_group),
                       row(widgetbox(p_rt1, width=120), widgetbox(radio_group_left)),
                       row(widgetbox(p_rt2, width=120), widgetbox(radio_group_right)),
                       row(widgetbox(p_rt4, width=120), widgetbox(radio_group_ampl)),
                       load_position_slider,
                       reset_button,
                       line_button),
                   column(plot_main,plot_normalF,plot_deform ) ) ) ] )



curdoc().add_root(doc_layout)
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '