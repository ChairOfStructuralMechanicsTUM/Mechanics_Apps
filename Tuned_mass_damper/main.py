from __future__ import division
from Spring import *
from Dashpot import *
from Mass import *
from Integrator import *
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import Slider, Button, Div, Arrow, OpenHead, Range1d
from math import cos, sin, radians, sqrt, pi, atan2
from os.path import dirname, join, split

## create and link objects
g=9.81
x1=6
x2=16
h=5
m1=100
m2=8.0
c2=3.7
k1 = 1000.0
k2 = 80.0
# create upper mass
topMass = RectangularMass(m2,-5,x2,4,4)
# create dashpot and spring linked to upper mass
dashpot = Dashpot((-2,x2),(-2,x1+h),c2)
# l2 = m2*g/k2+x2-x1-h so that start is at equilibrium
l2=m2*g/k2+x2-x1-h
spring = Spring((-4,x2),(-4,x1+h),l2,k2)
# link objects to upper mass
topMass.linkObj(spring,(-4,x2))
topMass.linkObj(dashpot,(-2,x2))
# create base spring
# l1 = g*(m1+m2)/k1+x1 for equilibrium
# where k2=100,k1=10000,x1=6,x2=16, m1=100,m2=1, h=5
l1=g*(m1+m2)/k1+x1
baseSpring = Spring((0,0),(0,6),l1,k1)
# link objects to main large mass
mainMass = RectangularMass(m1,-6,x1,12,h)
mainMass.linkObj(spring,(-4,x1+h))
mainMass.linkObj(dashpot,(-2,x1+h))
mainMass.linkObj(baseSpring,(0,x1))
# create ColumnDataSource for Amplitude as a function of frequency
AmplitudeFrequency = ColumnDataSource(data = dict(omega=[],A=[]))
# create ColumnDataSource for spot showing current frequency
Position = ColumnDataSource(data = dict(om=[],A=[]))
# create ColumnDataSource for arrow showing force
Arrow_source = ColumnDataSource(data = dict(xS=[], xE=[], yS=[], yE=[]))
# create vector of forces applied during simulation
ForceList = [0,0]
# create initial
Active=False
oscForceAngle = pi/2
oscAmp = 200.0
omega = 1
alpha=0.5
Omega0=0.01
dt = 0.1
t=0.0
# create integrator
Int = Integrator([topMass,mainMass],oscAmp,dashpot)

## functions

def evolve():
    global topMass, mainMass, oscForceAngle, oscAmp, omega, dt, t, displacement_range, time_range
    t+=dt
    # current force applied to main mass
    F=oscAmp*cos(oscForceAngle)
    mainMass.applyForce(Coord(0,F),None)
    # make system evolve by time dt
    Int.evolve(dt,oscForceAngle,omega)
    # calculate force at next timestep
    oscForceAngle+=omega*dt
    
    ## draw force arrow
    h=mainMass.getTop()
    
    ###########################################################################
    # Stream the new displacement to the displacement-time diagram
    mainMass_center_y = x1
    #mainMass_height   = h
    topMass_center_y = x2
    #topMass_height   = 4
    
    mainMass_position = mainMass.currentPos['y'][0]#+mainMass.currentPos['y'][1]/2
    topMass_position = topMass.currentPos['y'][0]#+topMass.currentPos['y'][1]/2

    mainMass_displacement = mainMass_position - mainMass_center_y#-mainMass_height/2
    topMass_displacement = topMass_position - topMass_center_y#-topMass_height/2

    print('topMass_displacement = ',topMass_displacement)
    mainMass_displacementTime_source.stream(
                                           dict(
                                                t=[t],
                                                y=[mainMass_displacement]
                                               )
                                          )
    topMass_displacementTime_source.stream(
                                           dict(
                                                t=[t],
                                                y=[topMass_displacement]
                                               )
                                          )
                                           
    # Change boundaries of displacement-time plot if exceeded
    # Determine the bigger displacement achieved by the two masses
    bigger_displacement = max(mainMass_displacement, topMass_displacement)
    smaller_displacement = min(mainMass_displacement, topMass_displacement)
    
    if bigger_displacement > displacement_range.end:
        #displacement_range.start = -abs(bigger_displacement)*1.1 
        displacement_range.end =  abs(bigger_displacement)*1.1  # multiplied by 1.1 for having an adsmall margin
    if smaller_displacement < displacement_range.start:
        displacement_range.start = smaller_displacement*1.1
    if t > time_range.end:
        time_range.end = t*2
    ###########################################################################
    
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
def calculateGraphPlot():
    global lam_input, kappa_input, mass_input, oscAmp, AmplitudeFrequency
    global m1, m2, k1, k2, c2
    # prepare vectors
    omega=[]
    Amplitude=[]
    
    # calculate points on graph
    for i in range(1,201):
        # find omega
        omega.append(i/10.0)
        om=i/10.0
        
        # find amplitude
        num=(c2/om)**2+(k2/om**2-m2)**2
        denom=((k1/om-m1*om)*(k2/om-m2*om)-k2*m2)**2+(c2*(k1/om-om*(m1+m2)))**2
        if (denom!=0):
            Amplitude.append(oscAmp*sqrt(num/denom))
        else:
            Amplitude.append(100000)
    
    # add calculated values to graph
    AmplitudeFrequency.data=dict(omega=omega,A=Amplitude)

def omegaScanStep():
    global Omega0, alpha, t, k1, k2, m1, m2, c2
    om=Omega0+alpha*t
    xi = sqrt(k2/m2) / om
    Dmod = c2/2.0/sqrt(m2*k2)
    
    A = k2-m2*om*om
    B = c2*om
    C = k1*k2-(k1*m2+k2*m1+m2*k2)*om*om+m1*m2*om*om*om*om
    D = (k1-(m1+m2)*om*om)*c2*om
    E = xi * xi - 1.0
    F = 2.0 * Dmod * xi
    G = C * E - D * F
    H = C * F + D * E
    
    norm = C*C+D*D
    norm2 = G*G+H*H
    
    if (norm!=0):
        x1re = (A*C+B*D) / norm
        x1im = (B*C-A*D) / norm
    else:
        x1re = 1000000
        x1im = 1000000
    if (norm2!=0):
        x2re = (A*G+B*H) / norm2
        x2im = (B*G-A*H) / norm2
    else:
        x1re = 1000000
        x1im = 1000000
    
    y0 = sqrt(x1re * x1re + x1im * x1im)
    y1 = -atan2(x1im , x1re)
    y2 = sqrt(x2re * x2re + x2im * x2im)
    y3 = -atan2(x2im , x2re)
    
    d = (4.0 * alpha * t + Omega0)*t
    
    global mainMass, Arrow_source, topMass, baseSpring, dashpot, spring, Position
    start = x1 + oscAmp * y0 * cos(d + y1)
    end = x2 + oscAmp * y2 * cos(d + y3) + oscAmp * y0 * cos(d + y1)
    mainMass.moveTo(-6,start,12,h)
    Arrow_source.data=dict(xS=[3], xE=[3], yS=[start+h], yE=[start+h+2])
    topMass.moveTo(-5,end,4,4)
    baseSpring.compressTo(Coord(0,0),Coord(0,start))
    dashpot.compressTo(Coord(-2,end),Coord(-2,start+h),1)
    dashpot.compressTo(Coord(-2,end),Coord(-2,start+h),1)
    spring.compressTo(Coord(-4,end),Coord(-4,start+h))
    Position.data=dict(om=[om],A=[oscAmp*y0])
    if (om>10.0):
        global Active, omega_input
        curdoc().remove_periodic_callback(omegaScanStep)
        Active=False
        Arrow_source.data=dict(xS=[], xE=[], yS=[], yE=[])
        omega_input.value=om
    t+=0.05

# draw title in the middle
title_box = Div(text="""<h2 style="text-align:center;">Schwingungstilger (Tuned mass damper)</h2>""",width=1000)

## create simulation drawing
fig = figure(title="", x_range=(-7,7), y_range=(0,20),width=350,height=500)
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
p = figure(title="", tools="",x_range=(0,10),y_range=(0,5),height=500)
p.axis.major_label_text_font_size="12pt"
p.axis.axis_label_text_font_style="normal"
p.axis.axis_label_text_font_size="14pt"
p.xaxis.axis_label=u"\u03C9 [s\u207B\u00B9]"
p.yaxis.axis_label="Amplitude [m]"
# plot graph
p.line(x='omega',y='A',source=AmplitudeFrequency,color="black")
# show current frequency
p.ellipse(x='om',y='A', width=0.5, height=0.25, source=Position,color="#E37222")

def change_mass(attr,old,new):
    global Active
    if (not Active):
        global topMass, omega, m2
        topMass.changeMass(new)
        m2=new
        #global m1, g, k1, k2, x2, x1, h
        #l2=m2*g/k2+x2-x1-h
        #spring.changeL0(l2)
        #l1=g*(m1+m2)/k1+x1
        #baseSpring.changeL0(l1)
        # recalculate graph for new values
        calculateGraphPlot()
        change_Omega(None,None,omega)
    elif (new!=topMass.mass):
        mass_input.value=topMass.mass
## Create slider to choose mass of upper mass
mass_input = Slider(title="Masse (mass) [kg]", value=m2, start=1, end=100.0, step=1,width=400)
mass_input.on_change('value',change_mass)

def change_kappa(attr,old,new):
    global Active
    if (not Active):
        global spring, omega, k2
        spring.changeSpringConst(new)
        k2=new
#        global m1, m2, g, k1, x2, x1, h
#        l2=m2*g/k2+x2-x1-h
#        spring.changeL0(l2)
#        l1=g*(m1+m2)/k1+x1
#        baseSpring.changeL0(l1)
        # recalculate graph for new values
        calculateGraphPlot()
        # plot frequency on new graph
        change_Omega(None,None,omega)
    elif (new!=spring.kappa):
        kappa_input.value=spring.kappa
## Create slider to choose spring constant
kappa_input = Slider(title="Federsteifigkeit (Spring stiffness) [N/m]", value=k2, start=1.0, end=200, step=10,width=400)
kappa_input.on_change('value',change_kappa)

def change_lam(attr,old,new):
    global Active
    if (not Active):
        global dashpot, omega,c2
        dashpot.changeDamperCoeff(new)
        c2=new
        # recalculate graph for new values
        calculateGraphPlot()
        # plot frequency on new graph
        change_Omega(None,None,omega)
    elif (new!=dashpot.lam):
        lam_input.value=dashpot.lam
## Create slider to choose damper coefficient
lam_input = Slider(title=u"D\u00E4mpfungskonstante (Damper Coefficient) [N*s/m]", value=c2, start=0.0, end=15, step=0.1,width=400)
lam_input.on_change('value',change_lam)

def change_Omega(attr,old,new):
    if (not Active):
        global omega, oscAmp
        omega = new
        if (omega==0):
            # if no oscillation then A is natural amplitude
            Position.data=dict(om=[new],A=[AmplitudeFrequency.data['A'][0]])
        else:
            # find amplitude for current frequency from AmplitudeFrequency graph
            Position.data=dict(om=[new],A=[AmplitudeFrequency.data['A'][int(floor(new*10))-1]])
    elif (new!=omega):
        omega_input.value=omega
## Create slider to choose damper coefficient
omega_input = Slider(title=u"\u03C9 [s\u207B\u00B9]", value=1.0, start=0.0, end=20.0, step=0.1,width=400)
omega_input.on_change('value',change_Omega)

## create functions for buttons which control simulation
def stop():
    global Active
    if (Active):
#        try:
        curdoc().remove_periodic_callback(evolve)
        Active=False
#        except:
#            pass
#        try:
#            global t, phi, omega_input
#            curdoc().remove_periodic_callback(omegaScanStep)
#            Active=False
#            omega_input.value=Omega0+alpha*t
#            t=0
#            phi=0
#        except:
#            pass
def play():
    global Active
    if (not Active):
        #reset()
        curdoc().add_periodic_callback(evolve,100)
        Active=True
def reset():
    global spring, topMass, dashpot, mainMass, baseSpring, oscForceAngle, x1, x2, h, t
    mass_input.value=8.0
    kappa_input.value=80.0
    lam_input.value=3.7
    omega_input.value=1.0
    # if simulation is running, then stop it
    stop()
    # reset objects
    spring.compressTo(Coord(-4,x2),Coord(-4,x2-h))
    # (done twice to implement 0 velocity)
    dashpot.compressTo(Coord(-2,x2),Coord(-2,x2-h),0.1)
    dashpot.compressTo(Coord(-2,x2),Coord(-2,x2-h),0.1)
    baseSpring.compressTo(Coord(0,0),Coord(0,x1))
    topMass.moveTo(-5,x2,4,4)
    topMass.resetLinks(spring,(-4,x2))
    topMass.resetLinks(dashpot,(-2,x2))
    topMass.changeInitV(0)
    mainMass.moveTo(-6,x1,12,h)
    mainMass.resetLinks(spring,(-4,x2-h))
    mainMass.resetLinks(dashpot,(-2,x2-h))
    mainMass.resetLinks(baseSpring,(0,x1))
    mainMass.changeInitV(0)
    oscForceAngle = pi/2
    Arrow_source.data=dict(xS=[], xE=[], yS=[], yE=[])
    
    # Clear the displacement-time diagram related data structures
    mainMass_displacementTime_source.data=dict(t=[0],y=[0]) # Default values
    topMass_displacementTime_source.data=dict(t=[0],y=[0]) # Default values
    time_source.data=dict(x=[0],y=[0])
    
    displacement_range.start = 0
    displacement_range.end   = 0
    time_range.end   = 0
    time_range.start = 0
    
    t = 0
def omega_scan():
    global Active, t
    if (not Active):
        reset()
        t=0
        curdoc().add_periodic_callback(omegaScanStep,100)
        Active=True
        Arrow_glyph.start=ArrowHead_glyph
        Arrow_glyph.end=None

## create buttons to control simulation
stop_button = Button(label="Stop", button_type="success",width=100)
stop_button.on_click(stop)
play_button = Button(label="Play", button_type="success",width=100)
play_button.on_click(play)
reset_button = Button(label="Reset", button_type="success",width=100)
reset_button.on_click(reset)
omega_scan_button = Button(label=u"\u03C9 scan", button_type="success",width=100)
omega_scan_button.on_click(omega_scan)

# setup initial conditions
calculateGraphPlot()
change_Omega(None,None,1.0)

'''
###############################################################################
Define the displacement-time diagram for both masses
###############################################################################
'''
mainMass_displacementTime_source = ColumnDataSource(data=dict(t=[0],y=[0])) # Default values
topMass_displacementTime_source = ColumnDataSource(data=dict(t=[0],y=[0])) # Default values
time_source    = ColumnDataSource(data=dict(x=[0],y=[0]))

displacement_range = Range1d(0,0)
time_range = Range1d(0,0)

displacementTime_plot = figure(
                                plot_width = 600,
                                plot_height= 600,
                                x_range  = time_range,
                                y_range  = displacement_range,
                                title = 'Displacement-Time Diagram',
                                tools=''
                              )
displacementTime_plot.title.text_font_size = "25px"
displacementTime_plot.title.align = "center"
displacementTime_plot.axis.axis_label_text_font_size="14pt"
displacementTime_plot.xaxis.axis_label="Time [second]"
displacementTime_plot.yaxis.axis_label="Displacement [meter]"

displacementTime_plot.line(x='t',y='y', source = mainMass_displacementTime_source, color='#0033FF', legend='Main mass')
displacementTime_plot.line(x='t',y='y', source = topMass_displacementTime_source, color='#330011', legend='Top mass')

## Send to window
curdoc().add_root(column(title_box,row(column(Spacer(height=100),play_button,stop_button,reset_button,omega_scan_button),Spacer(width=10),fig,displacementTime_plot,p),
#curdoc().add_root(column(title_box,row(column(Spacer(height=100),play_button,stop_button,reset_button),Spacer(width=10),fig,test_fig),
    row(mass_input,kappa_input),row(lam_input,omega_input)))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '