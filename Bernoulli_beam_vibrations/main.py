# -*- coding: utf-8 -*-
"""
@author: antonis
"""

import numpy as np
from bokeh.io import curdoc  
from bokeh.layouts import row,column
from bokeh.models import ColumnDataSource,CustomJS
from bokeh.models.widgets import Slider,Toggle
from bokeh.plotting import figure
from os.path import dirname, join, split 

l=1
#beam 1-->simply supported
beam1 = ColumnDataSource(data=dict(x=[0,1], y=[0,0]))
#create the boundary conditions for simply supported beam
support_left=ColumnDataSource(data=dict(x=[0,-0.05,0.05,0.025,0.05,0.025,0,0.025,0,-0.025,0,-0.025,-0.05,-0.025,-0.05,-0.075,-0.05,0.05,0], y=[0,-0.15,-0.15,
                                        -0.2,-0.15,-0.15,-0.2,-0.15,-0.15,-0.2,-0.15,-0.15,-0.2,-0.15,-0.15,-0.2,-0.15,-0.15,0]))
support_righta=ColumnDataSource(data=dict(x=[1,0.95,1.05,1],y=[0,-0.10,-0.10,0]))
support_rightb= ColumnDataSource(data=dict(x=[0.95,1.05,1.025,1.05,1.025,1,1.025,1,0.975,1,0.975,0.95,0.975,0.95],y=[-0.15,-0.15,-0.2,-0.15,-0.15,-0.2,-0.15,-0.15,
                                           -0.2,-0.15,-0.15,-0.2,-0.15,-0.15]))

#beam 2-->fixed at both ends
beam2 = ColumnDataSource(data=dict(x=[0,1], y=[-2.5,-2.5]))
#create the boundary conditions for the beam fixed at both ends
fixed_left=ColumnDataSource(data=dict(x=[0,0,-0.03,0,0,-0.03,0,0,-0.03,0,0,-0.03,0,0,-0.03],y=[-2.25,-2.75,-2.8,-2.75,-2.625,-2.675,-2.625,-2.5,-2.55,-2.5,-2.375,
                                      -2.425,-2.375,-2.25,-2.3]))
fixed_right=ColumnDataSource(data=dict(x=[1,1,1.03,1,1,1.03,1,1,1.03,1,1,1.03,1,1,1.03],y=[-2.25,-2.75,-2.7,-2.75,-2.625,-2.575,-2.625,-2.5,-2.45,-2.5,-2.375,-2.325,
                                       -2.375,-2.25,-2.2]))

#beam 3-->cantilever beam
beam3=ColumnDataSource(data=dict(x=[0,1], y=[-5,-5]))
#create the left fixed support for the cantilever beam
fixed_cantil=ColumnDataSource(data=dict(x=[0,0,-0.03,0,0,-0.03,0,0,-0.03,0,0,-0.03,0,0,-0.03],y=[-4.75,-5.25,-5.3,-5.25,-5.125,-5.175,-5.125,-5,-5.05,-5,-4.875,
                                        -4.925,-4.875,-4.75,-4.8]))

#simply supported beam
N=200
x1 = np.linspace(0, 1, N)
y1=-np.sin(np.pi*x1/l)
source1 = ColumnDataSource(data=dict(x=x1,y=y1))

#beam fixed at both ends
N=200
x2=np.linspace(0,1,N)
y2=-2.5-(1/2*(np.cosh(4.73004*x2/l)-np.cos(4.73004*x2/l))-((1/2*(np.cosh(4.73004)-np.cos(4.73004)))/(1/2*(np.sinh(4.73004)-np.sin(4.73004))))*1/2*
         (np.sinh(4.73004*x2/l)-np.sin(4.73004*x2/l)))
source2=ColumnDataSource(data=dict(x=x2,y=y2))

#cantilever beam
N=200
x3=np.linspace(0,1,N)
y3=-5-(1/2*(np.cosh(1.8751*x3/l)-np.cos(1.8751*x3/l))-((1/2*(np.cosh(1.8751)+np.cos(1.8751)))/(1/2*(np.sinh(1.8751)+np.sin(1.8751))))*1/2*(np.sinh(1.8751*x3/l)-
            np.sin(1.8751*x3/l)))
source3=ColumnDataSource(data=dict(x=x3,y=y3))

p1 = figure(plot_height=975, plot_width=800,title="Euler Bernoulli Beam Vibrations", tools="", x_range=(-0.075,1.5), y_range=(-8,1.5))
p1.axis.visible = False
p1.grid.visible = False
p1.outline_line_color = None
p1.title.text_font_size="18pt"

beam1=p1.line(x='x', y='y', source=beam1,line_width=5,line_color='black') 
eigenmodes_beam1=p1.line(x='x', y='y', source=source1,legend="""Eigenvalue Problem: sin(\u03BB)=0 / Solution: w\u1D62(\u03BE)=sin(i\u00B7\u03C0\u00B7\u03BE)""",
                         line_width=3,line_color='pink')
eigenmodes_beam1.visible=False
support_left_beam1=p1.line(x='x', y='y', source=support_left,line_width=1,line_color='black')
support_righta_beam1=p1.line(x='x', y='y', source=support_righta,line_width=1,line_color='black')
support_rightb_beam1=p1.line(x='x', y='y', source=support_rightb,line_width=1,line_color='black')

beam2=p1.line(x='x', y='y', source=beam2,line_width=5,line_color='black') 
eigenmodes_beam2=p1.line(x='x', y='y', source=source2,legend="Eigenvalue Problem: cosh(\u03BB)\u00B7cos(\u03BB)-1=0 / Solution: w\u1D62(\u03BE) = c(\u03BB\u1D62\u03BE) - c(\u03BB\u1D62) / s(\u03BB\u1D62) \u00B7s (\u03BB\u1D62\u03BE)",
                         line_width=3,line_color='purple')
eigenmodes_beam2.visible=False
fixed_support_left=p1.line(x='x', y='y', source=fixed_left,line_width=1,line_color='black')
fixed_support_right=p1.line(x='x', y='y', source=fixed_right,line_width=1,line_color='black')

beam3=p1.line(x='x', y='y', source=beam3,line_width=5,line_color='black') 
fixed_cantilever=p1.line(x='x', y='y', source=fixed_cantil,line_width=1,line_color='black')
eigenmodes_beam3=p1.line(x='x', y='y', source=source3,legend="Eigenvalue Problem: cosh(\u03BB)\u00B7cos(\u03BB)+1=0 / Solution: w\u1D62(\u03BE) = c(\u03BB\u1D62\u03BE) - C(\u03BB\u1D62) / S(\u03BB\u1D62) \u00B7s (\u03BB\u1D62\u03BE)",line_width=3,line_color='red')
eigenmodes_beam3.visible= False

definitions1=p1.line(x=[0],y=[0],line_width=1,line_color='white',legend="C(\u03BB\u00B7\u03BE)=\u00BD (cosh(\u03BB\u00B7\u03BE) + cos(\u03BB\u00B7\u03BE))")
definitions2=p1.line(x=[0],y=[0],line_width=1,line_color='white',legend="S(\u03BB\u00B7\u03BE)=\u00BD (sinh(\u03BB\u00B7\u03BE) + sin(\u03BB\u00B7\u03BE))")
definitions3=p1.line(x=[0],y=[0],line_width=1,line_color='white',legend="c(\u03BB\u00B7\u03BE)=\u00BD (cosh(\u03BB\u00B7\u03BE) - cos(\u03BB\u00B7\u03BE))")
definitions4=p1.line(x=[0],y=[0],line_width=1,line_color='white',legend="s(\u03BB\u00B7\u03BE)=\u00BD (sinh(\u03BB\u00B7\u03BE) - sin(\u03BB\u00B7\u03BE))")

p1.legend.label_text_font_size="10pt"
p1.legend.border_line_width = 3
p1.legend.border_line_color = "navy"
p1.legend.border_line_alpha = 0.5
p1.legend.location = "bottom_left"

# coffeescript to link toggle with visible property
code = '''\
object.visible = toggle.active
'''
#I created 3 callbacks with CustomJS so that when the student presses the button he sees the eigenmodes for the beam he chose.
#My only problem is that the first time one has to press the button twice in order to get the line. Then it works properly. Dont know why??
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
Eigenvalue_input = Slider(title="Eigenvalue/Eigenmode", value=1, start=1, end=4, step=1)

def update_data(attrname, old, new):
    global radio_button_group
    eigen_num=Eigenvalue_input.value
    #simply supported beam
    x1 = np.linspace(0, 1, N)
    y1=-np.sin(eigen_num*np.pi*x1/l)
    source1.data = dict(x=x1, y=y1)
    #beam fixed at both ends
    x2=np.linspace(0,1,N)
    if new==1:
        y2=-2.5-(1/2*(np.cosh(4.73004*x2/l)-np.cos(4.73004*x2/l))-((1/2*(np.cosh(4.73004)-np.cos(4.73004)))/(1/2*(np.sinh(4.73004)-np.sin(4.73004))))*1/2*(np.sinh(4.73004*x2/l)-np.sin(4.73004*x2/l)))
        source2.data=dict(x=x2,y=y2)
    elif new==2:
        y2=-2.5-(1/2*(np.cosh(7.853*x2/l)-np.cos(7.853*x2/l))-((1/2*(np.cosh(7.853)-np.cos(7.853)))/(1/2*(np.sinh(7.853)-np.sin(7.853))))*1/2*(np.sinh(7.853*x2/l)-np.sin(7.853*x2/l)))
        source2.data=dict(x=x2,y=y2)
    elif new==3:
        y2=-2.5-(1/2*(np.cosh(10.99561*x2/l)-np.cos(10.99561*x2/l))-((1/2*(np.cosh(10.99561)-np.cos(10.99561)))/(1/2*(np.sinh(10.99561)-np.sin(10.99561))))*1/2*(np.sinh(10.99561*x2/l)-np.sin(10.99561*x2/l)))
        source2.data=dict(x=x2,y=y2)
    elif new==4:
        y2=-2.5-(1/2*(np.cosh(14.137*x2/l)-np.cos(14.137*x2/l))-((1/2*(np.cosh(14.137)-np.cos(14.137)))/(1/2*(np.sinh(14.137)-np.sin(14.137))))*1/2*(np.sinh(14.137*x2/l)-np.sin(14.137*x2/l)))
        source2.data=dict(x=x2,y=y2) 
    #cantilever beam
    x3=np.linspace(0,1,N)
    if new==1:
        y3=-5-(1/2*(np.cosh(1.8751*x3/l)-np.cos(1.8751*x3/l))-((1/2*(np.cosh(1.8751)+np.cos(1.8751)))/(1/2*(np.sinh(1.8751)+np.sin(1.8751))))*1/2*(np.sinh(1.8751*x3/l)-np.sin(1.8751*x3/l)))
        source3.data=dict(x=x3,y=y3)
    elif new==2:
        y3=-5-(1/2*(np.cosh(4.69409*x3/l)-np.cos(4.69409*x3/l))-((1/2*(np.cosh(4.69409)+np.cos(4.69409)))/(1/2*(np.sinh(4.69409)+np.sin(4.69409))))*1/2*(np.sinh(4.69409*x3/l)-np.sin(4.69409*x3/l)))
        source3.data=dict(x=x3,y=y3)
    elif new==3:
        y3=-5-(1/2*(np.cosh(7.85476*x3/l)-np.cos(7.85476*x3/l))-((1/2*(np.cosh(7.85476)+np.cos(7.85476)))/(1/2*(np.sinh(7.85476)+np.sin(7.85476))))*1/2*(np.sinh(7.85476*x3/l)-np.sin(7.85476*x3/l)))
        source3.data=dict(x=x3,y=y3)
    elif new==4:
        y3=-5-(1/2*(np.cosh(10.99554*x3/l)-np.cos(10.99554*x3/l))-((1/2*(np.cosh(10.99554)+np.cos(10.99554)))/(1/2*(np.sinh(10.99554)+np.sin(10.99554))))*1/2*(np.sinh(10.99554*x3/l)-np.sin(10.99554*x3/l)))
        source3.data=dict(x=x3,y=y3)
    
Eigenvalue_input.on_change('value',update_data)

curdoc().add_root(row(column(p1),column(toggle1,toggle2,toggle3,Eigenvalue_input)))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '

