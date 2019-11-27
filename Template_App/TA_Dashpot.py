from bokeh.models import ColumnDataSource
from TA_Coord import TA_Coord
from copy import deepcopy

class TA_Dashpot(object):
    def __init__(self,start,end,w,damping_constant=1.0):
        start = TA_Coord(start[0],start[1])
        end   = TA_Coord(end[0],end[1])
        # define dashpot constant
        self.damping_constant = damping_constant
        # save points
        self.start     = start
        self.end       = end
        self.origStart = start
        self.origEnd   = end
        # define width
        self.width = w
        # find direction along which dashpot lies
        # (not normalised)
        self.direction = end-start
        # define (normalised) perpendicular vector for spike directions
        perpVect = self.direction.perp()
        perpVect *= self.width
        self.CasingStart = dict(x=[end.x-self.direction.x/8.0+perpVect.x/2.0,
            start.x+self.direction.x/8.0+perpVect.x/2.0,start.x+self.direction.x/8.0-perpVect.x/2.0,
            end.x-self.direction.x/8.0-perpVect.x/2.0],y=[end.y-self.direction.y/8.0+perpVect.y/2.0,
            start.y+self.direction.y/8.0+perpVect.y/2.0,start.y+self.direction.y/8.0-perpVect.y/2.0,
            end.y-self.direction.y/8.0-perpVect.y/2.0])
        self.Line1Start  = dict(x=[start.x,
            start.x+self.direction.x/8.0],y=[start.y,start.y+self.direction.y/8.0])
        self.PistonStart = dict(x=[end.x-self.direction.x/2.0+perpVect.x/2.0,
            end.x-self.direction.x/2.0-perpVect.x/2.0], y=[end.y-self.direction.y/2.0+perpVect.y/2.0,
            end.y-self.direction.y/2.0-perpVect.y/2.0])
        self.Line2Start  = dict(x=[end.x,
            end.x-self.direction.x/2.0],y=[end.y,end.y-self.direction.y/2.0])
        # Create ColumnDataSources with initial positions
        self.Casing = ColumnDataSource(data=self.CasingStart)
        self.Line1  = ColumnDataSource(data=self.Line1Start)
        self.Piston = ColumnDataSource(data=self.PistonStart)
        self.Line2  = ColumnDataSource(data=self.Line2Start)
        self.direction = self.direction.direction()
    
    ## define dashpot co-ordinates
    def draw(self,start,end):
        # can't be based on previous as bokeh too slow
        casing = deepcopy(self.CasingStart)
        line1  = deepcopy(self.Line1Start)
        displacement = start-self.origStart
        for i in range(0,4):
            casing['x'][i] += displacement.x
            casing['y'][i] += displacement.y
        for i in range(0,2):
            line1['x'][i]  += displacement.x
            line1['y'][i]  += displacement.y
        
        piston = deepcopy(self.PistonStart)
        line2  = deepcopy(self.Line2Start)
        displacement = end-self.origEnd
        for i in range(0,2):
            piston['x'][i] += displacement.x
            piston['y'][i] += displacement.y
            line2['x'][i]  += displacement.x
            line2['y'][i]  += displacement.y
        
        # add calculated points to figure
        self.Casing.data = casing
        self.Line1.data  = line1
        self.Piston.data = piston
        self.Line2.data  = line2
        
        displacement = end-self.end + start-self.start
        
        self.start = start.copy()
        self.end   = end.copy()
        
        # return total displacement
        return displacement.prod_scal(self.direction)
    
    ## draw dashpot on figure
    def plot(self,fig,colour="black",width=1):
        fig.line(x='x',y='y',color=colour,source=self.Casing,line_width=width)
        fig.line(x='x',y='y',color=colour,source=self.Piston,line_width=width)
        fig.line(x='x',y='y',color=colour,source=self.Line1, line_width=width)
        fig.line(x='x',y='y',color=colour,source=self.Line2, line_width=width)
    
    def changeDamperCoeff(self,damping_constant):
        self.damping_constant = damping_constant

    @property
    def getDampingCoefficient(self):
        return self.damping_constant

