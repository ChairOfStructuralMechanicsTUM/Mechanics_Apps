from __future__ import division
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.core.properties import Instance, List
from bokeh.models import ColumnDataSource, Slider, LabelSet, Arrow, OpenHead
from bokeh.io import curdoc
from math import sqrt
import pandas as pd
import BarChart as BC
from MoveNodeTool import *
from MathFuncs import *
from physics import *

RollerNodeSource = []
RollerPointXPos = []
RollerPointYPos = []
RollerCoasterPathSource = ColumnDataSource(data=dict(x=[],y=[]))
EllipseTest = ColumnDataSource(data=dict(x=[],y=[]))
NodeIndices=[0,1,2,3,4,5,6,7,8]
currentNode=-1
#Forces
NormalForce = ColumnDataSource(data=dict(xS=[],yS=[],xE=[],yE=[]))
DragForce = ColumnDataSource(data=dict(xS=[],yS=[],xE=[],yE=[]))
GravForce = ColumnDataSource(data=dict(xS=[],yS=[],xE=[],yE=[]))
#cartData
cartPosition=55
cartSpeed=0
cart = ColumnDataSource(data=dict(x=[],y=[]))

def init ():
    global RollerPointXPos,RollerPointYPos,RollerNodeSource
    X=[1,3,5,7,11,7,6,7,12]
    Y=[1,3,4,5,1,3,2,1,1]
    for i in range(0,len(X)):
        RollerNodeSource.append(ColumnDataSource(data=dict(x=[X[i]],y=[Y[i]])))
        RollerPointXPos.append(X[i])
        RollerPointYPos.append(Y[i])
        p.ellipse(x='x',y='y',width=1,height=1,source=RollerNodeSource[i], 
            fill_color="#CCCCC6",line_color=None)
    X=cubicSpline(NodeIndices,X)
    Y=cubicSpline(NodeIndices,Y)
    RollerCoasterPathSource.data=dict(x=X,y=Y)
    updateForces()
    drawCart()
    updateBars()

def normal (i):
   (dx,dy)=deriv (i);
   return (-dy,dx)

def deriv (i):
    global RollerCoasterPathSource
    n=len(RollerCoasterPathSource.data ['x'])
    if (i==0):
        dx=RollerCoasterPathSource.data ['x'][1]- RollerCoasterPathSource.data ['x'][0]
        if (dx==0):
            return (0,1)
        dy=( RollerCoasterPathSource.data ['y'][1]- RollerCoasterPathSource.data ['y'][0])/dx
    elif (i==n):
        dx=RollerCoasterPathSource.data ['x'][n-1]- RollerCoasterPathSource.data ['x'][n-2]
        if (dx==0):
            return (0,1)
        dy=( RollerCoasterPathSource.data ['y'][n-1]- RollerCoasterPathSource.data ['y'][n-2])/dx
    else:
        dx=RollerCoasterPathSource.data ['x'][i+1]- RollerCoasterPathSource.data ['x'][i-1]
        if (dx==0):
            return (0,1)
        dy=( RollerCoasterPathSource.data ['y'][i+1]- RollerCoasterPathSource.data ['y'][i-1])/dx
    dx=sign(dx)
    dy*=dx
    norme=sqrt(dx**2+dy**2)
    dx=dx/norme
    dy=dy/norme
    return (dx,dy)

def updateForces ():
    global cartPosition, RollerCoasterPathSource, NormalForce
    i=cartPosition
    x=RollerCoasterPathSource.data ['x'][i]
    y=RollerCoasterPathSource.data ['y'][i]
    (nx,ny)=normal(i)
    (x2,y2)=deriv(i)
    if (cartSpeed==0):
        DragForce.data=dict(xS=[],yS=[],xE=[],yE=[])
    else:
        DragForce.data=dict(xS=[x],yS=[y],xE=[x-x2*cartSpeed],yE=[y-y2*cartSpeed])
    GravForce.data=dict(xS=[x],yS=[y],xE=[x],yE=[y-2.0])
    norm=getNormalForce([nx,ny],[-x2*cartSpeed,-y2*cartSpeed],[0.0,-2.0],True)
    NormalForce.data=dict(xS=[x],yS=[y],xE=[x+norm[0]],yE=[y+norm[1]])
    acc=[norm[0]-x2*cartSpeed,norm[1]-y2*cartSpeed-2.0]

def drawCart ():
    global cartPosition
    X=[-0.5,0.5,0.5,0.3,0.1,0.1,-0.3,-0.3,-0.5]
    Y=[0.0,0.0,0.4,0.7,0.7,0.3,0.3,0.7,0.7]
    (cosTheta,sinTheta)=deriv(cartPosition)
    x=RollerCoasterPathSource.data['x'][cartPosition]
    y=RollerCoasterPathSource.data['y'][cartPosition]
    for i in range(0,len(X)):
        xtemp=X[i]
        X[i]=X[i]*cosTheta-Y[i]*sinTheta+x
        Y[i]=xtemp*sinTheta+Y[i]*cosTheta+y
    cart.data=dict(x=X,y=Y)

def inNode (xPos,yPos):
    global RollerPointXPos,RollerPointYPos
    for i in range(0,len(RollerPointXPos)):
        if (abs(xPos-RollerPointXPos[i])<=1 and abs(yPos-RollerPointYPos[i])<=1):
            return i
    return -1

def on_mouse_move(attr, old, new):
    global RollerPointXPos,RollerPointYPos,RollerNodeSource, currentNode
    if (len(old)==1 and new[0][u'x']!=-1):
        if (currentNode==-1):
            XStart=old[0][u'x']
            YStart=old[0][u'y']
            currentNode=inNode(XStart,YStart)
        if (currentNode!=-1):
            RollerNodeSource[currentNode].data=dict(x=[new[0][u'x']],y=[new[0][u'y']])
            RollerPointXPos[currentNode]=new[0][u'x']
            RollerPointYPos[currentNode]=new[0][u'y']
            RollerCoasterPathSource.data=dict(x=cubicSpline(NodeIndices,RollerPointXPos),
                y=cubicSpline(NodeIndices,RollerPointYPos))
            updateForces()
            drawCart()
            updateBars()
    else:
        currentNode=-1

def updateBars ():
    eFig.setHeight(0,9.81*RollerCoasterPathSource.data['y'][cartPosition])
    eFig.setHeight(1,0.5*cartSpeed**2)

# figure for bar charts
eFig = BC.BarChart(['Potentielle Energie\n(Potential Energy)',"Kinetische Energie\n(Kinetic Energy)"],
    [100,0],["red","blue"],[3,3])
eFig.Width(200)
eFig.Height(650)
eFig.fig.yaxis.visible=False

# figure for diagram
p = figure(title="", tools="zoom_in,zoom_out,wheel_zoom", x_range=(0,15), y_range=(0,15))
init();
p.line(x='x',y='y',source=RollerCoasterPathSource,line_color="black")
p.add_tools(MoveNodeTool())
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

## Send to window
curdoc().add_root(row(eFig.getFig(),column(p)))
#curdoc().add_root(p)
curdoc().title = "Rollercoaster"
