from Spring import *
from Dashpot import *
from Mass import *
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import Slider, Button, Div
from math import sin, radians

# z = lam/(2*sqrt(k*m))
# z = 1 => crit damped
# z > 1 => over damped
# z < 1 => under damped

mass = RectangularMass(6,-4,16,8,2)
spring = Spring((-2,16),(-2,9),7,150)
dashpot = Dashpot((2,16),(2,9),5)
oldBase = 9
mass.linkObj(spring,(-2,16))
mass.linkObj(dashpot,(2,16))
Bottom_Line = ColumnDataSource(data = dict(x=[-2,2],y=[9,9]))
Linking_Line = ColumnDataSource(data = dict(x=[0,0],y=[9,5]))
Position = ColumnDataSource(data = dict(t=[0],s=[0]))
Wheel_source = ColumnDataSource(data = dict(x=[0],y=[5]))
Floor = dict(x=[],y=[])
Floor_source = ColumnDataSource(data = dict(x=[],y=[]))
t=0
s=0
Floor_angle=164
Active=False

def init():
    global Floor, Floor_source, oldBase, Floor_angle
    #x_range=(-7,7)
    Floor = dict(x=[],y=[])    
    #for x in (-7,2)
    for i in range(0,91):
        Floor['x'].append(i/10.0-7.0)
        Floor['y'].append(4)
    #for x in (2,4)
    for i in range(91,110):
        Floor['x'].append(i/10.0-7.0)
        Floor['y'].append(-0.0308*(i/10.0)**3+0.7329*(i/10.0)**2-5.7046*i/10.0+18.4390)
    #for x in (4,7)
    for i in range(110,141):
        Floor['x'].append(i/10.0-7.0)
        Floor['y'].append(4-sin(radians((i-100)*4.0)))
    Floor_source.data = deepcopy(dict(Floor))
    stable_pos=16-9.81*float(mass_input.value)/float(kappa_input.value)
    mass.moveTo(-4,stable_pos,8,2)
    spring.compressTo(Coord(-2,stable_pos),Coord(-2,9))
    dashpot.compressTo(Coord(2,stable_pos),Coord(2,9))
    mass.resetLinks(spring,(-2,stable_pos))
    mass.resetLinks(dashpot,(2,stable_pos))
    oldBase=9
    Floor_angle=164

def updateFloor():
    global Floor, Floor_source, Floor_angle
    Floor['y'].pop(0)
    Floor['y'].append(4-sin(radians(Floor_angle)))
    Floor_source.data = deepcopy(dict(Floor))
    Floor_angle+=4

def evolve():
    global mass, Bottom_Line, Linking_Line, t, s, oldBase
    updateFloor()
    gradient = (Floor['y'][73]-Floor['y'][68])/0.5
    if (gradient==0):
        baseShift=Floor['y'][70]-4
    else:
        gradNorm = sqrt(1+gradient**2)
        baseShift=Floor['y'][int(floor(70+10.0*gradient/gradNorm))]-4-(1-1.0/gradNorm)
    Bottom_Line.data=dict(x=[-2,2],y=[9+baseShift,9+baseShift])
    Linking_Line.data=dict(x=[0,0],y=[9+baseShift,5+baseShift])
    Wheel_source.data=dict(x=[0],y=[5+baseShift])
    spring.movePoint(Coord(-2,oldBase),Coord(0,(9+baseShift)-oldBase))
    dashpot.movePoint(Coord(2,oldBase),Coord(0,(9+baseShift)-oldBase))
    oldBase+=baseShift
    mass.FreezeForces()
    disp=mass.evolve(0.03)
    s+=disp.y
    t+=0.03
    Position.stream(dict(t=[t],s=[s]))

title_box = Div(text="""<h2 style="text-align:center;">Fusspunkterregter Schwinger (Base-excited oscillator)</h2>""",width=1000)

fig = figure(title="", tools="", x_range=(-7,7), y_range=(0,20),width=350,height=500)
fig.title.text_font_size="20pt"
fig.axis.visible = False
fig.grid.visible = False
fig.outline_line_color = None
spring.plot(fig,width=2)
dashpot.plot(fig,width=2)
fig.line(x='x',y='y',source=Bottom_Line,color="black",line_width=3)
fig.line(x='x',y='y',source=Linking_Line,color="black",line_width=3)
fig.line(x='x',y='y',source=Floor_source,color="black",line_width=1)
fig.ellipse(x='x',y='y',width=2,height=2,source=Wheel_source,line_color="#E37222",fill_color=None,line_width=2)
mass.plot(fig)

p = figure(title="", tools="", y_range=(-5,5), x_range=(0,20),height=500)
p.line(x='t',y='s',source=Position,color="black")
p.axis.major_label_text_font_size="12pt"
p.axis.axis_label_text_font_style="normal"
p.axis.axis_label_text_font_size="14pt"
p.xaxis.axis_label="Zeit (Time) [s]"
p.yaxis.axis_label="Auslenkung (Displacement) [m]"

def change_mass(attr,old,new):
    global mass
    mass.changeMass(new)
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

init()

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
    global Position, t, s, Bottom_Line, Linking_Line, spring, mass, dashpot
    stop()
    t=0
    s=0
    Position.data=dict(t=[0],s=[0])
    Bottom_Line.data = dict(x=[-2,2],y=[9,9])
    Linking_Line.data = dict(x=[0,0],y=[9,5])
    Wheel_source.data = dict(x=[0],y=[5])
    init() 
    mass.changeInitV(0.0)

stop_button = Button(label="Stop", button_type="success",width=100)
stop_button.on_click(stop)
play_button = Button(label="Play", button_type="success",width=100)
play_button.on_click(play)
reset_button = Button(label="Reset", button_type="success",width=100)
reset_button.on_click(reset)

## Send to window
curdoc().add_root(column(title_box,row(column(Spacer(height=100),play_button,stop_button,reset_button),Spacer(width=10),fig,p),
    row(mass_input,kappa_input),row(lam_input)))
curdoc().title = "Fusspunkterregter Schwinger"
#curdoc().add_periodic_callback(evolve,100)

