"""
Python Bokeh program which interactively change two vectos and display its sum

"""


from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.models import ColumnDataSource, Slider, LabelSet, Arrow, OpenHead, Button, Line,Div, NormalHead
from bokeh.io import curdoc
from numpy import loadtxt
from os.path import dirname, join, split
from math import radians, cos, sin, tan, sqrt, atan, pi

from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexDiv, LatexLabel, LatexLabelSet, LatexSlider, LatexLegend


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
Resultant_values_source = ColumnDataSource(data=dict(x=[],y=[],names=[]))
global ShowVariable
ShowVariable = -1

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
        V1_label_source.data = dict (x=[xE+3],y=[yE-3],V1=["V"u"\u2081"])

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
        V2_label_source.data = dict (x=[xE-3],y=[yE+3],V2=["V"u"\u2082"])

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

    global ShowVariable    
    if (ShowVariable==1):
        xE=Vector1*cos(theta1)+Vector2*cos(theta2)
        yE=Vector1*sin(theta1)+Vector2*sin(theta2)
        if (xE>0 and yE>0):
            Resultant_values_source.data = dict(x=[100,140,100,140,155], y=[160,160, 140, 140,140], names=['|R| = ', round(sqrt(xE**2.0+yE**2.0),1), '\\alpha_{R} = ', round(atan(yE/xE)/pi*180,0), '^{\\circ}'])
        if (xE<0 and yE>0):
            if(round(atan(yE/xE)/pi*180,0)+180<100):
                Resultant_values_source.data = dict(x=[100,140,100,140,155], y=[160,160, 140, 140,140], names=['|R| = ', round(sqrt(xE**2.0+yE**2.0),1), '\\alpha_{R} = ', round(atan(yE/xE)/pi*180,0)+180, '^{\\circ}'])
            else:
                Resultant_values_source.data = dict(x=[100,140,100,140,163], y=[160,160, 140, 140,140], names=['|R| = ', round(sqrt(xE**2.0+yE**2.0),1), '\\alpha_{R} = ', round(atan(yE/xE)/pi*180,0)+180, '^{\\circ}'])
        if (xE<0 and yE<0):
            Resultant_values_source.data = dict(x=[100,140,100,140,163], y=[160,160, 140, 140,140], names=['|R| = ', round(sqrt(xE**2.0+yE**2.0),1), '\\alpha_{R} = ', round(atan(yE/xE)/pi*180,0)+180, '^{\\circ}'])
        if (xE>0 and yE<0 ):
            Resultant_values_source.data = dict(x=[100,140,100,140,163], y=[160,160, 140, 140,140], names=['|R| = ', round(sqrt(xE**2.0+yE**2.0),1), '\\alpha_{R} = ', round(atan(yE/xE)/pi*180,0)+360, '^{\\circ}'])                
    else:
        Resultant_values_source.data = dict(x=[], y=[], names=[])

def ChangeShow():
    global ShowVariable
    ShowVariable =ShowVariable*-1
    updateResultant()        

# adding the vectors to the plot
Vector1_glyph = Arrow(end=NormalHead(line_color="#A2AD00",fill_color="#A2AD00", line_width=2,size=15),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=Vector1_source,line_color="#A2AD00",line_width=7)
Vector2_glyph = Arrow(end=NormalHead(line_color="#0065BD", fill_color="#0065BD", line_width=2,size=15),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=Vector2_source,line_color="#0065BD",line_width=7)
VectorResultant_glyph = Arrow(end=NormalHead(line_color="#E37222",fill_color="#E37222", line_width=2,size=15),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=VectorResultant_source,line_color="#E37222",line_width=7)
V1_label_glyph=LabelSet(x='x', y='y',text='V1',text_font_size="15pt",level='glyph',source=V1_label_source)
V2_label_glyph=LabelSet(x='x', y='y',text='V2',text_font_size="15pt",level='glyph',source=V2_label_source)
Resultant_label_glyph = LabelSet(x='x',y='y',text='R',text_font_size="15pt",level='glyph',source=Resultant_label_source)
Resultant_values_glyph = LatexLabelSet(x='x',y='y',text='names',text_font_size="15pt", text_color="#E37222", level='glyph',source=Resultant_values_source)


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
p.add_layout(Resultant_values_glyph)
p.toolbar.logo = None

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

#changing theta1
def changetheta1(attr,old,new):
    global Vector1, Active, AngleVector1Slider,theta1
  
    theta1=radians(new)
    updateVector1()
    updateResultant()

#changing theta2
def changetheta2(attr,old,new):
    global Vector2, Active, AngleVector2Slider,theta2
  
    theta2=radians(new)
    updateVector2()
    updateResultant()
    
## Create slider to choose force applied
Vector1Slider = LatexSlider(title="|V1|=",value=50,start=0,end=100,step=5)
Vector1Slider.on_change('value',changeVector1)
Vector2Slider= LatexSlider(title="|V2|=", value=50.0, start=0.0, end=100.0, step=5)
Vector2Slider.on_change('value',changeVector2)

AngleVector1Slider= LatexSlider(title='\\alpha_{V1}=', value_unit='^{\\circ}', value=30.0, start=0.0, end=360.0, step=5)
AngleVector1Slider.on_change('value',changetheta1)
AngleVector2Slider= LatexSlider(title='\\alpha_{V2}=',value_unit='^{\\circ}', value=60.0, start=0.0, end=360.0, step=5)
AngleVector2Slider.on_change('value',changetheta2)

###Create Show Resultant Properties Button:
show_button = Button(label="Show/Hide Length and Direction of Resultant", button_type="success")
show_button.on_click(ChangeShow)


# add app description
description_filename = join(dirname(__file__), "description.html")

description = Div(text=open(description_filename).read(), render_as_text=False, width=1200)

## Send to window
curdoc().add_root(column(description,column(row(p,column(Vector1Slider,Vector2Slider,AngleVector1Slider,AngleVector2Slider,show_button)))))
curdoc().title = "Vector Addition"
