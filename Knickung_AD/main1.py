#main1
#Knickung (buckling) animation:
from bokeh.plotting import Figure, output_file , show
from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, Arrow, NormalHead
from bokeh.layouts import column, row
from bokeh.io import curdoc
import numpy as np
import math

#constant numbers:
resol           = 100                #resolution of beams
E               = 200.0e1            #modulus of elasticity
I               = 50                 #moment of inertia
f_end           = 1.5         #last slider value
punktezahl      = 30
factor          = 1.2
xf              = 0.0
fenster         = 16
xstart          = 0.02 * fenster
zstart          = 0.1 * fenster

class Column(object):
    def __init__(self,name,h,fcrit):
        self.pts        = ColumnDataSource(data=dict(x=[] , y=[]))
        self.h          = h #change this
        self.hi         = h
        self.name       = name
        self.deflection = 0
        self.fcrit      = fcrit
        self.xstart     = 0
        self.floor      = ColumnDataSource(data=dict(x0 = [] , x1 =[], y0 = [], y1 = []))
        self.arrow      = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
        self.labels     = ColumnDataSource(data=dict(x=[] , y=[],name = []))

    def fun_ground(self):
        x0 = []
        xf = []
        y0 = []
        yf = []
        i0 = drange(self.xstart-2,self.xstart+2,0.4)
        for i in i0:
            x0.append(i)
            xf.append(i+0.2)
            y0.append(-2)
            yf.append(0)
        print x0
        print yf
        self.floor.data = dict(x0 = x0, x1 = xf, y0 = y0, y1 = yf)

    def fun_arrow(self):
        xS = [self.xstart]
        xE = [self.xstart]
        yS = [self.h + 1.8*f_end ]
        yE = [self.h + 1.8*f_end - (weight_slide.value/1.9)]
        lW = [weight_slide.value*3]
        self.arrow.data = dict(xS = xS, xE = xE , yS = yS, yE = yE, lW = lW)

    def fun_labels(self):
        x = [self.xstart, self.xstart + 1]
        y = [self.h + 1.8*f_end + 2, 3]
        name = ["F",self.name]
        self.labels = dict(x = x, y = y, name = name)





weight_slide = Slider(title="Force", value=0, start=0, end=f_end, step=0.05)


def drange(start,stop,step):
    r = start
    while r < stop:
        yield r
        r += step

#create 4 functions that calculate the buckling
#create 4 objects called beam

col1 = Column("Free-Fixed",3,0.9)                        #beam: "Free-Fixed" Column
col2 = Column("Pinned-Pinned",2.0*col1.h,1.0*col1.fcrit)        #beam: "Fixed-Fixed" Column
col3 = Column("Pinned-Fixed",1.43*col2.h,1.0*col2.fcrit)       #beam: "Fixed-Fixed" Column
col4 = Column("Fixed-Fixed",2.0*col2.h,1.0*col2.fcrit)        #beam: "Fixed-Fixed" Column

#where the columns start on the graph:
col1.xstart = xstart
col2.xstart = xstart + 4.0
col3.xstart = xstart + 8.0
col4.xstart = xstart + 12.0
#col1.fun_create()
#col2.fun_create()
#col3.fun_create()
#col4.fun_create()



def fun_col1(paramFloat1,paramFloat2):
    x = []
    y = []
    d3 = col1.h/ punktezahl
    #this.Stab_I.reset()
    d1 = paramFloat1
    d2 = paramFloat2
    x0 = [d1]
    y0 = [d2]
    i0 = drange(0,col1.h+(d3/2),d3)
    for d4 in i0:
        d2 = d4
        d1 = col1.deflection * ( np.cos( np.pi * d2 / (2.0*col1.h) ) -1 )
        x.append(d1+paramFloat1)
        y.append(d2+paramFloat2)
    col1.pts.data = dict(x = x0 + x, y = y0 + y)

def fun_col2(paramFloat1,paramFloat2):
    x  = []
    y  = []
    d3 = col2.h/ punktezahl
    #this.Stab_I.reset()
    d1 = paramFloat1
    d2 = paramFloat2
    x0 = [d1]
    y0 = [d2]
    i0 = drange(0,col2.h+(d3/2),d3)

    for d4 in i0:
        d2 = d4
        d1 = col2.deflection * ( np.sin( np.pi * d2 / (col2.h) ) )
        x.append(d1+paramFloat1)
        y.append(d2+paramFloat2)

    col2.pts.data = dict(x = x0 + x, y = y0 + y)

def fun_col3(paramFloat1,paramFloat2):
    global Druckkraft
    x  = []
    y  = []
    d3 = col3.h / punktezahl
    d4 = 4.4 / col3.h
    #Stab_III.reset()
    d1 = paramFloat1
    d2 = paramFloat2
    x0 = [d1]
    y0 = [d2]
    i0 = drange(0,col3.h+(d3/2.0),d3)

    if (Druckkraft > 0.0):
        for d5 in i0:
            d2 = d5
            d1 = col3.deflection * (np.cos(d4*d2) - ( np.sin(d4*d2)/(d4*col3.h) ) + (d2/col3.h) - 1 )
            x.append(d1+paramFloat1)
            y.append(d2+paramFloat2)

    col3.pts.data = dict(x = x0 + x + [paramFloat1] , y = y0 + y + [paramFloat2 + col3.h])

def fun_col4(paramFloat1,paramFloat2):
    global Druckkraft
    x  = []
    y  = []
    d3 = (col4.h / (punktezahl-1))
    d4 = (col4.h / 4)
    d5 = (2.0 * d4)
    d6 =( 3.0 * d4 )

    #this.Stab_IV.reset()
    d1 = paramFloat1
    d2 = paramFloat2
    x0 = [d1]
    y0 = [d2]
    i0 = drange(0,d4,d3)
    i1 = drange(d4,d6,d3)
    i2 = drange(d6,col4.h,d3)
    if ( Druckkraft > 0.0):
        for d7 in i0:
            d2 = d7
            d1 = col4.deflection * (1.0 - np.cos(np.pi * (d2/d5) ) )
            x.append(d1+paramFloat1)
            y.append(d2+paramFloat2)
        for d7 in i1:
            d2 = d7
            d1 = col4.deflection * (np.sin(np.pi * (d2-d4) / (col4.h - d5) ) +1.0)
            x.append(d1+paramFloat1)
            y.append(d2+paramFloat2)
        for d7 in i2:
            d2 = d7
            d1 = col4.deflection * (1.0 - np.cos(np.pi*(col4.h-d2)/d5))
            x.append(d1+paramFloat1)
            y.append(d2+paramFloat2)

    col4.pts.data = dict(x = x0 + x + [paramFloat1] , y = y0 + y + [paramFloat2 + col4.h-0.05])

def fun_update(attr,old,new):
    #print col1.floor
    global Druckkraft
    Druckkraft = weight_slide.value
    col1.h -= 5.0E-4
    col2.h -= 5.0E-4
    col3.h -= 5.0E-4
    col4.h -= 5.0E-4

    if(Druckkraft > col1.fcrit):
        col1.deflection = ( factor * np.sqrt(np.sqrt(Druckkraft/col1.fcrit)-1) )
        col1.h         -= 0.005
    if(Druckkraft > col2.fcrit):
        col2.deflection = ( factor * np.sqrt(np.sqrt(Druckkraft/col2.fcrit)-1) )
        col2.h         -= 0.005
    if(Druckkraft > col3.fcrit):
        col3.deflection = ( factor * np.sqrt(np.sqrt(Druckkraft/col3.fcrit)-1) )
        col2.h         -= 0.005
    if(Druckkraft > col4.fcrit):
        col4.deflection = ( factor * np.sqrt(np.sqrt(Druckkraft/col4.fcrit)-1) )
        col4.h         -= 0.005

    fun_col1(col1.xstart,zstart)
    fun_col2(col2.xstart,zstart)
    fun_col3(col3.xstart,zstart)
    fun_col4(col4.xstart,zstart)
    col1.fun_arrow()
    col2.fun_arrow()
    col3.fun_arrow()
    col4.fun_arrow()
    col1.fun_labels()
    col2.fun_labels()
    col3.fun_labels()
    col4.fun_labels()




plot = Figure(title="Knickung", x_range=(-2,fenster), y_range=(0,fenster))
plot.line(x='x', y='y', source = col1.pts, color='blue',line_width=5)
plot.line(x='x', y='y', source = col2.pts, color='blue',line_width=5)
plot.line(x='x', y='y', source = col3.pts, color='blue',line_width=5)
plot.line(x='x', y='y', source = col4.pts, color='blue',line_width=5)

plot.segment(x0='x0', y0='y0', x1='x1', y1='y1',source = col1.floor)#, color="black",line_width=5)
#plot.segment(x0 = col1.floor['x0'] ,x1 = col1.floor['x1'] , y0 = col1.floor['y0'] ,y1 = col1.floor['y1'])
#plot.segment(x0 = col1.floor['x0'] ,x1 = col1.floor['x1'] , y0 = col1.floor['y0'] ,y1 = col1.floor['y1'])
col1_a = Arrow(end=NormalHead(line_color="#A2AD00",line_width= 4, size=10),
x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=col1.arrow,line_color="#A2AD00")
col2_a = Arrow(end=NormalHead(line_color="#A2AD00",line_width= 4, size=10),
x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=col2.arrow,line_color="#A2AD00")
col3_a = Arrow(end=NormalHead(line_color="#A2AD00",line_width= 4, size=10),
x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=col3.arrow,line_color="#A2AD00")
col4_a = Arrow(end=NormalHead(line_color="#A2AD00",line_width= 4, size=10),
x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=col4.arrow,line_color="#A2AD00")
#labels = LabelSet(x='x', y='y', text='name', level='glyph',
#              x_offset=0, y_offset=0, source=labels, render_mode='canvas')
labels = LabelSet(x=[0,1], y=[0,3], text=["hsdf","isdfs"], level='glyph',
              x_offset=0, y_offset=0, render_mode='canvas')
#labels2 = LabelSet(x='x', y='y', text='name', level='glyph',
#              x_offset=5, y_offset=-30, source=col2.labels, render_mode='canvas')
#labels3 = LabelSet(x='x', y='y', text='name', level='glyph',
#              x_offset=5, y_offset=-30, source=col3.labels, render_mode='canvas')
#labels4 = LabelSet(x='x', y='y', text='name', level='glyph',
#              x_offset=5, y_offset=-30, source=col4.labels, render_mode='canvas')
#labels = LabelSet(x='x', y='y', text='name', level='glyph',
#              x_offset=5, y_offset=-30, source=col1.fun_labels, render_mode='canvas')

#plot.axis.visible = False
#plot.grid.visible = False
plot.outline_line_width = 7
plot.outline_line_alpha = 0.3
plot.outline_line_color = "Black"


weight_slide.on_change('value', fun_update)
#p_arrow_glyph = Arrow(end=OpenHead(line_color="#A2AD00",line_width= 4, size=10),
#    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=p_arrow_source,line_color="#A2AD00")
plot.add_layout(col1_a)
plot.add_layout(col2_a)
plot.add_layout(col3_a)
plot.add_layout(col4_a)
plot.add_layout(labels)
#plot.add_layout(labels2)
#plot.add_layout(labels3)
#plot.add_layout(labels4)


curdoc().add_root(row(column(weight_slide),plot))
