from bokeh.plotting import Figure, output_file , show
from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, NormalHead, Arrow
from bokeh.layouts import column, row, widgetbox
from bokeh.models.widgets import Button
from bokeh.io import curdoc
import numpy as np
from os.path import dirname, join, split


#main1
#conversion of java code


class Frame(object):
    def __init__(self,name):
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
        self.arrow_source   = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
        self.e_s            = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
        self.tri            = ColumnDataSource(data=dict(x= [], y= [], size = []))
        self.seg            = ColumnDataSource(data=dict(x0=[], x1=[], y0=[], y1=[]))
        self.t_line         = ColumnDataSource(data=dict(x=[], y=[]))
        self.label          = ColumnDataSource(data=dict(x=[] , y=[], name = []))

        #self.mag_slider     = Slider(title= self.name + " Kraftbetrag", value=self.mag_val, start=self.mag_start, end=self.mag_end, step=1)
        #self.loc_slider     = Slider(title= self.name + " Kraftposition", value=self.loc_val, start=self.loc_start, end=self.loc_end, step=1)

    def set_mag(self, a):
        self.p_mag = a
    def set_param(self, a):
        self.p_loc = a
    def get_mag(self):
        return self.p_mag
    def get_param(self):
        return self.p_loc




#some constants
a           = 0.5
b           = 0.7
FScale      = 150.0
offsetKraft = 0.08
tri_size    = 30
changer     = 0
shift       = 0.01
shift2      = 0.015

#Arrow Sources:
#p_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
arr_scal        = 450.0
arr_lw          = 20.0
ground          = 0.07
orig            = Frame("o")
f1              = Frame("F1")
f2              = Frame("F2")
f1.tri.data     = dict(x = [0.1,0.8], y = [0.1,0.1], size = [tri_size,tri_size])
#seg             = dict(x0=[0.095,0.097,0.099,0.101,0.103,0.105],
#                x1=[0.095+shift,0.097+shift,0.099+shift,0.101+shift,0.103+shift,0.105+shift],
#                y0=[0.09]*5, y1=[0.088]*5)
t_line          = dict(x=[0.7,0.9], y=[ground,ground])

#sliders:
mag_start   = -100
mag_end     = 100
mag_val     = 0
mag_slider  = Slider(title="Kraftbetrag", value=mag_val, start=mag_start, end=mag_end, step=1)

#Toggle button:
button = Button(label="Save", button_type="success")
rbutton = Button(label="Reset", button_type="success")
loc_start = 0
loc_end = 100
loc_val = 50
loc_slider = Slider(title="Kraftposition", value=loc_val, start=loc_start, end=loc_end, step=1)
#p2loc_slider = Slider(title=f2.name + " Kraftposition", value=loc_val, start=loc_start, end=loc_end, step=1)


def create_orig(o):
    x = [o.x0,o.x0,o.xf,o.xf]
    y = [o.y0,o.yf,o.yf,o.y0]
    o.pts.data = dict(x = x, y = y )


def create_prof(f):
    paramInt = f.get_param()
    i = f.get_mag()
    if int(paramInt) < 30:
        side1(f,paramInt,i)

    elif (int(paramInt)> 30) & (int(paramInt) < 70) :
        side2(f,paramInt,i)

    elif  int(paramInt) > 70:
        side3(f,paramInt,i)

def side1(f,paramInt,i):
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
    if i<0:
        f.arrow_source.data = dict(xS= [0.12-i/arr_scal], xE= [0.12],
        yS= [0.1 + paramInt*(1.0/60)], yE=[0.1+ paramInt*(1.0/60)], lW = [abs(i/arr_lw)] )

        f.label.data = dict(x = [0.12-i/arr_scal], y = [0.1+ paramInt*(1.0/60)], name = [f.name])

    elif i>0:
        f.arrow_source.data = dict(xS= [0.08-i/arr_scal], xE= [0.08],
        yS= [0.1 + paramInt*(1.0/60)], yE=[0.1+ paramInt*(1.0/60)], lW = [abs(i/arr_lw)] )

        f.label.data = dict(x = [0.08-i/arr_scal], y = [0.1+ paramInt*(1.0/60)], name = [f.name])


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
    f.pts.data = dict(x = x, y = y )

def side2(f,paramInt,i):
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
    d7 = i / FScale

    localDouble = []

    #create a localdouble Point2d variable

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

def create_shift(f1, f2):
    paramInt1 = f1.get_param()
    paramInt2 = f2.get_param()

    localDouble1 = compute_shift(paramInt1,paramInt2, f2.get_mag())
    localDouble2 = compute_shift(paramInt2,paramInt1, f2.get_mag())

    d2 = 0
    d1 = 0
    sclr = 10
    if (paramInt1 < 30):
        d2 = paramInt1 / 30.0 * 0.5 + 0.1
        d1 = 0.1

        f1.e_s.data = dict(xS= [ d1 ], xE= [d1 + localDouble1[0]],
        yS= [d2], yE=[d2], lW = [abs(localDouble1[0]*sclr) ] )

    elif ((30 <= paramInt1) & (paramInt1 <= 70)):
        d1 = (paramInt1 - 30) / 40.0 * 0.7 + 0.1
        d2 = 0.6

        f1.e_s.data = dict(xS= [ d1 ], xE= [d1],
        yS= [d2 + localDouble1[1] ], yE=[d2], lW = [abs(localDouble1[1]*sclr) ] )

    elif (paramInt1 > 70):
        d1 = 0.8
        d2 = 0.6 - (paramInt1 - 70) / 30.0 * 0.5

        f1.e_s.data = dict(xS= [ d1], xE= [d1 + localDouble1[0] ],
        yS= [d2], yE=[d2], lW = [ abs(localDouble1[0]*sclr ) ] )


    if (paramInt2 < 30):
        d2 = paramInt2 / 30.0 * 0.5 + 0.1
        d1 = 0.1
        f2.e_s.data = dict(xS= [ d1 + localDouble2[0] ], xE= [d1],
        yS= [d2], yE=[d2], lW = [abs(localDouble2[0]*sclr ) ] )
    elif((30 <= paramInt2) & (paramInt2 <= 70)):
        d1 = (paramInt2 - 30) / 40.0 * 0.7 + 0.1
        d2 = 0.6
        f2.e_s.data = dict(xS= [ d1 ], xE= [d1],
        yS= [d2], yE=[d2 + localDouble1[1] ], lW = [abs(localDouble1[1]*sclr) ] )
    elif(paramInt2 > 70):
        d1 = 0.8
        d2 = 0.6 - (paramInt2 - 70) / 30.0 * 0.5

        f2.e_s.data = dict(xS= [ d1 ], xE= [d1 + localDouble2[0]],
        yS= [d2], yE=[d2], lW = [abs(localDouble2[0] *sclr) ] )


def update_fun(attr,old,new):
    if changer == 0:
        f1.set_param(loc_slider.value)
        f1.set_mag(mag_slider.value)
        create_prof(f1)
        f1.tri.data = dict(x = [0.1,f1.pts.data["x"][-1]], y = [0.1,f1.pts.data["y"][-1]], size = [tri_size,tri_size])
    elif changer != 0:
        f1.tri.data = dict(x = [], y = [], size = [])
        f2.set_param(loc_slider.value)
        f2.set_mag(mag_slider.value)
        create_prof(f2)
        create_shift(f1,f2)
        f2.tri.data = dict(x = [0.1,f2.pts.data["x"][-1]], y = [0.1,f2.pts.data["y"][-1]], size = [tri_size,tri_size])


def button_fun():
    global changer
    changer = 1
    f1.set_param(loc_slider.value)
    f1.set_mag(mag_slider.value)
    create_prof(f1)
    create_shift(f1,f2)


#Force 1 sliders:
#f1.loc_slider.on_change('value', update_fun)
#f1.mag_slider.on_change('value', update_fun)

loc_slider.on_change('value', update_fun)
mag_slider.on_change('value', update_fun)

#Force 2 sliders:
#f2.loc_slider.on_change('value', update_fun)
#f2.mag_slider.on_change('value', update_fun)





def init():
    global changer
    changer                 = 0
    f1.label.data           = dict(x=[0.45] , y=[0.65], name = ["F1"])
    f2.label.data           = dict(x=[] , y=[], name = [])
    mag_slider.value        = mag_val
    loc_slider.value        = loc_val
    f1.arrow_source.data    = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    f2.arrow_source.data    = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    f2.tri.data             = dict(x = [], y = [], size = [])
    f1.e_s.data             = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    f2.e_s.data             = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    f1.tri.data             = dict(x = [0.1,0.8], y = [0.1,0.1], size = [tri_size,tri_size])

def clearf2():
    f2.pts.data             = dict(x = [], y = [] )


button.on_click(button_fun)
rbutton.on_click(init)
rbutton.on_click(clearf2)

init()
create_orig(orig)

ps = 0.3
plot = Figure(tools = "",title="Maxwell",title_location = "above", x_range=(0.1-ps,0.8+ps), y_range=(0.0,1.0))
plot.line(x='x', y='y', source=orig.pts, color='Black',line_width=3)
plot.line(x='x', y='y', source=f1.pts, color="#808080",line_width=5)
plot.line(x='x', y='y', source=f2.pts, color="#E37222",line_width=5)
plot.line(x='x', y='y', source=t_line, color="Black",line_width=5)
plot.triangle(x='x', y='y', size = 'size', source= f1.tri,color="#808080", line_width=2)
plot.triangle(x='x', y='y', size = 'size', source= f2.tri,color="#E37222", line_width=2)
plot.axis.visible = False
plot.outline_line_width = 7
plot.outline_line_alpha = 0.3
plot.outline_line_color = "Black"
plot.title.text_color = "black"
plot.title.text_font_style = "bold"
plot.title.align = "center"


labels1 = LabelSet(x='x', y='y', text='name', level='glyph',
              x_offset=0, y_offset=0, source=f1.label, render_mode='canvas')
labels2 = LabelSet(x='x', y='y', text='name', level='glyph',
              x_offset=0, y_offset=0, source=f2.label, render_mode='canvas')

#P arrow:
p1_arrow_glyph = Arrow(end=NormalHead(line_color="#0065BD",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f1.arrow_source,line_color="#0065BD")
p2_arrow_glyph = Arrow(end=NormalHead(line_color="#E37222",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f2.arrow_source,line_color="#E37222")
e1_arrow_glyph = Arrow(end=OpenHead(line_color="#A2AD00",line_width= 1, size=7),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f1.e_s,line_color="#A2AD00")
e2_arrow_glyph = Arrow(end=OpenHead(line_color="#A2AD00",line_width= 1, size=7),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f2.e_s,line_color="#A2AD00")


plot.add_layout(p1_arrow_glyph)
plot.add_layout(p2_arrow_glyph)
plot.add_layout(e1_arrow_glyph)
plot.add_layout(e2_arrow_glyph)
plot.add_layout(labels1)
plot.add_layout(labels2)



#curdoc().add_root( row(column(f1.mag_slider,f1.loc_slider,f2.mag_slider,f2.loc_slider, toggle),plot ) )
curdoc().add_root( column(plot,row(mag_slider, loc_slider),button,rbutton) )
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
