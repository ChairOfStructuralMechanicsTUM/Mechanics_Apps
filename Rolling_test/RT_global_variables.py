from __future__ import division # float division only, like in python 3
from bokeh.models import ColumnDataSource
from math import sin, cos, radians
import numpy as np

# create variables
g             = 9.81
alpha         = radians(20)
# constants
maxR          = 4.0
alpha_max     = 25.0
rampLength    = 50
rampAddLength = 5  # excess length for better visualization
# variables created to avoid repeated calculations
# (speeds up calculations)
SIN           = sin(alpha)
COS           = cos(alpha)
offset        = -rampLength*COS
t             = 0.0
H             = rampLength*SIN

SphereXLines = [np.array([]),np.array([])]
SphereYLines = np.array([])


# create ColumnDataSources
fig0_data         = ColumnDataSource(data = dict(x=[],y=[],w=[],c=[],a=[]))
fig0_lines_data   = ColumnDataSource(data = dict(x=[],y=[]))
fig1_data         = ColumnDataSource(data = dict(x=[],y=[],w=[],c=[],a=[]))
fig1_lines_data   = ColumnDataSource(data = dict(x=[],y=[]))
fig2_data         = ColumnDataSource(data = dict(x=[],y=[],w=[],c=[],a=[]))
fig2_lines_data   = ColumnDataSource(data = dict(x=[],y=[]))
# put them in a list for easy access in functions
fig_data          = [fig0_data,fig1_data,fig2_data]
fig_lines_data    = [fig0_lines_data,fig1_lines_data,fig2_lines_data]


ramp_source       = ColumnDataSource(data = dict(x=[offset-rampAddLength*COS,0],y=[H+rampAddLength*SIN,0]))
wall_source       = ColumnDataSource(data = dict(x=[offset-rampAddLength*COS,offset-rampAddLength*COS],y=[H+rampAddLength*SIN,0]))
AngleMarkerSource = ColumnDataSource(data = dict(x=[],y=[]))
AlphaPos          = ColumnDataSource(data = dict(x=[],y=[],t=[]))

time_display      = [ColumnDataSource(data = dict(x=[],y=[],t=[])),
                     ColumnDataSource(data = dict(x=[],y=[],t=[])),
                     ColumnDataSource(data = dict(x=[],y=[],t=[]))]
fig_in_use        = [True,True,True]  # [True]*len(fig_data)  for more general case
figure_list       = [None,None,None]
glob_fun_handles  = [None,None,None]

# global variables
glob_callback_id  = ColumnDataSource(data = dict(callback_id = [None]))
glob_SphereXLines = ColumnDataSource(data = dict(SphereXLines = [SphereXLines]))
glob_SphereYLines = ColumnDataSource(data = dict(SphereYLines = [SphereYLines]))

glob_values = dict(offset = offset,
                   alpha  = alpha,
                   SIN    = SIN,
                   COS    = COS,
                   g      = g, # could also be constant
                   t      = t,
                   H      = H)

