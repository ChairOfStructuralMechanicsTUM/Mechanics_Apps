from bokeh.models import ColumnDataSource
from Coord import *
from copy import deepcopy

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
    
    # function which saves the forces so movement of other masses does not
    # affect this mass's behaviour
    def FreezeForces(self):
        # save forces
        self.thisStepForces=list(self.nextStepForces)
    
    ## get Velocity and Acceleration at this timestep
    def getVelAcc(self):
        # find the total force:
        # Start with gravitational force
        F=Coord(0,-self.mass*9.81)
        for i in range(0,len(self.thisStepForces)):
            # add all forces acting on mass (e.g. spring, dashpot)
            F+=self.thisStepForces.pop()
        # Find acceleration
        a=F/self.mass
        return [self.v.copy(), a, self.currentPos['y'][0]]
    
    # displace mass by disp
    def move(self,disp):
        for i in range(0,len(self.currentPos['x'])):
            # move x and y co-ordinates
            self.currentPos['x'][i]+=disp.x
            self.currentPos['y'][i]+=disp.y
        # update ColumnDataSource
        self.shape.data=deepcopy(self.currentPos)
        # This affects all the affectedObjects
        for i in range(0,len(self.affectedObjects)):
            # tell object that it has been affected and must move the end at
            # point self.affectedObjects[i][1] by displacement
            self.affectedObjects[i][0].movePoint(self.affectedObjects[i][1],disp)
            # N.B. calling this function refills nextStepForces for next timestep
            
            # change point so that it is accurate for next timestep
            self.affectedObjects[i][1]+=disp
    
    def changeMass(self,mass):
        self.mass=mass
    
    def changeInitV(self,v):
        self.v=Coord(0,v)

### Types of Masses

class RectangularMass(Mass):
    def __init__ (self, mass, x, y, w, h):
        Mass.__init__(self,mass)
        # create ColumnDataSource
        self.shape = ColumnDataSource(data=dict(x=[x,x,x+w,x+w],y=[y,y+h,y+h,y]))
        self.currentPos = dict(x=[x,x,x+w,x+w],y=[y,y+h,y+h,y])
    
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

class CircularMass(Mass):
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

