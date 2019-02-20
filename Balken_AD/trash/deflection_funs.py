#deflection function:

def Fun_Deflection(a,b,l,p,x,xf,resol,E,I):
    ynew = []
    ynew1 = []
    ynew2 = []

    if (l == 0):
        ynew = []
        a = xf - a;     #The a for cantilever is the distance between
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
            ynew = list(reversed(ynew))

    else:

        for i in range(0,int(l*(resol/10) ) ):
            if a > l:
                dy = ( ( p * b * x[i]) / (6 * E * I * l) ) * ( (l**2) - (x[i]**2) )
            else:
                if x[i] < a:
                    dy = ( ( p * b * x[i]) / (6 * E * I * l) ) * ( (l**2) - (b**2) - (x[i]**2) )
                elif x[i] == a:
                    dy = ( p * (a**2) * (b**2) ) / (3 * E * I * l)
                elif x[i] > a and x[i] <= l:
                    dy = ( (p * a * (l-x[i]) ) / (6 * E * I * l) ) * ( (2*l*x[i]) - (x[i]**2) - (a**2) )
            ynew1.append(dy)

        new_range = int(resol - l*10)
        for i in range(0,new_range):
            dy1 = -1 *( ( (p * a * b * x[i]) / (6 * E * I * l) ) * (l + a) )
            ynew2.append(dy1)
        ynew = ynew1 + ynew2
    return ynew
