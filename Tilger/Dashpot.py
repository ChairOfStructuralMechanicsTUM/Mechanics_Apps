from bokeh.models import ColumnDataSource
from Coord import *
from copy import deepcopy

class Dashpot(object):
    def __init__(self,start,end,lam=1.0):
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
            self.end.y-self.direction.y/8.0-perpVect.y/2.0])
        self.Line1Start=dict(x=[self.start.x,
            self.start.x+self.direction.x/8.0],y=[self.start.y,self.start.y+self.direction.y/8.0])
        self.PistonStart=dict(x=[self.end.x-self.direction.x/2.0+perpVect.x/2.0,
            self.end.x-self.direction.x/2.0-perpVect.x/2.0], y=[self.end.y-self.direction.y/2.0+perpVect.y/2.0,
            self.end.y-self.direction.y/2.0-perpVect.y/2.0])
        self.Line2Start=dict(x=[self.end.x,
            self.end.x-self.direction.x/2.0],y=[self.end.y,self.end.y-self.direction.y/2.0])
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
            self.actsOn.append((obj,'s'))
        else:
            self.actsOn.append((obj,'e'))
    
    ## define dashpot co-ordinates
    def draw(self,start,end):
        # can't be based on previous as bokeh too slow
        casing=deepcopy(self.CasingStart)
        line1=deepcopy(self.Line1Start)
        # get displacement of casing
        displacement=start-self.origStart
        # displace outside of piston
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
        #displacement = end-self.end+start-self.start
        
        # save new points
        self.startNow=start.copy()
        self.endNow=end.copy()
        
        # return total displacement (along dashpot)
        #return displacement.prod_scal(self.direction)
    
    ## draw spring on figure
    def plot(self,fig,colour="#808080",width=1):
        fig.line(x='x',y='y',color=colour,source=self.Casing,line_width=width)
        fig.line(x='x',y='y',color=colour,source=self.Piston,line_width=width)
        fig.line(x='x',y='y',color=colour,source=self.Line1,line_width=width)
        fig.line(x='x',y='y',color=colour,source=self.Line2,line_width=width)
    
    def assertForces(self,dt):
        # collect displacement
        displacement = (self.endNow-self.end+self.startNow-self.start).prod_scal(self.direction)
        self.end=self.endNow
        self.start=self.startNow
        # calculate the force exerted on/by the spring
        F = -self.lam*displacement/dt
        # apply this force to all connected objects
        for i in range(0,len(self.actsOn)):
            self.actsOn[i][0].applyForce(F*self.out(self.actsOn[i][1]),self)
    
    ## place dashpot in space over a certain time
    def compressTo(self,start,end,dt):
        # draw dashpot and collect displacement
        self.draw(start,end)
        displacement=(self.endNow-self.end+self.startNow-self.start).prod_scal(self.direction)
        self.end=self.endNow
        self.start=self.startNow
        # calculate the force exerted on/by the spring
        F = -self.lam*displacement/dt
        # apply this force to all connected objects
        for i in range(0,len(self.actsOn)):
            self.actsOn[i][0].applyForce(F*self.out(self.actsOn[i][1]),self)
        # return the force
        return F
    
    ## if a point (start) is moved then compress dashpot accordingly and calculate resulting force
    def movePoint(self,start,moveVect):
        if (start==self.startNow):
            self.draw(start+moveVect,self.endNow)
            #return self.compressTo(start+moveVect,self.end,dt)
        else:
            self.draw(self.startNow,start+moveVect)
            #return self.compressTo(self.start,start+moveVect,dt)
    
    # return outward direction
    def out(self,se):
        if (se=='s'):
            return self.direction
        else:
            return -self.direction
    
    def changeDamperCoeff(self,lam):
        self.lam=lam

