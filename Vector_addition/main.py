"""
Python Bokeh program which interactively changes two vectors and displays their sum

"""
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.models import ColumnDataSource, Arrow, Button, Div, NormalHead
from bokeh.io import curdoc
from math import radians, cos, sin, sqrt, atan, pi
import yaml 

from os.path import dirname, join, abspath # no split required, managed in strings.json
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir  = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexLabelSet, LatexSlider

std_lang = 'en'
strings  = yaml.safe_load(open('Vector_addition/static/strings.json'))
def changeLanguage():
    [lang] = flags.data["lang"]
    if lang == "en":
        setDocumentLanguage('de')
    elif lang == "de":
        setDocumentLanguage('en')

def setDocumentLanguage(lang):
    flags.patch( {'lang':[(0,lang)]} )
    for s in strings:
        if 'checkFlag' in strings[s]:
            flag = flags.data[strings[s]['checkFlag']][0]
            exec( (s + '=\"' + strings[s][flag][lang] + '\"').encode('utf-8') )
        elif 'isCode' in strings[s] and strings[s]['isCode']:
            exec( (s + '=' + strings[s][lang]).encode('utf-8') )
        else:
            exec( (s + '=\"' + strings[s][lang] + '\"').encode('utf-8') )
language_button = Button(button_type="success")
language_button.on_click(changeLanguage)

# Initialise Variables
glob_theta1             = ColumnDataSource(data=dict(val=[radians(50)]))
glob_theta2             = ColumnDataSource(data=dict(val=[radians(140)]))
glob_Vector1            = ColumnDataSource(data=dict(val=[95]))
glob_Vector2            = ColumnDataSource(data=dict(val=[100]))
Vector1_source          = ColumnDataSource(data=dict(xS=[], xE=[], yS=[],yE=[]))
Vector2_source          = ColumnDataSource(data=dict(xS=[], xE=[], yS=[],yE=[]))
VectorResultant_source  = ColumnDataSource(data=dict(xS=[], xE=[], yS=[],yE=[]))
V1parallel_line_source  = ColumnDataSource(data=dict(x=[],y=[]))
V2parallel_line_source  = ColumnDataSource(data=dict(x=[],y=[]))
V1_label_source         = ColumnDataSource(data=dict(x=[],y=[],V1=[]))
V2_label_source         = ColumnDataSource(data=dict(x=[],y=[],V2=[]))
Resultant_label_source  = ColumnDataSource(data=dict(x=[],y=[],R=[]))
Resultant_values_source = ColumnDataSource(data=dict(x=[],y=[],names=[]))
flags                   = ColumnDataSource(data=dict(show=[False],lang=[std_lang]))

# responsible for the display of initial conditions 
def init ():
    updateVector1()
    updateVector2()
    updateResultant()
    
# update Vectors
def updateVector1 ():
    [theta1]  = glob_theta1.data["val"]  # input/
    [Vector1] = glob_Vector1.data["val"] # input/
 
    if (Vector1== 0):
        #Vector1_source.data = dict(xS=[],yS=[],xE=[],yE=[])
        Vector1_source.stream(dict(xS=[],yS=[],xE=[],yE=[]), rollover=-1)
        V1_label_source.data = dict (x=[],y=[],V1=[])
    else:
    # else the arrow is proportional to the Vector1
        xE = Vector1*cos(theta1)
        yE = Vector1*sin(theta1)
       # Vector1_source.data  = dict(xS=[0], yS=[0], xE=[xE], yE=[yE])
        Vector1_source.stream(dict(xS=[0], yS=[0], xE=[xE], yE=[yE]), rollover=1)
        V1_label_source.data = dict (x=[xE+3],y=[yE-3],V1=["V_1"])

def updateVector2 ():
    [theta2]  = glob_theta2.data["val"]  # input/
    [Vector2] = glob_Vector2.data["val"] # input/
    # if Vector2 = 0 then there is no arrow
    if (Vector2== 0):
        #Vector2_source.data = dict(xS=[],yS=[],xE=[],yE=[])
        Vector2_source.stream(dict(xS=[],yS=[],xE=[],yE=[]), rollover=-1)
        V2_label_source.data = dict (x=[],y=[],V2=[])
    else:
        # else the arrow is proportional to the Vector1
        xE = Vector2*cos(theta2)
        yE = Vector2*sin(theta2)
        #Vector2_source.data  = dict(xS=[0], yS=[0], xE=[xE], yE=[yE])
        Vector2_source.stream(dict(xS=[0], yS=[0], xE=[xE], yE=[yE]), rollover=1)
        V2_label_source.data = dict (x=[xE+3],y=[yE-3],V2=["V_2"])

def updateResultant():
    [theta1]  = glob_theta1.data["val"]  # input/
    [theta2]  = glob_theta2.data["val"]  # input/
    [Vector1] = glob_Vector1.data["val"] # input/
    [Vector2] = glob_Vector2.data["val"] # input/
    [show]    = flags.data["show"]
    
    xE = Vector1*cos(theta1)+Vector2*cos(theta2)
    yE = Vector1*sin(theta1)+Vector2*sin(theta2)
    R  = round(sqrt(xE**2.0+yE**2.0),1)
    if (abs(R) < 1e-3):
        #VectorResultant_source.data = dict(xS=[], yS=[], xE=[], yE=[])
        VectorResultant_source.stream(dict(xS=[],yS=[],xE=[],yE=[]), rollover=-1)
        Resultant_label_source.data = dict(x=[], y=[], R=[])
    else:
        #VectorResultant_source.data = dict(xS=[0], yS=[0], xE=[xE], yE=[yE])
        VectorResultant_source.stream(dict(xS=[0], yS=[0], xE=[xE], yE=[yE]), rollover=1)
        # Readjust positions
        xL = xE-3
        yL = yE-6
        Resultant_label_source.data = dict (x=[(xL/(sqrt(xL**2+yL**2)))*(sqrt(xL**2+yL**2)+10)],y=[(yL/(sqrt(xL**2+yL**2)))*(sqrt(xL**2+yL**2)+10)],R=['R'])
        
    # Show the resultant paralleogram
    V1parallel_line_source.data = dict(x=[Vector2*cos(theta2),xE], y=[Vector2*sin(theta2),yE])
    V2parallel_line_source.data = dict(x=[Vector1*cos(theta1),xE], y=[Vector1*sin(theta1),yE])

    if show:
        if R==0:
            angle = "-"
        else:
            if (xE>0 and yE>0):
                angle = round(atan(yE/xE)/pi*180,0)
            elif (xE<0 and yE>0) or (xE<0 and yE<0):
                angle = round(atan(yE/xE)/pi*180,0)+180
            elif (xE>0 and yE<0):
                angle = round(atan(yE/xE)/pi*180,0)+360
            else:
                angle = 0
        Resultant_values_source.data = dict(x=[100,100], y=[160,140], names=["|R| = " + str(R) + "\, \\mathrm{N}", "\\alpha_{R} = " + str(angle) + "\\,^{\\circ}"])
    else:
        Resultant_values_source.data = dict(x=[], y=[], names=[])

def ChangeShow():
    [show] = flags.data["show"]
    flags.data["show"] = [not show]
    updateResultant()        

# adding the vectors to the plot
Vector1_glyph = Arrow(end=NormalHead(line_color="#A2AD00",fill_color="#A2AD00", line_width=2,size=15),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=Vector1_source,line_color="#A2AD00",line_width=7)
Vector2_glyph = Arrow(end=NormalHead(line_color="#0065BD", fill_color="#0065BD", line_width=2,size=15),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=Vector2_source,line_color="#0065BD",line_width=7)
VectorResultant_glyph = Arrow(end=NormalHead(line_color="#E37222",fill_color="#E37222", line_width=2,size=15),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=VectorResultant_source,line_color="#E37222",line_width=7)
V1_label_glyph=LatexLabelSet(x='x', y='y',text='V1',text_font_size="15pt",level='overlay',source=V1_label_source)
V2_label_glyph=LatexLabelSet(x='x', y='y',text='V2',text_font_size="15pt",level='overlay',source=V2_label_source)
Resultant_label_glyph  = LatexLabelSet(x='x',y='y',text='R',text_font_size="15pt",level='overlay',source=Resultant_label_source)
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

init()

#Changing Vector1
def changeVector1(attr,old,new):
    glob_Vector1.data = dict(val=[new]) #      /output
    updateVector1()
    updateResultant()

#Changing Vector2
def changeVector2(attr,old,new):
    glob_Vector2.data = dict(val=[new]) #      /output
    updateVector2()
    updateResultant()

#changing theta1
def changetheta1(attr,old,new):
    glob_theta1.data = dict(val=[radians(new)]) #      /output
    updateVector1()
    updateResultant()

#changing theta2
def changetheta2(attr,old,new):
    glob_theta2.data = dict(val=[radians(new)]) #      /output
    updateVector2()
    updateResultant()
    
## Create slider to choose force applied
Vector1Slider = LatexSlider(title="|V1|=", value=95.0, value_unit="\mathrm{N}", start=0, end=100, step=5)
Vector1Slider.on_change('value',changeVector1)
Vector2Slider = LatexSlider(title="|V2|=", value=100.0, value_unit="\mathrm{N}", start=0.0, end=100.0, step=5)
Vector2Slider.on_change('value',changeVector2)

AngleVector1Slider = LatexSlider(title='\\alpha_{V1}=', value_unit='^{\\circ}', value=60.0, start=0.0, end=360.0, step=5)
AngleVector1Slider.on_change('value',changetheta1)
AngleVector2Slider = LatexSlider(title='\\alpha_{V2}=',value_unit='^{\\circ}', value=140.0, start=0.0, end=360.0, step=5)
AngleVector2Slider.on_change('value',changetheta2)

###Create Show Resultant Properties Button:
show_button = Button(button_type="success")
show_button.on_click(ChangeShow)

# add app description
description = Div(render_as_text=False, width=1050)

setDocumentLanguage(std_lang)

## Send to window
curdoc().add_root(column(row(Spacer(width=750),language_button),description,column(row(p,column(Vector1Slider,Vector2Slider,AngleVector1Slider,AngleVector2Slider,show_button)))))
#curdoc().title # managed in file "/static/strings.json"
