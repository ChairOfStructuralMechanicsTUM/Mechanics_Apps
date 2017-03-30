from Spring import *
from Dashpot import *
from Mass import *
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.io import curdoc
from bokeh.models import Slider, Button

# z = lam/(2*sqrt(k*m))
# z = 1 => crit damped
# z > 1 => over damped
# z < 1 => under damped

mass = CircularMass(6,0,9,2,2)
mass.changeInitV(-5.0)
spring = Spring((-2,18),(-2,11),7,150)
dashpot = Dashpot((2,18),(2,11),5)
mass.linkObj(spring,(-2,11))
mass.linkObj(dashpot,(2,11))
Bottom_Line = ColumnDataSource(data = dict(x=[-2,2],y=[11,11]))
Linking_Line = ColumnDataSource(data = dict(x=[0,0],y=[11,9]))
Position = ColumnDataSource(data = dict(t=[0],s=[0]))
t=0
s=0

def evolve():
    global mass, Bottom_Line, Linking_Line, t, s
    mass.FreezeForces()
    disp=mass.evolve(0.03)
    s+=disp.y
    Bottom_Line.data=dict(x=[-2,2],y=[11+s, s+11])
    Linking_Line.data=dict(x=[0,0],y=[11+s, 9+s])
    t+=0.03
    Position.stream(dict(t=[t],s=[s]))

fig = figure(title="Federpendel (Spring pendulum)", tools="", x_range=(-10,10), y_range=(0,20))
fig.title.text_font_size="20pt"
fig.axis.visible = False
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

p = figure(title="Federpendel (Spring pendulum)", tools="", y_range=(-2,2))
p.line(x='t',y='s',source=Position,color="black")

def change_mass(attr,old,new):
    global mass
    mass.changeMass(new)
## Create slider to choose mass of blob
mass_input = Slider(title="Masse (mass) [kg]", value=6, start=0.0, end=10.0, step=0.1)
mass_input.on_change('value',change_mass)

def change_kappa(attr,old,new):
    global spring
    spring.changeSpringConst(new)
## Create slider to choose spring constant
kappa_input = Slider(title="Masse (Spring stiffness) [N/m]", value=150.0, start=0.0, end=200, step=10)
kappa_input.on_change('value',change_kappa)

def change_lam(attr,old,new):
    global dashpot
    dashpot.changeDamperCoeff(new)
## Create slider to choose damper coefficient
lam_input = Slider(title="Masse (Damper Coefficient) [N*s/m]", value=5.0, start=0.0, end=10, step=0.1)
lam_input.on_change('value',change_lam)

def change_initV(attr,old,new):
    global mass
    mass.changeInitV(new)
## Create slider to choose damper coefficient
initV_input = Slider(title="Anfangsgeschwindigkeit (Initial velocity) [m/s]", value=-5.0, start=-5.0, end=5.0, step=0.5,width=350)
initV_input.on_change('value',change_initV)

## Send to window
curdoc().add_root(column(row(fig,p),row(mass_input,kappa_input,lam_input,initV_input)))
#curdoc().title = "Federpendel"
curdoc().add_periodic_callback(evolve,100)
