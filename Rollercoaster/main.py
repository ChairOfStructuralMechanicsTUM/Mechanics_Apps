from __future__ import division
from DraggablePath import DraggablePath
from Cart import Cart
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.models import Arrow, OpenHead, Button, Toggle, Slider
from bokeh.io import curdoc
import BarChart as BC
from physics import getNormalForce
from math import floor, ceil
from os.path import dirname, split
from numpy import sign, sqrt
from MoveNodeTool import MoveNodeTool

## Physical parameters
mu=0.2 # friction
MechEng=100 # energy
gravForce = [0.0, -2.0] # gravity
## Forces
NormalForce_source = ColumnDataSource(data=dict(xS=[], yS=[], xE=[], yE=[]))
DragForce_source = ColumnDataSource(data=dict(xS=[], yS=[], xE=[], yE=[]))
GravForce_source = ColumnDataSource(data=dict(xS=[], yS=[], xE=[], yE=[]))
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
Active=False


def init():
    """
    initialisation
    :return:
    """
    updateForces()
    updateBars()
    eFig.ResetYRange()


def updateForces():
    """
    calculate new forces after movement
    :return:
    """
    # get coordinates
    (x,y)=path.get_point(cart.position)
    # get normal vector
    (nx,ny)=path.get_normal(cart.position)
    # get tangential vector
    (x2,y2)=path.get_derivative(cart.position)
    
    if cart.speed==0 or mu==0:
        # if there is no friction, remove arrow
        DragForce_source.data=dict(xS=[], yS=[], xE=[], yE=[])
    else:
        # else friction = -mu*v
        DragForce_source.data=dict(xS=[x], yS=[y], xE=[x - x2 * mu * cart.speed], yE=[y - y2 * mu * cart.speed])

    # Gravitational force = -2 \hat{y} (m=1,g=2)
    GravForce_source.data=dict(xS=[x], yS=[y], xE=[x + gravForce[0]], yE=[y + gravForce[1]])

    # normal force calculated such that forces in perpendicular direction are 0
    norm=getNormalForce([nx,ny],[-x2*mu*cart.speed,-y2*mu*cart.speed],gravForce,True)
    # save normal force to arrow
    NormalForce_source.data=dict(xS=[x], yS=[y], xE=[x + norm[0]], yE=[y + norm[1]])

    # save acceleration = sum forces as m=1
    cart.acceleration=[norm[0]-x2*mu*cart.speed+gravForce[0],norm[1]-y2*mu*cart.speed+gravForce[1]]


def updateBars():
    """
    update bar chart
    :return:
    """
    global MechEng
    # mechanical energy = kin energy + potential energy
    ME=0.5*cart.speed**2+2.0*path.get_height(cart.position)
    if (ME<MechEng):
        # update mechanical energy if and only if it has decreased
        # this removes (visually) the rounding errors that make the total energy increase
        eFig.setHeight(0,ME)
        MechEng=ME
    # update potential energy = mgh (m=1)
    eFig.setHeight(1,2.0*path.get_height(cart.position))
    # update kinetic energy = 0.5 m v^2 (m=1)
    eFig.setHeight(2,0.5*cart.speed**2)


# todo should be moved into Cart class!!!
def moveCart():
    """
    evolve cart position
    :return:
    """
    global Active
    dt=0.1
    # get new velocity, old velocity = speed*direction
    (nx,ny)=path.get_derivative(cart.position)
    cartSpeedX=cart.speed*nx+dt*cart.acceleration[0]
    cartSpeedY=cart.speed*ny+dt*cart.acceleration[1]
    # new speed = |velocity|*direction
    direction=sign(cartSpeedX)*sign(nx)
    cart.speed=direction*sqrt(cartSpeedX**2+cartSpeedY**2)
    # distance to be travelled
    s=abs(cart.speed*dt)
    # initialise loop values
    sDone=0
    step=0.1
    factor=1.0
    # if cart is at end of track and accelerates off track then stop the call
    if (cart.position==0 and cart.speed < 0) or (cart.position==len(path.control_point_x)-1 and cart.speed>0):
        curdoc().remove_periodic_callback(moveCart)
        Active=False
        sDone=s
    # take smaller and smaller steps to approach s
    # (there is no formula to find the appropriate t such that |(X(t)-xnow,Y(t)-ynow)|=s
    while sDone<s and factor<65:
        # find new position for current step
        newPos=cart.position + direction*step/factor
        # if step carries into new segment then distance cannot be calculated
        # as segment are defined by different equations
        if (int(floor(newPos))>int(floor(cart.position)) and int(floor(cart.position))!=cart.position):
            # if moving in a positive direction to new segment
            # new position is at boundary
            newPos=int(floor(newPos))
        elif (int(floor(newPos))<int(floor(cart.position)) and int(floor(cart.position))!=cart.position):
            # if moving in a negative direction to new segment
            # new position is at boundary
            newPos=int(floor(cart.position))
        # calculate distance travelled in this step
        pas=abs(path.get_distance(cart.position, newPos))
        if (sDone+pas<=s or factor==64):
            # if the step means that the total distance travelled is
            # less than the distance that must be travelled,
            # then update position and distance travelled in this function
            cart.position=newPos
            sDone+=pas
            if newPos==0 or newPos==len(path.control_point_x)-1:
                # if new position is first or last node then change direction
                direction=-direction
                cart.speed=-cart.speed
        else:
            # else reduce the step size
            factor*=2
    if (mu==0.0):
        # if no friction then use energy to calculate new speed
        # to remove energy fluctuations due to rounding errors
        cart.speed=sign(cart.speed)*sqrt(max(0,2.0*MechEng-4.0*path.get_height(cart.position)))
    # update the drawing
    cart.draw(path)
    updateForces()
    updateBars()
    if abs(cart.speed)<=0.001 and cart.acceleration[0]**2+cart.acceleration[1]**2<0.01:
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
plot = figure(title="", tools="", x_range=(0, 15), y_range=(0, 15))
path = DraggablePath(plot)
cart = Cart(plot, path)
cart.draw(path)
init()
plot.add_tools(MoveNodeTool())


def on_mouse_move(attr, old, new):
    """
    callback function for MoveNodeTool
    :param attr:
    :param old:
    :param new:
    :return:
    """
    currentNode=path.modify_path(old, new)
    down=int(floor(cart.position))
    up=int(ceil(cart.position))
    Min=min(up-1,down)
    Max=max(down+1,up)
    if Min <= path.currentNode and Max >= path.currentNode:
        # if the path is changed at an adjacent node then update the drawing
        # further nodes can influence the cart, but their influence is minimal
        # so this reduces lag
        global MechEng
        MechEng=100
        updateForces()
        cart.draw(path)
        updateBars()
    elif currentNode == -1:
        # when the movement is finished, update the cart position regardless
        global MechEng
        MechEng=100
        updateForces()
        cart.draw(path)
        updateBars()

plot.tool_events.on_change('geometries', on_mouse_move)

# add force arrows
Normal_arrow_glyph = Arrow(end=OpenHead(line_color="#003359",line_width=2, size=10),
                           x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_color="#003359", line_width=2, source=NormalForce_source)
plot.add_layout(Normal_arrow_glyph)
Drag_arrow_glyph = Arrow(end=OpenHead(line_color="#003359",line_width=2, size=10),
                         x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_color="#003359", line_width=2, source=DragForce_source)
plot.add_layout(Drag_arrow_glyph)
Grav_arrow_glyph = Arrow(end=OpenHead(line_color="#003359",line_width=2, size=10),
                         x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_color="#003359", line_width=2, source=GravForce_source)
plot.add_layout(Grav_arrow_glyph)

# functions which change the rollercoaster shape
def Ramp():
    global MechEng, eFig
    MechEng=1000
    path.compute_path(XRamp,YRamp)
    updateForces()
    cart.draw(path)
    updateBars()
    eFig.ResetYRange()
ramp_button = Button(label="Rampe", button_type="success")
ramp_button.on_click(Ramp)

def Bump():
    global MechEng, eFig
    MechEng=1000
    path.compute_path(XBump,YBump)
    updateForces()
    cart.draw(path)
    updateBars()
    eFig.ResetYRange()
bump_button = Button(label="Bumps", button_type="success")
bump_button.on_click(Bump)


def loop():
    global MechEng, eFig
    MechEng=1000
    path.compute_path(XLoop,YLoop)
    updateForces()
    cart.draw(path)
    updateBars()
    eFig.ResetYRange()


loop_button = Button(label="Loop", button_type="success")
loop_button.on_click(loop)


def reset():
    """
    function which returns the cart to the beginning of the rollercoaster
    :return:
    """
    global MechEng, eFig
    cart.reset()
    cart.draw(path)
    MechEng=1000
    updateForces()
    updateBars()
    eFig.ResetYRange()


reset_button = Button(label="Reset", button_type="success")
reset_button.on_click(reset)


def pause(toggled):
    """
    callback for pause button
    :param toggled:
    :return:
    """
    global Active
    # When active pause animation
    if(toggled):
        curdoc().remove_periodic_callback(moveCart)
        Active=False
    else:
        curdoc().add_periodic_callback(moveCart, 100)
        Active=True

pause_button = Toggle(label="Pause", button_type="success")
pause_button.on_click(pause)


def play():
    """
    callback for play button
    :return:
    """
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


def friction(attr, old, new):
    """
    callback for friction slider
    :param attr:
    :param old:
    :param new:
    :return:
    """
    global mu
    mu=new

drag_slider = Slider(title=u"Reibungskoeffizient (Coefficient of friction), \u00B5 = ", value=0.2, start=0.0, end=1.0, step=0.1,width=350)
drag_slider.on_change('value', friction)

## Send to window
curdoc().add_root(row(eFig.getFig(),
                      column(plot),
                      column(ramp_button,bump_button,loop_button,Spacer(height=50),play_button,pause_button,reset_button,drag_slider)
                      ))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
