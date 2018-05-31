# -*- coding: utf-8 -*-
"""
Created on Fr,18.05.2018

@author: Sascha Kubisch
"""

"""
Python Bokeh program which explains the concept of Mohr cirlce interactively

"""
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource,Slider,Div,Arrow,OpenHead,NormalHead,LabelSet,Button
from bokeh.models.markers import Square,Circle
from bokeh.models.glyphs import Ellipse,Wedge,Rect
from bokeh.io import curdoc
from os.path import dirname, join
from math import pi,sqrt,pow,sin,cos,atan


### Initial Values
radius = 10
centreX = 10
Nx =0
Nz =0
Nxz =0
P_Angle = 0*(pi/180)
Neta =0 
Nzeta =0 
Nzetaeta =0  
rleft_x = centreX-radius
rleft_z=0

global changeNx
changeNx    = 1 

global changeNz
changeNz    = 1

global changeNxz
changeNxz   = 1

global changeAngle
changeAngle = 0

global changeShow
changeShow  = 0


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


##Figure 2, Mohr Circle:
Newplane_line_source      = ColumnDataSource(data=dict(x=[],y=[]))
OriginalPlane_line_source = ColumnDataSource(data=dict(x=[],y=[]))


##Figure 3, Rotating plane: 
Rotating_Plane_source     = ColumnDataSource(data=dict(x=[], y=[],angle = [],size =[]))
Rotating_Plane_red_source = ColumnDataSource(data=dict(x=[], y=[],angle = [],size =[]))
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
Figure2Perm_Label_source   = ColumnDataSource(data=dict(x=[20.5,-3.5], y=[-3, 18], names=[u"\u03C3", u"\u03C4"]))
Figure2Moving_Label_source = ColumnDataSource(data=dict(x=[], y=[], names=[]))
Figure2Show_Label_source   = ColumnDataSource(data=dict(x=[], y=[], names=[]))
Figure3Perm_Label_source   = ColumnDataSource(data=dict(x=[22,1], y=[-5, -27], names=['x', 'z']))


### Figure 2: Data structures
Mohr_Circle_source = ColumnDataSource(data=dict(x=[], y=[], radius=[]))
Wedge_source       = ColumnDataSource(data=dict(x=[], y=[],radius=[], sA=[], eA=[]))

###Initial Calculations and Value settings
def init():
    P_Angle = 0*(pi/180)
    radius = 10
    centreX = 10
    Nx =0
    Nz =0
    Nxz =0
    Neta =0 
    Nzeta =0 
    Nzetaeta =0  
    rleft_x=centreX-radius
    rleft_z=0
    
    ## Calculations
    radius   = float(sqrt(pow(((Nx-Nz)/2),2)+pow(Nxz,2)))
    centreX  = float((Nx+Nz)/2)
    Nzeta    = float(((Nx+Nz)/2)+(((Nx-Nz)/2)*cos(2*P_Angle))+Nxz*sin(2*P_Angle))
    Neta     = float(((Nx+Nz)/2)-(((Nx-Nz)/2)*cos(2*P_Angle))-Nxz*sin(2*P_Angle))
    Nzetaeta = float((-(((Nx-Nz)/2)*sin(2*P_Angle)))+Nxz*cos(2*P_Angle))

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

    global changeNx
    changeNx    = 1

    global changeNz
    changeNz    = 1

    global changeNxz
    changeNxz   = 1

    global changeAngle
    changeAngle = 0

    global changeShow
    changeShow  = 0

    
    P_Angle = 0*(pi/180)
    radius = 10
    centreX = 10
    Nx =0
    Nz =0
    Nxz =0
    Neta =0 
    Nzeta =0 
    Nzetaeta =0  
    rleft_x=centreX-radius
    rleft_z=0
    
    ### Calculations
    radius    = float(sqrt(pow(((Nx-Nz)/2),2)+pow(Nxz,2)))
    centreX   = float((Nx+Nz)/2)
    Nzeta     = float(((Nx+Nz)/2)+(((Nx-Nz)/2)*cos(2*P_Angle))+Nxz*sin(2*P_Angle))
    Neta      = float(((Nx+Nz)/2)-(((Nx-Nz)/2)*cos(2*P_Angle))-Nxz*sin(2*P_Angle))
    Nzetaeta  = float((-(((Nx-Nz)/2)*sin(2*P_Angle)))+Nxz*cos(2*P_Angle))

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


    ## Figure 3, Reset rotating plane:
    Rotating_Plane_source.data     = dict(x=[], y=[],angle =[],size = [])
    Rotating_Plane_red_source.data = dict(x=[], y=[],angle =[],size = [])
    ## Figure 3, Reset Arrows:
    NzetaP_arrow_source.data    = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    NzetaN_arrow_source.data    = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    NetaP_arrow_source.data     = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    NetaN_arrow_source.data     = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nzetaeta1_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nzetaeta2_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nzetaeta3_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nzetaeta4_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    ## Figure 3, Reset Rectangles:
    NzetaP_rect_source.data    = dict(x=[], y=[], w=[], h=[], angle=[])
    NzetaN_rect_source.data    = dict(x=[], y=[], w=[], h=[], angle=[])
    NetaP_rect_source.data     = dict(x=[], y=[], w=[], h=[], angle=[])
    NetaN_rect_source.data     = dict(x=[], y=[], w=[], h=[], angle=[])
    Nzetaeta1_rect_source.data = dict(x=[], y=[], w=[], h=[], angle=[])
    Nzetaeta2_rect_source.data = dict(x=[], y=[], w=[], h=[], angle=[])
    Nzetaeta3_rect_source.data = dict(x=[], y=[], w=[], h=[], angle=[])
    Nzetaeta4_rect_source.data = dict(x=[], y=[], w=[], h=[], angle=[])





    
def show():
    
    if changeShow == 1:
        global P_Angle
        radius   = float(sqrt(pow(((Nx-Nz)/2),2)+pow(Nxz,2)))
        centreX  = float((Nx+Nz)/2)
        rleft_z  = 0
        rleft_x  = centreX-radius
        rright_x = centreX+radius
    

  
        ## Calculate forces in rotated element
        Nzeta    = float(((Nx+Nz)/2)+(((Nx-Nz)/2)*cos(2*P_Angle))+Nxz*sin(2*P_Angle))
        Neta     = float(((Nx+Nz)/2)-(((Nx-Nz)/2)*cos(2*P_Angle))-Nxz*sin(2*P_Angle))
        Nzetaeta = float((-(((Nx-Nz)/2)*sin(2*P_Angle)))+Nxz*cos(2*P_Angle))
        if P_Angle == 0:
            Nzeta    = Nx
            Neta     = Nz
            Nzetaeta = Nxz
        if P_Angle == (pi/2):
            Nzeta    = Nz
            Neta     = Nx
            Nzetaeta = -Nxz

        ## Print Labels for principal stress and direction
        alpha=180*atan(Nxz/(Nz+(-rleft_x+0.00001)))/(pi)
        alpha=int(alpha+0.5)
        Figure2Show_Label_source.data = dict(x=[rleft_x-3,rright_x+0.5,rleft_x-0.7,rright_x-0.5,-22,-19,centreX+0.5,centreX-0.5],y=[0,0,-1.1,-1.1,15,15,0,-1.1], names =[u"\u03C3"u"\u2082",u"\u03C3"u"\u2081","x","x",u"\u03B1"u"\u2080","=" + str(alpha) + "°",u"\u03C3"u"\u2098","x"])
        Wedge_source.data=dict(x=[rleft_x], y=[0],radius=[radius/2], sA=[atan(Nxz/(Nz+(-rleft_x)))], eA=[0])
        Wedge_glyph = Wedge(x="x", y="y", radius="radius", start_angle="sA", end_angle="eA", fill_color="firebrick", fill_alpha=0.6, direction="clock")



def draw():

    global changeNx
    changeNx = 0

    global Nxfix
    Nxfix = Nx

    global changeNz
    changeNz = 0

    global Nzfix
    Nzfix = Nz

    global changeNxz
    changeNxz = 0

    global Nxzfix
    Nxzfix = Nxz

    global changeAngle
    changeAngle = 1

    global changeShow
    changeShow  = 1


    ## Calculations
    radius    = float(sqrt(pow(((Nx-Nz)/2),2)+pow(Nxz,2)))
    centreX   = float((Nx+Nz)/2)
    Nzeta     = float(((Nx+Nz)/2)+(((Nx-Nz)/2)*cos(2*P_Angle))+Nxz*sin(2*P_Angle))
    Neta      = float(((Nx+Nz)/2)-(((Nx-Nz)/2)*cos(2*P_Angle))-Nxz*sin(2*P_Angle))
    Nzetaeta  = float((-(((Nx-Nz)/2)*sin(2*P_Angle)))+Nxz*cos(2*P_Angle))

    ## Figure 2 
    Mohr_Circle_source.data = dict(x=[centreX], y=[0], radius=[radius])
    Wedge_source.data       = dict(x=[], y=[],radius=[], sA=[], eA=[])

    Newplane_line_source.data       = dict(x=[rleft_x,Neta,Neta], y=[rleft_z,Nzetaeta,0])
    OriginalPlane_line_source.data  = dict(x=[rleft_x,Nz,Nz], y=[rleft_z,Nxz,0])
    Figure2Moving_Label_source.data = dict(x=[Nx,Nz,-4,Nx-0.5,Nz-0.5,-0.5,Nz,Neta+1.5],y=[-3,-3,Nxz-1,-1.1,-1.1,Nxz-1.2,Nxz,Nzetaeta],
                                           names =[u"\u03C3"u"\u0078",u"\u03C3"u"\u007A",u"\u03C4"u"\u0078"u"\u007A","x","x","-","A","B"])
    Figure2Show_Label_source.data   = dict(x=[],y=[], names =[])
  
    ## Figure 3, Rotating plane:
    Rotating_Plane_source.data = dict(x=[0], y=[0],angle =[-P_Angle],size = [75])
    
    NzetaP_arrow_source.data    = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    NzetaN_arrow_source.data    = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    NetaP_arrow_source.data     = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    NetaN_arrow_source.data     = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nzetaeta1_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nzetaeta2_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nzetaeta3_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nzetaeta4_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    
    ##Figure 1, Draw Nx and keep it until reset() ist called:
    new = Nx
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
    

    ##Figure 1, Draw Nz and keep it until reset() ist called:
    new = Nz
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
         
          
    new = Nxz
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



    
    ChangeRotatingPlane_Forces()
    ChangeMohrCircle()


def NormalForceX_init(attr,old,new):

    ## Figure 1, Present the Normal Forces while Draw-Button wasn't yet activated:  
    if changeNx == 1:
        ## Global change of Nx
        global Nx
        Nx = new 
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

    ## Freeze the Value of the Slider once the Draw-Button was hit:
    if changeNx == 0:
        Normal_X_slider.value = Nxfix
         
        
           
    #ChangeMohrCircle()
    #ChangeRotatingPlane_Forces()
    
def NormalForceZ_init(attr,old,new):

    ## Figure 1, Present the Normal Forces while Draw-Button wasn't yet activated:
    if changeNz == 1:

        ## Global change of Nz
        global Nz   
        Nz = new
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

    ## Freeze the Value of the Slider once the Draw-Button was hit:
    if changeNz == 0:
        Normal_Z_slider.value = Nzfix

    
    #ChangeMohrCircle()
    #ChangeRotatingPlane_Forces()
    
def TangentialXZ_init(attr,old,new):

    ## Figure 1, Present the Shear Forces while Draw-Button wasn't yet activated:
    if changeNxz == 1:

        ## global change of Nxz    
        global Nxz     
        Nxz = new
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

    ## Freeze the Value of the Slider once the Draw-Button was hit:
    if changeNxz == 0:
        Tangential_XZ_slider.value = Nxzfix

    
    #ChangeMohrCircle()
    #ChangeRotatingPlane_Forces()
        
def changePlaneAngle(attr,old,new):

     if changeAngle == 1:

        global P_Angle
        alpha= new
        P_Angle = -new*(pi/180)


        ## Paint Rotating Plane red if angle=alpha_0
        radius = float(sqrt(pow(((Nx-Nz)/2),2)+pow(Nxz,2)))
        centreX = float((Nx+Nz)/2)
        rleft_z=0
        rleft_x=centreX-radius
        rright_x=centreX+radius
        alpha_0=180*atan(Nxz/(Nz+(-rleft_x+0.00001)))/(pi)
        alpha_0=int(alpha_0+0.5)
        if alpha == alpha_0:
            Rotating_Plane_red_source.data = dict(x=[0], y=[0], angle =[-P_Angle], size = [75])
            Rotating_Plane_source.data     = dict(x=[],  y=[],  angle =[],         size = []  )
        else:
            Rotating_Plane_source.data     = dict(x=[0], y=[0], angle =[-P_Angle], size = [75])
            Rotating_Plane_red_source.data = dict(x=[],  y=[],  angle =[],         size = []  )


        ChangeMohrCircle()
        ChangeRotatingPlane_Forces()

     if changeAngle == 0:
         Plane_Angle_slider.value = 0
        
def ChangeMohrCircle():
    global P_Angle
    
    radius  = float(sqrt(pow(((Nx-Nz)/2),2)+pow(Nxz,2)))
    centreX = float((Nx+Nz)/2)
    rleft_z = 0
    rleft_x = centreX-radius
    
    Mohr_Circle_source.data = dict(x=[centreX], y=[0], radius=[radius])   
    OriginalPlane_line_source.data = dict(x=[rleft_x,Nz,Nz], y=[rleft_z,Nxz,0])
  
    ## Calculate forces in rotated element
    Nzeta     = float(((Nx+Nz)/2)+(((Nx-Nz)/2)*cos(2*P_Angle))+Nxz*sin(2*P_Angle))
    Neta      = float(((Nx+Nz)/2)-(((Nx-Nz)/2)*cos(2*P_Angle))-Nxz*sin(2*P_Angle))
    Nzetaeta  = float((-(((Nx-Nz)/2)*sin(2*P_Angle)))+Nxz*cos(2*P_Angle))

    if P_Angle == 0:
        Nzeta    = Nx
        Neta     = Nz
        Nzetaeta = Nxz
    if P_Angle == (pi/2):
        Nzeta    = Nz
        Neta     = Nx
        Nzetaeta = -Nxz


    Newplane_line_source.data       = dict(x=[rleft_x,Neta], y=[rleft_z,Nzetaeta])

    Figure2Moving_Label_source.data = dict(x=[Nx,Nz,-4,Nx-0.5,Nz-0.5,-0.5,Nz,Neta+1.5],y=[-3,-3,Nxz-1,-1.1,-1.1,Nxz-1.2,Nxz,Nzetaeta],
                                           names =[u"\u03C3"u"\u0078",u"\u03C3"u"\u007A",u"\u03C4"u"\u0078"u"\u007A","x","x","-","A","B"])
 




def ChangeRotatingPlane_Forces():
    
    global Nx,Nz,Nxz
    Nzeta    = float(float((Nx+Nz)/2)+(float((Nx-Nz)/2)*cos(2*P_Angle))+float(Nxz*sin(2*P_Angle)))
    Neta     = float(float((Nx+Nz)/2)-(float((Nx-Nz)/2)*cos(2*P_Angle))-float(Nxz*sin(2*P_Angle)))
    Nzetaeta = float((-(((Nx-Nz)/2)*sin(2*P_Angle)))+Nxz*cos(2*P_Angle))
   
    global P_Angle
    P_Angle = -P_Angle

    ## Set Nzetaeta=0 if angle-slider is set to principal direction
    alpha   = 180*P_Angle/pi
    alpha   = int(alpha+0.5)

    radius  = float(sqrt(pow(((Nx-Nz)/2),2)+pow(Nxz,2)))
    centreX = float((Nx+Nz)/2)
    rleft_x = centreX-radius

    alpha_0 = 180*atan(Nxz/(Nz+(-rleft_x+0.00001)))/(pi)
    alpha_0 = int(alpha_0+0.5)
    
    if alpha == alpha_0:
        Nzetaeta=0

        
    Nzeta = 0.75*Nzeta
    if Nzeta>0:
        NzetaP_arrow_source.data = dict(xS=[12.5*cos(P_Angle)],  xE=[(12.5+Nzeta)*cos(P_Angle)],  yS=[(12.5*sin(P_Angle))],   yE=[(((12.5+Nzeta)*sin(P_Angle)))],   lW = [2])
        NzetaN_arrow_source.data = dict(xS=[-12.5*cos(P_Angle)], xE=[(-12.5-Nzeta)*cos(P_Angle)], yS=[0-(12.5*sin(P_Angle))], yE=[(0-((12.5+Nzeta)*sin(P_Angle)))], lW = [2])
        
        
        NzetaP_rect_source.data  = dict(x=[(12.5*cos(P_Angle)+(12.5+Nzeta)*cos(P_Angle))/2],   y=[((12.5*sin(P_Angle))+(((12.5+Nzeta)*sin(P_Angle))))/2],   w=[Nzeta+1.5], h = [13], angle=[P_Angle])
        NzetaN_rect_source.data  = dict(x=[(-12.5*cos(P_Angle)+(-12.5-Nzeta)*cos(P_Angle))/2], y=[((-12.5*sin(P_Angle))+(-((12.5+Nzeta)*sin(P_Angle))))/2], w=[Nzeta+1.5], h = [13], angle=[P_Angle])

    elif Nzeta==0:
        NzetaP_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        NzetaN_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        
        NzetaP_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])
        NzetaN_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])

    else:
        NzetaP_arrow_source.data = dict(xS=[(12.5-Nzeta)*cos(P_Angle)],  xE=[12.5*cos(P_Angle)],   yS=[0+((12.5-Nzeta)*sin(P_Angle))],   yE=[0+(12.5*sin(P_Angle))], lW = [2])
        NzetaN_arrow_source.data = dict(xS=[(-12.5+Nzeta)*cos(P_Angle)], xE=[-12.5 *cos(P_Angle)], yS=[(0-((12.5-Nzeta)*sin(P_Angle)))], yE=[0-(12.5*sin(P_Angle))], lW = [2])
        
        NzetaP_rect_source.data  = dict(x=[(12.5*cos(P_Angle)+(12.5-Nzeta)*cos(P_Angle))/2],   y=[((12.5*sin(P_Angle))+(((12.5-Nzeta)*sin(P_Angle))))/2],   w=[Nzeta-1.5], h = [13], angle=[P_Angle])
        NzetaN_rect_source.data  = dict(x=[(-12.5*cos(P_Angle)+(-12.5+Nzeta)*cos(P_Angle))/2], y=[((-12.5*sin(P_Angle))+(-((12.5-Nzeta)*sin(P_Angle))))/2], w=[Nzeta-1.5], h = [13], angle=[P_Angle])

    Neta = 0.75*Neta
    if Neta>0:
        NetaP_arrow_source.data = dict(xS=[12.5*cos((pi/2)+P_Angle)], xE=[(12.5+Neta)*cos((pi/2)+P_Angle)], yS=[(12.5*sin((pi/2)+P_Angle))], yE=[((12.5+Neta)*sin((pi/2)+P_Angle))], lW = [2])
        NetaN_arrow_source.data = dict(xS=[12.5*sin(P_Angle)],        xE=[(12.5+Neta)*sin(P_Angle)],        yS=[-(12.5*cos(P_Angle))],       yE=[-((12.5+Neta)*cos(P_Angle))],       lW = [2]) 
        
        NetaP_rect_source.data  = dict(x=[(12.5*cos((pi/2)+P_Angle)+(12.5+Neta)*cos((pi/2)+P_Angle))/2], y=[((12.5*sin((pi/2)+P_Angle))+((12.5+Neta)*sin((pi/2)+P_Angle)))/2], h=[Neta+1.5], w = [13], angle=[P_Angle])
        NetaN_rect_source.data  = dict(x=[(12.5*sin(P_Angle)+(12.5+Neta)*sin(P_Angle))/2],               y=[(-(12.5*cos(P_Angle))+-((12.5+Neta)*cos(P_Angle)))/2],             h=[Neta+1.5], w = [13], angle=[P_Angle])

    elif Neta==0:
        NetaP_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        NetaN_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        
        NetaP_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])
        NetaN_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])

    else:
        NetaP_arrow_source.data = dict(xS=[(12.5-Neta)*cos((pi/2)+P_Angle)],xE=[12.5*cos((pi/2)+P_Angle)], yS=[((12.5-Neta)*sin((pi/2)+P_Angle))], yE=[0+(12.5*sin((pi/2)+P_Angle))],  lW = [2])
        NetaN_arrow_source.data = dict(xS=[(12.5-Neta)*sin(P_Angle)],xE=[12.5*sin(P_Angle)],               yS=[-(12.5-Neta)*cos(P_Angle)],         yE=[-12.5*cos(P_Angle)],            lW = [2])      
        
        NetaP_rect_source.data  = dict(x=[((12.5-Neta)*cos((pi/2)+P_Angle)+12.5*cos((pi/2)+P_Angle))/2], y=[(((12.5-Neta)*sin((pi/2)+P_Angle))+0+(12.5*sin((pi/2)+P_Angle)))/2], h=[Neta-1.5], w = [13], angle=[P_Angle])
        NetaN_rect_source.data  = dict(x=[((12.5-Neta)*sin(P_Angle)+12.5*sin(P_Angle))/2],               y=[(-(12.5-Neta)*cos(P_Angle)+-12.5*cos(P_Angle))/2],                   h=[Neta-1.5], w = [13], angle=[P_Angle])


    Nzetaeta=0.75*Nzetaeta
    if Nzetaeta>0:
        Nzetaeta1_arrow_source.data = dict(xS=[9*cos(P_Angle)+((Nzetaeta/2)*sin(P_Angle))],  xE=[9*cos(P_Angle)-((Nzetaeta/2)*sin(P_Angle))],  yS=[(0+9*sin(P_Angle))-((Nzetaeta/2)*cos(P_Angle))], yE=[(0+9*sin(P_Angle))+((Nzetaeta/2)*cos(P_Angle))], lW = [2])
        Nzetaeta2_arrow_source.data = dict(xS=[-9*sin(P_Angle)-((Nzetaeta/2)*cos(P_Angle))], xE=[-9*sin(P_Angle)+((Nzetaeta/2)*cos(P_Angle))], yS=[(0+9*cos(P_Angle))-((Nzetaeta/2)*sin(P_Angle))], yE=[(0+9*cos(P_Angle))+((Nzetaeta/2)*sin(P_Angle))], lW = [2])
        Nzetaeta3_arrow_source.data = dict(xS=[-9*cos(P_Angle)-((Nzetaeta/2)*sin(P_Angle))], xE=[-9*cos(P_Angle)+((Nzetaeta/2)*sin(P_Angle))], yS=[(0-9*sin(P_Angle))+((Nzetaeta/2)*cos(P_Angle))], yE=[(0-9*sin(P_Angle))-((Nzetaeta/2)*cos(P_Angle))], lW = [2])
        Nzetaeta4_arrow_source.data = dict(xS=[9*sin(P_Angle)+((Nzetaeta/2)*cos(P_Angle))],  xE=[9*sin(P_Angle)-((Nzetaeta/2)*cos(P_Angle))],  yS=[(0-9*cos(P_Angle))+((Nzetaeta/2)*sin(P_Angle))], yE=[(0-9*cos(P_Angle))-((Nzetaeta/2)*sin(P_Angle))], lW = [2])
        
        
        Nzetaeta1_rect_source.data  = dict(x=[(9*cos(P_Angle)+((Nzetaeta/2)*sin(P_Angle))+9*cos(P_Angle)-((Nzetaeta/2)*sin(P_Angle)))/2],   y=[((0+9*sin(P_Angle))-((Nzetaeta/2)*cos(P_Angle))+(0+9*sin(P_Angle))+((Nzetaeta/2)*cos(P_Angle)))/2], w=[0.3*Nzetaeta+.5], h = [13], angle=[P_Angle])
        Nzetaeta2_rect_source.data  = dict(x=[(-9*sin(P_Angle)-((Nzetaeta/2)*cos(P_Angle))+-9*sin(P_Angle)+((Nzetaeta/2)*cos(P_Angle)))/2], y=[((0+9*cos(P_Angle))-((Nzetaeta/2)*sin(P_Angle))+(0+9*cos(P_Angle))+((Nzetaeta/2)*sin(P_Angle)))/2], h=[0.3*Nzetaeta+.5], w = [13], angle=[P_Angle])
        Nzetaeta3_rect_source.data  = dict(x=[(-9*cos(P_Angle)-((Nzetaeta/2)*sin(P_Angle))-9*cos(P_Angle)+((Nzetaeta/2)*sin(P_Angle)))/2],  y=[((0-9*sin(P_Angle))+((Nzetaeta/2)*cos(P_Angle))+(0-9*sin(P_Angle))-((Nzetaeta/2)*cos(P_Angle)))/2], w=[0.3*Nzetaeta+.5], h = [13], angle=[P_Angle])
        Nzetaeta4_rect_source.data  = dict(x=[(9*sin(P_Angle)+((Nzetaeta/2)*cos(P_Angle))+9*sin(P_Angle)-((Nzetaeta/2)*cos(P_Angle)))/2],   y=[((0-9*cos(P_Angle))+((Nzetaeta/2)*sin(P_Angle))+(0-9*cos(P_Angle))-((Nzetaeta/2)*sin(P_Angle)))/2], h=[0.3*Nzetaeta+.5], w = [13], angle=[P_Angle])

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
        Nzetaeta1_arrow_source.data = dict(xS=[9*cos(P_Angle)+((Nzetaeta/2)*sin(P_Angle))],  xE=[9*cos(P_Angle)-((Nzetaeta/2)*sin(P_Angle))],  yS=[(0+9*sin(P_Angle))-((Nzetaeta/2)*cos(P_Angle))], yE=[(0+9*sin(P_Angle))+((Nzetaeta/2)*cos(P_Angle))], lW = [2])
        Nzetaeta2_arrow_source.data = dict(xS=[-9*sin(P_Angle)-((Nzetaeta/2)*cos(P_Angle))], xE=[-9*sin(P_Angle)+((Nzetaeta/2)*cos(P_Angle))], yS=[(0+9*cos(P_Angle))-((Nzetaeta/2)*sin(P_Angle))], yE=[(0+9*cos(P_Angle))+((Nzetaeta/2)*sin(P_Angle))], lW = [2])
        Nzetaeta3_arrow_source.data = dict(xS=[-9*cos(P_Angle)-((Nzetaeta/2)*sin(P_Angle))], xE=[-9*cos(P_Angle)+((Nzetaeta/2)*sin(P_Angle))], yS=[(0-9*sin(P_Angle))+((Nzetaeta/2)*cos(P_Angle))], yE=[(0-9*sin(P_Angle))-((Nzetaeta/2)*cos(P_Angle))], lW = [2])
        Nzetaeta4_arrow_source.data = dict(xS=[9*sin(P_Angle)+((Nzetaeta/2)*cos(P_Angle))],  xE=[9*sin(P_Angle)-((Nzetaeta/2)*cos(P_Angle))],  yS=[(0-9*cos(P_Angle))+((Nzetaeta/2)*sin(P_Angle))], yE=[(0-9*cos(P_Angle))-((Nzetaeta/2)*sin(P_Angle))], lW = [2])

        Nzetaeta1_rect_source.data  = dict(x=[(9*cos(P_Angle)+((Nzetaeta/2)*sin(P_Angle))+9*cos(P_Angle)-((Nzetaeta/2)*sin(P_Angle)))/2],   y=[((0+9*sin(P_Angle))-((Nzetaeta/2)*cos(P_Angle))+(0+9*sin(P_Angle))+((Nzetaeta/2)*cos(P_Angle)))/2], w=[0.3*Nzetaeta-.5], h = [13], angle=[P_Angle])
        Nzetaeta2_rect_source.data  = dict(x=[(-9*sin(P_Angle)-((Nzetaeta/2)*cos(P_Angle))+-9*sin(P_Angle)+((Nzetaeta/2)*cos(P_Angle)))/2], y=[((0+9*cos(P_Angle))-((Nzetaeta/2)*sin(P_Angle))+(0+9*cos(P_Angle))+((Nzetaeta/2)*sin(P_Angle)))/2], h=[0.3*Nzetaeta-.5], w = [13], angle=[P_Angle])
        Nzetaeta3_rect_source.data  = dict(x=[(-9*cos(P_Angle)-((Nzetaeta/2)*sin(P_Angle))-9*cos(P_Angle)+((Nzetaeta/2)*sin(P_Angle)))/2],  y=[((0-9*sin(P_Angle))+((Nzetaeta/2)*cos(P_Angle))+(0-9*sin(P_Angle))-((Nzetaeta/2)*cos(P_Angle)))/2], w=[0.3*Nzetaeta-.5], h = [13], angle=[P_Angle])
        Nzetaeta4_rect_source.data  = dict(x=[(9*sin(P_Angle)+((Nzetaeta/2)*cos(P_Angle))+9*sin(P_Angle)-((Nzetaeta/2)*cos(P_Angle)))/2],   y=[((0-9*cos(P_Angle))+((Nzetaeta/2)*sin(P_Angle))+(0-9*cos(P_Angle))-((Nzetaeta/2)*sin(P_Angle)))/2], h=[0.3*Nzetaeta-.5], w = [13], angle=[P_Angle])

    P_Angle=-P_Angle


   

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
figure1 = figure(title="Stress State A", tools="", x_range=(-30,30), y_range=(-30,30),width=400,height=400)
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
figure1_labels = LabelSet(x='x', y='y', text='names', level='glyph',
              x_offset=5, y_offset=5, source=Figure1Perm_Label_source, render_mode='canvas')
figure1.add_layout(figure1_labels)
figure1.add_glyph(NxP_rect_source,NxP_rect_glyph)
figure1.add_glyph(NxN_rect_source,NxN_rect_glyph)
figure1.add_glyph(NzP_rect_source,NzP_rect_glyph)
figure1.add_glyph(NzN_rect_source,NzN_rect_glyph)
figure1.add_glyph(Nxz1_rect_source,Nxz1_rect_glyph)
figure1.add_glyph(Nxz2_rect_source,Nxz1_rect_glyph)
figure1.add_glyph(Nxz3_rect_source,Nxz1_rect_glyph)
figure1.add_glyph(Nxz4_rect_source,Nxz1_rect_glyph)





### Figure 2: Define Geometry
Mohr_Circle_glyph = Circle(x='x',y='y',radius='radius', radius_dimension='y', fill_color='#c3c3c3', fill_alpha=0.5)
Wedge_glyph = Wedge(x="x", y="y", radius="radius", start_angle="sA", end_angle="eA", fill_color="firebrick", fill_alpha=0.6, direction="clock")
### Figure 2: Define Figure and add Geometry
figure2 = figure(title="", tools="", x_range=(-25,25), y_range=(-25,25),width=400,height=400)
figure2.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=-20, y_start=0, x_end=20, y_end=0))
figure2.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=0, y_start=-20, x_end=0, y_end=20))
figure2.add_glyph(Mohr_Circle_source,Mohr_Circle_glyph)
figure2.add_glyph(Wedge_source,Wedge_glyph)
# Modified line
figure2.line(x='x',y='y',source= Newplane_line_source, color="#A2AD00", line_width=3, line_join = 'bevel')
figure2.circle(x='x',y='y',source= Newplane_line_source, size=4, color="black", alpha=0.4)
figure2_labels1 = LabelSet(x='x', y='y', text='names', level='glyph',
              x_offset=0, y_offset=0, source=Figure2Perm_Label_source, render_mode='canvas')
figure2_labels2 = LabelSet(x='x', y='y', text='names', source=Figure2Moving_Label_source, text_color = 'black')
figure2_labels3 = LabelSet(x='x', y='y', text='names', source=Figure2Show_Label_source, text_color = 'firebrick')
figure2.add_layout(figure2_labels1)
figure2.add_layout(figure2_labels2)
figure2.add_layout(figure2_labels3)
# Original line
figure2.line(x='x',y='y',source= OriginalPlane_line_source, color="black", alpha=0.5, line_width=3, line_join = 'bevel')
figure2.circle(x='x',y='y',source= OriginalPlane_line_source, size=4, color="black", alpha=0.4)






### Figure 3: Define Geometry
Rotating_Plane_glyph = Square(x='x',y='y',angle='angle',size='size', fill_color = '#A2AD00', fill_alpha=0.5)
Rotating_Plane_red_glyph = Square(x='x',y='y',angle='angle',size='size', fill_color = 'firebrick', fill_alpha=0.5)

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
figure3 = figure(title="Stress State B", tools="", x_range=(-30,30), y_range=(-30,30),width=400,height=400)
figure3.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=0, y_start=0, x_end=25, y_end=0))
figure3.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=0, y_start=0, x_end=0, y_end=-25))
figure3_labels = LabelSet(x='x', y='y', text='names', level='glyph',
              x_offset=5, y_offset=5, source=Figure1Perm_Label_source, render_mode='canvas')
figure3.add_layout(figure3_labels)
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


### Turn off grid
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



### Creating  sliders to change Normal and Tangential Forces
Normal_X_slider= Slider(title=u"\u03C3"u"\u0078",value= 0,start = -10, end = 10, step = 0.5)
Normal_X_slider.on_change('value',NormalForceX_init)
    
Normal_Z_slider= Slider(title=u"\u03C3"u"\u007A",value= 0,start = -10, end = 10, step = 0.5)
Normal_Z_slider.on_change('value',NormalForceZ_init)
   
Tangential_XZ_slider= Slider(title=u"\u03C4"u"\u0078"u"\u007A",value= 0,start = 0, end = 10, step = 0.5)
Tangential_XZ_slider.on_change('value',TangentialXZ_init)
    
Plane_Angle_slider= Slider(title= u"\u03B1",value= 0,start = 0, end = 90, step = 1)
Plane_Angle_slider.on_change('value',changePlaneAngle)


###Create Reset Button:
reset_button = Button(label="Reset", button_type="success")
reset_button.on_click(reset)


###Create Draw Button:
draw_button = Button(label="Draw", button_type="success")
draw_button.on_click(draw)

###Create Show Button:
show_button = Button(label="Show principal stress + direction", button_type="success")
show_button.on_click(show)


### Initialising all column data for the initial plot
init()


### Adding description from HTML file
description_filename = join(dirname(__file__), "description.html")
description = Div(text=open(description_filename).read(), render_as_text=False, width=1200)

curdoc().add_root(column(description,row(column(figure1,Normal_X_slider,Normal_Z_slider,Tangential_XZ_slider),column(figure2,draw_button,show_button,reset_button),column(figure3, Plane_Angle_slider))))
curdoc().title = "Mohr Circle"

