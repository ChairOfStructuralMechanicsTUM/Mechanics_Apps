import Maxwell_Constants as glc
from Maxwell_Functions_Side import side1, side2, side3

################################################################################
### frame functions
################################################################################



def create_prof(f):
    '''creates profile of non-stationary frames'''
    paramInt = f.get_param()
    i = f.get_mag()
    if int(paramInt) < 30:
        side1(f,paramInt,i)
        f.dline.data = dict( x = [-10,10], y = [0.1+ paramInt*(1.0/60),0.1+ paramInt*(1.0/60)] )
        f.dlabel.data = dict(x=[glc.plotx0+0.05] , y=[0.1+ paramInt*(1.0/60)], name = [f.n])
    elif (int(paramInt)> 30) & (int(paramInt) < 70) :
        side2(f,paramInt,i)
        f.dline.data = dict( x = [0.1 + (paramInt-30)*(0.0175),0.1 + (paramInt-30)*(0.0175)], y = [-10,10] )
        f.dlabel.data = dict(x=[0.11 + (paramInt-30)*(0.0175)] , y=[glc.plotyf-0.06], name = [f.n])
    elif  int(paramInt) > 70:
        side3(f,paramInt,i)
        f.dline.data = dict( x = [-10,10], y = [0.6 - (paramInt%70)*(1.0/60),0.6 - (paramInt%70)*(1.0/60)] )
        f.dlabel.data = dict(x=[glc.plotxf-0.05] , y=[0.6 - (paramInt%70)*(1.0/60)], name = [f.n])

    if (i == 0):
        f.dline.data = dict(x = [], y = [] )
        f.dline.data = dict(x = [], y = [], name = [] )


    

def compute_shift(paramInt1, paramInt2, i):
    '''Computes the shift at the load. These values are used for the load arrows'''
    d7 = i / glc.FScale

    localDouble = []                                                            #create a localdouble array

    d1 = paramInt2 / 30.0 * glc.a
    d2 = glc.a - d1
    d4 = -(1.0/6.0) * d7 * d1 * glc.b
    d3 = -d4 + d7 / 2.0 * glc.a * glc.a - d7 / 2.0 * d2 * d2
    d5 = d7 * d1 * glc.b / 2.0 + d4
    d8 = -(1.0/6.0) * d7 * (glc.a**3) + d3 * glc.a + (1.0/6.0) * d7 * ( (glc.a - d1) ** 3 )
    d9 = 0.0
    d10 = 0.0
    if (paramInt1 < 30):
        d6 = paramInt1 / 30.0 * glc.a
        if (d6 < d1):
            d9 = -1.0/6.0 * d7 * d6 * d6 * d6 + d3 * d6
        else:
            d9 = -1.0/6.0 * d7 * d6 * d6 * d6 + d3 * d6 + 1.0/6.0 * d7 * ((d6 - d1)**3.0)

    if ((30 <= paramInt1) & (paramInt1 <= 70)):
        d6 = (paramInt1 - 30) / 40.0 * glc.b
        d10 = 0.5 * d7 * d1 * d6 * d6 - 1.0/6.0 * d7 * d1 / glc.b * (d6**3.0) + d4 * d6
        d9 = d8

    if (paramInt1 > 70):
        d6 = (paramInt1 - 70) / 30.0 * glc.a
        d9 = d5 * d6 + d8

    if (paramInt2 < 30):
        localDouble = [d9,d10]
        pass

    d11 = (paramInt2 - 30) / 40.0 * glc.b
    d4 = d7 / 6.0 * ( ((glc.b - d11)**3.0) - (glc.b - d11) * glc.b)
    d3 = -d4
    d5 = d7 / 2.0 * ( (glc.b - d11) * glc.b - ((glc.b - d11)**2.0) ) + d4

    d8 = d3 * glc.a
    d9 = 0.0
    d10 = 0.0
    if (paramInt1 < 30):
        d6 = paramInt1 / 30.0 * glc.a
        d9 = d3 * d6

    if ((30 <= paramInt1) & (paramInt1 <= 70)):
        d6 = (paramInt1 - 30) / 40.0 * glc.b
        if (d6 < d11):
            d10 = (d7 / 6.0) *  ( (glc.b - d11) / glc.b ) * d6 * d6 * d6 + d4 * d6
        else:
            d10 = d7 / 6.0 * (glc.b - d11) / glc.b * d6 * d6 * d6 + d4 * d6 - d7 / 6.0 * ((d6 - d11)**3.0)
        d9 = d8

    if (paramInt1 > 70):
        d6 = (paramInt1 - 70) / 30.0 * glc.a
        d9 = d5 * d6 + d8

    if ((paramInt2 >= 30) & (paramInt2 <= 70)):
        localDouble = [d9, d10]


    d1  = (100 - paramInt2) / 30.0 * glc.a
    d2  = glc.a - d1
    d12 = d7 * d1 / glc.b
    d4  = 1.0 / glc.b * (d7 * glc.a / 2.0 * glc.b * glc.b - d12 * glc.b * glc.b * glc.b / 6.0)
    d3  = -d4 - d7 / 2.0 * glc.a * glc.a
    d5  = -d7 * glc.a * glc.b + d12 * glc.b * glc.b / 2.0 + d4
    d8  = d7 / 6.0 * glc.a * glc.a * glc.a + d3 * glc.a
    d9  = 0.0
    d10 = 0.0
    if (paramInt1 < 30):
        d6 = paramInt1 / 30.0 * glc.a
        d9 = d7 / 6.0 * d6 * d6 * d6 + d3 * d6

    if ((30 <= paramInt1) & (paramInt1 <= 70)):
        d6  = (paramInt1 - 30) / 40.0 * glc.b
        d10 = -d7 * glc.a / 2.0 * d6 * d6 + d12 * d6 * d6 * d6 / 6.0 + d4 * d6
        d9  = d8

    if (paramInt1 > 70):
        d6 = (paramInt1 - 70) / 30.0 * glc.a
        if (d6 < d2):
            d9 = -d7 * d2 / 2.0 * d6 * d6 + d7 / 6.0 * d6 * d6 * d6 + d5 * d6 + d8
        else:
            d9 = -d7 * d2 / 2.0 * d6 * d6 + d7 / 6.0 * d6 * d6 * d6 + d5 * d6 - d7 / 6.0 * ((d6 - d2)**3.0) + d8

    if (paramInt2 > 70):
        localDouble = [d9, d10]

    return localDouble

def create_shift(f): 
    '''Changes the values of the arrows that display how much of
    a shift has occurred'''
    
    if (f.get_mag() == 0):
        if (f.get_param() == 0):
            f.e_s.stream(dict(xS= [], xE= [], yS= [], yE=[], lW = [] ),rollover=-1)
    else:
        paramInt1 = f.get_param()
        localDouble1 = compute_shift(paramInt1,paramInt1, f.get_mag())
        
        if (f.name == "F"u"\u2081"):
            names = " w"u"\u2081"u"\u2081"
        elif (f.name == "F"u"\u2082"):
            names = " w"u"\u2082"u"\u2082"

 
        d2 = 0
        d1 = 0
        sclr = 10
        if (paramInt1 < 30):
            d2 = paramInt1 / 30.0 * 0.5 + 0.1
            d1 = 0.1
            f.e_s.stream(dict(xS= [ d1 ], xE= [d1 + 1.35*localDouble1[0]],
            yS= [d2], yE=[d2], lW = [abs(localDouble1[0]*sclr) ] ),rollover=1)

            if (f.name ==  "F"u"\u2081"):
                y1 = -0.05
                y2 = -0.05
            elif (f.name ==  "F"u"\u2082"):
                y1 = 0.7
                y2 = 0.7
            x1 = d1 + 1.39*localDouble1[0]
            x2 = d1
        elif ((30 <= paramInt1) & (paramInt1 <= 70)):
            d1 = (paramInt1 - 30) / 40.0 * 0.7 + 0.1
            d2 = 0.6

            if (f.name ==  "F"u"\u2081"):
                x1 = 0
                x2 = 0
            elif (f.name ==  "F"u"\u2082"):
                x1 = 0.85
                x2 = 0.85
            y1 = d2 + localDouble1[1]
            y2 = d2

            f.e_s.stream(dict(xS= [ d1 ], xE= [d1],
            yS= [d2 + localDouble1[1] ], yE=[d2], lW = [abs(localDouble1[1]*sclr) ] ),rollover=1)

        elif (paramInt1 > 70):
            d1 = 0.8
            d2 = 0.6 - (paramInt1 - 70) / 30.0 * 0.5

            if (f.name ==  "F"u"\u2081"):
                y1 = -0.05
                y2 = -0.05
            elif (f.name ==  "F"u"\u2082"):
                y1 = 0.7
                y2 = 0.7

            x1 = d1 + localDouble1[0]
            x2 = d1
            f.e_s.stream(dict(xS= [ d1], xE= [d1 + localDouble1[0] ],
            yS= [d2], yE=[d2], lW = [ abs(localDouble1[0]*sclr ) ] ),rollover=1)

        f.w1.stream(dict(xS= [x1], xE= [x2],
        yS= [y1], yE=[y2], name = [names] ),rollover=1)
        
        f.w2.stream(dict(xS= [ x2 ], xE= [x1],
        yS= [y2], yE=[y1] ),rollover=1)
        


def create_wdline(f):
    '''Creates the dashed lines that represent how much has been deformed in each side.
       You can see that both lines are as far apart as w1 and w2. Therefore the dashed
       lines are dependent on w1 and w2'''
    if f.get_mag() == 0:
        f.wdline.data = dict(x1 = [] , x2 = [] ,y1 = [] , y2 = [])
    else:
        f.wdline.data = dict(x1 = [ f.w1.data['xS'][0], f.w1.data['xS'][0] ]  , x2 = [  f.w2.data['xS'][0], f.w2.data['xS'][0] ] ,
        y1 = [ f.w1.data['yS'][0] , f.e_s.data['yS'][0] ] , y2 = [ f.w2.data['yS'][0], f.e_s.data['yS'][0] ] )
