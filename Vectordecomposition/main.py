# -*- coding: utf-8 -*-
"""
Created on Sat May  4 22:02:48 2019

@author: Dawood com
"""

from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.models import ColumnDataSource, Slider, LabelSet, Arrow, OpenHead, Button, Line,Div, NormalHead
from bokeh.io import curdoc
from numpy import loadtxt
from os.path import dirname, join, split
from math import radians, cos, sin, tan, sqrt, atan, pi
from bokeh.models.glyphs import Ray

from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexDiv, LatexLabel, LatexLabelSet, LatexSlider, LatexLegend

a=(50**2)+(50**2)
b=sqrt(a)
#print b
Vector_source         = ColumnDataSource(data=dict(xS=[0], xE=[50], yS=[0],yE=[50]))
glob_Vector1           = ColumnDataSource(data=dict(val=[70]))
Vector2_source         = ColumnDataSource(data=dict(xS=[], xE=[], yS=[],yE=[]))
Vector3_source         = ColumnDataSource(data=dict(xS=[], xE=[], yS=[],yE=[]))
glob_theta1            = ColumnDataSource(data=dict(val=[radians(45)]))
glob_active   = ColumnDataSource(data=dict(Active=[False]))
V_label_source        = ColumnDataSource(data=dict(x=[50+3],y=[50-3],V1=['V']))
V1_label_source        = ColumnDataSource(data=dict(x=[],y=[],V=[]))
V2_label_source        = ColumnDataSource(data=dict(x=[],y=[],V=[]))
Resultant_values_source = ColumnDataSource(data=dict(x=[],y=[],names=[]))
def init ():
    createtwoarrows()
    changevectorvalue()
    
def createtwoarrows():
    [Vector1] = glob_Vector1.data["val"]
    [theta1 ] = glob_theta1.data["val"]
#    if (Vector1== 0):
#        Vector_source.data = dict(xS=[0], xE=[0], yS=[50],yE=[50])
#    
#    else:
    xE=Vector1*cos(theta1)
    yE=Vector1*sin(theta1)
#    print xE,yE
    Vector_source.data = dict(xS=[0],yS=[0],xE=[xE],yE=[yE])
    V_label_source.data= dict (x=[xE+3],y=[yE-3],V1=['V',])
#    Vector2_source.data = dict(xS=[0],yS=[0],xE=[xE],yE=[0])
#    Vector3_source.data = dict(xS=[0],yS=[0],xE=[0],yE=[yE])

def createarrows():
    [Vector1] = glob_Vector1.data["val"]
    [theta1 ] = glob_theta1.data["val"]
    [Active] = glob_active.data["Active"]
    if ( Active):
         Vector2_source.data = dict(xS=[],yS=[],xE=[],yE=[])
         Vector3_source.data = dict(xS=[],yS=[],xE=[],yE=[])
         V1_label_source.data=dict(x=[],y=[],V=[])
         V2_label_source.data=dict(x=[],y=[],V=[])
         Resultant_values_source.data = dict(x=[], y=[], names=[])
         
         glob_active.data   = dict(Active=[False])
         show_button.label = 'Show components'
    else:
        xE=Vector1*cos(theta1)
        yE=Vector1*sin(theta1)
        z=yE/2
        z1=xE/2
        z2=round(atan(yE/xE)/pi*180,0)
        

        Vector2_source.data = dict(xS=[0],yS=[0],xE=[xE],yE=[0])
        Vector3_source.data = dict(xS=[0],yS=[0],xE=[0],yE=[yE])
        V1_label_source.data=dict(x=[0-20],y=[z],V=['Vy'])
        V2_label_source.data=dict(x=[z1],y=[0-20],V=['Vx'])
        if(z2==0  ):
            
            
            Vector2_source.data = dict(xS=[],yS=[],xE=[],yE=[])
            Vector3_source.data = dict(xS=[],yS=[],xE=[],yE=[])
            V1_label_source.data=dict(x=[],y=[],V=[])
            V2_label_source.data=dict(x=[],y=[],V=[])
            Resultant_values_source.data = dict(x=[50,100,155], y=[160,160,160], names=['Error:', 'Parallel','basis']) 
        elif (z2==90):
           
            Vector2_source.data = dict(xS=[],yS=[],xE=[],yE=[])
            Vector3_source.data = dict(xS=[],yS=[],xE=[],yE=[])
            V1_label_source.data=dict(x=[],y=[],V=[])
            V2_label_source.data=dict(x=[],y=[],V=[])
            Resultant_values_source.data = dict(x=[50,100,170], y=[160,160,160], names=['Error:', 'Orthogonal','basis'])
            
        else:
            
            Resultant_values_source.data = dict(x=[100,140,100,140,155,100,140,100,140], y=[160,160, 140, 140,140,120,120,100,100], names=['|V| = ', round(sqrt(xE**2.0+yE**2.0),1), '\\theta = ', round(atan(yE/xE)/pi*180,0), '^{\\circ}','Vx=',round(xE,1),'Vy=',round(yE,1)])
        
        
        glob_active.data = dict(Active=[True])
        show_button.label = 'Hide components' 
        
def reset():
     glob_theta1.data = dict(val=[radians(45)])
     glob_Vector1.data = dict(val=([70]))
     Vector_source.data = dict(xS=[0], xE=[50], yS=[0],yE=[50])
     [Active] = glob_active.data["Active"]
     
     if Active == False:
        pass
     else:
        
        glob_active.data = dict(Active=[False])
     
     show_button.label = 'Show components'
     AngleVector1Slider.value=45
     Vector1Slider.value=70
     V1_label_source.data=dict(x=[],y=[],V=[])
     V2_label_source.data=dict(x=[],y=[],V=[])
     Resultant_values_source.data = dict(x=[], y=[], names=[])
     Vector2_source.data = dict(xS=[],yS=[],xE=[],yE=[])
     Vector3_source.data = dict(xS=[],yS=[],xE=[],yE=[])
        
 

Vector1_glyph = Arrow(end=NormalHead(line_color="#A2AD00",fill_color="#A2AD00", line_width=2,size=15),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=Vector_source,line_color="#A2AD00",line_width=7)
Vector2_glyph = Arrow(end=NormalHead(line_color="#0065BD", fill_color="#0065BD", line_width=2,size=15),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=Vector2_source,line_color="#0065BD",line_width=7)
VectorResultant_glyph = Arrow(end=NormalHead(line_color="#E37222",fill_color="#E37222", line_width=2,size=15),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=Vector3_source,line_color="#E37222",line_width=7)       


V_label_glyph=LatexLabelSet(x='x', y='y',text='V1',text_font_size="15pt",level='overlay',source=V_label_source)
V1_label_glyph=LatexLabelSet(x='x', y='y',text='V',text_font_size="15pt",level='overlay',source=V1_label_source)    
V2_label_glyph=LatexLabelSet(x='x', y='y',text='V',text_font_size="15pt",level='overlay',source=V2_label_source)    
p = figure(tools="", x_range=(-200,200), y_range=(-200,250),plot_width=800, plot_height=625)
Resultant_values_glyph = LatexLabelSet(x='x',y='y',text='names',text_font_size="15pt", text_color="#E37222", level='glyph',source=Resultant_values_source)

#p.ray(x=[0],y=[0],length=300, angle=0,line_width=10 )
p.ray(x=[-200],y=[0],length=400, angle=0,line_width=3)
p.ray(x=[0],y=[-200],length=400, angle=1.57079632679,line_width=3 )
#p.ray(x=[0],y=[0],length=-300, angle=1.57079632679,line_width=10)

p.title.text_font_size="20pt"
#p.line(x='x',y='y',line_dash='dashed',source= V2parallel_line_source, color="black")
#p.line(x='x',y='y',line_dash='dashed',source= V1parallel_line_source, color="black")
p.add_layout(Vector1_glyph)
p.add_layout(Vector2_glyph)
p.add_layout(VectorResultant_glyph)   
p.add_layout(V_label_glyph)
p.add_layout(V1_label_glyph)
p.add_layout(V2_label_glyph)
p.add_layout(Resultant_values_glyph)
p.toolbar.logo = None

def changetheta1(attr,old,new):
    glob_theta1.data = dict(val=[radians(new)]) #      /output
    createtwoarrows()
    Vector2_source.data = dict(xS=[],yS=[],xE=[],yE=[])
    Vector3_source.data = dict(xS=[],yS=[],xE=[],yE=[])
    V1_label_source.data=dict(x=[],y=[],V=[])
    V2_label_source.data=dict(x=[],y=[],V=[])
    Resultant_values_source.data = dict(x=[], y=[], names=[])
    show_button.label = 'Show components'
    [Active] = glob_active.data["Active"]
     
    if Active == False:
        pass
    else:
        
        
        glob_active.data = dict(Active=[False])
    
    
def changevectorvalue(attr,old,new):
    glob_Vector1.data = dict(val=([new]))
    createtwoarrows()
    Vector2_source.data = dict(xS=[],yS=[],xE=[],yE=[])
    Vector3_source.data = dict(xS=[],yS=[],xE=[],yE=[])
    V1_label_source.data=dict(x=[],y=[],V=[])
    Resultant_values_source.data = dict(x=[], y=[], names=[])
    V2_label_source.data=dict(x=[],y=[],V=[])
    show_button.label = 'Show components'
    [Active] = glob_active.data["Active"]
     
    if Active == False:
        pass
    else:
        
        
        glob_active.data = dict(Active=[False])
    
    
    

AngleVector1Slider= LatexSlider(title='\\theta=', value_unit='^{\\circ}', value=45.0, start=0.0, end=360.0, step=5)
AngleVector1Slider.on_change('value',changetheta1)     

Vector1Slider = LatexSlider(title="|V|=",value=70,start=0,end=195,step=5)
Vector1Slider.on_change('value',changevectorvalue)

show_button = Button(label="Show components", button_type="success")
show_button.on_click(createarrows)

how_button = Button(label="Reset", button_type="success")
how_button.on_click(reset)

        
description_filename = join(dirname(__file__), "description.html")

description = Div(text=open(description_filename).read(), render_as_text=False, width=1200)

## Send to window
curdoc().add_root(column(description,column(row(p,column(AngleVector1Slider,Vector1Slider,show_button,how_button)))))
      
curdoc().title = "Vector Decomposition"        
        
    

        
    


    