from bokeh.plotting import Figure, output_file , show
from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, NormalHead, Arrow
from bokeh.layouts import column, row, widgetbox
from bokeh.models.widgets import Button
from bokeh.models.glyphs import Text
from bokeh.io import curdoc
import numpy as np
from os.path import dirname, join, split


#main1
#conversion of java code

#Class frame: This creates an object of type Frame. The frame contains variables
#that are pertaining to the frame. For this app, 2 frames are created (F1 and F2)
#F1 is the initial frame, and F2 is the new frame once  F1 has been frozen.
class Frame(object):
    def __init__(self,name,n):
        self.pts            = ColumnDataSource(data=dict(x = [], y = [] ))
        self.p_mag          = 0
        self.boundary       = 0
        self.x0             = 0.1
        self.xf             = 0.8
        self.y0             = 0.1
        self.yf             = 0.6
        self.name           = name
        self.p_loc          = 0
        self.mag_start      = -100
        self.mag_end        = 100
        self.mag_val        = 0
        self.loc_start      = 0
        self.loc_end        = 100
        self.loc_val        = 50
        self.n              = n
        self.arrow_source   = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
        self.e_s            = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
        self.tri            = ColumnDataSource(data=dict(x= [], y= [], size = []))
        self.seg            = ColumnDataSource(data=dict(x0=[], x1=[], y0=[], y1=[]))
        self.t_line         = ColumnDataSource(data=dict(x=[], y=[]))
        self.label          = ColumnDataSource(data=dict(x=[] , y=[], name = []))
        self.dline          = ColumnDataSource(data=dict(x=[], y=[]))
        self.dlabel         = ColumnDataSource(data=dict(x=[] , y=[], name = []))
        self.w1             = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[]))
        self.w2             = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[]))
        self.wdline         = ColumnDataSource(data=dict(x1=[], x2 =[], y1 = [], y2=[]))

    def set_mag(self, a):
        '''Sets the magnitude of the load on frame (p_mag) equal to a'''
        self.p_mag = a
    def set_param(self, a):
        '''sets the location of load on frame (p_loc) equal to a'''
        self.p_loc = a
    def get_mag(self):
        '''Function returns load magnitude value'''
        return self.p_mag
    def get_param(self):
        '''Function returns load position value'''
        return self.p_loc

################################################################################
#global constants:
################################################################################
a           = 0.5                                                               #width of frames
b           = 0.7                                                               #Height of box
FScale      = 150.0                                                             #Scaling factor
#offsetKraft = 0.08                                                              #
tri_size    = 30                                                                #Default size of Triangle
changer     = 0                                                                 #Global variable that changes when 'save deformed button is clicked'
shift       = 0.01                                                              #Shifting factor
#shift2      = 0.015
ps = 0.3                                                                        #used to shift size of plot
plotx0 = 0.1-ps
plotxf = 0.8+ps                                                                 #plot x0 xf, y0, yf. used in plot creation.
ploty0 = -0.1
plotyf = 1.0
#Arrow Sources:
arr_scal        = 450.0                                                         #Scaling factor used for arrows
arr_lw          = 20.0                                                          #Scaling factor used for arrow widths
ground          = 0.07                                                          #height of ground (line made for the moveable side of frame)


################################################################################
###Creation of frames
################################################################################
orig            = Frame("o","0")                                                #Creation of original frame. This frame is a reference of the original location
default     = dict(x = [0.1,0.8], y = [0.1,0.1], size = [tri_size,tri_size])    #Creation of triangle of original frame
f1              = Frame("F1","n1")                                              #Creation of object Frame 1 "F1". This frame is the first to be deformed
f2              = Frame("F2","n2")                                              #Creation of object Frame 2
t_line          = dict(x=[0.7,0.9], y=[ground,ground])                          #Creation of Line



################################################################################
###Sliders and buttons
################################################################################

#Magnitude of load slider:
mag_start   = -100
mag_end     = 100
mag_val     = 0
mag_slider  = Slider(title="Magnitude", value=mag_val,
    start=mag_start, end=mag_end, step=1)



#Position of load slider:
loc_start = 0
loc_end = 100
loc_val = 50
loc_slider = Slider(title="Position", value=loc_val,
    start=loc_start, end=loc_end, step=1)

#Toggle buttons:
button = Button(label="Save Deformed Frame", button_type="success")             #Button to save the deformed frain. Calls function
rbutton = Button(label="Reset", button_type="success")                          #Reset button. Calls init function


################################################################################
###Functions
################################################################################

def create_orig(o):
    '''Creates stationary original frame'''
    x = [o.x0,o.x0,o.xf,o.xf]
    y = [o.y0,o.yf,o.yf,o.y0]
    o.pts.data = dict(x = x, y = y )


#ya =[0,0]
#xb = [0,0]
#a_fig = dict(xa = [orig.x0, orig.xf] , ya = [0,0], iay = [0-0.1,0+0.1], iax1 = [orig.x0,orig.x0], iax2 = [orig.xf,orig.xf] )


def create_prof(f):
    '''creates profile of non-stationary frames'''
    paramInt = f.get_param()
    i = f.get_mag()
    if int(paramInt) < 30:
        side1(f,paramInt,i)
        f.dline.data = dict( x = [-10,10], y = [0.1+ paramInt*(1.0/60),0.1+ paramInt*(1.0/60)] )
        f.dlabel.data = dict(x=[plotx0+0.05] , y=[0.1+ paramInt*(1.0/60)], name = [f.n])
    elif (int(paramInt)> 30) & (int(paramInt) < 70) :
        side2(f,paramInt,i)
        f.dline.data = dict( x = [0.1 + (paramInt-30)*(0.0175),0.1 + (paramInt-30)*(0.0175)], y = [-10,10] )
        f.dlabel.data = dict(x=[0.11 + (paramInt-30)*(0.0175)] , y=[plotyf-0.06], name = [f.n])
    elif  int(paramInt) > 70:
        side3(f,paramInt,i)
        f.dline.data = dict( x = [-10,10], y = [0.6 - (paramInt%70)*(1.0/60),0.6 - (paramInt%70)*(1.0/60)] )
        f.dlabel.data = dict(x=[plotxf-0.05] , y=[0.6 - (paramInt%70)*(1.0/60)], name = [f.n])

    if (i == 0):
        f.dline.data = dict(x = [], y = [] )
        f.dline.data = dict(x = [], y = [], name = [] )

def side1(f,paramInt,i):
    '''Calculates deformation of the left hand side (side1).
       Obtained from Java code'''
    x1          = []
    x2          = []
    x3          = []
    y1          = []
    y2          = []
    y3          = []

    d1 = i / FScale
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
        f.arrow_source.data = dict(xS= [0.12-i/arr_scal], xE= [0.12],
        yS= [0.1 + paramInt*(1.0/60)], yE=[0.1+ paramInt*(1.0/60)], lW = [abs(i/arr_lw)] )

        f.label.data = dict(x = [0.12-i/arr_scal], y = [0.1+ paramInt*(1.0/60)], name = [f.name])

    elif i>0:
        f.arrow_source.data = dict(xS= [0.08-i/arr_scal], xE= [0.08],
        yS= [0.1 + paramInt*(1.0/60)], yE=[0.1+ paramInt*(1.0/60)], lW = [abs(i/arr_lw)] )

        f.label.data = dict(x = [0.08-i/arr_scal], y = [0.1+ paramInt*(1.0/60)], name = [f.name])
    else:
        f.label.data = dict(x = [0.03-i/arr_scal], y = [0.1+ paramInt*(1.0/60)], name = [f.name])



    d2 = (paramInt / 30.0) * a

    d3 = a - d2
    d5 = (-1/3.0) * d1 * d2 * b
    d4 = -d5 + ( (d1 / 2.0) * a * a  ) - ( (d1 / 2.0) * d3 * d3)
    d6 = d1 * d2 * (b / 2.0) + d5
    d9 = a / 4.0
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
    d9 = b / 4.0

    for j in range(0,5):
        d13 = j * d9
        d7  = d13 + d11
        d8  = (0.5 * d1 * d2 * d13 * d13) -  ( (1.0/6.0) * d1 * (d2  /  b) * (d13**3.0) ) + (d5 * d13) + d12
        x2.append(d7)
        y2.append(d8)

    d11 = d7
    d12 = d8
    d9  = a/4.0

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
        f.arrow_source.data = dict(xS= [0.1 + (paramInt-30)*(0.0175)], xE= [0.1 + (paramInt-30)*(0.0175)],
        yS= [0.58+i/arr_scal], yE=[0.58], lW = [abs(i/arr_lw)] )

        f.label.data = dict(x = [0.1 + (paramInt-30)*(0.0175)], y = [0.58+i/arr_scal], name = [f.name])

    elif i>0:
        f.arrow_source.data = dict(xS= [0.1 + (paramInt-30)*(0.0175)], xE= [0.1 + (paramInt-30)*(0.0175)],
        yS= [0.62+i/arr_scal], yE=[0.62], lW = [abs(i/arr_lw)] )

        f.label.data = dict(x = [0.1 + (paramInt-30)*(0.0175)], y = [0.62+i/arr_scal], name = [f.name])
    else:
        f.label.data = dict(x = [0.1 + (paramInt-30)*(0.0175)], y = [0.62+i/arr_scal], name = [f.name])



    d1 = i / FScale
    d10 = 0
    d14 = 0
    d9  = (paramInt - 30) / 40.0 * b
    d5  = (d1 / 6.0) * ( ( (b - d9)**3.0 ) -  (  (b - d9) * b ) )
    d4  = -d5
    d6  =  (d1 / 2.0) * ( ((b - d9) * b) - ((b - d9)**2) ) + d5
    d10 = a / 4.0
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
    d10 = b/4.0

    for k in range(1,5):
        d14 = k * d10
        d7  = d14 + d12

        if (d14 < d9):
            d8 = d13 + (d1 / 6.0) * ( (b - d9) / b )  * d14 * d14 * d14 + (d5 * d14)
        else:
            d8 = d13 + d1 / 6.0 * (b - d9) / b * d14 * d14 * d14 + d5 * d14 - d1 / 6.0 * ((d14 - d9)**3.0)

        x2.append(d7)
        y2.append(d8)

    d12 = d7
    d13 = d8
    d10 = a/4.0

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
        f.arrow_source.data = dict(xS= [0.78+i/arr_scal], xE= [0.78],
        yS= [0.6 - (paramInt%70)*(1.0/60)], yE=[0.6 - (paramInt%70)*(1.0/60)], lW = [abs(i/arr_lw)] )

        f.label.data = dict(x = [0.78+i/arr_scal], y = [0.6 - (paramInt%70)*(1.0/60)], name = [f.name])

    elif i>0:
        f.arrow_source.data = dict(xS= [0.82+i/arr_scal], xE= [0.82],
        yS= [0.6 - (paramInt%70)*(1.0/60)], yE=[0.6 - (paramInt%70)*(1.0/60)], lW = [abs(i/arr_lw)] )

        f.label.data = dict(x = [0.82+i/arr_scal], y = [0.6 - (paramInt%70)*(1.0/60)], name = [f.name])
    else:
        f.label.data = dict(x = [0.82+i/arr_scal], y = [0.6 - (paramInt%70)*(1.0/60)], name = [f.name])


    d1 = i / FScale
    d2 = (100 - paramInt) / 30.0 * a
    d3 = a - d2
    d9 = d1 * d2 / b
    d5 = 10 / b * (d1 * a / 20 * b * b - d9 * b * b * b / 60)
    d4 = -d5 - d1 / 2.0 * a * a
    d6 = -d1 * a * b + d9 * b * b / 2.0 + d5
    d10 = a / 4.0
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
    d10 = b/4.0

    for k in range(1,5):
        d14 = k * d10
        d7 = d14 + d12
        d8 = d13 - d1 * a / 2.0 * d14 * d14 + d9 * d14 * d14 * d14 / 6.0 + d5 * d14
        x2.append(d7)
        y2.append(d8)

    d12 = d7
    d13 = d8
    d10 = a / 4.0

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

def compute_shift(paramInt1, paramInt2, i):
    '''Computes the shift at the load. These values are used for the load arrows'''
    d7 = i / FScale

    localDouble = []                                                            #create a localdouble array

    d1 = paramInt2 / 30.0 * a
    d2 = a - d1
    d4 = -(1.0/6.0) * d7 * d1 * b
    d3 = -d4 + d7 / 2.0 * a * a - d7 / 2.0 * d2 * d2
    d5 = d7 * d1 * b / 2.0 + d4
    d8 = -(1.0/6.0) * d7 * (a**3) + d3 * a + (1.0/6.0) * d7 * ( (a - d1) ** 3 )
    d9 = 0.0
    d10 = 0.0
    if (paramInt1 < 30):
        d6 = paramInt1 / 30.0 * a
        if (d6 < d1):
            d9 = -1.0/6.0 * d7 * d6 * d6 * d6 + d3 * d6
        else:
            d9 = -1.0/6.0 * d7 * d6 * d6 * d6 + d3 * d6 + 1.0/6.0 * d7 * ((d6 - d1)**3.0)

    if ((30 <= paramInt1) & (paramInt1 <= 70)):
        d6 = (paramInt1 - 30) / 40.0 * b
        d10 = 0.5 * d7 * d1 * d6 * d6 - 1.0/6.0 * d7 * d1 / b * (d6**3.0) + d4 * d6
        d9 = d8

    if (paramInt1 > 70):
        d6 = (paramInt1 - 70) / 30.0 * a
        d9 = d5 * d6 + d8

    if (paramInt2 < 30):
        localDouble = [d9,d10]
        pass

    d11 = (paramInt2 - 30) / 40.0 * b
    d4 = d7 / 6.0 * ( ((b - d11)**3.0) - (b - d11) * b)
    d3 = -d4
    d5 = d7 / 2.0 * ( (b - d11) * b - ((b - d11)**2.0) ) + d4

    d8 = d3 * a
    d9 = 0.0
    d10 = 0.0
    if (paramInt1 < 30):
        d6 = paramInt1 / 30.0 * a
        d9 = d3 * d6

    if ((30 <= paramInt1) & (paramInt1 <= 70)):
        d6 = (paramInt1 - 30) / 40.0 * b
        if (d6 < d11):
            d10 = (d7 / 6.0) *  ( (b - d11) / b ) * d6 * d6 * d6 + d4 * d6
        else:
            d10 = d7 / 6.0 * (b - d11) / b * d6 * d6 * d6 + d4 * d6 - d7 / 6.0 * ((d6 - d11)**3.0)
        d9 = d8

    if (paramInt1 > 70):
        d6 = (paramInt1 - 70) / 30.0 * a
        d9 = d5 * d6 + d8

    if ((paramInt2 >= 30) & (paramInt2 <= 70)):
        localDouble = [d9, d10]


    d1  = (100 - paramInt2) / 30.0 * a
    d2  = a - d1
    d12 = d7 * d1 / b
    d4  = 1.0 / b * (d7 * a / 2.0 * b * b - d12 * b * b * b / 6.0)
    d3  = -d4 - d7 / 2.0 * a * a
    d5  = -d7 * a * b + d12 * b * b / 2.0 + d4
    d8  = d7 / 6.0 * a * a * a + d3 * a
    d9  = 0.0
    d10 = 0.0
    if (paramInt1 < 30):
        d6 = paramInt1 / 30.0 * a
        d9 = d7 / 6.0 * d6 * d6 * d6 + d3 * d6

    if ((30 <= paramInt1) & (paramInt1 <= 70)):
        d6  = (paramInt1 - 30) / 40.0 * b
        d10 = -d7 * a / 2.0 * d6 * d6 + d12 * d6 * d6 * d6 / 6.0 + d4 * d6
        d9  = d8

    if (paramInt1 > 70):
        d6 = (paramInt1 - 70) / 30.0 * a
        if (d6 < d2):
            d9 = -d7 * d2 / 2.0 * d6 * d6 + d7 / 6.0 * d6 * d6 * d6 + d5 * d6 + d8
        else:
            d9 = -d7 * d2 / 2.0 * d6 * d6 + d7 / 6.0 * d6 * d6 * d6 + d5 * d6 - d7 / 6.0 * ((d6 - d2)**3.0) + d8

    if (paramInt2 > 70):
        localDouble = [d9, d10]

    return localDouble

def create_shift(f):
    '''Changes the values of the arrows that display how much of a shift has occurred'''
    if (f.get_mag() == 0):
        if (f.get_loc() == 0):
        f.e_s.data = dict(xS= [], xE= [],
        yS= [], yE=[], lW = [] )
    else:
        paramInt1 = f.get_param()
        #print orig.pts.data["y"]
        #sprint f2.pts.data["x"]
        #print f2.pts.data["y"]
        localDouble1 = compute_shift(paramInt1,paramInt1, f.get_mag())
        #print localDouble1
        d2 = 0
        d1 = 0
        sclr = 10
        if (paramInt1 < 30):
            d2 = paramInt1 / 30.0 * 0.5 + 0.1
            d1 = 0.1
            f.e_s.data = dict(xS= [ d1 ], xE= [d1 + localDouble1[0]],
            yS= [d2], yE=[d2], lW = [abs(localDouble1[0]*sclr) ] )

            if (f.name == "F1"):
                y1 = -0.05
                y2 = -0.05
            elif (f.name == "F2"):
                y1 = 0.7
                y2 = 0.7
            x1 = d1 + localDouble1[0]
            x2 = d1
        elif ((30 <= paramInt1) & (paramInt1 <= 70)):
            d1 = (paramInt1 - 30) / 40.0 * 0.7 + 0.1
            d2 = 0.6

            if (f.name == "F1"):
                x1 = 0
                x2 = 0
            elif (f.name == "F2"):
                x1 = 0.8
                x2 = 0.8
            y1 = d2 + localDouble1[1]
            y2 = d2

            f.e_s.data = dict(xS= [ d1 ], xE= [d1],
            yS= [d2 + localDouble1[1] ], yE=[d2], lW = [abs(localDouble1[1]*sclr) ] )

        elif (paramInt1 > 70):
            d1 = 0.8
            d2 = 0.6 - (paramInt1 - 70) / 30.0 * 0.5

            if (f.name == "F1"):
                y1 = -0.05
                y2 = -0.05
            elif (f.name == "F2"):
                y1 = 0.7
                y2 = 0.7

            x1 = d1 + localDouble1[0]
            x2 = d1
            f.e_s.data = dict(xS= [ d1], xE= [d1 + localDouble1[0] ],
            yS= [d2], yE=[d2], lW = [ abs(localDouble1[0]*sclr ) ] )

        f.w1.data = dict(xS= [x1], xE= [x2],
        yS= [y1], yE=[y2] )

        f.w2.data = dict(xS= [ x2 ], xE= [x1],
        yS= [y2], yE=[y1] )

def create_wdline(f):
    '''Creates the dashed lines that represent how much has been deformed in each side.
       You can see that both lines are as far apart as w1 and w2. Therefore the dashed
       lines are dependent on w1 and w2'''
    if f.get_mag() == 0:
        f.wdline.data = dict(x1 = [] , x2 = [] ,y1 = [] , y2 = [])
    else:
        f.wdline.data = dict(x1 = [ f.w1.data['xS'][0], f.w1.data['xS'][0] ]  , x2 = [  f.w2.data['xS'][0], f.w2.data['xS'][0] ] ,
        y1 = [ f.w1.data['yS'][0] , f.e_s.data['yS'][0] ] , y2 = [ f.w2.data['yS'][0], f.e_s.data['yS'][0] ] )

def update_fun(attr,old,new):
    '''This is the function that is called each time the sliders are used. It
    Changes the values of the frames and moves them. Most of the functions are
    called in update_fun

    changer == 0 means that the 'save deformed frame' button has not been
    pressed yet.
    changer == 1 is when the button has been preseed and f2 is created'''
    if changer == 0:
        f1.set_param(loc_slider.value)
        f1.set_mag(mag_slider.value)
        create_prof(f1)
        create_shift(f1)
        f1.tri.data = dict(x = [0.1,f1.pts.data["x"][-1]], y = [0.1,f1.pts.data["y"][-1]], size = [tri_size,tri_size])
        create_wdline(f1)
    elif changer != 0:
        f2.set_param(loc_slider.value)
        f2.set_mag(mag_slider.value)
        create_prof(f2)
        create_shift(f2)
        f2.tri.data = dict(x = [0.1,f2.pts.data["x"][-1]], y = [0.1,f2.pts.data["y"][-1]], size = [tri_size,tri_size])
        create_wdline(f2)
        f1.tri.data = dict(x = [0.1,f1.pts.data["x"][-1]], y = [0.1,f1.pts.data["y"][-1]], size = [tri_size,tri_size])

def button_fun():
    '''Function called when the 'save deformed frame' function is clicked.
    This button changes the changer value to 1, which affects update_fun
    (see update_fun for more details.) it also switches f2 to f1 if f2 already
    exists.'''
    global changer
    changer = 1
    f1.set_param(loc_slider.value)
    f1.set_mag(mag_slider.value)
    create_prof(f1)
    mag_slider.value        = mag_val
    loc_slider.value        = loc_val
    f2.e_s.data             = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    #update_fun(None,None,None)

def init():
    '''Function that initializes everything'''
    global changer
    changer                 = 0
    f1.label.data           = dict(x=[0.45] , y=[0.62], name = ["F1"])
    f2.label.data           = dict(x=[] , y=[], name = [])
    mag_slider.value        = mag_val
    loc_slider.value        = loc_val
    f1.arrow_source.data    = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    f2.arrow_source.data    = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    f2.tri.data             = dict(x = [], y = [], size = [])
    f1.e_s.data             = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    f2.e_s.data             = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    f1.pts.data             = dict(x = [], y = [] )
    #f1.tri.data             = dict(x = [0.1,0.8], y = [0.1,0.1], size = [tri_size,tri_size])
    f1.tri.data             = dict(x = [], y = [], size = [])
    f2.set_param(loc_val)
    f2.set_mag(mag_val)

def clearf2():
    '''Clears the f2 frame'''
    f2.pts.data             = dict(x = [], y = [] )

button.on_click(button_fun)
rbutton.on_click(init)
rbutton.on_click(clearf2)
loc_slider.on_change('value', update_fun)
mag_slider.on_change('value', update_fun)

################################################################################
###Main section
################################################################################

create_orig(orig)                                                               #Stationary frame is created

################################################################################
###Plot Section
################################################################################

#Plot constants
abshift = 0.02                                                                  #this is the size of the end-lines of the scale parameters a and b
xb      = -0.015                                                                #xb shift used in a and b creation
f1color = "#0065BD"                                                             #TUM approved color for F1 (blue)
f2color = "#E37222"                                                             #TUM approved color for F2 (orange)

########Main PLot:
plot = Figure(tools = "", x_range=(plotx0,plotxf),
        y_range=(ploty0,plotyf),plot_width=1000, plot_height=1000)
#Plot properties:
plot.axis.visible = True
plot.outline_line_width = 7
plot.outline_line_alpha = 0.3
plot.outline_line_color = "Black"
plot.title.text_color = "black"
plot.title.text_font_style = "bold"
plot.title.align = "center"
#########

#Plot of frames
plot.line(x='x', y='y', source=orig.pts, color="grey",line_width=3)             #Original stationary frame
plot.line(x='x', y='y', source=f1.pts, color=f1color,line_width=5)              #Frame 1
plot.line(x='x', y='y', source=f2.pts, color=f2color,line_width=5)              #Frame 2
plot.line(x='x', y='y', source=t_line, color="Black",line_width=5)              #Black line under frame righthandside

###Dashed Lines:
plot.line(x='x', y='y', source=f1.dline, color="Black",
        line_width=2,line_dash = 'dashed',line_alpha = 0.3)                     #Dashed lines that follow load arrow
plot.line(x='x', y='y', source=f2.dline, color="Black",
        line_width=2,line_dash = 'dashed',line_alpha = 0.3)

#dashed line that follows the deformations:
plot.line(x = 'x1' , y = 'y1',source = f1.wdline, color="Black",
        line_width=2,line_dash = 'dashed',line_alpha = 0.3)
plot.line(x = 'x2' , y = 'y2',source = f1.wdline, color="Black",
        line_width=2,line_dash = 'dashed',line_alpha = 0.3)
plot.line(x = 'x1' , y = 'y1',source = f2.wdline, color="Black",
        line_width=2,line_dash = 'dashed',line_alpha = 0.3)
plot.line(x = 'x2' , y = 'y2',source = f2.wdline, color="Black",
        line_width=2,line_dash = 'dashed',line_alpha = 0.3)

#creation of the a and b scale reference things:
plot.multi_line( [ [orig.x0, orig.xf],[orig.x0,orig.x0],[orig.xf,orig.xf] ],
        [ [0,0] ,[0-abshift,0+abshift] , [0-abshift,0+abshift] ],
        color=["black", "black","black"], line_width=10)
plot.multi_line( [ [xb,xb],[xb-abshift,xb+abshift],[xb-abshift,xb+abshift] ],
        [ [orig.y0,orig.yf], [orig.y0,orig.y0], [orig.yf,orig.yf] ],
        color=["black", "black","black"], line_width=10)

#Frame bases:
plot.triangle(x='x', y='y', size = 'size', source= default,color="grey", line_width=2)
plot.triangle(x='x', y='y', size = 'size', source= f1.tri,color=f1color, line_width=2)
plot.triangle(x='x', y='y', size = 'size', source= f2.tri,color=f2color, line_width=2)



#######labels
labels1 = LabelSet(x='x', y='y', text='name', level='glyph',
              x_offset=0, y_offset=0, source=f1.label, text_color=f1color,
              text_font_size = '16pt',  render_mode='canvas')
labels2 = LabelSet(x='x', y='y', text='name', level='glyph',
              x_offset=0, y_offset=0, source=f2.label,text_color=f2color,
              text_font_size = '16pt', render_mode='canvas')
labelsn1 = LabelSet(x='x', y='y', text='name', level='glyph',
              x_offset=0, y_offset=-20, source=f1.dlabel,text_color=f2color,
              text_font_size = '10pt', render_mode='canvas')
labelsn2 = LabelSet(x='x', y='y', text='name', level='glyph',
              x_offset=0, y_offset=-20, source=f2.dlabel,text_color=f2color,
              text_font_size = '10pt', render_mode='canvas')
labelsw1 = LabelSet(x=, y=0.0, text="(wij)n1", level='glyph',
              x_offset=10, y_offset=10,text_color=f2color,
              text_font_size = '12pt', render_mode='canvas')

absource = ColumnDataSource(dict(x=[ (orig.x0+orig.xf)/2,
        (0-0.05)], y=[ (0-0.05), (orig.y0+orig.yf)/2 ], text=['a','b']))
        abtext_glyph = Text( x='x' , y='y', text='text' ,text_color="Black",
        text_font_size="16pt",text_font_style = "bold")

########

#######Arrows:
#P arrow:
p1_arrow_glyph = Arrow(end=NormalHead(line_color=f1color,line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f1.arrow_source,line_color=f1color)
p2_arrow_glyph = Arrow(end=NormalHead(line_color=f2color,line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f2.arrow_source,line_color=f2color)

#e arrow:
e1_arrow_glyph = Arrow(end=OpenHead(line_color=f1color,line_width= 3, size=6,line_alpha = 0.5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= 4, source=f1.e_s,line_color=f1color,line_alpha = 0.5)
e2_arrow_glyph = Arrow(end=OpenHead(line_color=f2color,line_width= 3, size=6,line_alpha = 0.5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= 4, source=f2.e_s,line_color=f2color,line_alpha = 0.5)

#F1 w arrow
w11_arrow_glyph = Arrow(end=OpenHead(line_color=f1color,line_width= 3, size=6,line_alpha = 0.5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= 4, source=f1.w1,line_color=f1color,line_alpha = 0.4)
w12_arrow_glyph = Arrow(end=OpenHead(line_color=f1color,line_width= 3, size=6,line_alpha = 0.5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= 4, source=f1.w2,line_color=f1color,line_alpha = 0.4)

#F2 w arrow
w21_arrow_glyph = Arrow(end=OpenHead(line_color=f2color,line_width= 3, size=6,line_alpha = 0.5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= 4, source=f2.w1,line_color=f2color,line_alpha = 0.4)
w22_arrow_glyph = Arrow(end=OpenHead(line_color=f2color,line_width= 3, size=6,line_alpha = 0.5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= 4, source=f2.w2,line_color=f2color,line_alpha = 0.4)
########


########Layout adding
#Adding the arrows and labels to the plot:
plot.add_layout(p1_arrow_glyph)
plot.add_layout(p2_arrow_glyph)
plot.add_layout(e1_arrow_glyph)
plot.add_layout(e2_arrow_glyph)
plot.add_layout(w11_arrow_glyph)
plot.add_layout(w12_arrow_glyph)
plot.add_layout(w21_arrow_glyph)
plot.add_layout(w22_arrow_glyph)
plot.add_glyph(absource,abtext_glyph)
plot.add_layout(labels1)
plot.add_layout(labels2)
plot.add_layout(labelsn1)
plot.add_layout(labelsn2)
#plot.add_layout(labelsw1)
#plot.add_layout(labelsw2)
#########


################################################################################
###Send to the browser
################################################################################
#curdoc().add_root( row(column(f1.mag_slider,f1.loc_slider,f2.mag_slider,f2.loc_slider, toggle),plot ) )
curdoc().add_root( column(plot,row(mag_slider, loc_slider),button,rbutton) )
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
