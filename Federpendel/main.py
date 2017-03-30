from Spring import *
from Dashpot import *
from Mass import *
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.io import curdoc
from bokeh.models import Slider, Button

mass = CircularMass(0.6,0,9,2,2)
spring = Spring((-2,18),(-2,11),7,50)
dashpot = Dashpot((2,18),(2,11),4)
mass.linkObj(spring,(-2,11))
mass.linkObj(dashpot,(2,11))
Bottom_Line = ColumnDataSource(data = dict(x=[-2,2],y=[11,11]))
Linking_Line = ColumnDataSource(data = dict(x=[0,0],y=[11,9]))
refLine = [9,11]
i=0

def evolve():
    global mass, Bottom_Line, Linking_Line
    mass.FreezeForces()
    disp=mass.evolve(0.1)
    refLine[0]+=disp.y
    refLine[1]+=disp.y
    Bottom_Line.data=dict(x=[-2,2],y=[refLine[1], refLine[1]])
    Linking_Line.data=dict(x=[0,0],y=[refLine[1], refLine[0]])
    global i
    i+=1
    if (i>50):
        curdoc().remove_periodic_callback(evolve)

fig = figure(title="Federpendel (Spring pendulum)", tools="", x_range=(-10,10), y_range=(0,20))
fig.title.text_font_size="20pt"
#fig.axis.visible = False
fig.grid.visible = False
fig.outline_line_color = None
spring.plot(fig,width=2)
dashpot.plot(fig,width=2)
fig.line(x=[-2,2],y=[19,19],color="black",line_width=3)
fig.line(x=[0,0],y=[18,19],color="black",line_width=3)
fig.line(x=[-2,2],y=[18,18],color="black",line_width=3)
fig.multi_line(xs=[[-2,-1.25],[-1,-0.25],[0,0.75],[1,1.75],[2,2.75]],
    ys=[[19,19.75],[19,19.75],[19,19.75],[19,19.75],[19,19.75]],
    color="black",
    line_width=3)
fig.line(x='x',y='y',source=Bottom_Line,color="black",line_width=3)
fig.line(x='x',y='y',source=Linking_Line,color="black",line_width=3)
mass.plot(fig)

p = figure(title="Federpendel (Spring pendulum)", tools="", x_range=(0,20), y_range=(-10,10))

def change_mass(attr,old,new):
    global mass
    mass.changeMass(new)
## Create slider to choose mass of blob
mass_input = Slider(title="Masse (mass) [kg]", value=0.6, start=0.0, end=2.0, step=0.1)
mass_input.on_change('value',change_mass)

def change_kappa(attr,old,new):
    global spring
    spring.changeSpringConst(new)
## Create slider to choose spring constant
kappa_input = Slider(title="Masse (Spring stiffness) [N/m]", value=1.0, start=0.0, end=5, step=0.1)
kappa_input.on_change('value',change_kappa)

def change_lam(attr,old,new):
    global dashpot
    dashpot.changeDamperCoeff(new)
## Create slider to choose damper coefficient
lam_input = Slider(title="Masse (Damper Coefficient) [N*s/m]", value=1.0, start=0.0, end=5, step=0.1)
lam_input.on_change('value',change_lam)

def change_initV(attr,old,new):
    global mass
    mass.changeInitV(new)
## Create slider to choose damper coefficient
initV_input = Slider(title="Anfangsgeschwindigkeit (Initial velocity) [m/s]", value=0.0, start=-5.0, end=5.0, step=0.5,width=350)
initV_input.on_change('value',change_initV)


## Send to window
curdoc().add_root(column(row(fig,p),row(mass_input,kappa_input,lam_input,initV_input)))
#curdoc().title = "Federpendel"
curdoc().add_periodic_callback(evolve,100)
