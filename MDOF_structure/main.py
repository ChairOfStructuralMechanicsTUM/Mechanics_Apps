'''
###############################################################################
Imports
###############################################################################
'''
import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.io import curdoc
from Functions import *
from bokeh.models import Arrow, OpenHead, Button
from bokeh.layouts import column, row
from os.path import dirname, join, split

'''
###############################################################################
Create the plotting domain 
###############################################################################
'''
xmin, xmax = 0,10
ymin, ymax = 0,10
plot = figure(
              plot_width=800,
              plot_height=800,
              x_range=[xmin,xmax], 
              y_range=[ymin,ymax],
              tools="",
              title = '',
             )
plot.title.text_font_size = "25px"
plot.title.align = "center"
plot.grid.visible=False
plot.xaxis.visible=False
plot.yaxis.visible=False

Active = True

'''
###############################################################################
Define the objects to be plotted within the plotting domain
    (1) truss members
    (2) masses
    (3) constraints
###############################################################################
'''
############################# (1) truss members ###############################
'''
       node3 - - - - - node4
       /                  \
      /                    \
     /                      \
   node1                   node2
'''
node1 = ColumnDataSource(data=dict(x=1,y=1))
node2 = ColumnDataSource(data=dict(x=5,y=1))
node3 = ColumnDataSource(data=dict(x=2,y=3))
node4 = ColumnDataSource(data=dict(x=4,y=3))

member1 = {node1:node1 , node2:node3}
member2 = {node1:node3 , node2:node4}
member3 = {node1:node4 , node2:node2}

