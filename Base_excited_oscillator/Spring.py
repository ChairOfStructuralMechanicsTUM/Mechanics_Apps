from bokeh.models import ColumnDataSource
from math import floor
from Coord import *

class Spring(object):
    ## create spring
    def __init__(self,start,end,x0,kappa,spacing=1.0):
        InitialStart=Coord(start[0],start[1])
        InitialEnd=Coord(end[0],end[1])
        # define spring constant
        self.kappa=kappa
        # define rest directional length (length) and direction (Norm_Initial_Length)
        self.length = (InitialEnd-InitialStart)   # initial spring vector
        self.Norm_Initial_Length = self.length/self.length.norm()   # normalizd initial spring vector
        self.length = self.Norm_Initial_Length*x0
        # define the number of coils with respect to the relaxed position of the spring
        self.nCoils=int(floor(x0/spacing))
        # Create ColumnDataSource
        self.Position = ColumnDataSource(data=dict(x=[],y=[]))
        # objects that are influenced by the spring
        self.actsOn = []
        # draw spring
        self.draw(InitialStart,InitialEnd)
    
    ## add object affected by spring force 
    def linkTo(self,obj,point):
        if (point==self.start):
            self.actsOn.append((obj,'s'))
            # apply current spring force to the mass object
            #obj.applyForce(-self.kappa*((self.end-self.start)-self.length),self)
        else:
            self.actsOn.append((obj,'e'))
            # apply current spring force to the mass object
            #obj.applyForce(self.kappa*(self.end-self.start-self.length),self)
    
    ## define co-ordinates of points forming the spring
    def draw(self,start,end):
        self.start=start.copy() # update spring's starting point
        self.end=end.copy()     # update spring's end point
        # The spring vector along which spring lies (Spring's x and y components), (x comp = 0 in our case)
        SpringVec = end-start
        # Vector norm to find the length
        length = SpringVec.norm()
        # define (normalised) perpendicular vector for spring's spikes direction
        perpVect = Coord(SpringVec.y/length,-SpringVec.x/length)    # perpVect=(xperp,yperp), xperp=sin, yperp=cos
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
                step = SpringVec*0.05+SpringVec*0.9*float(i+j/4.0)/self.nCoils+wiggle[j]
                Pos['x'].append(start.x+step.x)
                Pos['y'].append(start.y+step.y)
        
        # add final points
        Pos['x'].append(end.x-0.05*SpringVec.x)
        Pos['y'].append(end.y-0.05*SpringVec.y)
        Pos['x'].append(end.x)
        Pos['y'].append(end.y)
        
        # add calculated points to figure
        self.Position.data=Pos
        # return length (with direction for overly compressed spring)
        return SpringVec
    
    ## draw spring on figure
    def plot(self,fig,colour="#808080",width=1):
        fig.line(x='x',y='y',color=colour,source=self.Position,line_width=width)
    
    ## place spring in space
    def compressTo(self,start,end):
        # draw deformed spring and equate current length to spring's vector
        length=self.draw(start,end) 

        # calculate the force exerted on/by the spring
        # This is done by finding the scalar product between (delta length vector = current SpringVec - initial SpringVec) 
        # and the (initial normalized spring vector). The scalar product produces the magnitude of the 
        # component of delta length vector which lies along initial normalized spring vector
        Fs = -self.kappa*(length-self.length).prod_scal(self.Norm_Initial_Length)  # Float

        # apply force to each object that the spring acts on
        for i in range(0,len(self.actsOn)):
            self.actsOn[i][0].applyForce(Fs*self.out(self.actsOn[i][1]),self)    # applyForce(Coord,obj)! multiply by Norm_Initial_Length to get a force vector
        # return the force
        return Fs
    
    ## if spring's current end (upper or lower) is moved, then compress spring accordingly and calculate resulting force
    def movePoint(self,SpringEnd,moveVect):
        if (SpringEnd==self.start):
            return self.compressTo(SpringEnd + moveVect,self.end) # spring's upper end displace due to mass movement
        else:
            return self.compressTo(self.start,SpringEnd + moveVect)  # spring's lower end displace due to root point excitation
    
    # return outward direction
    def out(self,se):
        # -1*direction
        if (se=='s'):
            return -self.Norm_Initial_Length
        else:
            return self.Norm_Initial_Length
    
    def changeSpringConst(self,kappa):
        self.kappa=kappa
    
    def changeL0(self,x0,spacing = 1.0):
        self.length = self.Norm_Initial_Length*x0
        # define the number of coils with respect to the relaxed position of the spring
        self.nCoils=int(floor(x0/spacing))

