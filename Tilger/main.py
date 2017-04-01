from Spring import *
from Dashpot import *
from Mass import *
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import Slider, Button, Div, Arrow, OpenHead
from math import cos, radians, sqrt

# z = lam/(2*sqrt(k*m))
# z = 1 => crit damped
# z > 1 => over damped
# z < 1 => under damped

topMass = RectangularMass(4,-5,16,4,4)
spring = Spring((-4,16),(-4,11),5,150)
dashpot = Dashpot((-2,16),(-2,11),5)
topMass.linkObj(spring,(-4,16))
topMass.linkObj(dashpot,(-2,16))
mainMass = RectangularMass(16,-6,6,12,5)
mainMass.linkObj(spring,(-4,11))
mainMass.linkObj(dashpot,(-2,11))
baseSpring = Spring((0,0),(0,6),6+20.0*9.81/200.0,200)
mainMass.linkObj(baseSpring,(0,6))
AmplitudeFrequency = ColumnDataSource(data = dict(omega=[],A=[]))
Active=False
oscForceAngle = 90
oscAmp = 100.0
omega = 1
Position = ColumnDataSource(data = dict(om=[],A=[]))
Arrow_source = ColumnDataSource(data = dict(xS=[], xE=[], yS=[], yE=[]))
dt = 0.01
t = 0

def evolve():
    global topMass, mainMass, oscForceAngle, oscAmp, omega, dt, t
    F=oscAmp*cos(radians(oscForceAngle))
    mainMass.applyForce(Coord(0,F),None)
    topMass.FreezeForces()
    mainMass.FreezeForces()
    oscForceAngle+=360.0*omega/100.0
    if (t!=5):
        t+=1
        topMass.evolve(dt,False,False)
        mainMass.evolve(dt,False,False)
    else:
        t=0
        topMass.evolve(dt,True,False)
        mainMass.evolve(dt,True,True)
    if (t==2 or t==4):
        h=mainMass.getTop()
        F/=50.0
        if (F<0):
            Arrow_source.data=dict(xS=[3], xE=[3], yS=[h], yE=[h-F])
            Arrow_glyph.start=ArrowHead_glyph
            Arrow_glyph.end=None
        else:
            Arrow_source.data=dict(xS=[3], xE=[3], yS=[h], yE=[h+F])
            Arrow_glyph.start=None
            Arrow_glyph.end=ArrowHead_glyph

def calculateGraphPlot():
    omega=[]
    Amplitude=[]
    c2=lam_input.value
    k2=kappa_input.value
    m2=mass_input.value
    k1=200
    m1=16
    for i in range(0,201):
        omega.append(i/10.0)
        om=i/10.0
        num=c2**2*om**2+(k2-m2*om**2)**2
        denom=((k1-m1*om**2)*(k2-m2*om**2)-k2*m2*om**2)**2+c2**2*om**2*(k1-m1*om**2-m2*om**2)**2
        Amplitude.append(oscAmp*sqrt(num/denom))
    AmplitudeFrequency.data=dict(omega=omega,A=Amplitude)

title_box = Div(text="""<h2 style="text-align:center;">Schwingungstilger (Tuned mass damper)</h2>""",width=1000)

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
ArrowHead_glyph = OpenHead(line_color="#E37222",line_width=3,size=10)
Arrow_glyph = Arrow(x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=Arrow_source,
    line_color="#E37222",line_width=3)
fig.add_layout(Arrow_glyph)

p = figure(title="", tools="", y_range=(0,20), x_range=(0,20),height=500)
p.line(x='omega',y='A',source=AmplitudeFrequency,color="black")
p.axis.major_label_text_font_size="12pt"
p.axis.axis_label_text_font_style="normal"
p.axis.axis_label_text_font_size="14pt"
p.xaxis.axis_label=u"\u03C9 [s\u207B\u00B9]"
p.yaxis.axis_label="Amplitude [m]"
p.ellipse(x='om',y='A', width=0.5, height=0.5, source=Position,color="#E37222")

def change_mass(attr,old,new):
    global mass, omega
    topMass.changeMass(new)
    calculateGraphPlot()
    change_Omega(None,None,omega)
## Create slider to choose mass of blob
mass_input = Slider(title="Masse (mass) [kg]", value=6, start=0.5, end=10.0, step=0.1,width=400)
mass_input.on_change('value',change_mass)

def change_kappa(attr,old,new):
    global spring, omega
    spring.changeSpringConst(new)
    calculateGraphPlot()
    change_Omega(None,None,omega)
## Create slider to choose spring constant
kappa_input = Slider(title="Federsteifigkeit (Spring stiffness) [N/m]", value=150.0, start=0.0, end=200, step=10,width=400)
kappa_input.on_change('value',change_kappa)

def change_lam(attr,old,new):
    global dashpot, omega
    dashpot.changeDamperCoeff(new)
    calculateGraphPlot()
    change_Omega(None,None,omega)
## Create slider to choose damper coefficient
lam_input = Slider(title=u"D\u00E4mpfungskonstante (Damper Coefficient) [N*s/m]", value=5.0, start=0.0, end=10, step=0.1,width=400)
lam_input.on_change('value',change_lam)

def change_Omega(attr,old,new):
    global omega
    omega = new
    Position.data=dict(om=[new],A=[AmplitudeFrequency.data['A'][int(floor(new*10))]])
## Create slider to choose damper coefficient
omega_input = Slider(title=u"\u03C9 [s\u207B\u00B9]", value=1.0, start=0.0, end=20.0, step=0.5,width=400)
omega_input.on_change('value',change_Omega)

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
    stop()
    #Position.data=dict(t=[0],s=[0])
    stable_pos = 16-4*9.81/150.0
    spring.compressTo(Coord(-4,stable_pos),Coord(-4,11))
    dashpot.compressTo(Coord(-2,stable_pos),Coord(-2,11),0.01)
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
    oscForceAngle = 0
    Arrow_source.data=dict(xS=[3], xE=[3], yS=[11], yE=[11+oscAmp/50.0])
    Arrow_glyph.start=None
    Arrow_glyph.end=ArrowHead_glyph

stop_button = Button(label="Stop", button_type="success",width=100)
stop_button.on_click(stop)
play_button = Button(label="Play", button_type="success",width=100)
play_button.on_click(play)
reset_button = Button(label="Reset", button_type="success",width=100)
reset_button.on_click(reset)

calculateGraphPlot()
change_Omega(None,None,1.0)
Arrow_source.data=dict(xS=[3], xE=[3], yS=[11], yE=[11+oscAmp/50.0])
Arrow_glyph.start=None
Arrow_glyph.end=ArrowHead_glyph

## Send to window
curdoc().add_root(column(title_box,row(column(Spacer(height=100),stop_button,play_button,reset_button),Spacer(width=10),fig,p),
    row(mass_input,kappa_input),row(lam_input,omega_input)))
curdoc().title = "Schwingungstilger"
#curdoc().add_periodic_callback(evolve,100)

