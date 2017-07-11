# -*- coding: utf-8 -*-
"""
Created on Fri Jul 07 14:27:08 2017

"""
from bokeh.plotting import figure 
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, LabelSet, Arrow, OpenHead,Div
from bokeh.io import curdoc
from os.path import dirname, join
import numpy as np



#Force Vectors
P1_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
P2_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))

lineR1 = ColumnDataSource(data=dict(x = [], y = [] )) 
lineR2 = ColumnDataSource(data=dict(x = [], y = [] )) 
#labels for Forces
P1_label_source = ColumnDataSource(data=dict(x=[],y=[],P1=[]))
P2_label_source = ColumnDataSource(data=dict(x=[],y=[],P2=[]))

One_label_source = ColumnDataSource(data=dict(x=[],y=[],One=[]))
Two_label_source = ColumnDataSource(data=dict(x=[],y=[],Two=[]))
Three_label_source = ColumnDataSource(data=dict(x=[],y=[],Three=[]))

#plot corresponding  to  change in  Force

def initialise():
    P1_arrow_source.data = dict(xS=[0], xE=[5], yS=[-30], yE=[-18], lW = [5])
    P1_label_source.data = dict(x=[1],y=[-20],P1=['P1'])
    P2_arrow_source.data = dict(xS=[14], xE=[9], yS=[-6], yE=[-18], lW = [5])
    P2_label_source.data = dict(x=[10],y=[-15],P2=['P2'])   
    One_label_source.data = dict(x=[17],y=[-20],One=['One'])
    Two_label_source.data = dict(x=[9],y=[12],Two=['Two'])
    Three_label_source.data = dict(x=[33],y=[22],Three=['Three'])
    lineR1.data = dict (x=[0,5],y=[0,-18])
    lineR2.data = dict (x=[0,9],y=[0,-18])
    


plot = figure(title="Moment_a_free_vector", x_range=(0-2,40+2), y_range=(-50,50))
plot.axis.axis_label_text_font_style="normal"
plot.axis.axis_label_text_font_size="14pt"
#plot.xaxis.axis_label="Distance [m]"
#plot.yaxis.axis_label="Force[N]"
plot.oval(x=[20], y=[0], width=45, height=90,
          angle=-0.7, color="#1D91C0")
plot.circle([15,7,30], [-18,10,20], size=10,color="red")


plot.line(x='x', y='y', source=lineR1, color="black",line_width=3)
plot.line(x='x', y='y', source=lineR2, color="black",line_width=3)

#plotting Vectors as arrows
P1_arrow_glyph = Arrow(end=OpenHead(line_color="#A2AD00",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=P1_arrow_source,line_color="#A2AD00")
P2_arrow_glyph = Arrow(end=OpenHead(line_color="#A2AD00",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=P2_arrow_source,line_color="#A2AD00")
P1_label_glyph=LabelSet(x='x', y='y',text='P1',text_font_size="15pt",level='glyph',source=P1_label_source)
P2_label_glyph=LabelSet(x='x', y='y',text='P2',text_font_size="15pt",level='glyph',source=P2_label_source)
One_label_glyph=LabelSet(x='x', y='y',text='One',text_font_size="15pt",level='glyph',source=One_label_source)
Two_label_glyph=LabelSet(x='x', y='y',text='Two',text_font_size="15pt",level='glyph',source=Two_label_source)
Three_label_glyph=LabelSet(x='x', y='y',text='Three',text_font_size="15pt",level='glyph',source=Three_label_source)


#plot.line(x='x',y='y', source=R2_line,line_width=3,line_color='red',legend=" R1" )
#plot.line(x='x',y='y', source=R2_line,line_width=3,line_color='red',legend=" R2" )

plot.add_layout(P1_arrow_glyph)
plot.add_layout(P2_arrow_glyph)
plot.add_layout(P1_label_glyph)
plot.add_layout(P2_label_glyph)
plot.add_layout(One_label_glyph)
plot.add_layout(Two_label_glyph)
plot.add_layout(Three_label_glyph)


initialise()

def FindM(attr,old,new):
    if new == 1:
        lineR1.data = dict (x=[15,5],y=[-18,-18])
        lineR2.data = dict (x=[15,9],y=[-18,-18])
    if new == 2:
        lineR1.data = dict (x=[7,5],y=[10,-18])
        lineR2.data = dict (x=[7,9],y=[10,-18])
    if new == 3 :
        lineR1.data = dict (x=[30,5],y=[20,-18])
        lineR2.data = dict (x=[30,9],y=[20,-18])
 

    
#creating  slider to change location of Forces F1 and F2
FindMoment_slider= Slider(title="Find Couple Moment at",value= 0,start = 0, end = 3, step = 1)
FindMoment_slider.on_change('value',FindM)

#adding description from HTML file
description_filename = join(dirname(__file__), "description.html")
description = Div(text=open(description_filename).read(), render_as_text=False, width=1200)

curdoc().add_root(column(description,row(plot,column(FindMoment_slider))))
curdoc().title = "Moment_a_free_vector"