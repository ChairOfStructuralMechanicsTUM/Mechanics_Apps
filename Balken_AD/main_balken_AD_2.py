from bokeh.plotting import Figure, output_file , show
from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, Arrow
from bokeh.layouts import column, row
from bokeh.io import curdoc
import numpy as np
import math


#Beam Properties:
resol = 100.0
x0 = 0             #starting value of beam
xf = 10            #ending value of beam
E  = 200.0e1        #modulus of elasticity
I  = 50          #moment of inertia
l  = xf-x0         #length of beam
plot_source = dict(x = np.linspace(x0,xf,resol), y = np.ones(resol) * 0 )

#Concentrated Load "P" properties:
p_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[]))
f2_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[]))
f1_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[]))

p_mag = 100.0 #initialize the p force

#Sliders:
p_loc_slide= Slider(title="Concentrated Load Location",value= xf/2,start = x0, end = xf, step = 1/resol)
p_mag_slide = Slider(title="Concentrated Load Magnitude", value=0, start=-2*p_mag, end=2*p_mag, step=1)
f2_loc_slide = Slider(title="Support 2 Location",value=xf,start = x0, end = xf, step = 1/resol)


#FUNCTION: Calculate Force at Support 1
def Fun_F(p_mag,b):
    f1_mag = (p_mag *b) / l
    return f1_mag

#FUNCTION: Calculation of MOMENT
#def Fun_Moment():
    #

#FUNCTION: Calculation of Shear
#def Fun_Shear(a_mag,b_mag,f2_loc, p_loc):

    #


#FUNCTION: Update P arrow size and location:
def Fun_UpdateParrow(attrname, old, new):
    p_coord = p_loc_slide.value
    p_mag = p_mag_slide.value

    if (p_mag==0):
        p_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[])
    elif (p_mag<0):
        p_arrow_source.data = dict(xS= [p_coord], xE= [p_coord], yS= [1-(p_mag/200.0)], yE=[1] )
    else:
        p_arrow_source.data = dict(xS= [p_coord], xE= [p_coord], yS= [-1-(p_mag/200.0)], yE=[-1] )

#FUNCTION: Update f1 arrow size and location:
def Fun_Updatef1arrow(attrname, old, new):
    b = f2_loc_slide.value - p_loc_slide.value
    print "b = %r" %b
    f1_mag = Fun_F(p_mag_slide.value,b)
    print "a1 = %r" %f1_mag

    if (f1_mag==0):
        f1_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[])
    elif (f1_mag<0):
        f1_arrow_source.data = dict(xS= 0, xE= 0, yS= [1-(f1_mag/200.0)], yE=[1] )
    else:
        f1_arrow_source.data = dict(xS= 0, xE= 0, yS= [-1-(f1_mag/200.0)], yE=[-1] )

#FUNCTION: Update f2 arrow size and location:
def Fun_Updatef2arrow(attrname, old, new):
    a = p_loc_slide.value
    f2_coord = f2_loc_slide.value
    f2_mag = Fun_F(p_mag_slide.value,a)
    print "position 2 mag and a are: %r and %r" %(f2_mag,a)

    #if (f2_mag==0):
    #    f2_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[])
    #elif (f2_mag<0):
    #    f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yS= [1-(f2_mag/200.0)], yE=[1] )
    #else:
    #    f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yS= [-1-(f2_mag/200.0)], yE=[-1] )
#

###Plotting###
plot = Figure(title="Doppeltgelagerter Balken und Einzellast", x_range=(x0-3,xf+3), y_range=(-5,5) )
plot.line(x='x', y='y', source=plot_source, color='blue',line_width=5)
#plot.line(x = [1, 2, 3, 4, 5], y = [1, 1, 1, 1, 1] , color = 'blue', line_width = 5 )

#arrow plotting:
#P arrow:
p_arrow_glyph = Arrow(end=OpenHead(line_color="red",line_width= 4,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=p_arrow_source,line_color="red",line_width=2)
plot.add_layout(p_arrow_glyph)
#Position 2 arrow:
f2_arrow_glyph = Arrow(end=OpenHead(line_color="blue",line_width= 4,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=f2_arrow_source,line_color="blue",line_width=2)
plot.add_layout(f2_arrow_glyph)
#Position 1 arrow:
f1_arrow_glyph = Arrow(end=OpenHead(line_color="blue",line_width= 4,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=f1_arrow_source,line_color="blue",line_width=2)
plot.add_layout(f1_arrow_glyph)

p_loc_slide.on_change('value', Fun_UpdateParrow)
p_mag_slide.on_change('value', Fun_UpdateParrow)
f2_loc_slide.on_change('value',Fun_Updatef1arrow)
f2_loc_slide.on_change('value',Fun_Updatef2arrow)

#show(row(column(plot)))#)p_loc_slide,p_mag_slide,f2_loc_slide),plot))
curdoc().add_root(row(column(p_loc_slide,p_mag_slide,f2_loc_slide),plot))
