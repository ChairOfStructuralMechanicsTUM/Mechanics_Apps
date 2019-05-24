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
Line_source         = ColumnDataSource(data=dict(x=[0,0],y=[-200,200]))
Line2_source         = ColumnDataSource(data=dict(x=[-200,200],y=[0,0]))
Line_source1         = ColumnDataSource(data=dict(x=[15,50],y=[25,50]))

ray_source1=  ColumnDataSource(data=dict(x=[0], y=[200], L=[10],Angle=[225]))
ray_source2=  ColumnDataSource(data=dict(x=[0], y=[(200/6)], L=[10],Angle=[225]))
ray_source3=  ColumnDataSource(data=dict(x=[0], y=[(2*200)/6], L=[10],Angle=[225]))
ray_source4=  ColumnDataSource(data=dict(x=[0], y=[(3*200)/6], L=[10],Angle=[225]))
ray_source5=  ColumnDataSource(data=dict(x=[0], y=[(4*200/6)], L=[10],Angle=[225]))
ray_source6=  ColumnDataSource(data=dict(x=[0], y=[(5*200)/6], L=[10],Angle=[225]))


ray_source7=  ColumnDataSource(data=dict(x=[0], y=[-200], L=[10],Angle=[225]))
ray_source8=  ColumnDataSource(data=dict(x=[0], y=[(-200/6)], L=[10],Angle=[225]))
ray_source9=  ColumnDataSource(data=dict(x=[0], y=[(2*-200)/6], L=[10],Angle=[225]))
ray_source10=  ColumnDataSource(data=dict(x=[0], y=[(3*-200)/6], L=[10],Angle=[225]))
ray_source11=  ColumnDataSource(data=dict(x=[0], y=[(4*-200/6)], L=[10],Angle=[225]))
ray_source12=  ColumnDataSource(data=dict(x=[0], y=[(5*-200)/6], L=[10],Angle=[225]))

V1parallel_line_source = ColumnDataSource(data=dict(x=[],y=[]))
V2parallel_line_source = ColumnDataSource(data=dict(x=[],y=[]))




ray2_source1=  ColumnDataSource(data=dict(x=[200], y=[0], L=[10],Angle=[225]))
ray2_source2=  ColumnDataSource(data=dict(x=[(200/6)], y=[0], L=[10],Angle=[225]))
ray2_source3=  ColumnDataSource(data=dict(x=[(2*200)/6], y=[0], L=[10],Angle=[225]))
ray2_source4=  ColumnDataSource(data=dict(x=[(3*200)/6], y=[0], L=[10],Angle=[225]))
ray2_source5=  ColumnDataSource(data=dict(x=[(4*200)/6], y=[0], L=[10],Angle=[225]))
ray2_source6=  ColumnDataSource(data=dict(x=[(5*200)/6], y=[0], L=[10],Angle=[225]))


ray2_source7=  ColumnDataSource(data=dict(x=[-200], y=[0], L=[10],Angle=[225]))
ray2_source8=  ColumnDataSource(data=dict(x=[(-200/6)], y=[0], L=[10],Angle=[225]))
ray2_source9=  ColumnDataSource(data=dict(x=[(2*-200)/6], y=[0], L=[10],Angle=[225]))
ray2_source10=  ColumnDataSource(data=dict(x=[(3*-200)/6], y=[0], L=[10],Angle=[225]))
ray2_source11=  ColumnDataSource(data=dict(x=[(4*-200)/6], y=[0], L=[10],Angle=[225]))
ray2_source12=  ColumnDataSource(data=dict(x=[(5*-200)/6], y=[0], L=[10],Angle=[225]))






Vector3_source         = ColumnDataSource(data=dict(xS=[], xE=[], yS=[],yE=[]))

glob_theta1            = ColumnDataSource(data=dict(val=[radians(45)]))
glob_theta1line1       = ColumnDataSource(data=dict(val=[radians(90)]))
glob_theta1line2       = ColumnDataSource(data=dict(val=[radians(0)]))
glob_active   = ColumnDataSource(data=dict(Active=[False]))
V_label_source        = ColumnDataSource(data=dict(x=[50+3],y=[50-3],V1=['V']))
V1_label_source        = ColumnDataSource(data=dict(x=[],y=[],V=[]))
V2_label_source        = ColumnDataSource(data=dict(x=[],y=[],V=[]))
LO1_label_source        = ColumnDataSource(data=dict(x=[0],y=[200],V=['LO1']))
LO2_label_source        = ColumnDataSource(data=dict(x=[200],y=[0],V=['LO2']))

Resultant_values_source = ColumnDataSource(data=dict(x=[],y=[],names=[]))
def init ():
    createtwoarrows()
    changevectorvalue()
    changeline()
    changeline2()

def changeline():
     [theta11 ] = glob_theta1line1.data["val"]
     [theeta111]=[theta11*(180/pi)]
     [b]=[45-theeta111]
     
     x1=200*cos(theta11)
     y1=200*sin(theta11)
     Line_source.data = dict(x=[-x1,x1],y=[-y1,y1])
     ray_source1.data=dict(x=[x1],y=[y1],L=[10],Angle=[180-b])
     ray_source2.data=  dict(x=[(x1/6)], y=[(y1/6)], L=[10],Angle=[180-b])
     ray_source3.data=  dict(x=[(2*x1/6)], y=[(2*y1/6)], L=[10],Angle=[180-b])
     ray_source4.data=  dict(x=[(3*x1/6)], y=[(3*y1/6)], L=[10],Angle=[180-b])
     ray_source5.data=  dict(x=[(4*x1/6)], y=[(4*y1/6)], L=[10],Angle=[180-b])
     ray_source6.data=  dict(x=[(5*x1/6)], y=[(5*y1/6)], L=[10],Angle=[180-b])
     ray_source7.data=dict(x=[-x1],y=[-y1],L=[10],Angle=[180-b])
     ray_source8.data=  dict(x=[(-x1/6)], y=[(-y1/6)], L=[10],Angle=[180-b])
     ray_source9.data=  dict(x=[((2*-x1)/6)], y=[(2*-y1)/6], L=[10],Angle=[180-b])
     ray_source10.data=  dict(x=[(3*-x1)/6], y=[(3*-y1)/6], L=[10],Angle=[180-b])
     ray_source11.data=  dict(x=[(4*-x1)/6], y=[(4*-y1)/6], L=[10],Angle=[180-b])
     ray_source12.data=  dict(x=[(5*-x1)/6], y=[(5*-y1)/6], L=[10],Angle=[180-b])
     LO1_label_source.data=dict(x=[x1],y=[y1],V=['LO1'])
     
     
     
#     print (ray_source1.data)
def changeline2():
     [theta111 ] = glob_theta1line2.data["val"]
     [theeta1111]=[theta111*(180/pi)]
     [b]=[45-theeta1111]
     
     x1=200*cos(theta111)
     y1=200*sin(theta111)
     Line2_source.data = dict(x=[-x1,x1],y=[-y1,y1])
     
     ray2_source1.data=dict(x=[x1],y=[y1],L=[10],Angle=[270-(b)])
     ray2_source2.data=  dict(x=[(x1/6)], y=[(y1/6)], L=[10],Angle=[(270-(b))])
     ray2_source3.data=  dict(x=[(2*x1/6)], y=[(2*y1/6)], L=[10],Angle=[(270-(b))])
     ray2_source4.data=  dict(x=[(3*x1/6)], y=[(3*y1/6)], L=[10],Angle=[(270-(b))])
     ray2_source5.data=  dict(x=[(4*x1/6)], y=[(4*y1/6)], L=[10],Angle=[(270-(b))])
     ray2_source6.data=  dict(x=[(5*x1/6)], y=[(5*y1/6)], L=[10],Angle=[(270-(b))])
     
     ray2_source7.data=dict(x=[-x1],y=[-y1],L=[10],Angle=[270-(b)])
     ray2_source8.data=  dict(x=[(-x1/6)], y=[(-y1/6)], L=[10],Angle=[(270-(b))])
     ray2_source9.data=  dict(x=[(2*-x1)/6], y=[(2*-y1)/6], L=[10],Angle=[(270-(b))])
     ray2_source10.data=  dict(x=[(3*-x1)/6], y=[(3*-y1)/6], L=[10],Angle=[(270-(b))])
     ray2_source11.data=  dict(x=[(4*-x1)/6], y=[(4*-y1)/6], L=[10],Angle=[(270-(b))])
     ray2_source12.data=  dict(x=[(5*-x1)/6], y=[(5*-y1)/6], L=[10],Angle=[(270-(b))])
     LO2_label_source.data=dict(x=[x1],y=[y1],V=['LO2'])
     
     
     
     
     
     
#     Line_source1.data = dict(x=[((x1/2)-10),x1],y=[y1/2,y1])    
     
def createtwocomponnets():
    
    
     [Active] = glob_active.data["Active"]
     [Vector1] = glob_Vector1.data["val"]
     [theta1 ] = glob_theta1.data["val"]
     [theta11 ] = glob_theta1line1.data["val"] #perpendicular line theta 2
     [theta111 ] = glob_theta1line2.data["val"] #horizantal line theta 1
#     print Vector1
#     print theta1
#     print theta11
#     print theta111
     z2=round(theta111/pi*180,0)
     z21=round(theta11/pi*180,0)
#     print z2,z21
     #Clculate Horizantla component of main vector
     if ( Active):
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
         
       if (z2==z21):
#            Resultant_values_source.data = dict(x=[50,100,155], y=[160,160,160], names=['Error:', 'Decomposing']) 
            value_plot.text = "Error decomposing. Chose different angles."
            V1parallel_line_source.data = dict(x=[],y=[])
            V2parallel_line_source.data=dict(x=[],y=[])
       else:
             
             Rx=Vector1*cos(theta1)
             Ry=Vector1*sin(theta1)
#             print (Rx)
#             print (Ry)
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
#             print (Forcecomponent2)
#             print (Forcecomponent1)
             xE1=Forcecomponent1*(a1)
             yE1=Forcecomponent1*(a2)
             xE2=Forcecomponent2*(b2)
             yE2=Forcecomponent2*(b1)
     
             Vector2_source.data = dict(xS=[0],yS=[0],xE=[xE1],yE=[yE1])
     
             Vector3_source.data = dict(xS=[0],yS=[0],xE=[xE2],yE=[yE2])
             V1parallel_line_source.data = dict(x=[xE2,Rx],y=[yE2,Ry])
             V2parallel_line_source.data=dict(x=[xE1,Rx],y=[yE1,Ry])
             V1_label_source.data=dict(x=[xE1+5],y=[yE1],V=['F2'])
             V2_label_source.data=dict(x=[xE2+5],y=[yE2],V=['F1'])
#             Resultant_values_source.data = dict(x=[100,140,100,140,155,100,140,100,140], y=[160,160, 140, 140,140,120,120,100,100], names=['|V| = ', round(sqrt(Ry**2.0+Rx**2.0),1), '\\theta = ', round(atan(Ry/Rx)/pi*180,0), '^{\\circ}','F1=',round(Forcecomponent1,1),'F2=',round(Forcecomponent2,1)])
             value_plot.text = "$$\\begin{aligned} F_1&=" + str(round(Forcecomponent1,1)) + "\\,\\mathrm{N}\\\\ F_2&=" + str(round(Forcecomponent2,1)) + "\\,\\mathrm{N} \\end{aligned}$$"
         
             glob_active.data = dict(Active=[True])
             show_button.label = 'Hide components' 
     
     
     
    
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

#def createarrows():
#    [Vector1] = glob_Vector1.data["val"]
#    [theta1 ] = glob_theta1.data["val"]
#    [Active] = glob_active.data["Active"]
#    if ( Active):
#         Vector2_source.data = dict(xS=[],yS=[],xE=[],yE=[])
#         Vector3_source.data = dict(xS=[],yS=[],xE=[],yE=[])
#         V1_label_source.data=dict(x=[],y=[],V=[])
#         V2_label_source.data=dict(x=[],y=[],V=[])
#         Resultant_values_source.data = dict(x=[], y=[], names=[])
#         
#         glob_active.data   = dict(Active=[False])
#         show_button.label = 'Show components'
#    else:
#        xE=Vector1*cos(theta1)
#        yE=Vector1*sin(theta1)
#        z=yE/2
#        z1=xE/2
#        z2=round(atan(yE/xE)/pi*180,0)
#        
#
#        Vector2_source.data = dict(xS=[0],yS=[0],xE=[xE],yE=[0])
#        Vector3_source.data = dict(xS=[0],yS=[0],xE=[0],yE=[yE])
#        V1_label_source.data=dict(x=[0-20],y=[z],V=['Vy'])
#        V2_label_source.data=dict(x=[z1],y=[0-20],V=['Vx'])
#        
##        if(z2==0  ):
##            
##            
##            Vector2_source.data = dict(xS=[],yS=[],xE=[],yE=[])
##            Vector3_source.data = dict(xS=[],yS=[],xE=[],yE=[])
##            V1_label_source.data=dict(x=[],y=[],V=[])
##            V2_label_source.data=dict(x=[],y=[],V=[])
##            Resultant_values_source.data = dict(x=[50,100,155], y=[160,160,160], names=['Error:', 'Parallel','basis']) 
##        elif (z2==90):
##           
##            Vector2_source.data = dict(xS=[],yS=[],xE=[],yE=[])
##            Vector3_source.data = dict(xS=[],yS=[],xE=[],yE=[])
##            V1_label_source.data=dict(x=[],y=[],V=[])
##            V2_label_source.data=dict(x=[],y=[],V=[])
##            Resultant_values_source.data = dict(x=[50,100,170], y=[160,160,160], names=['Error:', 'Orthogonal','basis'])
##            
##        else:
#            
#        Resultant_values_source.data = dict(x=[100,140,100,140,155,100,140,100,140], y=[160,160, 140, 140,140,120,120,100,100], names=['|V| = ', round(sqrt(xE**2.0+yE**2.0),1), '\\theta = ', round(atan(yE/xE)/pi*180,0), '^{\\circ}','Vx=',round(xE,1),'Vy=',round(yE,1)])
#        
#        
#        glob_active.data = dict(Active=[True])
#        show_button.label = 'Hide components' 
        
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
     Line_source.data        =(dict(x=[0,0],y=[-200,200]))
     Line2_source.data         =(dict(x=[-200,200],y=[0,0]))
     Line_source1.data        = dict(x=[15,50],y=[25,50])
     
     ray_source1.data=  (dict(x=[0], y=[200], L=[10],Angle=[225]))
     ray_source2.data=  (dict(x=[0], y=[(200/6)], L=[10],Angle=[225]))
     ray_source3.data=  (dict(x=[0], y=[(2*200)/6], L=[10],Angle=[225]))
     ray_source4.data=  (dict(x=[0], y=[(3*200)/6], L=[10],Angle=[225]))
     ray_source5.data=  (dict(x=[0], y=[(4*200/6)], L=[10],Angle=[225]))
     ray_source6.data=  (dict(x=[0], y=[(5*200)/6], L=[10],Angle=[225]))
     ray_source7.data= dict(x=[0], y=[-200], L=[10],Angle=[225])
     ray_source8.data=  dict(x=[0], y=[(-200/6)], L=[10],Angle=[225])
     ray_source9.data= dict(x=[0], y=[(2*-200)/6], L=[10],Angle=[225])
     ray_source10.data=  dict(x=[0], y=[(3*-200)/6], L=[10],Angle=[225])
     ray_source11.data=  dict(x=[0], y=[(4*-200/6)], L=[10],Angle=[225])
     ray_source12.data=  dict(x=[0], y=[(5*-200)/6], L=[10],Angle=[225])


     ray2_source1.data=  (dict(x=[200], y=[0], L=[10],Angle=[225]))
     ray2_source2.data=  (dict(x=[(200/6)], y=[0], L=[10],Angle=[225]))
     ray2_source3.data=  (dict(x=[(2*200)/6], y=[0], L=[10],Angle=[225]))
     ray2_source4.data=  (dict(x=[(3*200)/6], y=[0], L=[10],Angle=[225]))
     ray2_source5.data=  (dict(x=[(4*200/6)], y=[0], L=[10],Angle=[225]))
     ray2_source6.data=  (dict(x=[(5*200)/6], y=[0], L=[10],Angle=[225]))
     ray2_source7.data=  dict(x=[-200], y=[0], L=[10],Angle=[225])
     ray2_source8.data= dict(x=[(-200/6)], y=[0], L=[10],Angle=[225])
     ray2_source9.data=  dict(x=[(2*-200)/6], y=[0], L=[10],Angle=[225])
     ray2_source10.data=  dict(x=[(3*-200)/6], y=[0], L=[10],Angle=[225])
     ray2_source11.data=  dict(x=[(4*-200/6)], y=[0], L=[10],Angle=[225])
     ray2_source12.data=  dict(x=[(5*-200)/6], y=[0], L=[10],Angle=[225])
     LO1_label_source.data  =dict(x=[0],y=[200],V=['LO1'])
    
     LO2_label_source.data   = dict(x=[200],y=[0],V=['LO2'])
    
     
     
     
#     Vector2_source.data = dict(xS=[],yS=[],xE=[],yE=[])
#     Vector3_source.data = dict(xS=[],yS=[],xE=[],yE=[])
 

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
            
              
              
              
              
#p.ray(x=[0],y=[0],length=300, angle=0,line_width=10 )

#p.ray(x=[-200],y=[0],length=400, angle=0,line_width=3)
#p.ray(x=[0],y=[-200],length=400, angle=1.57079632679,line_width=
#p.ray(x=[0], y=[0], length=[45], angle=[90],
#      angle_units="deg", color="#FB8072", line_width=2)
      
      

#line11=sqrt(line1)
#p.ray(x=[0],y=[0],length=-300, angle=1.57079632679,line_width=10)

p.title.text_font_size="20pt"
#p.line(x='x',y='y',line_dash='dashed',source= V2parallel_line_source, color="black")
#p.line(x='x',y='y',line_dash='dashed',source= V1parallel_line_source, color="black")
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

my_line=p.line(x='x', y='y',source=Line_source, color='#0065BD',line_width=3)  
my_line=p.line(x='x', y='y',source=Line2_source, color='#0065BD',line_width=3)               
#my_line=p.line(x='x', y='y',source=Line_source1, color='#0065BD',line_width=3)  
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray_source1, color='#0065BD',line_width=3) 
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray_source2, color='#0065BD',line_width=3)               
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray_source3, color='#0065BD',line_width=3)               
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray_source4, color='#0065BD',line_width=3)               
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray_source5, color='#0065BD',line_width=3)              
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray_source6, color='#0065BD',line_width=3) 
              

my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray_source7, color='#0065BD',line_width=3) 
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray_source8, color='#0065BD',line_width=3)               
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray_source9, color='#0065BD',line_width=3)               
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray_source10, color='#0065BD',line_width=3)               
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray_source11, color='#0065BD',line_width=3)              
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray_source12, color='#0065BD',line_width=3) 
              
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray2_source1, color='#0065BD',line_width=3) 
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray2_source2, color='#0065BD',line_width=3)               
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray2_source3, color='#0065BD',line_width=3)               
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray2_source4, color='#0065BD',line_width=3)               
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray2_source5, color='#0065BD',line_width=3)              
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray2_source6, color='#0065BD',line_width=3)
              
              
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray2_source7, color='#0065BD',line_width=3) 
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray2_source8, color='#0065BD',line_width=3)               
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray2_source9, color='#0065BD',line_width=3)               
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray2_source10, color='#0065BD',line_width=3)               
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray2_source11, color='#0065BD',line_width=3)              
my_line=p.ray(x="x", y="y",length="L",angle="Angle",angle_units="deg",source=ray2_source12, color='#0065BD',line_width=3)
              



p.toolbar.logo = None


    
def changetheta1line1(attr,old,new):
    glob_theta1line1.data=dict(val=[radians(new)])
    
    
    changeline()
#    createtwocomponnets()
    V1parallel_line_source.data = dict(x=[],y=[])
    V2parallel_line_source.data=dict(x=[],y=[])
    
    Vector2_source.data = dict(xS=[],yS=[],xE=[],yE=[])
    Vector3_source.data = dict(xS=[],yS=[],xE=[],yE=[])
    V1_label_source.data=dict(x=[],y=[],V=[])
    V2_label_source.data=dict(x=[],y=[],V=[])
    Resultant_values_source.data = dict(x=[], y=[], names=[])
    show_button.label = 'Show components'
    value_plot.text=""
    [Active] = glob_active.data["Active"]
#    changeline()
#    createtwocomponnets()
     
    if Active == False:
        pass
    else:
        
        
        glob_active.data = dict(Active=[False])
        
        
#    changeline()
#    createtwocomponnets()
    
    
def changetheta1line2(attr,old,new):
    glob_theta1line2.data=dict(val=[radians(new)])
    
    
    changeline2()
#    createtwocomponnets()
    V1parallel_line_source.data = dict(x=[],y=[])
    V2parallel_line_source.data=dict(x=[],y=[])
    Vector2_source.data = dict(xS=[],yS=[],xE=[],yE=[])
    Vector3_source.data = dict(xS=[],yS=[],xE=[],yE=[])
    V1_label_source.data=dict(x=[],y=[],V=[])
    V2_label_source.data=dict(x=[],y=[],V=[])
    Resultant_values_source.data = dict(x=[], y=[], names=[])
    show_button.label = 'Show components'
    value_plot.text=""
    [Active] = glob_active.data["Active"]
#    changeline()
#    createtwocomponnets()
     
    if Active == False:
        pass
    else:
        
        
        glob_active.data = dict(Active=[False])
    
    
    
    
#    x1=Vector1*cos(theta1)
#    y1=Vector1*sin(theta1)
#    p.ray(x=[0], y=[0], length=[45], angle=[glob_theta1line1],
#      angle_units="deg", color="#FB8072", line_width=2)

   
    
    
    
    
    
    
    

def changetheta1(attr,old,new):
    glob_theta1.data = dict(val=[radians(new)]) #      /output
    createtwoarrows()
#    createtwocomponnets()
    V1parallel_line_source.data = dict(x=[],y=[])
    V2parallel_line_source.data=dict(x=[],y=[])
    Vector2_source.data = dict(xS=[],yS=[],xE=[],yE=[])
    Vector3_source.data = dict(xS=[],yS=[],xE=[],yE=[])
    V1_label_source.data=dict(x=[],y=[],V=[])
    V2_label_source.data=dict(x=[],y=[],V=[])
    Resultant_values_source.data = dict(x=[], y=[], names=[])
    show_button.label = 'Show components'
    value_plot.text=""
    [Active] = glob_active.data["Active"]
     
    if Active == False:
        pass
    else:
        
        
        glob_active.data = dict(Active=[False])
    
    
def changevectorvalue(attr,old,new):
    glob_Vector1.data = dict(val=([new]))
    createtwoarrows()
#    createtwocomponnets()
    V1parallel_line_source.data = dict(x=[],y=[])
    V2parallel_line_source.data=dict(x=[],y=[])
    Vector2_source.data = dict(xS=[],yS=[],xE=[],yE=[])
    Vector3_source.data = dict(xS=[],yS=[],xE=[],yE=[])
    V1_label_source.data=dict(x=[],y=[],V=[])
    Resultant_values_source.data = dict(x=[], y=[], names=[])
    V2_label_source.data=dict(x=[],y=[],V=[])
    show_button.label = 'Show components'
    value_plot.text=""
    [Active] = glob_active.data["Active"]
     
    if Active == False:
        pass
    else:
        
        
        glob_active.data = dict(Active=[False])
    
    
    

AngleVector1Slider= LatexSlider(title='\\theta=', value_unit='^{\\circ}', value=45.0, start=0.0, end=360.0, step=5)
AngleVector1Slider.on_change('value',changetheta1)
LineVector1Slider= LatexSlider(title='LOA1', value_unit='^{\\circ}', value=90.0, start=0.0, end=360.0, step=5)
LineVector1Slider.on_change('value',changetheta1line1)
LineVector2Slider= LatexSlider(title='LOA2', value_unit='^{\\circ}', value=0.0, start=0.0, end=360.0, step=5)
LineVector2Slider.on_change('value',changetheta1line2)     

Vector1Slider = LatexSlider(title="|V|=",value=70,start=0,end=100,step=5)
Vector1Slider.on_change('value',changevectorvalue)

show_button = Button(label="Show components", button_type="success")
show_button.on_click(createtwocomponnets)

how_button = Button(label="Reset", button_type="success")
how_button.on_click(reset)

        
description_filename = join(dirname(__file__), "description.html")

description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)

## Send to window
curdoc().add_root(column(description,column(row(p,column(LineVector1Slider,LineVector2Slider,AngleVector1Slider,Vector1Slider,show_button,how_button,value_plot)))))
      
curdoc().title = "Vector Decomposition"        
        
    

        
    


    