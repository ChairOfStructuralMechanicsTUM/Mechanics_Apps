"""
Python Bokeh program which interactively change two vectos and display its sum

done by :Rishith Ellath Meethal
"""


from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.models import ColumnDataSource, Slider, LabelSet, Arrow, OpenHead, Button, Line,Div
from bokeh.io import curdoc
from numpy import loadtxt
from os.path import dirname, join, split
from math import radians, cos, sin, tan



#Initialise Variables
theta1 = radians(30)
theta2 = radians(60)
Vector1=50
Vector2=50
Vector1_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[],yE=[]))
Vector2_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[],yE=[]))
VectorResultant_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[],yE=[]))
V1parallel_line_source = ColumnDataSource(data=dict(x=[],y=[]))
V2parallel_line_source = ColumnDataSource(data=dict(x=[],y=[]))
V1_label_source = ColumnDataSource(data=dict(x=[],y=[],V1=[]))
V2_label_source = ColumnDataSource(data=dict(x=[],y=[],V2=[]))
Resultant_label_source = ColumnDataSource(data=dict(x=[],y=[],R=[]))

#responsible for the display of initial conditions 
def init ():
    updateVector1()
    updateVector2()
    updateResultant()
    
# update Vectors
def updateVector1 ():
    global theta1,Vector1
 
    if (Vector1== 0):
        Vector1_source.data = dict(xS=[],yS=[],xE=[],yE=[])
    
    else:
    # else the arrow is proportional to the Vector1
        xE=Vector1*cos(theta1)
        yE=Vector1*sin(theta1)
        Vector1_source.data = dict(xS=[0], yS=[0], xE=[xE], yE=[yE])
        V1_label_source.data = dict (x=[xE+3],y=[yE+3],V1=['V1'])

def updateVector2 ():
    global Vector2, theta2
    # if Vector2 = 0 then there is no arrow
    if (Vector2== 0):
        Vector2_source.data = dict(xS=[],yS=[],xE=[],yE=[])
    else:
        # else the arrow is proportional to the Vector1
        xE=Vector2*cos(theta2)
        yE=Vector2*sin(theta2)
        Vector2_source.data = dict(xS=[0], yS=[0], xE=[xE], yE=[yE])
        V2_label_source.data = dict (x=[xE+3],y=[yE+3],V2=['V2'])

def updateResultant():
    global vector1,vector2,theta1,theta2
    
    xE=Vector1*cos(theta1)+Vector2*cos(theta2)
    yE=Vector1*sin(theta1)+Vector2*sin(theta2)
    if (xE==0 and yE==0):
        VectorResultant_source.data = dict(xS=[], yS=[], xE=[], yE=[])
    else:
        VectorResultant_source.data = dict(xS=[0], yS=[0], xE=[xE], yE=[yE])
        Resultant_label_source.data = dict (x=[xE+3],y=[yE+3],R=['R'])
        
    #fors showing the resultant paralleogram
    V1parallel_line_source.data = dict(x=[Vector2*cos(theta2),xE], y=[Vector2*sin(theta2),yE])
    V2parallel_line_source.data = dict(x=[Vector1*cos(theta1),xE], y=[Vector1*sin(theta1),yE])
    
    
        
# adding the vectors to the plot
Vector1_glyph = Arrow(end=OpenHead(line_color="black",line_width=10,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=Vector1_source,line_color="black",line_width=7)
Vector2_glyph = Arrow(end=OpenHead(line_color="blue",line_width=10,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=Vector2_source,line_color="blue",line_width=7)
VectorResultant_glyph = Arrow(end=OpenHead(line_color="red",line_width=10,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=VectorResultant_source,line_color="red",line_width=7)
V1_label_glyph=LabelSet(x='x', y='y',text='V1',text_font_size="15pt",level='glyph',source=V1_label_source)
V2_label_glyph=LabelSet(x='x', y='y',text='V2',text_font_size="15pt",level='glyph',source=V2_label_source)
Resultant_label_glyph = LabelSet(x='x',y='y',text='R',text_font_size="15pt",level='glyph',source=Resultant_label_source)

p = figure(tools="", x_range=(-200,200), y_range=(-200,200),plot_width=750, plot_height=625)
p.title.text_font_size="20pt"
p.line(x='x',y='y',line_dash='dashed',source= V2parallel_line_source, color="black")
p.line(x='x',y='y',line_dash='dashed',source= V1parallel_line_source, color="black")
p.add_layout(Vector1_glyph)
p.add_layout(Vector2_glyph)
p.add_layout(VectorResultant_glyph)
p.add_layout(V1_label_glyph)
p.add_layout(V2_label_glyph)
p.add_layout(Resultant_label_glyph)
#p.axis.visible = False
#p.grid.visible = False
#p.background_fill_color = "#D1F4FF"

init()

#Changing Vector1
def changeVector1(attr,old,new):
    global Vector1, Active, Vector1Slider
  
    Vector1=new
    updateVector1()
    updateResultant()

#Changing Vector2
def changeVector2(attr,old,new):
    global Vector2, Active, Vector2Slider
  
    Vector2=new
    updateVector2()
    updateResultant()

#changing thea1
def changetheta1(attr,old,new):
    global Vector1, Active, AngleVector1Slider,theta1
  
    theta1=radians(new)
    updateVector1()
    updateResultant()
 
#changing thea2
def changetheta2(attr,old,new):
    global Vector2, Active, AngleVector2Slider,theta2
  
    theta2=radians(new)
    updateVector2()
    updateResultant()
    
    
## Create slider to choose force applied

Vector1Slider = Slider(title="Vector 1",value=50,start=0,end=100,step=5)
Vector1Slider.on_change('value',changeVector1)
Vector2Slider= Slider(title="Vector 2", value=50.0, start=0.0, end=100.0, step=5)
Vector2Slider.on_change('value',changeVector2)


AngleVector1Slider= Slider(title="Angle of Vector 1", value=30.0, start=0.0, end=360.0, step=5)
AngleVector1Slider.on_change('value',changetheta1)
AngleVector2Slider= Slider(title="Angle of Vector 2", value=60.0, start=0.0, end=360.0, step=5)
AngleVector2Slider.on_change('value',changetheta2)

# add app description
description_filename = join(dirname(__file__), "description.html")

description = Div(text=open(description_filename).read(), render_as_text=False, width=1200)

## Send to window
curdoc().add_root(column(description,column(row(p,column(Vector1Slider,Vector2Slider,AngleVector1Slider,AngleVector2Slider)))))
curdoc().title = "Vector Addition"
