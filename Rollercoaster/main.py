from __future__ import division
from PathFuncs import *
from bokeh.layouts import column, row
from bokeh.core.properties import Instance, List
from bokeh.models import Slider, LabelSet, Arrow, OpenHead, Button, Toggle, Slider
from bokeh.io import curdoc
import pandas as pd
import BarChart as BC
from physics import *

#Forces
NormalForce = ColumnDataSource(data=dict(xS=[],yS=[],xE=[],yE=[]))
DragForce = ColumnDataSource(data=dict(xS=[],yS=[],xE=[],yE=[]))
GravForce = ColumnDataSource(data=dict(xS=[],yS=[],xE=[],yE=[]))
#Ramp
XRamp = [1,2.5,4,5.5,7,8.5,10,11.5,13]
YRamp = [13,11.5,10,8.5,7,5.5,4,2.5,1]
#Bumps
XBump = [0.8, 1.7, 3.6, 5.2, 6.9, 8.6, 10.35, 12.1, 14.2]
YBump = [14.2, 6.15, 6.9, 5.3, 6.55, 5.5, 6.8, 5.85, 7.3]
#Loop
XLoop = [1, 3.5, 6.64, 8.7, 6.8, 5.54, 10.0, 11.67, 13.9]
YLoop = [13, 3.3, 1.4, 3.8, 5.4, 3.16, 1.4, 4.8, 6.4]
#cartData
cartPosition=0
cartSpeed=0
cartAcc=[0,0]
cart = ColumnDataSource(data=dict(x=[],y=[]))
mu=0.2
Active=False

def init ():
    PathInit(p)
    updateForces()
    drawCart()
    updateBars()

def updateForces ():
    global cartPosition, RollerCoasterPathSource, NormalForce, cartAcc, mu
    i=cartPosition
    (x,y)=getPoint(i)
    (nx,ny)=normal(i)
    (x2,y2)=deriv(i)
    if (cartSpeed==0 or mu==0):
        DragForce.data=dict(xS=[],yS=[],xE=[],yE=[])
    else:
        DragForce.data=dict(xS=[x],yS=[y],xE=[x-x2*mu*cartSpeed],yE=[y-y2*mu*cartSpeed])
    GravForce.data=dict(xS=[x],yS=[y],xE=[x],yE=[y-2.0])
    norm=getNormalForce([nx,ny],[-x2*mu*cartSpeed,-y2*mu*cartSpeed],[0.0,-2.0],True)
    NormalForce.data=dict(xS=[x],yS=[y],xE=[x+norm[0]],yE=[y+norm[1]])
    cartAcc=[norm[0]-x2*mu*cartSpeed,norm[1]-y2*mu*cartSpeed-2.0]

def drawCart ():
    global cartPosition
    X=[-0.5,0.5,0.5,0.3,0.1,0.1,-0.3,-0.3,-0.5]
    Y=[0.0,0.0,0.4,0.7,0.7,0.3,0.3,0.7,0.7]
    (cosTheta,sinTheta)=deriv(cartPosition)
    (x,y)=getPoint(cartPosition)
    S=NZsign(cartSpeed)
    for i in range(0,len(X)):
        xtemp=X[i]*S
        X[i]=xtemp*cosTheta-Y[i]*sinTheta+x
        Y[i]=xtemp*sinTheta+Y[i]*cosTheta+y
    cart.data=dict(x=X,y=Y)

def updateBars ():
    eFig.setHeight(0,0.5*cartSpeed**2+2.0*getHeight(cartPosition))
    eFig.setHeight(1,2.0*getHeight(cartPosition))
    eFig.setHeight(2,0.5*cartSpeed**2)

def moveCart ():
    global cartPosition, cartSpeed, cartAcc
    dt=0.1
    (nx,ny)=deriv(cartPosition)
    cartSpeedX=cartSpeed*nx+dt*cartAcc[0]
    cartSpeedY=cartSpeed*ny+dt*cartAcc[1]
    cartSpeed=sign(cartSpeedX)*sign(nx)*sqrt(cartSpeedX**2+cartSpeedY**2)
    s=abs(cartSpeed*dt)
    direction=sign(cartSpeed)
    sDone=0
    step=0.1
    factor=1.0
    while (sDone<s and factor<33):
        newPos=cartPosition+direction*step/factor
        if (int(floor(newPos))>int(floor(cartPosition)) and int(floor(cartPosition))!=cartPosition):
            newPos=int(floor(newPos))
            if (newPos==len(RollerPointXPos)-1):
                direction=-direction
                cartSpeed=-cartSpeed
        elif (int(floor(newPos))<int(floor(cartPosition)) and int(floor(cartPosition))!=cartPosition):
            newPos=int(floor(cartPosition))
            if (newPos==0):
                direction=-direction
                cartSpeed=-cartSpeed
        pas=abs(getDistance(cartPosition,newPos))
        if (sDone+pas<=s):
            cartPosition=newPos
            sDone+=pas
        else:
            factor*=2
    drawCart()
    updateForces()
    updateBars()

# figure for bar charts
eFig = BC.BarChart(["Mechanische Energie\n(Mechanical Energy)","Potentielle Energie\n(Potential Energy)","Kinetische Energie\n(Kinetic Energy)"],
    [28,28,0],["purple","red","blue"],[3,3,3])
eFig.Width(300)
eFig.Height(650)
eFig.fig.yaxis.visible=False

# figure for diagram
p = figure(title="", tools="zoom_in,zoom_out,wheel_zoom", x_range=(0,15), y_range=(0,15))
init();
p.line(x='x',y='y',source=RollerCoasterPathSource,line_color="black")
p.add_tools(MoveNodeTool())
def on_mouse_move(attr, old, new):
    if (modify_path(attr,old,new)==1):
        updateForces()
        drawCart()
        updateBars()
p.tool_events.on_change('geometries', on_mouse_move)

Normal_arrow_glyph = Arrow(end=OpenHead(line_color="#003359",line_width=2, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_color="#003359",line_width=2,source=NormalForce)
p.add_layout(Normal_arrow_glyph)
Drag_arrow_glyph = Arrow(end=OpenHead(line_color="green",line_width=2, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_color="green",line_width=2,source=DragForce)
p.add_layout(Drag_arrow_glyph)
Grav_arrow_glyph = Arrow(end=OpenHead(line_color="#003359",line_width=2, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_color="#003359",line_width=2,source=GravForce)
p.add_layout(Grav_arrow_glyph)
p.patch(x='x',y='y',fill_color="red",source=cart,level='annotation')

def Ramp():
    drawPath(XRamp,YRamp)
    updateForces()
    drawCart()
    updateBars()
ramp_button = Button(label="Rampe", button_type="success")
ramp_button.on_click(Ramp)

def Bump():
    drawPath(XBump,YBump)
    updateForces()
    drawCart()
    updateBars()
bump_button = Button(label="Bumps", button_type="success")
bump_button.on_click(Bump)

def Loop():
    drawPath(XLoop,YLoop)
    updateForces()
    drawCart()
    updateBars()
loop_button = Button(label="Looping", button_type="success")
loop_button.on_click(Loop)

def Reset():
    global cartPosition, cartSpeed, cartAcc
    cartPosition=0
    cartSpeed=0
    cartAcc=[0,0]
    updateForces()
    drawCart()
    updateBars()
reset_button = Button(label="Reset", button_type="success")
reset_button.on_click(Reset)

## Create pause button
def pause (toggled):
    global Active
    # When active pause animation
    if (toggled):
        curdoc().remove_periodic_callback(moveCart)
        Active=False
    else:
        curdoc().add_periodic_callback(moveCart, 100)
        Active=True
pause_button = Toggle(label="Pause", button_type="success")
pause_button.on_click(pause)

## Create play button
def play ():
    global Active
    # if inactive, reactivate animation
    if (pause_button.active):
        # deactivating pause button reactivates animation
        # (calling add_periodic_callback twice gives errors)
        pause_button.active=False
    elif (not Active):
        curdoc().add_periodic_callback(moveCart, 100)
        Active=True
play_button = Button(label="Play", button_type="success")
play_button.on_click(play)

def Friction(attr,old,new):
    global mu
    mu=new
drag_slider = Slider(title=u"Friktion (Friction), \u00B5 = ", value=0.2, start=0.0, end=1.0, step=0.05)
drag_slider.on_change('value',Friction)

## Send to window
curdoc().add_root(row(eFig.getFig(),column(p),
    column(ramp_button,bump_button,loop_button,reset_button,play_button,pause_button,drag_slider)))
#curdoc().add_root(p)
curdoc().title = "Rollercoaster"
