"""
Dummy App - shows some common concepts used in this project
class concerning ball animations

"""
# general imports

# bokeh imports
from bokeh.models import ColumnDataSource
from bokeh.colors import RGB

# internal imports

# latex integration


#---------------------------------------------------------------------#


class DY_ball(object):
    # initialize
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.c = (0,0,0) # black   RGB color
        self.d = 1       # direction 1 = right, -1 = left
        self.cds = ColumnDataSource(data = dict(x=[self.x], y=[self.y], color=[RGB(*self.c)]))  # ColumnDataSource to update plot

    # print class information
    def __str__(self):
        print_string = ""
        print_string += "x = " + str(self.x) + "\n"
        print_string += "y = " + str(self.y) + "\n"
        print_string += "RGB color: " + str(self.c) + "\n"
        print_string += "direction: " + str(self.d) + "\n"
        return print_string

    # set the coordinates
    def set_coords(self,x,y):
        self.x = x
        self.y = y
        self.update_cds()
    
    # set the color
    def set_color(self,c):
        self.c = c
        self.update_cds()

    # get the coordinates
    def get_coords(self):
        return [self.x, self.y]

    # add displacement in x-direction
    def add_disp(self,displ):
        self.x += (displ*self.d)
        self.update_cds()

    def change_direction(self):
        if self.d == 1:    # if right
            self.d = -1    # change to left
        elif self.d == -1: # if left
            self.d = 1     # change to right
        else:
            print("Invalid direction!") 

    def update_cds(self):
        self.cds.data = dict(x=[self.x], y=[self.y], color=[RGB(*self.c)])  # the * unpacks the tuple self.c, the function RGB takes three inputs
        #self.cds.stream( dict(x=[self.x], y=[self.y], c=[self.c]), rollover=5 ) # use this for "speed effect"

    # plot the current configuration
    def plot(self, fig):
        #fig.circle(x=self.x, y=self.y, color=self.c, size=30) # plotting it this way would not remove the old ball from the plot
        #self.update_cds()
        fig.circle(x='x', y='y', color='color', source=self.cds, size=30) #changing the color does not work using ColumnDataSource