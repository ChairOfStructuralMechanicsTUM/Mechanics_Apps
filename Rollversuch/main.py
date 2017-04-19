from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, Button
from bokeh.io import curdoc
from math import sin, cos, pi, sqrt

r=2.0
ri=1.5
m=1.0
g=9.81
alpha=0.35
# variables created to avoid repeated calculations
# (speeds up calculations)
SIN=sin(alpha)
COS=cos(alpha)
rampLength=25
offset=-rampLength*COS
t=0.0
H = rampLength*SIN
SphereXLines=[[],[]]
SphereYLines=[]

sphere_data = ColumnDataSource(data = dict(x=[],y=[],w=[]))
sphere_lines_data = ColumnDataSource(data = dict(x=[],y=[]))
cylinder_data = ColumnDataSource(data = dict(x=[],y=[],w=[]))
cylinder_lines_data = ColumnDataSource(data = dict(x=[],y=[]))
hollowCylinder_outer_data = ColumnDataSource(data = dict(x=[],y=[],w=[]))
hollowCylinder_inner_data = ColumnDataSource(data = dict(x=[],y=[],w=[]))
hollowCylinder_lines_data = ColumnDataSource(data = dict(x=[],y=[]))
ramp_source = ColumnDataSource(data = dict(x=[offset,0],y=[H,0]))

def init():
    global SphereXLines, SphereYLines
    for i in range (0,17):
        SphereYLines.append((i/8.0-1.0)*r)
        SphereXLines[0].append(cos(pi/4.0)*sqrt(r*r-SphereYLines[i]*SphereYLines[i]))
        SphereXLines[1].append(-SphereXLines[0][i])
    createSphere()
    createCylinder()
    createHollowCylinder()
    

def createSphere():
    global sphere_data, sphere_lines_data, offset, r, SphereXLines, SphereYLines
    newX=offset+r*SIN
    newY=H+r*COS
    sphere_data.data=dict(x=[newX],y=[newY],w=[2*r])
    X1=[]
    X2=[]
    Y1=[]
    Y2=[]
    for i in range (0,len(SphereYLines)):
        X1.append(SphereXLines[0][i]*COS+SphereYLines[i]*SIN+newX)
        X2.append(SphereXLines[1][i]*COS+SphereYLines[i]*SIN+newX)
        Y1.append(-SphereXLines[0][i]*SIN+SphereYLines[i]*COS+newY)
        Y2.append(-SphereXLines[1][i]*SIN+SphereYLines[i]*COS+newY)
    sphere_lines_data.data=dict(x=[X1, X2],y=[Y1,Y2])

def moveSphere(t):
    global r, m, g, alpha, offset, sphere_data, SphereXLines, SphereYLines, sphere_lines_data
    displacement = g*SIN*t*t*1.25
    rotation = -displacement/r
    newXBase=displacement*COS+offset
    newX=newXBase+r*SIN
    newYBase=H-displacement*SIN
    newY=newYBase+r*COS
    sphere_data.data=dict(x=[newX],y=[newY],w=[2*r])
    X1=[]
    X2=[]
    Y1=[]
    Y2=[]
    cosAngle=cos(alpha-rotation)
    sinAngle=sin(alpha-rotation)
    for i in range (0,len(SphereYLines)):
        X1.append(SphereXLines[0][i]*cosAngle+SphereYLines[i]*sinAngle+newX)
        X2.append(SphereXLines[1][i]*cosAngle+SphereYLines[i]*sinAngle+newX)
        Y1.append(-SphereXLines[0][i]*sinAngle+SphereYLines[i]*cosAngle+newY)
        Y2.append(-SphereXLines[1][i]*sinAngle+SphereYLines[i]*cosAngle+newY)
    sphere_lines_data.data=dict(x=[X1, X2],y=[Y1,Y2])

def createCylinder():
    global cylinder_data, cylinder_lines_data,r,offset
    cylinder_data.data=dict(x=[offset+r*SIN],y=[H+r*COS],w=[2*r])
    cylinder_lines_data.data=dict(x=[[offset,offset+2*r*SIN],
        [offset+r*(SIN-COS),offset+r*(SIN+COS)]],
        y=[[H,H+2*r*COS],[H+r*(COS+SIN),H+r*(COS-SIN)]])

def moveCylinder(t):
    global r, m, g, alpha, offset, cylinder_data, cylinder_lines_data
    displacement = g*SIN*t*t
    rotation = -displacement/r
    newXBase=displacement*COS+offset
    newX=newXBase+r*SIN
    newYBase=H-displacement*SIN
    newY=newYBase+r*COS
    cosRAngle=r*cos(alpha-rotation)
    sinRAngle=r*sin(alpha-rotation)
    cylinder_data.data=dict(x=[newX],y=[newY],w=[2*r])
    cylinder_lines_data.data=dict(x=[[newX+cosRAngle,newX-cosRAngle],
        [newX+sinRAngle,newX-sinRAngle]],
        y=[[newY-sinRAngle,newY+sinRAngle],
        [newY+cosRAngle,newY-cosRAngle]])

def createHollowCylinder():
    global hollowCylinder_outer_data, sphere_lines_data
    hollowCylinder_outer_data.data=dict(x=[offset+r*SIN],y=[H+r*COS],w=[2*r])
    hollowCylinder_inner_data.data=dict(x=[offset+r*SIN],y=[H+r*COS],w=[2*ri])
    hollowCylinder_lines_data.data=dict(x=[[offset,offset+(r-ri)*SIN],
        [offset+(r+ri)*SIN,offset+2*r*SIN],
        [offset+r*(SIN-COS),offset+r*SIN-ri*COS],
        [offset+r*(SIN+COS),offset+r*SIN+ri*COS]],
        y=[[H,H+(r-ri)*COS],[H+(r+ri)*COS,H+2*r*COS],
        [H+r*(COS+SIN),H+r*COS+ri*SIN],
        [H+r*(COS-SIN),H+r*COS-ri*SIN]])

def moveHollowCylinder(t):
    global r, ri, m, g, alpha, offset, hollowCylinder_inner_data, hollowCylinder_outer_data, hollowCylinder_lines_data
    temp=r*g*SIN*t*t/(r*r+ri*ri)
    rotation = -temp
    displacement = r*temp
    # constants used multiple times calculated in advance to reduce computation time
    cosAR=cos(alpha-rotation)
    sinAR=sin(alpha-rotation)
    cosRAngle=r*cosAR
    cosRIAngle=ri*cosAR
    sinRAngle=r*sinAR
    sinRIAngle=ri*sinAR
    newX=displacement*COS+offset+r*SIN
    newY=H-displacement*SIN+r*COS
    hollowCylinder_outer_data.data=dict(x=[newX],y=[newY],w=[2*r])
    hollowCylinder_inner_data.data=dict(x=[newX],y=[newY],w=[2*ri])
    hollowCylinder_lines_data.data=dict(x=[[newX+cosRAngle,newX+cosRIAngle],
        [newX-cosRAngle,newX-cosRIAngle],
        [newX+sinRAngle,newX+sinRIAngle],
        [newX-sinRAngle,newX-sinRIAngle]],
        y=[[newY-sinRAngle,newY-sinRIAngle],
        [newY+sinRAngle,newY+sinRIAngle],
        [newY+cosRAngle,newY+cosRIAngle],
        [newY-cosRAngle,newY-cosRIAngle]])

def evolveFunc (t):
    moveHollowCylinder(t)
    moveCylinder(t)
    moveSphere(t)

figSph = figure(title="Kugel (Sphere)",x_range=(offset-r,0),y_range=(0,H+2*r),height=200)
figSph.ellipse(x='x',y='y',width='w',height='w',fill_color="#0065BD",
    line_color="#003359",line_width=3,source=sphere_data)
figSph.multi_line(xs='x',ys='y',line_color="#003359",line_width=3,source=sphere_lines_data)
figSph.line(x='x',y='y',color="black",line_width=2,source=ramp_source)

figCyl = figure(title="Vollzylinder (Full cylinder)",x_range=(offset-r,0),y_range=(0,H+2*r),height=200)
figCyl.ellipse(x='x',y='y',width='w',height='w',fill_color="#0065BD",
    line_color="#003359",line_width=3,source=cylinder_data)
figCyl.multi_line(xs='x',ys='y',line_color="#003359",line_width=3,source=cylinder_lines_data)
figCyl.line(x='x',y='y',color="black",line_width=2,source=ramp_source)

figHCyl = figure(title="Hohlzylinder (Hollow cylinder)",x_range=(offset-r,0),y_range=(0,H+2*r),height=200)
figHCyl.ellipse(x='x',y='y',width='w',height='w',fill_color="#0065BD",
    line_color="#003359",line_width=3,source=hollowCylinder_outer_data)
figHCyl.ellipse(x='x',y='y',width='w',height='w',fill_color="#FFFFFF",
    line_color="#003359",line_width=3,source=hollowCylinder_inner_data)
figHCyl.multi_line(xs='x',ys='y',color="#003359",line_width=3,source=hollowCylinder_lines_data)
figHCyl.line(x='x',y='y',color="black",line_width=2,source=ramp_source)

"""
def changeObject(attr,old,new):
    if (old=="Kugel (Sphere)"):
        removeSphere()
    elif (old=="Hohlzylinder (Hollow cylinder)"):
        removeHollowCylinder()
    else:
        removeCylinder()
    if (new == "Kugel (Sphere)"):
        createSphere()
        evolveFunc=moveSphere
    elif (new=="Hohlzylinder (Hollow cylinder)"):
        createHollowCylinder()
        evolveFunc=moveHollowCylinder
    else:
        createCylinder()
        evolveFunc=moveCylinder

object_select = Select(title="Object:", value="Kugel (Sphere)",
    options=["Kugel (Sphere)", "Hohlzylinder (Hollow cylinder)", "Vollzylinder (Full cylinder)"])
object_select.on_change('value',changeObject)
"""

def evolve():
    global t
    t+=0.05
    evolveFunc(t)

test_button = Button(label="Test", button_type="success")
test_button.on_click(evolve)

init()
## Send to window
curdoc().add_root(row(column(figSph,figCyl,figHCyl),column(test_button)))
curdoc().title = "Rollversuch"
curdoc().add_periodic_callback(evolve,200)
