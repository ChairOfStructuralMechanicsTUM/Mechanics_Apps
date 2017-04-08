#main file:

from bokeh.plotting import Figure, output_file , show
from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, Arrow
from bokeh.layouts import column, row
from bokeh.io import curdoc
import numpy as np
import math

#Beam Properties:
resol = 100.0
x0 = 0                  #starting value of beam
xf = 10                 #ending value of beam
E  = 200.0e1            #modulus of elasticity
I  = 50                 #moment of inertia
length  = xf-x0              #length of beam
plot_source = dict(x = np.linspace(x0,xf,resol), y = np.ones(resol) * 0 )
p_mag = 100.0           #initialize the p force
p_magi = 100.0
#Sources:
#Moment Source:
mom_source = ColumnDataSource(data=dict(x=[] , y=[]))
#Shear Source:
shear_source = ColumnDataSource(data=dict(x=[] , y=[]))
#Arrow Sources:
p_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
f2_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
f1_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
#label_source:
labels_source = ColumnDataSource(data=dict(x=[] , y=[],name = []))
#Position 2 Triangle source:
f2_triangle_source = ColumnDataSource(data=dict(x= [], y= [], size = []))
#Sliders:
p_loc_slide= Slider(title="Lastposition",value= xf/2,start = x0, end = xf, step = 1/resol)
p_mag_slide = Slider(title="Lastamplitude", value=p_mag, start=-2*p_mag, end=2*p_mag, step=1)
f2_loc_slide = Slider(title="Lagerposition",value=xf,start = x0, end = xf, step = 1/resol)


#FUNCTION: Calculate Force at Support 1
def Fun_F(p_mag,b,l):
    f1_mag = -1.0 * (p_mag *b) / l
    return f1_mag

#FUNCTION: Calculation of Max MOMENT
def Fun_Moment(p,a,b,l):
    mom_max = (p * a * b ) / l
    #x is 0, pcoord, f2_coord
    #y is 0, mom_max, 0
    return mom_max

#FUNCTION: Update moment plot:
def Fun_Update(attrname, old, new):
    a = p_loc_slide.value
    b = f2_loc_slide.value - p_loc_slide.value
    p_coord = p_loc_slide.value
    p_mag = p_mag_slide.value
    f2_coord = f2_loc_slide.value
    l = f2_coord
    f1_mag = Fun_F(p_mag_slide.value,b,l)
    f2_mag = Fun_F(p_mag_slide.value,a,l)
    move_tri = -0.25
    f2_triangle_source.data = dict(x = [0.0,f2_loc_slide.value], y = [0+move_tri, 0+move_tri], size = [20,20])

    #moment and shear:
    m_max = Fun_Moment(p_mag_slide.value,a,b,l)
    if (l >= a):
        mom_source.data = dict(x=[0,a,l] , y=[0,m_max,0])
        shear_source.data = dict(x=[0,a,a,l], y=[-f1_mag,-f1_mag,f2_mag,f2_mag])
    else:
        mom_source.data = dict(x=[0,l,a] , y=[0,m_max,0])
        shear_source.data = dict(x=[0,l,l,a], y=[-f1_mag,-f1_mag,p_mag,p_mag])

    #p_arrow and labels:
    if (p_mag==0):
        p_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        labels_source.data = dict(x = [] , y = [], name = ['F','A','B'])

    elif (p_mag<0):
        p_arrow_source.data = dict(xS= [p_coord], xE= [p_coord], yS= [1-(p_mag/200.0)], yE=[1], lW = [abs(p_mag/40.0)] )
        labels_source.data = dict(x = [p_coord,0,f2_coord] , y = [1,move_tri,move_tri],name = ['F','A','B'])

    else:
        p_arrow_source.data = dict(xS= [p_coord], xE= [p_coord], yS= [-1-(p_mag/200.0)], yE=[-1], lW = [abs(p_mag/40.0)] )
        labels_source.data = dict(x = [p_coord,0,f2_coord] , y = [-1,move_tri,move_tri],name = ['F','A','B'])

    #f1_arrow:
    #if (f1_mag==0):
        #f1_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    if (f1_mag<=-p_magi):
        f1_arrow_source.data = dict(xS= [0], xE= [0], yS= [1-(f1_mag/200.0)], yE=[0.8], lW = [6])
    elif ( f1_mag>-p_magi ) & ( f1_mag<=0 ):
        f1_arrow_source.data = dict(xS= [0], xE= [0], yS= [1-(f1_mag/200.0)], yE=[0.8], lW = [abs(f1_mag/40.0)])
    elif (f1_mag > 0) & ( f1_mag < p_magi ):
        f1_arrow_source.data = dict(xS= [0], xE= [0], yS= [-1-(f1_mag/200.0)], yE=[-0.8], lW = [abs(f1_mag/40.0)] )
    else:
        f1_arrow_source.data = dict(xS= [0], xE= [0], yS= [-1-(f1_mag/200.0)], yE=[-0.8], lW = [6] )

    #f2_arrow:
    #if (f2_mag==0):
    #    f2_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[])
    if (f2_mag<=-p_magi):
        f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yS= [1-(f2_mag/200.0)], yE=[0.8], lW = [6])
    elif (f2_mag > -p_magi) & (f2_mag <= 0.0):
        f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yS= [1-(f2_mag/200.0)], yE=[0.8], lW = [abs(f2_mag/40.0)])
    elif (f2_mag > 0) & ( f2_mag < p_magi ):
        f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yS= [-1-(f2_mag/200.0)], yE=[-0.8], lW = [abs(f2_mag/40.0)])
    else:
        f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yS= [-1-(f2_mag/200.0)], yE=[-0.8], lW = [6])

    #print labels_source.data


#initial function:
def initial():
    Fun_Update(None,None,None)

##########Plotting##########

###Main Plot:
plot = Figure(title="Doppeltgelagerter Balken und Einzellast", x_range=(x0-.5,xf+.5), y_range=(-2.5,2.5))
plot.line(x='x', y='y', source=plot_source, color='blue',line_width=20)
plot.triangle(x='x', y='y', size = 'size', source= f2_triangle_source,color="#99D594", line_width=2)
plot.axis.visible = False
plot.outline_line_width = 7
plot.outline_line_alpha = 0.3
plot.outline_line_color = "Black"
labels = LabelSet(x='x', y='y', text='name', level='glyph',
              x_offset=5, y_offset=-30, source=labels_source, render_mode='canvas')


###Plot with moment and shear:
plot1 = Figure(title="Biegemoment, Querkraft", x_range=(x0,xf), y_range=(-600,600), width = 400, height = 200)
plot1.line(x='x', y='y', source=mom_source, color='blue',line_width=5)
plot1.line(x='x', y='y', source=shear_source, color='red',line_width=5)
plot1.axis.visible = False

###arrow plotting:
#P arrow:
p_arrow_glyph = Arrow(end=OpenHead(line_color="red",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=p_arrow_source,line_color="red")
#Position 2 arrow:
f2_arrow_glyph = Arrow(end=OpenHead(line_color="blue",line_width= 4,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_width = "lW", source=f2_arrow_source,line_color="blue")
#Position 1 arrow:
f1_arrow_glyph = Arrow(end=OpenHead(line_color="blue",line_width= 4,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width = "lW", source=f1_arrow_source,line_color="blue" )

###add layouts:
plot.add_layout(labels)
plot.add_layout(p_arrow_glyph)
plot.add_layout(f2_arrow_glyph)
plot.add_layout(f1_arrow_glyph)

###on_change:

p_loc_slide.on_change('value', Fun_Update)
p_mag_slide.on_change('value', Fun_Update)
f2_loc_slide.on_change('value',Fun_Update)

#main:
initial()

curdoc().add_root(row(column(p_loc_slide,p_mag_slide,f2_loc_slide,plot1),plot))
