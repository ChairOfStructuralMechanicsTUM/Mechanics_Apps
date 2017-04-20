from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, Button, LabelSet, Slider
from bokeh.io import curdoc
from math import sin, cos, pi, sqrt, radians

maxR=4.0
g=9.81
alpha=radians(20)
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

fig1_data = ColumnDataSource(data = dict(x=[],y=[],w=[],c=[],a=[]))
fig1_lines_data = ColumnDataSource(data = dict(x=[],y=[]))
fig2_data = ColumnDataSource(data = dict(x=[],y=[],w=[],c=[],a=[]))
fig2_lines_data = ColumnDataSource(data = dict(x=[],y=[]))
fig3_data = ColumnDataSource(data = dict(x=[],y=[],w=[],c=[],a=[]))
fig3_lines_data = ColumnDataSource(data = dict(x=[],y=[]))
ramp_source = ColumnDataSource(data = dict(x=[offset,0],y=[H,0]))
AngleMarkerSource = ColumnDataSource(data = dict(x=[],y=[]))
AlphaPos = ColumnDataSource(data = dict(x=[],y=[],t=[]))

Active = False

def init():
    global SphereXLines, SphereYLines
    for i in range (0,13):
        SphereYLines.append((i/6.0-1.0))
        SphereXLines[0].append(cos(pi/4.0)*sqrt(1-SphereYLines[i]*SphereYLines[i]))
        SphereXLines[1].append(-SphereXLines[0][i])
    createSphere(2.0,fig1_data,fig1_lines_data)
    createCylinder(2.0,fig2_data,fig2_lines_data)
    createHollowCylinder(2.0,1.5,fig3_data,fig3_lines_data)
    X=[]
    Y=[]
    for i in range(0,11):
        X.append(-3*cos(i*alpha/10.0))
        Y.append(3*sin(i*alpha/10.0))
    AngleMarkerSource.data=dict(x=X,y=Y)
    AlphaPos.data=dict(x=[-4.5],y=[-0.1],t=[u"\u03B1"])

def createSphere(r,sphere_data,sphere_lines_data):
    global offset, SphereXLines, SphereYLines, SIN, COS
    newX=offset+r*SIN
    newY=H+r*COS
    sphere_data.data=dict(x=[newX],y=[newY],w=[2*r],c=["#0065BD"],a=[1])
    X1=[]
    X2=[]
    Y1=[]
    Y2=[]
    RCOS=r*COS
    RSIN=r*SIN
    for i in range (0,len(SphereYLines)):
        X1.append(SphereXLines[0][i]*RCOS+SphereYLines[i]*RSIN+newX)
        X2.append(SphereXLines[1][i]*RCOS+SphereYLines[i]*RSIN+newX)
        Y1.append(-SphereXLines[0][i]*RSIN+SphereYLines[i]*RCOS+newY)
        Y2.append(-SphereXLines[1][i]*RSIN+SphereYLines[i]*RCOS+newY)
    sphere_lines_data.data=dict(x=[X1, X2],y=[Y1,Y2])

def moveSphere(t,r,m,sphere_data,sphere_lines_data):
    global g, alpha, offset, SphereXLines, SphereYLines, SIN, COS
    displacement = g*SIN*t*t*1.25
    rotation = -displacement/r
    newXBase=displacement*COS+offset
    newX=newXBase+r*SIN
    newYBase=H-displacement*SIN
    newY=newYBase+r*COS
    sphere_data.data=dict(x=[newX],y=[newY],w=[2*r],c=["#0065BD"],a=[1])
    X1=[]
    X2=[]
    Y1=[]
    Y2=[]
    cosAngle=r*cos(alpha-rotation)
    sinAngle=r*sin(alpha-rotation)
    for i in range (0,len(SphereYLines)):
        X1.append(SphereXLines[0][i]*cosAngle+SphereYLines[i]*sinAngle+newX)
        X2.append(SphereXLines[1][i]*cosAngle+SphereYLines[i]*sinAngle+newX)
        Y1.append(-SphereXLines[0][i]*sinAngle+SphereYLines[i]*cosAngle+newY)
        Y2.append(-SphereXLines[1][i]*sinAngle+SphereYLines[i]*cosAngle+newY)
    sphere_lines_data.data=dict(x=[X1, X2],y=[Y1,Y2])
    return (newX,newY)

def createHollowSphere(r,sphere_data,sphere_lines_data):
    global offset, SphereXLines, SphereYLines, SIN, COS
    newX=offset+r*SIN
    newY=H+r*COS
    sphere_data.data=dict(x=[newX],y=[newY],w=[2*r],c=["#0065BD"],a=[0.4])
    X1=[]
    X2=[]
    Y1=[]
    Y2=[]
    RCOS=r*COS
    RSIN=r*SIN
    for i in range (0,len(SphereYLines)):
        X1.append(SphereXLines[0][i]*RCOS+SphereYLines[i]*RSIN+newX)
        X2.append(SphereXLines[1][i]*RCOS+SphereYLines[i]*RSIN+newX)
        Y1.append(-SphereXLines[0][i]*RSIN+SphereYLines[i]*RCOS+newY)
        Y2.append(-SphereXLines[1][i]*RSIN+SphereYLines[i]*RCOS+newY)
    sphere_lines_data.data=dict(x=[X1, X2],y=[Y1,Y2])

def moveHollowSphere(t,r,m,ri,sphere_data,sphere_lines_data):
    global g, alpha, offset, SphereXLines, SphereYLines, SIN, COS
    temp = r*g*SIN*t*t*1.25*(r**3-ri**3)/(r**5-ri**5)
    rotation = -temp
    displacement = temp*r
    newXBase=displacement*COS+offset
    newX=newXBase+r*SIN
    newYBase=H-displacement*SIN
    newY=newYBase+r*COS
    sphere_data.data=dict(x=[newX],y=[newY],w=[2*r],c=["#0065BD"],a=[0.4])
    X1=[]
    X2=[]
    Y1=[]
    Y2=[]
    cosAngle=r*cos(alpha-rotation)
    sinAngle=r*sin(alpha-rotation)
    for i in range (0,len(SphereYLines)):
        X1.append(SphereXLines[0][i]*cosAngle+SphereYLines[i]*sinAngle+newX)
        X2.append(SphereXLines[1][i]*cosAngle+SphereYLines[i]*sinAngle+newX)
        Y1.append(-SphereXLines[0][i]*sinAngle+SphereYLines[i]*cosAngle+newY)
        Y2.append(-SphereXLines[1][i]*sinAngle+SphereYLines[i]*cosAngle+newY)
    sphere_lines_data.data=dict(x=[X1, X2],y=[Y1,Y2])
    return (newX,newY)

def createCylinder(r, cylinder_data, cylinder_lines_data):
    global offset, SIN, COS
    cylinder_data.data=dict(x=[offset+r*SIN],y=[H+r*COS],w=[2*r],c=["#0065BD"],a=[1])
    cylinder_lines_data.data=dict(x=[[offset,offset+2*r*SIN],
        [offset+r*(SIN-COS),offset+r*(SIN+COS)]],
        y=[[H,H+2*r*COS],[H+r*(COS+SIN),H+r*(COS-SIN)]])

def moveCylinder(t,r,m, cylinder_data, cylinder_lines_data):
    global g, alpha, offset, SIN, COS
    displacement = g*SIN*t*t
    rotation = -displacement/r
    newXBase=displacement*COS+offset
    newX=newXBase+r*SIN
    newYBase=H-displacement*SIN
    newY=newYBase+r*COS
    cosRAngle=r*cos(alpha-rotation)
    sinRAngle=r*sin(alpha-rotation)
    cylinder_data.data=dict(x=[newX],y=[newY],w=[2*r],c=["#0065BD"],a=[1])
    cylinder_lines_data.data=dict(x=[[newX+cosRAngle,newX-cosRAngle],
        [newX+sinRAngle,newX-sinRAngle]],
        y=[[newY-sinRAngle,newY+sinRAngle],
        [newY+cosRAngle,newY-cosRAngle]])
    return (newX,newY)

def createHollowCylinder(r,ri, hollowCylinder_data, hollowCylinder_lines_data):
    global offset, SIN, COS
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
    global g, alpha, offset, SIN, COS
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

fig1 = figure(title="Kugel (Sphere)",x_range=(offset-maxR,0),y_range=(0,H+2*maxR),height=220)
fig1.ellipse(x='x',y='y',width='w',height='w',fill_color='c',fill_alpha='a',
    line_color="#003359",line_width=3,source=fig1_data)
fig1.multi_line(xs='x',ys='y',line_color="#003359",line_width=3,source=fig1_lines_data)
fig1.line(x='x',y='y',color="black",line_width=2,source=ramp_source)
fig1.line(x='x',y='y',color="black",line_width=2,source=AngleMarkerSource)
angle_glyph1=LabelSet(x='x', y='y',text='t',text_color='black',
    text_font_size="15pt", source=AlphaPos)
fig1.add_layout(angle_glyph1)

fig2 = figure(title="Vollzylinder (Full cylinder)",x_range=(offset-maxR,0),y_range=(0,H+2*maxR),height=220)
fig2.ellipse(x='x',y='y',width='w',height='w',fill_color='c',fill_alpha='a',
    line_color="#003359",line_width=3,source=fig2_data)
fig2.multi_line(xs='x',ys='y',line_color="#003359",line_width=3,source=fig2_lines_data)
fig2.line(x='x',y='y',color="black",line_width=2,source=ramp_source)
fig2.line(x='x',y='y',color="black",line_width=2,source=AngleMarkerSource)
angle_glyph2=LabelSet(x='x', y='y',text='t',text_color='black',
    text_font_size="15pt", source=AlphaPos)
fig2.add_layout(angle_glyph2)

fig3 = figure(title="Hohlzylinder (Hollow cylinder)",x_range=(offset-maxR,0),y_range=(0,H+2*maxR),height=220)
fig3.ellipse(x='x',y='y',width='w',height='w',fill_color='c',fill_alpha='a',
    line_color="#003359",line_width=3,source=fig3_data)
fig3.multi_line(xs='x',ys='y',color="#003359",line_width=3,source=fig3_lines_data)
fig3.line(x='x',y='y',color="black",line_width=2,source=ramp_source)
fig3.line(x='x',y='y',color="black",line_width=2,source=AngleMarkerSource)
angle_glyph3=LabelSet(x='x', y='y',text='t',text_color='black',
    text_font_size="15pt", source=AlphaPos)
fig3.add_layout(angle_glyph3)

evolveFunc1=lambda(x):moveSphere(x,2.0,1.0,fig1_data,fig1_lines_data)
evolveFunc2=lambda(x):moveCylinder(x,2.0,1.0,fig2_data,fig2_lines_data)
evolveFunc3=lambda(x):moveHollowCylinder(x,2.0,1.0,1.5,fig3_data,fig3_lines_data)

def changeObject(FIG,new,r,m):
    data=None
    line_data=None
    func=None
    if (FIG==1):
        data=fig1_data
        line_data=fig1_lines_data
    elif(FIG==2):
        data=fig2_data
        line_data=fig2_lines_data
    else:
        data=fig3_data
        line_data=fig3_lines_data
    if (new == "Kugel (Sphere)"):
        createSphere(r,data,line_data)
        func=lambda(x):moveSphere(x,r,m,data,line_data)
    elif (new=="Hohlzylinder (Hollow cylinder)"):
        createHollowCylinder(r,r-0.5,data,line_data)
        func=lambda(x):moveHollowCylinder(x,r,m,r-0.5,data,line_data)
    elif (new == "Hohlkugel (Hollow sphere)"):
        createHollowSphere(r,data,line_data)
        func=lambda(x):moveHollowSphere(x,r,m,r-0.5,data,line_data)
    else:
        createCylinder(r,data,line_data)
        func=lambda(x):moveCylinder(x,r,m,data,line_data)
    if (FIG==1):
        global evolveFunc1
        evolveFunc1=func
    elif(FIG==2):
        global evolveFunc2
        evolveFunc2=func
    else:
        global evolveFunc3
        evolveFunc3=func
    global Active,t
    if (Active):
        t=0.0

def changeObject1(attr,old,new):
    changeObject(1,new,radius_select1.value,1.0)

def changeObject2(attr,old,new):
    changeObject(2,new,radius_select2.value,1.0)

def changeObject3(attr,old,new):
    changeObject(3,new,radius_select3.value,1.0)

def changeRadius1(attr,old,new):
    changeObject(1,object_select1.value,new,1.0)

def changeRadius2(attr,old,new):
    changeObject(2,object_select2.value,new,1.0)

def changeRadius3(attr,old,new):
    changeObject(3,object_select3.value,new,1.0)

object_select1 = Select(title="Object:", value="Kugel (Sphere)",
    options=["Kugel (Sphere)", "Hohlkugel (Hollow sphere)", "Vollzylinder (Full cylinder)", "Hohlzylinder (Hollow cylinder)"])
object_select1.on_change('value',changeObject1)
object_select2 = Select(title="Object:", value="Vollzylinder (Full cylinder)",
    options=["Kugel (Sphere)", "Hohlkugel (Hollow sphere)", "Vollzylinder (Full cylinder)", "Hohlzylinder (Hollow cylinder)"])
object_select2.on_change('value',changeObject2)
object_select3 = Select(title="Object:", value="Hohlzylinder (Hollow cylinder)",
    options=["Kugel (Sphere)", "Hohlkugel (Hollow sphere)", "Vollzylinder (Full cylinder)", "Hohlzylinder (Hollow cylinder)"])
object_select3.on_change('value',changeObject3)
radius_select1 = Slider(title="Radius", value=2.0, start=1.0, end=4.0, step=0.5)
radius_select1.on_change('value',changeRadius1)
radius_select2 = Slider(title="Radius", value=2.0, start=1.0, end=4.0, step=0.5)
radius_select2.on_change('value',changeRadius2)
radius_select3 = Slider(title="Radius", value=2.0, start=1.0, end=4.0, step=0.5)
radius_select3.on_change('value',changeRadius3)

def changeAlpha(attr,old,new):
    global alpha, COS, SIN, offset, H, rampLength, ramp_source
    alpha=radians(new)
    X=[]
    Y=[]
    for i in range(0,11):
        X.append(-3*cos(i*alpha/10.0))
        Y.append(3*sin(i*alpha/10.0))
    AngleMarkerSource.data=dict(x=X,y=Y)
    COS=cos(alpha)
    SIN=sin(alpha)
    offset=-rampLength*COS
    H = rampLength*SIN
    ramp_source.data = dict(x=[offset,0],y=[H,0])
    stop()

alpha_slider = Slider(title=u"\u03B1", value=20.0, start=5.0, end=35.0, step=5.0)
alpha_slider.on_change('value',changeAlpha)

def start():
    global Active, t
    if (not Active):
        t = 0
        curdoc().add_periodic_callback(evolve,200)
        Active = True

def stop():
    global Active, t
    if (Active):
        t = 0
        curdoc().remove_periodic_callback(evolve)
        Active = False
    changeObject(1,object_select1.value,radius_select1.value,1.0)
    changeObject(2,object_select2.value,radius_select2.value,1.0)
    changeObject(3,object_select3.value,radius_select3.value,1.0)

def evolve():
    global t
    t+=0.05
    (x1,y1)=evolveFunc1(t)
    (x2,y2)=evolveFunc2(t)
    (x3,y3)=evolveFunc3(t)
    if (max(x1,x2,x3)>0 or min(y1,y2,y3)<0):
        global Active
        curdoc().remove_periodic_callback(evolve)
        Active = False

start_button = Button(label="Start", button_type="success")
start_button.on_click(start)
stop_button = Button(label="Stop", button_type="success")
stop_button.on_click(stop)

init()
## Send to window
curdoc().add_root(row(column(row(fig1,column(object_select1,radius_select1)),
    row(fig2,column(object_select2,radius_select2)),
    row(fig3,column(object_select3,radius_select3))),
    column(start_button,stop_button,alpha_slider)))
curdoc().title = "Rollversuch"
