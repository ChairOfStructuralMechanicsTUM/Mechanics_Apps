"""
Python Bokeh program calculate the complex number

"""
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.models import ColumnDataSource, Arrow, Button, Div, NormalHead,LabelSet,Span
from bokeh.io import curdoc
from math import radians, cos, sin, sqrt, atan, pi
from bokeh.models.widgets import DataTable, TableColumn,CheckboxGroup
import yaml 
from os.path import dirname, join, abspath # no split required, managed in strings.json
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir  = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexLabelSet, LatexSlider, LatexLabel,LatexDiv


# Initialise Variables
glob_theta1                                 = ColumnDataSource(data=dict(val=[radians(50)]))
glob_theta2                                 = ColumnDataSource(data=dict(val=[radians(140)]))
glob_Vector1                                = ColumnDataSource(data=dict(val=[45]))
glob_Vector2                                = ColumnDataSource(data=dict(val=[20]))
Vector1_source                              = ColumnDataSource(data=dict(xS=[], xE=[], yS=[],yE=[]))
Vector2_source                              = ColumnDataSource(data=dict(xS=[], xE=[], yS=[],yE=[]))
VectorSum_source                            = ColumnDataSource(data=dict(xS=[], xE=[], yS=[],yE=[]))
VectorSub_source                            = ColumnDataSource(data=dict(xS=[], xE=[], yS=[],yE=[]))
VectorMul_source                            = ColumnDataSource(data=dict(xS=[], xE=[], yS=[],yE=[]))
VectorDiv_source                            = ColumnDataSource(data=dict(xS=[], xE=[], yS=[],yE=[]))  
V1_label_source                             = ColumnDataSource(data=dict(x=[],y=[],Z1=[]))
V2_label_source                             = ColumnDataSource(data=dict(x=[],y=[],Z2=[]))
VectorSub_label_source                      = ColumnDataSource(data=dict(x=[],y=[],R=[]))
VectorDiv_label_source                      = ColumnDataSource(data=dict(x=[],y=[],R=[]))
VectorSum_label_source                      = ColumnDataSource(data=dict(x=[],y=[],R=[]))
VectorMul_label_source                      = ColumnDataSource(data=dict(x=[],y=[],R=[]))
VectorSum_values_source                     = ColumnDataSource(data=dict(x=[],y=[],names=[]))
VectorSub_values_source                     = ColumnDataSource(data=dict(x=[],y=[],names=[]))     
line1_source                                = ColumnDataSource(data=dict(x=[],y=[]))
line2_source                                = ColumnDataSource(data=dict(x=[],y=[]))

ValueZ1_Z2                                  = ColumnDataSource(data=dict(names1=['Z₁'],names2=['Z₂'],valuesZ1=[],valuesZ2=[]))
ValueZ3_Z6                                  = ColumnDataSource(data=dict(names1=['Z₃'],names2=['Z₄'],names3=['Z₅'],names4=['Z₆'],valuesZ3=[],valuesZ4=[],valuesZ5=[],valuesZ6=[]))
[theta1]  = glob_theta1.data["val"]
[Vector1] = glob_Vector1.data["val"]
[theta2]  = glob_theta2.data["val"]
[Vector2] = glob_Vector2.data["val"]

xE1 = Vector1*cos(theta1)
yE1 = Vector1*sin(theta1)
xE2 = Vector2*cos(theta2)
yE2 = Vector2*sin(theta2)
xE3 = Vector1*cos(theta1)+Vector2*cos(theta2)
yE3 = Vector1*sin(theta1)+Vector2*sin(theta2)
xE4 = Vector1*cos(theta1)-Vector2*cos(theta2)
yE4 = Vector1*sin(theta1)-Vector2*sin(theta2)
xE5 = xE1*xE2-yE1*yE2
yE5 = xE1*yE2+xE2*yE1
denominator=xE2*xE2+yE2*yE2
xE6 = (xE1*xE2+yE1*yE2)/denominator
yE6 = (xE1*yE2-xE2*yE1)/denominator
xL3 = xE3-3
yL3 = yE3-6
xL4 = xE4-3
yL4 = yE4-6


Vector1_source.stream(dict(xS=[0], yS=[0], xE=[xE1], yE=[yE1]), rollover=1)
V1_label_source.data = dict (x=[xE1+2],y=[yE1-2],Z1=["Z₁"])
Vector2_source.stream(dict(xS=[0], yS=[0], xE=[xE2], yE=[yE2]), rollover=1)
V2_label_source.data = dict (x=[xE2+3],y=[yE2-3],Z2=["Z₂"])
VectorSum_source.stream(dict(xS=[0], yS=[0], xE=[xE3], yE=[yE3]), rollover=1)
VectorSum_label_source.data=dict (x=[xE3],y=[xE3],R=["Z₃"])
VectorSub_source.stream(dict(xS=[0], yS=[0], xE=[xE4], yE=[yE4]), rollover=1)
VectorSub_label_source.data = dict (x=[xE4],y=[yE4],R=["Z₄"])  
VectorMul_source.stream(dict(xS=[0], yS=[0], xE=[xE5], yE=[yE5]), rollover=1)
VectorDiv_source.stream(dict(xS=[0], yS=[0], xE=[xE6], yE=[yE6]), rollover=1)
VectorMul_label_source.data = dict (x=[xE5],y=[yE5-1],R=["Z₅"])
VectorDiv_label_source.data = dict (x=[xE6],y=[yE6],R=["Z₆"])

line1_source.data = dict (x=[xE1, xE3],y=[yE1, yE3])
line2_source.data = dict (x=[xE1, xE4],y=[yE1, yE4])

xE1=round(xE1,1)
xE2=round(xE2,1)
yE1=round(yE1,1)
yE2=round(yE2,1)
xE3=round(xE3,1)
xE4=round(xE4,1)
yE3=round(yE3,1)
yE4=round(yE4,1)
xE5=round(xE5,1)
xE6=round(xE6,1)
yE5=round(yE5,1)
yE6=round(yE6,1)
valuesZ1='{x}+{y}i'.format(x=xE1,y=yE1)
valuesZ2='{x}+{y}i'.format(x=xE2,y=yE2)
valuesZ3='{x}+{y}i'.format(x=xE3,y=yE3)
valuesZ4='{x}+{y}i'.format(x=xE4,y=yE4)
valuesZ5='{x}+{y}i'.format(x=xE5,y=yE5)
valuesZ6='{x}+{y}i'.format(x=xE6,y=yE6)
ValueZ1_Z2.data= dict(names=['Z₁','Z₂'],valuesZ=[valuesZ1,valuesZ2])
ValueZ3_Z6.data= dict(names=['Z₃','Z₄','Z₅','Z₆'],valuesZ=[valuesZ3,valuesZ4,valuesZ5,valuesZ6])



def updateVector1 ():
    [theta1]  = glob_theta1.data["val"]  # input/
    [Vector1] = glob_Vector1.data["val"] # input/
    
    if (Vector1== 0):
       Vector1_source.stream(dict(xS=[],yS=[],xE=[],yE=[]),rollover=-1)
       V1_label_source.data = dict (x=[],y=[],Z1=[])
    else:
        xE = Vector1*cos(theta1)
        yE = Vector1*sin(theta1)
        Vector1_source.stream(dict(xS=[0], yS=[0], xE=[xE], yE=[yE]), rollover=1)
        V1_label_source.data = dict (x=[xE+3],y=[yE-3],Z1=["Z₁"])
    
    

def updateVector2 ():
    [theta2]  = glob_theta2.data["val"]  # input/
    [Vector2] = glob_Vector2.data["val"] # input/
    if (Vector2== 0):
        Vector2_source.stream(dict(xS=[],yS=[],xE=[],yE=[]), rollover=1)
        V2_label_source.data = dict (x=[],y=[],Z2=[])
    else:
        xE = Vector2*cos(theta2)
        yE = Vector2*sin(theta2)
        Vector2_source.stream(dict(xS=[0], yS=[0], xE=[xE], yE=[yE]), rollover=1)
        V2_label_source.data = dict (x=[xE+3],y=[yE-3],Z2=["Z₂"])

def updatevalues1():
    [theta1]  = glob_theta1.data["val"]  # input/
    [theta2]  = glob_theta2.data["val"]  # input/
    [Vector1] = glob_Vector1.data["val"] # input/
    [Vector2] = glob_Vector2.data["val"]
    xE1 = Vector1*cos(theta1)
    yE1 = Vector1*sin(theta1)    
    xE2 = Vector2*cos(theta2)
    yE2 = Vector2*sin(theta2)
    xE1=round(xE1,1)
    xE2=round(xE2,1)
    yE1=round(yE1,1)
    yE2=round(yE2,1)
    valuesZ1='{x}+{y}i'.format(x=xE1,y=yE1)
    valuesZ2='{x}+{y}i'.format(x=xE2,y=yE2)
    ValueZ1_Z2.data= dict(names=['Z₁','Z₂'],valuesZ=[valuesZ1,valuesZ2])

def updatevalues2():
    [theta1]  = glob_theta1.data["val"]  # input/
    [theta2]  = glob_theta2.data["val"]  # input/
    [Vector1] = glob_Vector1.data["val"] # input/
    [Vector2] = glob_Vector2.data["val"]
    xE1 = Vector1*cos(theta1)
    yE1 = Vector1*sin(theta1)
    xE2 = Vector2*cos(theta2)
    yE2 = Vector2*sin(theta2)
    xE3 = Vector1*cos(theta1)+Vector2*cos(theta2)
    yE3 = Vector1*sin(theta1)+Vector2*sin(theta2)
    xE4 = Vector1*cos(theta1)-Vector2*cos(theta2)
    yE4 = Vector1*sin(theta1)-Vector2*sin(theta2)  
    xE5 = xE1*xE2-yE1*yE2
    yE5 = xE1*yE2+xE2*yE1
    denominator=xE2*xE2+yE2*yE2
    xE6 = (xE1*xE2+yE1*yE2)/denominator
    yE6 = (xE1*yE2-xE2*yE1)/denominator
    xE3=round(xE3,1)
    xE4=round(xE4,1)
    yE3=round(yE3,1)
    yE4=round(yE4,1)
    xE5=round(xE5,1)
    xE6=round(xE6,1)
    yE5=round(yE5,1)
    yE6=round(yE6,1)
    
    valuesZ3='{x}+{y}i'.format(x=xE3,y=yE3)
    valuesZ4='{x}+{y}i'.format(x=xE4,y=yE4)
    valuesZ5='{x}+{y}i'.format(x=xE5,y=yE5)
    valuesZ6='{x}+{y}i'.format(x=xE6,y=yE6)   
    ValueZ3_Z6.data= dict(names=['Z₃','Z₄','Z₅','Z₆'],valuesZ=[valuesZ3,valuesZ4,valuesZ5,valuesZ6])

def updateSum():
    [theta1]  = glob_theta1.data["val"]  # input/
    [theta2]  = glob_theta2.data["val"]  # input/
    [Vector1] = glob_Vector1.data["val"] # input/
    [Vector2] = glob_Vector2.data["val"] # input/
    
    xE = Vector1*cos(theta1)+Vector2*cos(theta2)
    yE = Vector1*sin(theta1)+Vector2*sin(theta2)
    
    R  = round(sqrt(xE**2.0+yE**2.0),1)
    if (abs(R) < 1e-3):
        VectorSum_source.stream(dict(xS=[0], yS=[0], xE=[xE], yE=[yE]), rollover=1)
        VectorSum_label_source.data = dict(x=[], y=[], R=[])
    else:
        VectorSum_source.stream(dict(xS=[0], yS=[0], xE=[xE], yE=[yE]), rollover=1)
        # Readjust positions
        xL3 = xE-3
        yL3 = yE-6
        VectorSum_label_source.data=dict (x=[(xL3/(sqrt(xL3**2+yL3**2)))*(sqrt(xL3**2+yL3**2)+10)],y=[(yL3/(sqrt(xL3**2+yL3**2)))*(sqrt(xL3**2+yL3**2)+10)],R=["Z₃"])

def updateMul():
    [theta1]  = glob_theta1.data["val"]  # input/
    [theta2]  = glob_theta2.data["val"]  # input/
    [Vector1] = glob_Vector1.data["val"] # input/
    [Vector2] = glob_Vector2.data["val"] # input/
    
    xE1 = Vector1*cos(theta1)
    yE1 = Vector1*sin(theta1)
    xE2 = Vector2*cos(theta2)
    yE2 = Vector2*sin(theta2)
    xE5 = xE1*xE2-yE1*yE2
    yE5 = xE1*yE2+xE2*yE1
    R  = round(sqrt(xE5**2.0+yE5**2.0),1)
    if (abs(R) < 1e-3):
        VectorMul_source.stream(dict(xS=[0], yS=[0], xE=[xE5], yE=[yE5]), rollover=1)
        VectorMul_label_source.data = dict(x=[], y=[], R=[])
    else:
        VectorMul_source.stream(dict(xS=[0], yS=[0], xE=[xE5], yE=[yE5]), rollover=1)
        # Readjust positions
        xL5 = xE5-3
        yL5 = yE5-6
        VectorMul_label_source.data=dict (x=[(xL5/(sqrt(xL5**2+yL5**2)))*(sqrt(xL5**2+yL5**2)+10)],y=[(yL5/(sqrt(xL5**2+yL5**2)))*(sqrt(xL5**2+yL5**2)+10)],R=["Z₅"])

def updateDiv():
    [theta1]  = glob_theta1.data["val"]  # input/
    [theta2]  = glob_theta2.data["val"]  # input/
    [Vector1] = glob_Vector1.data["val"] # input/
    [Vector2] = glob_Vector2.data["val"] # input/
    
    xE1 = Vector1*cos(theta1)
    yE1 = Vector1*sin(theta1)
    xE2 = Vector2*cos(theta2)
    yE2 = Vector2*sin(theta2)
    denominator=xE2*xE2+yE2*yE2
    xE6 = (xE1*xE2+yE1*yE2)/denominator
    yE6 = (xE1*yE2-xE2*yE1)/denominator
    R  = round(sqrt(xE6**2.0+yE6**2.0),1)
    if (abs(R) < 1e-3):
        VectorDiv_source.stream(dict(xS=[0], yS=[0], xE=[xE6], yE=[yE6]), rollover=1)
        VectorDiv_label_source.data = dict(x=[], y=[], R=[])
    else:
        VectorDiv_source.stream(dict(xS=[0], yS=[0], xE=[xE6], yE=[yE6]), rollover=1)
        # Readjust positions
        xL6 = xE6-3
        yL6 = yE6-6
        VectorDiv_label_source.data=dict (x=[(xL6/(sqrt(xL6**2+yL6**2)))*(sqrt(xL6**2+yL6**2)+10)],y=[(yL6/(sqrt(xL6**2+yL6**2)))*(sqrt(xL6**2+yL6**2)+10)],R=["Z₆"])

def updateSub():
    [theta1]  = glob_theta1.data["val"]  # input/
    [theta2]  = glob_theta2.data["val"]  # input/
    [Vector1] = glob_Vector1.data["val"] # input/
    [Vector2] = glob_Vector2.data["val"] # input/
    
    xE = Vector1*cos(theta1)-Vector2*cos(theta2)
    yE = Vector1*sin(theta1)-Vector2*sin(theta2)

    R  = round(sqrt(xE**2.0+yE**2.0),1)
    if (abs(R) < 1e-3):
        VectorSub_source.stream(dict(xS=[0], yS=[0], xE=[xE], yE=[yE]), rollover=1)
        VectorSub_label_source.data = dict(x=[], y=[], R=[])

    else:
        VectorSub_source.stream(dict(xS=[0], yS=[0], xE=[xE], yE=[yE]), rollover=1)
        # Readjust positions
        xL3 = xE-3
        yL3 = yE-6
        VectorSub_label_source.data = dict (x=[(xL3/(sqrt(xL3**2+yL3**2)))*(sqrt(xL3**2+yL3**2)+10)],y=[(yL3/(sqrt(xL3**2+yL3**2)))*(sqrt(xL3**2+yL3**2)+10)],R=["Z₄"])  

def updateLine():
    [theta1]  = glob_theta1.data["val"]  # input/
    [theta2]  = glob_theta2.data["val"]  # input/
    [Vector1] = glob_Vector1.data["val"] # input/
    [Vector2] = glob_Vector2.data["val"]   
    x1 = Vector1*cos(theta1)
    y1 = Vector1*sin(theta1)
    xS = Vector1*cos(theta1)+Vector2*cos(theta2)
    yS = Vector1*sin(theta1)+Vector2*sin(theta2)
    xE = Vector1*cos(theta1)-Vector2*cos(theta2)
    yE = Vector1*sin(theta1)-Vector2*sin(theta2)

    line1_source.data = dict (x=[x1, xS],y=[y1, yS])
    line2_source.data = dict (x=[x1, xE],y=[y1, yE])

Conjugate_button = Button(label="Z₂ = complex conjugate of Z₁", button_type="success",width=100)

def conjugate():
    [theta1]  = glob_theta1.data["val"]  # input/
    [Vector1] = glob_Vector1.data["val"] # input
    xE1 = Vector1*cos(theta1)
    yE1 = Vector1*sin(theta1)
    #global glob_Vector2,glob_Vector2
    glob_theta2.data["val"]=[2*pi-theta1]
    glob_Vector2.data["val"]=[Vector1]
    xE2 = xE1
    yE2 = -yE1
    xE3=xE2+xE1
    yE3=yE2+yE1
    xE4=xE1-xE2
    yE4=yE1-yE2
    xE5 = xE1*xE2-yE1*yE2
    yE5 = xE1*yE2+xE2*yE1
    denominator=xE2*xE2+yE2*yE2
    xE6 = (xE1*xE2+yE1*yE2)/denominator
    yE6 = (xE1*yE2-xE2*yE1)/denominator
    Vector2_source.stream(dict(xS=[0], yS=[0], xE=[xE2], yE=[yE2]), rollover=1)
    V2_label_source.data = dict (x=[xE2+3],y=[yE2-3],Z2=["Z₂"])
    VectorSum_source.stream(dict(xS=[0], yS=[0], xE=[xE3], yE=[yE3]), rollover=1)
    VectorSum_label_source.data=dict (x=[xE3],y=[yE3],R=["Z₃"])
    VectorSub_source.stream(dict(xS=[0], yS=[0], xE=[xE4], yE=[yE4]), rollover=1)
    VectorSub_label_source.data=dict (x=[xE4],y=[yE4],R=["Z₄"])
    VectorMul_source.stream(dict(xS=[0], yS=[0], xE=[xE5], yE=[yE5]), rollover=1)
    VectorMul_label_source.data=dict (x=[xE5],y=[yE5],R=["Z₅"])
    VectorDiv_source.stream(dict(xS=[0], yS=[0], xE=[xE6], yE=[yE6]), rollover=1)
    VectorDiv_label_source.data=dict (x=[xE6],y=[yE6],R=["Z₆"])
    xE1=round(xE1,1)
    xE2=round(xE2,1)
    yE1=round(yE1,1)
    yE2=round(yE2,1)
    valuesZ1='{x}+{y}i'.format(x=xE1,y=yE1)
    valuesZ2='{x}+{y}i'.format(x=xE2,y=yE2)
    ValueZ1_Z2.data= dict(names=['Z₁','Z₂'],valuesZ=[valuesZ1,valuesZ2])
    xE3=round(xE3,1)
    xE4=round(xE4,1)
    yE3=round(yE3,1)
    yE4=round(yE4,1)
    xE5=round(xE5,1)
    xE6=round(xE6,1)
    yE5=round(yE5,1)
    yE6=round(yE6,1)
    valuesZ3='{x}+{y}i'.format(x=xE3,y=yE3)
    valuesZ4='{x}+{y}i'.format(x=xE4,y=yE4)
    valuesZ5='{x}+{y}i'.format(x=xE5,y=yE5)
    valuesZ6='{x}+{y}i'.format(x=xE6,y=yE6)   
    ValueZ3_Z6.data= dict(names=['Z₃','Z₄','Z₅','Z₆'],valuesZ=[valuesZ3,valuesZ4,valuesZ5,valuesZ6])
    line1_source.data = dict (x=[xE1, xE3],y=[yE1, yE3])
    line2_source.data = dict (x=[xE1, xE4],y=[yE1, yE4])
    updatevalues1()
    updatevalues2()
Conjugate_button.on_click(conjugate)

#table    
columns1 = [
    TableColumn(field="names", title="Complex Number"),
    TableColumn(field="valuesZ", title="Value"),
]
valueZ1Z2_table = DataTable(source=ValueZ1_Z2, columns=columns1, reorderable=False, sortable=False, selectable=False, index_position=None, width=400, height=150)

columns2 = [
    TableColumn(field="names", title="Complex Number"),
    TableColumn(field="valuesZ", title="Value"),
]
valueZ3Z4_table = DataTable(source=ValueZ3_Z6, columns=columns2, reorderable=False, sortable=False, selectable=False, index_position=None, width=400, height=150)

description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)
    
    # adding the vectors to the plot
Vector1_glyph = Arrow(end=NormalHead(line_color="#A2AD00",fill_color="#A2AD00", line_width=2,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=Vector1_source,line_color="#A2AD00",line_width=3)
Vector2_glyph = Arrow(end=NormalHead(line_color="#E37222", fill_color="#E37222", line_width=2,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=Vector2_source,line_color="#E37222",line_width=3)
VectorSum_glyph = Arrow(end=NormalHead(line_color="#0065BD",fill_color="#0065BD", line_width=2,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=VectorSum_source,line_color="#0065BD",line_width=3)
VectorSub_glyph = Arrow(end=NormalHead(line_color="#005293",fill_color="#005293", line_width=2,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=VectorSub_source,line_color="#005293",line_width=3)
VectorMul_glyph = Arrow(end=NormalHead(line_color="#64A0C8",fill_color="#64A0C8", line_width=2,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=VectorMul_source,line_color="#64A0C8",line_width=3)
VectorDiv_glyph = Arrow(end=NormalHead(line_color="#98C6EA",fill_color="#98C6EA", line_width=2,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=VectorDiv_source,line_color="#98C6EA",line_width=3)

V1_label_glyph         = LabelSet(x='x', y='y',text='Z1',text_font_size="15pt",level='overlay',source=V1_label_source)
V2_label_glyph         = LabelSet(x='x', y='y',text='Z2',text_font_size="15pt",level='overlay',source=V2_label_source)
V5_label_glyph         = LabelSet(x='x', y='y',text='R',text_font_size="15pt",level='overlay',source=VectorMul_label_source)
V6_label_glyph         = LabelSet(x='x', y='y',text='R',text_font_size="15pt",level='overlay',source=VectorDiv_label_source)
VectorSum_label_glyph  = LabelSet(x='x',y='y',text='R',text_font_size="15pt",level='overlay',source=VectorSum_label_source)
VectorSum_values_glyph = LabelSet(x='x',y='y',text='names',text_font_size="15pt", text_color="#E37222", level='glyph',source=VectorSum_values_source)   

VectorSub_label_glyph  = LabelSet(x='x',y='y',text='R',text_font_size="15pt",level='overlay',source=VectorSub_label_source)
VectorSub_values_glyph = LabelSet(x='x',y='y',text='names',text_font_size="15pt", text_color="#E37222", level='glyph',source=VectorSub_values_source)

vline = Span(location=0, dimension='height', line_color='#333333',line_dash='dashed')
hline = Span(location=0, dimension='width', line_color='#333333',line_dash='dashed')

p = figure( x_range=(-100,100), y_range=(-100,100),plot_width=500, plot_height=500,\
    toolbar_location="right", tools=["wheel_zoom,xwheel_pan,pan,reset"],x_axis_label="Realpart")
line1_glyph=p.line(x='x',y='y',line_dash='dashed',source= line1_source, color="black")
line2_glyph=p.line(x='x',y='y',line_dash='dashed',source= line2_source, color="black")
p.title.text_font_size="20pt"
p.axis.major_label_text_font_size="10pt"
p.axis.axis_label_text_font_style="normal"
p.axis.axis_label_text_font_size="20pt"
#p.xaxis.axis_label="xxxxxx"
p.yaxis.axis_label=" Imagirary Part"
#p.axis.fixed_location=0
p.add_layout(Vector1_glyph)
p.add_layout(Vector2_glyph)
p.add_layout(VectorSum_glyph)
p.add_layout(VectorSub_glyph)

p.add_layout(V1_label_glyph)
p.add_layout(V2_label_glyph)

p.add_layout(V5_label_glyph)
p.add_layout(V6_label_glyph)
p.add_layout(VectorSum_label_glyph)
p.add_layout(VectorSum_values_glyph)
p.add_layout(VectorMul_glyph)
p.add_layout(VectorDiv_glyph)
p.add_layout(VectorSub_label_glyph)
p.add_layout(VectorSub_values_glyph)

p.add_layout(vline)
p.add_layout(hline)



calculate_selection = CheckboxGroup(labels=["Addition Z₃", "Subtraction Z₄","Multiplication Z₅","Division Z₆"], active = [0,1,2,3])
print(calculate_selection.labels)
print(calculate_selection.active)


def choose_calculate(attr, old, new):
    VectorSum_glyph.visible        = 0 in calculate_selection.active   
    VectorSub_glyph.visible        = 1 in calculate_selection.active 
    VectorSum_label_glyph.visible  = 0 in calculate_selection.active
    VectorSub_label_glyph.visible  = 1 in calculate_selection.active
    line1_glyph.visible            = 0 in calculate_selection.active 
    line2_glyph.visible            = 1 in calculate_selection.active 
    VectorMul_glyph.visible        = 2 in calculate_selection.active
    VectorDiv_glyph.visible        = 3 in calculate_selection.active
    V5_label_glyph.visible         = 2 in calculate_selection.active
    V6_label_glyph.visible         = 3 in calculate_selection.active

calculate_selection.on_change('active',choose_calculate)

def changeVector1(attr,old,new):
    glob_Vector1.data = dict(val=[new]) #      /output
    updateVector1()
    updateSum()
    updateSub()
    updateLine()
    updatevalues1()  
    updatevalues2() 
    updateMul()
    updateDiv()
 
#Changing Vector2
def changeVector2(attr,old,new):
    glob_Vector2.data = dict(val=[new]) #      /output
    updateVector2()
    updateSum()
    updateSub()
    updateLine()
    updatevalues1()
    updatevalues2()
    updateMul()
    updateDiv()
   
#changing theta1
def changetheta1(attr,old,new):
    glob_theta1.data = dict(val=[radians(new)]) #      /output
    updateVector1()
    updateSub()
    updateSum()
    updateLine()
    updatevalues1()
    updatevalues2()
    updateMul()
    updateDiv()
  
#changing theta2
def changetheta2(attr,old,new):
    glob_theta2.data = dict(val=[radians(new)]) #      /output
    updateVector2()
    updateSub()
    updateSum()
    updateLine()
    updatevalues1()
    updatevalues2()
    updateMul()
    updateDiv()
    

Vector1Slider = LatexSlider(title="|Z1|=", value=45.0,  start=0, end=100, step=2)

Vector1Slider.on_change('value',changeVector1)
Vector2Slider = LatexSlider(title="|Z2|=", value=20.0,  start=0.0, end=100.0, step=2)

Vector2Slider.on_change('value',changeVector2)

AngleVector1Slider = LatexSlider(title='\\alpha_{Z1}=', value_unit='^{\\circ}', value=60.0, start=0.0, end=360.0, step=5)
AngleVector1Slider.on_change('value',changetheta1)
AngleVector2Slider = LatexSlider(title='\\alpha_{Z2}=',value_unit='^{\\circ}', value=140.0, start=0.0, end=360.0, step=5)
AngleVector2Slider.on_change('value',changetheta2)


curdoc().add_root(column(Spacer(height=50),description,column(row(Spacer(width=100),column(p,Spacer(height=50),row(column(Spacer(height=30),calculate_selection),valueZ3Z4_table)),column(Vector1Slider,Vector2Slider,AngleVector1Slider,AngleVector2Slider,valueZ1Z2_table,Conjugate_button)))))
