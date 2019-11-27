"""
Template App - costum class template to efficiently handle objects
"""
# general imports
import numpy as np

# bokeh imports
from bokeh.models import ColumnDataSource

# internal imports
from TA_constants import xsl, ysl, xsr, ysr

# latex integration

#---------------------------------------------------------------------#


# put the intials of the app before the class name
class TA_example_class():

    # this function is called when an object of this class is built
    # you need at least "self" as an argument
    # set default assignments if your function should also be callable with less parameters
    def __init__(self, some_num, inital_string="default"):
        # define class variables here
        # all class internal variables need the self to be used in other parts of the class
        self.some_num    = some_num
        self.test_string = inital_string

        # you can also build ColumnDataSources here
        self.test_cds = ColumnDataSource(data=dict(x=[], y=[]))

    # optional - called when print(my_object) is used
    # nice to have for debugging
    def __str__(self):
        tmp_str = "Example Object:\n"
        tmp_str += "  num:     " + str(self.some_num) + "\n"
        tmp_str += "  string:  " + self.test_string + "\n"
        return tmp_str

    # for other optional Python specific class function see the Python documenation
    # like e.g. __add__ or __truediv__

    
    # use getters and setters instead of directly accessing the class variables from outside
    # this makes the code more flexible, especially for more complex constructs
    def set_string(self, new_string):
        self.test_string = new_string

    def get_string(self):
        return self.test_string
    
    # plot function using a figure handle
    def plot_line(self,fig):
        self._update_cds()
        fig.line(x='x', y='y', source=self.test_cds)


    # use an underscore _ at the beginning of the function name to indicate that
    # this function is only to be used inside the class (no private keyword in Python)
    def _update_cds(self):
        self.test_cds.data = dict(x=[0,4], y=[1,1]) # direct update
        #self.test_cds.stream(dict(x=[0,4], y=[1,1]),rollover=2) # or stream and rollover with size of the columns




# you can of course add more classes here
# depending on your structure and complexity it could make sense to have several classes
# in one file, or creating a new file for each class