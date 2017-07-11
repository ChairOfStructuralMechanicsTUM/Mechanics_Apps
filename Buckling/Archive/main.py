#Knickung (buckling) animation:
from bokeh.plotting import Figure, output_file , show
from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, Arrow
from bokeh.layouts import column, row
from bokeh.io import curdoc
import numpy as np

#Euler Elastic Buckling
#have 4 beams of different lengths that buckle at the same value.
#Beams have different boundary conditions

#Shared properties:
resol = 100             #resolution of beams
E  = 200.0e1            #modulus of elasticity
I  = 50                 #moment of inertia
f_crit = 200            #Critical force
f_end = 1.5*f_crit      #last slider value

#Define source variables:
test_source = ColumnDataSource(data=dict(x=[] , y=[]))
#beam 1: "Free-Fixed" Beam ff
beam1_source = ColumnDataSource(data=dict(x=[] , y=[]))
#beam 2: "Pinned-Pinned" Beam pp
beam2_source = ColumnDataSource(data=dict(x=[] , y=[]))
#beam 3: "Pinned-Fixed" Beam pf
beam3_source = ColumnDataSource(data=dict(x=[] , y=[]))
#beam 4: "Fixed-Fixed" Beam fifi
beam4_source = ColumnDataSource(data=dict(x=[] , y=[]))

#bifurkation source:
w_source = ColumnDataSource(data=dict(x=[] , y=[]))
fplot_source = ColumnDataSource(data=dict(x=[] , y=[]))


#Force slider:
f_mag_slide = Slider(title="Buckling Load Magnitude, F", value=0, start=0, end=f_end, step=1)


#FUNCTION: Calculate lengths of all beams:
def fun_length():
    lpp =  np.sqrt( E*I / f_crit ) * np.pi   #length of pinned-pinned beam:
    lpf =  np.sqrt( E*I / f_crit ) * (np.pi/2)   #length of "Free-Fixed" beam:
    return lpp, lpf

#beam 1:
#FUNCTION: Calculate the deflection of "Pinned-Pinned":
def fun_deflect_pp(x,l,b):
    v = [0] * resol
    for i in range(0,resol):
        v[i] = b * np.sin( ( np.pi * x[i] ) / l )
    return v

def fun_deflect_ff(x,l,d):
    v = [0] * resol
    for i in range(0,resol):
        v[i] = d * (1 - np.cos( ( np.pi * x[i] ) / (2*l) ) )
    return v

lpp, lff = fun_length()

#initial values for x and y:
xpp = np.ones(resol) * 2
ypp = np.linspace(0,lpp,resol)

#fixed free:
xff = np.ones(resol) * 0
yff = np.linspace(0,lff,resol)

#f_mag = f_mag_slide.value

#beam2_source.data = dict(x=[0]*resol , y=[np.linspace(0,lpp,resol)])

#Possibility: create one function to update values, then one function to update graph

def Fun_Update_pp(attrname, old, new):
    f_mag = f_mag_slide.value
    if (f_mag <= f_crit):
        z=1
        #print "nothing happens"
    elif (f_mag > f_crit):
        vpp = fun_deflect_pp(ypp,lpp,f_mag/f_end)
        x1 = [0]*resol

        for i in range(0,resol):
            x1[i] = vpp[i] + xpp[i]
        beam2_source.data = dict(x= x1 , y=ypp)
        #print beam2_source.data
    else:
        print "error"



def Fun_Update_ff(attrname, old, new):
    f_mag = f_mag_slide.value
    if (f_mag <= f_crit):
        z=1
        #w_source.data = dict(x = f_mag, y = 0)
        #fplot_source.data = dict(x = f_mag, y = 0)
    elif (f_mag > f_crit):
        vff = fun_deflect_ff(yff,lff,f_mag/f_end)
        x1 = [0]*resol

        for i in range(0,resol):
            x1[i] = -vff[i] + xff[i]

        beam1_source.data = dict(x= x1 , y=yff)
        #w_source.data = dict(x = [f_mag], y = [vff[0]])
        #fplot_source.data = dict(x = [f_mag], y = 0)
        #print beam2_source.data
    else:
        print "error"

#initial function:
def initial():
    beam2_source.data = dict(x= xpp , y= ypp)
    beam1_source.data = dict(x= xff , y= yff)


##########Plotting##########
#Main Plot:
plot = Figure(title="Knickung", x_range=(-2,5), y_range=(-1,80))
plot.line(x='x', y='y', source = beam2_source, color='blue',line_width=5)
plot.line(x='x', y='y', source = beam1_source, color='blue',line_width=5)
#Beam lines:
#Pinned-Pinned Beam:

###Bifurkation Plot:
#plot1 = Figure(title="Bifurkation", x_range=(0,f_end), y_range=(-2,2), width = 450, height = 250)
#plot1.line(x='x', y='y', source=w_source, color='blue',line_width=5)
#plot1.line(x='x', y='y', source=fplot_source, color='red',line_width=5)

###on_change:
f_mag_slide.on_change('value', Fun_Update_pp)
f_mag_slide.on_change('value', Fun_Update_ff)

#main:
initial()
#print beam2_source.data
#show:
curdoc().add_root(row(column(f_mag_slide),plot))
