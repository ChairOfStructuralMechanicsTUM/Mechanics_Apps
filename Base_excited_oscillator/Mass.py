from bokeh.models import ColumnDataSource
from Coord import *
from copy import deepcopy
from Dashpot import *

class Mass(object):
    ## create mass
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
        self.currentPos=dict()
        self.shape=ColumnDataSource
        self.old = Coord(0,0)
    
    ## Add an object that is affected by the movement of the mass
    def linkObj(self,obj,point):
        p=Coord(point[0],point[1])
        # save the object and the current point where it is in contact with the mass
        self.affectedObjects.append([obj,p])
        # inform the object that it is linked to the mass, in order for it to apply forces on the mass
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
            # check if object has already applied a force in previous steps
            if (self.nextStepObjForces[i]==obj):
                # if so update it with the new force
                if(isinstance(obj, Dashpot)):
                    self.nextStepForces[i]=(F + self.old)
                    self.old = F
                else:
                    self.nextStepForces[i]=F
                # and exit while loop
                i=n+1
            i+=1
        # if object was not found
        if (i==n):
            # add to lists
            self.nextStepForces.append(F)
            self.nextStepObjForces.append(obj)
            
    
    # function which saves the forces so movement of other masses does not
    # affect this mass's behaviour
    def FreezeForces(self):
        # save forces
        self.thisStepForces=list(self.nextStepForces)
    
    ## get Velocity and Acceleration at current timestep
    def EvolveMass(self,dt):
        # find the total force:
        # gravitational force should not be included (displacement referring to the static- equilibrium position)
        F=Coord(0,-self.mass*9.81)
        for i in range(0,len(self.thisStepForces)):
            # add all forces acting on mass (e.g. spring, dashpot)
            F+=self.thisStepForces.pop()   # returns the last entry, adds it to the force, and eliminates it from the list 
        # Find acceleration
        ax=F.x/self.mass
        ay=F.y/self.mass
        a=Coord(ax,ay)

        #temp[0]*dt+0.5*dt*dt*temp[1]

        # Use explicit Euler to find new velocity
        self.v+=dt*a
        # Use implicit Euler to find displacement vector
        displacement=dt*self.v
        # Displace mass
        self.move(displacement)
        return displacement
    
    # displace mass by disp
    def move(self,disp):
        for i in range(0,len(self.currentPos['x'])):
            # move x and y co-ordinates
            self.currentPos['x'][i]+=disp.x # zero x disp
            self.currentPos['y'][i]+=disp.y # update mass vertices
        # update ColumnDataSource
        self.shape.data=deepcopy(self.currentPos)
        
        # This affects all affectedObjects
        for i in range(0,len(self.affectedObjects)):
            # an end of an object affected by mass displacement connected to the mass
            # must be displaced by that displacement
            # Note: calling this function finds nextStepForces for next timestep
            self.affectedObjects[i][0].movePoint(self.affectedObjects[i][1],disp)   # movePoint(Spring or Dashpot current End in contact with mass,moveVect)
            
            # update object's end in contact with the mass
            self.affectedObjects[i][1]+=disp
    
    def changeMass(self,mass):
        self.mass=mass
    
    def changeInitV(self,v):
        self.v=Coord(0,v)

### Types of Masses

class RectangularMass(Mass):    # Subclass inheriting attributes and methods of Mass class
    def __init__ (self, mass, x, y, w, h):
        Mass.__init__(self,mass)
        # create ColumnDataSource
        self.shape = ColumnDataSource(data=dict(x=[x,x,x+w,x+w],y=[y,y+h,y+h,y]))
        self.currentPos = dict(x=[x,x,x+w,x+w],y=[y,y+h,y+h,y]) # Rectangular Mass vertices CCW
    
    # add RectangularMass to figure
    def plot(self,fig,colour="#0065BD",width=1):
        fig.patch(x='x',y='y',color=colour,source=self.shape,line_width=width)
    
    # displace mass to position (used for reset)
    def moveTo(self,x,y,w,h):
        self.currentPos=dict(x=[x,x,x+w,x+w],y=[y,y+h,y+h,y])
        # update ColumnDataSource
        self.shape.data=deepcopy(self.currentPos)
    
    def getTop(self):
        return self.currentPos['y'][1]

class CircularMass(Mass):       # Subclass inheriting attributes and methods of Mass class
    def __init__ (self, mass, x, y, w, h):
        Mass.__init__(self,mass)
        # create ColumnDataSource
        self.shape = ColumnDataSource(data=dict(x=[x],y=[y],w=[w],h=[h]))
        self.currentPos = dict(x=[x],y=[y],w=[w],h=[h])
    
    # add CircularMass to figure
    def plot(self,fig,colour="#0065BD",width=1):
        fig.ellipse(x='x',y='y',width='w',height='h',color=colour,source=self.shape,line_width=width)
    
    # displace mass to position (used for reset)
    def moveTo(self,point):
        self.currentPos=dict(x=[point[0]], y=[point[1]], w=[self.shape.data['w'][0]], h=[self.shape.data['h'][0]])
        # update ColumnDataSource
        self.shape.data=self.currentPos

