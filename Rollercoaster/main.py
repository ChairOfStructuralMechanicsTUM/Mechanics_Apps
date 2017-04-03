from __future__ import division
from PathFuncs import *
from bokeh.layouts import column, row
from bokeh.core.properties import Instance, List
from bokeh.models import Slider, LabelSet, Arrow, OpenHead, Button, Toggle, Slider
from bokeh.io import curdoc
import pandas as pd
import BarChart as BC
from physics import *

## Forces
NormalForce = ColumnDataSource(data=dict(xS=[],yS=[],xE=[],yE=[]))
DragForce = ColumnDataSource(data=dict(xS=[],yS=[],xE=[],yE=[]))
GravForce = ColumnDataSource(data=dict(xS=[],yS=[],xE=[],yE=[]))
## Track configurations
#Ramp
XRamp = [1,2.5,4,5.5,7,8.5,10,11.5,13]
YRamp = [13,11.5,10,8.5,7,5.5,4,2.5,1]
#Bumps
XBump = [0.8, 1.7, 3.6, 5.2, 6.9, 8.6, 10.35, 12.1, 14.2]
YBump = [14.2, 6.15, 6.9, 5.3, 6.55, 5.5, 6.8, 5.85, 7.3]
#Loop
XLoop = [1, 3.5, 6.64, 8.7, 6.8, 5.54, 10.0, 11.67, 13.9]
YLoop = [13, 3.3, 1.4, 3.8, 5.4, 3.16, 1.4, 4.8, 6.4]
## cartData
cartPosition=0
cartSpeed=0
cartAcc=[0,0]
cart = ColumnDataSource(data=dict(x=[],y=[]))
mu=0.2
Active=False
MechEng=100

## Functions
# initialisation
def init ():
    PathInit(p)
    updateForces()
    drawCart()
    updateBars()

# calculate new forces after movement
def updateForces ():
    global cartPosition, RollerCoasterPathSource, NormalForce, cartAcc, mu
    # get coordinates
    (x,y)=getPoint(cartPosition)
    # get normal vector
    (nx,ny)=normal(cartPosition)
    # get tangential vector
    (x2,y2)=deriv(cartPosition)
    
    if (cartSpeed==0 or mu==0):
        # if there is no friction, remove arrow
        DragForce.data=dict(xS=[],yS=[],xE=[],yE=[])
    else:
        # else friction = -mu*v
        DragForce.data=dict(xS=[x],yS=[y],xE=[x-x2*mu*cartSpeed],yE=[y-y2*mu*cartSpeed])
    # Gravitational force = -2 \hat{y} (m=1,g=2)
    # g=2 gives nicer arrows
    GravForce.data=dict(xS=[x],yS=[y],xE=[x],yE=[y-2.0])
    # normal force calculated such that forces in perpendicular direction are 0
    norm=getNormalForce([nx,ny],[-x2*mu*cartSpeed,-y2*mu*cartSpeed],[0.0,-2.0],True)
    # save normal force to arrow
    NormalForce.data=dict(xS=[x],yS=[y],xE=[x+norm[0]],yE=[y+norm[1]])
    # save acceleration = sum forces as m=1
    cartAcc=[norm[0]-x2*mu*cartSpeed,norm[1]-y2*mu*cartSpeed-2.0]

# draw cart after movement
def drawCart ():
    global cartPosition
    # coordinates of cart at (0,0)
    X=[-0.5,0.5,0.5,0.3,0.1,0.1,-0.3,-0.3,-0.5]
    Y=[0.0,0.0,0.4,0.7,0.7,0.3,0.3,0.7,0.7]
    # find cos(theta)=a/h, sin(theta)=o/h
    # theta angle between line and x axis
    # h=1 as |deriv|=1
    # => cos(theta)=x, sin(theta)=y
    (cosTheta,sinTheta)=deriv(cartPosition)
    # get coordinates
    (x,y)=getPoint(cartPosition)
    # get direction of travel
    S=NZsign(cartSpeed)
    for i in range(0,len(X)):
        # find position of coordinates
        xtemp=X[i]*S
        X[i]=xtemp*cosTheta-Y[i]*sinTheta+x
        Y[i]=xtemp*sinTheta+Y[i]*cosTheta+y
    # update cart
    cart.data=dict(x=X,y=Y)

# update bar chart
def updateBars ():
    global MechEng, cartSpeed, cartPosition
    # mechanical energy = kin energy + potential energy
    ME=0.5*cartSpeed**2+2.0*getHeight(cartPosition)
    if (ME<MechEng):
        # update mechanical energy if and only if it has decreased
        # this removes (visually) the rounding errors that make the total energy increase
        eFig.setHeight(0,ME)
        MechEng=ME
    # update potential energy = mgh (m=1)
    eFig.setHeight(1,2.0*getHeight(cartPosition))
    # update kinetic energy = 0.5 m v^2 (m=1)
    eFig.setHeight(2,0.5*cartSpeed**2)

# evolve cart position
def moveCart ():
    global cartPosition, cartSpeed, cartAcc, mu, Active
    dt=0.1
    # get new velocity, old velocity = speed*direction
    (nx,ny)=deriv(cartPosition)
    cartSpeedX=cartSpeed*nx+dt*cartAcc[0]
    cartSpeedY=cartSpeed*ny+dt*cartAcc[1]
    # new speed = |velocity|*direction
    direction=sign(cartSpeedX)*sign(nx)
    cartSpeed=direction*sqrt(cartSpeedX**2+cartSpeedY**2)
    # distance to be travelled
    s=abs(cartSpeed*dt)
    # initialise loop values
    sDone=0
    step=0.1
    factor=1.0
    # if cart is at end of track and accelerates off track then stop the call
    if ((cartPosition==0 and cartSpeed<0) or (cartPosition==len(RollerPointXPos)-1 and cartSpeed>0)):
        curdoc().remove_periodic_callback(moveCart)
        Active=False
        sDone=s
    # take smaller and smaller steps to approach s
    # (there is no formula to find the appropriate t such that |(X(t)-xnow,Y(t)-ynow)|=s
    while (sDone<s and factor<65):
        # find new position for current step
        newPos=cartPosition+direction*step/factor
        # if step carries into new segment then distance cannot be calculated
        # as segment are defined by different equations
        if (int(floor(newPos))>int(floor(cartPosition)) and int(floor(cartPosition))!=cartPosition):
            # if moving in a positive direction to new segment
            # new position is at boundary
            newPos=int(floor(newPos))
        elif (int(floor(newPos))<int(floor(cartPosition)) and int(floor(cartPosition))!=cartPosition):
            # if moving in a negative direction to new segment
            # new position is at boundary
            newPos=int(floor(cartPosition))
        # calculate distance travelled in this step
        pas=abs(getDistance(cartPosition,newPos))
        if (sDone+pas<=s or factor==64):
            # if the step means that the total distance travelled is
            # less than the distance that must be travelled,
            # then update position and distance travelled in this function
            cartPosition=newPos
            sDone+=pas
            if (newPos==0 or newPos==len(RollerPointXPos)-1):
                # if new position is first or last node then change direction
                direction=-direction
                cartSpeed=-cartSpeed
        else:
            # else reduce the step size
            factor*=2
    if (mu==0.0):
        # if no friction then use energy to calculate new speed
        # to remove energy fluctuations due to rounding errors
        cartSpeed=sign(cartSpeed)*sqrt(max(0,2.0*MechEng-4.0*getHeight(cartPosition)))
    # update the drawing
    drawCart()
    updateForces()
    updateBars()
    if (abs(cartSpeed)<=0.001 and cartAcc[0]**2+cartAcc[1]**2<0.01):
        # if an equilibrium has been reached then stop
        curdoc().remove_periodic_callback(moveCart)
        Active=False

# figure for bar charts
eFig = BC.BarChart(["Mechanische Energie\n(Mechanical Energy)","Potentielle Energie\n(Potential Energy)","Kinetische Energie\n(Kinetic Energy)"],
    [28,28,0],["#98C6EA","#A2AD00","#E37222"],[3,3,3])
eFig.Width(300)
eFig.Height(650)
eFig.fig.yaxis.visible=False

# figure for diagram
p = figure(title="", tools="", x_range=(0,15), y_range=(0,15))
init();
p.line(x='x',y='y',source=RollerCoasterPathSource,line_color="black")
p.add_tools(MoveNodeTool())
# function for tool
def on_mouse_move(attr, old, new):
    if (modify_path(attr,old,new)==1):
        # if the path is changed then update the drawing
        global MechEng
        MechEng=100
        updateForces()
        drawCart()
        updateBars()
p.tool_events.on_change('geometries', on_mouse_move)

# add force arrows
Normal_arrow_glyph = Arrow(end=OpenHead(line_color="#003359",line_width=2, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_color="#003359",line_width=2,source=NormalForce)
p.add_layout(Normal_arrow_glyph)
Drag_arrow_glyph = Arrow(end=OpenHead(line_color="#003359",line_width=2, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_color="#003359",line_width=2,source=DragForce)
p.add_layout(Drag_arrow_glyph)
Grav_arrow_glyph = Arrow(end=OpenHead(line_color="#003359",line_width=2, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_color="#003359",line_width=2,source=GravForce)
p.add_layout(Grav_arrow_glyph)
# add cart drawing
p.patch(x='x',y='y',fill_color="#0065BD",source=cart,level='annotation')

# functions which change the rollercoaster shape
def Ramp():
    global MechEng
    MechEng=100
    drawPath(XRamp,YRamp)
    updateForces()
    drawCart()
    updateBars()
ramp_button = Button(label="Rampe", button_type="success")
ramp_button.on_click(Ramp)

def Bump():
    global MechEng
    MechEng=100
    drawPath(XBump,YBump)
    updateForces()
    drawCart()
    updateBars()
bump_button = Button(label="Bumps", button_type="success")
bump_button.on_click(Bump)

def Loop():
    global MechEng
    MechEng=100
    drawPath(XLoop,YLoop)
    updateForces()
    drawCart()
    updateBars()
loop_button = Button(label="Looping", button_type="success")
loop_button.on_click(Loop)

# function which returns the cart to the beginning of the rollercoaster
def Reset():
    global cartPosition, cartSpeed, cartAcc, MechEng
    cartPosition=0
    cartSpeed=0
    cartAcc=[0,0]
    MechEng=100
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

# create slider to vary values of mu for the friction
def Friction(attr,old,new):
    global mu
    mu=new
drag_slider = Slider(title=u"Reibungskoeffizient (Coefficient of friction), \u00B5 = ", value=0.2, start=0.0, end=1.0, step=0.1,width=350)
drag_slider.on_change('value',Friction)

## Send to window
curdoc().add_root(row(eFig.getFig(),column(p),
    column(ramp_button,bump_button,loop_button,reset_button,play_button,pause_button,drag_slider)))
curdoc().title = "Rollercoaster"
