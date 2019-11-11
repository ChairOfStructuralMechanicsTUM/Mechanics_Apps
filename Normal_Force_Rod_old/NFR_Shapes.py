## Shapes used in Plots

from bokeh.models import ColumnDataSource
from abc import ABCMeta, abstractmethod

import numpy as np

#from NFR_DrawAPI import NFR_DrawAPI
from NFR_constants import (
        xr_start, xr_end, y_offset, sol_reso
        )

class NFR_Shape(object):
    __metaclass__ = ABCMeta
    ## create shape
    @abstractmethod
    def __init__ (self, DrawAPI):
        # initialise value
        self.drawAPI = DrawAPI
        self.shape   = ColumnDataSource()
        
    @abstractmethod
    def draw(self, fig):
        pass
    
    

### Types of Masses

class NFR_Rod(NFR_Shape):
    def __init__(self, DrawAPI, hh=0.1): #hh = half height -> centered
        NFR_Shape.__init__(self, DrawAPI)
        self.shape.data = dict(x=[xr_start, xr_start, xr_end, xr_end], y=[y_offset-hh, y_offset+hh, y_offset+hh, y_offset-hh])
    def draw(self, fig):
        self.drawAPI.drawPatch(fig, self.shape)
                  
class NFR_RodShadow(NFR_Shape):
    def __init__(self, DrawAPI):
        NFR_Shape.__init__(self, DrawAPI)
        self.shape.data = dict(x=[xr_start,xr_end], y=[0, 0])
    def draw(self, fig):
        self.drawAPI.drawLine(fig, self.shape)

class NFR_ForceArrow(NFR_Shape):
    def __init__(self, DrawAPI, xs, xe, ys, ye):
        NFR_Shape.__init__(self, DrawAPI)
        #self.shape.data = dict(xS=[xr_start-1.0], xE=[xr_start], yS=[y_offset+0.1], yE=[y_offset+0.1])
        self.shape.data = dict(xS=[xs], xE=[xe], yS=[ys+y_offset], yE=[ye+y_offset])
    def draw(self, fig):
        self.drawAPI.drawArrow(fig, self.shape)
        
        
class NFR_ConstantLoad(NFR_Shape):
    def __init__(self, DrawAPI, load_position, lb, ub):  # lb = lower boundary, ub = upper boundary
        NFR_Shape.__init__(self, DrawAPI)
        self.shape.data = dict(x=[xr_start, xr_start, load_position, load_position], y=[y_offset+lb, y_offset+ub, y_offset+ub, y_offset+lb])
    def draw(self, fig):
        self.drawAPI.drawPatch(fig, self.shape)
        
class NFR_TriangularLoad(NFR_Shape):
    def __init__(self, DrawAPI, load_position, lb, ub):  # lb = lower boundary, ub = upper boundary
        NFR_Shape.__init__(self, DrawAPI)
        self.shape.data = dict(x=[xr_start, xr_start, load_position], y=[y_offset+lb, y_offset+ub, y_offset+lb])
    def draw(self, fig):
        self.drawAPI.drawPatch(fig, self.shape)

class NFR_TemperatureLoad(NFR_Shape):
    def __init__(self, DrawAPI, load_position, lb, ub):  # lb = lower boundary, ub = upper boundary
        NFR_Shape.__init__(self, DrawAPI)
        self.shape.data = dict(x=[xr_start, xr_start, load_position, load_position], y=[y_offset+lb, y_offset+ub, y_offset+ub, y_offset+lb])
    def draw(self, fig):
        self.drawAPI.drawPatch(fig, self.shape)


class NFR_Labels(NFR_Shape):
    def __init__(self, DrawAPI, load_position):
        NFR_Shape.__init__(self, DrawAPI)
        self.shape.data = dict(x=[xr_start-0.1+load_position, xr_start-0.05+load_position],y=[y_offset+0.3,y_offset],name=['F','|'])
    def draw(self, fig):
        self.drawAPI.drawLabels(fig, self.shape)



class NFR_GraphN(NFR_Shape):
    def __init__(self, DrawAPI):
        NFR_Shape.__init__(self, DrawAPI)
        #x_samples = np.linspace(xr_start,xr_end,sol_reso)
        #self.shape.data = dict(x=x_samples, y=x_samples)
        self.shape.data = dict(x=[], y=[])
    def draw(self, fig):
        self.drawAPI.drawGraph(fig, self.shape)


class NFR_GraphU(NFR_Shape):
    def __init__(self, DrawAPI):
        NFR_Shape.__init__(self, DrawAPI)
        #x_samples = np.linspace(xr_start,xr_end,sol_reso)
        #self.shape.data = dict(x=x_samples, y=x_samples)
        self.shape.data = dict(x=[], y=[])
    def draw(self, fig):
        self.drawAPI.drawGraph(fig, self.shape)
















