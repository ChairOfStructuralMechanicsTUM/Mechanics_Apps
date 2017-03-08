from __future__ import division
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.core.properties import Instance, List
from bokeh.models import ColumnDataSource, Slider, LabelSet, Arrow, OpenHead, Tool, CustomJS
from bokeh.io import curdoc
import pandas as pd
import BarChart as BC

RollerNodeSource = []
RollerPointXPos = []
RollerPointYPos = []
RollerCoasterPathSource = ColumnDataSource(data=dict(x=[],y=[]))
EllipseTest = ColumnDataSource(data=dict(x=[],y=[]))

def inNode (xPos,yPos):
    global RollerPointXPos,RollerPointYPos
    for i in range(0,len(RollerPointXPos)):
        if (abs(xPos-RollerPointXPos[i])<=1 and abs(yPos-RollerPointYPos[i])<=1):
            return i
    return -1

def init ():
    global RollerPointXPos,RollerPointYPos,RollerNodeSource
    X=[1,3,5,7,11]
    Y=[1,3,4,5,1]
    for i in range(0,len(X)):
        RollerNodeSource.append(ColumnDataSource(data=dict(x=[X[i]],y=[Y[i]])))
        RollerPointXPos.append(X[i])
        RollerPointYPos.append(Y[i])
        p.ellipse(x='x',y='y',width=1,height=1,source=RollerNodeSource[i], 
            fill_color="#CCCCC6",line_color=None)
    cubicSpline(X,Y)

def find2Deriv (x,f):
    temp=[0,(f[2]-f[1])/(x[2]-x[1])-(f[1]-f[0])/(x[1]-x[0])]
    uDiag=[(x[2]-x[0])/3.0]
    for i in range(1,len(x)-2):
        b=(f[i+2]-f[i+1])/(x[i+2]-x[i+1])-(f[i+1]-f[i])/(x[i+1]-x[i])
        lNow=(x[i+1]-x[i])/(6.0*uDiag[i-1])
        temp.append(b-lNow*temp[i])
        uDiag.append((x[i+2]-x[i])/3.0-lNow*(x[i+1]-x[i])/6.0)
    n=len(uDiag)
    temp[n]/=uDiag[n-1]
    for i in range(n-1,0,-1):
        temp[i]=(temp[i]-(x[i+1]-x[i])*temp[i+1]/6.0)/uDiag[i-1]
    temp.append(0)
    return temp

def cubicSpline(x,f):
    f2=find2Deriv(x,f)
    X=[]
    Y=[]
    for i in range(0,len(x)-1):
        h=x[i+1]-x[i];
        xnow=x[i]
        X.append(xnow)
        Y.append(f[i])
        # test and optimise number
        for j in range(1,20):
            xnow+=h/20.0
            X.append(xnow)
            Y.append((f2[i]*(x[i+1]-xnow)**3 + f2[i+1]*(xnow-x[i])**3)/(h*6.0)
                + ((f[i+1]-f[i])/h + (f2[i]-f2[i+1])*h/6.0)*(xnow-x[i])+f[i]-f2[i]*h**2/6.0)
    X.append(x[len(x)-1])
    Y.append(f[len(x)-1])
    RollerCoasterPathSource.data=dict(x=X,y=Y)

# figure for diagram
p = figure(title="", tools="zoom_in,zoom_out,wheel_zoom", x_range=(0,15), y_range=(0,15))
init();
p.line(x='x',y='y',source=RollerCoasterPathSource,line_color="black")

JS_CODE = """
import * as p from "core/properties"
import {GestureTool, GestureToolView} from "models/tools/gestures/gesture_tool"

export class DrawToolView extends GestureToolView

  # this is executed on subsequent mouse/touch moves
  _pan: (e) ->
      frame = @plot_model.frame
      canvas = @plot_view.canvas

      vx = canvas.sx_to_vx(e.bokeh.sx)
      vy = canvas.sy_to_vy(e.bokeh.sy)
      if not frame.contains(vx, vy)
        return null

      x = frame.x_mappers['default'].map_from_target(vx)
      y = frame.y_mappers['default'].map_from_target(vy)
      @plot_model.plot.tool_events.geometries = [{x:x, y:y}]

  # this is executed then the pan/drag ends
  _pan_end: (e) ->
      @plot_model.plot.tool_events.geometries = [{x:-1, y:-1}]

export class DrawTool extends GestureTool
  default_view: DrawToolView
  type: "DrawTool"

  tool_name: "Drag Span"
  icon: "bk-tool-icon-pan"
  event_type: "pan"
  default_order: 12

  @define { vals: [ p.Instance ] }
"""

class DrawTool(Tool):
    __implementation__ = JS_CODE

p.add_tools(DrawTool())

def on_mouse_move(attr, old, new):
    global RollerPointXPos,RollerPointYPos,RollerNodeSource
    if (len(old)==1 and new[0][u'x']!=-1):
        XStart=old[0][u'x']
        YStart=old[0][u'y']
        i=inNode(XStart,YStart)
        if (i!=-1):
            RollerNodeSource[i].data=dict(x=[new[0][u'x']],y=[new[0][u'y']])
            RollerPointXPos[i]=new[0][u'x']
            RollerPointYPos[i]=new[0][u'y']
            cubicSpline(RollerPointXPos,RollerPointYPos)
        
p.tool_events.on_change('geometries', on_mouse_move)

# figure for bar charts
eFig = BC.BarChart(['Potentielle Energie\n(Potential Energy)',"Kinetische Energie\n(Kinetic Energy)"],
    [100,0],["red","blue"],[3,3])
eFig.Width(200)
eFig.Height(650)
eFig.fig.yaxis.visible=False

## Send to window
curdoc().add_root(row(eFig.getFig(),column(p)))
#curdoc().add_root(p)
curdoc().title = "Rollercoaster"
