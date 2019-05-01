from __future__ import division # float division only, like in python 3
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer, widgetbox
from bokeh.models import ColumnDataSource, LabelSet, CustomJS
from bokeh.models.widgets import Paragraph
#from bokeh.models.ranges import DataRange1d
from bokeh.io import curdoc
from math import sin, cos, pi, sqrt, radians
from os.path import dirname, split, abspath, join
import numpy as np

import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexLabelSet, LatexDiv

###############################################################################
###                            inner app imports                            ###
###############################################################################
from RT_global_variables import (
        glob_SphereXLines, glob_SphereYLines,
        fig_data, fig_lines_data,
        alpha, alpha_max,
        rampLength, maxR,
        ramp_source, wall_source,
        AngleMarkerSource, AlphaPos,
        time_display,
        figure_list,
        TX0, TY0
        )
from RT_object_creation import (
        createSphere,
        createCylinder, createHollowCylinder
        )
from RT_buttons import (
        start_button, reset_button, mode_selection,
        object_select0, object_select1, object_select2,
        radius_slider0, radius_slider1, radius_slider2,
        ri_slider0, ri_slider1, ri_slider2,
        alpha_slider
        )
from RT_callback_functions import (
        start, reset,
        changeObject0, changeObject1, changeObject2, 
        changeRadius0, changeRadius1, changeRadius2, 
        changeWall0, changeWall1, changeWall2,
        changeAlpha,
        object_select_JS
        )


###############################################################################
###                            inital appearance                            ###
###############################################################################
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
        X.append(TX0-3*cos(i*alpha/10.0))
        Y.append(TY0+3*sin(i*alpha/10.0))
    AngleMarkerSource.data=dict(x=X,y=Y)
    AlphaPos.data=dict(x=[-8],y=[-0.1],t=[u"\u03B1"])
    


###############################################################################
###                          general plot settings                          ###
###############################################################################

XStart = TX0-rampLength-maxR-3#-5
#YEnd   = H+2*maxR # start height, but we need height for max alpha
YEnd   = TY0+rampLength*sin(radians(alpha_max))+2*maxR
#Width  = -255.4*XStart/YEnd #-220.0*XStart/YEnd
Width = 500

###############################################################################
###                              ramp figures                               ###
###############################################################################
# draw 3 graphs each containing a ramp, the angle marker, an ellipse, and lines

fig0 = figure(title="Sphere",x_range=(XStart,TX0),y_range=(TY0,YEnd),height=220,width=int(Width), tools="", match_aspect=True)
fig0.ellipse(x='x',y='y',width='w',height='w',fill_color='c',fill_alpha='a',
    line_color="#003359",line_width=3,source=fig_data[0])
fig0.multi_line(xs='x',ys='y',line_color="#003359",line_width=3,source=fig_lines_data[0])
fig0.line(x='x',y='y',color="black",line_width=2,source=ramp_source)
fig0.line(x='x',y='y',color="black",line_width=2,source=wall_source)
fig0.line(x='x',y='y',color="black",line_width=2,source=AngleMarkerSource)
#fig0.grid.visible     = False
fig0.axis.visible     = False
fig0.toolbar_location = None
time_lable0 = LabelSet(x='x', y='y', text='t', source=time_display[0])
fig0.add_layout(time_lable0)
#fig0.circle()


fig1 = figure(title="Full cylinder",x_range=(XStart,TX0),y_range=(TY0,YEnd),height=220,width=int(Width), tools="", match_aspect=True)
fig1.ellipse(x='x',y='y',width='w',height='w',fill_color='c',fill_alpha='a',
    line_color="#003359",line_width=3,source=fig_data[1])
fig1.multi_line(xs='x',ys='y',line_color="#003359",line_width=3,source=fig_lines_data[1])
fig1.line(x='x',y='y',color="black",line_width=2,source=ramp_source)
fig1.line(x='x',y='y',color="black",line_width=2,source=wall_source)
fig1.line(x='x',y='y',color="black",line_width=2,source=AngleMarkerSource)
#fig1.grid.visible     = False
fig1.axis.visible     = False
fig1.toolbar_location = None
time_lable1 = LabelSet(x='x', y='y', text='t', source=time_display[1])
fig1.add_layout(time_lable1)


fig2 = figure(title="Hollow cylinder",x_range=(XStart,TX0),y_range=(TY0,YEnd),height=220,width=int(Width), tools="", match_aspect=True)
fig2.ellipse(x='x',y='y',width='w',height='w',fill_color='c',fill_alpha='a',
    line_color="#003359",line_width=3,source=fig_data[2])
fig2.multi_line(xs='x',ys='y',color="#003359",line_width=3,source=fig_lines_data[2])
fig2.line(x='x',y='y',color="black",line_width=2,source=ramp_source)
fig2.line(x='x',y='y',color="black",line_width=2,source=wall_source)
fig2.line(x='x',y='y',color="black",line_width=2,source=AngleMarkerSource)
#fig2.grid.visible     = False
fig2.axis.visible     = False
fig2.toolbar_location = None
time_lable2 = LabelSet(x='x', y='y', text='t', source=time_display[2])
fig2.add_layout(time_lable2)


###############################################################################
###                           annotation figures                            ###
###############################################################################
# sketch of the ramp and objects
# settings for the annotation plot
a_COS = cos(alpha)
a_SIN = sin(alpha)
atx0 = 0
aty0 = 0
atx1 = atx0 - 50*a_COS
aty1 = aty0 + 50*a_SIN
alx1 = atx1 + 2*a_SIN
aly1 = aty1 + 2*a_COS
alx0 = alx1 + 50*a_COS
aly0 = aly1 - 50*a_SIN
ou = lambda(x): ((aly1-aty1)/(alx1-atx1)*(x-atx1)+aty1)
od = lambda(x): ((aly0-aty0)/(alx0-atx0)*(x-atx0)+aty0)

msr4 = 200/295*1.1  # manual scaling ratio

fig3 = figure(title="Annotations", x_range=(-55,5), y_range=(0,25), height=200, width=295, tools="")
fig3.line(x=[atx0,atx1-5*a_COS],y=[aty0,aty1+5*a_SIN],color="black",line_width=2) # ramp
fig3.line(x=[atx1-5*a_COS,atx1-5*a_COS],y=[aty0,aty1+5*a_SIN],color="black",line_width=2) # wall
fig3.ellipse(x=[alx1],y=[aly1],width=[4],height=[4*msr4],fill_color="#0065BD",fill_alpha=[0.2],line_color="#003359",line_alpha=[0.2],line_width=3)
fig3.ellipse(x=[alx1],y=[aly1],width=[2.5],height=[4*msr4],fill_alpha=[0],line_color="#003359",line_alpha=[0.2],line_width=3, angle=-0.7)
#fig3.ellipse(x=[0],y=[-1],width=[12], height=[10], fill_alpha=[0], line_color='black', line_width=2, line_dash='15 50', line_dash_offset=-10)

# L annotation
fig3.line(x=[alx1,alx0],y=[aly1,aly0],color="black",line_width=1.5)
fig3.line(x=[alx1-0.8,alx1+0.9],y=[ou(alx1-0.5),ou(alx1+0.5)],color="black",line_width=1.5)
fig3.line(x=[alx0-0.5,alx0+1.1],y=[od(alx0-0.5),od(alx0+0.5)],color="black",line_width=1.5)

L_label_source = ColumnDataSource(data=dict(x=[-23],y=[11],t=["L"]))
L_label = LabelSet(x='x', y='y', text='t', angle=-radians(25),  source=L_label_source, render_mode="css")
fig3.add_layout(L_label)

# alpha annotation
fig3.line(x=[TX0-10*cos(i*alpha/10.0) for i in range(0,11)],y=[TY0+10*sin(i*alpha/10.0) for i in range(0,11)],color="black",line_width=2)
angle_glyph3 = LabelSet(x='x', y='y',text='t',text_color='black',text_font_size="15pt", source=AlphaPos)
fig3.add_layout(angle_glyph3)

fig3.grid.visible = False
fig3.axis.visible = False
fig3.toolbar_location = None

#x_range = DataRange1d(start=-10, end=10, bounds=(-10,10))
#y_range = DataRange1d(start=-5, end=5, bounds=(-5,5))

#x_range = DataRange1d(bounds=(-10,10))
#y_range = DataRange1d(bounds=(-5,5))
f4h  = 200
f4w  = 295
msr4 = f4h/f4w*1.1  # manual scaling ratio

fig4 = figure(x_range=(-10,10), y_range=(-5,5), height=f4h, width=f4w, tools="", match_aspect=True)
#fig4 = figure(x_range=x_range, y_range=y_range, height=f4h, width=f4w, tools="", aspect_scale=f4h/f4w)#, match_aspect=True)
#fig4 = figure(x_range=x_range, y_range=y_range, height=f4h, width=f4w, tools="")#, match_aspect=True)
#fig4.ellipse(x=[-5,-5],y=[0,0],width=[4,6],height=[4,6],fill_alpha=[0,0],line_color='black',line_width=3)
fig4.ellipse(x=[-5,-5],y=[0,0],width=[6,8],height=[6*msr4,8*msr4],fill_alpha=[0,0],line_color='black',line_width=3)
#fig4.circle(x=[-5,-5],y=[0,0],radius=[2,3],radius_dimension='y',fill_alpha=[0,0],line_color='black',line_width=3)
fig4.line(x=[-5,-5],y=[0,4*msr4],line_width=2)
#fig4.line(x=[-5,-5],y=[0,3],line_width=2)
fig4.line(x=[-5,-2],y=[0,0],line_width=2)
r_lables_source = ColumnDataSource(data=dict(x=[-4.2,-5.7,0,0],y=[-0.9,1,1,-1],t=["r_i","r","r\\:=\\text{Radius}","r_i=\\text{Inner radius}"]))
r_lables = LatexLabelSet(x='x', y='y', text='t', source=r_lables_source)
fig4.add_layout(r_lables)
fig4.grid.visible = False
fig4.axis.visible = False
fig4.toolbar_location = None



# put the figures in a list for easy access in functions
#figure_list = [fig0,fig1,fig2]
figure_list[0] = fig0
figure_list[1] = fig1
figure_list[2] = fig2




###############################################################################
###                           selection callbacks                           ###
###############################################################################
object_select0.on_change('value',changeObject0)
object_select1.on_change('value',changeObject1)
object_select2.on_change('value',changeObject2)

# stears visability of inner radius sliders (show only for hollow objects)
object_select0.callback = CustomJS(code=object_select_JS)
object_select1.callback = CustomJS(code=object_select_JS)
object_select2.callback = CustomJS(code=object_select_JS)


###############################################################################
###                            slider callbacks                             ###
###############################################################################
# radius
radius_slider0.on_change('value',changeRadius0)
radius_slider1.on_change('value',changeRadius1)
radius_slider2.on_change('value',changeRadius2)

# inner radius
ri_slider0.on_change('value',changeWall0)
ri_slider1.on_change('value',changeWall1)
ri_slider2.on_change('value',changeWall2)

# angle of the ramp
alpha_slider.on_change('value',changeAlpha)


###############################################################################
###                            button callbacks                             ###
###############################################################################
start_button.on_click(start)
reset_button.on_click(reset)



###############################################################################
###                          page styling / layout                          ###
###############################################################################
 # initial appearance
init()

# description of radio button mode choice
p_mode = Paragraph(text="""Stopping mode: """)

# description of the app
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1180)

## Send to window
curdoc().add_root(column(description,row(column(row(fig0,column(object_select0,radius_slider0,ri_slider0)),
    row(fig1,column(object_select1,radius_slider1,ri_slider1)),
    row(fig2,column(object_select2,radius_slider2,ri_slider2))),Spacer(width=100),
    column(start_button,reset_button,row(widgetbox(p_mode,width=120),mode_selection),alpha_slider, Spacer(height=20), fig3, Spacer(height=40), fig4))))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
