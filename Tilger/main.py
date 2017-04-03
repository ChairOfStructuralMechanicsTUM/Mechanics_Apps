from Spring import *
from Dashpot import *
from Mass import *
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import Slider, Button, Div

# z = lam/(2*sqrt(k*m))
# z = 1 => crit damped
# z > 1 => over damped
# z < 1 => under damped

topMass = RectangularMass(4,-5,16,4,4)
spring = Spring((-4,16),(-4,11),5,150)
dashpot = Dashpot((-2,16),(-2,11),5)
topMass.linkObj(spring,(-4,16))
topMass.linkObj(dashpot,(-2,16))
mainMass = RectangularMass(16,-6,6,12,5,False)
mainMass.linkObj(spring,(-4,11))
mainMass.linkObj(dashpot,(-2,11))
baseSpring = Spring((0,0),(0,6),6+16.0*9.81/500.0,500)
mainMass.linkObj(baseSpring,(0,6))
Position = ColumnDataSource(data = dict(omega=[0],v=[0]))
Active=False

def evolve():
    global topMass, mainMass
    topMass.FreezeForces()
    mainMass.FreezeForces()
    mainMass.evolve(0.03)
    topMass.evolve(0.03)
    #Position.stream(dict(t=[t],s=[s]))

title_box = Div(text="""<h2 style="text-align:center;">Federpendel (Spring pendulum)</h2>""",width=1000)

fig = figure(title="", tools="", x_range=(-7,7), y_range=(0,20),width=350,height=500)
fig.title.text_font_size="20pt"
fig.axis.visible = False
fig.grid.visible = False
fig.outline_line_color = None
spring.plot(fig,width=2)
baseSpring.plot(fig,width=2)
dashpot.plot(fig,width=2)
mainMass.plot(fig)
topMass.plot(fig)

p = figure(title="", tools="", y_range=(-5,5), x_range=(0,20),height=500)
#p.line(x='t',y='s',source=Position,color="black")
p.axis.major_label_text_font_size="12pt"
p.axis.axis_label_text_font_style="normal"
p.axis.axis_label_text_font_size="14pt"
p.xaxis.axis_label="Zeit (Time) [s]"
p.yaxis.axis_label="Auslenkung (Displacement) [m]"

def change_mass(attr,old,new):
    global mass
    topMass.changeMass(new)
## Create slider to choose mass of blob
mass_input = Slider(title="Masse (mass) [kg]", value=6, start=0.0, end=10.0, step=0.1,width=400)
mass_input.on_change('value',change_mass)

def change_kappa(attr,old,new):
    global spring
    spring.changeSpringConst(new)
## Create slider to choose spring constant
kappa_input = Slider(title="Federsteifigkeit (Spring stiffness) [N/m]", value=150.0, start=0.0, end=200, step=10,width=400)
kappa_input.on_change('value',change_kappa)

def change_lam(attr,old,new):
    global dashpot
    dashpot.changeDamperCoeff(new)
## Create slider to choose damper coefficient
lam_input = Slider(title=u"D\u00E4mpfungskonstante (Damper Coefficient) [N*s/m]", value=5.0, start=0.0, end=10, step=0.1,width=400)
lam_input.on_change('value',change_lam)

#def change_initV(attr,old,new):
#    global mass
#    mass.changeInitV(new)
## Create slider to choose damper coefficient
#initV_input = Slider(title="Anfangsgeschwindigkeit (Initial velocity) [m/s]", value=-5.0, start=-5.0, end=5.0, step=0.5,width=400)
#initV_input.on_change('value',change_initV)

def stop():
    global Active
    if (Active):
        curdoc().remove_periodic_callback(evolve)
        Active=False
def play():
    global Active
    if (not Active):
        reset()
        curdoc().add_periodic_callback(evolve,100)
        Active=True
def reset():
    global spring, topMass, dashpot, mainMass, baseSpring
    stop()
    #Position.data=dict(t=[0],s=[0])
    stable_pos = 16-4*9.81/150.0
    spring.compressTo(Coord(-4,stable_pos),Coord(-4,11))
    dashpot.compressTo(Coord(-2,stable_pos),Coord(-2,11))
    baseSpring.compressTo(Coord(0,0),Coord(0,6))
    topMass.moveTo(-5,stable_pos,4,4)
    topMass.resetLinks(spring,(-4,stable_pos))
    topMass.resetLinks(dashpot,(-2,stable_pos))
    topMass.changeInitV(0)
    mainMass.moveTo(-6,6,12,5)
    mainMass.resetLinks(spring,(-4,11))
    mainMass.resetLinks(dashpot,(-2,11))
    mainMass.changeInitV(0)
    mainMass.resetLinks(baseSpring,(0,6))

stop_button = Button(label="Stop", button_type="success",width=100)
stop_button.on_click(stop)
play_button = Button(label="Play", button_type="success",width=100)
play_button.on_click(play)
reset_button = Button(label="Reset", button_type="success",width=100)
reset_button.on_click(reset)

reset()
evolve()

## Send to window
curdoc().add_root(column(title_box,row(column(Spacer(height=100),stop_button,play_button,reset_button),Spacer(width=10),fig,p),
    row(mass_input,kappa_input),row(lam_input)))
curdoc().title = "Federpendel"
#curdoc().add_periodic_callback(evolve,100)

