
# class that can add tuples to lists of x and y values
# e.g. a patch is defined by coordinates X=[...], Y=[...]
# if we want to displace the object by (b,c) then
# if the patch coordinates are saved in a Shape we can simply do
# myShape+(b,c)

class SD_Shape:
    def __init__ (self,x,y):
        self.x=x
        self.y=y
    
    def __add__(self,(b,c)):
        x=list(self.x)
        y=list(self.y)
        for i in range(0,len(x)):
            x[i]+=b
            y[i]+=c
        return SD_Shape(x,y)
