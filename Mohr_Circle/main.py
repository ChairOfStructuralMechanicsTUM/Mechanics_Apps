# -*- coding: utf-8 -*-
"""
Created on Mon Nov 06 11:01:35 2017

@author: Rishith Ellath Meethal
"""

"""
Python Bokeh program which explains the concept of Mohr cirlce interactively

"""
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource,Slider,Div,Arrow,OpenHead,NormalHead,LabelSet
from bokeh.models.markers import Square,Circle
from bokeh.io import curdoc
from os.path import dirname, join
from math import pi,sqrt,pow,sin,cos

radius = 10
centreX = 10
Nx =10
Ny =10
Nxy =10
P_Angle = 45*(pi/180)
Neta =0 
Nzeta =0 
Nzetaeta =0  
#Data sources for 1st figure, ie The planes and the forces
NxP_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NyP_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NxN_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
NyN_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nxy1_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nxy2_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nxy3_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Nxy4_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
Rotating_Plane_source = ColumnDataSource(data=dict(x=[], y=[],angle = [],size =[]))

OriginalPlane_line_source = ColumnDataSource(data=dict(x=[],y=[]))
Newplane_line_source = ColumnDataSource(data=dict(x=[],y=[]))

#labels
Figure1Perm_Label_source = ColumnDataSource(data=dict(x=[18,-3],
                                    y=[12, 24],names=['x', 'y']))

Figure2Perm_Label_source = ColumnDataSource(data=dict(x=[23,-3],
                                    y=[-3, 23],names=['x', 'y']))
Figure2Moving_Label_source = ColumnDataSource(data=dict(x=[],
                                    y=[],names=[]))

#Data structures for the second figure ie the Mohr ciircel and lines 
Mohr_Circle_source = ColumnDataSource(data=dict(x=[], y=[], radius=[]))

def init():
    
    P_Angle = 45*(pi/180)
    #Calculations
    radius = float(sqrt(pow(((Nx-Ny)/2),2)+pow(Nxy,2)))
    centreX = float((Nx+Ny)/2)
    Nzeta = float(((Nx+Ny)/2)+(((Nx-Ny)/2)*cos(2*P_Angle))+Nxy*sin(2*P_Angle))
    Neta  = float(((Nx+Ny)/2)-(((Nx-Ny)/2)*cos(2*P_Angle))-Nxy*sin(2*P_Angle))
    Nzetaeta =float((-(((Nx-Ny)/2)*sin(2*P_Angle)))+Nxy*cos(2*P_Angle))
    #Figure 1
    NxP_arrow_source.data  = dict(xS=[5], xE=[15], yS=[15], yE=[15], lW = [5])
    NxN_arrow_source.data  = dict(xS=[-5], xE=[-15], yS=[15], yE=[15], lW = [5])
    NyP_arrow_source.data  = dict(xS=[0], xE=[0], yS=[20], yE=[30], lW = [5])
    NyN_arrow_source.data  = dict(xS=[0], xE=[0], yS=[10], yE=[0], lW = [5])
    Nxy1_arrow_source.data = dict(xS=[5], xE=[5], yS=[10], yE=[20], lW = [5])
    Nxy2_arrow_source.data = dict(xS=[-5], xE=[5], yS=[20], yE=[20], lW = [5])
    Nxy3_arrow_source.data = dict(xS=[-5], xE=[-5], yS=[20], yE=[10], lW = [5])
    Nxy4_arrow_source.data = dict(xS=[5], xE=[-5], yS=[10], yE=[10], lW = [5])
    Rotating_Plane_source.data = dict(x=[0], y=[-15],angle =[45*(pi/180)],size = [80])
    
    #Figure 2 
    Mohr_Circle_source.data = dict(x=[centreX], y=[0], radius=[radius])
    OriginalPlane_line_source.data = dict(x=[Ny,Ny,Nx,Nx], y=[0,-Nxy,Nxy,0])
    Newplane_line_source.data = dict(x=[Neta,Neta,Nzeta,Nzeta], y=[0,-Nzetaeta,Nzetaeta,0])
    
    Figure2Moving_Label_source.data = dict(x=[Nx,Ny,Nzeta,Neta],y=[-2,-2,-2,-2],
                                           names=[u"\u03C3"u"x", u"\u03C3"u"y",u"\u03C3"u"\u03B6",u"\u03C3"u"\u03B7"])
    
def NormalForceX(attr,old,new):
    global Nx
    if(new<0):
        NxP_arrow_source.data  = dict(xS=[5-new], xE=[5], yS=[15], yE=[15], lW = [5])
        NxN_arrow_source.data  = dict(xS=[-5+new], xE=[-5], yS=[15], yE=[15], lW = [5])    
    else:
        NxP_arrow_source.data  = dict(xS=[5], xE=[5+new], yS=[15], yE=[15], lW = [5])
        NxN_arrow_source.data  = dict(xS=[-5], xE=[-5-new], yS=[15], yE=[15], lW = [5])
    Nx = new 
    ChangeMohrCircle()
    
def NormalForceY(attr,old,new):
    global Ny
    if(new<0):
        NyP_arrow_source.data  = dict(xS=[0], xE=[0], yS=[20-new], yE=[20], lW = [5])
        NyN_arrow_source.data  = dict(xS=[0], xE=[0], yS=[10+new], yE=[10], lW = [5])
    else:
        NyP_arrow_source.data  = dict(xS=[0], xE=[0], yS=[20], yE=[20+new], lW = [5])
        NyN_arrow_source.data  = dict(xS=[0], xE=[0], yS=[10], yE=[10-new], lW = [5])
    Ny = new
    ChangeMohrCircle()
    
def TangentialXY(attr,old,new):
    global Nxy
    if(new<0):
         Nxy1_arrow_source.data = dict(xS=[5], xE=[5], yS=[15-(new/2)], yE=[15+(new/2)], lW = [5])
         Nxy2_arrow_source.data = dict(xS=[-5], xE=[-5], yS=[15+(new/2)], yE=[15-(new/2)], lW = [5])
         Nxy3_arrow_source.data = dict(xS=[-new/2], xE=[new/2], yS=[20], yE=[20], lW = [5])
         Nxy4_arrow_source.data = dict(xS=[(new/2)], xE=[(-new/2)], yS=[10], yE=[10], lW = [5])
    else:     
         Nxy1_arrow_source.data = dict(xS=[5], xE=[5], yS=[15-(new/2)], yE=[15+(new/2)], lW = [5])
         Nxy2_arrow_source.data = dict(xS=[-5], xE=[-5], yS=[15+(new/2)], yE=[15-(new/2)], lW = [5])
         Nxy3_arrow_source.data = dict(xS=[-new/2], xE=[new/2], yS=[20], yE=[20], lW = [5])
         Nxy4_arrow_source.data = dict(xS=[(new/2)], xE=[-(new/2)], yS=[10], yE=[10], lW = [5])   
    Nxy = new
    ChangeMohrCircle()
    
    
def changePlaneAngle(attr,old,new):
     global P_Angle
     P_Angle = new*(pi/180)
     Rotating_Plane_source.data = dict(x=[0], y=[-15],angle =[P_Angle],size = [80])
     ChangeMohrCircle()
    #figure2.circle([0], [0], size=25000, alpha=0.5)
        
def ChangeMohrCircle():
    global P_Angle
    radius = float(sqrt(pow(((Nx-Ny)/2),2)+pow(Nxy,2)))
    centreX = float((Nx+Ny)/2)
    Mohr_Circle_source.data = dict(x=[centreX], y=[0], radius=[radius])   
    OriginalPlane_line_source.data = dict(x=[Ny,Ny,Nx,Nx], y=[0,-Nxy,Nxy,0])
    #for second plane
    Nzeta = float(((Nx+Ny)/2)+(((Nx-Ny)/2)*cos(2*P_Angle))+Nxy*sin(2*P_Angle))
    Neta  = float(((Nx+Ny)/2)-(((Nx-Ny)/2)*cos(2*P_Angle))-Nxy*sin(2*P_Angle))
    Nzetaeta = float((-(((Nx-Ny)/2)*sin(2*P_Angle)))+Nxy*cos(2*P_Angle))
    Newplane_line_source.data = dict(x=[Neta,Neta,Nzeta,Nzeta], y=[0,-Nzetaeta,Nzetaeta,0])
    
    Figure2Moving_Label_source.data = dict(x=[Nx,Ny,Nzeta,Neta],y=[-2,-2,-2,-2],
                                           names =[u"\u03C3"u"\u2093", u"\u03C3"u"y",u"\u03C3"u"\u03B6",u"\u03C3"u"\u03B7"])
    
#plotting Vectors as arrows on the squares
NxP_arrow_glyph = Arrow(end=OpenHead(line_color="#A2AD00",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NxP_arrow_source,line_color="#A2AD00")

NxN_arrow_glyph = Arrow(end=OpenHead(line_color="#A2AD00",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NxN_arrow_source,line_color="#A2AD00")

NyP_arrow_glyph = Arrow(end=OpenHead(line_color="#A2AD00",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NyP_arrow_source,line_color="#A2AD00")

NyN_arrow_glyph = Arrow(end=OpenHead(line_color="#A2AD00",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=NyN_arrow_source,line_color="#A2AD00")

Nxy1_arrow_glyph = Arrow(end=OpenHead(line_color="#d53e4f",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nxy1_arrow_source,line_color="#d53e4f")

Nxy2_arrow_glyph = Arrow(end=OpenHead(line_color="#d53e4f",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nxy2_arrow_source,line_color="#d53e4f")

Nxy3_arrow_glyph = Arrow(end=OpenHead(line_color="#d53e4f",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nxy3_arrow_source,line_color="#d53e4f")

Nxy4_arrow_glyph = Arrow(end=OpenHead(line_color="#d53e4f",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=Nxy4_arrow_source,line_color="#d53e4f")
Rotating_Plane_glyph = Square(x='x',y='y',angle='angle',size='size')
Mohr_Circle_glyph = Circle(x='x',y='y',radius='radius')

figure1 = figure(title="", tools="", x_range=(-30,30), y_range=(-30,30),width=500,height=500)

#figure1.square([0], [-15], size=75, color="red", alpha=0.5,angle = pi/4)
figure1.square([0], [15], size=75, color="yellow", alpha=0.5)

figure1.add_layout(Arrow(end=NormalHead(fill_color="orange"),
                   x_start=0, y_start=15, x_end=25, y_end=15))
figure1.add_layout(Arrow(end=NormalHead(fill_color="orange"),
                   x_start=0, y_start=15, x_end=0, y_end=30))
figure1.add_layout(NxP_arrow_glyph)
figure1.add_layout(NxN_arrow_glyph)
figure1.add_layout(NyP_arrow_glyph)
figure1.add_layout(NyN_arrow_glyph)
figure1.add_layout(Nxy1_arrow_glyph)
figure1.add_layout(Nxy2_arrow_glyph)
figure1.add_layout(Nxy3_arrow_glyph)
figure1.add_layout(Nxy4_arrow_glyph)
figure1.add_glyph(Rotating_Plane_source,Rotating_Plane_glyph)



figure1_labels = LabelSet(x='x', y='y', text='names', level='glyph',
              x_offset=5, y_offset=5, source=Figure1Perm_Label_source, render_mode='canvas')
figure1.add_layout(figure1_labels)


figure2 = figure(title="", tools="", x_range=(-30,30), y_range=(-30,30),width=500,height=500)

figure2.add_layout(Arrow(end=NormalHead(fill_color="orange"),
                   x_start=0, y_start=0, x_end=30, y_end=0))
figure2.add_layout(Arrow(end=NormalHead(fill_color="orange"),
                   x_start=0, y_start=0, x_end=0, y_end=30))
figure2.add_glyph(Mohr_Circle_source,Mohr_Circle_glyph)


figure2.line(x='x',y='y',source= OriginalPlane_line_source, color="red")
figure2.line(x='x',y='y',source= Newplane_line_source, color="blue")


figure2_labels1 = LabelSet(x='x', y='y', text='names', level='glyph',
              x_offset=5, y_offset=5, source=Figure2Perm_Label_source, render_mode='canvas')
figure2_labels2 = LabelSet(x='x', y='y', text='names', level='glyph', x_offset=5, y_offset=5, source=Figure2Moving_Label_source, render_mode='canvas')
figure2.add_layout(figure2_labels1)
figure2.add_layout(figure2_labels2)


#initialising all column data for th initial plot
init()

#creating  sliders to change Normal and Tangential Forces
Normal_X_slider= Slider(title="Change Normal in X direction",value= 10,start = -10, end = 10, step = 1)
Normal_X_slider.on_change('value',NormalForceX)

Normal_Y_slider= Slider(title="Change Normal in Y direction",value= 10,start = -10, end = 10, step = 1)
Normal_Y_slider.on_change('value',NormalForceY)

Tangential_XY_slider= Slider(title="Change Shear Force",value= 10,start = -10, end = 10, step = 1)
Tangential_XY_slider.on_change('value',TangentialXY)

Plane_Angle_slider= Slider(title="Change Angle of Cross seection",value= 45,start = 0, end = 90, step = 5)
Plane_Angle_slider.on_change('value',changePlaneAngle)


#adding description from HTML file
description_filename = join(dirname(__file__), "description.html")
description = Div(text=open(description_filename).read(), render_as_text=False, width=1200)

curdoc().add_root(column(description,row(figure1,figure2),row(Normal_X_slider,Normal_Y_slider),row(Tangential_XY_slider,Plane_Angle_slider)))
curdoc().title = "Mohr Circle"

