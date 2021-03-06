from bokeh.models import ColumnDataSource
from beo_coord import Coord
from copy import deepcopy

class Dashpot(object):
    def __init__(self,start,end,lam):
        # define dashpot constant
        self.lam=lam
        # save points
        self.start=Coord(start[0],start[1])
        self.end=Coord(end[0],end[1])
        self.origStart=self.start
        self.origEnd=self.end
        self.startNow=self.start
        self.endNow=self.end
        
        # find direction along which dashpot lies
        # (not normalised)
        self.direction = self.end-self.start
        
        # define (normalised) perpendicular vector for spike directions
        perpVect = self.direction.perp()
        
        # define initial positions of dashpot coordinates
        self.CasingStart=dict(x=[self.end.x-self.direction.x/8.0+perpVect.x/2.0,
            self.start.x+self.direction.x/8.0+perpVect.x/2.0,self.start.x+self.direction.x/8.0-perpVect.x/2.0,
            self.end.x-self.direction.x/8.0-perpVect.x/2.0],y=[self.end.y-self.direction.y/8.0+perpVect.y/2.0,
            self.start.y+self.direction.y/8.0+perpVect.y/2.0,self.start.y+self.direction.y/8.0-perpVect.y/2.0,
            self.end.y-self.direction.y/8.0-perpVect.y/2.0])    # damper casing (4 points CCW)
        self.Line1Start=dict(x=[self.start.x,
            self.start.x+self.direction.x/8.0],y=[self.start.y,self.start.y+self.direction.y/8.0])  # top vertical line
        self.PistonStart=dict(x=[self.end.x-self.direction.x/2.0+perpVect.x/2.0,
            self.end.x-self.direction.x/2.0-perpVect.x/2.0], y=[self.end.y-self.direction.y/2.0+perpVect.y/2.0,
            self.end.y-self.direction.y/2.0-perpVect.y/2.0])    # plunger
        self.Line2Start=dict(x=[self.end.x,
            self.end.x-self.direction.x/2.0],y=[self.end.y,self.end.y-self.direction.y/2.0])    # bottom vertical line
        
        # Create ColumnDataSources with initial positions
        self.Casing = ColumnDataSource(data=self.CasingStart)
        self.Line1 = ColumnDataSource(data=self.Line1Start)
        self.Piston = ColumnDataSource(data=self.PistonStart)
        self.Line2 = ColumnDataSource(data=self.Line2Start)
        # once positions have been calculated direction is normalised
        self.direction=self.direction.direction()
        # objects that are influenced by the dashpot
        self.actsOn = []
        
    ## add influenced object
    def linkTo(self,obj,point):
        if (point==self.start):
            self.actsOn.append([obj,'s'])
        else:
            self.actsOn.append([obj,'e'])
    
    ## define dashpot co-ordinates
    def draw(self,start,end):
        # can't be based on previous as bokeh too slow
        casing=deepcopy(self.CasingStart)
        line1=deepcopy(self.Line1Start)
        # get displacement of casing w.r.t initial position
        displacement=start-self.origStart
        # displace casing and top vertical line points coordinates
        for i in range(0,4):
            casing['x'][i]+=displacement.x
            casing['y'][i]+=displacement.y
        for i in range(0,2):
            line1['x'][i]+=displacement.x
            line1['y'][i]+=displacement.y
        
        piston=deepcopy(self.PistonStart)
        line2=deepcopy(self.Line2Start)
        # get displacement of plunger
        displacement=end-self.origEnd
        # displace plunger
        for i in range(0,2):
            piston['x'][i]+=displacement.x
            piston['y'][i]+=displacement.y
            line2['x'][i]+=displacement.x
            line2['y'][i]+=displacement.y
        
        # add calculated points to figure
        self.Casing.data=casing
        self.Line1.data=line1
        self.Piston.data=piston
        self.Line2.data=line2
        
        # calculate change in length
        displacement = (end-start)-(self.end-self.start)
        # save new points
        self.start=start.copy()
        self.end=end.copy()
        
        # return total displacement (along dashpot)
        return displacement.prod_scal(self.direction)
        
    ## draw dashpot on figure
    def plot(self,fig,colour="#8a8a8a",width=1):
        fig.line(x='x',y='y',color=colour,source=self.Casing,line_width=width)
        fig.line(x='x',y='y',color=colour,source=self.Piston,line_width=width)
        fig.line(x='x',y='y',color=colour,source=self.Line1,line_width=width)
        fig.line(x='x',y='y',color=colour,source=self.Line2,line_width=width)
    
    ## place dashpot in space over a certain time
    def compressTo(self,start,end,type):
        dt=0.0075
        # draw dashpot and collect displacement
        displacement=self.draw(start,end)
        # calculate the force exerted on/by the dashpot
        if (type==0): # if dashpot is compressed in order to reach static equilibrium
            Fd = 0 # no damping force
        else:
            Fd = -self.lam*(displacement/dt)
            # apply this force to all connected objects
        for i in range(0,len(self.actsOn)):
            self.actsOn[i][0].applyForce(Fd*self.out(self.actsOn[i][1]),self)
        # return the force
        return Fd
    
    ## if a point (start) is moved then compress dashpot accordingly and calculate resulting force
    def movePoint(self,DashpotEnd,moveVect):
        if (DashpotEnd==self.start):
            #self.draw(start+moveVect,self.endNow)
            return self.compressTo(DashpotEnd+moveVect,self.end,1)
        else:
            #self.draw(self.startNow,end+moveVect)
            return self.compressTo(self.start,DashpotEnd+moveVect,1)
    
    # return outward direction
    def out(self,se):
        if (se=='s'):
            return -self.direction
        else:
            return self.direction
    
    def changeDamperCoeff(self,lam):
        self.lam=lam

