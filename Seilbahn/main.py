from __future__ import division
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Slider, Tool
from bokeh.io import curdoc
from draggablePost import DraggablePost
from draggableCart import DraggableCart
import numpy as np


BearingSource = []

# figure for diagram
p = figure(title="", tools="zoom_in,zoom_out,wheel_zoom", x_range=(0, 15), y_range=(0, 15))
draggables = [DraggablePost(p, 1.0, 1.0, 1.0, 1.0),
              DraggablePost(p, 1.0, 1.0, 5.0, 1.0),
              DraggableCart(p, 1.0, 1.0, 2.5, 5.0),]

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
    global RollerPointXPos, RollerPointYPos, RollerNodeSource
    if (len(old) == 1 and new[0][u'x'] != -1):
        XStart = old[0][u'x']
        YStart = old[0][u'y']
        XEnd = new[0][u'x']
        YEnd = new[0][u'y']
        dx = XEnd - XStart
        dy = YEnd - YStart
        for i in range(draggables.__len__()):
            draggable = draggables[i]
            if draggable.is_hit(XStart, YStart):
                draggable.translate(dx, dy)

p.tool_events.on_change('geometries', on_mouse_move)

## Send to window
curdoc().add_root(p)
# curdoc().add_root(p)
curdoc().title = "Seilbahn"