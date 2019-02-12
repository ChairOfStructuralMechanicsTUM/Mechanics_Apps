# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 16:24:44 2019

@author: Boulbrachene
"""

from bokeh.models import Button, ColumnDataSource
from bokeh.layouts import layout
from bokeh.plotting import curdoc, figure
from bokeh.models.widgets import TextInput
from bokeh.layouts import widgetbox,column,row

fig = figure(
    title='Third figure',
    width=400,
    height=400,
    x_range=[-5, 10], 
    y_range=(0, 5),
    tools='pan, wheel_zoom, zoom_in, zoom_out, box_select, lasso_select, tap, reset',
    x_axis_label='x axis',
    y_axis_label='y axis',
)

x = [1, 2, 3, 4]
y = [4, 3, 2, 1]

source = ColumnDataSource(data=dict(x=x, y=y))

fig.circle(
    x='x',
    y='y',
    source=source,
    radius=0.5,              
    fill_alpha=0.6,          
    fill_color='green',
    line_color='black',
)

def add_button():
    print("adding figure")
    layout1.children.insert(1,Amp_input)
    layout1.children.insert(2,fig)

def remove_button():
    print("removing figure")
    layout1.children[2].children[0]= button2

Amp_input = TextInput(title="Input Amplitude:")
button = Button(label="Click to add the figure", button_type="success")
button.on_click(add_button)

controls = [Amp_input,button]
controls_box = widgetbox(controls, sizing_mode='scale_width')  # all controls
print(controls_box.children[0])
#print(len(controls_box))

button_rmv = Button(label="Click to remove the figure", button_type="success")
button1 = Button(label="Button 1", button_type="success")
button2 = Button(label="Button 2", button_type="success")
button_rmv.on_click(remove_button)

#layout1 = layout([[button,button_rmv], [[button],[button_rmv]]],sizing_mode='stretch_both')


layout1 = column(button,button_rmv, controls_box)

#print(layout.children[0])
#print(len(layout1.children))
curdoc().add_root(layout1)