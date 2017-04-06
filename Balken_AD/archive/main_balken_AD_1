#import
from bokeh.plotting import Figure, output_file , show
from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, Arrow
from bokeh.layouts import column, row
from bokeh.io import curdoc
import numpy as np
import math


#Balken and Einzallast: Double bearing beam and single cell
#Make a class for the beam. Beam Class
class Beam:
    #shared class variables
    global x0              #starting value of beam
    global xf             #ending value of beam
    global y0              #height of beam on plot
    global E           #modulus of elasticity
    global I            #moment of inertia
    global l           #length of beam
    force_source = ColumnDataSource(data=dict(fmag_a=[],fmag_b=[]))
    graph_source = ColumnDataSource(data=dict(moment=[], shear=[]))

    #Constructor
    def __init__(self, resol):
        global x0              #starting value of beam
        global xf             #ending value of beam
        global y0              #height of beam on plot
        global E           #modulus of elasticity
        global I            #moment of inertia
        global l           #length of beam
        self.x = np.linspace(x0,xf,resol)             #x-array of beam
        self.y = [0] * resol    #y-array of beam
        plot_source = dict(x = x, y = y)
        self.fmag_a = 0.0       #init magnitude of force at point a
        self.fmag_b = 0.0       #init mag of force at point b
        self.pmag = 1000.0      #init mag of p force
        self.moment = []        #init of moment
        self.shear = []         #init of shear
        self.lth  = 0.0         #init of length-to-height ratio
        self.l_a = 0.0          #init of distance from a to p
        self.l_b = 0.0          #init of distance from p to b
        self.l_c = 0.0          #init of distance from b to end of beam

    def ForcesMag(self, p_loc, b_loc, p_mag):
        self.l_a = p_loc
        self.l_b = b_loc-p_loc
        self.l_c = b_loc-xf
        self.pmag = p_mag
        self.fmag_a = (self.pmag * self.l_b) / l
        self.fmag_b = (self.pmag * self.l_a) / l
        force_source.data = dict(fmag_a = self.fmag_a, fmag_b = self.fmag_b)


def ChangeForces(attrname, old, new):
    a.ForcesMag(p_loc_slide.value, b_loc_slide.value, p_mag_slide.value)



###Main File###
a = Beam(100) #define beam a

#Slider controls:
p_loc_slide= Slider(title="Concentrated Load Location",value=resol/2,start = 0.0, end = resol, step = 1)
p_mag_slide = Slider(title="Concentrated Load Magnitude", value=0, start=-pmag, end=pmag, step=1)
b_loc_slide = Slider(title="Support B Location",value=resol,start = 0.0, end = resol, step = 1)

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
