# -*- coding: utf-8 -*-
"""
Created on Wed,13.06.2018

@author: Sascha Kubisch
refactored by Matthias Ebert
"""

"""
Python Bokeh program which explains the concept of Mohr's Cirlce interactively

"""
from bokeh.plotting import figure
from bokeh.layouts import column, row, layout
from bokeh.models import Arrow,OpenHead,NormalHead,Button
from bokeh.models.markers import Square,Circle
from bokeh.models.glyphs import Wedge,Rect
from bokeh.models.layouts import Spacer
from bokeh.io import curdoc

from math import pi,sqrt,pow,atan 

from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexDiv, LatexLabel, LatexLabelSet, LatexSlider, LatexLegend

# external files
import Mohr_Variables as Mvar
from Mohr_ChangeFunctions import changePlaneAngle
from Mohr_Draw import draw

###Initial Calculations and Value settings
def init():
    Normal_X_slider.value=0
    Normal_Z_slider.value=0
    Tangential_XZ_slider.value=0
    Plane_Angle_slider.value=0

    ## Figure 1: Set values for arrows
    #Mvar.NxP_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.NxP_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    #Mvar.NxN_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.NxN_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    #Mvar.NzP_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.NzP_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    #Mvar.NzN_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.NzN_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    #Mvar.Nxz1_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.Nxz1_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    #Mvar.Nxz2_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.Nxz2_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    #Mvar.Nxz3_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.Nxz3_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    #Mvar.Nxz4_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.Nxz4_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    ##Figure 1, Set Rectangles:
    Mvar.NxP_rect_source.data   = dict(x=[], y=[], w=[], h=[], angle=[])
    Mvar.NxN_rect_source.data   = dict(x=[], y=[], w=[], h=[], angle=[])
    Mvar.NzP_rect_source.data   = dict(x=[], y=[], w=[], h=[], angle=[])
    Mvar.NxN_rect_source.data   = dict(x=[], y=[], w=[], h=[], angle=[])
    Mvar.Nxz1_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
    Mvar.Nxz2_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
    Mvar.Nxz3_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
    Mvar.Nxz4_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
    
def reset():
    Normal_X_slider.disabled        = False
    Normal_Z_slider.disabled        = False
    Tangential_XZ_slider.disabled   = False
    Plane_Angle_slider.disabled     = True

    Mvar.glob_MohrChangeShow.data   = dict(val=[-1])         #      /output
    Mvar.glob_NzetaI0.data          = dict(val=[0])          #      /output
    Mvar.glob_NetaI0.data           = dict(val=[0])          #      /output
    
    Mvar.glob_alpha.data            = dict(val=[0])          #      /output
    Mvar.glob_MohrP_Angle.data      = dict(val=[0*(pi/180)]) #      /output
   
    radius    = 0 #10
    centreX   = 0 #10
    Mvar.glob_MohrNx.data  = dict(val=[0]) #      /output
    Mvar.glob_MohrNz.data  = dict(val=[0]) #      /output
    Mvar.glob_MohrNxz.data = dict(val=[0]) #      /output
    
    ### Calculations
    #radius    = float(sqrt(pow(((glMohrNx-glMohrNz)/2),2)+pow(glMohrNxz,2)))
    #centreX   = float((glMohrNx+glMohrNz)/2)

    Normal_X_slider.value      = 0
    Normal_Z_slider.value      = 0
    Tangential_XZ_slider.value = 0
    Plane_Angle_slider.value   = 0

    ### Figure 1, Reset values for arrows:
    #Mvar.NxP_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.NxP_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    #Mvar.NxN_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.NxN_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    #Mvar.NzP_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.NzP_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    #Mvar.NzN_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.NzN_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    #Mvar.Nxz1_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.Nxz1_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    #Mvar.Nxz2_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.Nxz2_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    #Mvar.Nxz3_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.Nxz3_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    #Mvar.Nxz4_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.Nxz4_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    ## Figure 1, Reset Rectangles:
    Mvar.NxP_rect_source.data   = dict(x=[], y=[], w=[], h=[], angle=[])
    Mvar.NxN_rect_source.data   = dict(x=[], y=[], w=[], h=[], angle=[])
    Mvar.NzP_rect_source.data   = dict(x=[], y=[], w=[], h=[], angle=[])
    Mvar.NzN_rect_source.data   = dict(x=[], y=[], w=[], h=[], angle=[])
    Mvar.Nxz1_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
    Mvar.Nxz2_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
    Mvar.Nxz3_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
    Mvar.Nxz4_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
    
    ### Figure 2, Reset Circle:
    Mvar.Mohr_Circle_source.data          = dict(x=[centreX], y=[0], radius=[radius])
    Mvar.Newplane_line_source.data        = dict(x=[], y=[])
    Mvar.OriginalPlane_line_source.data   = dict(x=[], y=[])
    Mvar.Figure2Moving_Label_source.data  = dict(x=[],y=[],names =[])
    Mvar.Figure2Show_Label_source.data    = dict(x=[],y=[],names =[])
    Mvar.Wedge_source.data                = dict(x=[], y=[],radius=[], sA=[], eA=[])
    glMohrFigure2_angle_label.text = ''

    ## Figure 3, Reset rotating plane:
    Mvar.Rotating_Plane_source.data     = dict(x=[], y=[],angle =[],size = [])
    Mvar.Rotating_Plane_red_source.data = dict(x=[], y=[],angle =[],size = [])
    ## Figure 3, Reset arrows:
    #Mvar.NxP_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.NxP_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    #Mvar.NxN_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.NxN_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    #Mvar.NzP_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.NzP_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    #Mvar.NzN_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.NzN_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    #Mvar.Nxz1_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.Nxz1_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    #Mvar.Nxz2_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.Nxz2_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    #Mvar.Nxz3_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.Nxz3_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    #Mvar.Nxz4_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    Mvar.Nxz4_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
    ## Figure 3, Reset rectangles:
    Mvar.NzetaP_rect_source.data    = dict(x=[], y=[], w=[], h=[], angle=[])
    Mvar.NzetaN_rect_source.data    = dict(x=[], y=[], w=[], h=[], angle=[])
    Mvar.NetaP_rect_source.data     = dict(x=[], y=[], w=[], h=[], angle=[])
    Mvar.NetaN_rect_source.data     = dict(x=[], y=[], w=[], h=[], angle=[])
    Mvar.Nzetaeta1_rect_source.data = dict(x=[], y=[], w=[], h=[], angle=[])
    Mvar.Nzetaeta2_rect_source.data = dict(x=[], y=[], w=[], h=[], angle=[])
    Mvar.Nzetaeta3_rect_source.data = dict(x=[], y=[], w=[], h=[], angle=[])
    Mvar.Nzetaeta4_rect_source.data = dict(x=[], y=[], w=[], h=[], angle=[])
    ## Figure 3, Reset rotating axis:
    Mvar.Rotating_Axis_X_source.data     = dict(xS=[], yS=[], xE=[], yE=[])
    Mvar.Rotating_Axis_Y_source.data     = dict(xS=[], yS=[], xE=[], yE=[])
    Mvar.Figure3Moving_Label_source.data = dict(x=[], y=[], names =[])
    
def show():
    [glMohrChangeShow] = Mvar.glob_MohrChangeShow.data["val"] # input/output
    [glMohrNx]         = Mvar.glob_MohrNx.data["val"]         # input/
    [glMohrNz]         = Mvar.glob_MohrNz.data["val"]         # input/
    [glMohrNxz]        = Mvar.glob_MohrNxz.data["val"]        # input/
    if glMohrChangeShow == 1:
        radius   = float(sqrt(pow(((glMohrNx-glMohrNz)/2),2)+pow(glMohrNxz,2)))
        centreX  = float((glMohrNx+glMohrNz)/2)
        Mvar.rleft_x  = centreX-radius
        rright_x      = centreX+radius

        ## Print Labels for principal stress and direction
        alpha = 180*atan(glMohrNxz/(glMohrNz+(-Mvar.rleft_x+0.00001)))/(pi)
        alpha = int(alpha+0.5)
        Mvar.Figure2Show_Label_source.data = dict(x=[Mvar.rleft_x,rright_x,centreX],
                                                y=[0,0,0],
                                                names=['\\sigma_{II}','\\sigma_{I}','\\sigma_{M}'])
        Mvar.Wedge_source.data = dict(x=[Mvar.rleft_x], y=[0],radius=[radius/2], sA=[atan(glMohrNxz/(glMohrNz+(-Mvar.rleft_x)))], eA=[0])
        glMohrFigure2_angle_label.text = '\\alpha_0=' + str(alpha)
        glMohrChangeShow = glMohrChangeShow*-1

    elif glMohrChangeShow == -1:
        
        Mvar.Wedge_source.data                = dict(x=[], y=[],radius=[], sA=[], eA=[])
        Mvar.Figure2Show_Label_source.data    = dict(x=[], y=[], names =[])
        glMohrFigure2_angle_label.text = ''
        glMohrChangeShow = glMohrChangeShow*-1
        
    Mvar.glob_MohrChangeShow.data = dict(val=[glMohrChangeShow])

def draw_main():
    Normal_X_slider.disabled      = True
    Normal_Z_slider.disabled      = True
    Tangential_XZ_slider.disabled = True
    Plane_Angle_slider.disabled   = False
    draw()

def NormalForceX_init(attr,old,new):
   ## Figure 1, Present the Normal Forces while Draw-Button wasn't yet activated:  
        Mvar.glob_MohrNx.data = dict(val=[new]) #      /output
        new = new*0.75
        if(new<0):
            #Mvar.NxP_arrow_source.data = dict(xS=[12.5-new],  xE=[12.5],  yS=[0], yE=[0], lW = [2])
            Mvar.NxP_arrow_source.stream(dict(xS=[12.5-new],  xE=[12.5],  yS=[0], yE=[0], lW = [2]),rollover=1)
            #Mvar.NxN_arrow_source.data = dict(xS=[-12.5+new], xE=[-12.5], yS=[0], yE=[0], lW = [2]) 
            Mvar.NxN_arrow_source.stream(dict(xS=[-12.5+new], xE=[-12.5], yS=[0], yE=[0], lW = [2]),rollover=1)
     
            Mvar.NxP_rect_source.data  = dict(x=[(25-new)/2],  y=[0], w=[new-1.5], h = [13], angle=[0])
            Mvar.NxN_rect_source.data  = dict(x=[(-25+new)/2], y=[0], w=[new-1.5], h = [13], angle=[0]) 
        elif(new==0):
            #Mvar.NxP_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
            #Mvar.NxN_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
            Mvar.NxP_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
            Mvar.NxN_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)     
            Mvar.NxP_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])
            Mvar.NxN_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])

        else:
            #Mvar.NxP_arrow_source.data  = dict(xS=[12.5],  xE=[12.5+new],  yS=[0], yE=[0], lW = [2])
            #Mvar.NxN_arrow_source.data  = dict(xS=[-12.5], xE=[-12.5-new], yS=[0], yE=[0], lW = [2])
            Mvar.NxN_arrow_source.stream(dict(xS=[12.5],  xE=[12.5+new],  yS=[0], yE=[0], lW = [2]),rollover=1)
            Mvar.NxN_arrow_source.stream(dict(xS=[-12.5], xE=[-12.5-new], yS=[0], yE=[0], lW = [2]),rollover=1)
            Mvar.NxP_rect_source.data   = dict(x=[(25+new)/2],  y=[0], w=[new+1.5], h = [13], angle=[0])        
            Mvar.NxN_rect_source.data   = dict(x=[(-25-new)/2], y=[0], w=[new+1.5], h = [13], angle=[0]) 
    
def NormalForceZ_init(attr,old,new):
    ## Figure 1, Present the Normal Forces while draw() hasn't been called yet:
        ## Global change of glMohrNz
        Mvar.glob_MohrNz.data = dict(val=[new]) #      /output
        new = new*0.75
        if(new<0):
            #Mvar.NzP_arrow_source.data = dict(xS=[0], xE=[0], yS=[12.5-new],  yE=[12.5],  lW = [2])
            #Mvar.NzN_arrow_source.data = dict(xS=[0], xE=[0], yS=[-12.5+new], yE=[-12.5], lW = [2])
            Mvar.NzP_arrow_source.stream(dict(xS=[0], xE=[0], yS=[12.5-new],  yE=[12.5],  lW = [2]),rollover=1)
            Mvar.NzN_arrow_source.stream(dict(xS=[0], xE=[0], yS=[-12.5+new], yE=[-12.5], lW = [2]),rollover=1)

            Mvar.NzP_rect_source.data  = dict(x=[0], y=[(25-new)/2],  w=[13], h = [new-1.5], angle=[0])
            Mvar.NzN_rect_source.data  = dict(x=[0], y=[(-25+new)/2], w=[13], h = [new-1.5], angle=[0])   
        elif (new==0):
           # Mvar.NzP_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
            #Mvar.NzN_arrow_source.data  = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
            Mvar.NzP_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
            Mvar.NzN_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
            Mvar.NzP_rect_source.data   = dict(x=[], y=[], w=[], h = [], angle=[])
            Mvar.NzN_rect_source.data   = dict(x=[], y=[], w=[], h = [], angle=[])
        else:
            #Mvar.NzP_arrow_source.data = dict(xS=[0], xE=[0], yS=[12.5],  yE=[12.5+new],  lW = [2])
            #Mvar.NzN_arrow_source.data = dict(xS=[0], xE=[0], yS=[-12.5], yE=[-12.5-new], lW = [2])
            Mvar.NzP_arrow_source.stream(dict(xS=[0], xE=[0], yS=[12.5],  yE=[12.5+new],  lW = [2]),rollover=1)
            Mvar.NzN_arrow_source.stream(dict(xS=[0], xE=[0], yS=[-12.5], yE=[-12.5-new], lW = [2]),rollover=1)
            Mvar.NzP_rect_source.data  = dict(x=[0], y=[(25+new)/2],  w=[13], h = [new+1.5], angle=[0])
            Mvar.NzN_rect_source.data  = dict(x=[0], y=[(-25-new)/2], w=[13], h = [new+1.5], angle=[0])   

def TangentialXZ_init(attr,old,new):
    ## Figure 1, Present the Shear Forces while draw() hasn't yet been called:
        ## global change of glMohrNxz    
        glMohrNxz = new

        # Check if glMohrNxz is zero to prevent division by zero:
        if glMohrNxz == 0:
            glMohrNxz = 0.00001
        Mvar.glob_MohrNxz.data = dict(val=[glMohrNxz]) #      /output
        
        new=new*0.75
            
        if(new==0):
            #Mvar.Nxz1_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
            #Mvar.Nxz2_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
            #Mvar.Nxz3_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
            #Mvar.Nxz4_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])    
            Mvar.Nxz1_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
            Mvar.Nxz2_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
            Mvar.Nxz3_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
            Mvar.Nxz4_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)        
            Mvar.Nxz1_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
            Mvar.Nxz2_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
            Mvar.Nxz3_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
            Mvar.Nxz4_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
    
        else:     
           # Mvar.Nxz1_arrow_source.data = dict(xS=[9],       xE=[9],        yS=[0-(new/2)], yE=[0+(new/2)], lW = [2])
           # Mvar.Nxz2_arrow_source.data = dict(xS=[-9],      xE=[-9],       yS=[0+(new/2)], yE=[0-(new/2)], lW = [2])
           # Mvar.Nxz3_arrow_source.data = dict(xS=[-new/2],  xE=[new/2],    yS=[9],         yE=[9],         lW = [2])
           # Mvar.Nxz4_arrow_source.data = dict(xS=[(new/2)], xE=[-(new/2)], yS=[-9],        yE=[-9],        lW = [2]) 
            Mvar.Nxz1_arrow_source.stream(dict(xS=[9],       xE=[9],        yS=[0-(new/2)], yE=[0+(new/2)], lW = [2]),rollover=1)
            Mvar.Nxz2_arrow_source.stream(dict(xS=[-9],      xE=[-9],       yS=[0+(new/2)], yE=[0-(new/2)], lW = [2]),rollover=1)
            Mvar.Nxz3_arrow_source.stream(dict(xS=[-new/2],  xE=[new/2],    yS=[9],         yE=[9],         lW = [2]),rollover=1)
            Mvar.Nxz4_arrow_source.stream(dict(xS=[(new/2)], xE=[-(new/2)], yS=[-9],        yE=[-9],        lW = [2]),rollover=1)         
            Mvar.Nxz1_rect_source.data  = dict(x=[9],  y=[0],  w=[0.3*new+0.5], h=[13],          angle=[0])
            Mvar.Nxz2_rect_source.data  = dict(x=[-9], y=[0],  w=[0.3*new+0.5], h=[13],          angle=[0])
            Mvar.Nxz3_rect_source.data  = dict(x=[0],  y=[9],  w=[13],          h=[0.3*new+0.5], angle=[0])
            Mvar.Nxz4_rect_source.data  = dict(x=[0],  y=[-9], w=[13],          h=[0.3*new+0.5], angle=[0])

   
### Figure 1, Define Geometry:
NxP_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Mvar.NxP_arrow_source,line_color="#E37222")
NxN_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Mvar.NxN_arrow_source,line_color="#E37222")
NzP_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Mvar.NzP_arrow_source,line_color="#E37222")
NzN_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Mvar.NzN_arrow_source,line_color="#E37222")
Nxz1_arrow_glyph = Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Mvar.Nxz1_arrow_source,line_color="#0065BD")
Nxz2_arrow_glyph = Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Mvar.Nxz2_arrow_source,line_color="#0065BD")
Nxz3_arrow_glyph = Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Mvar.Nxz3_arrow_source,line_color="#0065BD")
Nxz4_arrow_glyph = Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Mvar.Nxz4_arrow_source,line_color="#0065BD")
### Figure 1, Rectangle glyphs:
NxP_rect_glyph  = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#E37222", fill_alpha=0.5)
NxN_rect_glyph  = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#E37222", fill_alpha=0.5)
NzP_rect_glyph  = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#E37222", fill_alpha=0.5)
NzN_rect_glyph  = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#E37222", fill_alpha=0.5)
Nxz1_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#0065BD", fill_alpha=0.5)
Nxz2_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#0065BD", fill_alpha=0.5)
Nxz3_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#0065BD", fill_alpha=0.5)
Nxz4_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#0065BD", fill_alpha=0.5)

### Figure 1, Define Figure and add Geometry:
figure1 = figure(title="Stress State A", tools="save", x_range=(-30,30), y_range=(-30,30),width=400,height=400)
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
                                x_offset=0, y_offset=0, source=Mvar.Figure1Perm_Label_source)
figure1.add_layout(figure1_labels)
figure1.add_glyph(Mvar.NxP_rect_source,NxP_rect_glyph)
figure1.add_glyph(Mvar.NxN_rect_source,NxN_rect_glyph)
figure1.add_glyph(Mvar.NzP_rect_source,NzP_rect_glyph)
figure1.add_glyph(Mvar.NzN_rect_source,NzN_rect_glyph)
figure1.add_glyph(Mvar.Nxz1_rect_source,Nxz1_rect_glyph)
figure1.add_glyph(Mvar.Nxz2_rect_source,Nxz1_rect_glyph)
figure1.add_glyph(Mvar.Nxz3_rect_source,Nxz1_rect_glyph)
figure1.add_glyph(Mvar.Nxz4_rect_source,Nxz1_rect_glyph)

# dummy glyphs for the legend entries
dummy_normal_1 = figure1.square([0.0],[0.0],size=0,fill_color="#E37222",fill_alpha=0.5)
dummy_shear_1  = figure1.square([0.0],[0.0],size=0,fill_color="#0065BD",fill_alpha=0.5)

legend1 = LatexLegend(items=[
    ("\\text{Normal Stresses}\\ \\sigma_x, \\sigma_z", [dummy_normal_1]),
    ("\\text{Shear Stresses}\\ \\tau_{xz}", [dummy_shear_1]),
], location='top_left', max_label_width = 220)
figure1.add_layout(legend1)

### Figure 2: Define Geometry
Mohr_Circle_glyph = Circle(x='x',y='y',radius='radius', radius_dimension='y', fill_color='#c3c3c3', fill_alpha=0.5)
Wedge_glyph       = Wedge(x="x", y="y", radius="radius", start_angle="sA", end_angle="eA", fill_color="firebrick", fill_alpha=0.6, direction="clock")
### Figure 2: Define Figure and add Geometry
figure2 = figure(title="Mohr's Circle", tools="pan,save,wheel_zoom,reset", x_range=(-25.5,25.5), y_range=(-25.5,25.5),width=400,height=400, toolbar_location="right")
figure2.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=-23, y_start=0, x_end=23, y_end=0))
figure2.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=0, y_start=-23, x_end=0, y_end=23))
figure2.add_glyph(Mvar.Mohr_Circle_source,Mohr_Circle_glyph)
figure2.add_glyph(Mvar.Wedge_source,Wedge_glyph)
# Modified line
figure2.line(x='x',y='y',source= Mvar.Newplane_line_source, color="#A2AD00", line_width=3, line_join = 'bevel')
figure2.circle(x='x',y='y',source= Mvar.Newplane_line_source, size=4, color="black", alpha=0.4)
figure2.circle(x='x', y='y', source=Mvar.Figure2Moving_Label_source, size=5, color="black")
figure2.circle(x='x', y='y', source=Mvar.Figure2Show_Label_source, size=5, color="firebrick")
figure2_labels1 = LatexLabelSet(x='x', y='y', text='names', level='glyph', x_offset=0, y_offset=0, source=Mvar.Figure2Perm_Label_source)
figure2_labels2 = LatexLabelSet(x='x', y='y', text='names', source=Mvar.Figure2Moving_Label_source, text_color = 'black', level='glyph', x_offset=3, y_offset=3)
figure2_labels3 = LatexLabelSet(x='x', y='y', text='names', source=Mvar.Figure2Show_Label_source, text_color = 'firebrick', level='glyph', x_offset=3, y_offset=-15)
figure2.add_layout(figure2_labels1)
figure2.add_layout(figure2_labels2)
figure2.add_layout(figure2_labels3)
# Original line
figure2.line(x='x',y='y',source= Mvar.OriginalPlane_line_source, color="black", alpha=0.5, line_width=3, line_join = 'bevel')
figure2.circle(x='x',y='y',source= Mvar.OriginalPlane_line_source, size=4, color="black", alpha=0.4)
glMohrFigure2_angle_label = LatexLabel(text="",x=20,y=330,render_mode='css',text_color='firebrick', x_units='screen', y_units='screen')
figure2.add_layout(glMohrFigure2_angle_label)

### Figure 3: Define Geometry
Rotating_Plane_glyph = Square(x='x',y='y',angle='angle',size='size', fill_color = '#A2AD00', fill_alpha=0.5)
Rotating_Plane_red_glyph = Square(x='x',y='y',angle='angle',size='size', fill_color = 'firebrick', fill_alpha=0.5)

Rotating_Axis_X_glyph = Arrow(end=NormalHead(fill_color='#A2AD00', size=15), x_start='xS', y_start='yS', x_end='xE', y_end='yE', source=Mvar.Rotating_Axis_X_source )
Rotating_Axis_Y_glyph = Arrow(end=NormalHead(fill_color='#A2AD00', size=15), x_start='xS', y_start='yS', x_end='xE', y_end='yE', source=Mvar.Rotating_Axis_Y_source )

Mvar.NzetaP_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Mvar.NzetaP_arrow_source,line_color="#E37222")
Mvar.NzetaN_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Mvar.NzetaN_arrow_source,line_color="#E37222")
Mvar.NetaP_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Mvar.NetaP_arrow_source,line_color="#E37222")
Mvar.NetaN_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Mvar.NetaN_arrow_source,line_color="#E37222")
Mvar.Nzetaeta1_arrow_glyph= Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Mvar.Nzetaeta1_arrow_source,line_color="#0065BD")
Mvar.Nzetaeta2_arrow_glyph=Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Mvar.Nzetaeta2_arrow_source,line_color="#0065BD")
Mvar.Nzetaeta3_arrow_glyph= Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Mvar.Nzetaeta3_arrow_source,line_color="#0065BD")
Mvar.Nzetaeta4_arrow_glyph=Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Mvar.Nzetaeta4_arrow_source,line_color="#0065BD")
### Figure 3, Rectangle glyphs:
Mvar.NzetaP_rect_glyph    = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#E37222", fill_alpha=0.5)
Mvar.NzetaN_rect_glyph    = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#E37222", fill_alpha=0.5)
Mvar.NetaP_rect_glyph     = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#E37222", fill_alpha=0.5)
Mvar.NetaN_rect_glyph     = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#E37222", fill_alpha=0.5)
Mvar.Nzetaeta1_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#0065BD", fill_alpha=0.5)
Mvar.Nzetaeta2_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#0065BD", fill_alpha=0.5)
Mvar.Nzetaeta3_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#0065BD", fill_alpha=0.5)
Mvar.Nzetaeta4_rect_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#0065BD", fill_alpha=0.5)
### Figure 3, Define Figure and add Geometry:
figure3 = figure(title="Stress State B", tools="save", x_range=(-30,30), y_range=(-30,30),width=400,height=400,)
figure3.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=0, y_start=0, x_end=25, y_end=0))
figure3.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=0, y_start=0, x_end=0, y_end=-25))
figure3_labels  = LatexLabelSet(x='x', y='y', text='names', level='glyph', x_offset=5, y_offset=5, source=Mvar.Figure1Perm_Label_source)
figure3_labels2 = LatexLabelSet(x='x', y='y', text='names', source=Mvar.Figure3Moving_Label_source)


figure3.add_glyph(Mvar.Rotating_Plane_source,Rotating_Plane_glyph)
figure3.add_glyph(Mvar.Rotating_Plane_red_source,Rotating_Plane_red_glyph)
figure3.add_glyph(Mvar.NzetaP_rect_source,Mvar.NzetaP_rect_glyph)
figure3.add_glyph(Mvar.NzetaN_rect_source,Mvar.NzetaN_rect_glyph)
figure3.add_glyph(Mvar.NetaP_rect_source,Mvar.NetaP_rect_glyph)
figure3.add_glyph(Mvar.NetaN_rect_source,Mvar.NetaN_rect_glyph)
figure3.add_glyph(Mvar.Nzetaeta1_rect_source,Mvar.Nzetaeta1_rect_glyph)
figure3.add_glyph(Mvar.Nzetaeta2_rect_source,Mvar.Nzetaeta2_rect_glyph)
figure3.add_glyph(Mvar.Nzetaeta3_rect_source,Mvar.Nzetaeta3_rect_glyph)
figure3.add_glyph(Mvar.Nzetaeta4_rect_source,Mvar.Nzetaeta4_rect_glyph)
figure3.add_layout(figure3_labels)
figure3.add_layout(figure3_labels2)
figure3.add_layout(Mvar.NzetaP_arrow_glyph)
figure3.add_layout(Mvar.NzetaN_arrow_glyph)
figure3.add_layout(Mvar.NetaP_arrow_glyph)
figure3.add_layout(Mvar.NetaN_arrow_glyph)
figure3.add_layout(Mvar.Nzetaeta1_arrow_glyph)
figure3.add_layout(Mvar.Nzetaeta2_arrow_glyph)
figure3.add_layout(Mvar.Nzetaeta3_arrow_glyph)
figure3.add_layout(Mvar.Nzetaeta4_arrow_glyph)
figure3.add_layout(Rotating_Axis_X_glyph)
figure3.add_layout(Rotating_Axis_Y_glyph)

# dummy glyphs for the legend entries
dummy_normal_3 = figure3.square([0.0],[0.0],size=0,fill_color="#E37222",fill_alpha=0.5)
dummy_shear_3  = figure3.square([0.0],[0.0],size=0,fill_color="#0065BD",fill_alpha=0.5)

legend3 = LatexLegend(items=[
    ("\\text{Normal Stresses}\\ \\sigma_x, \\sigma_z", [dummy_normal_3]),
    ("\\text{Shear Stresses}\\ \\tau_{xz}", [dummy_shear_3]),
], location='top_left', max_label_width = 220)
figure3.add_layout(legend3)

### All figures, Turn off grids: 
figure1.xaxis.major_tick_line_color  = None
figure1.xaxis.major_label_text_color = None
figure1.xaxis.minor_tick_line_color  = None
figure1.xaxis.axis_line_color        = None
figure1.yaxis.major_tick_line_color  = None
figure1.yaxis.major_label_text_color = None
figure1.yaxis.minor_tick_line_color  = None
figure1.yaxis.axis_line_color        = None
figure1.xgrid.visible                = False
figure1.ygrid.visible                = False
figure1.toolbar.logo                 = None

figure2.xaxis.major_tick_line_color  = None
figure2.xaxis.major_label_text_color = None
figure2.xaxis.minor_tick_line_color  = None
figure2.xaxis.axis_line_color        = None
figure2.yaxis.major_tick_line_color  = None
figure2.yaxis.major_label_text_color = None
figure2.yaxis.minor_tick_line_color  = None
figure2.yaxis.axis_line_color        = None
figure2.xgrid.visible                = False
figure2.ygrid.visible                = False
figure2.toolbar.logo                 = None

figure3.xaxis.major_tick_line_color  = None
figure3.xaxis.major_label_text_color = None
figure3.xaxis.minor_tick_line_color  = None
figure3.xaxis.axis_line_color        = None
figure3.yaxis.major_tick_line_color  = None
figure3.yaxis.major_label_text_color = None
figure3.yaxis.minor_tick_line_color  = None
figure3.yaxis.axis_line_color        = None
figure3.xgrid.visible                = False
figure3.ygrid.visible                = False
figure3.toolbar.logo                 = None

### Create  sliders to change Normal and Tangential Forces
Normal_X_slider= LatexSlider(title="\\sigma_x=",value_unit='\\frac{\\mathrm{N}}{\\mathrm{mm}^2}',value= 0,start = -10, end = 10, step = 0.5)
Normal_X_slider.on_change('value',NormalForceX_init)

Normal_Z_slider= LatexSlider(title="\\sigma_z=",value_unit='\\frac{\\mathrm{N}}{\\mathrm{mm}^2}',value= 0,start = -10, end = 10, step = 0.5)
Normal_Z_slider.on_change('value',NormalForceZ_init)
   
Tangential_XZ_slider= LatexSlider(title="\\tau_{xz}=",value_unit='\\frac{\\mathrm{N}}{\\mathrm{mm}^2}',value= 0,start = 0, end = 10, step = 0.5)
Tangential_XZ_slider.on_change('value',TangentialXZ_init)
    
Plane_Angle_slider= LatexSlider(title= "\\alpha=",value_unit='^{\\circ}',value= 0,start = -180, end = 180, step = 1)
Plane_Angle_slider.on_change('value',changePlaneAngle)
Plane_Angle_slider.disabled = True

###Create Reset Button:
reset_button = Button(label="Reset", button_type="success")
reset_button.on_click(reset)
###Create Draw Button:
draw_button = Button(label="Draw", button_type="success")
draw_button.on_click(draw_main)
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
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
