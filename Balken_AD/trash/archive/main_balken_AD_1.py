#import
from bokeh.plotting import Figure, output_file , show
from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, Arrow
from bokeh.layouts import column, row
from bokeh.io import curdoc
import numpy as np
import math


#Balken and Einzallast: Double bearing beam and single cell
#Make a class for the beam. Beam Class

#Beam Properties:
x0 = 0             #starting value of beam
xf = 10            #ending value of beam
x = np.linspace(x0,xf,resol)             #x-array of beam
y = [0] * resol    #y-array of beam
E  = 200.0e1        #modulus of elasticity
I  = 50          #moment of inertia
l  = xf-x0         #length of beam
plot_source = dict(x = x, y = y)

a_force_source = ColumnDataSource(data=dict(x=[],y=[]))
moment_source = ColumnDataSource(data=dict(x=[],y=[]))
shear_source = ColumnDataSource(data=dict(x=[],y=[]))
a_arrow = ColumnDataSource(data=dict(xS=[],yS=[],xE=[],yE=[]))
b_arrow = ColumnDataSource(data=dict(xS=[],yS=[],xE=[],yE=[]))
p_arrow = ColumnDataSource(data=dict(xS=[],yS=[],xE=[],yE=[]))
fmag_a = 0.0       #init magnitude of force at point a
fmag_b = 0.0       #init mag of force at point b
pmag = 1000.0      #init mag of p force
moment = 0.0       #init of moment
shear = 0.0         #init of shear
l_to_h  = 0.0         #init of length-to-height ratio
l_a = 0.0          #init of distance from a to p
l_b = 0.0          #init of distance from p to b
l_c = 0.0          #init of distance from b to end of beam

def ForcesMag(p_loc, b_loc, p_mag):
    l_a = p_loc
    l_b = b_loc - p_loc
    l_c = b_loc - xf
    fmag_a = (p_mag * l_b) / l
    fmag_b = (p_mag * l_a) / l
    force_source.data = dict( fmag_a = fmag_a, fmag_b = .fmag_b)

def



def ChangeForces(attrname, old, new):
    a.ForcesMag(p_loc_slide.value, b_loc_slide.value, p_mag_slide.value)
def Change

#Slider controls:
p_loc_slide= Slider(title="Concentrated Load Location",value=resol/2,start = 0.0, end = resol, step = 1)
p_mag_slide = Slider(title="Concentrated Load Magnitude", value=0, start=-pmag, end=pmag, step=1)
b_loc_slide = Slider(title="Support B Location",value=resol,start = 0.0, end = resol, step = 1)



###Main File###



#Plotting
plot = Figure(title="Doppeltgelagerter Balken und Einzellast", x_range=[x0-3,xf+3], y_range=[-5,5])
plot.line(x='x', y='y', source=plot_source, color='blue',line_width=5)
print plot_source.value

#Callback for defs in class
p_loc_slide.on_change('value', ForcesMag)
p_mag_slide.on_change('value', ForcesMag)
b_loc_slide.on_change('value', ForcesMag)

#arrow plotting:
#arrow_glyph = Arrow(end=OpenHead(line_color="red",line_width= 4,size=10),
#    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=arrow_source,line_color="red",line_width=2)
#plot.add_layout(arrow_glyph)

#Layout
show(row(column(p_loc_slide,p_mag_slide,b_loc_slide),plot))
#curdoc().add_root(row(column(p_loc_slide,p_mag_slide,b_loc_slide),plot))
