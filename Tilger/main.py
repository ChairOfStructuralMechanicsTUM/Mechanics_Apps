from Spring import *
from Dashpot import *
from Mass import *
from Integrator import *
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import Slider, Button, Div, Arrow, OpenHead
from math import cos, radians, sqrt, pi

## create and link objects
# create upper mass
topMass = RectangularMass(4,-5,16,4,4)
# create dashpot and spring linked to upper mass
dashpot = Dashpot((-2,16),(-2,11),5)
# l2 = m2*g/k2+x2-x1-h so that start is at equilibrium
# where k2=150,k1=200,x1=6,x2=16, m1=16,m2=4, h=5
l2=4*9.81/150.0+5
spring = Spring((-4,16),(-4,11),l2,150)
# link objects to upper mass
topMass.linkObj(spring,(-4,16))
topMass.linkObj(dashpot,(-2,16))
# create base spring
# l1 = g*(m1+m2)/k1+x1 for equilibrium
# where k2=150,k1=200,x1=6,x2=16, m1=16,m2=4, h=5
l1=6.981
baseSpring = Spring((0,0),(0,6),l1,200)
# link objects to main large mass
mainMass = RectangularMass(16,-6,6,12,5)
mainMass.linkObj(spring,(-4,11))
mainMass.linkObj(dashpot,(-2,11))
mainMass.linkObj(baseSpring,(0,6))
# create ColumnDataSource for Amplitude as a function of frequency
AmplitudeFrequency = ColumnDataSource(data = dict(omega=[],A=[]))
# create ColumnDataSource for spot showing current frequency
Position = ColumnDataSource(data = dict(om=[],A=[]))
# create ColumnDataSource for arrow showing force
Arrow_source = ColumnDataSource(data = dict(xS=[], xE=[], yS=[], yE=[]))
# create vector of forces applied during simulation
ForceList = [0,0]
# create integrator
Int = Integrator([topMass,mainMass],ForceList)
# create initial
Active=False
oscForceAngle = pi/2
oscAmp = 100.0
omega = 1
dt = 0.1

## functions

def evolve():
    global topMass, mainMass, oscForceAngle, oscAmp, omega, dt, t
    # current force applied to main mass
    F=oscAmp*cos(oscForceAngle)
    mainMass.applyForce(Coord(0,F),None)
    # calculate force at next timestep
    oscForceAngle+=omega*dt
    # add to ForceList so integrator can use it
    ForceList[1]=oscAmp*cos(oscForceAngle)
    # make system evolve by time dt
    Int.evolve(dt)
    
    ## draw force arrow
    h=mainMass.getTop()
    # reduce F to make arrow normal sized on drawing
    F/=50.0
    # draw arrow in correct direction
    if (F<0):
        Arrow_source.data=dict(xS=[3], xE=[3], yS=[h], yE=[h-F])
        Arrow_glyph.start=ArrowHead_glyph
        Arrow_glyph.end=None
    else:
        Arrow_source.data=dict(xS=[3], xE=[3], yS=[h], yE=[h+F])
        Arrow_glyph.start=None
        Arrow_glyph.end=ArrowHead_glyph

## calculate Amplitude as a function of frequency
# (simplified version with no gravity or rest length)
# this changes the value of the amplitude but not the shape of the graph or the resonant frequency
# it is therefore a sufficient approximation
def calculateGraphPlot():
    global lam_input, kappa_input, mass_input, oscAmp, AmplitudeFrequency
    # prepare vectors
    omega=[]
    Amplitude=[]
    # save spring, dashpot and mass constants
    c2=lam_input.value
    k2=kappa_input.value
    m2=mass_input.value
    k1=200
    m1=16
    # calculate points on graph
    for i in range(1,201):
        # find omega
        omega.append(i/10.0)
        om=i/10.0
        
        # find amplitude
        num=c2**2*om**2+(k2-m2*om**2)**2
        denom=((k1-m1*om**2)*(k2-m2*om**2)-k2*m2*om**2)**2+c2**2*om**2*(k1-m1*om**2-m2*om**2)**2
        Amplitude.append(oscAmp*sqrt(num/denom))
    
    # add calculated values to graph
    AmplitudeFrequency.data=dict(omega=omega,A=Amplitude)

# draw title in the middle
title_box = Div(text="""<h2 style="text-align:center;">Schwingungstilger (Tuned mass damper)</h2>""",width=1000)

## create simulation drawing
fig = figure(title="", tools="", x_range=(-7,7), y_range=(0,20),width=350,height=500)
fig.title.text_font_size="20pt"
fig.axis.visible = False
fig.grid.visible = False
fig.outline_line_color = None
# add objects to plot
spring.plot(fig,width=2)
baseSpring.plot(fig,width=2)
dashpot.plot(fig,width=2)
mainMass.plot(fig)
topMass.plot(fig)
# create and add force arrow to plot
ArrowHead_glyph = OpenHead(line_color="#E37222",line_width=3,size=10)
Arrow_glyph = Arrow(x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=Arrow_source,
    line_color="#E37222",line_width=3)
fig.add_layout(Arrow_glyph)

## create amplitude frequency diagram
p = figure(title="", tools="",y_range=(0,20),x_range=(0,20),height=500)
p.axis.major_label_text_font_size="12pt"
p.axis.axis_label_text_font_style="normal"
p.axis.axis_label_text_font_size="14pt"
p.xaxis.axis_label=u"\u03C9 [s\u207B\u00B9]"
p.yaxis.axis_label="Amplitude [m]"
# plot graph
p.line(x='omega',y='A',source=AmplitudeFrequency,color="black")
# show current frequency
p.ellipse(x='om',y='A', width=0.5, height=0.5, source=Position,color="#E37222")

def change_mass(attr,old,new):
    global topMass, omega
    topMass.changeMass(new)
    # recalculate graph for new values
    calculateGraphPlot()
    change_Omega(None,None,omega)
## Create slider to choose mass of upper mass
mass_input = Slider(title="Masse (mass) [kg]", value=4, start=0.5, end=10.0, step=0.1,width=400)
mass_input.on_change('value',change_mass)

def change_kappa(attr,old,new):
    global spring, omega
    spring.changeSpringConst(new)
    # recalculate graph for new values
    calculateGraphPlot()
    # plot frequency on new graph
    change_Omega(None,None,omega)
## Create slider to choose spring constant
kappa_input = Slider(title="Federsteifigkeit (Spring stiffness) [N/m]", value=150.0, start=0.0, end=200, step=10,width=400)
kappa_input.on_change('value',change_kappa)

def change_lam(attr,old,new):
    global dashpot, omega
    dashpot.changeDamperCoeff(new)
    # recalculate graph for new values
    calculateGraphPlot()
    # plot frequency on new graph
    change_Omega(None,None,omega)
## Create slider to choose damper coefficient
lam_input = Slider(title=u"D\u00E4mpfungskonstante (Damper Coefficient) [N*s/m]", value=5.0, start=0.0, end=10, step=0.1,width=400)
lam_input.on_change('value',change_lam)

def change_Omega(attr,old,new):
    global omega, oscAmp
    omega = new
    if (omega==0):
        # if no oscillation then A is natural amplitude
        Position.data=dict(om=[new],A=[oscAmp/200.0])
    else:
        # find amplitude for current frequency from AmplitudeFrequency graph
        Position.data=dict(om=[new],A=[AmplitudeFrequency.data['A'][int(floor(new*10))-1]])
## Create slider to choose damper coefficient
omega_input = Slider(title=u"\u03C9 [s\u207B\u00B9]", value=1.0, start=0.0, end=20.0, step=0.1,width=400)
omega_input.on_change('value',change_Omega)

## create functions for buttons which control simulation
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
    global spring, topMass, dashpot, mainMass, baseSpring, oscForceAngle
    # if simulation is running, then stop it
    stop()
    # reset objects
    spring.compressTo(Coord(-4,16),Coord(-4,11))
    # (done twice to implement 0 velocity)
    dashpot.compressTo(Coord(-2,16),Coord(-2,11),0.1)
    dashpot.compressTo(Coord(-2,16),Coord(-2,11),0.1)
    baseSpring.compressTo(Coord(0,0),Coord(0,6))
    topMass.moveTo(-5,16,4,4)
    topMass.resetLinks(spring,(-4,16))
    topMass.resetLinks(dashpot,(-2,16))
    topMass.changeInitV(0)
    mainMass.moveTo(-6,6,12,5)
    mainMass.resetLinks(spring,(-4,11))
    mainMass.resetLinks(dashpot,(-2,11))
    mainMass.resetLinks(baseSpring,(0,6))
    mainMass.changeInitV(0)
    oscForceAngle = pi/2
    Arrow_source.data=dict(xS=[], xE=[], yS=[], yE=[])

## create buttons to control simulation
stop_button = Button(label="Stop", button_type="success",width=100)
stop_button.on_click(stop)
play_button = Button(label="Play", button_type="success",width=100)
play_button.on_click(play)
reset_button = Button(label="Reset", button_type="success",width=100)
reset_button.on_click(reset)

# setup initial conditions
calculateGraphPlot()
change_Omega(None,None,1.0)

## Send to window
curdoc().add_root(column(title_box,row(column(Spacer(height=100),stop_button,play_button,reset_button),Spacer(width=10),fig,p),
    row(mass_input,kappa_input),row(lam_input,omega_input)))
curdoc().title = "Schwingungstilger"

