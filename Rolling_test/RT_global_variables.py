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
#offset        = -rampLength*COS
t             = 0.0
#H             = rampLength*SIN


###############################################################################
###               coordinates of the triangle (for reference)               ###
###############################################################################
# ramplength L is constant
# (TX0,TY0), alpha and L are given
# (TX1,TY1) and (TX2,TY2) are calculated from this
# aswell as the center of the objects in the creation functions

# (TX2,TY2) stays constant during the whole simulation
# (TX1,TY1) can change due to a new alpha value

#    (TX1,TY1)
#        .
#        .   .
#        .       .
#        .           .   L
#        .               .
#        .                   .
#        .                       .
#        .                      .    .
#        .                     .  alpha  .
#        ....................................
#    (TX2,TY2)                           (TX0,TY0)

TX0 = 0
TY0 = 0

TX1 = TX0 - COS*rampLength
TX2 = TX1

TY1 = TY0 + SIN*rampLength
TY2 = TY0



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


ramp_source       = ColumnDataSource(data = dict(x=[TX1-rampAddLength*COS,TX0],y=[TY1+rampAddLength*SIN,TY0]))
wall_source       = ColumnDataSource(data = dict(x=[TX1-rampAddLength*COS,TX1-rampAddLength*COS],y=[TY1+rampAddLength*SIN,TY0]))
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

glob_values = dict(TX1    = TX1,
                   alpha  = alpha,
                   SIN    = SIN,
                   COS    = COS,
                   g      = g, # could also be constant
                   t      = t,
                   TY1    = TY1)

