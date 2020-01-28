
"""
Instant centre of rotation - 
@author: antonis / martin
"""
# general imports
from numpy      import math, loadtxt

# bokeh imports
from bokeh.plotting         import figure
from bokeh.models.layouts   import Spacer
from bokeh.layouts          import column, row, widgetbox, layout
from bokeh.models           import ColumnDataSource, Slider, Button, LabelSet, Div, Arrow, OpenHead, NormalHead, VeeHead
from bokeh.models.glyphs    import ImageURL
from bokeh.io               import curdoc

# internal imports
from TA_constants           import (
    slide_support_img,                              # support image
    support_width, support_height,                  # support scale
    c_black, c_blue, c_orange, c_gray, c_white      # colors used
)

# latex integration
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexDiv, LatexLabel, LatexLabelSet, LatexSlider, LatexLegend

#--------Data Source--------#
# -> trace curve
trace_curve_data = loadtxt('Instant_centre_of_rotation/graph.txt')
trace_curve=ColumnDataSource( data = dict(x=[], y=[]))
# -> Hatching
hatching_data = loadtxt('Instant_centre_of_rotation/hatching.txt')
wall_horizontal_hatching    = ColumnDataSource( data = dict(x=hatching_data[0:105,0], y=hatching_data[0:105,1]) )
wall_vertical_hatching      = ColumnDataSource( data = dict(x=hatching_data[106:196,0], y=hatching_data[106:196,1]) )
#--------Data Source--------#

#--------initialize variables--------#
# -> define constant length
const_length                = 5
# -> global variable
global_vars = dict(show=-1)
# -> immutable objects
wall_horizontal             = ColumnDataSource( data = dict( x=[-1,const_length+1], y=[-0.06,-0.06]) )
wall_vertical               = ColumnDataSource( data = dict( x=[-0.06,-0.06], y=[-0.06,const_length+1]) )
Frame_w                     = ColumnDataSource( data = dict( x=[0.5,3,3,0.5,0.5], y=[0.1,0.1,0.4,0.4,0.1]))
Frame_u                     = ColumnDataSource( data = dict( x=[0.5,3,3,0.5,0.5], y=[-0.1,-0.1,-0.4,-0.4,-0.1]))
displacement_ratio_w        = ColumnDataSource( data = dict( x=[0.52,0.52], y=[0.25,0.25]) )
displacement_ratio_u        = ColumnDataSource( data = dict( x=[0.52,2.98], y=[-0.25,-0.25]) )
displacement_ratio_w_label  = ColumnDataSource( data = dict( x=[0.1], y=[0.15], text=['w:']) )
displacement_ratio_u_label  = ColumnDataSource( data = dict( x=[0.1], y=[-0.35], text=['u:']) )
# -> mutable objects
current_coords              = ColumnDataSource( data = dict( x=[0],y=[const_length], x0=[0], y0=[0]) )
beam_position               = ColumnDataSource( data = dict( x=[0,0], y=[const_length,0]) )
support_A_img_source        = ColumnDataSource( data = dict( sp_img=[], x=[] , y=[]) )
support_B_img_source        = ColumnDataSource( data = dict( sp_img=[], x=[] , y=[]) )
support_A_locus             = ColumnDataSource( data = dict( x=[-1,const_length+1], y=[const_length,const_length]) )
support_B_locus             = ColumnDataSource( data = dict( x=[0,0], y=[-1,const_length+1]) )
displacement_w_source       = ColumnDataSource( data = dict( xS=[0], xE=[0], yS=[const_length], yE=[const_length-0.8]) )
displacement_u_source       = ColumnDataSource( data = dict( xS=[0], xE=[0+0.8], yS=[0], yE=[0]) )
displacement_w_label_source = ColumnDataSource( data = dict( x=[0.05], y=[const_length-0.45], text=['w']) )
displacement_u_label_source = ColumnDataSource( data = dict( x=[0.3], y=[0.05], text=['u']) )
ICR_label_source            = ColumnDataSource( data = dict( x=[0.1], y=[const_length+0.1], text=['ICR']) )
#--------initialize variables--------#

#--------------------------------------Main--------------------------------------#
# -> create figures
fig_1 = figure( plot_height=650, plot_width=650, tools="", x_range=(-1,const_length+1), y_range=(-1,const_length+1), toolbar_location=None )
fig_1.axis.visible = False
fig_1.grid.visible = False
fig_1.outline_line_color = None
fig_2 = figure( plot_height=100, plot_width=310, tools="", x_range=(0,3.05), y_range=(-0.55,0.55), toolbar_location=None )
fig_2.axis.visible = False
fig_2.grid.visible = False
fig_2.outline_line_color = None

# -> plot objects
fig_1.line(x='x', y='y', source=wall_horizontal_hatching, line_width=1, line_color=c_black)                 #Wall horizontal hatching
fig_1.line(x='x', y='y', source=wall_vertical_hatching, line_width=1, line_color=c_black)                   #Wall vertical hatching
fig_1.line(x='x', y='y', source=wall_horizontal, line_width=3, line_color=c_black)                          #Wall horizontal
fig_1.line(x='x', y='y', source=wall_vertical, line_width=3, line_color=c_black)                            #Wall vertival
fig_1.line(x='x', y='y', source=beam_position, line_width=10, line_color=c_gray)                            #beam
fig_1.circle(x='x0', y='y', source=current_coords, radius=0.06, line_color=c_black, fill_color=c_white)     #joint A
fig_1.circle(x='x', y='y0', source=current_coords, radius=0.06, line_color=c_black, fill_color=c_white)     #joint B
fig_1.line(x='x', y='y', source=support_A_locus, line_width=2, line_color=c_blue, line_dash=[10,10] )       #A locus 
fig_1.line(x='x', y='y', source=support_B_locus, line_width=2, line_color=c_blue, line_dash=[10,10] )       #B locus
fig_1.line(x='x', y='y', source=trace_curve, line_width=2, line_color=c_orange)                             #trace curve
displacement_w = Arrow(end=OpenHead(line_color=c_blue, line_width=2), x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_color=c_blue, line_width=2, level='glyph', source=displacement_w_source)
fig_1.add_layout(displacement_w)                                                                            #displacement w
displacement_u = Arrow(end=OpenHead(line_color=c_blue, line_width=2), x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_color=c_blue, line_width=2, level='glyph', source=displacement_u_source)
fig_1.add_layout(displacement_u)                                                                            #displacement u
displacement_w_label = LabelSet( x='x', y='y', text='text', source=displacement_w_label_source, text_font_size="15pt", level='glyph', text_color=c_blue )
fig_1.add_layout(displacement_w_label)                                                                      #displacement w label
displacement_u_label = LabelSet( x='x', y='y', text='text', source=displacement_u_label_source, text_font_size="15pt", level='glyph', text_color=c_blue )
fig_1.add_layout(displacement_u_label)                                                                      #displacement u label

# -> add support images
fig_1.add_glyph(support_A_img_source , ImageURL(url="sp_img", x="x", y="y",  w=0.66, h=0.4, anchor="center", angle=3/2*math.pi))
fig_1.add_glyph(support_B_img_source , ImageURL(url="sp_img", x="x", y="y",  w=0.66, h=0.4, anchor="center"))

# -> plott ICR
fig_1.circle(x='x', y='y', source=current_coords, radius=0.05, line_color=c_orange, fill_color=c_orange) #ICR
ICR_label=LabelSet( x='x', y='y', text='text', source=ICR_label_source, text_font_size="15pt", level='glyph', text_color=c_orange )
fig_1.add_layout(ICR_label)

# -> displacement ratio 
fig_2.line(x='x', y='y', source=displacement_ratio_w, line_width=22, line_color=c_blue)
fig_2.line(x='x', y='y', source=displacement_ratio_u, line_width=22, line_color=c_blue)
fig_2.line(x='x', y='y', source=Frame_w, line_width=4, line_color=c_black)
fig_2.line(x='x', y='y', source=Frame_u, line_width=4, line_color=c_black)  
ratio_w_label = LabelSet( x='x', y='y', text='text', source=displacement_ratio_w_label, text_font_size="15pt", level='glyph', text_color=c_black )
fig_2.add_layout(ratio_w_label)
ratio_u_label = LabelSet( x='x', y='y', text='text', source=displacement_ratio_u_label, text_font_size="15pt", level='glyph', text_color=c_black )
fig_2.add_layout(ratio_u_label)

# -> inputs: create silder and button
slider_angle= LatexSlider(title='\\text{Inclination of ladder:}', value_unit='^{\\circ}', value=0.0, start=0.0, end=90, step=90/20)
#slider_angle.on_change('value',changeTheta1)
#slider_angle = Slider( title="Inclination of ladder", value=0.0, start=0.0, end=90, step=90/20, width=300 )
button_structural_system = Button(label="Show/Hide structural system", button_type="success", width=300)

# -> function: updates the drawing, for change of angle
def slider_func(attr, old, new):
    angle=(slider_angle.value) * math.pi/180
    trace_curve_index=int(round(angle * 180/math.pi * 20/90,0))
    #current coordinates
    x_current = trace_curve_data[trace_curve_index,0]
    y_current = trace_curve_data[trace_curve_index,1]
    current_coords.data = dict( x=[x_current], y=[y_current], x0=[0], y0=[0] )
    #displacement w and u
    ratio_w = 1/(x_current+y_current) * x_current 
    ratio_u = 1/(x_current+y_current) * y_current
    displacement_ratio_w.data   = dict( x=[0.52,0.52+2.48*ratio_w], y=[0.25,0.25])
    displacement_ratio_u.data   = dict( x=[0.52,0.52+2.48*ratio_u], y=[-0.25,-0.25])
	#adjusts the coordinates of all mutable objects
    beam_position.data          = dict( x=[0,x_current], y=[y_current,0] )
    support_A_locus.data        = dict( x=[-1,const_length+1], y=[y_current, y_current] )
    support_B_locus.data        = dict( x=[x_current,x_current], y=[-1, const_length+1] )
    ICR_label_source.data       = dict( x=[x_current+0.1], y=[y_current+0.1], text=['ICR'] )
    displacement_w_label_source.data        = dict( x=[0.05], y=[y_current-0.45], text=['w'])
    displacement_u_label_source.data        = dict( x=[x_current+0.3], y=[0.05], text=['u'])
    displacement_w_source.stream(           dict( xS=[0], xE=[0], yS=[y_current], yE=[y_current-0.8]), rollover=-1)
    displacement_u_source.stream(           dict( xS=[x_current], xE=[x_current+0.8], yS=[0], yE=[0]), rollover=-1)
    if global_vars['show'] == 1:
        support_A_img_source.data           = dict( sp_img=[slide_support_img], x=[0.4] , y=[y_current+0.14] )
        support_B_img_source.data           = dict( sp_img=[slide_support_img], x=[x_current] , y=[-0.14] )
        wall_horizontal_hatching.data       = dict(x=[], y=[])
        wall_vertical_hatching.data         = dict(x=[], y=[])
    else:
        support_A_img_source.data           = dict( sp_img=[], x=[] , y=[] )
        support_B_img_source.data           = dict( sp_img=[], x=[] , y=[] )
        wall_horizontal_hatching.data       = dict(x=hatching_data[0:105,0], y=hatching_data[0:105,1])
        wall_vertical_hatching.data         = dict(x=hatching_data[106:198,0], y=hatching_data[106:198,1])
    trace_curve.data = dict( x=trace_curve_data[0:trace_curve_index+1,0], y=trace_curve_data[0:trace_curve_index+1,1])
    pass
    
# -> function: show/hide structural system
def show_structural_system():
    global_vars['show']=global_vars['show'] * -1
    slider_func(None,None,None)
    pass

# -> call functions
slider_angle.on_change('value',slider_func)
button_structural_system.on_click(show_structural_system)

#--------------------------------------Main--------------------------------------#

# add app description text
description_filename = join(dirname(__file__), "description.html")
description = Div(text=open(description_filename).read(), render_as_text=False, width=1200)
caption_filename = join(dirname(__file__), "caption.html")
caption = Div(text=open(caption_filename).read(), render_as_text=False, width=300)

# send to window
doc_layout=layout(children=[ column(description, row( column( widgetbox(slider_angle), widgetbox(button_structural_system), Spacer(height=50,width=300), caption, fig_2), column(fig_1) ) ) ] )
curdoc().add_root(doc_layout)
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '