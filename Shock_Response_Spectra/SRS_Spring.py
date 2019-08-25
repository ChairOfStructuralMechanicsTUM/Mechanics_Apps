from bokeh.models import ColumnDataSource
from math import floor
from SRS_Coord import SRS_Coord

class SRS_Spring(object):
    ## create spring
    def __init__(self,start,end,x0,spring_constant=50.0,spacing = 1.0):
        start = SRS_Coord(start[0],start[1])
        end   = SRS_Coord(end[0],end[1])
        # define spring constant
        self.spring_constant = spring_constant
        # define rest length
        self.length = x0
        # define the number of coils with respect to the relaxed position of the spring
        self.nCoils = int(floor(self.length/spacing))
        # Create ColumnDataSource
        self.Position = ColumnDataSource(data=dict(x=[],y=[]))
        # draw spring
        self.draw(start,end)
    
    ## define spring co-ordinates
    def draw(self,start,end):
        self.start=start.copy()
        self.end=end.copy()
        # find direction along which spring lies
        # (not normalised)
        direction = end-start
        # find normalising constant (=length)
        length = direction.norm()
        self.direction = SRS_Coord(direction.x/length,direction.y/length)
        # define (normalised) perpendicular vector for spike directions
        perpVect = SRS_Coord(direction.y/length,-direction.x/length)
        # create values to help with loop
        Pos    = dict(x=[],y=[])
        Zero   = SRS_Coord(0,0)
        wiggle = [Zero,perpVect,Zero,-perpVect]
        
        # add first points
        Pos['x'].append(start.x)
        Pos['y'].append(start.y)
        
        # loop over each coil
        for i in range(0,self.nCoils):
            # loop over the 4 points in the coil
            for j in range(0,4):
                # save points
                stepx = direction.x*0.05+direction.x*0.9*float(i+j/4.0)/self.nCoils+wiggle[j].x
                stepy = direction.y*0.05+direction.y*0.9*float(i+j/4.0)/self.nCoils+wiggle[j].y
                Pos['x'].append(start.x+stepx)
                Pos['y'].append(start.y+stepy)
        
        # add final points
        Pos['x'].append(end.x-0.05*direction.x)
        Pos['y'].append(end.y-0.05*direction.y)
        Pos['x'].append(end.x)
        Pos['y'].append(end.y)
        
        # add calculated points to figure
        self.Position.data=Pos
        # return current length
        return length
    
    ## draw spring on figure
    def plot(self,fig,colour="black",width=1):
        fig.line(x='x',y='y',color=colour,source=self.Position,line_width=width)
    
    def changeSpringConst(self,spring_constant):
        self.spring_constant=spring_constant

    @property
    def getSpringConstant(self):
        return self.spring_constant
