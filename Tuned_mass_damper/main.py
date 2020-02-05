from __future__ import division
from tmd_spring import Spring
from tmd_dashpot import Dashpot
from tmd_mass import RectangularMass
from tmd_integrator import Integrator
from tmd_coord import Coord

from tmd_functions import Calculate_MagnificationFactor_PhaseAngle, Calculate_Current_Amplification_PhaseAngle
from tmd_functions import Clear_Time_History

from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import Slider, Button, Div, Arrow, NormalHead, Range1d, LabelSet, OpenHead, ColumnDataSource
from math import cos, sin, radians, sqrt, pi, atan2

import numpy as np
from numpy.linalg import inv

from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv, LatexSlider

## set start parameters
x1=6                #y-coordinate of main mass
x2=16               #y-coordinate of top mass
m1=5.0              #mass
m2=0.25
c1=sqrt(10)/5       #damping coefficient
c2=sqrt(10)/100
k1 = 200.0          #stiffness coefficient
k2 = 10.0

Active=False
oscForceAngle = 0   
oscAmp = 1
omega = 2*sqrt(10)  #F(t)=ascAmp*cos(omega*t+oscForceAngle)
dt = 0.01
t=0.0

## coefficients for Newmark solver
gamma = 0.5
beta = 0.25

## create masses, springs, dashpots and link them
topMass = RectangularMass(m2,-5,x2,4,4)
dashpot = Dashpot((-2,x2),(-2,x1+5),c2)
spring = Spring((-4,x2),(-4,x1+5),5,k2)

topMass.linkObj(spring,(-4,x2))
topMass.linkObj(dashpot,(-2,x2))

mainMass = RectangularMass(m1,-6,x1,12,5)
baseSpring = Spring((-1,6),(-1,0),6,k1)
baseDashpot = Dashpot((1,6),(1,0),c1)

mainMass.linkObj(spring,(-4,x1+5))
mainMass.linkObj(dashpot,(-2,x1+5))
mainMass.linkObj(baseSpring,(-1,x1))
mainMass.linkObj(baseDashpot,(1,x1))

## create matrices for equation of motion Ma+Cv+Kd = F (a: acceleration, v: velocity, d: displacement)
M = np.array([[mainMass.mass,0.],
              [0., topMass.mass]])

C = np.array([[baseDashpot.lam+dashpot.lam,-dashpot.lam],
              [-dashpot.lam,                 dashpot.lam]])

K = np.array([[baseSpring.kappa+spring.kappa,-spring.kappa],
              [-spring.kappa,                 spring.kappa]])

lhs = np.array([[0.,0.],
                [0.,0.]]) 

rhs = np.array([[0.,0.],
                [0.,0.]])

## initial conditions
velOld = np.array([0.,0.])
dispOld = np.array([0.,0.])
F0 = np.array([-1.,0.])
accOld = inv(M).dot(F0-K.dot(dispOld)-C.dot(velOld))

## create ColumnDataSources            
arrow_line   = ColumnDataSource(data = dict(x1=[3],y1=[5+x1+5],x2=[3],y2=[x1+5]))   #arrow line showing initial force
arrow_offset = ColumnDataSource(data = dict(x1=[3],y1=[x1+5+0.1],x2=[3],y2=[x1+5])) #arrow head showing initial force

m1_label_source = ColumnDataSource(data=dict(x=[0],y=[x1+2.5],t=['m']))             #'m_1' and 'm_2' label at initial position
m2_label_source = ColumnDataSource(data=dict(x=[-3],y=[x2+2],t=['m']))
m1_index_label_source = ColumnDataSource(data=dict(x=[0.6],y=[x1+2.2],t=['1']))
m2_index_label_source = ColumnDataSource(data=dict(x=[-2.4],y=[x2+1.7],t=['2']))


################################################################################
#Define the displacement-time diagram for both masses and the force-time diagram
################################################################################

## create ColumnDataSources
mainMass_displacementTime_source = ColumnDataSource(data=dict(x=[0],y=[0])) #initial displacement of main mass
topMass_displacementTime_source = ColumnDataSource(data=dict(x=[0],y=[0]))  #initial displacement of top mass
forceTime_source = ColumnDataSource(data=dict(x=[0],y=[-1]))                #initial force acting on main mass

## plot-boundaries
displacement_range = Range1d(-6,6)
force_range = Range1d(-1.2,1.2)
time_range = Range1d(0,20)

##displacement-time diagram
displacementTime_plot = figure(title="",tools=["ywheel_zoom,xwheel_pan,pan,reset"],width = 400,height= 300,x_range  = time_range,
    y_range  = displacement_range)
displacementTime_plot.axis.axis_label_text_font_size="12pt"
displacementTime_plot.axis.axis_label_text_font_style="normal"
displacementTime_plot.yaxis.axis_label="Normalized Displacement u/(F/k)"
displacementTime_plot.line(x='x',y='y', source = mainMass_displacementTime_source, color='#e37222', legend_label='Main Mass')
displacementTime_plot.line(x='x',y='y', source = topMass_displacementTime_source, color='#3070b3', legend_label='Top Mass')
displacementTime_plot.toolbar.logo = None

##force-time diagram
forceTime_plot = figure(title="",tools=["ywheel_zoom,xwheel_pan,pan,reset"],width = 400,height= 300,x_range  = time_range,
    y_range  = force_range)
forceTime_plot.axis.axis_label_text_font_size="12pt"
forceTime_plot.axis.axis_label_text_font_style="normal"
forceTime_plot.xaxis.axis_label="Time [s]"
forceTime_plot.yaxis.axis_label="Force [N]"
forceTime_plot.line(x='x',y='y', source = forceTime_source, color='black')
forceTime_plot.toolbar.logo = None


################################################################################
#Add application describtion
################################################################################

## add app description
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)


################################################################################
#Define the amplification-frequency and phase angle-frequency diagrams for both masses
################################################################################

## create ColumnDataSources
mainMass_amplificationFrequency_source = ColumnDataSource(data=dict(x=[0],y=[0]))   #default values
mainMass_phaseAngleFrequency_source = ColumnDataSource(data=dict(x=[0],y=[0]))      #default values
Amplification_current_source = ColumnDataSource(data=dict(x=[0],y=[0]))             #spot showing current amplification
PhaseAngle_current_source = ColumnDataSource(data=dict(x=[0],y=[0]))                #spot showing current phase angle

## plot-boundaries
Amplification_range = Range1d(0,30)
PhaseAngle_range = Range1d(0,3.5)       #(0,pi)
Frequency_range = Range1d(0,5)

## amplification-frequency diagram
Amplification_Frequency_plot = figure(plot_width = 400,plot_height= 300,x_range  = Frequency_range,y_range  = Amplification_range, tools='')
Amplification_Frequency_plot.axis.axis_label_text_font_size="12pt"
Amplification_Frequency_plot.axis.axis_label_text_font_style="normal"
Amplification_Frequency_plot.yaxis.axis_label="Amplification"
Amplification_Frequency_plot.line(x='x',y='y', source = mainMass_amplificationFrequency_source, color="#a2ad00")
Amplification_Frequency_plot.circle(x='x',y='y', color="#e37222", source=Amplification_current_source, radius=0.1)
Amplification_Frequency_plot.toolbar.logo = None

## phase angle-frequency diagram
PhaseAngle_Frequency_plot = figure(plot_width = 400,plot_height= 300,x_range  = Frequency_range,y_range  = PhaseAngle_range, tools='')
PhaseAngle_Frequency_plot.axis.axis_label_text_font_size="12pt"
PhaseAngle_Frequency_plot.axis.axis_label_text_font_style="normal"
PhaseAngle_Frequency_plot.xaxis.axis_label="Excitation Frequency Ratio"
PhaseAngle_Frequency_plot.yaxis.axis_label="Phase Angle [rad]"
PhaseAngle_Frequency_plot.line(x='x',y='y', source = mainMass_phaseAngleFrequency_source, color="#a2ad00")
PhaseAngle_Frequency_plot.circle(x='x',y='y', color="#e37222", source=PhaseAngle_current_source, radius=0.1)
PhaseAngle_Frequency_plot.toolbar.logo = None


################################################################################
#Create simulation drawing
################################################################################

fig = figure(title="", tools = "", x_range=(-7,7), y_range=(-5,35),width=300,height=550)
fig.axis.visible = False
fig.grid.visible = False
fig.outline_line_color = None
fig.toolbar.logo = None
fig.add_layout(LabelSet(x='x',y='y',text='t',text_color='black',text_font_size="15pt",level='overlay',text_baseline="middle",
    text_align="center",source=m2_label_source))
fig.add_layout(LabelSet(x='x',y='y',text='t',text_color='black',text_font_size="15pt",level='overlay',text_baseline="middle",
    text_align="center",source=m1_label_source))
fig.add_layout(LabelSet(x='x',y='y',text='t',text_color='black',text_font_size="10pt",level='overlay',text_baseline="middle",
    text_align="center",source=m2_index_label_source))
fig.add_layout(LabelSet(x='x',y='y',text='t',text_color='black',text_font_size="10pt",level='overlay',text_baseline="middle",
    text_align="center",source=m1_index_label_source))

# add objects to plot
spring.plot(fig,width=2)
baseSpring.plot(fig,width=2)
dashpot.plot(fig,width=2)
mainMass.plot(fig)
topMass.plot(fig)
baseDashpot.plot(fig,width=2)

fig.add_layout(Arrow(end=None,line_color="#e37222",line_width=2,x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=arrow_line))
fig.add_layout(Arrow(end=NormalHead(fill_color="#e37222",line_color="#e37222"),line_color="#e37222",line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=arrow_offset))
fig.line(x=[-3,3],y=[0,0],color="black",line_width=3)
fig.multi_line(xs=[[-3.75,-3],[-2.75,-2],[-1.75,-1],[-0.75,0],[0.25,1],[1.25,2],[2.25,3]],
    ys=[[-0.75,0],[-0.75,0],[-0.75,0],[-0.75,0],[-0.75,0],[-0.75,0],[-0.75,0]],color="black",line_width=3)


################################################################################
#functions
################################################################################

## set all objects to initial setting
def init_pos():
    topMass.moveTo(-5,x2,4,4)
    mainMass.moveTo(-6,x1,12,5)
    spring.compressTo(Coord(-4,x2),Coord(-4,x1+5))
    dashpot.compressTo(Coord(-2,x2),Coord(-2,x1+5),0)
    baseSpring.compressTo(Coord(-1,x1),Coord(-1,0))
    baseDashpot.compressTo(Coord(1,x1),Coord(1,0),0)
    topMass.resetLinks(spring,(-4,x2))
    topMass.resetLinks(dashpot,(-2,x2))
    mainMass.resetLinks(spring,(-4,x1+5))
    mainMass.resetLinks(dashpot,(-2,x1+5))
    mainMass.resetLinks(baseSpring,(-1,x1))
    mainMass.resetLinks(baseDashpot,(1,x1))

## called periodically to solve equation of motion
def evolve():
    global topMass, mainMass, oscForceAngle, oscAmp, omega, dt, t, mainMass_displacementTime_source, topMass_displacementTime_source, M, C, K, velOld, dispOld, lhs, F0, rhs, gamma, beta, accOld, x1, x2
    oscForceAngle+=omega*dt
    t+=dt
    
    F1_next=-oscAmp*cos(oscForceAngle)      #force applied to main mass
    F_next = np.array([[F1_next,0]])
    
    # Newmark method with gamma = 0.5 and beta = 0.25:
    # v_n+1 = v_n+dt*[(1-gamma)*a_n+gamma*a_n+1]
    # d_n+1 = d_n+dt*v_n+dt*dt*[(0.5-beta)*a_n+beta*a_n+1]
    # Ma_n+1 + Cv_n+1 + Kd_n+1 = F_n+1
    
    lhs = M+gamma*dt*C+beta*dt*dt*K
    rhs = F_next-C.dot(velOld+(1-gamma)*dt*accOld)-K.dot(dispOld+dt*velOld+dt*dt*(0.5-beta)*accOld)
    rhs_array = np.array([rhs[0][0],rhs[0][1]])
    
    accNew = inv(lhs).dot(rhs_array)
    velNew = velOld+(1-gamma)*dt*accOld+gamma*dt*accNew
    dispNew = dispOld+dt*velOld+dt*dt*(0.5-beta)*accOld+dt*dt*beta*accNew
    
    mainMass.move(Coord(0,dispNew[0]-dispOld[0])*baseSpring.kappa)      #move main mass by calculated displacement normalized with spring stiffness
    topMass.move(Coord(0,dispNew[1]-dispOld[1])*spring.kappa)           #move top mass by calculated displacement normalized with spring stiffness
   
    accOld = accNew         #a_n for next time step
    velOld = velNew         #v_n for next time step
    dispOld = dispNew       #d_n for next time step

    h1=mainMass.getTop()
    h2=topMass.getTop()
    
    mainMass_position = mainMass.currentPos['y'][0]
    topMass_position = topMass.currentPos['y'][0]
    mainMass_displacement = mainMass_position - x1
    topMass_displacement = topMass_position - x2
    mainMass_displacementTime_source.stream(dict(x=[t],y=[mainMass_displacement]))
    topMass_displacementTime_source.stream(dict(x=[t],y=[topMass_displacement]))
    forceTime_source.stream(dict(x=[t],y=[F1_next]))                                       
    
    # update force arrow
    F_for_vis = F1_next*5 #scale
    # draw arrow in correct direction
    if (F1_next<1e-10):
        arrow_line.stream(dict(x1=[3], x2=[3], y1=[h1-F_for_vis], y2=[h1]),rollover=1)
        arrow_offset.stream(dict(x1=[3], x2=[3], y1=[h1+0.1], y2=[h1]),rollover=1)
    else:
        arrow_line.stream(dict(x1=[3], x2=[3], y1=[h1-F_for_vis], y2=[h1]),rollover=1)
        arrow_offset.stream(dict(x1=[3], x2=[3], y1=[h1-0.1], y2=[h1]),rollover=1)

    # update position of m_1 and m_2 label    
    m1_label_source.data=dict(x=[0], y=[h1-2.5], t=['m'])
    m2_label_source.data=dict(x=[-3], y=[h2-2], t=['m'])
    m1_index_label_source.data=dict(x=[0.6], y=[h1-2.8], t=['1'])
    m2_index_label_source.data=dict(x=[-2.4], y=[h2-2.3], t=['2'])


def change_mass_ratio(attr,old,new):
    global M, accOld
    Update_system()
    Update_current_state()
    topMass.changeMass(new*m1)
    M = np.array([[mainMass.mass,0.],
                  [0., topMass.mass]])
    accOld = inv(M).dot(F0-K.dot(dispOld)-C.dot(velOld))

## Create slider to choose mass of upper mass
mass_ratio_input = LatexSlider(title="\\text{Mass Ratio } \mu = \\frac{m_2}{m_1} = ", value=m2/m1, start=0.01, end=0.20, step=0.01, width=450)
mass_ratio_input.on_change('value',change_mass_ratio)

def change_tuning(attr,old,new):
    global K, accOld
    Update_system()
    Update_current_state()
    spring.changeSpringConst(new*new*k1*mass_ratio_input.value)
    K = np.array([[baseSpring.kappa+spring.kappa,-spring.kappa],
                 [-spring.kappa,                 spring.kappa]])
    accOld = inv(M).dot(F0-K.dot(dispOld)-C.dot(velOld))

## Create slider to choose spring constant
tuning_input = LatexSlider(title="\\text{TMD Tuning } \kappa = \\frac{\omega_2}{\omega_1} = \sqrt{\\frac{k_2 \cdot m_1}{k_1 \cdot m_2}} = ", value=sqrt(k2*m1/(k1*m2)), start=0.7, end=1.3, step=0.01, width=450)
tuning_input.on_change('value',change_tuning)

def change_D1(attr,old,new):
    global C, accOld
    Update_system()
    Update_current_state()
    baseDashpot.changeDamperCoeff(new*2*m1*sqrt(k1/m1))
    C = np.array([[baseDashpot.lam+dashpot.lam,-dashpot.lam],
                 [-dashpot.lam,                 dashpot.lam]])
    accOld = inv(M).dot(F0-K.dot(dispOld)-C.dot(velOld))

## Create slider to choose base damper coefficient
#D1_input = LatexSlider(title="\\text{Percentage of Critical Damping of Main Mass } D_1 = \\frac{c_1}{2 \cdot m_1 \cdot \omega_1} = ", value=c1/(2*m1*sqrt(k1/m1)), start=0.001, end=0.1, step=0.001, width=450)
D1_input = LatexSlider(title="\\text{Percentage of Critical Damping of Main Mass } D_1 = \\frac{c_1}{2 \cdot m_1 \cdot \omega_1} = ", value=c1/(2*m1*sqrt(k1/m1)), start=0.01, end=0.1, step=0.01, width=450)
D1_input.on_change('value',change_D1)

def change_D2(attr,old,new):
    global C, accOld
    Update_system()
    Update_current_state()
    dashpot.changeDamperCoeff(new*2*mass_ratio_input.value*m1*sqrt(tuning_input.value*tuning_input.value*k1/m1))
    C = np.array([[baseDashpot.lam+dashpot.lam,-dashpot.lam],
                 [-dashpot.lam,                 dashpot.lam]])
    accOld = inv(M).dot(F0-K.dot(dispOld)-C.dot(velOld))

## Create slider to choose upper damper coefficient
#D2_input = LatexSlider(title="\\text{Percentage of Critical Damping of Top Mass } D_2  = \\frac{c_2}{2 \cdot m_2 \cdot \omega_2} = ", value=c2/(2*m2*sqrt(k2/m2)), start=0.001, end=0.1, step=0.001, width=450)
D2_input = LatexSlider(title="\\text{Percentage of Critical Damping of Top Mass } D_2  = \\frac{c_2}{2 \cdot m_2 \cdot \omega_2} = ", value=c2/(2*m2*sqrt(k2/m2)), start=0.01, end=0.1, step=0.01, width=450)
D2_input.on_change('value',change_D2)

def change_frequeny_ratio(attr,old,new):
    global omega, oscAmp
    omega = new*sqrt(k1/m1)
    Update_current_state()

## Create slider to choose excitation frequency omega
frequency_ratio_input = LatexSlider(title="\\text{Excitation Frequency Ratio } \eta  = \\frac{\Omega}{\omega_1} = ", value=omega/sqrt(k1/m1), start=0.0, end=5.0, step=0.05, width=400)
frequency_ratio_input.on_change('value',change_frequeny_ratio)

def disable_all_sliders(d=True):

    mass_ratio_input.disabled = d
    tuning_input.disabled = d
    D1_input.disabled = d
    D2_input.disabled = d
    frequency_ratio_input.disabled = d

def play_pause():
    if play_pause_button.label == "Play":
        play()
    else: 
        pause()

def play():
    global Active, g1BaseOscillator
    if (not Active):
        disable_all_sliders(True)       #while the app is running, it's not possible to change any values
        #Add a callback to be invoked on a session periodically
        g1BaseOscillator = curdoc().add_periodic_callback(evolve,dt*1000)
        play_pause_button.label = "Pause"
        Active=True

def pause():
    global Active, g1BaseOscillator
    if (Active):
        curdoc().remove_periodic_callback(g1BaseOscillator)
        play_pause_button.label = "Play"
        Active=False

def stop():
    #set everything except slider values to initial settings
    global spring, topMass, dashpot, mainMass, baseSpring, baseDashpot, oscForceAngle, x1, x2, t, accOld, velOld, dispOld, F0, M, K , C, F0
    disable_all_sliders(False)
    pause()
    t=0      
    oscForceAngle = 0            
    init_pos()   
    # Clear the displacement-time diagram related data structures
    mainMass_displacementTime_source.data=dict(x=[0],y=[0]) 
    topMass_displacementTime_source.data=dict(x=[0],y=[0]) 
    forceTime_source.data=dict(x=[0],y=[-1])
    arrow_line.stream(dict(x1=[3], x2=[3], y1=[x1+5+5], y2=[x1+5]),rollover=1)
    arrow_offset.stream(dict(x1=[3], x2=[3], y1=[x1+5+0.1], y2=[x1+5]),rollover=1)
    m1_label_source.data=dict(x=[0], y=[x1+2.5], t=['m'])
    m2_label_source.data=dict(x=[-3], y=[x2+2], t=['m'])
    m1_index_label_source.data=dict(x=[0.6], y=[x1+2.2], t=['1'])
    m2_index_label_source.data=dict(x=[-2.4], y=[x2+1.7], t=['2'])
    velOld = np.array([0.,0.])
    dispOld = np.array([0.,0.])
    accOld = inv(M).dot(F0-K.dot(dispOld)-C.dot(velOld))

def reset():
    mass_ratio_input.value = m2/m1
    tuning_input.value = sqrt(k2*m1/(m2*k1))
    D1_input.value = c1/(2*m1*sqrt(k1/m1))
    D2_input.value = c2/(2*m2*sqrt(k2/m2))
    frequency_ratio_input.value = (2*sqrt(10))/sqrt(k1/m1)
    stop()

def Update_system():    
    Calculate_MagnificationFactor_PhaseAngle(mass_ratio_input.value,tuning_input.value,D1_input.value,D2_input.value,mainMass_amplificationFrequency_source,mainMass_phaseAngleFrequency_source,k1,m1)
    
def Update_current_state():
    Calculate_Current_Amplification_PhaseAngle(frequency_ratio_input.value,tuning_input.value,mass_ratio_input.value,D1_input.value,D2_input.value,Amplification_current_source,PhaseAngle_current_source,k1,m1)

## create buttons to control simulation
play_pause_button = Button(label="Play", button_type="success",width=100)
play_pause_button.on_click(play_pause)
reset_button = Button(label="Reset", button_type="success",width=100)
reset_button.on_click(reset)
stop_button = Button(label="Stop", button_type="success",width=100)
stop_button.on_click(stop)

## Fill the Amplification factor and Phase angle diagrams
Update_system()
Update_current_state()

## Send to window
curdoc().add_root(column(description,row(column(Spacer(height=200),play_pause_button,stop_button,reset_button),fig,column(Amplification_Frequency_plot,PhaseAngle_Frequency_plot),
Spacer(width=50),column(displacementTime_plot,forceTime_plot)),
Spacer(height=30),row(column(mass_ratio_input,tuning_input,column(D1_input,D2_input)),                                     
Spacer(width=420),column(frequency_ratio_input))))
                                  
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '