#Maxwell Equation
#Maxwell's reciprocity theorem/Reziprozitatssatz von Maxwell

from bokeh.plotting import Figure, output_file , show
from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, Arrow
from bokeh.layouts import column, row
from bokeh.io import curdoc
import numpy as np
import math

#Steps
#1. Find Maxwell reciprocity equation information online
    #Was sent a beam equation.
#2. Create multiple points in the shape of the square
#3. add the sliders to change force magnitude and the location of the force
#4. distort the points by using the Maxwell reciprocity
#5. add in the details

#Create initial x and y coordinates for box:
box_resol = 100
x0 = 0
xf = 7
y0 = 5
yf = 5
x = np.linspace(x0,xf,box_resol)
y = np.ones(box_resol) * 5
#np.size(x)
#np.size(y)
fmagnitude = 1000

#Initialize variables
E = 200.0e1       #modolus of elasticity
I = 50.0         #moment of inertia
l = xf - x0     #length of beam

# set up data sources for moving objects:
#data source for the line (soon to be full rectangle)
data_source = ColumnDataSource(data=dict(x=[], y=[]))
#data source for arrow:
arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[]))


#
#controls
force_loc = Slider(title="Force Location",value=box_resol/2,start = 0.0, end = box_resol, step = 1)
force_input = Slider(title="Force", value=0, start=-fmagnitude, end=fmagnitude, step=1)

#function fun_change: changes value based on maxwell recip:
def fun_change(attrname, old, new):
    ynew = []
    f_coord1 = int(force_loc.value)
    f_coord = (x[f_coord1],y[f_coord1])
    f_mag = force_input.value
    b = xf - x[f_coord1]
    a = x[f_coord1]
    #print("new force mag: %r") %f_mag
    #print("a loc: %r") %a
    for i in range(1,box_resol):
        #conditional statement to determine which displacement to use
        if x0 <= x[i] and x[i] <= a:
            w = ( (f_mag * b) / (6.0 * E * I* l) ) * ( ( (l**2) * x[i]) - ((b**2) * x[i]) - (x[i]**3) )
        elif a <= x[i] and x[i] <= xf:
            w = ( (f_mag * b) / (6.0 * E * I* l) ) * ( (l/b) * (( x[i] - a)**3) + (( (l**2) - (b**2) )*x[i]) - (x[i]**3) )
        yn = y[i] + w
        ynew.append(yn)
    data_source.data = dict(x = x, y = ynew)
        # Only display the dL arrow and label if dL=/=0
    if (f_mag==0):
        arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[])
    elif (f_mag<0):
        arrow_source.data = dict(xS= [x[f_coord1]], xE= [x[f_coord1]], yS= [y[f_coord1]+1-(f_mag/200.0)], yE=[y[f_coord1]+1] )
    else:
        arrow_source.data = dict(xS= [x[f_coord1]], xE= [x[f_coord1]], yS= [y[f_coord1]-1-(f_mag/200.0)], yE=[y[f_coord1]-1])


print(len(x))
print(len(y))


def init_data():
    fun_change(None,None,None)


# Plotting
plot = Figure(title="Maxwell reciprocity", x_range=[x0-3,xf+3], y_range=[-15,15.1])
plot.line(x='x', y='y', source=data_source, color='blue',line_width=5)
#Callback
force_loc.on_change('value', fun_change)
force_input.on_change('value', fun_change)

#arrow plotting:
arrow_glyph = Arrow(end=OpenHead(line_color="red",line_width= 4,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=arrow_source,line_color="red",line_width=2)
plot.add_layout(arrow_glyph)

#main:
init_data()


#Layout
#show(row(column(force_loc,force_input),plot))
curdoc().add_root(row(column(force_loc,force_input),plot))
