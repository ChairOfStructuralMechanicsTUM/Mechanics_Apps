"""
Python Bokeh program which shows why Couple moment is called a free vector

"""


from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.models import ColumnDataSource, Slider, LabelSet, Arrow, OpenHead, Button, Line,Div
from bokeh.io import curdoc
from numpy import loadtxt
from os.path import dirname, join, split
from math import radians, cos, sin, tan

#Initialise Variables
Sp=0    # Distnace the Force couple that can be moved along the dotted line
theta = radians(90)
Dist = 50   # Perpendicular distance between the lines of action of vectors
theta1=90
Vector1=50              #Any vector which form a couple with Vector 2
Vector2=Vector1         #Any vector which form a couple with Vector 1
Vector1_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[],yE=[]))
Vector2_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[],yE=[]))

#For labels
V1_label_source = ColumnDataSource(data=dict(x=[],y=[],V1=[]))
V2_label_source = ColumnDataSource(data=dict(x=[],y=[],V2=[]))
RigidBody_label_source = ColumnDataSource(data=dict(x=[],y=[],RG=[]))
Distance_label_source = ColumnDataSource(data=dict(x=[],y=[],Dis=[]))   #for labeling the perpendicular distance line between vectors

#For lines                                       
Distance_line_source = ColumnDataSource(data=dict(x=[],y=[]))   # To draw the line between the points of application of Vectors
NewpositionLine1_source = ColumnDataSource(data=dict(x=[],y=[],angle=[]))
NewpositionLine2_source = ColumnDataSource(data=dict(x=[],y=[],angle=[]))
NewpositionLine3_source = ColumnDataSource(data=dict(x=[],y=[],angle=[]))
NewpositionLine4_source = ColumnDataSource(data=dict(x=[],y=[],angle=[]))


#responsible for the display of initial conditions 
def init ():
    updateVector1()
    updateVector2()
    #Distance_line_source.data = dict(x=[-150,-100], y=[-150,-150])
    Distance_line_source.stream(dict(x=[-150,-100], y=[-150,-150]),rollover=1)
    #NewpositionLine1_source.data = dict(x=[-150],y=[-150],angle=[90])
    NewpositionLine1_source.stream(dict(x=[-150],y=[-150],angle=[90]),rollover=1)
    #NewpositionLine2_source.data = dict(x=[-150],y=[-150],angle=[-90])
    NewpositionLine2_source.stream(dict(x=[-150],y=[-150],angle=[-90]), rollover=1)
    #NewpositionLine3_source.data = dict(x=[-100],y=[-150],angle=[90])
    NewpositionLine3_source.stream(dict(x=[-100],y=[-150],angle=[90]),rollover=1)
    #NewpositionLine4_source.data = dict(x=[-100],y=[-150],angle=[-90])
    NewpositionLine4_source.stream(dict(x=[-100],y=[-150],angle=[-90]),rollover=1)

    RigidBody_label_source.data=dict(x=[30],y=[-200],RG=["Rigid Body"])
    Distance_label_source.data =dict(x=[-105],y=[-150],Dis=["d = 50 "])
    
# update Vectors
def updateVector1 ():     # To update Vector 1 based on Angle it makes with horiizontal & its position on dotted line
    global Sp,theta,Vector1
 
    if (Vector1== 0):
        #Vector1_source.data = dict(xS=[],yS=[],xE=[],yE=[])
        Vector1_source.stream(dict(xS=[],yS=[],xE=[],yE=[]),rollover=1)
    
    else:
    # else the arrow is proportional to the Vector1
        Vector1 = 50/(sin(theta))
        xS=-150+Sp
        yS=-150+Sp
        xE=xS+Vector1*cos(theta)
        yE=yS+Vector1*sin(theta)
        #Vector1_source.data = dict(xS=[xS], yS=[yS], xE=[xE], yE=[yE])
        Vector1_source.stream(dict(xS=[xS], yS=[yS], xE=[xE], yE=[yE]),rollover=1)
        V1_label_source.data = dict (x=[xE+3],y=[yE-3],V1=["V"])    
        
        
        
def updateVector2 ():               # To update Vector 2 based on Angle it makes with horiizontal & its position on dotted line
    global Sp,Vector2, theta
    # if Vector2 = 0 then there is no arrow
    if (Vector2== 0):
        #Vector2_source.data = dict(xS=[],yS=[],xE=[],yE=[])
        Vector2_source.stream(dict(xS=[],yS=[],xE=[],yE=[]),rollover=1)
    else:
        # else the arrow is proportional to the Vector1
        Vector2 = 50/(sin(theta))
        xS=-100+Sp
        yS=-150+Sp
        xE=xS-(Vector2*cos(theta))
        yE=yS-(Vector2*sin(theta))
        #Vector2_source.data = dict(xS=[xS], yS=[yS], xE=[xE], yE=[yE])
        Vector2_source.stream(dict(xS=[xS], yS=[yS], xE=[xE], yE=[yE]),rollover=1)
        V2_label_source.data = dict (x=[xE+3],y=[yE+3],V2=["V"])

        
        
def updateLineOfAction():
    global Sp,Vector1,theta1
 
    #NewpositionLine1_source.data = dict(x=[-150+Sp],y=[-150+Sp],angle=[theta1])
    #NewpositionLine2_source.data = dict(x=[-150+Sp],y=[-150+Sp],angle=[theta1-180])
    #NewpositionLine3_source.data = dict(x=[-100+Sp],y=[-150+Sp],angle=[theta1])
    #NewpositionLine4_source.data = dict(x=[-100+Sp],y=[-150+Sp],angle=[theta1-180])
    NewpositionLine1_source.stream(dict(x=[-150+Sp],y=[-150+Sp],angle=[theta1]),rollover=1)
    NewpositionLine2_source.stream(dict(x=[-150+Sp],y=[-150+Sp],angle=[theta1-180]),rollover=1)
    NewpositionLine3_source.stream(dict(x=[-100+Sp],y=[-150+Sp],angle=[theta1]),rollover=1)
    NewpositionLine4_source.stream(dict(x=[-100+Sp],y=[-150+Sp],angle=[theta1-180]),rollover=1)

        
def UpdateDistanceLine():     #To update the distance line between Vectors
    global Sp,theta,Dist
    Dist = float(50*sin(theta))   
    #Distance_line_source.data = dict(x=[-150+Sp,-150+Sp+(Dist*sin(theta))], y=[-150+Sp,-150+Sp-(Dist*cos(theta))])
    Distance_line_source.stream(dict(x=[-150+Sp,-150+Sp+(Dist*sin(theta))], y=[-150+Sp,-150+Sp-(Dist*cos(theta))]))
    Distance_label_source.data= dict (x=[-150+Sp+(Dist*sin(theta))],y=[-150+Sp-(Dist*cos(theta))],Dis=["d = "])
    
# adding the vectors to the plot
Vector1_glyph = Arrow(end=OpenHead(line_color="black",line_width=10,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=Vector1_source,line_color="black",line_width=7)
Vector2_glyph = Arrow(end=OpenHead(line_color="blue",line_width=10,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=Vector2_source,line_color="blue",line_width=7)
V1_label_glyph=LabelSet(x='x', y='y',text='V1',text_font_size="15pt",level='glyph',source=V1_label_source)
V2_label_glyph=LabelSet(x='x', y='y',text='V2',text_font_size="15pt",level='glyph',source=V2_label_source)

RigidBody_label_glyph=LabelSet(x='x', y='y',text='RG',text_font_size="15pt",level='glyph',source=RigidBody_label_source)
Distance_label_glyph = LabelSet(x='x', y='y',text='Dis',text_font_size="20pt",level='glyph',source=Distance_label_source)

p = figure(tools="", x_range=(-200,200), y_range=(-200,200),plot_width=750, plot_height=625)
p.title.text_font_size="20pt"
p.ellipse(x=[-5], y=[-5], width=[410], height=300,
          angle=-40, color="#CAB2D6")   # ellipse centres at (-5,-5) as rigid body
p.line(x='x',y='y',line_dash='dashed',source= Distance_line_source, color="red")   
p.ray(x='x',y='y', length=400,angle='angle',angle_units="deg",line_dash='dashed',source= NewpositionLine1_source, color="black")
p.ray(x='x',y='y', length=400,angle='angle',angle_units="deg",line_dash='dashed',source= NewpositionLine2_source, color="black")
p.ray(x='x',y='y', length=400,angle='angle',angle_units="deg",line_dash='dashed',source= NewpositionLine3_source, color="black")
p.ray(x='x',y='y', length=400,angle='angle',angle_units="deg",line_dash='dashed',source= NewpositionLine4_source, color="black")


p.add_layout(Vector1_glyph)
p.add_layout(Vector2_glyph)
p.add_layout(V1_label_glyph)
p.add_layout(V2_label_glyph)
p.add_layout(RigidBody_label_glyph)
p.add_layout(Distance_label_glyph)

p.axis.visible = False
p.grid.visible = False
p.background_fill_color = "#D1F4FF"
init()

#Changing Distance along dotted line
def changeCouplePosition(attr,old,new):
    global Sp,Vector1, Active, DistanceSlider
  
    Sp=new
    Vector1=50
    updateVector1()
    updateVector2()
    UpdateDistanceLine()
    updateLineOfAction()
    
#changing theta
def changetheta(attr,old,new):
    global Vector1, Active, AngleVector1Slider,theta,theta1
  
    theta1=new
    theta=radians(new)
    updateVector1()
    updateVector2()
    UpdateDistanceLine()
    updateLineOfAction()
    
          
## Create slider to move couple along dotted line
DistanceSlider = Slider(title="Distance S",value=0,start=0,end=240,step=5)
DistanceSlider.on_change('value',changeCouplePosition)

## Create slider to move change the angle vector 1 makes with horizontal line
AngleVector1Slider= Slider(title="Angle of Vector 1", value=90.0, start=5.0, end=175.0, step=5)
AngleVector1Slider.on_change('value',changetheta)

# add app description
description_filename = join(dirname(__file__), "description.html")

description = Div(text=open(description_filename).read(), render_as_text=False, width=1200)

## Send to window
curdoc().add_root(column(description,column(row(p,column(DistanceSlider,AngleVector1Slider)))))
curdoc().title = "Moment a free vector"
