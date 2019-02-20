from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.models import ColumnDataSource, Select, Button, LabelSet, Slider, CustomJS
from bokeh.io import curdoc
from math import sin, cos, pi, sqrt, radians
from os.path import dirname, split
import numpy as np

# create variables
g         = 9.81
alpha     = radians(20)
# constants
maxR       = 4.0
alpha_max  = 25.0
rampLength = 50
# variables created to avoid repeated calculations
# (speeds up calculations)
SIN        = sin(alpha)
COS        = cos(alpha)
offset     = -rampLength*COS
t          = 0.0
H          = rampLength*SIN

SphereXLines = [np.array([]),np.array([])]
SphereYLines = np.array([])

# create ColumnDataSources
fig1_data         = ColumnDataSource(data = dict(x=[],y=[],w=[],c=[],a=[]))
fig1_lines_data   = ColumnDataSource(data = dict(x=[],y=[]))
fig2_data         = ColumnDataSource(data = dict(x=[],y=[],w=[],c=[],a=[]))
fig2_lines_data   = ColumnDataSource(data = dict(x=[],y=[]))
fig3_data         = ColumnDataSource(data = dict(x=[],y=[],w=[],c=[],a=[]))
fig3_lines_data   = ColumnDataSource(data = dict(x=[],y=[]))
ramp_source       = ColumnDataSource(data = dict(x=[offset,0],y=[H,0]))
AngleMarkerSource = ColumnDataSource(data = dict(x=[],y=[]))
AlphaPos          = ColumnDataSource(data = dict(x=[],y=[],t=[]))

# global variables
glob_callback_id  = ColumnDataSource(data = dict(callback_id = [None]))
glob_SphereXLines = ColumnDataSource(data = dict(SphereXLines = [SphereXLines]))
glob_SphereYLines = ColumnDataSource(data = dict(SphereYLines = [SphereYLines]))
# following ColumnDataSources could be exchanged by a single dict
#
#glob_offset       = ColumnDataSource(data = dict(offset = [offset]))
#glob_SIN          = ColumnDataSource(data = dict(SIN = [SIN]))
#glob_COS          = ColumnDataSource(data = dict(COS = [COS]))
#glob_g            = ColumnDataSource(data = dict(g = [g]))
#glob_alpha        = ColumnDataSource(data = dict(alpha = [alpha]))
#glob_t            = ColumnDataSource(data = dict(t = [t]))

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
    createSphere(2.0,fig1_data,fig1_lines_data)
    createCylinder(2.0,fig2_data,fig2_lines_data)
    createHollowCylinder(2.0,1.5,fig3_data,fig3_lines_data)
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
    #[offset]       = glob_offset.data["offset"]             # input/
    #[SIN]          = glob_SIN.data["SIN"]                   # input/
    #[COS]          = glob_COS.data["COS"]                   # input/
    load_vals = ["SIN", "COS", "offset", "H"]
    SIN, COS, offset, H = [glob_values.get(val) for val in load_vals]
    # find the centre, knowing that it touches the ramp at (offset,H)
    newX = offset+r*SIN
    #newX = glob_values["offset"]+r*glob_values["SIN"]
    newY = H+r*COS
    #newY = glob_values["H"]+r*glob_values["COS"]
    # draw the sphere in blue
    sphere_data.data=dict(x=[newX],y=[newY],w=[2*r],c=["#0065BD"],a=[1])
    # use the referece lines to find the current position of the lines
    RCOS = r*COS
    RSIN = r*SIN
    #RCOS = r*glob_values["COS"]
    #RSIN = r*glob_values["SIN"]
    X1 = SphereXLines[0]*RCOS+SphereYLines*RSIN+newX
    X2 = SphereXLines[1]*RCOS+SphereYLines*RSIN+newX
    Y1 = -SphereXLines[0]*RSIN+SphereYLines*RCOS+newY
    Y2 = -SphereXLines[1]*RSIN+SphereYLines*RCOS+newY
    # draw the lines
    sphere_lines_data.data=dict(x=[X1, X2],y=[Y1,Y2])

def moveSphere(t,r,m,sphere_data,sphere_lines_data):
    [SphereXLines] = glob_SphereXLines.data["SphereXLines"] # input/
    [SphereYLines] = glob_SphereYLines.data["SphereYLines"] # input/
    #[offset]       = glob_offset.data["offset"]             # input/
    #[SIN]          = glob_SIN.data["SIN"]                   # input/
    #[COS]          = glob_COS.data["COS"]                   # input/
    #[g]            = glob_g.data["g"]                       # input/
    #[alpha]        = glob_alpha.data["alpha"]               # input/
    load_vals = ["g", "alpha", "SIN", "COS", "offset", "H"]
    g, alpha, SIN, COS, offset, H = [glob_values.get(val) for val in load_vals]
    # find the displacement of the point touching the ramp
    displacement = g*SIN*t*t*1.25
    #displacement = glob_values["g"]*SIN*t*t*1.25
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
    #[offset]       = glob_offset.data["offset"]             # input/
    #[SIN]          = glob_SIN.data["SIN"]                   # input/
    #[COS]          = glob_COS.data["COS"]                   # input/
    load_vals = ["SIN", "COS", "offset", "H"]
    SIN, COS, offset, H = [glob_values.get(val) for val in load_vals]
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
    #[offset]       = glob_offset.data["offset"]             # input/
    #[SIN]          = glob_SIN.data["SIN"]                   # input/
    #[COS]          = glob_COS.data["COS"]                   # input/
    #[g]            = glob_g.data["g"]                       # input/
    #[alpha]        = glob_alpha.data["alpha"]               # input/
    load_vals = ["g", "alpha", "SIN", "COS", "offset", "H"]
    g, alpha, SIN, COS, offset, H = [glob_values.get(val) for val in load_vals]
    try:
        temp = r*g*SIN*t*t*1.25*(r**3-ri**3)/(r**5-ri**5)
    except ZeroDivisionError:
        ri   = r-1e-3;
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
    #[offset]       = glob_offset.data["offset"]             # input/
    #[SIN]          = glob_SIN.data["SIN"]                   # input/
    #[COS]          = glob_COS.data["COS"]                   # input/
    load_vals = ["SIN", "COS", "offset", "H"]
    SIN, COS, offset, H = [glob_values.get(val) for val in load_vals]
    # draw the cylinder around the centre, knowing that it touches the ramp at (offset,H)
    cylinder_data.data=dict(x=[offset+r*SIN],y=[H+r*COS],w=[2*r],c=["#0065BD"],a=[1])
    cylinder_lines_data.data=dict(x=[[offset,offset+2*r*SIN],
        [offset+r*(SIN-COS),offset+r*(SIN+COS)]],
        y=[[H,H+2*r*COS],[H+r*(COS+SIN),H+r*(COS-SIN)]])

def moveCylinder(t,r,m, cylinder_data, cylinder_lines_data):
    #[offset]       = glob_offset.data["offset"]             # input/
    #[SIN]          = glob_SIN.data["SIN"]                   # input/
    #[COS]          = glob_COS.data["COS"]                   # input/
    #[g]            = glob_g.data["g"]                       # input/
    #[alpha]        = glob_alpha.data["alpha"]               # input/
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
    #[offset]       = glob_offset.data["offset"]             # input/
    #[SIN]          = glob_SIN.data["SIN"]                   # input/
    #[COS]          = glob_COS.data["COS"]                   # input/
    load_vals = ["SIN", "COS", "offset", "H"]
    SIN, COS, offset, H = [glob_values.get(val) for val in load_vals]
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
    #[offset]       = glob_offset.data["offset"]             # input/
    #[SIN]          = glob_SIN.data["SIN"]                   # input/
    #[COS]          = glob_COS.data["COS"]                   # input/
    #[g]            = glob_g.data["g"]                       # input/
    #[alpha]        = glob_alpha.data["alpha"]               # input/
    load_vals = ["g", "alpha", "SIN", "COS", "offset", "H"]
    g, alpha, SIN, COS, offset, H = [glob_values.get(val) for val in load_vals]
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

XStart = -rampLength-maxR-5
#YEnd   = H+2*maxR # start height, but we need height for max alpha
YEnd   = rampLength*sin(radians(alpha_max))+2*maxR
Width  = -255.4*XStart/YEnd #-220.0*XStart/YEnd
fig1 = figure(title="Sphere",x_range=(XStart,0),y_range=(0,YEnd),height=220,width=int(Width))
fig1.ellipse(x='x',y='y',width='w',height='w',fill_color='c',fill_alpha='a',
    line_color="#003359",line_width=3,source=fig1_data)
fig1.multi_line(xs='x',ys='y',line_color="#003359",line_width=3,source=fig1_lines_data)
fig1.line(x='x',y='y',color="black",line_width=2,source=ramp_source)
fig1.line(x='x',y='y',color="black",line_width=2,source=AngleMarkerSource)
angle_glyph1=LabelSet(x='x', y='y',text='t',text_color='black',
    text_font_size="15pt", source=AlphaPos)
fig1.add_layout(angle_glyph1)
fig1.toolbar_location = None
#fig1.toolbar.logo = None

fig2 = figure(title="Full cylinder",x_range=(XStart,0),y_range=(0,YEnd),height=220,width=int(Width))
fig2.ellipse(x='x',y='y',width='w',height='w',fill_color='c',fill_alpha='a',
    line_color="#003359",line_width=3,source=fig2_data)
fig2.multi_line(xs='x',ys='y',line_color="#003359",line_width=3,source=fig2_lines_data)
fig2.line(x='x',y='y',color="black",line_width=2,source=ramp_source)
fig2.line(x='x',y='y',color="black",line_width=2,source=AngleMarkerSource)
angle_glyph2=LabelSet(x='x', y='y',text='t',text_color='black',
    text_font_size="15pt", source=AlphaPos)
fig2.add_layout(angle_glyph2)
fig2.toolbar_location = None
#fig2.toolbar.logo = None

fig3 = figure(title="Hollow cylinder",x_range=(XStart,0),y_range=(0,YEnd),height=220,width=int(Width))
fig3.ellipse(x='x',y='y',width='w',height='w',fill_color='c',fill_alpha='a',
    line_color="#003359",line_width=3,source=fig3_data)
fig3.multi_line(xs='x',ys='y',color="#003359",line_width=3,source=fig3_lines_data)
fig3.line(x='x',y='y',color="black",line_width=2,source=ramp_source)
fig3.line(x='x',y='y',color="black",line_width=2,source=AngleMarkerSource)
angle_glyph3=LabelSet(x='x', y='y',text='t',text_color='black',
    text_font_size="15pt", source=AlphaPos)
fig3.add_layout(angle_glyph3)
fig3.toolbar_location = None

# name the functions to be used by each figure depending upon their content
evolveFunc1=lambda(x):moveSphere(x,2.0,1.0,fig1_data,fig1_lines_data)
evolveFunc2=lambda(x):moveCylinder(x,2.0,1.0,fig2_data,fig2_lines_data)
evolveFunc3=lambda(x):moveHollowCylinder(x,2.0,1.0,1.5,fig3_data,fig3_lines_data)
glob_fun_handles = dict(fun1=evolveFunc1, fun2=evolveFunc2, fun3=evolveFunc3)

# function to change the shape, radius, or mass of the object in figure FIG
def changeObject(FIG,new,r,wt,m):
    # save the data concerned in data and line_data
    if (FIG==1):
        data=fig1_data
        line_data=fig1_lines_data
    elif(FIG==2):
        data=fig2_data
        line_data=fig2_lines_data
    else:
        data=fig3_data
        line_data=fig3_lines_data
    # depending on the shape specified, create the object and
    # save the new evolution function in the variable func
    if (new == "Sphere"):
        createSphere(r,data,line_data)
        func=lambda(x):moveSphere(x,r,m,data,line_data)
    elif (new=="Hollow cylinder"):
        createHollowCylinder(r,r-wt,data,line_data)
        func=lambda(x):moveHollowCylinder(x,r,m,r-wt,data,line_data)
    elif (new == "Hollow sphere"):
        createHollowSphere(r,r-wt,data,line_data)
        func=lambda(x):moveHollowSphere(x,r,m,r-wt,data,line_data)
    else:
        createCylinder(r,data,line_data)
        func=lambda(x):moveCylinder(x,r,m,data,line_data)
    # save the evolution function to the appropriate function handle
    if (FIG==1):
        #global evolveFunc1
        #evolveFunc1=func
        glob_fun_handles["fun1"] = func
        
        fig1.title.text=new
    elif(FIG==2):
        #global evolveFunc2
        #evolveFunc2=func
        glob_fun_handles["fun2"] = func
        fig2.title.text=new
    else:
        #global evolveFunc3
        #evolveFunc3=func
        glob_fun_handles["fun3"] = func
        fig3.title.text=new
    # if a simulation is in progress, restart it
    #global Active,t
    #if (Active):
    #    t=0.0

## slider functions
# functions to change the shape
def changeObject1(attr,old,new):
    changeObject(1,new,radius_select1.value,wall_select1.value,1.0)

def changeObject2(attr,old,new):
    changeObject(2,new,radius_select2.value,wall_select2.value,1.0)

def changeObject3(attr,old,new):
    changeObject(3,new,radius_select3.value,wall_select3.value,1.0)

# functions to change the radius
def changeRadius1(attr,old,new):
    changeObject(1,object_select1.value,new,wall_select1.value,1.0)
    wall_select1.end = new

def changeRadius2(attr,old,new):
    changeObject(2,object_select2.value,new,wall_select2.value,1.0)
    wall_select2.end = new

def changeRadius3(attr,old,new):
    changeObject(3,object_select3.value,new,wall_select3.value,1.0)
    wall_select3.end = new
    
#functions to change the inner radius  / wall thickness
def changeWall1(attr,old,new):
    changeObject(1,object_select1.value,radius_select1.value,new,1.0)
def changeWall2(attr,old,new):
    changeObject(2,object_select2.value,radius_select2.value,new,1.0)
def changeWall3(attr,old,new):
    changeObject(3,object_select3.value,radius_select3.value,new,1.0)
    
#changeWall3_JS = """
#console.log("test");
#"""

object_select_JS = """
choice = cb_obj.value;
console.log(choice);
caller = cb_obj.name;
console.log(caller);

// extract the number of the name and convert it to integer
slider_idx = parseInt(caller.match(/\d/g).join(""))-1; //-1 for starting at 0
console.log(slider_idx)

slider_in_question = document.getElementsByClassName("wall_slider")[slider_idx];

console.log(slider_in_question)

// if hollow object is selected, show the slider (get rid of hidden)
if(choice.includes("Hollow")){
        slider_in_question.className=slider_in_question.className.replace(" hidden","");
        // special case for hollow sphere: ri != r, i.e. wallthickness of zero not allowed
        if(choice.includes("sphere")){
                console.log("there");
                console.log(slider_in_question.start); // undefined
                slider_in_question.start=0.5;  // does not work, how to access start??
        }
}
// if full object is select, check if slider is hidden; if not, hide it
else if(!slider_in_question.className.includes("hidden")){
        slider_in_question.className+=" hidden";
}

console.log(slider_in_question)
console.log("------")


"""


# sliders
object_select1 = Select(title="Object:", value="Sphere", name="obj1",
    options=["Sphere", "Hollow sphere", "Full cylinder", "Hollow cylinder"])
object_select1.on_change('value',changeObject1)
object_select2 = Select(title="Object:", value="Full cylinder", name="obj2",
    options=["Sphere", "Hollow sphere", "Full cylinder", "Hollow cylinder"])
object_select2.on_change('value',changeObject2)
object_select3 = Select(title="Object:", value="Hollow cylinder", name="obj3",
    options=["Sphere", "Hollow sphere", "Full cylinder", "Hollow cylinder"])
object_select3.on_change('value',changeObject3)

object_select1.callback = CustomJS(code=object_select_JS)
object_select2.callback = CustomJS(code=object_select_JS)
object_select3.callback = CustomJS(code=object_select_JS)

radius_select1 = Slider(title="Radius", value=2.0, start=1.0, end=maxR, step=0.5)
radius_select1.on_change('value',changeRadius1)
radius_select2 = Slider(title="Radius", value=2.0, start=1.0, end=maxR, step=0.5)
radius_select2.on_change('value',changeRadius2)
radius_select3 = Slider(title="Radius", value=2.0, start=1.0, end=maxR, step=0.5)
radius_select3.on_change('value',changeRadius3)

# ri = 0 ok
# ri = r  --> zero div at hollow sphere
# ri = r - wall_thickness
# end value dependend on selected radius size
wall_select1 = Slider(title="wall thickness", value=0.5, start=0.0, end=2.0, step=0.5, css_classes=["wall_slider", "obj1", "hidden"])
wall_select1.on_change('value',changeWall1)
wall_select2 = Slider(title="wall thickness", value=0.5, start=0.0, end=2.0, step=0.5, css_classes=["wall_slider", "obj2", "hidden"])
wall_select2.on_change('value',changeWall2)
wall_select3 = Slider(title="wall thickness", value=0.5, start=0.0, end=2.0, step=0.5, css_classes=["wall_slider", "obj3", "hidden"])
wall_select3.on_change('value',changeWall3)
#wall_select3.js_on_change('value',changeWall3_JS)
#wall_select3.callback = CustomJS(code=changeWall3_JS)

# slider function for the angle
def changeAlpha(attr,old,new):
    #global alpha, COS, SIN, offset, H
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
    #print("<<<<check<<<<", glob_values)
    ramp_source.data = dict(x=[offset,0],y=[H,0])
    reset()

# slider for the angle
alpha_slider = Slider(title=u"\u03B1", value=20.0, start=5.0, end=alpha_max, step=1.0)
alpha_slider.on_change('value',changeAlpha)

def disable_all_sliders(d=True):
    object_select1.disabled = d
    object_select2.disabled = d
    object_select3.disabled = d
    radius_select1.disabled = d
    radius_select2.disabled = d
    radius_select3.disabled = d
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
    #[t] = glob_t.data["t"] # input/output
    # reset the simulation
    #glob_t.data = dict(t = [0.0]) #      /output
    glob_values["t"] = 0.0 #      /output
    changeObject(1,object_select1.value,radius_select1.value,0.5,1.0)
    changeObject(2,object_select2.value,radius_select2.value,0.5,1.0)
    changeObject(3,object_select3.value,radius_select3.value,0.5,1.0)
    disable_all_sliders(False)

    

def evolve():
    #[t] = glob_t.data["t"] # input/output
    t = glob_values["t"] # input/output
    t+=0.01
    #glob_t.data = dict(t = [t])
    glob_values["t"] = t
    # call all necessary functions
    #(x1,y1)=evolveFunc1(t)
    #(x2,y2)=evolveFunc2(t)
    #(x3,y3)=evolveFunc3(t)
    (x1,y1) = glob_fun_handles["fun1"](t)
    (x2,y2) = glob_fun_handles["fun2"](t)
    (x3,y3) = glob_fun_handles["fun3"](t)
    # if an object has reached the end of the ramp then stop the simulation
    if (max(x1,x2,x3)>0 or min(y1,y2,y3)<0):
        start() #equals to stop if it is running

# create the buttons
start_button = Button(label="Start", button_type="success")
start_button.on_click(start)
reset_button = Button(label="Reset", button_type="success")
reset_button.on_click(reset)

init()
## Send to window
curdoc().add_root(row(column(row(fig1,column(object_select1,radius_select1,wall_select1)),
    row(fig2,column(object_select2,radius_select2,wall_select2)),
    row(fig3,column(object_select3,radius_select3,wall_select3))),Spacer(width=100),
    column(start_button,reset_button,alpha_slider)))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
