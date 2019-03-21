from bokeh.models import ColumnDataSource
from math import pi


### Initial Values
radius = 10
centreX = 10
glob_MohrNx      = ColumnDataSource(data=dict(val=[0]))
glob_MohrNz      = ColumnDataSource(data=dict(val=[0]))
glob_MohrNxz     = ColumnDataSource(data=dict(val=[0]))
glob_MohrP_Angle = ColumnDataSource(data=dict(val=[0*(pi/180)]))
Neta =0 
Nzeta =0 
Nzetaeta =0  
rleft_x = centreX-radius
rleft_z=0


glob_MohrChangeShow = ColumnDataSource(data=dict(val=[-1]))
glob_NzetaI0        = ColumnDataSource(data=dict(val=[0]))
glob_NetaI0         = ColumnDataSource(data=dict(val=[0]))
glob_alpha          = ColumnDataSource(data=dict(val=[0]))

glob_MohrNzeta_zero_angles = ColumnDataSource(data=dict(val=[0]))
glob_MohrNeta_zero_angles  = ColumnDataSource(data=dict(val=[0]))


### Initializing variables
## Figure 1, Arrows: 
NxP_arrow_source  = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NzP_arrow_source  = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NxN_arrow_source  = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NzN_arrow_source  = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nxz1_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nxz2_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nxz3_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nxz4_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
## Figure 1, Rectangles:
NxP_rect_source  = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
NzP_rect_source  = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
NxN_rect_source  = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
NzN_rect_source  = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
Nxz1_rect_source = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
Nxz2_rect_source = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
Nxz3_rect_source = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
Nxz4_rect_source = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))

### Figure 2, Mohr Circle:
Mohr_Circle_source = ColumnDataSource(data=dict(x=[], y=[], radius=[]))
Wedge_source       = ColumnDataSource(data=dict(x=[], y=[],radius=[], sA=[], eA=[]))
Newplane_line_source      = ColumnDataSource(data=dict(x=[],y=[]))
OriginalPlane_line_source = ColumnDataSource(data=dict(x=[],y=[]))

##Figure 3, Rotating plane: 
Rotating_Plane_source     = ColumnDataSource(data=dict(x=[], y=[],angle = [],size =[]))
Rotating_Plane_red_source = ColumnDataSource(data=dict(x=[], y=[],angle = [],size =[]))
###Figure 3, Rotating Coordinate-System:
Rotating_Axis_X_source = ColumnDataSource(data=dict(xS=[], yS=[], xE=[], yE=[]))
Rotating_Axis_Y_source = ColumnDataSource(data=dict(xS=[], yS=[], xE=[], yE=[]))
##Figure 3, Arrows:
NzetaP_arrow_source    = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NzetaN_arrow_source    = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NetaP_arrow_source     = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NetaN_arrow_source     = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nzetaeta1_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nzetaeta2_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nzetaeta3_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nzetaeta4_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
##Figure 3, Rectangles:
NzetaP_rect_source    = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
NzetaN_rect_source    = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
NetaP_rect_source     = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
NetaN_rect_source     = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
Nzetaeta1_rect_source = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
Nzetaeta2_rect_source = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
Nzetaeta3_rect_source = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
Nzetaeta4_rect_source = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))


### Labels
Figure1Perm_Label_source   = ColumnDataSource(data=dict(x=[22,1], y=[-5, -27], names=['x', 'z']))
Figure2Perm_Label_source   = ColumnDataSource(data=dict(x=[23.5,1.5], y=[-2.5, 23], names=["\\sigma", "\\tau"]))
Figure2Moving_Label_source = ColumnDataSource(data=dict(x=[], y=[], names=[]))
Figure2Show_Label_source   = ColumnDataSource(data=dict(x=[], y=[], names=[]))
Figure3Perm_Label_source   = ColumnDataSource(data=dict(x=[22,1], y=[-5, -27], names=['x', 'z']))
Figure3Moving_Label_source = ColumnDataSource(data=dict(x=[], y=[], names =[]))
