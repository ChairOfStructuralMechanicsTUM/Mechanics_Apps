#cantilever functions:


def Fun_Cantilever():
    triangle_source.data = dict(x = [], y = [], size = [])
    f1_arrow_source.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [])
    f2_arrow_source.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [])
    top = 2
    bottom  = -top
    left = -1
    right = 0
    clines = 40
    quad_source.data = dict(top = [top], bottom = [bottom], left = [left] , right = [right])
    xseg = np.ones(clines) * left
    yseg = np.linspace(bottom,top-0.2,clines)
    x1seg = np.ones(clines) * right
    y1seg = np.linspace(bottom+0.2,top,clines)
    segment_source.data = dict(x0= xseg, y0= yseg,x1 = x1seg, y1 =y1seg)

def Fun_C_Deflection(p,b,x,resol,xf,E,I):
    '''Calculates the deflection of the beam when it is cantilever'''
    #b is the distance from the wall to the concentrated load

    ynew = []
    a = xf - b;     #The a for cantilever is the distance between
                    #the free end and the concentrated load.
    for i in range(0,resol):
        if x[i] < a:
            #dy = (  ( p * ( ( xf - x[i])**2 ) ) / (6 * E * I) ) * ( (3*b) - xf + x[i] )
            dy = (  ( p * (b**2) ) / (6 * E * I)  ) * ( (3*xf) - (3*x[i]) - b )
        elif x[i] == a:
            dy = ( p * (b**3) ) / (3 * E * I)
        elif x[i] > a:
            #dy = (  ( p * (a**2) ) / (6 * E * I)  ) * ( (3*xf) - (3*x[i]) - a )
            dy = (  ( p * ( ( xf - x[i])**2 ) ) / (6 * E * I) ) * ( (3*b) - xf + x[i] )
        ynew.append(dy)

    return list(reversed(ynew))     #need to reverse because x is calculated in the opposite direction
