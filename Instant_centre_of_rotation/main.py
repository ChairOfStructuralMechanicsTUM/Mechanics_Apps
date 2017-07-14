# -*- coding: utf-8 -*-
"""
@author: antonis
"""
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, LabelSet, Div
from bokeh.io import curdoc
from numpy import math,loadtxt
from os.path import dirname, join, split 

#define constant length
l=4;
#load txt file which includes the coordinates of the spurkurve line
DataPlotter = loadtxt('Instant_centre_of_rotation/graph.txt');
DataPlotterDictionary = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]; 
#data sources for drawing
bar_position_source=ColumnDataSource(data=dict(x=[], y=[]))
vb_arrow_source=ColumnDataSource(data=dict(x=[], y=[])) 
Vb_label_source=ColumnDataSource(data=dict(x=[],y=[],Vb=[''])) 
va_arrow_source=ColumnDataSource(data=dict(x=[0, 0.5,0.35,0.5,0.35], y=[0,0,0.15,0,-0.15]))
Va_label_source=ColumnDataSource(data=dict(x=[0.50], y=[0],Va=['V']))
vb_perpendicular = ColumnDataSource(data=dict(x=[0,5], y=[l,l]))
va_perpendicular = ColumnDataSource(data=dict(x=[0,0],y=[0,l]))
current_coords= ColumnDataSource(data=dict(x=[0],y=[l]))
vertical_wall=ColumnDataSource(data=dict(x=[-0.25,-0.04,-0.04,-0.25,-0.04,-0.04,-0.25,-0.04,-0.04,-0.25,-0.04,-0.04,-0.25,-0.04,-0.04,-0.25,-0.04,-0.04,-0.25,-0.04,-0.04,-0.25,-0.04,-0.04,-0.25,-0.04,-0.04,-0.25,-0.04,-0.04,-0.25,-0.04],y=[-0.25,-0.04,0.5,0.25,0.5,1,0.75,1,1.5,1.25,1.5,2,1.75,2,2.5,2.25,2.5,3,2.75,3,3.5,3.25,3.5,4,3.75,4,4.5,4.25,4.5,5,4.75,5]))
horizontal_wall=ColumnDataSource(data=dict(x=[-0.25,-0.04,0.5,0.25,0.5,1,0.75,1,1.5,1.25,1.5,2,1.75,2,2.5,2.25,2.5,3,2.75,3,3.5,3.25,3.5,4,3.75,4,4.5,4.25,4.5,5,4.75,5],y=[-0.25,-0.04,-0.04,-0.25,-0.04,-0.04,-0.25,-0.04,-0.04,-0.25,-0.04,-0.04,-0.25,-0.04,-0.04,-0.25,-0.04,-0.04,-0.25,-0.04,-0.04,-0.25,-0.04,-0.04,-0.25,-0.04,-0.04,-0.25,-0.04,-0.04,-0.25,-0.04]))
ICR_label_source = ColumnDataSource(data=dict(x=[0],y=[l+0.1],ICR=['ICR']))
spurkurve=ColumnDataSource(data=dict(x=[], y=[]))

def init():  
    # initialise the position of the bar
    X=[0, 0]
    Y=[0, l]
    bar_position_source.data = dict(x=X, y=Y)
     
########### Main ###########
## Initialise
init()
p = figure(plot_height=875, plot_width=1000, tools="", x_range=(-1,5), y_range=(-1,5))
#p.title.text_font_size="18pt"
#  remove graph lines
p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None
p.line(x='x', y='y', source=bar_position_source,line_width=10,line_color='grey') 
p.line(x='x', y='y', source=vb_perpendicular, line_color='purple',line_width=3,line_dash=[10,10]) 
p.line(x='x', y='y', source=va_perpendicular, line_color='purple',line_width=3,line_dash=[10,10]) 
p.line(x='x', y='y', source=va_arrow_source,line_width=3, line_color='red')
p.line(x='x', y='y', source=vb_arrow_source,line_width=3,line_color='red')
p.circle(x='x', y='y', source=current_coords, radius=0.05)
p.line(x='x',y='y',source=vertical_wall,line_width=3,line_color='black')
p.line(x='x',y='y',source=horizontal_wall,line_width=3,line_color='black')
ICR_label_glyph=LabelSet(x='x', y='y',text='ICR',text_font_size="15pt",level='glyph',source=ICR_label_source)
p.add_layout(ICR_label_glyph)
Vb_label_glyph=LabelSet(x='x', y='y',text='Vb',text_font_size="15pt",text_color='red',level='glyph',source=Vb_label_source)
p.add_layout(Vb_label_glyph)
Va_label_glyph=LabelSet(x='x', y='y',text='Va',text_font_size="15pt",text_color='red',level='glyph',source=Va_label_source)
p.add_layout(Va_label_glyph)
p.line(x='x',y='y', source=spurkurve,line_width=3,line_color='red',legend="Spurkurve" )
p.legend.location="top_right"
p.legend.label_text_font_size="15pt"

## Create slider widget to choose angle wmega
Wmega_input = Slider(title="angle "u"\u03B8 in radians", value=0.0, start=0.0, end=math.pi/2, step=math.pi/40)

def slide(attrname, old, new): #function which updates the drawing for the change of angle wmega with the use of the bar
    global DataPlotter, DataPlotterDictionary
    w=Wmega_input.value
    bar_position_source.data=dict(x=[l*math.sin(w), 0],y=[0,l*math.cos(w)])
    vb_perpendicular.data=dict(x=[0,5],y=[l*math.cos(w),l*math.cos(w)])
    va_perpendicular.data=dict(x=[l*math.sin(w),l*math.sin(w)],y=[0,5])
    if w!=1.5708:
        va_arrow_source.data=dict(x=[0+l*math.sin(w), 0.5+l*math.sin(w),0.35+l*math.sin(w),0.5+l*math.sin(w),0.35+l*math.sin(w)],y=[0,0,0.15,0,-0.15])
    else:
        va_arrow_source.data=dict(x=[],y=[])
        
    if w!=0:
        vb_arrow_source.data=dict(x=[0,0,0.15,0,-0.15],y=[l*math.cos(w),-0.5+l*math.cos(w),-0.35+l*math.cos(w),-0.5+l*math.cos(w),-0.35+l*math.cos(w)])
    else:
        vb_arrow_source.data=dict(x=[],y=[])
        
    current_coords.data=dict(x=[l*math.sin(w)],y=[l*math.cos(w)])
    ICR_label_glyph.text_alpha=1
    ICR_label_source.data=dict(x=[0.1+l*math.sin(w)],y=[0.1+l*math.cos(w)],ICR=['ICR'])
    Vb_label_source.data=dict(x=[0],y=[l*math.cos(w)-0.77],Vb=['V'])
    Va_label_source.data=dict(x=[0.50+l*math.sin(w)],y=[0],Va=['V'])
    i=int(new*40/math.pi)
    spurkurve.data = dict(x=DataPlotter[0:DataPlotterDictionary[i],0],y=DataPlotter[0:DataPlotterDictionary[i],1])
Wmega_input.on_change('value',slide)

# add app description
description_filename = join(dirname(__file__), "description.html")

description = Div(text=open(description_filename).read(), render_as_text=False, width=1200)


curdoc().add_root(column(description,row(p),Wmega_input))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '









