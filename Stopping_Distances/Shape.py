

class Shape:
    def __init__ (self,x,y):
        self.x=x
        self.y=y
    
    def __add__(self,(b,c)):
        x=list(self.x)
        y=list(self.y)
        for i in range(0,len(x)):
            x[i]+=b
            y[i]+=c
        return Shape(x,y)
