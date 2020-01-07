
"""
Instant centre of rotation - 
@author: antonis / martin
"""
# general imports
from numpy import math, loadtxt
from os.path import dirname, join, split 
#from latex_support import LatexLabelSet, LatexSlider

# bokeh imports
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, Button, LabelSet, Div, Arrow, OpenHead, NormalHead, VeeHead
from bokeh.io import curdoc

# internal imports: none

# latex integration: none

#--------Data Source--------#
# ->TUM colors
color_TUM_black         = '#333333'
color_TUM_blue          = '#3070b3'
color_TUM_green         = '#a2ad00'
color_TUM_orange        = '#e37222'
color_TUM_grey          = '#b3b3b3'
color_TUM_greytext      = '#8a8a8a'
color_TUM_lightgrey1    = '#e6e6e6'
color_TUM_lightgrey2    = '#f7f7f7'

# -> trace curve
trace_curve_data = loadtxt('Instant_centre_of_rotation/graph.txt')
trace_curve_data_dictionary = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
trace_curve=ColumnDataSource(data=dict(x=[], y=[]))
#--------Data Source--------#

#--------initialize variables--------#
# -> define constant length
const_length                = 5
# -> immutable objects
wall_horizontal             = ColumnDataSource( data = dict(x=[0,0], y=[0,const_length+1]) )
wall_vertical               = ColumnDataSource( data = dict(x=[-1,const_length+1], y=[0,0]) )
wall_horizontal_hatching    = ColumnDataSource( data = dict(x=[0,0], y=[0,0]) )
wall_vertical_hatching      = ColumnDataSource( data = dict(x=[0,0], y=[0,0]) )
# -> mutable objects
current_coords              = ColumnDataSource( data = dict(x=[0],y=[const_length]) )
beam_position               = ColumnDataSource( data = dict(x=[0,0], y=[const_length,0]) )
support_A_locus             = ColumnDataSource( data = dict(x=[-1,const_length+1], y=[const_length,const_length]) )
support_B_locus             = ColumnDataSource( data = dict(x=[0,0], y=[-1,const_length+1]) )
support_A_arrow_source      = ColumnDataSource( data = dict(xS=[], xE=[], yS=[], yE=[]) )
support_B_arrow_source      = ColumnDataSource( data = dict(xS=[], xE=[], yS=[], yE=[]) )
support_A_label_source      = ColumnDataSource( data = dict(x=[0.50], y=[], text=['A']) )
support_B_label_source      = ColumnDataSource( data = dict(x=[], y=[0.50], text=['B']) )
ICR_label_source            = ColumnDataSource( data = dict(x=[0.1], y=[const_length+0.1], text=['ICR']))
#--------initialize variables--------#

#--------------------------------------Main--------------------------------------#
glob_var_dict = dict(x=0)

# -> create figure
fig = figure( plot_height=750, plot_width=750, tools="", x_range=(-1,const_length+1), y_range=(-1,const_length+1), toolbar_location=None )
fig.axis.visible = False
fig.grid.visible = False
fig.outline_line_color = None

# -> plot objects
fig.line(x='x', y='y', source=wall_horizontal, line_width=3, line_color=color_TUM_black)                        #Wall horizontal
fig.line(x='x', y='y', source=wall_vertical, line_width=3, line_color=color_TUM_black)                          #Wall vertival
fig.line(x='x', y='y', source=beam_position, line_width=10, line_color=color_TUM_grey)                          #beam
fig.line(x='x', y='y', source=support_A_locus, line_width=2, line_color=color_TUM_blue, line_dash=[10,10] )     #A locus    
fig.line(x='x', y='y', source=support_B_locus, line_width=2, line_color=color_TUM_blue, line_dash=[10,10] )     #B locus
fig.line(x='x', y='y', source=trace_curve, line_width=2, line_color=color_TUM_orange)                           #trace curve
fig.circle(x='x', y='y', source=current_coords, radius=0.05, line_color=color_TUM_orange, fill_color=color_TUM_orange) #ICR
support_A_arrow = Arrow( x_start='xS', y_start='yS', x_end='xE', y_end='yE', source=support_A_arrow_source, end=OpenHead(line_color=color_TUM_orange, line_width=3), line_color=color_TUM_orange, line_width=3 )
fig.add_layout(support_A_arrow) #Arrow A
support_B_arrow = Arrow( x_start='xS', y_start='yS', x_end='xE', y_end='yE', source=support_B_arrow_source, end=OpenHead(line_color=color_TUM_orange, line_width=3), line_color=color_TUM_orange, line_width=3 )
fig.add_layout(support_B_arrow) #Arrow B

# -> plot labels
support_A_label=LabelSet( x='x', y='y', text='text', source=support_A_label_source, text_font_size="15pt", level='glyph', text_color=color_TUM_orange )
fig.add_layout(support_A_label)
support_B_label=LabelSet( x='x', y='y', text='text', source=support_B_label_source, text_font_size="15pt", level='glyph', text_color=color_TUM_orange )
fig.add_layout(support_B_label)
ICR_label=LabelSet( x='x', y='y', text='text', source=ICR_label_source, text_font_size="15pt", level='glyph', text_color=color_TUM_orange )
fig.add_layout(ICR_label)

# -> inputs: create silder and button
slider_angle = Slider( title="angle in degree", value=0.0, start=0.0, end=90, step=90/40, width=400 )
button_structural_system = Button(label="button", button_type="success", width=100)

# -> function: updates the drawing, for change of angle
def slider_func(attr, old, new):
    angle=(slider_angle.value) * math.pi/180
    step=int(new * math.pi/180 * 40/90)
    #current coordinates
    x_current = const_length*math.sin(angle)
    y_current = const_length*math.cos(angle)
    current_coords.data = dict( x=[x_current], y=[y_current] )
    #length of arrows
    Arrow_length_A = x_current * 1/3
    Arrow_length_B = y_current * 1/3
	#adjusts the coordinates of the beam, the loci and the labels
    beam_position.data          = dict( x=[0,x_current], y=[y_current,0] )
    support_A_locus.data        = dict( x=[-1,const_length+1], y=[y_current, y_current] )
    support_B_locus.data        = dict( x=[x_current,x_current], y=[-1, const_length+1] )
    support_A_label_source.data = dict( x=[-0.2], y=[y_current-Arrow_length_A/2], text=['A'] )
    support_B_label_source.data = dict( x=[x_current+Arrow_length_B/2], y=[-0.2], text=['B'] )
    ICR_label_source.data       = dict( x=[x_current+0.1], y=[y_current+0.1], text=['ICR'] )
    #adjusts the coordinates of the arrows
    if Arrow_length_A < 0.01: #moves arrow out of range
        support_A_arrow_source.stream(dict( xS=[10], xE=[10], yS=[10], yE=[10]), rollover=1)
    else:
        support_A_arrow_source.stream(dict( xS=[0.05], xE=[0.05], yS=[y_current], yE=[y_current-Arrow_length_A]), rollover=1)
    if Arrow_length_B < 0.01: #moves arrow out of range
        support_B_arrow_source.stream(dict( xS=[10], xE=[10], yS=[10], yE=[10]), rollover=1)
    else:
        support_B_arrow_source.stream(dict( xS=[x_current], xE=[x_current+Arrow_length_B], yS=[0.05], yE=[0.05]), rollover=1)
    pass
    #refreshing trace curve
    trace_curve.data = dict( x=trace_curve_data[0:trace_curve_data_dictionary[step],0], y=trace_curve_data[0:trace_curve_data_dictionary[step],1])
    print(step)
    print(trace_curve)
# -> function: updates the drawing, for activateing the structural system
def button_func(attr, old, new):
    pass

# -> call functions
slider_angle.on_change('value',slider_func) #callback function
#button_structural_system.on_change('active',button_func)

#--------------------------------------Main--------------------------------------#

# add app description text
description_filename = join(dirname(__file__), "description.html")
description = Div(text=open(description_filename).read(), render_as_text=False, width=1200)

# send to window
curdoc().add_root(column(description,row(fig), slider_angle))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '



