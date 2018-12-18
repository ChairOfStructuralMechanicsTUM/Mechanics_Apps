from bokeh.models import ColumnDataSource
from Coord import *
from abc import ABCMeta, abstractmethod

class DiscreteMass(object):
    __metaclass__ = ABCMeta
    ## create mass
    @abstractmethod
    def __init__ (self, mass):
        # initialise value
        self.mass=mass
        # create vector of external forces (besides gravity) acting on the mass
        self.nextStepForces=[]
        self.nextStepObjForces=[]
        # initialise velocity
        self.v=Coord(0,0)
        #create the (empty) shape
        self.shape=ColumnDataSource
    
    def changeMass(self,mass):
        self.mass=mass

    @property
    def getMass(self):
        return self.mass

    @abstractmethod
    def plot(self,fig,colour,width):
        pass

    @abstractmethod
    def moveTo(self,x,y,w,h):
        pass

### Types of Masses

class RectangularMass(DiscreteMass):
    def __init__ (self, mass, x, y, w, h):
        DiscreteMass.__init__(self,mass)
        # create ColumnDataSource
        self.shape = ColumnDataSource(data=dict(x=[x,x,x+w,x+w],y=[y,y+h,y+h,y]))
    
    # add RectangularMass to figure
    def plot(self,fig,colour="#0065BD",width=1):
        fig.patch(x='x',y='y',color=colour,source=self.shape,line_width=width)
    
    # displace mass to position (used for reset)
    def moveTo(self,x,y,w,h):
        temp=dict(x=[x,x,x+w,x+w],y=[y,y+h,y+h,y])
        # update ColumnDataSource
        self.shape.data=temp

class CircularMass(DiscreteMass):
    def __init__ (self, mass, x=0, y=0, w=0, h=0):
        DiscreteMass.__init__(self,mass)
        # create ColumnDataSource
        self.shape = ColumnDataSource(data=dict(x=[x],y=[y],w=[w],h=[h]))
    
    # add CircularMass to figure
    def plot(self,fig,colour="#3070b3",width=1):
        fig.ellipse(x='x',y='y',width='w',height='h',color=colour,source=self.shape,line_width=width)
    
    # displace mass to position (used for reset)
    def moveTo(self,point):
        temp=dict(x=[point[0]], y=[point[1]], w=[self.shape.data['w'][0]], h=[self.shape.data['h'][0]])
        # update ColumnDataSource
        self.shape.data=temp
    def Getmass(self):
        return self.mass