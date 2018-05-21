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
from bokeh.models.glyphs import Ellipse
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
rleft_x=centreX-radius
rleft_z=0


### Initializing variables

## Figure 1: 

NxP_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NzP_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NxN_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NzN_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nxz1_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nxz2_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nxz3_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nxz4_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))

##Figure 2: Mohr Circle
OriginalPlane_line_source = ColumnDataSource(data=dict(x=[],y=[]))
Newplane_line_source = ColumnDataSource(data=dict(x=[],y=[]))

##Figure 3: Rotating plane 
Rotating_Plane_source = ColumnDataSource(data=dict(x=[], y=[],angle = [],size =[]))

NzetaP_arrow_source    = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NzetaN_arrow_source    = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NetaP_arrow_source     = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NetaN_arrow_source     = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nzetaeta1_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nzetaeta2_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nzetaeta3_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nzetaeta4_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))


### Labels
Figure1Perm_Label_source = ColumnDataSource(data=dict(x=[22,1],
                                    y=[-5, -27],names=['x', 'z']))
Figure2Perm_Label_source = ColumnDataSource(data=dict(x=[27.5,-3.5],
                                    y=[-5, 26],names=[u"\u03C3", u"\u03C4"]))
Figure2Moving_Label_source = ColumnDataSource(data=dict(x=[],
                                    y=[],names=[]))


### Figure 2: Data structures
Mohr_Circle_source = ColumnDataSource(data=dict(x=[], y=[], radius=[]))


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
    radius = float(sqrt(pow(((Nx-Nz)/2),2)+pow(Nxz,2)))
    centreX = float((Nx+Nz)/2)
    Nzeta = float(((Nx+Nz)/2)+(((Nx-Nz)/2)*cos(2*P_Angle))+Nxz*sin(2*P_Angle))
    Neta  = float(((Nx+Nz)/2)-(((Nx-Nz)/2)*cos(2*P_Angle))-Nxz*sin(2*P_Angle))
    Nzetaeta =float((-(((Nx-Nz)/2)*sin(2*P_Angle)))+Nxz*cos(2*P_Angle))

    ## Figure 1: Set values for arrows

    NxP_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    NxN_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    NzP_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    NzN_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nxz1_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nxz2_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nxz3_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nxz4_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    
    


    ## Figure 3: Rotating plane
    Rotating_Plane_source.data = dict(x=[0], y=[0],angle =[0*(pi/180)],size = [75])
    NzetaP_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    NzetaN_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    NetaP_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    NetaN_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nzetaeta1_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nzetaeta2_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nzetaeta3_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Nzetaeta4_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])


    ## Figure 2 
    Mohr_Circle_source.data = dict(x=[centreX], y=[0], radius=[radius])


    OriginalPlane_line_source.data = dict(x=[rleft_x,Nz,Nz], y=[rleft_z,Nxz,0])
    Newplane_line_source.data = dict(x=[rleft_x,Neta,Neta], y=[rleft_z,Nzetaeta,0])
    

    Figure2Moving_Label_source.data = dict(x=[Nx,Nz,1,Nx-0.7,Nz-0.7,-0.5,Nz,Neta+1.5],y=[-4,-4,Nxz-1.4,-1.4,-1.4,Nxz-1.2,Nxz,Nzetaeta],
                                           names =[u"\u03C3"u"\u0078",u"\u03C3"u"\u007A",u"\u03C4"u"\u0078"u"\u007A","x","x","-","A","B"])

 


def NormalForceX(attr,old,new):
    global Nx
    Nx = new  
    if(new<0):
        NxP_arrow_source.data  = dict(xS=[10-new], xE=[10], yS=[0], yE=[0], lW = [3])
        NxN_arrow_source.data  = dict(xS=[-10+new], xE=[-10], yS=[0], yE=[0], lW = [3]) 
    else:
        NxP_arrow_source.data  = dict(xS=[10], xE=[10+new], yS=[0], yE=[0], lW = [3])
        NxN_arrow_source.data  = dict(xS=[-10], xE=[-10-new], yS=[0], yE=[0], lW = [3])
        
    ChangeMohrCircle()
    ChangeRotatingPlane_Forces()
    
def NormalForceZ(attr,old,new):
    global Nz   
    if(new<0):
        NzP_arrow_source.data  = dict(xS=[0], xE=[0], yS=[10-new], yE=[10], lW = [3])
        NzN_arrow_source.data  = dict(xS=[0], xE=[0], yS=[-10+new], yE=[-10], lW = [3])
    else:
        NzP_arrow_source.data  = dict(xS=[0], xE=[0], yS=[10], yE=[10+new], lW = [3])
        NzN_arrow_source.data  = dict(xS=[0], xE=[0], yS=[-10], yE=[-10-new], lW = [3])
        
    Nz = new
    ChangeMohrCircle()
    ChangeRotatingPlane_Forces()
    
def TangentialXZ(attr,old,new):
    global Nxz     
    if(new<0):
         Nxz1_arrow_source.data = dict(xS=[8], xE=[8], yS=[0-(new/2)], yE=[0+(new/2)], lW = [5])
         Nxz2_arrow_source.data = dict(xS=[-8], xE=[-8], yS=[0+(new/2)], yE=[0-(new/2)], lW = [5])
         Nxz3_arrow_source.data = dict(xS=[-new/2], xE=[new/2], yS=[8], yE=[8], lW = [5])
         Nxz4_arrow_source.data = dict(xS=[(new/2)], xE=[(-new/2)], yS=[-8], yE=[-8], lW = [5])
    else:     
         Nxz1_arrow_source.data = dict(xS=[8], xE=[8], yS=[0-(new/2)], yE=[0+(new/2)], lW = [5])
         Nxz2_arrow_source.data = dict(xS=[-8], xE=[-8], yS=[0+(new/2)], yE=[0-(new/2)], lW = [5])
         Nxz3_arrow_source.data = dict(xS=[-new/2], xE=[new/2], yS=[8], yE=[8], lW = [5])
         Nxz4_arrow_source.data = dict(xS=[(new/2)], xE=[-(new/2)], yS=[-8], yE=[-8], lW = [5])   
    Nxz = new
    ChangeMohrCircle()
    ChangeRotatingPlane_Forces()
        
def changePlaneAngle(attr,old,new):
     global P_Angle
     P_Angle = -new*(pi/180)
     Rotating_Plane_source.data = dict(x=[0], y=[0],angle =[-P_Angle],size = [75])
     ChangeMohrCircle()
     ChangeRotatingPlane_Forces()
        
def ChangeMohrCircle():
    global P_Angle
    radius = float(sqrt(pow(((Nx-Nz)/2),2)+pow(Nxz,2)))
    centreX = float((Nx+Nz)/2)
    rleft_z=0
    rleft_x=centreX-radius
    Mohr_Circle_source.data = dict(x=[centreX], y=[0], radius=[radius])   
    #OriginalPlane_line_source.data = dict(x=[Nz,Nz,Nx,Nx], y=[0,-Nxz,Nxz,0])
    OriginalPlane_line_source.data = dict(x=[rleft_x,Nz,Nz], y=[rleft_z,Nxz,0])
  
    ## Calculate forces in rotated element
    Nzeta = float(((Nx+Nz)/2)+(((Nx-Nz)/2)*cos(2*P_Angle))+Nxz*sin(2*P_Angle))
    Neta  = float(((Nx+Nz)/2)-(((Nx-Nz)/2)*cos(2*P_Angle))-Nxz*sin(2*P_Angle))
    Nzetaeta = float((-(((Nx-Nz)/2)*sin(2*P_Angle)))+Nxz*cos(2*P_Angle))
    if P_Angle == 0:
        Nzeta = Nx
        Neta  = Nz
        Nzetaeta =Nxz
    if P_Angle == (pi/2):
        Nzeta = Nz
        Neta  = Nx
        Nzetaeta =-Nxz

    Newplane_line_source.data = dict(x=[rleft_x,Neta], y=[rleft_z,Nzetaeta])

    Figure2Moving_Label_source.data = dict(x=[Nx,Nz,1,Nx-0.7,Nz-0.7,-0.5,Nz,Neta+1.5],y=[-4,-4,Nxz-1.4,-1.4,-1.4,Nxz-1.2,Nxz,Nzetaeta],
                                           names =[u"\u03C3"u"\u0078",u"\u03C3"u"\u007A",u"\u03C4"u"\u0078"u"\u007A","x","x","-","A","B"])


def ChangeRotatingPlane_Forces():
    
    global Nx,Nz,Nxz
    Nzeta = float(float((Nx+Nz)/2)+(float((Nx-Nz)/2)*cos(2*P_Angle))+float(Nxz*sin(2*P_Angle)))
    Neta  = float(float((Nx+Nz)/2)-(float((Nx-Nz)/2)*cos(2*P_Angle))-float(Nxz*sin(2*P_Angle)))
    Nzetaeta = float((-(((Nx-Nz)/2)*sin(2*P_Angle)))+Nxz*cos(2*P_Angle))
    
    global P_Angle
    P_Angle=-P_Angle

    if Nzeta>0:
        NzetaP_arrow_source.data = dict(xS=[10*cos(P_Angle)], xE=[(10+Nzeta)*cos(P_Angle)], yS=[(10*sin(P_Angle))], yE=[(((10+Nzeta)*sin(P_Angle)))], lW = [3])
        NzetaN_arrow_source.data = dict(xS=[-10*cos(P_Angle)], xE=[(-10-Nzeta)*cos(P_Angle)], yS=[0-(10*sin(P_Angle))], yE=[(0-((10+Nzeta)*sin(P_Angle)))], lW = [3])
    else:
        NzetaP_arrow_source.data = dict(xS=[(10-Nzeta)*cos(P_Angle)], xE=[10*cos(P_Angle)], yS=[0+((10-Nzeta)*sin(P_Angle))], yE=[0+(10*sin(P_Angle))], lW = [3])
        NzetaN_arrow_source.data = dict(xS=[(-10+Nzeta)*cos(P_Angle)], xE=[-10 *cos(P_Angle)], yS=[(0-((10-Nzeta)*sin(P_Angle)))], yE=[0-(10*sin(P_Angle))], lW = [3])

    if Neta>0:
        NetaP_arrow_source.data = dict(xS=[10*cos((pi/2)+P_Angle)], xE=[(10+Neta)*cos((pi/2)+P_Angle)], yS=[(10*sin((pi/2)+P_Angle))], yE=[((10+Neta)*sin((pi/2)+P_Angle))], lW = [3])
        NetaN_arrow_source.data =  dict(xS=[10*sin(P_Angle)], xE=[(10+Neta)*sin(P_Angle)], yS=[-(10*cos(P_Angle))], yE=[-((10+Neta)*cos(P_Angle))], lW = [3])      
    else:
        NetaP_arrow_source.data = dict(xS=[(10-Neta)*cos((pi/2)+P_Angle)],xE=[10*cos((pi/2)+P_Angle)],yS=[((10-Neta)*sin((pi/2)+P_Angle))], yE=[0+(10*sin((pi/2)+P_Angle))],  lW = [3])
        NetaN_arrow_source.data = dict(xS=[(10-Neta)*sin(P_Angle)],xE=[10*sin(P_Angle)], yS=[-(10-Neta)*cos(P_Angle)],yE=[-10*cos(P_Angle)], lW = [3])      
        
    if Nzetaeta>0:
        Nzetaeta1_arrow_source.data = dict(xS=[8*cos(P_Angle)+((Nzetaeta/2)*sin(P_Angle))], xE=[8*cos(P_Angle)-((Nzetaeta/2)*sin(P_Angle))], yS=[(0+8*sin(P_Angle))-((Nzetaeta/2)*cos(P_Angle))], yE=[(0+8*sin(P_Angle))+((Nzetaeta/2)*cos(P_Angle))], lW = [5])
        Nzetaeta2_arrow_source.data = dict(xS=[-8*sin(P_Angle)-((Nzetaeta/2)*cos(P_Angle))], xE=[-8*sin(P_Angle)+((Nzetaeta/2)*cos(P_Angle))], yS=[(0+8*cos(P_Angle))-((Nzetaeta/2)*sin(P_Angle))], yE=[(0+8*cos(P_Angle))+((Nzetaeta/2)*sin(P_Angle))], lW = [5])
        Nzetaeta3_arrow_source.data = dict(xS=[-8*cos(P_Angle)-((Nzetaeta/2)*sin(P_Angle))], xE=[-8*cos(P_Angle)+((Nzetaeta/2)*sin(P_Angle))], yS=[(0-8*sin(P_Angle))+((Nzetaeta/2)*cos(P_Angle))], yE=[(0-8*sin(P_Angle))-((Nzetaeta/2)*cos(P_Angle))], lW = [5])
        Nzetaeta4_arrow_source.data = dict(xS=[8*sin(P_Angle)+((Nzetaeta/2)*cos(P_Angle))], xE=[8*sin(P_Angle)-((Nzetaeta/2)*cos(P_Angle))], yS=[(0-8*cos(P_Angle))+((Nzetaeta/2)*sin(P_Angle))], yE=[(0-8*cos(P_Angle))-((Nzetaeta/2)*sin(P_Angle))], lW = [5])
    else:
        Nzetaeta1_arrow_source.data = dict(xS=[8*cos(P_Angle)+((Nzetaeta/2)*sin(P_Angle))], xE=[8*cos(P_Angle)-((Nzetaeta/2)*sin(P_Angle))], yS=[(0+8*sin(P_Angle))-((Nzetaeta/2)*cos(P_Angle))], yE=[(0+8*sin(P_Angle))+((Nzetaeta/2)*cos(P_Angle))], lW = [5])
        Nzetaeta2_arrow_source.data = dict(xS=[-8*sin(P_Angle)-((Nzetaeta/2)*cos(P_Angle))], xE=[-8*sin(P_Angle)+((Nzetaeta/2)*cos(P_Angle))], yS=[(0+8*cos(P_Angle))-((Nzetaeta/2)*sin(P_Angle))], yE=[(0+8*cos(P_Angle))+((Nzetaeta/2)*sin(P_Angle))], lW = [5])
        Nzetaeta3_arrow_source.data = dict(xS=[-8*cos(P_Angle)-((Nzetaeta/2)*sin(P_Angle))], xE=[-8*cos(P_Angle)+((Nzetaeta/2)*sin(P_Angle))], yS=[(0-8*sin(P_Angle))+((Nzetaeta/2)*cos(P_Angle))], yE=[(0-8*sin(P_Angle))-((Nzetaeta/2)*cos(P_Angle))], lW = [5])
        Nzetaeta4_arrow_source.data = dict(xS=[8*sin(P_Angle)+((Nzetaeta/2)*cos(P_Angle))], xE=[8*sin(P_Angle)-((Nzetaeta/2)*cos(P_Angle))], yS=[(0-8*cos(P_Angle))+((Nzetaeta/2)*sin(P_Angle))], yE=[(0-8*cos(P_Angle))-((Nzetaeta/2)*sin(P_Angle))], lW = [5])
    P_Angle=-P_Angle


   

### Figure 1: Plotting Arrows
NxP_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NxP_arrow_source,line_color="#E37222")
NxN_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NxN_arrow_source,line_color="#E37222")
NzP_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NzP_arrow_source,line_color="#E37222")
NzN_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NzN_arrow_source,line_color="#E37222")
Nxz1_arrow_glyph = Arrow(end=OpenHead(line_color="#0065BD",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nxz1_arrow_source,line_color="#0065BD")

Nxz2_arrow_glyph = Arrow(end=OpenHead(line_color="#0065BD",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nxz2_arrow_source,line_color="#0065BD")

Nxz3_arrow_glyph = Arrow(end=OpenHead(line_color="#0065BD",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nxz3_arrow_source,line_color="#0065BD")

Nxz4_arrow_glyph = Arrow(end=OpenHead(line_color="#0065BD",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nxz4_arrow_source,line_color="#0065BD")

### Figure 3: Plotting Arrows
Rotating_Plane_glyph = Square(x='x',y='y',angle='angle',size='size', fill_color = '#A2AD00', fill_alpha=0.5)

NzetaP_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NzetaP_arrow_source,line_color="#E37222")
NzetaN_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NzetaN_arrow_source,line_color="#E37222")
NetaP_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NetaP_arrow_source,line_color="#E37222")
NetaN_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NetaN_arrow_source,line_color="#E37222")
Nzetaeta1_arrow_glyph= Arrow(end=OpenHead(line_color="#0065BD",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nzetaeta1_arrow_source,line_color="#0065BD")
Nzetaeta2_arrow_glyph=Arrow(end=OpenHead(line_color="#0065BD",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nzetaeta2_arrow_source,line_color="#0065BD")
Nzetaeta3_arrow_glyph= Arrow(end=OpenHead(line_color="#0065BD",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nzetaeta3_arrow_source,line_color="#0065BD")
Nzetaeta4_arrow_glyph=Arrow(end=OpenHead(line_color="#0065BD",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nzetaeta4_arrow_source,line_color="#0065BD")

### Figure 2: Plotting Mohr Circle 
Mohr_Circle_glyph = Circle(x='x',y='y',radius='radius', radius_dimension='y', fill_color='#c3c3c3', fill_alpha=0.5)

### Figure 1: Define dimensions
figure1 = figure(title="Stress State A", tools="", x_range=(-30,30), y_range=(-30,30),width=400,height=400)

### Figure 1: Add geometry
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

### Figure 3: Define dimensions
figure3 = figure(title="Stress State B", tools="", x_range=(-30,30), y_range=(-30,30),width=400,height=400)

### Figure 3: Add geometry
figure3.add_layout(NzetaP_arrow_glyph)
figure3.add_layout(NzetaN_arrow_glyph)
figure3.add_layout(NetaP_arrow_glyph)
figure3.add_layout(NetaN_arrow_glyph)
figure3.add_layout(Nzetaeta1_arrow_glyph)
figure3.add_layout(Nzetaeta2_arrow_glyph)
figure3.add_layout(Nzetaeta3_arrow_glyph)
figure3.add_layout(Nzetaeta4_arrow_glyph)

figure3.add_glyph(Rotating_Plane_source,Rotating_Plane_glyph)


### Figure 2: Define dimensions
figure2 = figure(title="", tools="", x_range=(-30,30), y_range=(-30,30),width=400,height=400)


### Figure 2: Add geometry
figure2.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=-30, y_start=0, x_end=30, y_end=0))
figure2.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=0, y_start=-30, x_end=0, y_end=30))
figure2.add_glyph(Mohr_Circle_source,Mohr_Circle_glyph)

#Originallinie
figure2.line(x='x',y='y',source= OriginalPlane_line_source, color="black", alpha=0.5, line_width=3, line_join = 'bevel')
figure2.circle(x='x',y='y',source= OriginalPlane_line_source, size=4, color="black", alpha=0.4)

#Gedrehte Linie
figure2.line(x='x',y='y',source= Newplane_line_source, color="#A2AD00", line_width=3, line_join = 'bevel')
figure2.circle(x='x',y='y',source= Newplane_line_source, size=4, color="black", alpha=0.4)

figure2_labels1 = LabelSet(x='x', y='y', text='names', level='glyph',
              x_offset=0, y_offset=0, source=Figure2Perm_Label_source, render_mode='canvas')
figure2_labels2 = LabelSet(x='x', y='y', text='names', source=Figure2Moving_Label_source, text_color = 'black')

figure2.add_layout(figure2_labels1)
figure2.add_layout(figure2_labels2)


### 
figure1.xaxis.major_tick_line_color=None
figure1.xaxis.major_label_text_color=None
figure1.xaxis.minor_tick_line_color=None
figure1.xaxis.axis_line_color=None
figure1.yaxis.major_tick_line_color=None
figure1.yaxis.major_label_text_color=None
figure1.yaxis.minor_tick_line_color=None
figure1.yaxis.axis_line_color=None

figure2.xaxis.major_tick_line_color=None
figure2.xaxis.major_label_text_color=None
figure2.xaxis.minor_tick_line_color=None
figure2.xaxis.axis_line_color=None
figure2.yaxis.major_tick_line_color=None
figure2.yaxis.major_label_text_color=None
figure2.yaxis.minor_tick_line_color=None
figure2.yaxis.axis_line_color=None

figure3.xaxis.major_tick_line_color=None
figure3.xaxis.major_label_text_color=None
figure3.xaxis.minor_tick_line_color=None
figure3.xaxis.axis_line_color=None
figure3.yaxis.major_tick_line_color=None
figure3.yaxis.major_label_text_color=None
figure3.yaxis.minor_tick_line_color=None
figure3.yaxis.axis_line_color=None



### Initialising all column data for th initial plot
init()

### Creating  sliders to change Normal and Tangential Forces
Normal_X_slider= Slider(title="Normal force in X direction (N)",value= 0,start = -10, end = 10, step = 0.5)
Normal_X_slider.on_change('value',NormalForceX)

Normal_Z_slider= Slider(title="Normal force in Z direction (N)",value= 0,start = -10, end = 10, step = 0.5)
Normal_Z_slider.on_change('value',NormalForceZ)

Tangential_XZ_slider= Slider(title="Shear force (N)",value= 0,start = 0, end = 10, step = 0.5)
Tangential_XZ_slider.on_change('value',TangentialXZ)

Plane_Angle_slider= Slider(title="Angle of cross section (º)",value= 0,start = 0, end = 90, step = 0.5)
Plane_Angle_slider.on_change('value',changePlaneAngle)

###Create Reset Button:
button = Button(label="Reset", button_type="success")

###Let program know what functions button calls when clicked:

button.on_click(init)

### Adding description from HTML file
description_filename = join(dirname(__file__), "description.html")
description = Div(text=open(description_filename).read(), render_as_text=False, width=1200)

curdoc().add_root(column(description,row(column(figure1,Normal_X_slider,Normal_Z_slider, row(Tangential_XZ_slider,button)),figure2,column(figure3, Plane_Angle_slider))))
curdoc().title = "Mohr Circle"

