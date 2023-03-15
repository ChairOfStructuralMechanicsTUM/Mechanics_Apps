from math import sqrt

class SRS_Coord(object):
    # initialise class
    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    # define Coord+Coord
    def __add__(self,A):
        return SRS_Coord(self.x+A.x,self.y+A.y)

    # define Coord+=Coord
    def __iadd__(self,A):
        self.x+=A.x
        self.y+=A.y
        return self
    
    # define Coord-Coord
    def __sub__(self,A):
        return SRS_Coord(self.x-A.x,self.y-A.y)
    
    # define Coord-=Coord
    def __isub__(self,A):
        self.x-=A.x
        self.y-=A.y
        return self
    
    # define Coord*num
    def __mul__(self,a):
        return SRS_Coord(self.x*a,self.y*a)
    
    # define num*Coord
    def __rmul__(self,a):
        return SRS_Coord(self.x*a,self.y*a)
    
    # define Coord*=num
    def __imul__(self,a):
        self.x*=a
        self.y*=a
        return self
    
    # define Coord/num
    def __div__(self,a):
        return SRS_Coord(self.x/a,self.y/a)
    
    # define Coord/=num
    def __idiv__(self,a):
        self.x/=a
        self.y/=a
        return self
    
    # define -Coord
    def __neg__(self):
        return SRS_Coord(-self.x,-self.y)
    
    # define Coord==Coord
    def __eq__ (self,A):
        # leave room for rounding errors
        return (abs(self.x-A.x)<1e-10 and abs(self.y-A.y)<1e-10)
    
    # define Coord!=Coord
    def __neq__(self,A):
        return (not (self==A))
    
    # define what is printed by print
    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+")"
    
    # function returning the norm
    def norm(self):
        return float(sqrt(self.x**2+self.y**2))
    
    # function returning the direction
    def direction(self):
        return SRS_Coord(self.x/self.norm(),self.y/self.norm())
    
    # function returning the perpendicular direction
    def perp(self):
        return SRS_Coord(self.y/self.norm(),-self.x/self.norm())
    
    def copy(self):
        return SRS_Coord(self.x,self.y)
    
    def prod_scal(self,A):
        return self.x*A.x+self.y*A.y
