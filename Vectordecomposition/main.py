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

Vector_source         = ColumnDataSource(data=dict(xS=[0], xE=[50], yS=[0],yE=[50]))
glob_Vector1           = ColumnDataSource(data=dict(val=[70]))
Vector2_source         = ColumnDataSource(data=dict(xS=[], xE=[], yS=[],yE=[]))
Line_source         = ColumnDataSource(data=dict(x=[0,0],y=[-1000,1000]))
Line2_source         = ColumnDataSource(data=dict(x=[-1000,1000],y=[0,0]))
Line_source1         = ColumnDataSource(data=dict(x=[15,50],y=[25,50]))


V1parallel_line_source = ColumnDataSource(data=dict(x=[],y=[]))
V2parallel_line_source = ColumnDataSource(data=dict(x=[],y=[]))










Vector3_source         = ColumnDataSource(data=dict(xS=[], xE=[], yS=[],yE=[]))

glob_theta1            = ColumnDataSource(data=dict(val=[radians(45)]))
glob_theta1line1       = ColumnDataSource(data=dict(val=[radians(90)]))
glob_theta1line2       = ColumnDataSource(data=dict(val=[radians(0)]))
glob_active   = ColumnDataSource(data=dict(Active=[False]))
V_label_source        = ColumnDataSource(data=dict(x=[50+3],y=[50-3],V1=['F']))
V1_label_source        = ColumnDataSource(data=dict(x=[],y=[],V=[]))
V2_label_source        = ColumnDataSource(data=dict(x=[],y=[],V=[]))
LO1_label_source        = ColumnDataSource(data=dict(x=[0],y=[200],V=["\\text {Direction 1}"]))
LO2_label_source        = ColumnDataSource(data=dict(x=[200],y=[0],V=["\\text {Direction 2}"]))

Resultant_values_source = ColumnDataSource(data=dict(x=[],y=[],names=[]))
def init ():
    createtwoarrows()
    changevectorvalue()
    changeline()
    changeline2()

def changeline():
     [theta11 ] = glob_theta1line1.data["val"]
     
     
     x1=1000*cos(theta11)
     y1=1000*sin(theta11)
     Line_source.data = dict(x=[-x1,x1],y=[-y1,y1])

     LO1_label_source.data=dict(x=[x1/5],y=[y1/5],V=["\\text {Direction 1}"])
     
     
     

def changeline2():
     [theta111 ] = glob_theta1line2.data["val"]

     
     x1=1000*cos(theta111)
     y1=1000*sin(theta111)
     Line2_source.data = dict(x=[-x1,x1],y=[-y1,y1])
     

     LO2_label_source.data=dict(x=[x1/5],y=[y1/5],V=["\\text {Direction 2}"])
     
     
     
     
     
     
  
     
def createtwocomponnets():
    

     [Active] = glob_active.data["Active"]
     [Vector1] = glob_Vector1.data["val"]
     [theta1 ] = glob_theta1.data["val"]
     [theta11 ] = glob_theta1line1.data["val"] #perpendicular line theta 2
     [theta111 ] = glob_theta1line2.data["val"] #horizantal line theta 1

     z2=round(theta111/pi*180,0)
     z21=round(theta11/pi*180,0)

     #Clculate Horizantla component of main vector
     if (Active==True):

         V1parallel_line_source.data = dict(x=[],y=[])
         V2parallel_line_source.data=dict(x=[],y=[])
         Vector2_source.data = dict(xS=[],yS=[],xE=[],yE=[])
         Vector3_source.data = dict(xS=[],yS=[],xE=[],yE=[])
         glob_active.data   = dict(Active=[False])
         show_button.label = 'Show components'
         value_plot.text=""
         V1_label_source.data=dict(x=[],y=[],V=[])
         V2_label_source.data=dict(x=[],y=[],V=[])
         
     else:
         
       if (z2==z21 or (abs(z2-z21)==180) or (abs(z2-z21)==360) ):
            

            value_plot.text = "Error decomposing. Chose different angles."
            V1parallel_line_source.data = dict(x=[],y=[])
            V2parallel_line_source.data=dict(x=[],y=[])
            Vector2_source.data = dict(xS=[],yS=[],xE=[],yE=[])
            Vector3_source.data = dict(xS=[],yS=[],xE=[],yE=[])
            V1_label_source.data=dict(x=[],y=[],V=[])
            V2_label_source.data=dict(x=[],y=[],V=[])
            glob_active.data = dict(Active=[True])
            show_button.label = 'Hide components'
            
       else:
#             print (4)
             Rx=Vector1*cos(theta1)
             Ry=Vector1*sin(theta1)

     #Form two equations
             a1=cos(theta111)
             b1=sin(theta11)
             a2=sin(theta111)
             b2=cos(theta11)
             c1= (b2/a1)*a2
             F1=(b1-c1)
             Rx1=(Rx/a1)*a2
             Forcecomponent2=(Ry-Rx1)/F1
             Forcecomponent1=(Rx-(Forcecomponent2*b2))/a1
             F22=round(Forcecomponent2,1)
             
             
             F11=round(Forcecomponent1,1)
            
             xE1=Forcecomponent1*(a1)
             yE1=Forcecomponent1*(a2)
             xE2=Forcecomponent2*(b2)
             yE2=Forcecomponent2*(b1)
             
             
             if (F22==0 ):
                  Vector3_source.data = dict(xS=[],yS=[],xE=[],yE=[])
                  value_plot.text = "$$\\begin{aligned} F_1&=" + str(F22) + "\\,\\mathrm{N}\\\\ F_2&=" + str(F11) + "\\,\\mathrm{N} \\end{aligned}$$"
                  Vector2_source.data = dict(xS=[0],yS=[0],xE=[xE1],yE=[yE1])
                  V2_label_source.data=dict(x=[],y=[],V=[])
                  V1_label_source.data=dict(x=[xE1+5],y=[yE1],V=['F2'])
                  glob_active.data = dict(Active=[True])
                  show_button.label = 'Hide components' 
                  V1parallel_line_source.data = dict(x=[],y=[])
                  V2parallel_line_source.data=dict(x=[],y=[])
                  
                  
             elif (F11==0 ):
                  value_plot.text = "$$\\begin{aligned} F_1&=" + str(F22) + "\\,\\mathrm{N}\\\\ F_2&=" + str(F11) + "\\,\\mathrm{N} \\end{aligned}$$"
                  Vector2_source.data = dict(xS=[],yS=[],xE=[],yE=[])
                  Vector3_source.data = dict(xS=[0],yS=[0],xE=[xE2],yE=[yE2])
                  V2_label_source.data=dict(x=[xE2+5],y=[yE2],V=['F1'])
                  
                  V1_label_source.data=dict(x=[],y=[],V=[])
                  glob_active.data = dict(Active=[True])
                  show_button.label = 'Hide components' 
                  V1parallel_line_source.data = dict(x=[],y=[])
                  V2parallel_line_source.data=dict(x=[],y=[])
             else:
                 value_plot.text = "$$\\begin{aligned} F_1&=" + str(F22) + "\\,\\mathrm{N}\\\\ F_2&=" + str(F11) + "\\,\\mathrm{N} \\end{aligned}$$"
                 Vector2_source.data = dict(xS=[0],yS=[0],xE=[xE1],yE=[yE1])
         
                 Vector3_source.data = dict(xS=[0],yS=[0],xE=[xE2],yE=[yE2])
                 
                 V1parallel_line_source.data = dict(x=[xE2,Rx],y=[yE2,Ry])
                 V2parallel_line_source.data=dict(x=[xE1,Rx],y=[yE1,Ry])
                 
                 V1_label_source.data=dict(x=[xE1+5],y=[yE1],V=['F2'])
                 V2_label_source.data=dict(x=[xE2+5],y=[yE2],V=['F1'])
 

                 glob_active.data = dict(Active=[True])
                 show_button.label = 'Hide components' 
     
     
     
    
def createtwoarrows():
    [Vector1] = glob_Vector1.data["val"]
    [theta1 ] = glob_theta1.data["val"]

    xE=Vector1*cos(theta1)
    yE=Vector1*sin(theta1)

    Vector_source.data = dict(xS=[0],yS=[0],xE=[xE],yE=[yE])
    V_label_source.data= dict (x=[xE+3],y=[yE-3],V1=['F',])


        
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
     value_plot.text=""
     Vector1Slider.value=70
     LineVector1Slider.value=90
     LineVector2Slider.value=0
     V1parallel_line_source.data = dict(x=[],y=[])
     V2parallel_line_source.data=dict(x=[],y=[])
     
     V1_label_source.data=dict(x=[],y=[],V=[])
     V2_label_source.data=dict(x=[],y=[],V=[])
     Resultant_values_source.data = dict(x=[], y=[], names=[])
     Vector2_source.data = dict(xS=[],yS=[],xE=[],yE=[])
     Vector3_source.data = dict(xS=[],yS=[],xE=[],yE=[])
     Line_source.data        =(dict(x=[0,0],y=[-1000,1000]))
     Line2_source.data         =(dict(x=[-1000,1000],y=[0,0]))
     Line_source1.data        = dict(x=[15,50],y=[25,50])
     

     LO1_label_source.data  =dict(x=[0],y=[200],V=["\\text {Direction 1}"])
    
     LO2_label_source.data   = dict(x=[200],y=[0],V=["\\text {Direction 2}"])
    
     
     
     

 

Vector1_glyph = Arrow(end=NormalHead(line_color="#A2AD00",fill_color="#A2AD00", line_width=2,size=15),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=Vector_source,line_color="#A2AD00",line_width=7)
Vector2_glyph = Arrow(end=NormalHead(line_color="#0065BD", fill_color="#0065BD", line_width=2,size=15),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=Vector2_source,line_color="#0065BD",line_width=7)
VectorResultant_glyph = Arrow(end=NormalHead(line_color="#E37222",fill_color="#E37222", line_width=2,size=15),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=Vector3_source,line_color="#E37222",line_width=7)       


V_label_glyph=LatexLabelSet(x='x', y='y',text='V1',text_font_size="15pt",level='overlay',source=V_label_source)
V1_label_glyph=LatexLabelSet(x='x', y='y',text='V',text_font_size="15pt",level='overlay',source=V1_label_source)    
V2_label_glyph=LatexLabelSet(x='x', y='y',text='V',text_font_size="15pt",level='overlay',source=V2_label_source) 
LO1_label_glyph=LatexLabelSet(x='x', y='y',text='V',text_font_size="10pt",level='overlay',source=LO1_label_source)    
LO2_label_glyph=LatexLabelSet(x='x', y='y',text='V',text_font_size="10pt",level='overlay',source=LO2_label_source) 
   
p = figure(tools="", x_range=(-200,200), y_range=(-200,200),plot_width=800, plot_height=625)
Resultant_values_glyph = LatexLabelSet(x='x',y='y',text='names',text_font_size="15pt", text_color="#E37222", level='glyph',source=Resultant_values_source)

p.line(x='x',y='y',line_dash='dashed',source= V2parallel_line_source, color="black")
p.line(x='x',y='y',line_dash='dashed',source= V1parallel_line_source, color="black")                                      
            
              
              
              
              


p.title.text_font_size="20pt"

p.add_layout(Vector1_glyph)
p.add_layout(LO1_label_glyph)
p.add_layout(LO2_label_glyph)
p.add_layout(Vector2_glyph)
p.add_layout(VectorResultant_glyph)   
p.add_layout(V_label_glyph)
p.add_layout(V1_label_glyph)
p.add_layout(V2_label_glyph)
p.add_layout(Resultant_values_glyph)
value_plot = LatexDiv(text="", render_as_text=False, width=300)

my_line=p.line(x='x', y='y',line_dash='dashed',source=Line_source, color='#0065BD',line_width=3)  
my_line=p.line(x='x', y='y',line_dash='dashed',source=Line2_source, color='#0065BD',line_width=3)               



p.toolbar.logo = None


    
def changetheta1line1(attr,old,new):
    glob_theta1line1.data=dict(val=[radians(new)])
    [Active] = glob_active.data["Active"]
    
   
    
    changeline()
    
    if show_button.label == "Hide components":
     
        glob_active.data = dict(Active=[False])
        createtwocomponnets()
        
   
    
    
def changetheta1line2(attr,old,new):
    glob_theta1line2.data=dict(val=[radians(new)])


    changeline2()

    if show_button.label == "Hide components":
       
        glob_active.data = dict(Active=[False])
        createtwocomponnets()
        

    
    
    
    
    
    
    

def changetheta1(attr,old,new):
    glob_theta1.data = dict(val=[radians(new)]) #      /output
    createtwoarrows()

    if show_button.label == "Hide components":

        glob_active.data = dict(Active=[False])
        createtwocomponnets()

    
    
    

    
def changevectorvalue(attr,old,new):
    glob_Vector1.data = dict(val=([new]))
    createtwoarrows()

    if show_button.label == "Hide components":


        glob_active.data = dict(Active=[False])
        createtwocomponnets()

    
    

  
    

AngleVector1Slider= LatexSlider(title='\\theta=', value_unit='^{\\circ}', value=45.0, start=0.0, end=360.0, step=5)
AngleVector1Slider.on_change('value',changetheta1)
LineVector1Slider= LatexSlider(title="\\text {Direction 1}", value_unit='^{\\circ}', value=90.0, start=0.0, end=360.0, step=5)
LineVector1Slider.on_change('value',changetheta1line1)
LineVector2Slider= LatexSlider(title="\\text {Direction 2}", value_unit='^{\\circ}', value=0.0, start=0.0, end=360.0, step=5)
LineVector2Slider.on_change('value',changetheta1line2)     

Vector1Slider = LatexSlider(title="|F|=",value=70,start=0,end=100,step=5)
Vector1Slider.on_change('value',changevectorvalue)

show_button = Button(label="Show components", button_type="success")
show_button.on_click(createtwocomponnets)

how_button = Button(label="Reset", button_type="success")
how_button.on_click(reset)

        
description_filename = join(dirname(__file__), "description.html")

description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)

## Send to window
curdoc().add_root(column(description,column(row(p,(Spacer(width=40)),column(LineVector1Slider,LineVector2Slider,AngleVector1Slider,Vector1Slider,show_button,how_button,value_plot)))))
      
curdoc().title = "Vector Decomposition"        
        
    

        
    


    