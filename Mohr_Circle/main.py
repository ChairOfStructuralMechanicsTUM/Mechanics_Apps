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
from bokeh.models import ColumnDataSource,Slider,Div,Arrow,OpenHead,NormalHead,LabelSet
from bokeh.models.markers import Square,Circle
from bokeh.models.glyphs import Ellipse
from bokeh.io import curdoc
from os.path import dirname, join
from math import pi,sqrt,pow,sin,cos


### Initial Values
radius = 10
centreX = 10
Nx =0
Ny =0
Nxy =0
P_Angle = 0*(pi/180)
Neta =0 
Nzeta =0 
Nzetaeta =0  
rleft_x=centreX-radius
rleft_y=0


### Initializing variables

## Figure 1: 
NxP1_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NxP2_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NxP3_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))

NyP1_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NyP2_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NyP3_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))

NxN1_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NxN2_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NxN3_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))

NyN1_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NyN2_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NyN3_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))

Nxy1_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nxy2_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nxy3_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nxy4_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))

##Figure 2: Mohr Circle
OriginalPlane_line_source = ColumnDataSource(data=dict(x=[],y=[]))
Newplane_line_source = ColumnDataSource(data=dict(x=[],y=[]))

##Figure 3: Rotating plane 
Rotating_Plane_source = ColumnDataSource(data=dict(x=[], y=[],angle = [],size =[]))

NzetaP1_arrow_source    = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NzetaP2_arrow_source    = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NzetaP3_arrow_source    = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))

NzetaN1_arrow_source    = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NzetaN2_arrow_source    = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NzetaN3_arrow_source    = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))

NetaP1_arrow_source     = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NetaP2_arrow_source     = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NetaP3_arrow_source     = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))

NetaN1_arrow_source     = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NetaN2_arrow_source     = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NetaN3_arrow_source     = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))

Nzetaeta1_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nzetaeta2_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nzetaeta3_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nzetaeta4_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))


### Labels
Figure1Perm_Label_source = ColumnDataSource(data=dict(x=[22,1],
                                    y=[-5, -27],names=['x', 'z']))
Figure2Perm_Label_source = ColumnDataSource(data=dict(x=[26,-3.5],
                                    y=[-3.5, 26],names=["\u03C3", 'tau']))
Figure2Moving_Label_source = ColumnDataSource(data=dict(x=[],
                                    y=[],names=[]))


### Figure 2: Data structures
Mohr_Circle_source = ColumnDataSource(data=dict(x=[], y=[], radius=[]))


###Initial Calculations and Value settings
def init():
    
    P_Angle = 0*(pi/180)
    
    
    ## Calculations
    radius = float(sqrt(pow(((Nx-Ny)/2),2)+pow(Nxy,2)))
    centreX = float((Nx+Ny)/2)
    Nzeta = float(((Nx+Ny)/2)+(((Nx-Ny)/2)*cos(2*P_Angle))+Nxy*sin(2*P_Angle))
    Neta  = float(((Nx+Ny)/2)-(((Nx-Ny)/2)*cos(2*P_Angle))-Nxy*sin(2*P_Angle))
    Nzetaeta =float((-(((Nx-Ny)/2)*sin(2*P_Angle)))+Nxy*cos(2*P_Angle))

    ## Figure 1: Set values for arrows
    NxP1_arrow_source.data  = dict(xS=[10], xE=[10], yS=[5], yE=[5], lW = [3])
    NxP2_arrow_source.data  = dict(xS=[10], xE=[10], yS=[0], yE=[0], lW = [3])
    NxP3_arrow_source.data  = dict(xS=[10], xE=[10], yS=[-5], yE=[-5], lW = [3])

    NxN1_arrow_source.data  = dict(xS=[-10], xE=[-10], yS=[5], yE=[5], lW = [1])
    NxN2_arrow_source.data  = dict(xS=[-10], xE=[-10], yS=[0], yE=[0], lW = [1])
    NxN3_arrow_source.data  = dict(xS=[-10], xE=[-10], yS=[-5], yE=[-5], lW = [1])
    
    NyP1_arrow_source.data  = dict(xS=[5], xE=[5], yS=[10], yE=[10], lW = [1])
    NyP2_arrow_source.data  = dict(xS=[0], xE=[0], yS=[10], yE=[10], lW = [1])
    NyP3_arrow_source.data  = dict(xS=[-5], xE=[-5], yS=[10], yE=[10], lW = [1])
    
    NyN1_arrow_source.data  = dict(xS=[5], xE=[5], yS=[-10], yE=[-10], lW = [1])
    NyN2_arrow_source.data  = dict(xS=[0], xE=[0], yS=[-10], yE=[-10], lW = [1])
    NyN3_arrow_source.data  = dict(xS=[-5], xE=[-5], yS=[-10], yE=[-10], lW = [1])
    
    Nxy1_arrow_source.data = dict(xS=[8], xE=[8], yS=[0], yE=[0], lW = [3])
    Nxy2_arrow_source.data = dict(xS=[0], xE=[0], yS=[8], yE=[8], lW = [3])
    Nxy3_arrow_source.data = dict(xS=[-7], xE=[-7], yS=[0], yE=[0], lW = [3])
    Nxy4_arrow_source.data = dict(xS=[0], xE=[0], yS=[-8], yE=[-8], lW = [3])
     
    ## Figure 3: Rotating plane
    Rotating_Plane_source.data = dict(x=[0], y=[0],angle =[0*(pi/180)],size = [75])

    ## Figure 2 
    Mohr_Circle_source.data = dict(x=[centreX], y=[0], radius=[radius])

    #OriginalPlane_line_source.data = dict(x=[Ny,Ny,Nx,Nx], y=[0,-Nxy,Nxy,0])
    OriginalPlane_line_source.data = dict(x=[rleft_x,Ny,Ny], y=[rleft_y,Nxy,0])

    #Newplane_line_source.data = dict(x=[Neta,Neta,Nzeta,Nzeta], y=[0,-Nzetaeta,Nzetaeta,0])
    Newplane_line_source.data = dict(x=[rleft_x,Neta,Neta], y=[rleft_y,Nzetaeta,0])
    
    Figure2Moving_Label_source.data = dict(x=[Nx,Ny,0],y=[-3,-3,Nxy],
                                           names =[u"\u03C3"u"\u2093", u"\u03C3"u"y","t"],
                                           colors=['#E37222','#E37222','#A2AD00'])

 


def NormalForceX(attr,old,new):
    global Nx
    Nx = new  
    if(new<0):
        NxP1_arrow_source.data  = dict(xS=[10-new], xE=[10], yS=[5], yE=[5], lW = [1])
        NxP2_arrow_source.data  = dict(xS=[10-new], xE=[10], yS=[0], yE=[0], lW = [1])
        NxP3_arrow_source.data  = dict(xS=[10-new], xE=[10], yS=[-5], yE=[-5], lW = [1])
        
        NxN1_arrow_source.data  = dict(xS=[-10+new], xE=[-10], yS=[5], yE=[5], lW = [1])  
        NxN2_arrow_source.data  = dict(xS=[-10+new], xE=[-10], yS=[0], yE=[0], lW = [1]) 
        NxN3_arrow_source.data  = dict(xS=[-10+new], xE=[-10], yS=[-5], yE=[-5], lW = [1]) 
        
    else:
        NxP1_arrow_source.data  = dict(xS=[10], xE=[10+new], yS=[5], yE=[5], lW = [1])
        NxP2_arrow_source.data  = dict(xS=[10], xE=[10+new], yS=[0], yE=[0], lW = [1])
        NxP3_arrow_source.data  = dict(xS=[10], xE=[10+new], yS=[-5], yE=[-5], lW = [1])

        NxN1_arrow_source.data  = dict(xS=[-10], xE=[-10-new], yS=[5], yE=[5], lW = [1])
        NxN2_arrow_source.data  = dict(xS=[-10], xE=[-10-new], yS=[0], yE=[0], lW = [1])
        NxN3_arrow_source.data  = dict(xS=[-10], xE=[-10-new], yS=[-5], yE=[-5], lW = [1])
        
    ChangeMohrCircle()
    ChangeRotatingPlane_Forces()
    
def NormalForceY(attr,old,new):
    global Ny   
    if(new<0):
        NyP1_arrow_source.data  = dict(xS=[5], xE=[5], yS=[10-new], yE=[10], lW = [1])
        NyP2_arrow_source.data  = dict(xS=[0], xE=[0], yS=[10-new], yE=[10], lW = [1])
        NyP3_arrow_source.data  = dict(xS=[-5], xE=[-5], yS=[10-new], yE=[10], lW = [1])
        
        NyN1_arrow_source.data  = dict(xS=[5], xE=[5], yS=[-10+new], yE=[-10], lW = [1])
        NyN2_arrow_source.data  = dict(xS=[0], xE=[0], yS=[-10+new], yE=[-10], lW = [1])
        NyN3_arrow_source.data  = dict(xS=[-5], xE=[-5], yS=[-10+new], yE=[-10], lW = [1])

    else:
        NyP1_arrow_source.data  = dict(xS=[5], xE=[5], yS=[10], yE=[10+new], lW = [1])
        NyP2_arrow_source.data  = dict(xS=[0], xE=[0], yS=[10], yE=[10+new], lW = [1])
        NyP3_arrow_source.data  = dict(xS=[-5], xE=[-5], yS=[10], yE=[10+new], lW = [1])
        
        NyN1_arrow_source.data  = dict(xS=[5], xE=[5], yS=[-10], yE=[-10-new], lW = [1])
        NyN2_arrow_source.data  = dict(xS=[0], xE=[0], yS=[-10], yE=[-10-new], lW = [1])
        NyN3_arrow_source.data  = dict(xS=[-5], xE=[-5], yS=[-10], yE=[-10-new], lW = [1])
       
    Ny = new
    ChangeMohrCircle()
    ChangeRotatingPlane_Forces()
    
def TangentialXY(attr,old,new):
    global Nxy     
    if(new<0):
         Nxy1_arrow_source.data = dict(xS=[8], xE=[8], yS=[0-(new/2)], yE=[0+(new/2)], lW = [3])
         Nxy2_arrow_source.data = dict(xS=[-8], xE=[-8], yS=[0+(new/2)], yE=[0-(new/2)], lW = [3])
         Nxy3_arrow_source.data = dict(xS=[-new/2], xE=[new/2], yS=[8], yE=[8], lW = [3])
         Nxy4_arrow_source.data = dict(xS=[(new/2)], xE=[(-new/2)], yS=[-8], yE=[-8], lW = [3])
    else:     
         Nxy1_arrow_source.data = dict(xS=[8], xE=[8], yS=[0-(new/2)], yE=[0+(new/2)], lW = [3])
         Nxy2_arrow_source.data = dict(xS=[-8], xE=[-8], yS=[0+(new/2)], yE=[0-(new/2)], lW = [3])
         Nxy3_arrow_source.data = dict(xS=[-new/2], xE=[new/2], yS=[8], yE=[8], lW = [3])
         Nxy4_arrow_source.data = dict(xS=[(new/2)], xE=[-(new/2)], yS=[-8], yE=[-8], lW = [3])   
    Nxy = new
    ChangeMohrCircle()
    ChangeRotatingPlane_Forces()
        
def changePlaneAngle(attr,old,new):
     global P_Angle
     #P_Angle = new*(pi/180)
     P_Angle = -new*(pi/180)
     Rotating_Plane_source.data = dict(x=[0], y=[0],angle =[-P_Angle],size = [75])
     ChangeMohrCircle()
     ChangeRotatingPlane_Forces()
        
def ChangeMohrCircle():
    global P_Angle
    radius = float(sqrt(pow(((Nx-Ny)/2),2)+pow(Nxy,2)))
    centreX = float((Nx+Ny)/2)
    rleft_y=0
    rleft_x=centreX-radius
    Mohr_Circle_source.data = dict(x=[centreX], y=[0], radius=[radius])   
    #OriginalPlane_line_source.data = dict(x=[Ny,Ny,Nx,Nx], y=[0,-Nxy,Nxy,0])
    OriginalPlane_line_source.data = dict(x=[rleft_x,Ny,Ny], y=[rleft_y,Nxy,0])
  
    ## Calculate forces in rotated element
    Nzeta = float(((Nx+Ny)/2)+(((Nx-Ny)/2)*cos(2*P_Angle))+Nxy*sin(2*P_Angle))
    Neta  = float(((Nx+Ny)/2)-(((Nx-Ny)/2)*cos(2*P_Angle))-Nxy*sin(2*P_Angle))
    Nzetaeta = float((-(((Nx-Ny)/2)*sin(2*P_Angle)))+Nxy*cos(2*P_Angle))
    if P_Angle == 0:
        Nzeta = Nx
        Neta  = Ny
        Nzetaeta =Nxy
    if P_Angle == (pi/2):
        Nzeta = Ny
        Neta  = Nx
        Nzetaeta =-Nxy
    
    #Newplane_line_source.data = dict(x=[Neta,Neta,Nzeta,Nzeta], y=[0,-Nzetaeta,Nzetaeta,0])
    Newplane_line_source.data = dict(x=[rleft_x,Neta,Neta], y=[rleft_y,Nzetaeta,0])
    
    Figure2Moving_Label_source.data = dict(x=[Nx,Ny,0],y=[-5,-5,Nxy],
                                           names =[u"\u03C3"u"\u2093", u"\u03C3"u"y","t"],
                                           colors=['#E37222','#E37222','#E37222'])

def ChangeRotatingPlane_Forces():
    
    global Nx,Ny,Nxy
    Nzeta = float(float((Nx+Ny)/2)+(float((Nx-Ny)/2)*cos(2*P_Angle))+float(Nxy*sin(2*P_Angle)))
    Neta  = float(float((Nx+Ny)/2)-(float((Nx-Ny)/2)*cos(2*P_Angle))-float(Nxy*sin(2*P_Angle)))
    Nzetaeta = float((-(((Nx-Ny)/2)*sin(2*P_Angle)))+Nxy*cos(2*P_Angle))
    
    global P_Angle
    P_Angle=-P_Angle

    if Nzeta>0:
        NzetaP1_arrow_source.data = dict(xS=[10*cos(P_Angle)], xE=[(10+Nzeta)*cos(P_Angle)], yS=[5+(5*sin(P_Angle))], yE=[5+((5+Nzeta)*sin(P_Angle))], lW = [3])
        NzetaP2_arrow_source.data = dict(xS=[10*cos(P_Angle)], xE=[(10+Nzeta)*cos(P_Angle)], yS=[0+(5*sin(P_Angle))], yE=[0+((5+Nzeta)*sin(P_Angle))], lW = [3])
        NzetaP3_arrow_source.data = dict(xS=[10*cos(P_Angle)], xE=[(10+Nzeta)*cos(P_Angle)], yS=[-5+(5*sin(P_Angle))], yE=[-5+((5+Nzeta)*sin(P_Angle))], lW = [3])
        
        NzetaN1_arrow_source.data = dict(xS=[-10*cos(P_Angle)], xE=[(-10-Nzeta)*cos(P_Angle)], yS=[5-(5*sin(P_Angle))], yE=[(5-((5+Nzeta)*sin(P_Angle)))], lW = [3])
        NzetaN2_arrow_source.data = dict(xS=[-10*cos(P_Angle)], xE=[(-10-Nzeta)*cos(P_Angle)], yS=[0-(5*sin(P_Angle))], yE=[(0-((5+Nzeta)*sin(P_Angle)))], lW = [3])
        NzetaN3_arrow_source.data = dict(xS=[-10*cos(P_Angle)], xE=[(-10-Nzeta)*cos(P_Angle)], yS=[-5-(5*sin(P_Angle))], yE=[(-5-((5+Nzeta)*sin(P_Angle)))], lW = [53])
      
    else:
        NzetaP1_arrow_source.data = dict(xS=[(10-Nzeta)*cos(P_Angle)], xE=[10*cos(P_Angle)], yS=[5+((5-Nzeta)*sin(P_Angle))], yE=[5+(5*sin(P_Angle))], lW = [3])
        NzetaP2_arrow_source.data = dict(xS=[(10-Nzeta)*cos(P_Angle)], xE=[10*cos(P_Angle)], yS=[0+((5-Nzeta)*sin(P_Angle))], yE=[0+(5*sin(P_Angle))], lW = [3])
        NzetaP3_arrow_source.data = dict(xS=[(10-Nzeta)*cos(P_Angle)], xE=[10*cos(P_Angle)], yS=[-5+((5-Nzeta)*sin(P_Angle))], yE=[-5+(5*sin(P_Angle))], lW = [3])
        
        NzetaN1_arrow_source.data = dict(xS=[(-10+Nzeta)*cos(P_Angle)], xE=[-10*cos(P_Angle)], yS=[(5-((5-Nzeta)*sin(P_Angle)))], yE=[5-(5*sin(P_Angle))], lW = [3])
        NzetaN2_arrow_source.data = dict(xS=[(-10+Nzeta)*cos(P_Angle)], xE=[-10*cos(P_Angle)], yS=[(0-((5-Nzeta)*sin(P_Angle)))], yE=[0-(5*sin(P_Angle))], lW = [3])
        NzetaN3_arrow_source.data = dict(xS=[(-10+Nzeta)*cos(P_Angle)], xE=[-10*cos(P_Angle)], yS=[(-5-((5-Nzeta)*sin(P_Angle)))], yE=[-5-(5*sin(P_Angle))], lW = [3])
    
    if Neta>0:
        NetaP1_arrow_source.data = dict(xS=[5*cos((pi/2)+P_Angle)], xE=[(5+Neta)*cos((pi/2)+P_Angle)], yS=[10+(5*sin((pi/2)+P_Angle))], yE=[10+((5+Neta)*sin((pi/2)+P_Angle))], lW = [3])
        NetaP2_arrow_source.data = dict(xS=[0*cos((pi/2)+P_Angle)], xE=[(0+Neta)*cos((pi/2)+P_Angle)], yS=[10+(5*sin((pi/2)+P_Angle))], yE=[10+((5+Neta)*sin((pi/2)+P_Angle))], lW = [3])
        NetaP3_arrow_source.data = dict(xS=[-5*cos((pi/2)+P_Angle)], xE=[(-5+Neta)*cos((pi/2)+P_Angle)], yS=[10+(5*sin((pi/2)+P_Angle))], yE=[10+((5+Neta)*sin((pi/2)+P_Angle))], lW = [3])
        
        NetaN1_arrow_source.data =  dict(xS=[5*cos((3*pi/2)+P_Angle)], xE=[(5+Neta)*cos((3*pi/2)+P_Angle)], yS=[-10+(5*sin((3*pi/2)+P_Angle))], yE=[-10+((5+Neta)*sin((3*pi/2)+P_Angle))], lW = [3])      
        NetaN2_arrow_source.data =  dict(xS=[0*cos((3*pi/2)+P_Angle)], xE=[(0+Neta)*cos((3*pi/2)+P_Angle)], yS=[-10+(5*sin((3*pi/2)+P_Angle))], yE=[-10+((5+Neta)*sin((3*pi/2)+P_Angle))], lW = [3])      
        NetaN3_arrow_source.data =  dict(xS=[-5*cos((3*pi/2)+P_Angle)], xE=[(-5+Neta)*cos((3*pi/2)+P_Angle)], yS=[-10+(5*sin((3*pi/2)+P_Angle))], yE=[-10+((5+Neta)*sin((3*pi/2)+P_Angle))], lW = [3])      

    else:
        NetaP1_arrow_source.data = dict(xS=[(10-Neta)*cos((pi/2)+P_Angle)],xE=[10*cos((pi/2)+P_Angle)],yS=[5+((5-Neta)*sin((pi/2)+P_Angle))], yE=[5+(5*sin((pi/2)+P_Angle))],  lW = [3])
        NetaP2_arrow_source.data = dict(xS=[(10-Neta)*cos((pi/2)+P_Angle)],xE=[10*cos((pi/2)+P_Angle)],yS=[0+((5-Neta)*sin((pi/2)+P_Angle))], yE=[0+(5*sin((pi/2)+P_Angle))],  lW = [3])
        NetaP3_arrow_source.data = dict(xS=[(10-Neta)*cos((pi/2)+P_Angle)],xE=[10*cos((pi/2)+P_Angle)],yS=[-5+((5-Neta)*sin((pi/2)+P_Angle))], yE=[-5+(5*sin((pi/2)+P_Angle))],  lW = [3])
        
        NetaN1_arrow_source.data = dict(xS=[(10-Neta)*cos((3*pi/2)+P_Angle)],xE=[10*cos((3*pi/2)+P_Angle)], yS=[5+((5-Neta)*sin((3*pi/2)+P_Angle))],yE=[5+(5*sin((3*pi/2)+P_Angle))], lW = [3])      
        NetaN2_arrow_source.data = dict(xS=[(10-Neta)*cos((3*pi/2)+P_Angle)],xE=[10*cos((3*pi/2)+P_Angle)], yS=[0+((5-Neta)*sin((3*pi/2)+P_Angle))],yE=[0+(5*sin((3*pi/2)+P_Angle))], lW = [3])      
        NetaN3_arrow_source.data = dict(xS=[(10-Neta)*cos((3*pi/2)+P_Angle)],xE=[10*cos((3*pi/2)+P_Angle)], yS=[-5+((5-Neta)*sin((3*pi/2)+P_Angle))],yE=[-5+(5*sin((3*pi/2)+P_Angle))], lW = [3])      
  
    if Nzetaeta>0:
        Nzetaeta1_arrow_source.data = dict(xS=[8*cos(P_Angle)+((Nzetaeta/2)*sin(P_Angle))], xE=[8*cos(P_Angle)-((Nzetaeta/2)*sin(P_Angle))], yS=[(0+5*sin(P_Angle))-((Nzetaeta/2)*cos(P_Angle))], yE=[(0+5*sin(P_Angle))+((Nzetaeta/2)*cos(P_Angle))], lW = [5])
        Nzetaeta2_arrow_source.data = dict(xS=[-8*sin(P_Angle)-((Nzetaeta/2)*cos(P_Angle))], xE=[-8*sin(P_Angle)+((Nzetaeta/2)*cos(P_Angle))], yS=[(0+5*cos(P_Angle))-((Nzetaeta/2)*sin(P_Angle))], yE=[(0+5*cos(P_Angle))+((Nzetaeta/2)*sin(P_Angle))], lW = [5])
        Nzetaeta3_arrow_source.data = dict(xS=[-8*cos(P_Angle)-((Nzetaeta/2)*sin(P_Angle))], xE=[-8*cos(P_Angle)+((Nzetaeta/2)*sin(P_Angle))], yS=[(0-5*sin(P_Angle))+((Nzetaeta/2)*cos(P_Angle))], yE=[(0-5*sin(P_Angle))-((Nzetaeta/2)*cos(P_Angle))], lW = [5])
        Nzetaeta4_arrow_source.data = dict(xS=[8*sin(P_Angle)+((Nzetaeta/2)*cos(P_Angle))], xE=[8*sin(P_Angle)-((Nzetaeta/2)*cos(P_Angle))], yS=[(0-5*cos(P_Angle))+((Nzetaeta/2)*sin(P_Angle))], yE=[(0-5*cos(P_Angle))-((Nzetaeta/2)*sin(P_Angle))], lW = [5])
    else:
        Nzetaeta1_arrow_source.data = dict(xS=[8*cos(P_Angle)+((Nzetaeta/2)*sin(P_Angle))], xE=[8*cos(P_Angle)-((Nzetaeta/2)*sin(P_Angle))], yS=[(0+5*sin(P_Angle))-((Nzetaeta/2)*cos(P_Angle))], yE=[(0+5*sin(P_Angle))+((Nzetaeta/2)*cos(P_Angle))], lW = [5])
        Nzetaeta2_arrow_source.data = dict(xS=[-8*sin(P_Angle)-((Nzetaeta/2)*cos(P_Angle))], xE=[-8*sin(P_Angle)+((Nzetaeta/2)*cos(P_Angle))], yS=[(0+5*cos(P_Angle))-((Nzetaeta/2)*sin(P_Angle))], yE=[(0+5*cos(P_Angle))+((Nzetaeta/2)*sin(P_Angle))], lW = [5])
        Nzetaeta3_arrow_source.data = dict(xS=[-8*cos(P_Angle)-((Nzetaeta/2)*sin(P_Angle))], xE=[-8*cos(P_Angle)+((Nzetaeta/2)*sin(P_Angle))], yS=[(0-5*sin(P_Angle))+((Nzetaeta/2)*cos(P_Angle))], yE=[(0-5*sin(P_Angle))-((Nzetaeta/2)*cos(P_Angle))], lW = [5])
        Nzetaeta4_arrow_source.data = dict(xS=[8*sin(P_Angle)+((Nzetaeta/2)*cos(P_Angle))], xE=[8*sin(P_Angle)-((Nzetaeta/2)*cos(P_Angle))], yS=[(0-5*cos(P_Angle))+((Nzetaeta/2)*sin(P_Angle))], yE=[(0-5*cos(P_Angle))-((Nzetaeta/2)*sin(P_Angle))], lW = [5])
        P_Angle=-P_Angle


   

### Figure 1: Plotting Arrows
NxP1_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NxP1_arrow_source,line_color="#E37222")
NxP2_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NxP2_arrow_source,line_color="#E37222")
NxP3_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NxP3_arrow_source,line_color="#E37222")

NxN1_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NxN1_arrow_source,line_color="#E37222")
NxN2_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NxN2_arrow_source,line_color="#E37222")
NxN3_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NxN3_arrow_source,line_color="#E37222")

NyP1_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NyP1_arrow_source,line_color="#E37222")
NyP2_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NyP2_arrow_source,line_color="#E37222")
NyP3_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NyP3_arrow_source,line_color="#E37222")

NyN1_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NyN1_arrow_source,line_color="#E37222")
NyN2_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NyN2_arrow_source,line_color="#E37222")
NyN3_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NyN3_arrow_source,line_color="#E37222")

Nxy1_arrow_glyph = Arrow(end=OpenHead(line_color="#0065BD",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nxy1_arrow_source,line_color="#0065BD")

Nxy2_arrow_glyph = Arrow(end=OpenHead(line_color="#0065BD",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nxy2_arrow_source,line_color="#0065BD")

Nxy3_arrow_glyph = Arrow(end=OpenHead(line_color="#0065BD",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nxy3_arrow_source,line_color="#0065BD")

Nxy4_arrow_glyph = Arrow(end=OpenHead(line_color="#0065BD",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nxy4_arrow_source,line_color="#0065BD")

### Figure 3: Plotting Arrows
Rotating_Plane_glyph = Square(x='x',y='y',angle='angle',size='size', fill_color = '#c3c3c3')

NzetaP1_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NzetaP1_arrow_source,line_color="#E37222")
NzetaP2_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NzetaP2_arrow_source,line_color="#E37222")
NzetaP3_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NzetaP3_arrow_source,line_color="#E37222")

NzetaN1_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NzetaN1_arrow_source,line_color="#E37222")
NzetaN2_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NzetaN2_arrow_source,line_color="#E37222")
NzetaN3_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NzetaN3_arrow_source,line_color="#E37222")

NetaP1_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NetaP1_arrow_source,line_color="#E37222")
NetaP2_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NetaP2_arrow_source,line_color="#E37222")
NetaP3_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NetaP3_arrow_source,line_color="#E37222")

NetaN1_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NetaN1_arrow_source,line_color="#E37222")
NetaN2_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NetaN2_arrow_source,line_color="#E37222")
NetaN3_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 3, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NetaN3_arrow_source,line_color="#E37222")


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
figure1.square([0], [0], size=75, color='#c3c3c3', alpha=0.5)

figure1.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=0, y_start=0, x_end=25, y_end=0))
figure1.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=0, y_start=0, x_end=0, y_end=-25))

figure1.add_layout(NxP1_arrow_glyph)
figure1.add_layout(NxP2_arrow_glyph)
figure1.add_layout(NxP3_arrow_glyph)

figure1.add_layout(NxN1_arrow_glyph)
figure1.add_layout(NxN2_arrow_glyph)
figure1.add_layout(NxN3_arrow_glyph)

figure1.add_layout(NyP1_arrow_glyph)
figure1.add_layout(NyP2_arrow_glyph)
figure1.add_layout(NyP3_arrow_glyph)

figure1.add_layout(NyN1_arrow_glyph)
figure1.add_layout(NyN2_arrow_glyph)
figure1.add_layout(NyN3_arrow_glyph)

figure1.add_layout(Nxy1_arrow_glyph)
figure1.add_layout(Nxy2_arrow_glyph)
figure1.add_layout(Nxy3_arrow_glyph)
figure1.add_layout(Nxy4_arrow_glyph)

figure1_labels = LabelSet(x='x', y='y', text='names', level='glyph',
              x_offset=5, y_offset=5, source=Figure1Perm_Label_source, render_mode='canvas')
figure1.add_layout(figure1_labels)

### Figure 3: Define dimensions
figure3 = figure(title="Stress State B", tools="", x_range=(-30,30), y_range=(-30,30),width=400,height=400)

### Figure 3: Add geometry
figure3.square([0], [0], size=75, color='#c3c3c3', alpha=0.5)
figure3.add_layout(NzetaP1_arrow_glyph)
figure3.add_layout(NzetaP2_arrow_glyph)
figure3.add_layout(NzetaP3_arrow_glyph)

figure3.add_layout(NzetaN1_arrow_glyph)
figure3.add_layout(NzetaN2_arrow_glyph)
figure3.add_layout(NzetaN3_arrow_glyph)

figure3.add_layout(NetaP1_arrow_glyph)
figure3.add_layout(NetaP2_arrow_glyph)
figure3.add_layout(NetaP3_arrow_glyph)

figure3.add_layout(NetaN1_arrow_glyph)
figure3.add_layout(NetaN2_arrow_glyph)
figure3.add_layout(NetaN3_arrow_glyph)

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
figure2.line(x='x',y='y',source= OriginalPlane_line_source, color='#E37222', line_width=3, line_join = 'bevel')
#Originalkreuze
figure2.circle(x='x',y='y',source= OriginalPlane_line_source, size=4, color='#E37222')

#Gedrehte Linie
figure2.line(x='x',y='y',source= Newplane_line_source, color="#A2AD00", line_width=3, line_join = 'bevel')
#Gedrehte kreuze
figure2.circle(x='x',y='y',source= Newplane_line_source, size=4, color="#A2AD00")

figure2.x(x=Nx,y=Ny, size=6, color='black')



figure2_labels1 = LabelSet(x='x', y='y', text='names', level='glyph',
              x_offset=5, y_offset=5, source=Figure2Perm_Label_source, render_mode='canvas')
figure2_labels2 = LabelSet(x='x', y='y', text='names', level='glyph', x_offset=5, y_offset=5,
                           source=Figure2Moving_Label_source, render_mode='canvas',
                           text_color = 'black', background_fill_color='colors')
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

Normal_Y_slider= Slider(title="Normal force in Y direction (N)",value= 0,start = -10, end = 10, step = 0.5)
Normal_Y_slider.on_change('value',NormalForceY)

Tangential_XY_slider= Slider(title="Shear force (N)",value= 0,start = 0, end = 10, step = 0.5)
Tangential_XY_slider.on_change('value',TangentialXY)

Plane_Angle_slider= Slider(title="Angle of cross section (º)",value= 0,start = 0, end = 90, step = 0.5)
Plane_Angle_slider.on_change('value',changePlaneAngle)


### Adding description from HTML file
description_filename = join(dirname(__file__), "description.html")
description = Div(text=open(description_filename).read(), render_as_text=False, width=1200)

curdoc().add_root(column(description,row(column(figure1,Normal_X_slider,Normal_Y_slider, Tangential_XY_slider),figure2,column(figure3, Plane_Angle_slider))))
curdoc().title = "Mohr Circle"

