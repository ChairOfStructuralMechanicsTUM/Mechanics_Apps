"""
Dummy App - shows some common concepts used in this project
class concerning ball animations

"""
# general imports
import numpy as np
from math import sin, cos, pi, radians

# bokeh imports
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.models import ColumnDataSource, Slider

# internal imports

# latex integration


#---------------------------------------------------------------------#


# implementation withouth CDS

# TODO: add implementation with CDS

class DY_ball(object):
    # initialize
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.c = (0,0,0) # black   RGB color
        self.d = 1       # direction 1 = right, -1 = left
        self.cds = ColumnDataSource(data = dict(x=[self.x], y=[self.y], c=[self.c]))

    # print class information
    def __str__(self):
        print_string = ""
        print_string + "x = " + str(self.x) + "\n"
        print_string + "y = " + str(self.y) + "\n"
        print_string + "RGB color: " + str(self.c) + "\n"
        print_string + "direction: " + str(self.d) + "\n"
        return print_string

    # set the coordinates
    def set_coords(self,x,y):
        self.x = x
        self.y = y
    
    # set the color
    def set_color(self,c):
        self.c = c

    # get the coordinates
    def get_coords(self):
        return [self.x, self.y]

    # add displacement in x-direction
    def add_disp(self,displ):
        self.x += (displ*self.d)

    def change_direction(self):
        if self.d == 1:    # if right
            self.d = -1    # change to left
        elif self.d == -1: # if left
            self.d = 1     # change to right
        else:
            print("Invalid direction!") 

    def update_cds(self):
        self.cds.data = dict(x=[self.x], y=[self.y], c=[self.c])

    # plot the current configuration
    def plot(self, fig):
        #fig.circle(x=self.x, y=self.y, color=self.c, size=30)
        self.update_cds()
        fig.circle(x='x', y='y', source=self.cds, size=30)