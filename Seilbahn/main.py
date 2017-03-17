from __future__ import division
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Slider, Tool
from bokeh.io import curdoc
from draggableAxisAlignedRectangle import DraggableAxisAlignedRectangle
import numpy as np


BearingSource = []

# figure for diagram
p = figure(title="", tools="zoom_in,zoom_out,wheel_zoom", x_range=(0, 15), y_range=(0, 15))
draggables = [DraggableAxisAlignedRectangle(p, 1.0, 1.0, 1.0, 1.0),
              DraggableAxisAlignedRectangle(p, 1.0, 1.0, 5.0, 1.0)]

post_sources = draggables.__len__() * [None]

# create post holding the cable
for i in range(draggables.__len__()):
    handle = draggables[i]
    post_height = 5
    post_sources[i] = ColumnDataSource(dict(xs=[np.array([handle._pos_x,
                                                          handle._pos_x + handle._width,
                                                          handle._pos_x + .5 * handle._width])],
                                            ys=[np.array([handle._pos_y + handle._height,
                                                          handle._pos_y + handle._height,
                                                          handle._pos_y + handle._height + post_height])],
                                            cs=['k']))
    p.patches(xs='xs', ys='ys', color='cs', source=post_sources[i])


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

                xs = post_sources[i].data['xs']
                ys = post_sources[i].data['ys']
                cs = post_sources[i].data['cs']
                for j in range(xs.__len__()):
                    xs[j] += dx
                    ys[j] += dy

                print xs
                print ys
                post_sources[i].data = dict(xs=xs, ys=ys, cs=cs)
                #p.patches(xs='xs', ys='ys', color='cs', source=post_sources[i])

p.tool_events.on_change('geometries', on_mouse_move)

## Send to window
curdoc().add_root(p)
# curdoc().add_root(p)
curdoc().title = "Seilbahn"