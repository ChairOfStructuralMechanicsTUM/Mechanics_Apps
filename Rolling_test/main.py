from __future__ import division # float devision only, like in python 3
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer, widgetbox
from bokeh.models import ColumnDataSource, Select, Button, LabelSet, Slider, CustomJS
from bokeh.models.widgets import RadioGroup, Paragraph
from bokeh.io import curdoc
from math import sin, cos, pi, sqrt, radians
from os.path import dirname, split, abspath, join
import numpy as np

import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexLabelSet

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

#TODO: move this function (and some other functions) in separate files
def is_empty(obj):
    if obj:  # returns true in a boolean context if obj has elements inside 
        return False
    else:
        return True

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

# global variables
glob_callback_id  = ColumnDataSource(data = dict(callback_id = [None]))
glob_SphereXLines = ColumnDataSource(data = dict(SphereXLines = [SphereXLines]))
glob_SphereYLines = ColumnDataSource(data = dict(SphereYLines = [SphereYLines]))

glob_values = dict(offset = offset,
                   alpha  = alpha,
                   SIN    = SIN,
                   COS    = COS,
                   g      = g,
                   t      = t,
                   H      = H)

def init():
    [SphereXLines] = glob_SphereXLines.data["SphereXLines"] #      /output
    [SphereYLines] = glob_SphereYLines.data["SphereYLines"] #      /output
    # create the lines on a reference sphere
    X=[[],[]]
    Y=[]
    for i in range (0,10):
        # use Chebychev nodes to reduce the number of points required
        Y.append((1-cos(pi*i/9))-1)
        X[0].append(cos(pi/4.0)*sqrt(1-Y[i]*Y[i]))
        X[1].append(-X[0][i])
    SphereXLines[0] = np.array(X[0])
    SphereXLines[1] = np.array(X[1])
    SphereYLines    = np.array(Y)
    glob_SphereXLines.data = dict(SphereXLines = [SphereXLines])
    glob_SphereYLines.data = dict(SphereYLines = [SphereYLines])
    # create the objects
    createSphere(2.0,fig_data[0],fig_lines_data[0])
    createCylinder(2.0,fig_data[1],fig_lines_data[1])
    createHollowCylinder(2.0,1.5,fig_data[2],fig_lines_data[2])
    
    # create the curve which indicates the angle between the ground and the ramp
    X=[]
    Y=[]
    for i in range(0,11):
        X.append(-3*cos(i*alpha/10.0))
        Y.append(3*sin(i*alpha/10.0))
    AngleMarkerSource.data=dict(x=X,y=Y)
    AlphaPos.data=dict(x=[-8],y=[-0.1],t=[u"\u03B1"])
    


def createSphere(r,sphere_data,sphere_lines_data):
    [SphereXLines] = glob_SphereXLines.data["SphereXLines"] # input/
    [SphereYLines] = glob_SphereYLines.data["SphereYLines"] # input/
    load_vals = ["SIN", "COS", "offset", "H"]
    SIN, COS, offset, H = [glob_values.get(val) for val in load_vals]
    # find the centre, knowing that it touches the ramp at (offset,H)
    newX = offset+r*SIN
    newY = H+r*COS
    # draw the sphere in blue
    sphere_data.data=dict(x=[newX],y=[newY],w=[2*r],c=["#0065BD"],a=[1])
    # use the referece lines to find the current position of the lines
    RCOS = r*COS
    RSIN = r*SIN
    X1 = SphereXLines[0]*RCOS+SphereYLines*RSIN+newX
    X2 = SphereXLines[1]*RCOS+SphereYLines*RSIN+newX
    Y1 = -SphereXLines[0]*RSIN+SphereYLines*RCOS+newY
    Y2 = -SphereXLines[1]*RSIN+SphereYLines*RCOS+newY
    # draw the lines
    sphere_lines_data.data=dict(x=[X1, X2],y=[Y1,Y2])

def moveSphere(t,r,m,sphere_data,sphere_lines_data):
    [SphereXLines] = glob_SphereXLines.data["SphereXLines"] # input/
    [SphereYLines] = glob_SphereYLines.data["SphereYLines"] # input/
    load_vals = ["g", "alpha", "SIN", "COS", "offset", "H"]
    g, alpha, SIN, COS, offset, H = [glob_values.get(val) for val in load_vals]
    # find the displacement of the point touching the ramp
    displacement = g*SIN*t*t*1.25
    # find the rotation of the sphere
    rotation = -displacement/r
    # find the new centre of the sphere
    newX = displacement*COS+offset+r*SIN
    newY = H-displacement*SIN+r*COS
    # update the drawing
    sphere_data.data=dict(x=[newX],y=[newY],w=[2*r],c=["#0065BD"],a=[1])
    # find the new positions of the guidelines from the reference sphere
    cosAngle = r*cos(alpha-rotation)
    sinAngle = r*sin(alpha-rotation)
    X1 = SphereXLines[0]*cosAngle+SphereYLines*sinAngle+newX
    X2 = SphereXLines[1]*cosAngle+SphereYLines*sinAngle+newX
    Y1 = -SphereXLines[0]*sinAngle+SphereYLines*cosAngle+newY
    Y2 = -SphereXLines[1]*sinAngle+SphereYLines*cosAngle+newY
    
    sphere_lines_data.data=dict(x=[X1, X2],y=[Y1,Y2])
    return (newX,newY)

def createHollowSphere(r,ri,sphere_data,sphere_lines_data):
    [SphereXLines] = glob_SphereXLines.data["SphereXLines"] # input/
    [SphereYLines] = glob_SphereYLines.data["SphereYLines"] # input/
    load_vals = ["SIN", "COS", "offset", "H"]
    SIN, COS, offset, H = [glob_values.get(val) for val in load_vals]
    
    if (abs(r-ri)<1e-5):
        # empty data if radius == inner radius (numerically)
        sphere_data.data       = dict(x=[],y=[],w=[],c=[],a=[])
        sphere_lines_data.data = dict(x=[],y=[])
    else:    
        # find the centre, knowing that it touches the ramp at (offset,H)
        newX = offset+r*SIN
        newY = H+r*COS
        # draw the sphere in semi-transparent blue
        sphere_data.data=dict(x=[newX],y=[newY],w=[2*r],c=["#0065BD"],a=[1-ri/r]) # a=[0.4]
        # use the referece lines to find the current position of the lines
        RCOS = r*COS
        RSIN = r*SIN
        X1 = SphereXLines[0]*RCOS+SphereYLines*RSIN+newX
        X2 = SphereXLines[1]*RCOS+SphereYLines*RSIN+newX
        Y1 = -SphereXLines[0]*RSIN+SphereYLines*RCOS+newY
        Y2 = -SphereXLines[1]*RSIN+SphereYLines*RCOS+newY
        # draw the lines
        sphere_lines_data.data=dict(x=[X1, X2],y=[Y1,Y2])

def moveHollowSphere(t,r,m,ri,sphere_data,sphere_lines_data):
    [SphereXLines] = glob_SphereXLines.data["SphereXLines"] # input/
    [SphereYLines] = glob_SphereYLines.data["SphereYLines"] # input/
    load_vals = ["g", "alpha", "SIN", "COS", "offset", "H"]
    g, alpha, SIN, COS, offset, H = [glob_values.get(val) for val in load_vals]
    if (abs(r-ri) < 1e-5): # ri close to r
        temp = -1000 # out of sight, object doesn't exist
    else:
        temp = r*g*SIN*t*t*1.25*(r**3-ri**3)/(r**5-ri**5)
    # find the rotation of the sphere
    rotation = -temp
    # find the displacement of the point touching the ramp
    displacement = temp*r
    # find the new centre of the sphere
    newX = displacement*COS+offset+r*SIN
    newY = H-displacement*SIN+r*COS
    # update the drawing
    sphere_data.data=dict(x=[newX],y=[newY],w=[2*r],c=["#0065BD"],a=[1-ri/r])
    # find the new positions of the guidelines from the reference sphere
    cosAngle = r*cos(alpha-rotation)
    sinAngle = r*sin(alpha-rotation)
    X1 = SphereXLines[0]*cosAngle+SphereYLines*sinAngle+newX
    X2 = SphereXLines[1]*cosAngle+SphereYLines*sinAngle+newX
    Y1 = -SphereXLines[0]*sinAngle+SphereYLines*cosAngle+newY
    Y2 = -SphereXLines[1]*sinAngle+SphereYLines*cosAngle+newY
    sphere_lines_data.data=dict(x=[X1, X2],y=[Y1,Y2])
    return (newX,newY)

def createCylinder(r, cylinder_data, cylinder_lines_data):
    load_vals = ["SIN", "COS", "offset", "H"]
    SIN, COS, offset, H = [glob_values.get(val) for val in load_vals]
    # draw the cylinder around the centre, knowing that it touches the ramp at (offset,H)
    cylinder_data.data=dict(x=[offset+r*SIN],y=[H+r*COS],w=[2*r],c=["#0065BD"],a=[1])
    cylinder_lines_data.data=dict(x=[[offset,offset+2*r*SIN],
        [offset+r*(SIN-COS),offset+r*(SIN+COS)]],
        y=[[H,H+2*r*COS],[H+r*(COS+SIN),H+r*(COS-SIN)]])

def moveCylinder(t,r,m, cylinder_data, cylinder_lines_data):
    load_vals = ["g", "alpha", "SIN", "COS", "offset", "H"]
    g, alpha, SIN, COS, offset, H = [glob_values.get(val) for val in load_vals]
    # find the displacement of the point touching the ramp
    displacement = g*SIN*t*t
    # find the rotation of the cylinder
    rotation = -displacement/r
    # find the new centre of the cylinder
    newX      = displacement*COS+offset+r*SIN
    newY      = H-displacement*SIN+r*COS
    cosRAngle = r*cos(alpha-rotation)
    sinRAngle = r*sin(alpha-rotation)
    # update the drawing
    cylinder_data.data=dict(x=[newX],y=[newY],w=[2*r],c=["#0065BD"],a=[1])
    cylinder_lines_data.data=dict(x=[[newX+cosRAngle,newX-cosRAngle],
        [newX+sinRAngle,newX-sinRAngle]],
        y=[[newY-sinRAngle,newY+sinRAngle],
        [newY+cosRAngle,newY-cosRAngle]])
    return (newX,newY)

def createHollowCylinder(r,ri, hollowCylinder_data, hollowCylinder_lines_data):
    load_vals = ["SIN", "COS", "offset", "H"]
    SIN, COS, offset, H = [glob_values.get(val) for val in load_vals]
    
    if (abs(r-ri)<1e-5):
        # empty data if radius == inner radius (numerically)
        hollowCylinder_data.data       = dict(x=[],y=[],w=[],c=[],a=[])
        hollowCylinder_lines_data.data = dict(x=[],y=[])
    else:
        # draw the cylinder around the centre, knowing that it touches the ramp at (offset,H)
        hollowCylinder_data.data=dict(x=[offset+r*SIN,offset+r*SIN],
            y=[H+r*COS,H+r*COS],w=[2*r,2*ri],c=["#0065BD","#FFFFFF"],a=[1,1])
        hollowCylinder_lines_data.data=dict(x=[[offset,offset+(r-ri)*SIN],
            [offset+(r+ri)*SIN,offset+2*r*SIN],
            [offset+r*(SIN-COS),offset+r*SIN-ri*COS],
            [offset+r*(SIN+COS),offset+r*SIN+ri*COS]],
            y=[[H,H+(r-ri)*COS],[H+(r+ri)*COS,H+2*r*COS],
            [H+r*(COS+SIN),H+r*COS+ri*SIN],
            [H+r*(COS-SIN),H+r*COS-ri*SIN]])

def moveHollowCylinder(t,r,m,ri,hollowCylinder_data,hollowCylinder_lines_data):
    load_vals = ["g", "alpha", "SIN", "COS", "offset", "H"]
    g, alpha, SIN, COS, offset, H = [glob_values.get(val) for val in load_vals]
    if (abs(r-ri) < 1e-5): # ri close to r
        temp = -1000 # out of sight, object doesn't exist
    else:
        temp = r*g*SIN*t*t/(r*r+ri*ri)
    # find the rotation of the cylinder
    rotation = -temp
    # find the displacement of the point touching the ramp
    displacement = r*temp
    # constants used multiple times calculated in advance to reduce computation time
    cosAR      = cos(alpha-rotation)
    sinAR      = sin(alpha-rotation)
    cosRAngle  = r*cosAR
    cosRIAngle = ri*cosAR
    sinRAngle  = r*sinAR
    sinRIAngle = ri*sinAR
    # find the new centre of the cylinder
    newX = displacement*COS+offset+r*SIN
    newY = H-displacement*SIN+r*COS
    # update the drawing
    hollowCylinder_data.data=dict(x=[newX,newX],
        y=[newY,newY],w=[2*r,2*ri],c=["#0065BD","#FFFFFF"],a=[1,1])
    hollowCylinder_lines_data.data=dict(x=[[newX+cosRAngle,newX+cosRIAngle],
        [newX-cosRAngle,newX-cosRIAngle],
        [newX+sinRAngle,newX+sinRIAngle],
        [newX-sinRAngle,newX-sinRIAngle]],
        y=[[newY-sinRAngle,newY-sinRIAngle],
        [newY+sinRAngle,newY+sinRIAngle],
        [newY+cosRAngle,newY+cosRIAngle],
        [newY-cosRAngle,newY-cosRIAngle]])
    return (newX,newY)

## draw 3 graphs each containing a ramp, the angle marker, an ellipse, and lines

XStart = -rampLength-maxR-3#-5
#YEnd   = H+2*maxR # start height, but we need height for max alpha
YEnd   = rampLength*sin(radians(alpha_max))+2*maxR
Width  = -255.4*XStart/YEnd #-220.0*XStart/YEnd
fig0 = figure(title="Sphere",x_range=(XStart,0),y_range=(0,YEnd),height=220,width=int(Width), tools="")
fig0.ellipse(x='x',y='y',width='w',height='w',fill_color='c',fill_alpha='a',
    line_color="#003359",line_width=3,source=fig_data[0])
fig0.multi_line(xs='x',ys='y',line_color="#003359",line_width=3,source=fig_lines_data[0])
fig0.line(x='x',y='y',color="black",line_width=2,source=ramp_source)
fig0.line(x='x',y='y',color="black",line_width=2,source=wall_source)
fig0.line(x='x',y='y',color="black",line_width=2,source=AngleMarkerSource)
#angle_glyph1=LabelSet(x='x', y='y',text='t',text_color='black',
#    text_font_size="15pt", source=AlphaPos)
#fig0.add_layout(angle_glyph1)
fig0.grid.visible = False
fig0.axis.visible = False
fig0.toolbar_location = None
time_lable0 = LabelSet(x='x', y='y', text='t', source=time_display[0])
# this if does not work, since it will be executed before the variable will be altered!
# -> use array of time_display ColumnDataSources
#if glob_values["hit_end"][0]:
#    fig1.add_layout(time_lable1)
fig0.add_layout(time_lable0)


fig1 = figure(title="Full cylinder",x_range=(XStart,0),y_range=(0,YEnd),height=220,width=int(Width), tools="")
fig1.ellipse(x='x',y='y',width='w',height='w',fill_color='c',fill_alpha='a',
    line_color="#003359",line_width=3,source=fig_data[1])
fig1.multi_line(xs='x',ys='y',line_color="#003359",line_width=3,source=fig_lines_data[1])
fig1.line(x='x',y='y',color="black",line_width=2,source=ramp_source)
fig1.line(x='x',y='y',color="black",line_width=2,source=wall_source)
fig1.line(x='x',y='y',color="black",line_width=2,source=AngleMarkerSource)
#angle_glyph2=LabelSet(x='x', y='y',text='t',text_color='black',
#    text_font_size="15pt", source=AlphaPos)
#fig2.add_layout(angle_glyph2)
#fig2.grid.visible = False
fig1.axis.visible = False
fig1.toolbar_location = None
time_lable1 = LabelSet(x='x', y='y', text='t', source=time_display[1])
fig1.add_layout(time_lable1)

fig2 = figure(title="Hollow cylinder",x_range=(XStart,0),y_range=(0,YEnd),height=220,width=int(Width), tools="")
fig2.ellipse(x='x',y='y',width='w',height='w',fill_color='c',fill_alpha='a',
    line_color="#003359",line_width=3,source=fig_data[2])
fig2.multi_line(xs='x',ys='y',color="#003359",line_width=3,source=fig_lines_data[2])
fig2.line(x='x',y='y',color="black",line_width=2,source=ramp_source)
fig2.line(x='x',y='y',color="black",line_width=2,source=wall_source)
fig2.line(x='x',y='y',color="black",line_width=2,source=AngleMarkerSource)
#angle_glyph3=LabelSet(x='x', y='y',text='t',text_color='black',
#    text_font_size="15pt", source=AlphaPos)
#fig3.add_layout(angle_glyph3)
#fig2.grid.visible = False
#fig2.axis.visible = False
fig2.toolbar_location = None
time_lable2 = LabelSet(x='x', y='y', text='t', source=time_display[2])
fig2.add_layout(time_lable2)


# sketch of the ramp and objects
fig3 = figure(title="Annotations", x_range=(-50,0), y_range=(0,25), height=220, width=400, tools="")
#fig4.line(x='x',y='y',color="black",line_width=2,source=ramp_source)
fig3.line(x=[0,-48],y=[0,18],color="black",line_width=2) # ramp
fig3.line(x=[-48,-48],y=[0,18],color="black",line_width=2) # wall
fig3.ellipse(x=[-45],y=[19],width=[4],height=[4],fill_color="#0065BD",line_color="#003359",line_width=3)
fig3.ellipse(x=[-45],y=[19],width=[2.5],height=[4],fill_alpha=[0],line_color="#003359",line_width=3, angle=-0.7)
fig3.ellipse(x=[0],y=[-1],width=[12], height=[10], fill_alpha=[0], line_color='black', line_width=2, line_dash='15 50', line_dash_offset=-10)
#fig4.line(x='x',y='y',color="black",line_width=2,source=AngleMarkerSource)
angle_glyph4=LabelSet(x='x', y='y',text='t',text_color='black',
    text_font_size="15pt", source=AlphaPos)
fig3.add_layout(angle_glyph4)
fig3.grid.visible = False
fig3.axis.visible = False
fig3.toolbar_location = None

fig4 = figure(x_range=(-10,10), y_range=(-5,5), height=220, width=400, tools="")
fig4.ellipse(x=[-5,-5],y=[0,0],width=[4,6],height=[4,6],fill_alpha=[0,0],line_color='black',line_width=3)
fig4.line(x=[-5,-5],y=[0,3],line_width=2)
fig4.line(x=[-5,-3],y=[0,0],line_width=2)
r_lables_source = ColumnDataSource(data=dict(x=[-4.2,-5.7,1,1],y=[-0.8,1,1,-1],t=["r_i","r","r\\:=\\text{Radius}","r_i=\\text{Inner radius}"]))
r_lables = LatexLabelSet(x='x', y='y', text='t', source=r_lables_source)
fig4.add_layout(r_lables)
fig4.grid.visible = False
fig4.axis.visible = False
fig4.toolbar_location = None

# put the figures in a list for easy access in functions
figure_list = [fig0,fig1,fig2]

# name the functions to be used by each figure depending upon their content
evolveFunc0=lambda(x):moveSphere(x,2.0,1.0,fig_data[0],fig_lines_data[0])
evolveFunc1=lambda(x):moveCylinder(x,2.0,1.0,fig_data[1],fig_lines_data[1])
evolveFunc2=lambda(x):moveHollowCylinder(x,2.0,1.0,1.5,fig_data[2],fig_lines_data[2])
glob_fun_handles = [evolveFunc0,evolveFunc1,evolveFunc2]

# function to change the shape, radius, or mass of the object in figure FIG
def changeObject(FIG,new_object,r,ri,m):
    # save the data concerned in data and line_data
    data      = fig_data[FIG]
    line_data = fig_lines_data[FIG]
    # depending on the shape specified, create the object and
    # save the new evolution function in the variable func
    if (new_object == "Sphere"):
        createSphere(r,data,line_data)
        func=lambda(x):moveSphere(x,r,m,data,line_data)
    elif (new_object =="Hollow cylinder"):
        createHollowCylinder(r,ri,data,line_data)
        func=lambda(x):moveHollowCylinder(x,r,m,ri,data,line_data)
    elif (new_object == "Hollow sphere"):
        createHollowSphere(r,ri,data,line_data)
        if (abs(r-ri)<1e-5):
            time_display[FIG].data=dict(x=[-20],y=[20],t=["Object vanished!"])
        else:
            time_display[FIG].data=dict(x=[],y=[],t=[])
        func=lambda(x):moveHollowSphere(x,r,m,ri,data,line_data)
    else:
        createCylinder(r,data,line_data)
        func=lambda(x):moveCylinder(x,r,m,data,line_data)
    
    
    #TODO: outsource this part into another function (other purpose)
    # check if the data of each plot is empty
    f1_data_is_empty = is_empty(sum(fig_data[0].data.values(),[]))
    f2_data_is_empty = is_empty(sum(fig_data[1].data.values(),[]))
    f3_data_is_empty = is_empty(sum(fig_data[2].data.values(),[]))
    
    if (f1_data_is_empty and f2_data_is_empty and f3_data_is_empty):
        # if all datas are empty (radius == inner radius) disable the start button
        # simulation cannot be run without any existing object
        start_button.disabled = True
    else:
        # if any of the data is not empty, at least one obejcts exists
        # therefore, enable start button
        start_button.disabled = False
    
    # save the evolution function to the appropriate function handle
    glob_fun_handles[FIG] = func
    figure_list[FIG].title.text=new_object

## slider functions
# functions to change the shape
def changeObject0(attr,old,new):
    changeObject(0,new,radius_slider0.value,ri_slider0.value,1.0)

def changeObject1(attr,old,new):
    changeObject(1,new,radius_slider1.value,ri_slider1.value,1.0)

def changeObject2(attr,old,new):
    changeObject(2,new,radius_slider2.value,ri_slider2.value,1.0)

# functions to change the radius
def changeRadius0(attr,old,new):
    changeObject(0,object_select0.value,new,ri_slider0.value,1.0)
    ri_slider0.end = new
    ri_slider0.value = min(ri_slider0.value,new)

def changeRadius1(attr,old,new):
    changeObject(1,object_select1.value,new,ri_slider1.value,1.0)
    ri_slider1.end = new
    ri_slider1.value = min(ri_slider0.value,new)

def changeRadius2(attr,old,new):
    changeObject(2,object_select2.value,new,ri_slider2.value,1.0)
    ri_slider2.end = new
    ri_slider2.value = min(ri_slider2.value,new)
    
#functions to change the inner radius  / wall thickness
def changeWall0(attr,old,new):
    changeObject(0,object_select0.value,radius_slider0.value,new,1.0)
def changeWall1(attr,old,new):
    changeObject(1,object_select1.value,radius_slider1.value,new,1.0)
def changeWall2(attr,old,new):
    changeObject(2,object_select2.value,radius_slider2.value,new,1.0)

# hide inner radius slider if full object is selected
# show inner radius slider if hollow object is selected    
object_select_JS = """
choice = cb_obj.value;
caller = cb_obj.name;

// extract the number of the name and convert it to integer
slider_idx = parseInt(caller.match(/\d/g).join("")); //-1; //-1 for starting at 0

slider_in_question = document.getElementsByClassName("wall_slider")[slider_idx];

// if hollow object is selected, show the slider (get rid of hidden)
if(choice.includes("Hollow")){
        slider_in_question.className=slider_in_question.className.replace(" hidden","");
}
// if full object is selected, check if slider is hidden; if not, hide it
else if(!slider_in_question.className.includes("hidden")){
        slider_in_question.className+=" hidden";
}
"""

# sliders
object_select0 = Select(title="Object:", value="Sphere", name="obj0",
    options=["Sphere", "Hollow sphere", "Full cylinder", "Hollow cylinder"])
object_select0.on_change('value',changeObject0)
object_select1 = Select(title="Object:", value="Full cylinder", name="obj1",
    options=["Sphere", "Hollow sphere", "Full cylinder", "Hollow cylinder"])
object_select1.on_change('value',changeObject1)
object_select2 = Select(title="Object:", value="Hollow cylinder", name="obj2",
    options=["Sphere", "Hollow sphere", "Full cylinder", "Hollow cylinder"])
object_select2.on_change('value',changeObject2)

object_select0.callback = CustomJS(code=object_select_JS)
object_select1.callback = CustomJS(code=object_select_JS)
object_select2.callback = CustomJS(code=object_select_JS)

radius_slider0 = Slider(title="Radius", value=2.0, start=1.0, end=maxR, step=0.5)
radius_slider0.on_change('value',changeRadius0)
radius_slider1 = Slider(title="Radius", value=2.0, start=1.0, end=maxR, step=0.5)
radius_slider1.on_change('value',changeRadius1)
radius_slider2 = Slider(title="Radius", value=2.0, start=1.0, end=maxR, step=0.5)
radius_slider2.on_change('value',changeRadius2)

# end value dependend on selected radius size
ri_slider0 = Slider(title="Inner radius", value=0.5, start=0.0, end=2.0, step=0.5, css_classes=["wall_slider", "obj1", "hidden"])
ri_slider0.on_change('value',changeWall0)
ri_slider1 = Slider(title="Inner radius", value=0.5, start=0.0, end=2.0, step=0.5, css_classes=["wall_slider", "obj2", "hidden"])
ri_slider1.on_change('value',changeWall1)
ri_slider2 = Slider(title="Inner radius", value=1.5, start=0.0, end=2.0, step=0.5, css_classes=["wall_slider", "obj3"])
ri_slider2.on_change('value',changeWall2)



mode_selection = RadioGroup(labels=["one", "all"], active=0, inline=True)
p_mode = Paragraph(text="""Stopping mode: """)


# slider function for the angle
def changeAlpha(attr,old,new):
    alpha=radians(new)
    X=[]
    Y=[]
    for i in range(0,11):
        X.append(-3*cos(i*alpha/10.0))
        Y.append(3*sin(i*alpha/10.0))
    AngleMarkerSource.data=dict(x=X,y=Y)
    COS    = cos(alpha)
    SIN    = sin(alpha)
    offset = -rampLength*COS
    H      = rampLength*SIN
    glob_values.update(dict(alpha=alpha, SIN=SIN, COS=COS, offset=offset, H=H)) #      /output
    ramp_source.data = dict(x=[offset-rampAddLength*COS,0],y=[H+rampAddLength*SIN,0])
    wall_source.data = dict(x=[offset-rampAddLength*COS,offset-rampAddLength*COS],y=[H+rampAddLength*SIN,0])
    reset()

# slider for the angle
alpha_slider = Slider(title=u"\u03B1", value=20.0, start=5.0, end=alpha_max, step=1.0)
alpha_slider.on_change('value',changeAlpha)

def disable_all_sliders(d=True):
    object_select0.disabled = d
    object_select1.disabled = d
    object_select2.disabled = d
    radius_slider0.disabled = d
    radius_slider1.disabled = d
    radius_slider2.disabled = d
    ri_slider0.disabled     = d
    ri_slider1.disabled     = d
    ri_slider2.disabled     = d
    alpha_slider.disabled   = d

def start():
    [callback_id] = glob_callback_id.data["callback_id"] # input/output
    # switch the label
    if start_button.label == "Start":
        start_button.label = "Stop"
        reset_button.disabled = True
        # add the call to evolve
        callback_id = curdoc().add_periodic_callback(evolve,50)
        glob_callback_id.data = dict(callback_id = [callback_id])
    elif start_button.label == "Stop":
        start_button.label = "Start"
        reset_button.disabled = False
        # remove the call to evolve
        curdoc().remove_periodic_callback(callback_id)
    # disable sliders during simulation
    disable_all_sliders(True)
    

def reset():
    glob_values["t"] = 0.0 #      /output
    changeObject(0,object_select0.value,radius_slider0.value,ri_slider0.value,1.0)
    changeObject(1,object_select1.value,radius_slider1.value,ri_slider1.value,1.0)
    changeObject(2,object_select2.value,radius_slider2.value,ri_slider2.value,1.0)
    disable_all_sliders(False)
    time_display[0].data=dict(x=[],y=[],t=[])
    time_display[1].data=dict(x=[],y=[],t=[])
    time_display[2].data=dict(x=[],y=[],t=[])
    fig_in_use[:] = [True,True,True] # [True]*len(fig_data)  for more general case
    
    
def get_coordinates(fun_handles, in_execution, t):
    # Input:  - list of function handles, size n
    #         - list of bool values if function is still in execution, size n
    #         - time t to evaluate the function on
    # Output: - list of x- and y-coordinates, size 2xn
    x_coords = np.zeros(len(fun_handles))
    y_coords = x_coords.copy()
    for j, handle in enumerate(fun_handles):
        if in_execution[j]:
            (x_coords[j], y_coords[j]) = handle(t)
        else:
            (x_coords[j], y_coords[j]) = (-50,50)
    return (x_coords, y_coords)
    
    

def evolve():
    t = glob_values["t"] # input/output
    t+=0.01
    glob_values["t"] = t
    
    # call all necessary functions
    # get new coordinates of objects which are still running
    (x_coords,y_coords) = get_coordinates(glob_fun_handles, fig_in_use, t)
    
    
    # if an object has reached the end of the ramp then stop the simulation
    ind_x_max = np.argmax(x_coords)
    ind_y_max = np.argmax(y_coords)
    #max_x = max(x_coords)  # avoid multiple max and min evaluations
    #min_y = min(y_coords)
    if (x_coords[ind_x_max]>0 or y_coords[ind_y_max]<0):
        # in mode "one" (active==0) the simulation is stopped after one of the objects reached the end of the ramp
        # in mode "all" (active==1) the simulation is stopped after all objects reached the end of the ramp 
        #               -> (only one fig in use at this time, one "True" <==> sum==1)
        # mode "one" is selected -> run until one simulation is finished
        # mode "all" is selected -> run all simulations till the end
        if (mode_selection.active==0 or sum(fig_in_use)==1):
            start() #equals to stop if it is running
        
        # get the index (number of the plot) to know which plot finished the simulation
        plot_num = ind_x_max if x_coords[ind_x_max]>0 else ind_y_max
        fig_in_use[plot_num] = False
        print(plot_num)
        print("------")
        # change the corresponding CDS to display the time only in this plot
        time_display[plot_num].data=dict(x=[-10],y=[20],t=[str(glob_values["t"])+" s"])
#TODO: only stop one figure and let the others finish too
#      display finish time on each plot
#      maybe add a button to switch between "let all run through" and "stop all"

# create the buttons
start_button = Button(label="Start", button_type="success")
start_button.on_click(start)
reset_button = Button(label="Reset", button_type="success")
reset_button.on_click(reset)

init()
## Send to window
curdoc().add_root(row(column(row(fig0,column(object_select0,radius_slider0,ri_slider0)),
    row(fig1,column(object_select1,radius_slider1,ri_slider1)),
    row(fig2,column(object_select2,radius_slider2,ri_slider2))),Spacer(width=100),
    column(start_button,reset_button,row(widgetbox(p_mode,width=120),mode_selection),alpha_slider, Spacer(height=30), fig3, fig4)))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
