from bokeh.models import ColumnDataSource
from math import floor
from Coord import *

class Spring(object):
    ## create spring
    def __init__(self,start,end,x0,kappa=1.0,spacing = 1.0):
        start=Coord(start[0],start[1])
        end=Coord(end[0],end[1])
        # define spring constant
        self.kappa=kappa
        # define rest length (directional) and direction
        self.length = (end-start)
        self.direction = self.length/self.length.norm()
        self.length = self.direction*x0
        # define the number of coils with respect to the relaxed position of the spring
        self.nCoils=int(floor(x0/spacing))
        # Create ColumnDataSource
        self.Position = ColumnDataSource(data=dict(x=[],y=[]))
        # objects that are influenced by the spring
        self.actsOn = []
        # draw spring
        self.draw(start,end)
    
    ## add influenced object
    def linkTo(self,obj,point):
        if (point==self.start):
            self.actsOn.append((obj,'s'))
            # apply current force to object
            obj.applyForce(-self.kappa*(self.end-self.start-self.length),self)
        else:
            self.actsOn.append((obj,'e'))
            # apply current force to object
            obj.applyForce(self.kappa*(self.end-self.start-self.length),self)
    
    ## define spring co-ordinates
    def draw(self,start,end):
        self.start=start.copy()
        self.end=end.copy()
        # find direction along which spring lies
        # (not normalised)
        direction = end-start
        # find normalising constant (=length)
        length = direction.norm()
        # define (normalised) perpendicular vector for spike directions
        perpVect = Coord(direction.y/length,-direction.x/length)
        # create values to help with loop
        Pos=dict(x=[],y=[])
        Zero=Coord(0,0)
        wiggle=[Zero,perpVect,Zero,-perpVect]
        
        # add first points
        Pos['x'].append(start.x)
        Pos['y'].append(start.y)
        
        # loop over each coil
        for i in range(0,self.nCoils):
            # loop over the 4 points in the coil
            for j in range(0,4):
                # save points
                step = direction*0.05+direction*0.9*float(i+j/4.0)/self.nCoils+wiggle[j]
                Pos['x'].append(start.x+step.x)
                Pos['y'].append(start.y+step.y)
        
        # add final points
        Pos['x'].append(end.x-0.05*direction.x)
        Pos['y'].append(end.y-0.05*direction.y)
        Pos['x'].append(end.x)
        Pos['y'].append(end.y)
        
        # add calculated points to figure
        self.Position.data=Pos
        # return length (with direction for overly compressed spring)
        return direction
    
    ## draw spring on figure
    def plot(self,fig,colour="#808080",width=1):
        fig.line(x='x',y='y',color=colour,source=self.Position,line_width=width)
    
    ## place spring in space
    def compressTo(self,start,end):
        # draw spring and collect current length
        length=self.draw(start,end)
        # calculate the force exerted on/by the spring
        F = -self.kappa*(length-self.length).prod_scal(self.direction)
        # apply force to each object that the spring acts on
        for i in range(0,len(self.actsOn)):
            self.actsOn[i][0].applyForce(F*self.out(self.actsOn[i][1]),self)
        # return the force
        return F
    
    ## if a point (start) is moved then compress spring accordingly and calculate resulting force
    def movePoint(self,start,moveVect):
        if (start==self.start):
            return self.compressTo(start+moveVect,self.end)
        else:
            return self.compressTo(self.start,start+moveVect)
    
    # return outward direction
    def out(self,se):
        # -1*direction
        if (se=='s'):
            return -self.direction
        else:
            return self.direction
    
    def changeSpringConst(self,kappa):
        self.kappa=kappa
    
    def changeL0(self,x0,spacing = 1.0):
        self.length = self.direction*x0
        # define the number of coils with respect to the relaxed position of the spring
        self.nCoils=int(floor(x0/spacing))

