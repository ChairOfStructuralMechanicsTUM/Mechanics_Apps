import Maxwell_Constants as glc

################################################################################
### all three side functions
################################################################################


def side1(f,paramInt,i):
    '''Calculates deformation of the left hand side (side1).
       Obtained from Java code'''
    x1          = []
    x2          = []
    x3          = []
    y1          = []
    y2          = []
    y3          = []

    d1 = i / glc.FScale
    d7 = 0.8
    d8 = 0.1
    d2 = 0
    d3 = 0
    d5 = 0
    d4 = 0
    d6 = 0
    d9 = 0
    d12 = 0
    d13 = 0

    #change arrow:
    if (i<0):
       # f.arrow_source.data = dict(xS= [0.12-i/glc.arr_scal], xE= [0.12],
        #yS= [0.1 + paramInt*(1.0/60)], yE=[0.1+ paramInt*(1.0/60)], lW = [abs(i/glc.arr_scal)] )
        f.arrow_source.stream(dict(xS= [0.12-i/glc.arr_scal], xE= [0.12],
        yS= [0.1 + paramInt*(1.0/60)], yE=[0.1+ paramInt*(1.0/60)], lW = [abs(i/glc.arr_scal)]),rollover=1)
        f.label.data = dict(x = [0.12-i/glc.arr_scal], y = [0.1+ paramInt*(1.0/60)], name = [f.name])

    elif i>0:
        #f.arrow_source.data = dict(xS= [0.08-i/glc.arr_scal], xE= [0.08],
        #yS= [0.1 + paramInt*(1.0/60)], yE=[0.1+ paramInt*(1.0/60)], lW = [abs(i/glc.arr_scal)] )
        f.arrow_source.stream(dict(xS= [0.08-i/glc.arr_scal], xE= [0.08],
        yS= [0.1 + paramInt*(1.0/60)], yE=[0.1+ paramInt*(1.0/60)], lW = [abs(i/glc.arr_scal)]),rollover=1)
        
        f.label.data = dict(x = [0.08-i/glc.arr_scal], y = [0.1+ paramInt*(1.0/60)], name = [f.name])
    else:
        f.label.data = dict(x = [0.03-i/glc.arr_scal], y = [0.1+ paramInt*(1.0/60)], name = [f.name])



    d2 = (paramInt / 30.0) * glc.a

    d3 = glc.a - d2
    d5 = (-1/3.0) * d1 * d2 * glc.b
    d4 = -d5 + ( (d1 / 2.0) * glc.a * glc.a  ) - ( (d1 / 2.0) * d3 * d3)
    d6 = d1 * d2 * (glc.b / 2.0) + d5
    d9 = glc.a / 4.0
    d11 = 0.1
    d12 = 0.1
    d7 = 0.0
    d8 = 0.0

    for j in range(1,5):
        d13 = j * d9
        d8 = d13 + d12
        if (d13 < d2):
            d7 = (-1.0/6.0) * (d1 * d13 * d13 * d13) + (d4 * d13) + d11
        else:
            d7 = (-1.0/6.0) * (d1 * d13 * d13 * d13) + (d4 * d13) + (1.0/6.0) * (d1 * ( (d13 - d2)**3 ) ) + d11
        x1.append(d7)
        y1.append(d8)
    d11 = d7
    d12 = d8
    d9 = glc.b / 4.0

    for j in range(0,5):
        d13 = j * d9
        d7  = d13 + d11
        d8  = (0.5 * d1 * d2 * d13 * d13) -  ( (1.0/6.0) * d1 * (d2  /  glc.b) * (d13**3.0) ) + (d5 * d13) + d12
        x2.append(d7)
        y2.append(d8)

    d11 = d7
    d12 = d8
    d9  = glc.a/4.0

    for j in range(0,5):
        d13 = j * d9
        d8 = d12 - d13
        d7 = d11 + (d6 * d13)
        x3.append(d7)
        y3.append(d8)

        #output:
    x = [0.1] + x1 + x2 + x3
    y = [0.1] + y1 + y2 + y3
    f.pts.data = dict(x = x, y = y )                                            #updates the frame of object f

def side2(f,paramInt,i):
    '''Calculates the deformations of the top of the frame (side 2)'''
    x1          = []
    x2          = []
    x3          = []
    y1          = []
    y2          = []
    y3          = []

    #add arrow changing function here
    #change arrow:

    if i<0:
        #f.arrow_source.data = dict(xS= [0.1 + (paramInt-30)*(0.0175)], xE= [0.1 + (paramInt-30)*(0.0175)],
        #yS= [0.58+i/glc.arr_scal], yE=[0.58], lW = [abs(i/glc.arr_scal)] )
        f.arrow_source.stream(dict(xS= [0.1 + (paramInt-30)*(0.0175)], xE= [0.1 + (paramInt-30)*(0.0175)],
        yS= [0.58+i/glc.arr_scal], yE=[0.58], lW = [abs(i/glc.arr_scal)] ),rollover=1)
        f.label.data = dict(x = [0.1 + (paramInt-30)*(0.0175)], y = [0.58+i/glc.arr_scal], name = [f.name])

    elif i>0:
        #f.arrow_source.data = dict(xS= [0.1 + (paramInt-30)*(0.0175)], xE= [0.1 + (paramInt-30)*(0.0175)],
        #yS= [0.62+i/glc.arr_scal], yE=[0.62], lW = [abs(i/glc.arr_scal)] )
        f.arrow_source.stream(dict(xS= [0.1 + (paramInt-30)*(0.0175)], xE= [0.1 + (paramInt-30)*(0.0175)],
        yS= [0.62+i/glc.arr_scal], yE=[0.62], lW = [abs(i/glc.arr_scal)] ),rollover=1)
        f.label.data = dict(x = [0.1 + (paramInt-30)*(0.0175)], y = [0.62+i/glc.arr_scal], name = [f.name])
    else:
        f.label.data = dict(x = [0.1 + (paramInt-30)*(0.0175)], y = [0.62+i/glc.arr_scal], name = [f.name])



    d1 = i / glc.FScale
    d10 = 0
    d14 = 0
    d9  = (paramInt - 30) / 40.0 * glc.b
    d5  = (d1 / 6.0) * ( ( (glc.b - d9)**3.0 ) -  (  (glc.b - d9) * glc.b ) )
    d4  = -d5
    d6  =  (d1 / 2.0) * ( ((glc.b - d9) * glc.b) - ((glc.b - d9)**2) ) + d5
    d10 = glc.a / 4.0
    d12 = 0.1
    d13 = 0.1
    d7  = 0
    d8  = 0

    for k in range(1,5):
        d14 = k * d10
        d8  = d13 + d14
        d7  = (d4 * d14) + d12
        x1.append(d7)
        y1.append(d8)

    d12 = d7
    d13 = d8
    d10 = glc.b/4.0

    for k in range(1,5):
        d14 = k * d10
        d7  = d14 + d12

        if (d14 < d9):
            d8 = d13 + (d1 / 6.0) * ( (glc.b - d9) / glc.b )  * d14 * d14 * d14 + (d5 * d14)
        else:
            d8 = d13 + d1 / 6.0 * (glc.b - d9) / glc.b * d14 * d14 * d14 + d5 * d14 - d1 / 6.0 * ((d14 - d9)**3.0)

        x2.append(d7)
        y2.append(d8)

    d12 = d7
    d13 = d8
    d10 = glc.a/4.0

    for k in range(1,5):
        d14 = k * d10
        d8 = d13 - d14
        d7 = d12 + d6 * d14
        x3.append(d7)
        y3.append(d8)

        #output:
    x = [0.1] + x1 + x2 + x3
    y = [0.1] + y1 + y2 + y3
    f.pts.data = dict(x = x, y = y )

def side3(f,paramInt,i):
    '''Calculates the deformation of the right hand side (side 3)'''
    x1          = []
    x2          = []
    x3          = []
    y1          = []
    y2          = []
    y3          = []


    #change arrow:

    if i<0:
        #f.arrow_source.data = dict(xS= [0.78+i/glc.arr_scal], xE= [0.78],
        #yS= [0.6 - (paramInt%70)*(1.0/60)], yE=[0.6 - (paramInt%70)*(1.0/60)], lW = [abs(i/glc.arr_scal)] )
        f.arrow_source.stream(dict(xS= [0.78+i/glc.arr_scal], xE= [0.78],
        yS= [0.6 - (paramInt%70)*(1.0/60)], yE=[0.6 - (paramInt%70)*(1.0/60)], lW = [abs(i/glc.arr_scal)] ),rollover=1)
        f.label.data = dict(x = [0.78+i/glc.arr_scal], y = [0.6 - (paramInt%70)*(1.0/60)], name = [f.name])

    elif i>0:
        #f.arrow_source.data = dict(xS= [0.82+i/glc.arr_scal], xE= [0.82],
        #yS= [0.6 - (paramInt%70)*(1.0/60)], yE=[0.6 - (paramInt%70)*(1.0/60)], lW = [abs(i/glc.arr_scal)] )
        f.arrow_source.stream(dict(xS= [0.82+i/glc.arr_scal], xE= [0.82],
        yS= [0.6 - (paramInt%70)*(1.0/60)], yE=[0.6 - (paramInt%70)*(1.0/60)], lW = [abs(i/glc.arr_scal)] ),rollover=1)
        f.label.data = dict(x = [0.82+i/glc.arr_scal], y = [0.6 - (paramInt%70)*(1.0/60)], name = [f.name])
    else:
        f.label.data = dict(x = [0.82+i/glc.arr_scal], y = [0.6 - (paramInt%70)*(1.0/60)], name = [f.name])


    d1 = i / glc.FScale
    d2 = (100 - paramInt) / 30.0 * glc.a
    d3 = glc.a - d2
    d9 = d1 * d2 / glc.b
    d5 = 10 / glc.b * (d1 * glc.a / 20 * glc.b * glc.b - d9 * glc.b * glc.b * glc.b / 60)
    d4 = -d5 - d1 / 2.0 * glc.a * glc.a
    d6 = -d1 * glc.a * glc.b + d9 * glc.b * glc.b / 2.0 + d5
    d10 = glc.a / 4.0
    d12 = 0.1
    d13 = 0.1
    d7 = 0.0
    d8 = 0.0

    for k in range(1,5):
        d14 = k * d10
        d8 = d14 + d13
        d7 = d1 / 6.0 * d14 * d14 * d14 + d4 * d14 + d12
        x1.append(d7)
        y1.append(d8)

    d12 = d7
    d13 = d8
    d10 = glc.b/4.0

    for k in range(1,5):
        d14 = k * d10
        d7 = d14 + d12
        d8 = d13 - d1 * glc.a / 2.0 * d14 * d14 + d9 * d14 * d14 * d14 / 6.0 + d5 * d14
        x2.append(d7)
        y2.append(d8)

    d12 = d7
    d13 = d8
    d10 = glc.a / 4.0

    for k in range(1,5):
        d14 = k * d10
        d8 = d13 - d14

        if (d14<d3):
            d7 = d12 - d1 * d3 / 2.0 * d14 * d14 + d1 / 6.0 * d14 * d14 * d14 + d6 * d14
        else:
            d7 = d12 - d1 * d3 / 2.0 * d14 * d14 + d1 / 6.0 * d14 * d14 * d14 + d6 * d14 - d1 / 6.0 * ( (d14 - d3)**3.0)
        x3.append(d7)
        y3.append(d8)

        #output:
    x = [0.1] + x1 + x2 + x3
    y = [0.1] + y1 + y2 + y3
    f.pts.data = dict(x = x, y = y )
