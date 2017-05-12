from __future__ import division
from bokeh.plotting import figure
from bokeh.models import Slider, LabelSet, Arrow, OpenHead, Select, Button
from bokeh.layouts import column, row
from bokeh.io import curdoc
from drawingFuncs import *
from math import radians, cos, sin, tan
from os.path import dirname, join, split

# initialise variables
aim_line = ColumnDataSource(data=dict(x=[],y=[]))
hill_source = ColumnDataSource(data=dict(x=[],y=[]))
theta = radians(30)
speed = 50
g = 9.81
PlanetGravity = dict(Weltraum = 0.0, Mercur = 3.61, Venus = 8.83, Erde = 9.81, Mars = 3.75, Ceres = 0.27,
    Jupiter = 26.0, Saturn = 11.2, Uranus = 10.5, Neptun = 13.3, Pluto = 0.61)
PlanetHue = dict(Weltraum = "#696A8C", Mercur = "#EDD9FC", Venus = "#FCDDBB", Erde = "#D1F4FF", Mars = "#FF9E9E", Ceres = "#C4C4C4",
    Jupiter = "#FFE1AD", Saturn = "#F3FFC9", Uranus = "#46FAB2", Neptun = "#AFC0DB", Pluto = "#DBD0D0")
x_0 = 5.0
y_0 = 7.5
direction_arrow = ColumnDataSource(data=dict(xS=[],yS=[],xE=[],yE=[]))
t=0
Active = False
height = 0
mass = 0.7

def init ():
    updateTargetArrow()

# calculate banana position during trajectory
def bananaPosition (t):
    global x_0, speed, theta
    x = x_0 + speed*cos(theta)*t
    y = y_0 + speed*sin(theta)*t-g*t**2/2.0
    return (x,y)

# calculate monkey position during fall
def monkeyDrop (t):
    y = -g*t**2/2.0
    return y

# update directional indicator arrows
def updateTargetArrow ():
    global direction_arrow, speed, theta, aim_line, x_0, y_0
    # if speed = 0 then there is no arrow
    if (speed == 0):
        direction_arrow.data = dict(xS=[],yS=[],xE=[],yE=[])
    else:
        # else the arrow is proportional to the speed
        xE=speed*cos(theta)
        yE=speed*sin(theta)
        direction_arrow.data = dict(xS=[x_0], yS=[y_0], xE=[xE+x_0], yE=[yE+y_0])
        # the dotted line is calculated from cos and sin as numerical errors
        # mean that a solution using tan does not lie on the direction arrow
        aim_line.data = dict(x=[x_0,100*xE],y=[y_0,y_0+100*yE])

# function which makes banana and monkey move
def evolve ():
    global t, Active
    t+=0.1
    (xB,yB)=moveBanana(bananaPosition(t))
    (xM,yM)=moveMonkey(monkeyDrop(t))
    # if monkey is hit with banana then stop
    if (xB>xM and xB<xM+20 and yB>yM and yB<yM+20):
        curdoc().remove_periodic_callback(evolve)
        Active = False
    # else if the banana hit the floor then stop
    elif (yB<0 or yM<0):
        curdoc().remove_periodic_callback(evolve)
        Active = False
    # else if nothing is falling and the banana has exited the screen
    elif (grav_select.value=="Weltraum" and yB>105):
        curdoc().remove_periodic_callback(evolve)
        Active = False

# set up image
p = figure(tools="",x_range=(0,200),y_range=(0,100),width=900,height=450)
p.line(x='x',y='y',line_dash='dashed',source=aim_line,color="black")
p.line(x='x',y='y',source=hill_source,color="black")
arrow_glyph = Arrow(end=OpenHead(line_color="black",line_width=3,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=direction_arrow,
    line_color="black",line_width=3)
p.add_layout(arrow_glyph)
drawMonkey(p)
drawBranch(p)
drawBanana(p)
drawCannon(p)
drawBase(p)
p.background_fill_color = PlanetHue["Erde"]
p.grid.visible=False

init()

## slider/button/dropdown functions
def changeTheta(attr,old,new):
    global theta, Active, angle_slider
    # if it has been modified during the simulation
    # move back == deactivated (does not exist in bokeh)
    if (Active and theta!=radians(new)):
        angle_slider.value=old
    else:
        # else update angle and update images
        theta=radians(new)
        rotateCannon(radians(30-new))
        updateTargetArrow()
# angle increment is large to prevent lag
angle_slider = Slider(title=u"\u0398 (\u00B0)",value=30,start=0,end=65,step=5)
angle_slider.on_change('value',changeTheta)
def changeSpeed(attr,old,new):
    global speed, Active, speed_slider
    # if it has been modified during the simulation
    # move back == deactivated (does not exist in bokeh)
    if (Active and speed!=new):
        speed_slider.value=old
    else:
        # else update speed and directional arrow
        speed=new
        updateTargetArrow()
speed_slider = Slider(title="Geschwindigkeit (m/s)",value=50,start=0,end=120,step=5)
speed_slider.on_change('value',changeSpeed)
# mass is not necessary but function is needed to protect the integrity of the simulation
def massCheck(attr,old,new):
    global Active, mass, mass_slider
    if (Active and mass!=new):
        mass_slider.value=old
    else:
        mass=new
mass_slider = Slider(title="Masse (kg)",value=mass,start=0,end=2,step=0.1)
mass_slider.on_change('value',massCheck)
def changeHeight(attr,old,new):
    global y_0, hill_source, Active, speed_slider
    # if it has been modified during the simulation
    # move back == deactivated (does not exist in bokeh)
    if (Active and height!=new):
        speed_slider.value=old
    else:
        # else change height and update drawings
        modifyHeight(new)
        y_0+=(new-old)
        updateTargetArrow()
        hill_source.data=dict(x=[0,30,30],y=[new,new,0])
height_slider = Slider(title=u"H\u00F6he (m)",value=0.0,start=0,end=60,step=5)
height_slider.on_change('value',changeHeight)
def changeGrav(attr,old,new):
    global g, PlanetGravity, Active
    # if it has been modified during the simulation
    # move back == deactivated (does not exist in bokeh)
    if (Active and g!=PlanetGravity[new]):
        grav_select.value=old
    else:
        # else reset and change gravity
        g=PlanetGravity[new]
        p.background_fill_color = PlanetHue[new]
        Reset()
grav_select = Select(title="Planet:", value="Erde",
    options=["Weltraum", "Mercur", "Venus", "Erde", "Mars", "Ceres", "Jupiter", "Saturn", "Uranus", "Neptun","Pluto"])
grav_select.on_change('value',changeGrav)

def Fire():
    global Active, grav_select
    if (not Active):
        if (t!=0):
            Reset()
        # if simulation is not already started
        # release branch and start simulation
        monkeyLetGo(grav_select.value!="Erde")
        curdoc().add_periodic_callback(evolve, 50)
        Active = True
fire_button = Button(label="Feuer",button_type="success")
fire_button.on_click(Fire)

def Reset():
    global Active,t
    # if simulation is in progress, stop simulation
    if (Active):
        curdoc().remove_periodic_callback(evolve)
        Active = False
    # return banana, monkey and cannon to original positions
    moveBanana()
    moveMonkey()
    # make monkey grab branch again (also resets helmet)
    monkeyGrab(grav_select.value!="Erde")
    # reset time
    t=0
reset_button = Button(label="Reset",button_type="success")
reset_button.on_click(Reset)

## Send to window
curdoc().add_root(row(p,column(angle_slider,speed_slider,mass_slider,height_slider,grav_select,fire_button,reset_button)))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
