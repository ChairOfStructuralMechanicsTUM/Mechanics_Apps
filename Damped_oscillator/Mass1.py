from bokeh.models import ColumnDataSource
from Coord1 import *
from copy import deepcopy
from abc import ABCMeta, abstractmethod

class Mass(object):
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
        # create vector of objects affected by this object
        self.affectedObjects=[]
        #create the (empty) shape
        self.shape=ColumnDataSource
    
    ## Add an object that is affected by the movement of the mass
    def linkObj(self,obj,point):
        p=Coord(point[0],point[1])
        # save the object and the point where it touches the object
        self.affectedObjects.append([obj,p])
        # tell the object that it is linked so it can also apply forces to the mass
        obj.linkTo(self,p)
    
    ## reset linking point between mass and object
    def resetLinks(self,obj,point):
        p=Coord(point[0],point[1])
        # initialise values for loop
        n=len(self.affectedObjects)
        i=0
        while (i<n):
            # check for object
            if (self.affectedObjects[i][0]==obj):
                # if so update it to the new force
                self.affectedObjects[i][1]=p
                # and exit while loop
                i=n+1
            i+=1
    
    ## Usually called by spring or dashpot to apply a force to the mass
    def applyForce(self,F,obj):
        # initialise values for loop
        n=len(self.nextStepForces)
        i=0
        while (i<n):
            # check if object has already applied a force
            if (self.nextStepObjForces[i]==obj):
                # if so update it to the new force
                self.nextStepForces[i]=F
                # and exit while loop
                i=n+1
            i+=1
        # if object was not found
        if (i==n):
            # add to lists
            self.nextStepForces.append(F)
            self.nextStepObjForces.append(obj)
    
    # function which saves the forces so evolution of other masses does not
    # affect this mass's behaviour
    def FreezeForces(self):
        # save forces
        self.thisStepForces=list(self.nextStepForces)
        # reinitialise Force monitoring vectors to collect new influences
        self.nextStepForces=[]
        self.nextStepObjForces=[]
    
    ## carry out 1 time step
    def evolve(self,dt):
        # find the total force:
        # Start with gravitational force
        F=Coord(0,-self.mass*9.81)
        for i in range(0,len(self.thisStepForces)):
            # add all forces acting on mass (e.g. spring, dashpot)
            F+=self.thisStepForces.pop()
        # Find acceleration
        a=F/self.mass
        # Use explicit Euler to find new velocity
        self.v+=dt*a
        # Use implicit Euler to find displacement vector
        displacement=dt*self.v
        # Displace mass
        self.move(displacement)
        # This affects all the affectedObjects
        for i in range(0,len(self.affectedObjects)):
            # tell object that it has been affected and must move the end at
            # point self.affectedObjects[i][1] by displacement
            self.affectedObjects[i][0].movePoint(self.affectedObjects[i][1],displacement)
            # N.B. calling this function refills nextStepForces for next timestep
            
            # change point so that it is accurate for next timestep
            self.affectedObjects[i][1]+=displacement
        return displacement
    
    # displace mass by disp
    def move(self,disp):
        temp=deepcopy(dict(self.shape.data))
        for i in range(0,len(self.shape.data['x'])):
            # move x and y co-ordinates
            temp['x'][i]+=disp.x
            temp['y'][i]+=disp.y
        # update ColumnDataSource
        self.shape.data=temp
    
    def changeMass(self,mass):
        self.mass=mass
    
    def changeInitV(self,v):
        self.v=Coord(0,v)

    @abstractmethod
    def plot(self,fig,colour,width):
        pass

    @abstractmethod
    def moveTo(self,x,y,w,h):
        pass

### Types of Masses

class RectangularMass(Mass):
    def __init__ (self, mass, x, y, w, h):
        Mass.__init__(self,mass)
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

class CircularMass(Mass):
    def __init__ (self, mass, x=0, y=0, w=0, h=0):
        Mass.__init__(self,mass)
        # create ColumnDataSource
        self.shape = ColumnDataSource(data=dict(x=[x],y=[y],w=[w],h=[h]))
    
    # add CircularMass to figure
    def plot(self,fig,colour="#0065BD",width=1):
        fig.ellipse(x='x',y='y',width='w',height='h',color=colour,source=self.shape,line_width=width)
    
    # displace mass to position (used for reset)
    def moveTo(self,point):
        temp=dict(x=[point[0]], y=[point[1]], w=[self.shape.data['w'][0]], h=[self.shape.data['h'][0]])
        # update ColumnDataSource
        self.shape.data=temp
