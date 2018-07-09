# -*- coding: utf-8 -*-
"""
@author: antonis, matthias (re-structured to function design)
"""
from __future__ import division
import numpy as np

from scipy.optimize import brentq # fast numerical solver for roots
from bokeh.io import curdoc
from bokeh.layouts import column, Spacer
from bokeh.models import ColumnDataSource
from bokeh.models.glyphs import ImageURL
from bokeh.models.widgets import Slider
from bokeh.plotting import figure
from os.path import dirname, join, split, abspath

# for LaTeX support
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv, LatexLegend

# beam length
l=1

# first ev eigenvalues for each beam
ev_total = 6

#beam 1-->simply supported
beam1 = ColumnDataSource(data=dict(x=[0,1], y=[0,0]))

#beam 2-->fixed at both ends
beam2 = ColumnDataSource(data=dict(x=[0,1], y=[0,0]))

#beam 3-->cantilever beam
beam3=ColumnDataSource(data=dict(x=[0,1], y=[0,0]))

# load support symbols
support1 = "Bernoulli_beam_vibrations/static/images/auflager01.svg"
support2 = "Bernoulli_beam_vibrations/static/images/auflager02.svg"
support3 = "Bernoulli_beam_vibrations/static/images/auflager03.svg"
support4 = "Bernoulli_beam_vibrations/static/images/auflager04.svg"
support_src = ColumnDataSource(dict(sp1=[support1], sp2=[support2], sp3=[support3], sp4=[support4]))

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
    # y2=-(1/2*(np.cosh(ev*x2/l)-np.cos(ev*x2/l))-((1/2*(np.cosh(ev)-np.cos(ev)))/(1/2*(np.sinh(ev)-np.sin(ev))))*1/2*(np.sinh(ev*x2/l)-np.sin(ev*x2/l)))
    y2cosh=-(1/2*(np.cosh(ev*x2/l)))
    y2sinh=((1/2*(np.cosh(ev)-np.cos(ev)))/(1/2*(np.sinh(ev)-np.sin(ev))))*1/2*(np.sinh(ev*x2/l))
    y2cos=(1/2*(np.cos(ev*x2/l)))
    y2sin=-((1/2*(np.cosh(ev)-np.cos(ev)))/(1/2*(np.sinh(ev)-np.sin(ev))))*1/2*(np.sin(ev*x2/l))
    y2 = y2cos+y2cosh+y2sin+y2sinh
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
    # y3=-(1/2*(np.cosh(ev*x3/l)-np.cos(ev*x3/l))-((1/2*(np.cosh(ev)+np.cos(ev)))/(1/2*(np.sinh(ev)+np.sin(ev))))*1/2*(np.sinh(ev*x3/l)-
    #             np.sin(ev*x3/l)))
    y3cosh=-(1/2*(np.cosh(ev*x3/l)))
    y3sinh=+((1/2*(np.cosh(ev)+np.cos(ev)))/(1/2*(np.sinh(ev)+np.sin(ev))))*1/2*(np.sinh(ev*x3/l))
    y3cos=+(1/2*(np.cos(ev*x3/l)))
    y3sin=-((1/2*(np.cosh(ev)+np.cos(ev)))/(1/2*(np.sinh(ev)+np.sin(ev))))*1/2*(np.sin(ev*x3/l))
    y3 = y3cos+y3cosh+y3sin+y3sinh
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
p1.outline_line_width = 2
p1.outline_line_color = "black"
p1.title.text_font_size="13pt"

beam1=p1.line(x='x', y='y', source=beam1,line_width=5,line_color='black') 
eigenmodes_beam1=p1.line(x='x', y='y', source=source1,
                         line_width=3,line_color='#3070b3') # TUM color pantone 300
eigenmodes_beam1.visible=True
p1.add_glyph(support_src,ImageURL(url="sp2", x=0.0, y=0.35, w=2, h=2, anchor="top_center"))
p1.add_glyph(support_src,ImageURL(url="sp1", x=1.0, y=0.35, w=1.8, h=1.8, anchor="top_center"))
    
legend1 = LatexLegend(items=[
    ("\\text{Eigenvalue Problem: } \\sin(\\lambda) = 0 \\rightarrow \\text{Solution: } w_i(\\xi) = \\sin(i \\cdot \\pi \\xi)"   , [eigenmodes_beam1]),
], location=(0, 5), label_height=27, border_line_width=2, border_line_color="black", max_label_width=865)

p1.add_layout(legend1, 'above')
p1.legend.click_policy="hide"
p1.toolbar.logo = None

#Plot 2
p2 = figure(plot_height=500, plot_width=900,title="Beam fixed at both ends", tools="", x_range=(-0.075,1.075), y_range=(-3,3))
p2.axis.visible = False
p2.outline_line_width = 2
p2.outline_line_color = "black"
p2.title.text_font_size="13pt"

beam2=p2.line(x='x', y='y', source=beam2,line_width=5,line_color='black') 
eigenmodes_beam2=p2.line(x='x', y='y', source=source2,
                         line_width=3,line_color='#3070b3') # TUM color pantone 300
eigenmodes_beam2cosh=p2.line(x='x', y='y', source=source2cosh,
                         line_width=1, color='#005293') # TUM color pantone 301
eigenmodes_beam2sinh=p2.line(x='x', y='y', source=source2sinh,
                         line_width=1,line_color='#003359') # TUM color pantone 540
eigenmodes_beam2cos=p2.line(x='x', y='y', source=source2cos,
                         line_width=1,line_color='#64A0C8') # TUM color pantone 542 
eigenmodes_beam2sin=p2.line(x='x', y='y', source=source2sin,
                         line_width=1,line_color='#98C6EA') # TUM color pantone 283
p2.add_glyph(support_src,ImageURL(url="sp3", x=-0.0105, y=0.0, w=2, h=2, anchor="center"))
p2.add_glyph(support_src,ImageURL(url="sp4", x=1.0105, y=0.0, w=2, h=2, anchor="center"))

legend2 = LatexLegend(items=[
    ("\\text{Eigenvalue Problem: } \cosh(\\lambda) \cdot \cos(\\lambda) -1 = 0 \\rightarrow \\text{Solution: } w_i(\\xi) = c(\\lambda_i \\xi) - \\frac{c(\\lambda_i)}{s(\\lambda_i)} \\cdot s(\\lambda_i \\xi)", [eigenmodes_beam2]),
    ("\\text{Solution part: } - \\frac{1}{2} \\cosh(\\lambda \\cdot \\xi)", [eigenmodes_beam2cosh]),
    ("\\text{Solution part: } \\frac{1}{2} \\frac{c(\\lambda)}{s(\\lambda)} \\cdot \\sinh(\\lambda \\xi)", [eigenmodes_beam2sinh]),
    ("\\text{Solution part: } \\frac{1}{2} \\cos(\\lambda \\cdot \\xi)", [eigenmodes_beam2cos]),
    ("\\text{Solution part: } - \\frac{1}{2} \\frac{c(\\lambda)}{s(\\lambda)} \\cdot \\sin(\\lambda \\xi)", [eigenmodes_beam2sin]),
], location=(0, 5), label_height=27, border_line_width=2, border_line_color="black", max_label_width=865)

p2.add_layout(legend2, 'above')
p2.legend.click_policy="hide"
p2.toolbar.logo = None


#Plot 3
p3 = figure(plot_height=500, plot_width=900,title="Cantilever beam", tools="", x_range=(-0.075,1.075), y_range=(-3,3))
p3.axis.visible = False
#p3.grid.visible = False
p3.outline_line_width = 2
p3.outline_line_color = "black"
p3.title.text_font_size="13pt"

beam3=p3.line(x='x', y='y', source=beam3,line_width=5,line_color='black') 
p3.add_glyph(support_src,ImageURL(url="sp3", x=-0.0105, y=0.0, w=2, h=2, anchor="center"))
eigenmodes_beam3=p3.line(x='x', y='y', source=source3,
                         line_width=3,line_color='#3070b3') # TUM color pantone 300
eigenmodes_beam3cosh=p3.line(x='x', y='y', source=source3cosh,
                         line_width=1, color='#005293') # TUM color pantone 301
eigenmodes_beam3sinh=p3.line(x='x', y='y', source=source3sinh,
                         line_width=1,line_color='#003359') # TUM color pantone 540
eigenmodes_beam3cos=p3.line(x='x', y='y', source=source3cos,
                         line_width=1,line_color='#64A0C8') # TUM color pantone 542 
eigenmodes_beam3sin=p3.line(x='x', y='y', source=source3sin,
                         line_width=1,line_color='#98C6EA') # TUM color pantone 283

legend3 = LatexLegend(items=[
    ("\\text{Eigenvalue Problem: } \cosh(\\lambda) \cdot \cos(\\lambda) +1 = 0 \\rightarrow \\text{Solution: } w_i(\\xi) = c(\\lambda_i \\xi) - \\frac{C(\\lambda_i)}{S(\\lambda_i)} \\cdot s(\\lambda_i \\xi)", [eigenmodes_beam3]),
    ("\\text{Solution part: } - \\frac{1}{2} \\cosh(\\lambda \\cdot \\xi)", [eigenmodes_beam3cosh]),
    ("\\text{Solution part: } \\frac{1}{2} \\frac{C(\\lambda)}{S(\\lambda)} \\cdot \\sinh(\\lambda \\xi)", [eigenmodes_beam3sinh]),
    ("\\text{Solution part: } \\frac{1}{2} \\cos(\\lambda \\cdot \\xi)", [eigenmodes_beam3cos]),
    ("\\text{Solution part: } - \\frac{1}{2} \\frac{C(\\lambda)}{S(\\lambda)} \\cdot \\sin(\\lambda \\xi)", [eigenmodes_beam3sin]),
], location=(0, 5), label_height=27, border_line_width=2, border_line_color="black", max_label_width=865)

p3.add_layout(legend3, 'above')
p3.legend.click_policy="hide"
p3.toolbar.logo = None

## Create slider widgets to choose eigenvalue from 1 to ev_total
ev_input1 = Slider(title="Eigenvalue/Eigenmode", value=1, start=1, end=ev_total, step=1, width=862)
ev_input2 = Slider(title="Eigenvalue/Eigenmode", value=1, start=1, end=ev_total, step=1, width=862)
ev_input3 = Slider(title="Eigenvalue/Eigenmode", value=1, start=1, end=ev_total, step=1, width=862)

# functions to update plots when using the specific sliders
def update_simple_beam(attrname, old, new):
    beam_simple_supp(ev_num=new)

def update_fixed_beam(attrname, old, new):
    beam_fixed_ends(ev_num=new)

def update_cantilever_beam(attrname, old, new):
    beam_cantilever(ev_num=new)
    
ev_input1.on_change('value',update_simple_beam)
ev_input2.on_change('value',update_fixed_beam)
ev_input3.on_change('value',update_cantilever_beam)


# app description
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)

curdoc().add_root(column(description, Spacer(height=50), \
                  p1,ev_input1, Spacer(height=100), \
                  p2,ev_input2, Spacer(height=100), \
                  p3,ev_input3))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '

