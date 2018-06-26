# -*- coding: utf-8 -*-
"""
Created on Wed,13.06.2018

@author: Sascha Kubisch
"""

"""
Python Bokeh program which explains the concept of Mohr's Cirlce interactively

"""
from bokeh.plotting import figure
from bokeh.layouts import column, row, layout
from bokeh.models import ColumnDataSource,Slider,Div,Arrow,OpenHead,NormalHead,LabelSet,Button
from bokeh.models.markers import Square,Circle
from bokeh.models.glyphs import Ellipse,Wedge,Rect
from bokeh.models.layouts import Spacer
from bokeh.io import curdoc

from math import pi,sqrt,pow,sin,cos,atan 

from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_div import LatexDiv
from latex_label import LatexLabel
from latex_label_set import LatexLabelSet

### Initial Values
radius = 10
centreX = 10
glMohrNx =0
glMohrNz =0
glMohrNxz =0
glMohrP_Angle = 0*(pi/180)
Neta =0 
Nzeta =0 
Nzetaeta =0  
rleft_x = centreX-radius
rleft_z=0

global glMohrChangeShow
glMohrChangeShow  = -1

global NzetaI0
NzetaI0     =  0

global NetaI0
NetaI0      =  0

global alpha
alpha       = 0


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
Figure2Perm_Label_source   = ColumnDataSource(data=dict(x=[16,1.5], y=[-2.5, 15.5], names=["\\sigma", "\\tau"]))
Figure2Moving_Label_source = ColumnDataSource(data=dict(x=[], y=[], names=[]))
Figure2Show_Label_source   = ColumnDataSource(data=dict(x=[], y=[], names=[]))
Figure3Perm_Label_source   = ColumnDataSource(data=dict(x=[22,1], y=[-5, -27], names=['x', 'z']))
Figure3Moving_Label_source = ColumnDataSource(data=dict(x=[], y=[], names =[]))


###Initial Calculations and Value settings
def init():

    Normal_X_slider.value=0
    Normal_Z_slider.value=0
    Tangential_XZ_slider.value=0
    Plane_Angle_slider.value=0

    ## Figure 1: Set values for arrows
    NxP_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    NxN_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    NzP_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    NzN_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nxz1_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nxz2_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nxz3_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nxz4_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    ##Figure 1, Set Rectangles:
    NxP_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
    NxN_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
    NzP_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
    NxN_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
    Nxz1_rect_source.data = dict(x=[], y=[], w=[], h=[], angle=[])
    Nxz2_rect_source.data = dict(x=[], y=[], w=[], h=[], angle=[])
    Nxz3_rect_source.data = dict(x=[], y=[], w=[], h=[], angle=[])
    Nxz4_rect_source.data = dict(x=[], y=[], w=[], h=[], angle=[])
    

    
    

def reset():

    Normal_X_slider.disabled      = False
    Normal_Z_slider.disabled      = False
    Tangential_XZ_slider.disabled = False
    Plane_Angle_slider.disabled   = True

    global glMohrChangeShow
    glMohrChangeShow  = -1
   
    global NzetaI0
    NzetaI0     =  0

    global NetaI0
    NetaI0      =  0

    global alpha
    global glMohrP_Angle
    alpha = 0
    glMohrP_Angle = 0*(pi/180)
    radius = 10
    centreX = 10
    glMohrNx =0
    glMohrNz =0
    glMohrNxz =0
    
    ### Calculations
    radius    = float(sqrt(pow(((glMohrNx-glMohrNz)/2),2)+pow(glMohrNxz,2)))
    centreX   = float((glMohrNx+glMohrNz)/2)

    Normal_X_slider.value=0
    Normal_Z_slider.value=0
    Tangential_XZ_slider.value=0
    Plane_Angle_slider.value=0

    ### Figure 1, Reset values for arrows:
    NxP_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    NxN_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    NzP_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    NzN_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nxz1_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nxz2_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nxz3_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nxz4_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    ## Figure 1, Reset Rectangles:
    NxP_rect_source.data   = dict(x=[], y=[], w=[], h=[], angle=[])
    NxN_rect_source.data   = dict(x=[], y=[], w=[], h=[], angle=[])
    NzP_rect_source.data   = dict(x=[], y=[], w=[], h=[], angle=[])
    NzN_rect_source.data   = dict(x=[], y=[], w=[], h=[], angle=[])
    Nxz1_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
    Nxz2_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
    Nxz3_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
    Nxz4_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
    
    ### Figure 2, Reset Circle:
    Mohr_Circle_source.data          = dict(x=[centreX], y=[0], radius=[radius])
    Newplane_line_source.data        = dict(x=[], y=[])
    OriginalPlane_line_source.data   = dict(x=[], y=[])
    Figure2Moving_Label_source.data  = dict(x=[],y=[],names =[])
    Figure2Show_Label_source.data    = dict(x=[],y=[],names =[])
    Wedge_source.data                = dict(x=[], y=[],radius=[], sA=[], eA=[])
    glMohrFigure2_angle_label.text = ''

    ## Figure 3, Reset rotating plane:
    Rotating_Plane_source.data     = dict(x=[], y=[],angle =[],size = [])
    Rotating_Plane_red_source.data = dict(x=[], y=[],angle =[],size = [])
    ## Figure 3, Reset arrows:
    NzetaP_arrow_source.data    = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    NzetaN_arrow_source.data    = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    NetaP_arrow_source.data     = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    NetaN_arrow_source.data     = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nzetaeta1_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nzetaeta2_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nzetaeta3_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nzetaeta4_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    ## Figure 3, Reset rectangles:
    NzetaP_rect_source.data    = dict(x=[], y=[], w=[], h=[], angle=[])
    NzetaN_rect_source.data    = dict(x=[], y=[], w=[], h=[], angle=[])
    NetaP_rect_source.data     = dict(x=[], y=[], w=[], h=[], angle=[])
    NetaN_rect_source.data     = dict(x=[], y=[], w=[], h=[], angle=[])
    Nzetaeta1_rect_source.data = dict(x=[], y=[], w=[], h=[], angle=[])
    Nzetaeta2_rect_source.data = dict(x=[], y=[], w=[], h=[], angle=[])
    Nzetaeta3_rect_source.data = dict(x=[], y=[], w=[], h=[], angle=[])
    Nzetaeta4_rect_source.data = dict(x=[], y=[], w=[], h=[], angle=[])
    ## Figure 3, Reset rotating axis:
    Rotating_Axis_X_source.data=dict(xS=[], yS=[], xE=[], yE=[])
    Rotating_Axis_Y_source.data=dict(xS=[], yS=[], xE=[], yE=[])
    Figure3Moving_Label_source.data=dict(x=[], y=[], names =[])
    






    
def show():
    
    global glMohrChangeShow
    if glMohrChangeShow == 1:
        global glMohrP_Angle
        radius   = float(sqrt(pow(((glMohrNx-glMohrNz)/2),2)+pow(glMohrNxz,2)))
        centreX  = float((glMohrNx+glMohrNz)/2)
        rleft_x  = centreX-radius
        rright_x = centreX+radius

        ## Print Labels for principal stress and direction
        alpha=180*atan(glMohrNxz/(glMohrNz+(-rleft_x+0.00001)))/(pi)
        alpha=int(alpha+0.5)
        Figure2Show_Label_source.data = dict(x=[rleft_x,rright_x,centreX],
                                                y=[0,0,0],
                                                names=['\\sigma_{II}','\\sigma_{I}','\\sigma_{M}'])
        Wedge_source.data=dict(x=[rleft_x], y=[0],radius=[radius/2], sA=[atan(glMohrNxz/(glMohrNz+(-rleft_x)))], eA=[0])
        glMohrFigure2_angle_label.text = '\\alpha_0=' + str(alpha)
        glMohrChangeShow = glMohrChangeShow*-1

    elif glMohrChangeShow == -1:
        
        Wedge_source.data                = dict(x=[], y=[],radius=[], sA=[], eA=[])
        Figure2Show_Label_source.data    = dict(x=[], y=[], names =[])
        glMohrFigure2_angle_label.text = ''
        #global glMohrChangeShow
        glMohrChangeShow = glMohrChangeShow*-1




def draw():

    Normal_X_slider.disabled      = True
    Normal_Z_slider.disabled      = True
    Tangential_XZ_slider.disabled = True
    Plane_Angle_slider.disabled   = False

    global glMohrChangeShow
    glMohrChangeShow  = 1

    ## Calculations
    radius    = float(sqrt(pow(((glMohrNx-glMohrNz)/2),2)+pow(glMohrNxz,2)))
    centreX   = float((glMohrNx+glMohrNz)/2)
    Neta      = float(((glMohrNx+glMohrNz)/2)-(((glMohrNx-glMohrNz)/2)*cos(2*glMohrP_Angle))-glMohrNxz*sin(2*glMohrP_Angle))
    Nzetaeta  = float((-(((glMohrNx-glMohrNz)/2)*sin(2*glMohrP_Angle)))+glMohrNxz*cos(2*glMohrP_Angle))

    ## Calculate Angle for which Nzeta or Neta will be zero (sign-change-method):
    global glMohrNzeta_zero_angles
    global glMohrNeta_zero_angles

    NZeta_List0 = [181]*360
    NZeta_List1 = [181]*360
    glMohrNzeta_zero_angles = [181]*360
    Neta_List0 = [181]*360
    Neta_List1 = [181]*360
    glMohrNeta_zero_angles = [181]*360

    ## Nzeta:
    for n in range(-180,180):
        NZeta_List0[n+180] = float(((glMohrNx+glMohrNz)/2)+(((glMohrNx-glMohrNz)/2)*cos(2*-n*pi/180))+glMohrNxz*sin(2*-n*pi/180))
        NZeta_List1[n+180] = n
    count = 0
    for m in range(-180,179):
        if NZeta_List0[m+180]*NZeta_List0[m+181]<0:
            glMohrNzeta_zero_angles[count]=NZeta_List1[m+180]
            count = count+1
    ## Neta:
    for n in range(-180,180):
        Neta_List0[n+180] = float(((glMohrNx+glMohrNz)/2)-(((glMohrNx-glMohrNz)/2)*cos(2*-n*pi/180))-glMohrNxz*sin(2*-n*pi/180))
        Neta_List1[n+180] = n
    count = 0
    for m in range(-180,179):
        if Neta_List0[m+180]*Neta_List0[m+181]<0:
            glMohrNeta_zero_angles[count]=Neta_List1[m+180]
            count = count+1


    ##Figure 1, Draw glMohrNx and keep it until reset() ist called:
    
    if(glMohrNx*0.75<0):
        NxP_arrow_source.data = dict(xS=[12.5-glMohrNx*0.75],  xE=[12.5],  yS=[0], yE=[0], lW = [2])
        NxN_arrow_source.data = dict(xS=[-12.5+glMohrNx*0.75], xE=[-12.5], yS=[0], yE=[0], lW = [2]) 

        NxP_rect_source.data  = dict(x=[(25-glMohrNx*0.75)/2],  y=[0], w=[glMohrNx*0.75-1.5], h = [13], angle=[0])
        NxN_rect_source.data  = dict(x=[(-25+glMohrNx*0.75)/2], y=[0], w=[glMohrNx*0.75-1.5], h = [13], angle=[0])
        
    elif(glMohrNx*0.75==0):
        NxP_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        NxN_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])

        NxP_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])
        NxN_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])

    else:
        NxP_arrow_source.data  = dict(xS=[12.5],  xE=[12.5+glMohrNx*0.75],  yS=[0], yE=[0], lW = [2])
        NxN_arrow_source.data  = dict(xS=[-12.5], xE=[-12.5-glMohrNx*0.75], yS=[0], yE=[0], lW = [2])

        NxP_rect_source.data   = dict(x=[(25+glMohrNx*0.75)/2],  y=[0], w=[glMohrNx*0.75+1.5], h = [13], angle=[0])        
        NxN_rect_source.data   = dict(x=[(-25-glMohrNx*0.75)/2], y=[0], w=[glMohrNx*0.75+1.5], h = [13], angle=[0])  
    

    ##Figure 1, Draw glMohrNz and keep it until reset() ist called:
    new = glMohrNz
    new=new*0.75
    if(new<0):
        NzP_arrow_source.data = dict(xS=[0], xE=[0], yS=[12.5-new],  yE=[12.5],  lW = [2])
        NzN_arrow_source.data = dict(xS=[0], xE=[0], yS=[-12.5+new], yE=[-12.5], lW = [2])

        NzP_rect_source.data  = dict(x=[0], y=[(25-new)/2],  w=[13], h = [new-1.5], angle=[0])
        NzN_rect_source.data  = dict(x=[0], y=[(-25+new)/2], w=[13], h = [new-1.5], angle=[0])   
    elif (new==0):
        NzP_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        NzN_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])

        NzP_rect_source.data   = dict(x=[], y=[], w=[], h = [], angle=[])
        NzN_rect_source.data   = dict(x=[], y=[], w=[], h = [], angle=[])
    else:
        NzP_arrow_source.data = dict(xS=[0], xE=[0], yS=[12.5],  yE=[12.5+new], lW = [2])
        NzN_arrow_source.data = dict(xS=[0], xE=[0], yS=[-12.5], yE=[-12.5-new], lW = [2])

        NzP_rect_source.data  = dict(x=[0], y=[(25+new)/2],  w=[13], h = [new+1.5], angle=[0])
        NzN_rect_source.data  = dict(x=[0], y=[(-25-new)/2], w=[13], h = [new+1.5], angle=[0])   
         
          
    new = glMohrNxz
    new=new*0.75        
    if(new==0):
        Nxz1_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        Nxz2_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        Nxz3_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        Nxz4_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])    
         
        Nxz1_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
        Nxz2_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
        Nxz3_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
        Nxz4_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
    else:     
        Nxz1_arrow_source.data = dict(xS=[9],       xE=[9],        yS=[0-(new/2)], yE=[0+(new/2)], lW = [2])
        Nxz2_arrow_source.data = dict(xS=[-9],      xE=[-9],       yS=[0+(new/2)], yE=[0-(new/2)], lW = [2])
        Nxz3_arrow_source.data = dict(xS=[-new/2],  xE=[new/2],    yS=[9],         yE=[9],         lW = [2])
        Nxz4_arrow_source.data = dict(xS=[(new/2)], xE=[-(new/2)], yS=[-9],        yE=[-9],        lW = [2]) 
         
        Nxz1_rect_source.data  = dict(x=[9],  y=[0],  w=[0.3*new+0.5], h=[13],          angle=[0])
        Nxz2_rect_source.data  = dict(x=[-9], y=[0],  w=[0.3*new+0.5], h=[13],          angle=[0])
        Nxz3_rect_source.data  = dict(x=[0],  y=[9],  w=[13],          h=[0.3*new+0.5], angle=[0])
        Nxz4_rect_source.data  = dict(x=[0],  y=[-9], w=[13],          h=[0.3*new+0.5], angle=[0])


    ## Figure 2, draw Mohr-Circle:
    Mohr_Circle_source.data = dict(x=[centreX], y=[0], radius=[radius])
    Wedge_source.data       = dict(x=[], y=[],radius=[], sA=[], eA=[])

    Newplane_line_source.data       = dict(x=[rleft_x,Neta,Neta], y=[rleft_z,Nzetaeta,0])
    OriginalPlane_line_source.data  = dict(x=[rleft_x,glMohrNz,glMohrNz], y=[rleft_z,glMohrNxz,0])
    Figure2Show_Label_source.data   = dict(x=[],y=[], names =[])

    ## Figure 3, initializing:
    Rotating_Plane_source.data = dict(x=[0], y=[0],angle =[-glMohrP_Angle],size = [75])

  
    ChangeRotatingPlane_Forces()
    ChangeMohrCircle()



def NormalForceX_init(attr,old,new):

   ## Figure 1, Present the Normal Forces while Draw-Button wasn't yet activated:  
   
        global glMohrNx
        glMohrNx = new 
        new = new*0.75
        if(new<0):
            NxP_arrow_source.data = dict(xS=[12.5-new],  xE=[12.5],  yS=[0], yE=[0], lW = [2])
            NxN_arrow_source.data = dict(xS=[-12.5+new], xE=[-12.5], yS=[0], yE=[0], lW = [2]) 
     
            NxP_rect_source.data  = dict(x=[(25-new)/2],  y=[0], w=[new-1.5], h = [13], angle=[0])
            NxN_rect_source.data  = dict(x=[(-25+new)/2], y=[0], w=[new-1.5], h = [13], angle=[0]) 
        elif(new==0):
            NxP_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
            NxN_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
     
            NxP_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])
            NxN_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])

        else:
            NxP_arrow_source.data  = dict(xS=[12.5],  xE=[12.5+new],  yS=[0], yE=[0], lW = [2])
            NxN_arrow_source.data  = dict(xS=[-12.5], xE=[-12.5-new], yS=[0], yE=[0], lW = [2])
 
            NxP_rect_source.data   = dict(x=[(25+new)/2],  y=[0], w=[new+1.5], h = [13], angle=[0])        
            NxN_rect_source.data   = dict(x=[(-25-new)/2], y=[0], w=[new+1.5], h = [13], angle=[0]) 


    
def NormalForceZ_init(attr,old,new):

    ## Figure 1, Present the Normal Forces while draw() hasn't been called yet:

        ## Global change of glMohrNz
        global glMohrNz   
        glMohrNz = new
        new=new*0.75
        if(new<0):
            NzP_arrow_source.data = dict(xS=[0], xE=[0], yS=[12.5-new],  yE=[12.5],  lW = [2])
            NzN_arrow_source.data = dict(xS=[0], xE=[0], yS=[-12.5+new], yE=[-12.5], lW = [2])

            NzP_rect_source.data  = dict(x=[0], y=[(25-new)/2],  w=[13], h = [new-1.5], angle=[0])
            NzN_rect_source.data  = dict(x=[0], y=[(-25+new)/2], w=[13], h = [new-1.5], angle=[0])   
        elif (new==0):
            NzP_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
            NzN_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])

            NzP_rect_source.data   = dict(x=[], y=[], w=[], h = [], angle=[])
            NzN_rect_source.data   = dict(x=[], y=[], w=[], h = [], angle=[])
        else:
            NzP_arrow_source.data = dict(xS=[0], xE=[0], yS=[12.5],  yE=[12.5+new],  lW = [2])
            NzN_arrow_source.data = dict(xS=[0], xE=[0], yS=[-12.5], yE=[-12.5-new], lW = [2])

            NzP_rect_source.data  = dict(x=[0], y=[(25+new)/2],  w=[13], h = [new+1.5], angle=[0])
            NzN_rect_source.data  = dict(x=[0], y=[(-25-new)/2], w=[13], h = [new+1.5], angle=[0])   


    
def TangentialXZ_init(attr,old,new):

    ## Figure 1, Present the Shear Forces while draw() hasn't yet been called:

        ## global change of glMohrNxz    
        global glMohrNxz     
        glMohrNxz = new

        # Check if glMohrNxz is zero to prevent division by zero:
        if glMohrNxz == 0:
            glMohrNxz = 0.00001
        
        new=new*0.75
            
        if(new==0):
            Nxz1_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
            Nxz2_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
            Nxz3_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
            Nxz4_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])    
         
            Nxz1_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
            Nxz2_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
            Nxz3_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
            Nxz4_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
    
        else:     
            Nxz1_arrow_source.data = dict(xS=[9],       xE=[9],        yS=[0-(new/2)], yE=[0+(new/2)], lW = [2])
            Nxz2_arrow_source.data = dict(xS=[-9],      xE=[-9],       yS=[0+(new/2)], yE=[0-(new/2)], lW = [2])
            Nxz3_arrow_source.data = dict(xS=[-new/2],  xE=[new/2],    yS=[9],         yE=[9],         lW = [2])
            Nxz4_arrow_source.data = dict(xS=[(new/2)], xE=[-(new/2)], yS=[-9],        yE=[-9],        lW = [2]) 
         
            Nxz1_rect_source.data  = dict(x=[9],  y=[0],  w=[0.3*new+0.5], h=[13],          angle=[0])
            Nxz2_rect_source.data  = dict(x=[-9], y=[0],  w=[0.3*new+0.5], h=[13],          angle=[0])
            Nxz3_rect_source.data  = dict(x=[0],  y=[9],  w=[13],          h=[0.3*new+0.5], angle=[0])
            Nxz4_rect_source.data  = dict(x=[0],  y=[-9], w=[13],          h=[0.3*new+0.5], angle=[0])


        
def changePlaneAngle(attr,old,new):

        global glMohrP_Angle
        global alpha

        alpha= new
        glMohrP_Angle = -new*(pi/180)


        ## Paint Rotating Plane red if angle=alpha_0
        radius = float(sqrt(pow(((glMohrNx-glMohrNz)/2),2)+pow(glMohrNxz,2)))
        centreX = float((glMohrNx+glMohrNz)/2)
        rleft_x=centreX-radius
        alpha_0=180*atan(glMohrNxz/(glMohrNz+(-rleft_x+0.00001)))/(pi)
        alpha_0=int(alpha_0+0.5)
        
        alpharepetitions = [-90, -180, 0, 90, 180]
        for n in alpharepetitions:
            if alpha == alpha_0+n:
                Rotating_Plane_red_source.data = dict(x=[0], y=[0], angle =[-glMohrP_Angle], size = [75])
                Rotating_Plane_source.data     = dict(x=[],  y=[],  angle =[],         size = []  )
                break
        else:
            Rotating_Plane_source.data     = dict(x=[0], y=[0], angle =[-glMohrP_Angle], size = [75])
            Rotating_Plane_red_source.data = dict(x=[],  y=[],  angle =[],         size = []  )

        # Figure 3, Rotate Axis:  
        glMohrP_Angle = -glMohrP_Angle
        Rotating_Axis_X_source.data = dict(xS=[0], yS=[0], xE=[25*cos(glMohrP_Angle)],    yE=[25*sin(glMohrP_Angle)  ])
        Rotating_Axis_Y_source.data = dict(xS=[0], yS=[0], xE=[-25*sin(-glMohrP_Angle)],  yE=[-25*cos(-glMohrP_Angle)])
        
        glMohrP_Angle = -glMohrP_Angle
        ChangeMohrCircle()
        ChangeRotatingPlane_Forces()


                 
def ChangeMohrCircle():
    global glMohrP_Angle
    
    radius  = float(sqrt(pow(((glMohrNx-glMohrNz)/2),2)+pow(glMohrNxz,2)))
    centreX = float((glMohrNx+glMohrNz)/2)
    rleft_z = 0
    rleft_x = centreX-radius
    
    Mohr_Circle_source.data        = dict(x=[centreX], y=[0], radius=[radius])   
    OriginalPlane_line_source.data = dict(x=[rleft_x,glMohrNz,glMohrNz], y=[rleft_z,glMohrNxz,0])
  
    ## Calculate forces in rotated element
    Nzeta     = float(((glMohrNx+glMohrNz)/2)+(((glMohrNx-glMohrNz)/2)*cos(2*glMohrP_Angle))+glMohrNxz*sin(2*glMohrP_Angle))
    Neta      = float(((glMohrNx+glMohrNz)/2)-(((glMohrNx-glMohrNz)/2)*cos(2*glMohrP_Angle))-glMohrNxz*sin(2*glMohrP_Angle))
    Nzetaeta  = float((-(((glMohrNx-glMohrNz)/2)*sin(2*glMohrP_Angle)))+glMohrNxz*cos(2*glMohrP_Angle))

    if glMohrP_Angle == 0:
        Nzeta    = glMohrNx
        Neta     = glMohrNz
        Nzetaeta = glMohrNxz
    if glMohrP_Angle == (pi/2):
        Nzeta    = glMohrNz
        Neta     = glMohrNx
        Nzetaeta = -glMohrNxz


    Newplane_line_source.data       = dict(x=[rleft_x,Neta], y=[rleft_z,Nzetaeta])

    Figure2Moving_Label_source.data = dict(x=[glMohrNx,glMohrNz,0.0, 0.0, Neta,Nzeta,glMohrNz,Neta],
                                            y=[0.0,0.0,glMohrNxz, Nzetaeta,0.0,0.0,glMohrNxz,Nzetaeta],
                                            names=['\\sigma_x','\\sigma_z','\\tau_{xz}','\\tau_{\\overline{xz}}','\\sigma_{\\overline{z}}','\\sigma_{\\overline{x}}',"A","B"])
    
    Figure3Moving_Label_source.data = dict(x=[(25+2.5)*cos(-glMohrP_Angle)-1,(-25-2.5)*sin(glMohrP_Angle)-1],y=[(25+2.5)*sin(-glMohrP_Angle)-1,(-25-2.5)*cos(glMohrP_Angle)-1], 
                                        names = ['\\overline{x}', '\\overline{z}'])


    
def ChangeRotatingPlane_Forces():
    
    global glMohrP_Angle
    global glMohrNx,glMohrNz,glMohrNxz
    Nzeta    = float(float((glMohrNx+glMohrNz)/2)+(float((glMohrNx-glMohrNz)/2)*cos(2*glMohrP_Angle))+float(glMohrNxz*sin(2*glMohrP_Angle)))
    Neta     = float(float((glMohrNx+glMohrNz)/2)-(float((glMohrNx-glMohrNz)/2)*cos(2*glMohrP_Angle))-float(glMohrNxz*sin(2*glMohrP_Angle)))
    Nzetaeta = float((-(((glMohrNx-glMohrNz)/2)*sin(2*glMohrP_Angle)))+glMohrNxz*cos(2*glMohrP_Angle))
   
    glMohrP_Angle = -glMohrP_Angle

    ## Set Nzetaeta=0 if angle-slider is set to principal direction
    radius  = float(sqrt(pow(((glMohrNx-glMohrNz)/2),2)+pow(glMohrNxz,2)))
    centreX = float((glMohrNx+glMohrNz)/2)
    rleft_x = centreX-radius

    alpha_0 = 180*atan(glMohrNxz/(glMohrNz+(-rleft_x+0.00001)))/(pi)
    alpha_0 = int(alpha_0+0.5)

    alpharepetitions = [-90, -180, 0, 90, 180]
    for n in alpharepetitions:
        if alpha == alpha_0+n:
            Nzetaeta=0         
            break
    ## Set Nzeta = 0 if alpha equals value in list glMohrNzeta_zero_angles
    for m in glMohrNzeta_zero_angles: 
        if alpha == m:
            Nzeta = 0
            break
    ## Set Neta = 0 if alpha equals value in list glMohrNeta_zero_angles
    for m in glMohrNeta_zero_angles: 
        if alpha == m:
            Neta = 0
            break


    Nzeta = 0.75*Nzeta
    if Nzeta>0:
        NzetaP_arrow_source.data = dict(xS=[12.5*cos(glMohrP_Angle)],  xE=[(12.5+Nzeta)*cos(glMohrP_Angle)],  yS=[(12.5*sin(glMohrP_Angle))],   yE=[(((12.5+Nzeta)*sin(glMohrP_Angle)))],   lW = [2])
        NzetaN_arrow_source.data = dict(xS=[-12.5*cos(glMohrP_Angle)], xE=[(-12.5-Nzeta)*cos(glMohrP_Angle)], yS=[0-(12.5*sin(glMohrP_Angle))], yE=[(0-((12.5+Nzeta)*sin(glMohrP_Angle)))], lW = [2])
        
        
        NzetaP_rect_source.data  = dict(x=[(12.5*cos(glMohrP_Angle)+(12.5+Nzeta)*cos(glMohrP_Angle))/2],   y=[((12.5*sin(glMohrP_Angle))+(((12.5+Nzeta)*sin(glMohrP_Angle))))/2],   w=[Nzeta+1.5], h = [13], angle=[glMohrP_Angle])
        NzetaN_rect_source.data  = dict(x=[(-12.5*cos(glMohrP_Angle)+(-12.5-Nzeta)*cos(glMohrP_Angle))/2], y=[((-12.5*sin(glMohrP_Angle))+(-((12.5+Nzeta)*sin(glMohrP_Angle))))/2], w=[Nzeta+1.5], h = [13], angle=[glMohrP_Angle])

    elif Nzeta==0:
        NzetaP_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        NzetaN_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        
        NzetaP_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])
        NzetaN_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])

    else:
        NzetaP_arrow_source.data = dict(xS=[(12.5-Nzeta)*cos(glMohrP_Angle)],  xE=[12.5*cos(glMohrP_Angle)],   yS=[0+((12.5-Nzeta)*sin(glMohrP_Angle))],   yE=[0+(12.5*sin(glMohrP_Angle))], lW = [2])
        NzetaN_arrow_source.data = dict(xS=[(-12.5+Nzeta)*cos(glMohrP_Angle)], xE=[-12.5 *cos(glMohrP_Angle)], yS=[(0-((12.5-Nzeta)*sin(glMohrP_Angle)))], yE=[0-(12.5*sin(glMohrP_Angle))], lW = [2])
        
        NzetaP_rect_source.data  = dict(x=[(12.5*cos(glMohrP_Angle)+(12.5-Nzeta)*cos(glMohrP_Angle))/2],   y=[((12.5*sin(glMohrP_Angle))+(((12.5-Nzeta)*sin(glMohrP_Angle))))/2],   w=[Nzeta-1.5], h = [13], angle=[glMohrP_Angle])
        NzetaN_rect_source.data  = dict(x=[(-12.5*cos(glMohrP_Angle)+(-12.5+Nzeta)*cos(glMohrP_Angle))/2], y=[((-12.5*sin(glMohrP_Angle))+(-((12.5-Nzeta)*sin(glMohrP_Angle))))/2], w=[Nzeta-1.5], h = [13], angle=[glMohrP_Angle])

    Neta = 0.75*Neta
    if Neta>0:
        NetaP_arrow_source.data = dict(xS=[12.5*cos((pi/2)+glMohrP_Angle)], xE=[(12.5+Neta)*cos((pi/2)+glMohrP_Angle)], yS=[(12.5*sin((pi/2)+glMohrP_Angle))], yE=[((12.5+Neta)*sin((pi/2)+glMohrP_Angle))], lW = [2])
        NetaN_arrow_source.data = dict(xS=[12.5*sin(glMohrP_Angle)],        xE=[(12.5+Neta)*sin(glMohrP_Angle)],        yS=[-(12.5*cos(glMohrP_Angle))],       yE=[-((12.5+Neta)*cos(glMohrP_Angle))],       lW = [2]) 
        
        NetaP_rect_source.data  = dict(x=[(12.5*cos((pi/2)+glMohrP_Angle)+(12.5+Neta)*cos((pi/2)+glMohrP_Angle))/2], y=[((12.5*sin((pi/2)+glMohrP_Angle))+((12.5+Neta)*sin((pi/2)+glMohrP_Angle)))/2], h=[Neta+1.5], w = [13], angle=[glMohrP_Angle])
        NetaN_rect_source.data  = dict(x=[(12.5*sin(glMohrP_Angle)+(12.5+Neta)*sin(glMohrP_Angle))/2],               y=[(-(12.5*cos(glMohrP_Angle))+-((12.5+Neta)*cos(glMohrP_Angle)))/2],             h=[Neta+1.5], w = [13], angle=[glMohrP_Angle])

    elif Neta==0:
        NetaP_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        NetaN_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        
        NetaP_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])
        NetaN_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])

    else:
        NetaP_arrow_source.data = dict(xS=[(12.5-Neta)*cos((pi/2)+glMohrP_Angle)],xE=[12.5*cos((pi/2)+glMohrP_Angle)], yS=[((12.5-Neta)*sin((pi/2)+glMohrP_Angle))], yE=[0+(12.5*sin((pi/2)+glMohrP_Angle))],  lW = [2])
        NetaN_arrow_source.data = dict(xS=[(12.5-Neta)*sin(glMohrP_Angle)],xE=[12.5*sin(glMohrP_Angle)],               yS=[-(12.5-Neta)*cos(glMohrP_Angle)],         yE=[-12.5*cos(glMohrP_Angle)],            lW = [2])      
        
        NetaP_rect_source.data  = dict(x=[((12.5-Neta)*cos((pi/2)+glMohrP_Angle)+12.5*cos((pi/2)+glMohrP_Angle))/2], y=[(((12.5-Neta)*sin((pi/2)+glMohrP_Angle))+0+(12.5*sin((pi/2)+glMohrP_Angle)))/2], h=[Neta-1.5], w = [13], angle=[glMohrP_Angle])
        NetaN_rect_source.data  = dict(x=[((12.5-Neta)*sin(glMohrP_Angle)+12.5*sin(glMohrP_Angle))/2],               y=[(-(12.5-Neta)*cos(glMohrP_Angle)+-12.5*cos(glMohrP_Angle))/2],                   h=[Neta-1.5], w = [13], angle=[glMohrP_Angle])


    Nzetaeta=0.75*Nzetaeta
    if Nzetaeta>0:
        Nzetaeta1_arrow_source.data = dict(xS=[9*cos(glMohrP_Angle)+((Nzetaeta/2)*sin(glMohrP_Angle))],  xE=[9*cos(glMohrP_Angle)-((Nzetaeta/2)*sin(glMohrP_Angle))],  yS=[(0+9*sin(glMohrP_Angle))-((Nzetaeta/2)*cos(glMohrP_Angle))], yE=[(0+9*sin(glMohrP_Angle))+((Nzetaeta/2)*cos(glMohrP_Angle))], lW = [2])
        Nzetaeta2_arrow_source.data = dict(xS=[-9*sin(glMohrP_Angle)-((Nzetaeta/2)*cos(glMohrP_Angle))], xE=[-9*sin(glMohrP_Angle)+((Nzetaeta/2)*cos(glMohrP_Angle))], yS=[(0+9*cos(glMohrP_Angle))-((Nzetaeta/2)*sin(glMohrP_Angle))], yE=[(0+9*cos(glMohrP_Angle))+((Nzetaeta/2)*sin(glMohrP_Angle))], lW = [2])
        Nzetaeta3_arrow_source.data = dict(xS=[-9*cos(glMohrP_Angle)-((Nzetaeta/2)*sin(glMohrP_Angle))], xE=[-9*cos(glMohrP_Angle)+((Nzetaeta/2)*sin(glMohrP_Angle))], yS=[(0-9*sin(glMohrP_Angle))+((Nzetaeta/2)*cos(glMohrP_Angle))], yE=[(0-9*sin(glMohrP_Angle))-((Nzetaeta/2)*cos(glMohrP_Angle))], lW = [2])
        Nzetaeta4_arrow_source.data = dict(xS=[9*sin(glMohrP_Angle)+((Nzetaeta/2)*cos(glMohrP_Angle))],  xE=[9*sin(glMohrP_Angle)-((Nzetaeta/2)*cos(glMohrP_Angle))],  yS=[(0-9*cos(glMohrP_Angle))+((Nzetaeta/2)*sin(glMohrP_Angle))], yE=[(0-9*cos(glMohrP_Angle))-((Nzetaeta/2)*sin(glMohrP_Angle))], lW = [2])
        
        
        Nzetaeta1_rect_source.data  = dict(x=[(9*cos(glMohrP_Angle)+((Nzetaeta/2)*sin(glMohrP_Angle))+9*cos(glMohrP_Angle)-((Nzetaeta/2)*sin(glMohrP_Angle)))/2],   y=[((0+9*sin(glMohrP_Angle))-((Nzetaeta/2)*cos(glMohrP_Angle))+(0+9*sin(glMohrP_Angle))+((Nzetaeta/2)*cos(glMohrP_Angle)))/2], w=[0.3*Nzetaeta+.5], h = [13], angle=[glMohrP_Angle])
        Nzetaeta2_rect_source.data  = dict(x=[(-9*sin(glMohrP_Angle)-((Nzetaeta/2)*cos(glMohrP_Angle))+-9*sin(glMohrP_Angle)+((Nzetaeta/2)*cos(glMohrP_Angle)))/2], y=[((0+9*cos(glMohrP_Angle))-((Nzetaeta/2)*sin(glMohrP_Angle))+(0+9*cos(glMohrP_Angle))+((Nzetaeta/2)*sin(glMohrP_Angle)))/2], h=[0.3*Nzetaeta+.5], w = [13], angle=[glMohrP_Angle])
        Nzetaeta3_rect_source.data  = dict(x=[(-9*cos(glMohrP_Angle)-((Nzetaeta/2)*sin(glMohrP_Angle))-9*cos(glMohrP_Angle)+((Nzetaeta/2)*sin(glMohrP_Angle)))/2],  y=[((0-9*sin(glMohrP_Angle))+((Nzetaeta/2)*cos(glMohrP_Angle))+(0-9*sin(glMohrP_Angle))-((Nzetaeta/2)*cos(glMohrP_Angle)))/2], w=[0.3*Nzetaeta+.5], h = [13], angle=[glMohrP_Angle])
        Nzetaeta4_rect_source.data  = dict(x=[(9*sin(glMohrP_Angle)+((Nzetaeta/2)*cos(glMohrP_Angle))+9*sin(glMohrP_Angle)-((Nzetaeta/2)*cos(glMohrP_Angle)))/2],   y=[((0-9*cos(glMohrP_Angle))+((Nzetaeta/2)*sin(glMohrP_Angle))+(0-9*cos(glMohrP_Angle))-((Nzetaeta/2)*sin(glMohrP_Angle)))/2], h=[0.3*Nzetaeta+.5], w = [13], angle=[glMohrP_Angle])

    elif Nzetaeta==0:
        Nzetaeta1_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        Nzetaeta2_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        Nzetaeta3_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        Nzetaeta4_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
       
        Nzetaeta1_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])
        Nzetaeta2_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])
        Nzetaeta3_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])
        Nzetaeta4_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])
       

    else:
        Nzetaeta1_arrow_source.data = dict(xS=[9*cos(glMohrP_Angle)+((Nzetaeta/2)*sin(glMohrP_Angle))],  xE=[9*cos(glMohrP_Angle)-((Nzetaeta/2)*sin(glMohrP_Angle))],  yS=[(0+9*sin(glMohrP_Angle))-((Nzetaeta/2)*cos(glMohrP_Angle))], yE=[(0+9*sin(glMohrP_Angle))+((Nzetaeta/2)*cos(glMohrP_Angle))], lW = [2])
        Nzetaeta2_arrow_source.data = dict(xS=[-9*sin(glMohrP_Angle)-((Nzetaeta/2)*cos(glMohrP_Angle))], xE=[-9*sin(glMohrP_Angle)+((Nzetaeta/2)*cos(glMohrP_Angle))], yS=[(0+9*cos(glMohrP_Angle))-((Nzetaeta/2)*sin(glMohrP_Angle))], yE=[(0+9*cos(glMohrP_Angle))+((Nzetaeta/2)*sin(glMohrP_Angle))], lW = [2])
        Nzetaeta3_arrow_source.data = dict(xS=[-9*cos(glMohrP_Angle)-((Nzetaeta/2)*sin(glMohrP_Angle))], xE=[-9*cos(glMohrP_Angle)+((Nzetaeta/2)*sin(glMohrP_Angle))], yS=[(0-9*sin(glMohrP_Angle))+((Nzetaeta/2)*cos(glMohrP_Angle))], yE=[(0-9*sin(glMohrP_Angle))-((Nzetaeta/2)*cos(glMohrP_Angle))], lW = [2])
        Nzetaeta4_arrow_source.data = dict(xS=[9*sin(glMohrP_Angle)+((Nzetaeta/2)*cos(glMohrP_Angle))],  xE=[9*sin(glMohrP_Angle)-((Nzetaeta/2)*cos(glMohrP_Angle))],  yS=[(0-9*cos(glMohrP_Angle))+((Nzetaeta/2)*sin(glMohrP_Angle))], yE=[(0-9*cos(glMohrP_Angle))-((Nzetaeta/2)*sin(glMohrP_Angle))], lW = [2])

        Nzetaeta1_rect_source.data  = dict(x=[(9*cos(glMohrP_Angle)+((Nzetaeta/2)*sin(glMohrP_Angle))+9*cos(glMohrP_Angle)-((Nzetaeta/2)*sin(glMohrP_Angle)))/2],   y=[((0+9*sin(glMohrP_Angle))-((Nzetaeta/2)*cos(glMohrP_Angle))+(0+9*sin(glMohrP_Angle))+((Nzetaeta/2)*cos(glMohrP_Angle)))/2], w=[0.3*Nzetaeta-.5], h = [13], angle=[glMohrP_Angle])
        Nzetaeta2_rect_source.data  = dict(x=[(-9*sin(glMohrP_Angle)-((Nzetaeta/2)*cos(glMohrP_Angle))+-9*sin(glMohrP_Angle)+((Nzetaeta/2)*cos(glMohrP_Angle)))/2], y=[((0+9*cos(glMohrP_Angle))-((Nzetaeta/2)*sin(glMohrP_Angle))+(0+9*cos(glMohrP_Angle))+((Nzetaeta/2)*sin(glMohrP_Angle)))/2], h=[0.3*Nzetaeta-.5], w = [13], angle=[glMohrP_Angle])
        Nzetaeta3_rect_source.data  = dict(x=[(-9*cos(glMohrP_Angle)-((Nzetaeta/2)*sin(glMohrP_Angle))-9*cos(glMohrP_Angle)+((Nzetaeta/2)*sin(glMohrP_Angle)))/2],  y=[((0-9*sin(glMohrP_Angle))+((Nzetaeta/2)*cos(glMohrP_Angle))+(0-9*sin(glMohrP_Angle))-((Nzetaeta/2)*cos(glMohrP_Angle)))/2], w=[0.3*Nzetaeta-.5], h = [13], angle=[glMohrP_Angle])
        Nzetaeta4_rect_source.data  = dict(x=[(9*sin(glMohrP_Angle)+((Nzetaeta/2)*cos(glMohrP_Angle))+9*sin(glMohrP_Angle)-((Nzetaeta/2)*cos(glMohrP_Angle)))/2],   y=[((0-9*cos(glMohrP_Angle))+((Nzetaeta/2)*sin(glMohrP_Angle))+(0-9*cos(glMohrP_Angle))-((Nzetaeta/2)*sin(glMohrP_Angle)))/2], h=[0.3*Nzetaeta-.5], w = [13], angle=[glMohrP_Angle])

    glMohrP_Angle=-glMohrP_Angle


   

### Figure 1, Define Geometry:
NxP_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NxP_arrow_source,line_color="#E37222")
NxN_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NxN_arrow_source,line_color="#E37222")
NzP_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NzP_arrow_source,line_color="#E37222")
NzN_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NzN_arrow_source,line_color="#E37222")
Nxz1_arrow_glyph = Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nxz1_arrow_source,line_color="#0065BD")
Nxz2_arrow_glyph = Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nxz2_arrow_source,line_color="#0065BD")
Nxz3_arrow_glyph = Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nxz3_arrow_source,line_color="#0065BD")
Nxz4_arrow_glyph = Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nxz4_arrow_source,line_color="#0065BD")
### Figure 1, Rectangle glyphs:
NxP_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#E37222", fill_alpha=0.5)
NxN_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#E37222", fill_alpha=0.5)
NzP_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#E37222", fill_alpha=0.5)
NzN_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#E37222", fill_alpha=0.5)
Nxz1_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#0065BD", fill_alpha=0.5)
Nxz2_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#0065BD", fill_alpha=0.5)
Nxz3_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#0065BD", fill_alpha=0.5)
Nxz4_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#0065BD", fill_alpha=0.5)

### Figure 1, Define Figure and add Geometry:
figure1 = figure(title="Stress State A", tools="save", x_range=(-30,30), y_range=(-30,30),width=400,height=400, logo=None)
figure1.square([0], [0], size=75, color="black", alpha=0.5)
figure1.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=0, y_start=0, x_end=25, y_end=0))
figure1.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=0, y_start=0, x_end=0, y_end=-25))
figure1.add_layout(NxP_arrow_glyph)
figure1.add_layout(NxN_arrow_glyph)
figure1.add_layout(NzP_arrow_glyph)
figure1.add_layout(NzN_arrow_glyph)
figure1.add_layout(Nxz1_arrow_glyph)
figure1.add_layout(Nxz2_arrow_glyph)
figure1.add_layout(Nxz3_arrow_glyph)
figure1.add_layout(Nxz4_arrow_glyph)

figure1_labels = LatexLabelSet(x='x', y='y', text='names', level='glyph',
                                x_offset=0, y_offset=0, source=Figure1Perm_Label_source)

figure1.add_layout(figure1_labels)
figure1.add_glyph(NxP_rect_source,NxP_rect_glyph)
figure1.add_glyph(NxN_rect_source,NxN_rect_glyph)
figure1.add_glyph(NzP_rect_source,NzP_rect_glyph)
figure1.add_glyph(NzN_rect_source,NzN_rect_glyph)
figure1.add_glyph(Nxz1_rect_source,Nxz1_rect_glyph)
figure1.add_glyph(Nxz2_rect_source,Nxz1_rect_glyph)
figure1.add_glyph(Nxz3_rect_source,Nxz1_rect_glyph)
figure1.add_glyph(Nxz4_rect_source,Nxz1_rect_glyph)

# dummy glyphs for the legend entries
figure1.square([0.0],[0.0],size=0,fill_color="#E37222",fill_alpha=0.5,legend="Normal Stresses")
figure1.square([0.0],[0.0],size=0,fill_color="#0065BD",fill_alpha=0.5,legend="Shear Stresses")
figure1.legend.location = 'top_left'


### Figure 2: Define Geometry
Mohr_Circle_glyph = Circle(x='x',y='y',radius='radius', radius_dimension='y', fill_color='#c3c3c3', fill_alpha=0.5)
Wedge_glyph = Wedge(x="x", y="y", radius="radius", start_angle="sA", end_angle="eA", fill_color="firebrick", fill_alpha=0.6, direction="clock")
### Figure 2: Define Figure and add Geometry
figure2 = figure(title="Mohr's Circle", tools="pan,save,wheel_zoom,reset", x_range=(-18.5,18.5), y_range=(-18.5,18.5),width=400,height=400, logo=None, toolbar_location="right")
figure2.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=-17, y_start=0, x_end=17, y_end=0))
figure2.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=0, y_start=-17, x_end=0, y_end=17))
figure2.add_glyph(Mohr_Circle_source,Mohr_Circle_glyph)
figure2.add_glyph(Wedge_source,Wedge_glyph)
# Modified line
figure2.line(x='x',y='y',source= Newplane_line_source, color="#A2AD00", line_width=3, line_join = 'bevel')
figure2.circle(x='x',y='y',source= Newplane_line_source, size=4, color="black", alpha=0.4)
figure2.circle(x='x', y='y', source=Figure2Moving_Label_source, size=5, color="black")
figure2.circle(x='x', y='y', source=Figure2Show_Label_source, size=5, color="firebrick")
figure2_labels1 = LatexLabelSet(x='x', y='y', text='names', level='glyph',
              x_offset=0, y_offset=0, source=Figure2Perm_Label_source)
figure2_labels2 = LatexLabelSet(x='x', y='y', text='names', source=Figure2Moving_Label_source, text_color = 'black', level='glyph', x_offset=3, y_offset=3)
figure2_labels3 = LatexLabelSet(x='x', y='y', text='names', source=Figure2Show_Label_source, text_color = 'firebrick', level='glyph', x_offset=3, y_offset=-15)
figure2.add_layout(figure2_labels1)
figure2.add_layout(figure2_labels2)
figure2.add_layout(figure2_labels3)
# Original line
figure2.line(x='x',y='y',source= OriginalPlane_line_source, color="black", alpha=0.5, line_width=3, line_join = 'bevel')
figure2.circle(x='x',y='y',source= OriginalPlane_line_source, size=4, color="black", alpha=0.4)
global glMohrFigure2_angle_label
glMohrFigure2_angle_label = LatexLabel(text="",x=20,y=330,render_mode='css',text_color='firebrick', x_units='screen', y_units='screen')
figure2.add_layout(glMohrFigure2_angle_label)

### Figure 3: Define Geometry
Rotating_Plane_glyph = Square(x='x',y='y',angle='angle',size='size', fill_color = '#A2AD00', fill_alpha=0.5)
Rotating_Plane_red_glyph = Square(x='x',y='y',angle='angle',size='size', fill_color = 'firebrick', fill_alpha=0.5)

Rotating_Axis_X_glyph = Arrow(end=NormalHead(fill_color='#A2AD00', size=15), x_start='xS', y_start='yS', x_end='xE', y_end='yE', source=Rotating_Axis_X_source )
Rotating_Axis_Y_glyph = Arrow(end=NormalHead(fill_color='#A2AD00', size=15), x_start='xS', y_start='yS', x_end='xE', y_end='yE', source=Rotating_Axis_Y_source )

NzetaP_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NzetaP_arrow_source,line_color="#E37222")
NzetaN_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NzetaN_arrow_source,line_color="#E37222")
NetaP_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NetaP_arrow_source,line_color="#E37222")
NetaN_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NetaN_arrow_source,line_color="#E37222")
Nzetaeta1_arrow_glyph= Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nzetaeta1_arrow_source,line_color="#0065BD")
Nzetaeta2_arrow_glyph=Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nzetaeta2_arrow_source,line_color="#0065BD")
Nzetaeta3_arrow_glyph= Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nzetaeta3_arrow_source,line_color="#0065BD")
Nzetaeta4_arrow_glyph=Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nzetaeta4_arrow_source,line_color="#0065BD")
### Figure 3, Rectangle glyphs:
NzetaP_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#E37222", fill_alpha=0.5)
NzetaN_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#E37222", fill_alpha=0.5)
NetaP_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#E37222", fill_alpha=0.5)
NetaN_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#E37222", fill_alpha=0.5)
Nzetaeta1_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#0065BD", fill_alpha=0.5)
Nzetaeta2_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#0065BD", fill_alpha=0.5)
Nzetaeta3_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#0065BD", fill_alpha=0.5)
Nzetaeta4_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#0065BD", fill_alpha=0.5)
### Figure 3, Define Figure and add Geometry:
figure3 = figure(title="Stress State B", tools="save", x_range=(-30,30), y_range=(-30,30),width=400,height=400, logo=None)
figure3.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=0, y_start=0, x_end=25, y_end=0))
figure3.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=0, y_start=0, x_end=0, y_end=-25))
figure3_labels = LatexLabelSet(x='x', y='y', text='names', level='glyph', x_offset=5, y_offset=5, source=Figure1Perm_Label_source)
figure3_labels2 = LatexLabelSet(x='x', y='y', text='names', source=Figure3Moving_Label_source)

figure3.add_layout(figure3_labels)
figure3.add_layout(figure3_labels2)
figure3.add_layout(NzetaP_arrow_glyph)
figure3.add_layout(NzetaN_arrow_glyph)
figure3.add_layout(NetaP_arrow_glyph)
figure3.add_layout(NetaN_arrow_glyph)
figure3.add_layout(Nzetaeta1_arrow_glyph)
figure3.add_layout(Nzetaeta2_arrow_glyph)
figure3.add_layout(Nzetaeta3_arrow_glyph)
figure3.add_layout(Nzetaeta4_arrow_glyph)
figure3.add_glyph(Rotating_Plane_source,Rotating_Plane_glyph)
figure3.add_glyph(Rotating_Plane_red_source,Rotating_Plane_red_glyph)
figure3.add_glyph(NzetaP_rect_source,NzetaP_rect_glyph)
figure3.add_glyph(NzetaN_rect_source,NzetaN_rect_glyph)
figure3.add_glyph(NetaP_rect_source,NetaP_rect_glyph)
figure3.add_glyph(NetaN_rect_source,NetaN_rect_glyph)
figure3.add_glyph(Nzetaeta1_rect_source,Nzetaeta1_rect_glyph)
figure3.add_glyph(Nzetaeta2_rect_source,Nzetaeta2_rect_glyph)
figure3.add_glyph(Nzetaeta3_rect_source,Nzetaeta3_rect_glyph)
figure3.add_glyph(Nzetaeta4_rect_source,Nzetaeta4_rect_glyph)
figure3.add_layout(Rotating_Axis_X_glyph)
figure3.add_layout(Rotating_Axis_Y_glyph)

figure3.square([0.0],[0.0],size=0,fill_color="#E37222",fill_alpha=0.5,legend="Normal Stresses")
figure3.square([0.0],[0.0],size=0,fill_color="#0065BD",fill_alpha=0.5,legend="Shear Stresses")
figure3.legend.location = 'top_left'

### All figures, Turn off grids: 
figure1.xaxis.major_tick_line_color=None
figure1.xaxis.major_label_text_color=None
figure1.xaxis.minor_tick_line_color=None
figure1.xaxis.axis_line_color=None
figure1.yaxis.major_tick_line_color=None
figure1.yaxis.major_label_text_color=None
figure1.yaxis.minor_tick_line_color=None
figure1.yaxis.axis_line_color=None
figure1.xgrid.visible = False
figure1.ygrid.visible = False

figure2.xaxis.major_tick_line_color=None
figure2.xaxis.major_label_text_color=None
figure2.xaxis.minor_tick_line_color=None
figure2.xaxis.axis_line_color=None
figure2.yaxis.major_tick_line_color=None
figure2.yaxis.major_label_text_color=None
figure2.yaxis.minor_tick_line_color=None
figure2.yaxis.axis_line_color=None
figure2.xgrid.visible = False
figure2.ygrid.visible = False

figure3.xaxis.major_tick_line_color=None
figure3.xaxis.major_label_text_color=None
figure3.xaxis.minor_tick_line_color=None
figure3.xaxis.axis_line_color=None
figure3.yaxis.major_tick_line_color=None
figure3.yaxis.major_label_text_color=None
figure3.yaxis.minor_tick_line_color=None
figure3.yaxis.axis_line_color=None
figure3.xgrid.visible = False
figure3.ygrid.visible = False


### Create  sliders to change Normal and Tangential Forces
Normal_X_slider= Slider(title=u"\u03C3"u"\u0078",value= 0,start = -10, end = 10, step = 0.5)
Normal_X_slider.on_change('value',NormalForceX_init)

    
Normal_Z_slider= Slider(title=u"\u03C3"u"\u007A",value= 0,start = -10, end = 10, step = 0.5)
Normal_Z_slider.on_change('value',NormalForceZ_init)
   
Tangential_XZ_slider= Slider(title=u"\u03C4"u"\u0078"u"\u007A",value= 0,start = 0, end = 10, step = 0.5)
Tangential_XZ_slider.on_change('value',TangentialXZ_init)
    
Plane_Angle_slider= Slider(title= u"\u03B1",value= 0,start = -180, end = 180, step = 1)
Plane_Angle_slider.on_change('value',changePlaneAngle)
Plane_Angle_slider.disabled = True


###Create Reset Button:
reset_button = Button(label="Reset", button_type="success")
reset_button.on_click(reset)


###Create Draw Button:
draw_button = Button(label="Draw", button_type="success")
draw_button.on_click(draw)

###Create Show Button:
show_button = Button(label="Show/Hide principal stress + direction", button_type="success")
show_button.on_click(show)


### Initialising all column data for the initial plot
init()

### Add description from HTML file
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1140)

### Arrange layout
doc_layout = layout(children=[column(
    row(Spacer(height=200,width=18),description),
    row(Spacer(height=30)),
    row(column(figure1,row(Spacer(height=10,width=50),column(Normal_X_slider,Normal_Z_slider,Tangential_XZ_slider))),column(figure2,row(Spacer(height=10,width=50),column(draw_button,show_button,reset_button))),column(figure3, row(Spacer(height=10,width=50),Plane_Angle_slider))))])
curdoc().add_root(doc_layout)
curdoc().title = "Mohr Circle"

