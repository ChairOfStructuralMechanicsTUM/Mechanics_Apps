# -*- coding: utf-8 -*-
"""
@author: antonis, matthias (re-structured to function design)
"""
from __future__ import division
import numpy as np
import pandas as pd
from scipy.optimize import brentq # fast numerical solver for roots
from bokeh.io import curdoc
from bokeh.layouts import row,column, gridplot
from bokeh.models import ColumnDataSource,CustomJS, Label,Legend
from bokeh.models.widgets import Slider,Toggle, Paragraph
from bokeh.plotting import figure
from os.path import dirname, join, split, abspath
# for LaTeX support
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_div import LatexDiv

# beam length
l=1

# first ev eigenvalues for each beam
ev_total = 4

#beam 1-->simply supported
beam1 = ColumnDataSource(data=dict(x=[0,1], y=[0,0]))
#create the boundary conditions for simply supported beam
support_left=ColumnDataSource(data=dict(x=[0,-0.05,0.05,0.025,0.05,0.025,0,0.025,0,-0.025,0,-0.025,-0.05,-0.025,-0.05,-0.075,-0.05,0.05,0], y=[0,-0.5,-0.5,
                                        -0.7,-0.5,-0.5,-0.7,-0.5,-0.5,-0.7,-0.5,-0.5,-0.7,-0.5,-0.5,-0.7,-0.5,-0.5,0]))
support_righta=ColumnDataSource(data=dict(x=[1,0.95,1.05,1],y=[0,-0.5,-0.5,0]))
support_rightb= ColumnDataSource(data=dict(x=[0.95,1.05,1.025,1.05,1.025,1,1.025,1,0.975,1,0.975,0.95,0.975,0.95],y=[-0.7,-0.7,-0.9,-0.7,-0.7,-0.9,-0.7,-0.7,
                                           -0.9,-0.7,-0.7,-0.9,-0.7,-0.7]))

#beam 2-->fixed at both ends
beam2 = ColumnDataSource(data=dict(x=[0,1], y=[0,0]))
#create the boundary conditions for the beam fixed at both ends
fixed_left=ColumnDataSource(data=dict(x=[0,0,-0.03,0,0,-0.03,0,0,-0.03,0,0,-0.03,0,0,-0.03],y=[2*0.25,-2*0.25,-2*0.3,-2*0.25,-2*0.125,-2*0.175,-2*0.125,0,-2*0.05,-0,+2*0.125,
                                        +2*0.075,+2*0.125,2*0.25,2*0.2]))
fixed_right=ColumnDataSource(data=dict(x=[1,1,1.03,1,1,1.03,1,1,1.03,1,1,1.03,1,1,1.03],y=[2*0.25,-2*0.25,-2*0.3,-2*0.25,-2*0.125,-2*0.175,-2*0.125,0,-2*0.05,-0,+2*0.125,
                                        +2*0.075,+2*0.125,2*0.25,2*0.2]))

#beam 3-->cantilever beam
beam3=ColumnDataSource(data=dict(x=[0,1], y=[0,0]))
#create the left fixed support for the cantilever beam
fixed_cantil=ColumnDataSource(data=dict(x=[0,0,-0.03,0,0,-0.03,0,0,-0.03,0,0,-0.03,0,0,-0.03],y=[2*0.25,-2*0.25,-2*0.3,-2*0.25,-2*0.125,-2*0.175,-2*0.125,0,-2*0.05,-0,+2*0.125,
                                        +2*0.075,+2*0.125,2*0.25,2*0.2]))


## pre-compute the eigenvalues for all beams
def eq_fixed_beam(x):
    return np.cosh(x)*np.cos(x) - 1.0

def eq_cantilever_beam(x):
    return np.cosh(x)*np.cos(x) + 1.0


x_start_fixed_beam, x_start_cant_beam = [[],[]] 
x_end_fixed_beam, x_end_cant_beam = [[],[]]

# set start and end of intervals surounding a root
# x_mid approximates the roots (good approximation for ev>3)
# set some variance to define an interval for the root search via brentq
for k in range(1,ev_total+1):
    x_mid_fixed_beam = 0.5*np.pi*(2*k+1)/l
    x_mid_cant_beam  = 0.5*np.pi*(2*k-1)/l
    x_start_fixed_beam.append(x_mid_fixed_beam - 0.5)
    x_start_cant_beam.append(x_mid_cant_beam - 0.5)
    x_end_fixed_beam.append(x_mid_fixed_beam + 0.5)
    x_end_cant_beam.append(x_mid_cant_beam + 0.5)

# compute the roots, i.e. eigenvalues
ev_fixed_beam = np.zeros((ev_total,1))
ev_cant_beam = np.zeros((ev_total,1))
for k in range(0,ev_total):
    ev_fixed_beam[k] = brentq(eq_fixed_beam, x_start_fixed_beam[k], x_end_fixed_beam[k])
    ev_cant_beam[k]  = brentq(eq_cantilever_beam, x_start_cant_beam[k], x_end_cant_beam[k])
## end of pre-computation


# initialize ColumnDataSources
source1 = ColumnDataSource(data=dict(x=[0],y=[0]))

source2=ColumnDataSource(data=dict(x=[0],y=[0]))
source2cosh=ColumnDataSource(data=dict(x=[0],y=[0]))
source2sinh=ColumnDataSource(data=dict(x=[0],y=[0]))
source2cos=ColumnDataSource(data=dict(x=[0],y=[0]))
source2sin=ColumnDataSource(data=dict(x=[0],y=[0]))

source3=ColumnDataSource(data=dict(x=[0],y=[0]))
source3cosh=ColumnDataSource(data=dict(x=[0],y=[0]))
source3sinh=ColumnDataSource(data=dict(x=[0],y=[0]))
source3cos=ColumnDataSource(data=dict(x=[0],y=[0]))
source3sin=ColumnDataSource(data=dict(x=[0],y=[0]))

    
# define functions instead of hard-coded solutions
def beam_simple_supp(ev_num=1, N=200):
    #print("simple_supp:", ev_num)
    x1 = np.linspace(0, 1, N)
    y1=-np.sin(ev_num*np.pi*x1/l)
    source1.data=dict(x=x1,y=y1)
    
def beam_fixed_ends(ev_num=1, N=200):
    #print("fixed: ", ev_num)
    x2=np.linspace(0,1,N)
    ev = ev_fixed_beam[ev_num-1]
    #print("fixed_val: ", ev)
    y2=-(1/2*(np.cosh(ev*x2/l)-np.cos(ev*x2/l))-((1/2*(np.cosh(ev)-np.cos(ev)))/(1/2*(np.sinh(ev)-np.sin(ev))))*1/2*(np.sinh(ev*x2/l)-np.sin(ev*x2/l)))
    y2cosh=-(1/2*(np.cosh(ev*x2/l)))
    y2sinh=+((1/2*(np.cosh(ev)-np.cos(ev)))/(1/2*(np.sinh(ev)-np.sin(ev))))*1/2*(np.sinh(ev*x2/l))
    y2cos=-(1/2*(np.cos(ev*x2/l)))
    y2sin=-((1/2*(np.cosh(ev)-np.cos(ev)))/(1/2*(np.sinh(ev)-np.sin(ev))))*1/2*(np.sin(ev*x2/l))
    source2.data=dict(x=x2,y=y2)
    source2cosh.data=dict(x=x2,y=y2cosh)
    source2sinh.data=dict(x=x2,y=y2sinh)
    source2cos.data=dict(x=x2,y=y2cos)
    source2sin.data=dict(x=x2,y=y2sin)
    
def beam_cantilever(ev_num=1, N=200):
    #print("canti: ", ev_num)
    x3=np.linspace(0,1,N)
    ev = ev_cant_beam[ev_num-1]
    #print("cant_val: ", ev)
    y3=-(1/2*(np.cosh(ev*x3/l)-np.cos(ev*x3/l))-((1/2*(np.cosh(ev)+np.cos(ev)))/(1/2*(np.sinh(ev)+np.sin(ev))))*1/2*(np.sinh(ev*x3/l)-
                np.sin(ev*x3/l)))
    y3cosh=-(1/2*(np.cosh(ev*x3/l)))
    y3sinh=+((1/2*(np.cosh(ev)+np.cos(ev)))/(1/2*(np.sinh(ev)+np.sin(ev))))*1/2*(np.sinh(ev*x3/l))
    y3cos=-(1/2*(np.cos(ev*x3/l)))
    y3sin=-((1/2*(np.cosh(ev)+np.cos(ev)))/(1/2*(np.sinh(ev)+np.sin(ev))))*1/2*(np.sin(ev*x3/l))
    source3.data=dict(x=x3,y=y3)
    source3cosh.data=dict(x=x3,y=y3cosh)
    source3sinh.data=dict(x=x3,y=y3sinh)
    source3cos.data=dict(x=x3,y=y3cos)
    source3sin.data=dict(x=x3,y=y3sin)

    
# call functions for initial view
beam_simple_supp()
beam_fixed_ends()
beam_cantilever()



#Plot 1
p1 = figure(plot_height=250, plot_width=900,title="Simply supported beam", tools="", x_range=(-0.075,1.075), y_range=(-2.5,2.5))
p1.axis.visible = False
#p1.grid.visible = False
p1.outline_line_color = None
p1.title.text_font_size="13pt"

beam1=p1.line(x='x', y='y', source=beam1,line_width=5,line_color='black') 
eigenmodes_beam1=p1.line(x='x', y='y', source=source1,
                         line_width=3,line_color='#0065BD')
eigenmodes_beam1.visible=True
support_left_beam1=p1.line(x='x', y='y', source=support_left,line_width=2,line_color='black')
support_righta_beam1=p1.line(x='x', y='y', source=support_righta,line_width=2,line_color='black')
support_rightb_beam1=p1.line(x='x', y='y', source=support_rightb,line_width=2,line_color='black')

legend1 = Legend(items=[
    ("Eigenvalue Problem: sin("u"\u03BB)=0 "u"\u279CSolution: w"u"\u1D62("u"\u03BE)=sin(i"u"\u00B7"u"\u03C0"u"\u00B7"u"\u03BE)"   , [eigenmodes_beam1]),
], location=(0, 0))

p1.add_layout(legend1, 'above')
p1.legend.click_policy="hide"

#Plot 2
p2 = figure(plot_height=400, plot_width=900,title="Beam fixed at both ends", tools="", x_range=(-0.075,1.075), y_range=(-3,3))
p2.axis.visible = False
#p2.grid.visible = False
p2.outline_line_color = None
p2.title.text_font_size="13pt"

beam2=p2.line(x='x', y='y', source=beam2,line_width=5,line_color='black') 
eigenmodes_beam2=p2.line(x='x', y='y', source=source2,
                         line_width=3,line_color='#A2AD00')# pantone 383
eigenmodes_beam2cosh=p2.line(x='x', y='y', source=source2cosh,
                         line_width=1, color='#c6f808')#greeny wellow
eigenmodes_beam2sinh=p2.line(x='x', y='y', source=source2sinh,
                         line_width=1,line_color='#9bb53c')#booger
eigenmodes_beam2cos=p2.line(x='x', y='y', source=source2cos,
                         line_width=1,line_color='#677a04')#olive green
eigenmodes_beam2sin=p2.line(x='x', y='y', source=source2sin,
                         line_width=1,line_color='#ffda03')#sunflower yellow
fixed_support_left=p2.line(x='x', y='y', source=fixed_left,line_width=2,line_color='black')
fixed_support_right=p2.line(x='x', y='y', source=fixed_right,line_width=2,line_color='black')
legend2 = Legend(items=[
    ("Eigenvalue Problem: cosh("u"\u03BB)"u"\u00B7cos("u"\u03BB)-1=0 "u"\u279C Solution: w"u"\u1D62("u"\u03BE) = c("u"\u03BB"u"\u1D62"u"\u03BE) - c("u"\u03BB"u"\u1D62) / s("u"\u03BB"u"\u1D62) "u"\u00B7s ("u"\u03BB"u"\u1D62"u"\u03BE)", [eigenmodes_beam2]),
    ("Solution part: "u"\u00BD "u"\u00B7 cosh ("u"\u03BB"u"\u00B7"u"\u03BE)", [eigenmodes_beam2cosh]),
    ("Solution part: -"u"\u00BD "u"\u00B7 c("u"\u03BB)/s("u"\u03BB)"u"\u00B7 sinh ("u"\u03BB"u"\u00B7"u"\u03BE)", [eigenmodes_beam2sinh]),
    ("Solution part: -"u"\u00BD "u"\u00B7 cos ("u"\u03BB"u"\u00B7"u"\u03BE)", [eigenmodes_beam2cos]),
    ("Solution part: "u"\u00BD "u"\u00B7 c("u"\u03BB)/s("u"\u03BB) "u"\u00B7 sin ("u"\u03BB"u"\u00B7"u"\u03BE)", [eigenmodes_beam2sin]),
], location=(0, 0))

p2.add_layout(legend2, 'above')
p2.legend.click_policy="hide"

#Plot 3
p3 = figure(plot_height=400, plot_width=900,title="Cantilever beam", tools="", x_range=(-0.075,1.075), y_range=(-3,3))
p3.axis.visible = False
#p3.grid.visible = False
p3.outline_line_color = None
p3.title.text_font_size="13pt"

beam3=p3.line(x='x', y='y', source=beam3,line_width=5,line_color='black') 
fixed_cantilever=p3.line(x='x', y='y', source=fixed_cantil,line_width=2,line_color='black')
eigenmodes_beam3=p3.line(x='x', y='y', source=source3,line_width=3,line_color='#E37222')
eigenmodes_beam3cosh=p3.line(x='x', y='y', source=source3cosh,
                         line_width=1, color='#fd8d49')#orangeish
eigenmodes_beam3sinh=p3.line(x='x', y='y', source=source3sinh,
                         line_width=1,line_color='#c45508')#rust orange
eigenmodes_beam3cos=p3.line(x='x', y='y', source=source3cos,
                         line_width=1,line_color='#fe4b03')#blood orange
eigenmodes_beam3sin=p3.line(x='x', y='y', source=source3sin,
                         line_width=1,line_color='#fdaa48')#ligth orange
#eigenmodes_beam3.visible= False
legend3 = Legend(items=[
    ("Eigenvalue Problem: cosh("u"\u03BB)"u"\u00B7cos("u"\u03BB)+1=0 "u"\u279C Solution: w"u"\u1D62("u"\u03BE) = c("u"\u03BB"u"\u1D62"u"\u03BE) - C("u"\u03BB"u"\u1D62) / S("u"\u03BB"u"\u1D62) "u"\u00B7s ("u"\u03BB"u"\u1D62"u"\u03BE)", [eigenmodes_beam3]),
    ("Solution part: "u"\u00BD "u"\u00B7 cosh ("u"\u03BB"u"\u00B7"u"\u03BE)", [eigenmodes_beam3cosh]),
    ("Solution part: -"u"\u00BD  "u"\u00B7 C("u"\u03BB)/S("u"\u03BB)"u"\u00B7 sinh ("u"\u03BB"u"\u00B7"u"\u03BE)", [eigenmodes_beam3sinh]),
    ("Solution part: -"u"\u00BD "u"\u00B7 cos ("u"\u03BB"u"\u00B7"u"\u03BE)", [eigenmodes_beam3cos]),
    ("Solution part: "u"\u00BD "u"\u00B7 C("u"\u03BB)/S("u"\u03BB) "u"\u00B7 sin ("u"\u03BB"u"\u00B7"u"\u03BE)", [eigenmodes_beam3sin]),
], location=(0, 0))

p3.add_layout(legend3, 'above')
p3.legend.click_policy="hide"

#Description paragraph as label of an empy plot

p4 = figure(plot_height=200, plot_width=300,title="Definitions", tools="", x_range=(0,0), y_range=(0,0))
definitions1=p4.line(x=[0],y=[0],line_width=1,line_color='white',legend="C("u"\u03BB)="u"\u00BD [cosh("u"\u03BB) + cos("u"\u03BB)]")
definitions2=p4.line(x=[0],y=[0],line_width=1,line_color='white',legend="S("u"\u03BB)="u"\u00BD [sinh("u"\u03BB) + sin("u"\u03BB)]")
definitions3=p4.line(x=[0],y=[0],line_width=1,line_color='white',legend="c("u"\u03BB)="u"\u00BD [cosh("u"\u03BB) - cos("u"\u03BB)]")
definitions4=p4.line(x=[0],y=[0],line_width=1,line_color='white',legend="s("u"\u03BB)="u"\u00BD [sinh("u"\u03BB) - sin("u"\u03BB)]")
definitions5=p4.line(x=[0],y=[0],line_width=1,line_color='white',legend=""u"\u03BE=x/l")
definitions6=p4.line(x=[0],y=[0],line_width=1,line_color='white',legend=""u"\u03BB=l"u"\u221C("u"\u03BC "u"\u03C9"u"\u00B2/ (EI) )")

p4.axis.visible = False
p4.grid.visible = False
p4.outline_line_color = None
p4.legend.location = "bottom_left"
p4.legend.border_line_color = "white"

#Toggle not necessary
# coffeescript to link toggle with visible property
code = '''\
object.visible = Toggle.active
'''
#I created 3 callbacks with CustomJS so that when the student presses the button he sees the eigenmodes for the beam he chose.
#My only problem is that the first time one has to press the button twice in order to get the line. Then it works properly. Dont know why??
#[Matthias]: I could not reproduce the problem, works fine for me.
callback1 = CustomJS.from_coffeescript(code=code, args={})
toggle1 = Toggle(label="Simply supported beam", button_type="success",callback=callback1)
callback1.args = {'toggle': toggle1, 'object':eigenmodes_beam1 }

callback2 = CustomJS.from_coffeescript(code=code, args={})
toggle2 = Toggle(label="Beam fixed at both ends", button_type="success",callback=callback2)
callback2.args = {'toggle': toggle2, 'object':eigenmodes_beam2 }

callback3 = CustomJS.from_coffeescript(code=code, args={})
toggle3 = Toggle(label="Cantilever beam", button_type="success",callback=callback3)
callback3.args = {'toggle': toggle3, 'object':eigenmodes_beam3 }

## Create slider widget to choose eigenvalue 1-4
Eigenvalue_input = Slider(title="Eigenvalue/Eigenmode", value=1, start=1, end=ev_total, step=1)


def update_data(attrname, old, new):
    global radio_button_group
    
    beam_simple_supp(ev_num=new)
    beam_fixed_ends(ev_num=new)
    beam_cantilever(ev_num=new)
    
    
Eigenvalue_input.on_change('value',update_data)


# app description
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)

#curdoc().add_root(row(column(p1,p2,p3),column(Eigenvalue_input,p4)))
def_scroll = column(Eigenvalue_input, css_classes=['scrollable']) # also defined in index.html file
curdoc().add_root(column(description, row(column(p1,p2,p3),def_scroll)))
#curdoc().add_root(column(description, row(column(p1,p2,p3),column(Eigenvalue_input,p4))))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '

