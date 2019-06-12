from __future__ import division # float division only, like in python 3
from bokeh.models import ColumnDataSource
from math import sin, cos, radians
import numpy as np

# constants
g             = 9.81
maxR          = 4.0
alpha_max     = 25.0
rampLength    = 50
rampAddLength = 5  # excess length for better visualization
max_samples   = 100
buf           = 1e-10 # buffer size for stopping criterion
# create variables
alpha         = radians(20)
t             = 0
# variables created to avoid repeated calculations
# (speeds up calculations)
SIN           = sin(alpha)
COS           = cos(alpha)


###############################################################################
###               coordinates of the triangle (for reference)               ###
###############################################################################
# ramplength L is constant
# (TX0,TY0), alpha and L are given
# (TX1,TY1) and (TX2,TY2) are calculated from this
# aswell as the center of the objects in the creation functions

# (.,TY2) stays constant during the whole simulation
# (TX2,.), (TX1,TY1) can change due to a new alpha value

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

###############################################################################
###                    data sources and global variables                    ###
###############################################################################

# displacement, distance traveled
t_end             = [0.0,0.0,0.0]
fig0_samples      = []
fig1_samples      = []
fig2_samples      = []

# relate objects to figures
fig0_object       = "Sphere"
fig1_object       = "Full cylinder"
fig2_object       = "Hollow cylinder"

# plotting data for moving objects
fig0_data         = ColumnDataSource(data = dict(x=[],y=[],w=[],c=[],a=[]))
fig1_data         = ColumnDataSource(data = dict(x=[],y=[],w=[],c=[],a=[]))
fig2_data         = ColumnDataSource(data = dict(x=[],y=[],w=[],c=[],a=[]))
fig0_lines_data   = ColumnDataSource(data = dict(x=[],y=[]))
fig1_lines_data   = ColumnDataSource(data = dict(x=[],y=[]))
fig2_lines_data   = ColumnDataSource(data = dict(x=[],y=[]))
SphereXLines      = [np.array([]),np.array([])]
SphereYLines      = np.array([])

# values needed for calculations in corresponding plots
fig0_values       = dict(TX1=TX1,TY1=TY1,alpha=alpha,SIN=SIN,COS=COS,r=2.0,ri=0.5)
fig1_values       = dict(TX1=TX1,TY1=TY1,alpha=alpha,SIN=SIN,COS=COS,r=2.0,ri=0.5)
fig2_values       = dict(TX1=TX1,TY1=TY1,alpha=alpha,SIN=SIN,COS=COS,r=2.0,ri=1.5)

# plotting data for fixed objects
ramp_source0      = ColumnDataSource(data = dict(x=[TX1-rampAddLength*COS,TX0],y=[TY1+rampAddLength*SIN,TY0]))
ramp_source1      = ColumnDataSource(data = dict(x=[TX1-rampAddLength*COS,TX0],y=[TY1+rampAddLength*SIN,TY0]))
ramp_source2      = ColumnDataSource(data = dict(x=[TX1-rampAddLength*COS,TX0],y=[TY1+rampAddLength*SIN,TY0]))
wall_source0      = ColumnDataSource(data = dict(x=[TX1-rampAddLength*COS,TX1-rampAddLength*COS],y=[TY1+rampAddLength*SIN,TY0]))
wall_source1      = ColumnDataSource(data = dict(x=[TX1-rampAddLength*COS,TX1-rampAddLength*COS],y=[TY1+rampAddLength*SIN,TY0]))
wall_source2      = ColumnDataSource(data = dict(x=[TX1-rampAddLength*COS,TX1-rampAddLength*COS],y=[TY1+rampAddLength*SIN,TY0]))

# put them in a list for easy access in functions
fig_data          = [fig0_data,fig1_data,fig2_data]
fig_lines_data    = [fig0_lines_data,fig1_lines_data,fig2_lines_data]
fig_values        = [fig0_values,fig1_values,fig2_values]
fig_samples       = [fig0_samples,fig1_samples,fig2_samples]
fig_objects       = [fig0_object, fig1_object, fig2_object]
ramp_sources      = [ramp_source0,ramp_source1,ramp_source2]
wall_sources      = [wall_source0,wall_source1,wall_source2]

# global variables to stear internal stuff
time_display      = [ColumnDataSource(data = dict(x=[],y=[],t=[])),
                     ColumnDataSource(data = dict(x=[],y=[],t=[])),
                     ColumnDataSource(data = dict(x=[],y=[],t=[]))]
fig_in_use        = [True,True,True]  # [True]*len(fig_data)  for more general case
figure_list       = [None,None,None]
glob_fun_handles  = [None,None,None]

glob_callback_id  = ColumnDataSource(data = dict(callback_id  = [None]))
glob_SphereXLines = ColumnDataSource(data = dict(SphereXLines = [SphereXLines]))
glob_SphereYLines = ColumnDataSource(data = dict(SphereYLines = [SphereYLines]))

glob_time         = dict(t=t, t_samples = np.linspace(0.0,6.0,max_samples), num_rolls=0)

# images/icons
icon_display      = [ColumnDataSource(data = dict(x=[],y=[],img=[])),
                     ColumnDataSource(data = dict(x=[],y=[],img=[])),
                     ColumnDataSource(data = dict(x=[],y=[],img=[]))]
### bokeh bug?: ###
#"Rolling_test/static/images/first.svg" does not show reliably???
# use winner.svg for now
###             ###
icons_collection  = ["Rolling_test/static/images/winner.svg",
                     "Rolling_test/static/images/second.svg",
                     "Rolling_test/static/images/third.svg"]
