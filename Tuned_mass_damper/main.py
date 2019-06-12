from __future__ import division
from TMD_Spring import *
from TMD_Dashpot import *
from TMD_Mass import *
from TMD_Integrator import *
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import Slider, Button, Div, Arrow, Range1d, LabelSet,NormalHead,ColumnDataSource,HoverTool
from math import cos, sin, radians, sqrt, pi, atan2
from os.path import dirname, join, split
from TMD_Functions import Calculate_MagnificationFactor_PhaseAngle, Calculate_Current_Amplification_PhaseAngle
from TMD_Functions import Clear_Time_History
import numpy as np
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.layouts import gridplot


from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexDiv, LatexLabel, LatexLabelSet, LatexSlider, LatexLegend
## create and link objects
##Create column data source for all global variables
glob_callback = ColumnDataSource(data=dict(cid=[None]))






glob_active   = ColumnDataSource(data=dict(Active=[False]))
glob_t        = ColumnDataSource(data=dict(val=[0]))
glob_g        = ColumnDataSource(data=dict(val=[9.81]))
glob_x1    = ColumnDataSource(data=dict(val=[6]))
glob_x2    = ColumnDataSource(data=dict(val=[16]))
glob_h   = ColumnDataSource(data=dict(val=[5]))
glob_m1    = ColumnDataSource(data=dict(val=[100]))
#glob_m2    = ColumnDataSource(data=dict(val=[8.0]))
#glob_c2    = ColumnDataSource(data=dict(val=[3.7]))
glob_k1    = ColumnDataSource(data=dict(val=[1000.0]))
#glob_k2    = ColumnDataSource(data=dict(val=[80.0]))

glob_Forced          = ColumnDataSource(data=dict(val=[0.004]))
glob_Muu           = ColumnDataSource(data=dict(val=[0.5]))
glob_Dd           = ColumnDataSource(data=dict(val=[0.5]))
[Dd]=glob_Dd.data["val"]
[Muu ]     = glob_Muu.data["val"]

[m1 ]     = glob_m1.data["val"]

#print(Muu,m1)
m2=(Muu*m1)
glob_m2         = ColumnDataSource(data=dict(val=[m2]))
#print (m2)
#print (m2)

#[c2 ]     = glob_c2 .data["val"]
[x1 ]     = glob_x1.data["val"]
[x2]     = glob_x2.data["val"]
[h ]     = glob_h.data["val"]
# create upper mass
[k1]     = glob_k1.data["val"]
[Forced]=glob_Forced.data["val"]
#print('Forced1=',Forced)
glob_Omega0=ColumnDataSource(data=dict(val=[0.01]))
   
[Omega0]=glob_Omega0.data["val"]

omega=Omega0/Forced
#print()
glob_omega          = ColumnDataSource(data=dict(val=[omega]))
[omega]=glob_omega.data["val"]
#omega=3

#omega=1

c2=2*omega*m2*Dd
glob_c2         = ColumnDataSource(data=dict(val=[c2]))
[c2]=glob_c2.data["val"]

#print (c2)

#print(c2)
k2=(omega*omega)*m2
glob_k2       = ColumnDataSource(data=dict(val=[k2]))

print('m1',m1,'m2',m2,'c1',c2,'k1',k2,'omega',omega)
#print('Omega=',omega)
#print('K2=', k2)
#k2=80
#m2=8

#print ('m2 and k2',m2,k2)

#[k2]     = glob_k2.data["val"]

parameters    = ColumnDataSource(data = dict(names1=['Damping C2','Stiffness K2','m1','m2','omega','Damping ratio','Muu','Forcing ratio'],values1=[round(c2,4),round(k2,4),round(m1,4),round(m2,4),round(omega,4),round(Dd,4),round(Muu,4),round(Forced,4)]))
topMass = RectangularMass(m2,-5,x2,4,4)
glob_topMass   = ColumnDataSource(data = dict(topMass = [topMass]))
[topMass]    = glob_topMass.data["topMass"]
# create dashpot and spring linked to upper mass
dashpot = Dashpot((-2,x2),(-2,x1+h),c2)
glob_dashpot   = ColumnDataSource(data = dict(dashpot = [dashpot]))
[dashpot ]    = glob_dashpot.data["dashpot"]
# l2 = m2*g/k2+x2-x1-h so that start is at equilibrium
[g]     = glob_g.data["val"] 
l2=m2*g/k2+x2-x1-h
spring = Spring((-4,x2),(-4,x1+h),l2,k2)
glob_spring    = ColumnDataSource(data = dict(spring = [spring]))
[spring]    = glob_spring.data["spring"]
# link objects to upper mass
topMass.linkObj(spring,(-4,x2))
topMass.linkObj(dashpot,(-2,x2))
# create base spring
# l1 = g*(m1+m2)/k1+x1 for equilibrium
# where k2=100,k1=10000,x1=6,x2=16, m1=100,m2=1, h=5
l1=g*(m1+m2)/k1+x1
baseSpring = Spring((0,0),(0,6),l1,k1)
glob_baseSpring    = ColumnDataSource(data = dict(baseSpring = [baseSpring]))
[baseSpring]    = glob_baseSpring.data["baseSpring"]
# link objects to main large mass
mainMass = RectangularMass(m1,-6,x1,12,h)

glob_mainMass= ColumnDataSource(data = dict(mainMass = [mainMass]))
[mainMass]    = glob_mainMass.data["mainMass"]
mainMass.linkObj(spring,(-4,x1+h))
mainMass.linkObj(dashpot,(-2,x1+h))
mainMass.linkObj(baseSpring,(0,x1))
#glob_omega=ColumnDataSource(data=dict(val=[1]))
#[omega] = glob_omega.data["val"]
#[Forced]=glob_Forced.data["val"]
#glob_Omega0=ColumnDataSource(data=dict(val=[0.01]))
#[Omega0]=glob_Omega0.data["val"]
#omega=Omega0/Forced


# create ColumnDataSource for Amplitude as a function of frequency
AmplitudeFrequency = ColumnDataSource(data = dict(omega=[],A=[]))
# create ColumnDataSource for spot showing current frequency
Position = ColumnDataSource(data = dict(om=[],A=[]))
# create ColumnDataSource for arrow showing force
Arrow_source = ColumnDataSource(data = dict(xS=[], xE=[], yS=[], yE=[]))
# create ColumnDataSource for force label
ForceLabel_source = ColumnDataSource(data=dict(x=[],y=[],t=[]))
# create vector of forces applied during simulation
ForceList = [0,0]
# create initial
glob_oscForceAngle=ColumnDataSource(data=dict(val=[pi/2]))
[oscForceAngle ]     = glob_oscForceAngle.data["val"]
glob_oscAmp=ColumnDataSource(data=dict(val=[200.0]))
[oscAmp ]     = glob_oscAmp.data["val"]
#glob_Omega0=ColumnDataSource(data=dict(val=[0.01]))
glob_alpha=ColumnDataSource(data=dict(val=[0.5]))
#############################################################################################################33
# create integrator
Int = Integrator([topMass,mainMass],oscAmp,dashpot)

'''
###############################################################################
Define the displacement-time diagram for both masses
###############################################################################
'''
mainMass_displacementTime_source = ColumnDataSource(data=dict(x=[0],y=[0])) # Default values
topMass_displacementTime_source = ColumnDataSource(data=dict(x=[0],y=[0])) # Default values

# Initial space and time plot-boundaries
displacement_range = Range1d(-4,4)
glob_displacement_range   = ColumnDataSource(data = dict(displacement_range = [displacement_range]))
[displacement_range ]    = glob_displacement_range.data["displacement_range"]

time_range = Range1d(0,15)
glob_time_range   = ColumnDataSource(data = dict(time_range = [time_range]))
[time_range ]    = glob_time_range.data["time_range"]
hover = HoverTool(tooltips=[("time","@x s"), ("displacement","@y m")])
displacementTime_plot = figure(
                               toolbar_location="right", tools=[hover,"ywheel_zoom,xwheel_pan,pan,reset"],
                                plot_height= 550,
                                
                                x_range  = time_range,
                                y_range  = displacement_range,
                                title = 'Displacement-Time Plot',
                                #tools=''
                              )
displacementTime_plot.title.text_font_size = "20px"
displacementTime_plot.title.align = "center"
displacementTime_plot.axis.axis_label_text_font_size="14pt"
displacementTime_plot.xaxis.axis_label="Time [second]"
displacementTime_plot.yaxis.axis_label="Displacement [meter]"

displacementTime_plot.line(x='x',y='y', source = mainMass_displacementTime_source, color="#e37222",line_width=2, legend='Main mass')
displacementTime_plot.line(x='x',y='y', source = topMass_displacementTime_source, color="#a2ad00", legend='Top mass')
                           

'''
###############################################################################
Add application describtion
###############################################################################
'''
# add app description
description_filename = join(dirname(__file__), "description.html")
description = Div(text=open(description_filename).read(), render_as_text=False, width=1325)

'''
###############################################################################
Define the amplification-frequency and phase angle-frequency diagrams for both masses
###############################################################################
'''
mainMass_amplificationFrequency_source = ColumnDataSource(data=dict(x=[0],y=[0]))
topMass_amplificationFrequency_source = ColumnDataSource(data=dict(x=[0],y=[0]))
mainMass_phaseAngleFrequency_source = ColumnDataSource(data=dict(x=[0],y=[0]))
topMass_phaseAngleFrequency_source = ColumnDataSource(data=dict(x=[0],y=[0]))
Amplification_current_source = ColumnDataSource(data=dict(x=[0],y=[0],c=['#000000']))
PhaseAngle_current_source = ColumnDataSource(data=dict(x=[0],y=[0],c=['#000000']))

Amplificaiton_range = Range1d(0,0)
PhaseAngle_range = Range1d(0,0)
Frequency_range = Range1d(0,0)

Amplification_Frequency_plot = figure(
                                plot_width = 300,
                                plot_height= 300,
                                x_range  = Frequency_range,
                                y_range  = Amplificaiton_range,
                                title = 'Amplification Factor vs. Frequency Ratio Plot',
                                tools=''
                              )
Amplification_Frequency_plot.title.text_font_size = "11.5px"
Amplification_Frequency_plot.title.align = "center"
Amplification_Frequency_plot.axis.axis_label_text_font_size="10pt"
Amplification_Frequency_plot.xaxis.axis_label="Frequency Ratio"
Amplification_Frequency_plot.yaxis.axis_label="Amplification Factor"

PhaseAngle_Frequency_plot = figure(
                                plot_width = 300,
                                plot_height= 300,
                                x_range  = Frequency_range,
                                y_range  = PhaseAngle_range,
                                title = 'Phase Angle vs. Frequency Ratio Plot',
                                tools=''
                              )
PhaseAngle_Frequency_plot.title.text_font_size = "11.5px"
PhaseAngle_Frequency_plot.title.align = "center"
PhaseAngle_Frequency_plot.axis.axis_label_text_font_size="10pt"
PhaseAngle_Frequency_plot.xaxis.axis_label="Frequency Ratio"
PhaseAngle_Frequency_plot.yaxis.axis_label="Phase Angle [rad]"

Amplification_Frequency_plot.line(x='x',y='y', source = mainMass_amplificationFrequency_source, color="#a2ad00", legend='Main mass')


PhaseAngle_Frequency_plot.line(x='x',y='y', source = mainMass_phaseAngleFrequency_source, color="#a2ad00", legend='Main mass')


Amplification_Frequency_plot.circle(x='x',y='y', color="#e37222", source=Amplification_current_source, radius=0.1)
PhaseAngle_Frequency_plot.circle(x='x',y='y', color="#e37222", source=PhaseAngle_current_source, radius=0.1)
## functions
PhaseAngle_Frequency_plot.toolbar.logo = None
PhaseAngle_Frequency_plot.toolbar_location = None
Amplification_Frequency_plot.toolbar.logo = None
Amplification_Frequency_plot.toolbar_location = None

displacementTime_plot.toolbar.logo = None
#displacementTime_plot.toolbar_location = None

#print('Forced21=',Forced)

def evolve():
#    [topMass] = glob_topMass.data["topMass"]
#    [Forced]=glob_Forced.data["val"]
#    [Muu ]     = glob_Muu.data["val"]
#    [m1 ]     = glob_m1.data["val"]
#    [Omega0]=glob_Omega0.data["val"]
#    [Dd]=glob_Dd.data["val"]
#    omega=Omega0/Forced
#    m2=(Muu*m1)
#    c2=2*omega*m2*Dd
#    
#    k2=(omega*omega)*m2
#    
#    [m1 ]     = glob_m1.data["val"]
#    [k1 ]     = glob_k1.data["val"]
#    [m2 ]     = glob_m2.data["val"]
#    [c2 ]     = glob_c2.data["val"]
#    [k2 ]     = glob_k2.data["val"]
    [omega]=glob_omega.data["val"]
    
#   
    [Omega0]=glob_Omega0.data["val"]
    [displacement_range ]    = glob_displacement_range.data["displacement_range"]
    [time_range ]    = glob_time_range.data["time_range"]
#    [Forced]=glob_Forced.data["val"]
#    [glob_Omega0]=ColumnDataSource(data=dict(val=[0.01]))
    [Omega0]=glob_Omega0.data["val"]
#    print('Forced evolve=',Forced)
#    omega=Omega0/Forced
    
#    omega=1
#    print('Forced evolve2=',Forced)
#    print('glob_Omega0=',Omega0)
#    print('omega=',omega)
#    [omega] = glob_omega.data["val"]
    [topMass]    = glob_topMass.data["topMass"]
    [mainMass]    = glob_mainMass.data["mainMass"]
    [oscAmp]     = glob_oscAmp.data["val"]
    [oscForceAngle] = glob_oscForceAngle.data["val"]
    [t] = glob_t.data["val"]
    t+=0.1
    glob_t.data = dict(val=[t])
    
    # current force applied to main mass
    F=oscAmp*cos(oscForceAngle)
    mainMass.applyForce(Coord(0,F),None)
    # make system evolve by time dt
    Int.evolve(0.1,oscForceAngle,omega)
    # calculate force at next timestep
    oscForceAngle+=omega*0.1
    glob_oscForceAngle.data = dict(val = [oscForceAngle])
    print('Evolve','m1',m1,'m2',m2,'c2',c2,'k2',k2,'omega',omega)
    
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

    #print('topMass_displacement = ',topMass_displacement)
    mainMass_displacementTime_source.stream(
                                           dict(
                                                x=[t],
                                                y=[mainMass_displacement]
                                               )
                                          )
    topMass_displacementTime_source.stream(
                                           dict(
                                                x=[t],
                                                y=[topMass_displacement]
                                               )
                                          )
                                           
    # Change boundaries of displacement-time plot if exceeded
    # Determine the bigger displacement achieved by the two masses
    bigger_displacement = max(mainMass_displacement, topMass_displacement)
    smaller_displacement = min(mainMass_displacement, topMass_displacement)
    
    if bigger_displacement > displacement_range.end:
        #displacement_range.start = -abs(bigger_displacement)*1.1 
        displacement_range.end =  abs(bigger_displacement)*1.01  # multiplied by 1.1 for having an adsmall margin
    if smaller_displacement < displacement_range.start:
        displacement_range.start = smaller_displacement*1.01
    if t > time_range.end:
        time_range.end = t*1.1
    ###########################################################################
      
    # reduce F to make arrow normal sized on drawing
    F_for_vis = F/50.0
    OscAmp_for_vis = oscAmp/50
    # draw arrow in correct direction
    if (F<0):
        Arrow_source.data=dict(xS=[3], xE=[3], yS=[h], yE=[h-F_for_vis])
        Arrow_glyph.start=ArrowHead_glyph
        Arrow_glyph.end=None
    else:
        Arrow_source.data=dict(xS=[3], xE=[3], yS=[h], yE=[h+F_for_vis])
        Arrow_glyph.start=None
        Arrow_glyph.end=ArrowHead_glyph
        
    ForceLabel_source.data=dict(x=[3], y=[1.1*(h+OscAmp_for_vis)], t=['Force = '+str(round(F,1))])

## calculate Amplitude as a function of frequency
def calculateGraphPlot():
#    [Forced]=glob_Forced.data["val"]
##    print('Forced3=',Forced)
#    [Omega0]=glob_Omega0.data["val"]
#    omega=Omega0/Forced
    
#    [omega] = glob_omega.data["val"]
    [oscAmp ]     = glob_oscAmp.data["val"]
#    [m1 ]     = glob_m1.data["val"]

#    
#    [Muu ]     = glob_Muu.data["val"]
#    
#    m2=(Muu*m1)
#    [Dd]=glob_Dd.data["val"]
#    c2=2*omega*m2*Dd
##    c2=4
#    print(c2)
##    [c2 ]     = glob_c2 .data["val"]
#    [k1]     = glob_k1.data["val"]
#   
#   
#    [Omega0]=glob_Omega0.data["val"]
#    
#    k2=(omega*omega)*m2
    [m1 ]     = glob_m1.data["val"]
    [k1 ]     = glob_k1.data["val"]
    [m2 ]     = glob_m2.data["val"]
    [c2 ]     = glob_c2.data["val"]
    [k2 ]     = glob_k2.data["val"]
    [omega]=glob_omega.data["val"]
    [Omega0]=glob_Omega0.data["val"]
#   
    [Omega0]=glob_Omega0.data["val"]
#    [k2]     = glob_k2.data["val"]
    print('calculateGraphPlot','m1',m1,'m2',m2,'c1',c2,'k1',k2,'omega',omega)
    # prepare vectors
    omega=[]
    Amplitude=[]
#    print(m1,m2,k1,k2,c2)
    
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
    
#    [m1 ]     = glob_m1.data["val"]
#    [Forced]=glob_Forced.data["val"]
#    print('Forced4=',Forced)
   
#    [Omega0]=glob_Omega0.data["val"]
#    omega=Omega0/Forced
##    [Muu ]     = glob_Muu.data["val"]
#
#    m2=(Muu*m1)
#    [Dd]=glob_Dd.data["val"]
#    
#    c2=2*omega*m2*Dd
#    c2=4
    
#    [c2 ]     = glob_c2 .data["val"]
#    [k1]     = glob_k1.data["val"]
##    [k2]     = glob_k2.data["val"]
#    
#    k2=(omega*omega)*m2
    [m1 ]     = glob_m1.data["val"]
    [k1 ]     = glob_k1.data["val"]
    [m2 ]     = glob_m2.data["val"]
    [c2 ]     = glob_c2.data["val"]
    [k2 ]     = glob_k2.data["val"]
    [omega]=glob_omega.data["val"]
    [Omega0]=glob_Omega0.data["val"]
    
    [alpha]=glob_alpha.data["val"]
    [Omega0]=glob_Omega0.data["val"]
    [spring]    = glob_spring.data["spring"]
    
    [t] = glob_t.data["val"]
    om=Omega0+alpha*t
    xi = sqrt(k2/m2) / om
    Dmod = c2/2.0/sqrt(m2*k2)
    print('m1',m1,'m2',m2,'c1',c2,'k1',k2,'omega',omega)
    A = k2-m2*om*om
    B = c2*om
    C = k1*k2-(k1*m2+k2*m1+m2*k2)*om*om+m1*m2*om*om*om*om
    D = (k1-(m1+m2)*om*om)*c2*om
    E = xi * xi - 1.0
    F = 2.0 * Dmod * xi
    G = C * E - D * F
    H = C * F + D * E
    print('Omegascanstep','m1',m1,'m2',m2,'c1',c2,'k1',k2,'omega',omega)
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
    
    
    [baseSpring]    = glob_baseSpring.data["baseSpring"]
    [dashpot ]    = glob_dashpot.data["dashpot"]
    [mainMass]    = glob_mainMass.data["mainMass"]
    [topMass]    = glob_topMass.data["topMass"]
    [spring]    = glob_spring.data["spring"]
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
        
        [g1tunedmass] = glob_callback.data["cid"]
        curdoc().remove_periodic_callback(g1tunedmass)
        glob_active.data = dict(Active=[False])
        Arrow_source.data=dict(xS=[], xE=[], yS=[], yE=[])
        omega_input.value=om
    t+=0.05
    glob_t.data = dict(val=[t])

# draw title in the middle
title_box = Div(text="""<h2 style="text-align:center;">Schwingungstilger (Tuned mass damper)</h2>""",width=1000)

## create simulation drawing
fig = figure(title="", tools = "", x_range=(-7,7), y_range=(-1,23),width=350,height=450)
fig.title.text_font_size = "20px"
fig.title.align = "center"
fig.axis.visible = False
fig.grid.visible = False
fig.outline_line_color = None
# add objects to plot
spring.plot(fig,width=2)
baseSpring.plot(fig,width=2)
dashpot.plot(fig,width=2)
mainMass.plot(fig)
topMass.plot(fig)
fig.line(x=[-2,2],y=[0.05,0.05],color="black",line_width=3)
fig.multi_line(xs=[[-2.75,-2],[-1.75,-1.0],[-0.75,0],[.25,1],[1.25,2]],
    ys=[[-0.5,0.05],[-0.5,0.05],[-0.5,0.05],[-0.5,0.05],[-0.5,0.05]],
    color="black",
    line_width=3)

ArrowHead_glyph =  NormalHead(line_color="red",line_width=3,size=10)
Arrow_glyph = (Arrow(x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=Arrow_source,
    line_color="red",line_width=3))
fig.add_layout(Arrow_glyph)




fig.toolbar.logo = None
fig.toolbar_location = None


# Construct and add external force label
fig.add_layout(
               LabelSet(
                          x='x', y='y',
                          text='t',
                          text_color='black',text_font_size="15pt",
                          level='glyph',text_baseline="middle",text_align="center",
                          source=ForceLabel_source
                       )
              )

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
p.circle(x='om',y='A', radius=0.5, source=Position,color="#E37222")

System_Parameters_text = Div(text="""<b>System Parameters</b> """)
ExternalForce_Parameter_text = Div(text="""<b>External Force Parameters</b> """)



columns = [
    TableColumn(field="names1", title="Parameter"),
    TableColumn(field="values1", title="Value"),
#    TableColumn(field="values2", title="Value"),
#    TableColumn(field="values3", title="Value"),
 
]

parameter_table = DataTable(source=parameters, columns=columns, reorderable=False, sortable=False, selectable=False, index_position=None, width=300, height=500)



def change_mass(attr,old,new):
#    Update_system()
#    Update_current_state()
    
    [m1 ]     = glob_m1.data["val"]
    [m2 ]     = glob_m2.data["val"]
    [c2 ]     = glob_c2.data["val"]
    [k2 ]     = glob_k2.data["val"]
    [omega]=glob_omega.data["val"]
    [Omega0]=glob_Omega0.data["val"]

    omegamax=Omega0/omega_input.start
    
    
    Calculate_MagnificationFactor_PhaseAngle( 
                                       m1, m2, k1, k2, c2,
                                       oscAmp, omegamax, omega, 200,
                                       mainMass_amplificationFrequency_source, 
                                       topMass_amplificationFrequency_source,
                                       mainMass_phaseAngleFrequency_source,
                                       topMass_phaseAngleFrequency_source,
                                       Amplificaiton_range, 
                                       PhaseAngle_range, 
                                       Frequency_range,
                                      )
    Calculate_Current_Amplification_PhaseAngle(
                                                m1, m2, k1, k2,
                                                c2, oscAmp, omegamax, omega,
                                                Amplification_current_source, PhaseAngle_current_source
                                              )
    [Active] = glob_active.data["Active"]
#    glob_Muu.data = dict(val=([new]))
#    [Forced]=glob_Forced.data["val"]
#    [Muu ]     = glob_Muu.data["val"]
#    [m1 ]     = glob_m1.data["val"]
#    [Omega0]=glob_Omega0.data["val"]
#    [Dd]=glob_Dd.data["val"]
#    omega=Omega0/Forced
#    m2=(Muu*m1)
#    c2=2*omega*m2*Dd
#    
#    k2=(omega*omega)*m2
#    print('m1',m1,'m2',m2,'c1',c2,'k1',k2,'omega',omega)
#    parameters.data=dict(names1=['Damping C2','Stiffness K2'],names2=['m1','m2','omega'],names3=['Damping ratio','Muu','Forcing ratio'],values1=[round(c2,4),round(k2,4)],values2=[round(m1,4),round(m2,4),round(omega,4)],values3=[round(Dd,4),round(Muu,4),round(Forced,4)])
    
    if (not Active):
        glob_Muu.data = dict(val=([new]))
        [topMass] = glob_topMass.data["topMass"]
        [Muu ]     = glob_Muu.data["val"]
        [m1 ]     = glob_m1.data["val"]
        [Omega0]=glob_Omega0.data["val"]
        [Dd]=glob_Dd.data["val"]
        [omega]=glob_omega.data["val"]
        
        m2=(Muu*m1)
        glob_m2.data=dict(val=([m2]))
        [m2 ]     = glob_m2.data["val"]
        c2=2*omega*m2*Dd
        glob_c2.data=dict(val=([c2]))
        [c2 ]     = glob_c2.data["val"]
        k2=(omega*omega)*m2
        glob_k2.data=dict(val=([k2]))
        
        
        [m1 ]     = glob_m1.data["val"]
        [m2 ]     = glob_m2.data["val"]
        [c2 ]     = glob_c2.data["val"]
        [k2 ]     = glob_k2.data["val"]
        [omega]=glob_omega.data["val"]
        [Omega0]=glob_Omega0.data["val"]
    
        omegamax=Omega0/omega_input.start
        
        
        Calculate_MagnificationFactor_PhaseAngle( 
                                           m1, m2, k1, k2, c2,
                                           oscAmp, omegamax, omega, 200,
                                           mainMass_amplificationFrequency_source, 
                                           topMass_amplificationFrequency_source,
                                           mainMass_phaseAngleFrequency_source,
                                           topMass_phaseAngleFrequency_source,
                                           Amplificaiton_range, 
                                           PhaseAngle_range, 
                                           Frequency_range,
                                          )
        Calculate_Current_Amplification_PhaseAngle(
                                                    m1, m2, k1, k2,
                                                    c2, oscAmp, omegamax, omega,
                                                    Amplification_current_source, PhaseAngle_current_source
                                                  )
        
            
        
        
        
        
        
        parameters.data=dict(names1=['Damping C2','Stiffness K2'],names2=['m1','m2','omega'],names3=['Damping ratio','Muu','Forcing ratio'],values1=[round(c2,4),round(k2,4)],values2=[round(m1,4),round(m2,4),round(omega,4)],values3=[round(Dd,4),round(Muu,4),round(Forced,4)])
        
        
#        [m2]     = glob_m2.data["val"]
#        [Forced]=glob_Forced.data["val"]
##        print('Forced5=',Forced)
##        lob_Omega0=ColumnDataSource(data=dict(val=[0.01]))g
#        [Omega0]=glob_Omega0.data["val"]
#        omega=Omega0/Forced
#        K2=(omega*omega)*m2
        
#        [omega] = glob_omega.data["val"]
        
        topMass.changeMass(m2)
        
        m2=new
        
        # recalculate graph for new values
        calculateGraphPlot()
        change_Omega(None,None,Forced)
    elif (m2!=topMass.mass):
        m2=topMass.mass
## Create slider to choose mass of upper mass
mass_input = LatexSlider(title="\\text {Mass ratio =}",value_unit='',value=0.5, start=0.1, end=1, step=0.01,width=400)
mass_input.on_change('value',change_mass)

def change_kappa(attr,old,new):
#    Update_system()
#    Update_current_state()
    [m1 ]     = glob_m1.data["val"]
    [m2 ]     = glob_m2.data["val"]
    [c2 ]     = glob_c2.data["val"]
    [k2 ]     = glob_k2.data["val"]
    [omega]=glob_omega.data["val"]
    [Omega0]=glob_Omega0.data["val"]

    omegamax=Omega0/omega_input.start
    
    
    Calculate_MagnificationFactor_PhaseAngle( 
                                       m1, m2, k1, k2, c2,
                                       oscAmp, omegamax, omega, 200,
                                       mainMass_amplificationFrequency_source, 
                                       topMass_amplificationFrequency_source,
                                       mainMass_phaseAngleFrequency_source,
                                       topMass_phaseAngleFrequency_source,
                                       Amplificaiton_range, 
                                       PhaseAngle_range, 
                                       Frequency_range,
                                      )
    Calculate_Current_Amplification_PhaseAngle(
                                                m1, m2, k1, k2,
                                                c2, oscAmp, omegamax, omega,
                                                Amplification_current_source, PhaseAngle_current_source
                                              )
    
    
    
    
    
#    [m1 ]     = glob_m1.data["val"]
#    [Forced]=glob_Forced.data["val"]
#    glob_Muu.data=dict(val=[(new)])
##    print('Forced6=',Forced)
#   
#    [Omega0]=glob_Omega0.data["val"]
#    omega=Omega0/Forced
#    [Muu ]     = glob_Muu.data["val"]
#    [Dd]=glob_Dd.data["val"]
#    m2=(Muu*m1)
#    k2=(omega*omega)*m2
#    c2=2*omega*m2*Dd
#    print('m1',m1,'m2',m2,'c1',c2,'k1',k2,'omega',omega)
#    parameters.data=dict(names1=['Damping C2','Stiffness K2','m1','m2','omega','Damping ratio','Muu','Forcing ratio'],values1=[round(c2,4),round(k2,4),round(m1,4),round(m2,4),round(omega,4),round(Dd,4),round(Muu,4),round(Forced,4)])
#    
    [Active] = glob_active.data["Active"]
    if (not Active):
        
        [m2 ]     = glob_m2.data["val"]
        [c2 ]     = glob_c2.data["val"]
        [k2 ]     = glob_k2.data["val"]
        [omega]=glob_omega.data["val"]
        [m1 ]     = glob_m1.data["val"]
        [m2 ]     = glob_m2.data["val"]
        [c2 ]     = glob_c2.data["val"]
        [k2 ]     = glob_k2.data["val"]
        [omega]=glob_omega.data["val"]
        [Omega0]=glob_Omega0.data["val"]
    
        omegamax=Omega0/omega_input.start
        
        
        Calculate_MagnificationFactor_PhaseAngle( 
                                           m1, m2, k1, k2, c2,
                                           oscAmp, omegamax, omega, 200,
                                           mainMass_amplificationFrequency_source, 
                                           topMass_amplificationFrequency_source,
                                           mainMass_phaseAngleFrequency_source,
                                           topMass_phaseAngleFrequency_source,
                                           Amplificaiton_range, 
                                           PhaseAngle_range, 
                                           Frequency_range,
                                          )
        Calculate_Current_Amplification_PhaseAngle(
                                                    m1, m2, k1, k2,
                                                    c2, oscAmp, omegamax, omega,
                                                    Amplification_current_source, PhaseAngle_current_source
                                                  )
            
        
        
        
        
        parameters.data=dict(names1=['Damping C2','Stiffness K2'],names2=['m1','m2','omega'],names3=['Damping ratio','Muu','Forcing ratio'],values1=[round(c2,4),round(k2,4)],values2=[round(m1,4),round(m2,4),round(omega,4)],values3=[round(Dd,4),round(Muu,4),round(Forced,4)])
#        [omega] = glob_omega.data["val"]
#        [k2]     = glob_k2.data["val"]
        
        [spring]    = glob_spring.data["spring"]
        spring.changeSpringConst(new)
        k2=k2
       
        # recalculate graph for new values
        calculateGraphPlot()
        # plot frequency on new graph
        change_Omega(None,None,Forced)
    elif (new!=spring.kappa):
        k2=spring.kappa
## Create slider to choose spring constant
#kappa_input = LatexSlider(title="\\text {Stiffness =}",value_unit='\\frac{\\mathrm{N}}{\\mathrm{m}}', value=k2, start=1.0, end=200, step=10,width=400)
#kappa_input.on_change('value',change_kappa)

def change_lam(attr,old,new):
    [m1 ]     = glob_m1.data["val"]
    [m2 ]     = glob_m2.data["val"]
    [c2 ]     = glob_c2.data["val"]
    [k2 ]     = glob_k2.data["val"]
    [omega]=glob_omega.data["val"]
    [Omega0]=glob_Omega0.data["val"]

    omegamax=Omega0/omega_input.start
    
    
    Calculate_MagnificationFactor_PhaseAngle( 
                                       m1, m2, k1, k2, c2,
                                       oscAmp, omegamax, omega, 200,
                                       mainMass_amplificationFrequency_source, 
                                       topMass_amplificationFrequency_source,
                                       mainMass_phaseAngleFrequency_source,
                                       topMass_phaseAngleFrequency_source,
                                       Amplificaiton_range, 
                                       PhaseAngle_range, 
                                       Frequency_range,
                                      )
    Calculate_Current_Amplification_PhaseAngle(
                                                m1, m2, k1, k2,
                                                c2, oscAmp, omegamax, omega,
                                                Amplification_current_source, PhaseAngle_current_source
                                              )
    
    

#    Update_system()
#    Update_current_state()
#    glob_Dd.data=dict(val=[(new)])
#    print('DDtest=',new)
#    [Dd]=glob_Dd.data["val"]
    [Active] = glob_active.data["Active"]
#    [Muu ]     = glob_Muu.data["val"]
#    [m1 ]     = glob_m1.data["val"]
#    
#    m2=(Muu*m1)
#    [Forced]=glob_Forced.data["val"]
#    print('Forcedtestintg=',Forced)
#       
#    [Omega0]=glob_Omega0.data["val"]
#    omega=Omega0/Forced
#    c2=2*omega*m2*Dd
#    k2=(omega*omega)*m2
#    print('m1',m1,'m2',m2,'c1',c2,'k1',k2,'omega',omega)
#    
#    parameters.data=dict(names1=['Damping C2','Stiffness K2','m1','m2','omega','Damping ratio','Muu','Forcing ratio'],values1=[round(c2,4),round(k2,4),round(m1,4),round(m2,4),round(omega,4),round(Dd,4),round(Muu,4),round(Forced,4)])
    if (not Active):
        glob_Dd.data=dict(val=[(new)])
        [Dd]=glob_Dd.data["val"]
        [Forced]=glob_Forced.data["val"]
        [Muu ]     = glob_Muu.data["val"]
        [m1 ]     = glob_m1.data["val"]
        [Omega0]=glob_Omega0.data["val"]
        [Dd]=glob_Dd.data["val"]
        [omega]=glob_omega.data["val"]

        [m2 ]     = glob_m2.data["val"]
        c2=2*omega*m2*Dd
        glob_c2.data=dict(val=([c2]))
        [c2 ]     = glob_c2.data["val"]
        [m1 ]     = glob_m1.data["val"]
        [m2 ]     = glob_m2.data["val"]
        [c2 ]     = glob_c2.data["val"]
        [k2 ]     = glob_k2.data["val"]
        [omega]=glob_omega.data["val"]
        [Omega0]=glob_Omega0.data["val"]
    
        omegamax=Omega0/omega_input.start
        
        
        Calculate_MagnificationFactor_PhaseAngle( 
                                           m1, m2, k1, k2, c2,
                                           oscAmp, omegamax, omega, 200,
                                           mainMass_amplificationFrequency_source, 
                                           topMass_amplificationFrequency_source,
                                           mainMass_phaseAngleFrequency_source,
                                           topMass_phaseAngleFrequency_source,
                                           Amplificaiton_range, 
                                           PhaseAngle_range, 
                                           Frequency_range,
                                          )
        Calculate_Current_Amplification_PhaseAngle(
                                                    m1, m2, k1, k2,
                                                    c2, oscAmp, omegamax, omega,
                                                    Amplification_current_source, PhaseAngle_current_source
                                                  )
            
#        k2=(omega*omega)*m2
        
        parameters.data=dict(names1=['Damping C2','Stiffness K2','m1','m2','omega','Damping ratio','Muu','Forcing ratio'],values1=[round(c2,4),round(k2,4),round(m1,4),round(m2,4),round(omega,4),round(Dd,4),round(Muu,4),round(Forced,4)])#    print('Error=',omega)
        
        [dashpot ]    = glob_dashpot.data["dashpot"]
#        [omega] = glob_omega.data["val"]
#        [c2]     = glob_c2.data["val"]
        dashpot.changeDamperCoeff(c2)
        c2=c2
        # recalculate graph for new values
        calculateGraphPlot()
        # plot frequency on new graph
        change_Omega(None,None,Forced)
    elif (new!=dashpot.lam):
        c2=dashpot.lam
## Create slider to choose damper coefficient
lam_input = LatexSlider(title="\\text {Lehr Damping ratio =}",value_unit='', value=0.5, start=0.1, end=0.9, step=0.1,width=400)
lam_input.on_change('value',change_lam)

def change_Omega(attr,old,new):
    #global m1, k1, k2, c2, oscAmp, Amplification_current_source, PhaseAngle_current_source
    [Active] = glob_active.data["Active"]
    glob_Forced.data=dict(val=[(new)])
#    print ('Error2=',new)
#    
#    [Forced]=glob_Forced.data["val"]
##    print('Forced8=',Forced)
#    [Omega0]=glob_Omega0.data["val"]
#    omega=Omega0/Forced
#    [Dd]=glob_Dd.data["val"]
#    [Active] = glob_active.data["Active"]
#    [Muu ]     = glob_Muu.data["val"]
#    [m1 ]     = glob_m1.data["val"]
#    
#    m2=(Muu*m1)
##    [Forced]=glob_Forced.data["val"]
#    print('Forced6=',Forced)
#    c2=2*omega*m2*Dd
#    k2=(omega*omega)*m2
#    
#    print('m1',m1,'m2',m2,'c1',c2,'k1',k2,'omega',omega)
    
    
#    parameters.data=dict(names1=['Damping C2','Stiffness K2','m1','m2','omega','Damping ratio','Muu','Forcing ratio'],values1=[round(c2,4),round(k2,4),round(m1,4),round(m2,4),round(omega,4),round(Dd,4),round(Muu,4),round(Forced,4)])#    print('Error=',omega)
    if (not Active):
        glob_Forced.data=dict(val=[(new)])
        [Forced]=glob_Forced.data["val"]
        [Muu ]     = glob_Muu.data["val"]
        [m1 ]     = glob_m1.data["val"]
        [Omega0]=glob_Omega0.data["val"]
        [Dd]=glob_Dd.data["val"]
        omega=Omega0/Forced
        glob_omega.data=dict(val=[(omega)])
        
        [m2 ]     = glob_m2.data["val"]
        c2=2*omega*m2*Dd
        glob_c2.data=dict(val=[(c2)])
        [c2 ]     = glob_c2.data["val"]
        
        [m1 ]     = glob_m1.data["val"]
        [m2 ]     = glob_m2.data["val"]
        [c2 ]     = glob_c2.data["val"]
        [k2 ]     = glob_k2.data["val"]
        [omega]=glob_omega.data["val"]
        [Omega0]=glob_Omega0.data["val"]
    
        omegamax=Omega0/omega_input.start
        [oscAmp ]     = glob_oscAmp.data["val"]
        
        Calculate_MagnificationFactor_PhaseAngle( 
                                           m1, m2, k1, k2, c2,
                                           oscAmp, omegamax, omega, 200,
                                           mainMass_amplificationFrequency_source, 
                                           topMass_amplificationFrequency_source,
                                           mainMass_phaseAngleFrequency_source,
                                           topMass_phaseAngleFrequency_source,
                                           Amplificaiton_range, 
                                           PhaseAngle_range, 
                                           Frequency_range,
                                          )
        Calculate_Current_Amplification_PhaseAngle(
                                                    m1, m2, k1, k2,
                                                    c2, oscAmp, omegamax, omega,
                                                    Amplification_current_source, PhaseAngle_current_source
                                                  )
        
        k2=(omega*omega)*m2
        glob_k2.data=dict(val=[(k2)])
        [k2 ]     = glob_k2.data["val"]
        parameters.data=dict(names1=['Damping C2','Stiffness K2','m1','m2','omega','Damping ratio','Muu','Forcing ratio'],values1=[round(c2,4),round(k2,4),round(m1,4),round(m2,4),round(omega,4),round(Dd,4),round(Muu,4),round(Forced,4)])#    print('Error=',omega)
        
       
#        [omega] = glob_omega.data["val"]
        omega = omega
        if (omega==0):
            # if no oscillation then A is natural amplitude
            Position.data=dict(om=[omega],A=[AmplitudeFrequency.data['A'][0]])
        else:
            # find amplitude for current frequency from AmplitudeFrequency graph
            Position.data=dict(om=[omega],A=[AmplitudeFrequency.data['A'][int(floor(omega*10))-1]])
            
#        Update_current_state()
        
    elif (new!=omega):
        omega_input.value=Forced
## Create slider to choose damper coefficient
omega_input = LatexSlider(title="\\text{Forcing frequency ratio}",value_unit='', value=0.004, start=0.001, end=0.01, step=0.0005,width=400)
omega_input.on_change('value',change_Omega)

## create functions for buttons which control simulation
Simulation_Controls_text = Div(text="""<b>Simulation Controls</b> """)



def disable_all_sliders(d=True):
    mass_input.disabled  = d
#    kappa_input.disabled = d
    lam_input.disabled  = d
    omega_input.disabled = d
   
def PlayStop():
    
    [Active] = glob_active.data["Active"]
    [g1tunedmass] = glob_callback.data["cid"]
    if (not Active):
        #reset()
        
        g1tunedmass=curdoc().add_periodic_callback(evolve,100)
        glob_callback.data = dict(cid=[g1tunedmass])
        glob_active.data   = dict(Active=[True])
        disable_all_sliders(True)
        PlayStop_button.label = 'Pause' 
    else:
        [g1tunedmass] = glob_callback.data["cid"]
        curdoc().remove_periodic_callback(g1tunedmass)
        glob_active.data = dict(Active=[False])
        PlayStop_button.label = 'Play' 
        
def reset():
    
    [topMass]    = glob_topMass.data["topMass"]
    [dashpot ]    = glob_dashpot.data["dashpot"]
    [baseSpring]    = glob_baseSpring.data["baseSpring"]
    [mainMass]    = glob_mainMass.data["mainMass"]
    [oscForceAngle ]     = glob_oscForceAngle.data["val"]
    [spring]    = glob_spring.data["spring"]
    [x1] = glob_x1.data["val"]
    [x2] = glob_x2.data["val"]
    [h] = glob_h.data["val"]
    [t] = glob_t.data["val"]
    
    mass_input.value=0.5
#    kappa_input.value=80.0
    lam_input.value=0.5
    omega_input.value=0.004
    disable_all_sliders(False)
    # if simulation is running, then stop it
#    glob_active.data = dict(Active=[False])
#    PlayStop()
    # reset objects
    [Active] = glob_active.data["Active"]
    if Active == False:
        pass
    else:
        [g1tunedmass] = glob_callback.data["cid"]
        curdoc().remove_periodic_callback(g1tunedmass)
        glob_active.data = dict(Active=[False])

    #Reset Play Button
    PlayStop_button.label = 'Play' 
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
    glob_oscForceAngle.data = dict(val = [pi/2])
    
    print('m1',m1,'m2',m2,'c1',c2,'k1',k2,'omega',omega)
    
    
    Arrow_source.data=dict(xS=[], xE=[], yS=[], yE=[])
    ForceLabel_source.data=dict(x=[],y=[],t=[])
    
    # Clear the displacement-time diagram related data structures
    mainMass_displacementTime_source.data=dict(x=[0],y=[0]) # Default values
    topMass_displacementTime_source.data=dict(x=[0],y=[0]) # Default values
    
    displacement_range.start = -4
    displacement_range.end   = 4
    time_range.end   = 15
    time_range.start = 0
    
    t = 0
    glob_t.data = dict(val=[t])

    
def omega_scan():
    [t] = glob_t.data["val"]
    [Active] = glob_active.data["Active"]
    if (not Active):
        reset()
        t=0
        glob_t.data = dict(val=[t])
        
        g1tunedmass=curdoc().add_periodic_callback(omegaScanStep,100)
        glob_callback.data = dict(cid=[g1tunedmass])
        Arrow_glyph.start=ArrowHead_glyph
        Arrow_glyph.end=None
        
def ClearAndReset_DisplacementTime_History():
    [topMass]    = glob_topMass.data["topMass"]
    [dashpot ]    = glob_dashpot.data["dashpot"]
    [baseSpring]    = glob_baseSpring.data["baseSpring"]
    [mainMass]    = glob_mainMass.data["mainMass"]
    [oscForceAngle ]     = glob_oscForceAngle.data["val"]
    [spring]    = glob_spring.data["spring"]
    [x1] = glob_x1.data["val"]
    [x2] = glob_x2.data["val"]
    [h] = glob_h.data["val"]
    [t] = glob_t.data["val"]
    [displacement_range ]    = glob_displacement_range.data["displacement_range"]
    [time_range ]    = glob_time_range.data["time_range"]
    [t] = glob_t.data["val"]
    
    
    [Active] = glob_active.data["Active"]
    if Active == False:
       pass
    else:
        [g1tunedmass] = glob_callback.data["cid"]
        curdoc().remove_periodic_callback(g1tunedmass)
        glob_active.data = dict(Active=[False])
    
    PlayStop_button.label = 'Play' 
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
    glob_oscForceAngle.data = dict(val = [pi/2])
    
    
    
    
    Arrow_source.data=dict(xS=[], xE=[], yS=[], yE=[])
    ForceLabel_source.data=dict(x=[],y=[],t=[])
    # Clear Displacement-Time sources
    disable_all_sliders(False)
    
    Clear_Time_History(
                       mainMass_displacementTime_source,
                       topMass_displacementTime_source
                      )

    # Reset Displacement-Time plot time boundary
    displacement_range.start = -4
    displacement_range.end   = 4
    time_range.end   = 15
    time_range.start = 0
    
    
    
    # Reset time
    t = 0
    glob_t.data = dict(val=[t])
    
    

## create buttons to control simulation
PlayStop_button = Button(label="Play", button_type="success",width=100)
PlayStop_button.on_click(PlayStop)
#play_button = Button(label="Play", button_type="success",width=100)
#play_button.on_click(play)
reset_button = Button(label="Reset", button_type="success",width=100)
reset_button.on_click(reset)
omega_scan_button = Button(label=u"\u03C9 scan", button_type="success",width=100)
omega_scan_button.on_click(omega_scan)

ClearResetTimeHistory_button = Button(label="Stop", button_type="success",width=100)
ClearResetTimeHistory_button.on_click(ClearAndReset_DisplacementTime_History)

def Update_system():
#    [m1 ]     = glob_m1.data["val"]
#    [k1 ]     = glob_k1.data["val"]
#    [m2 ]     = glob_m2.data["val"]
#    [c2 ]     = glob_c2.data["val"]
#    [k2 ]     = glob_k2.data["val"]
#    [omega]=glob_omega.data["val"]
#    
##   
#    [Omega0]=glob_Omega0.data["val"]

    omegamax=Omega0/omega_input.start
#    print('m1',m1,'m2',m2,'c1',c2,'k1',k2,'omega',omega)
#    print('omegamax',omegamax)
    Calculate_MagnificationFactor_PhaseAngle( 
                                       m1, m2, k1, k2, c2,
                                       oscAmp, omegamax, omega, 200,
                                       mainMass_amplificationFrequency_source, 
                                       topMass_amplificationFrequency_source,
                                       mainMass_phaseAngleFrequency_source,
                                       topMass_phaseAngleFrequency_source,
                                       Amplificaiton_range, 
                                       PhaseAngle_range, 
                                       Frequency_range,
                                      )
    
   
    
def Update_current_state():
    [m1 ]     = glob_m1.data["val"]
    [k1 ]     = glob_k1.data["val"]
    [m2 ]     = glob_m2.data["val"]
    [c2 ]     = glob_c2.data["val"]
    [k2 ]     = glob_k2.data["val"]
    [omega]=glob_omega.data["val"]
    
#   
    [Omega0]=glob_Omega0.data["val"]

    omegamax=Omega0/omega_input.start
#    omegamax=Omega0/omega_input.start
# 
#
#   
#    k2=(omega*omega)*m2
#    [Dd]=glob_Dd.data["val"]
#    c2=2*omega*m2*Dd
#    print('m1',m1,'m2',m2,'c1',c2,'k1',k2,'omega',omega)
    Calculate_Current_Amplification_PhaseAngle(
                                                m1, m2, k1, k2,
                                                c2, oscAmp, omegamax, omega,
                                                Amplification_current_source, PhaseAngle_current_source
                                              )

# setup initial conditions
calculateGraphPlot()
change_Omega(None,None,0.004)

# Fill the Amplification factor and Phase angle diagrams
#[m1 ]     = glob_m1.data["val"]
#[m2 ]     = glob_m2.data["val"]
#[c2 ]     = glob_c2.data["val"]
#[k2 ]     = glob_k2.data["val"]
#[omega]=glob_omega.data["val"]
[Omega0]=glob_Omega0.data["val"]
#
omegamax=Omega0/omega_input.start


Calculate_MagnificationFactor_PhaseAngle( 
                                   m1, m2, k1, k2, c2,
                                   oscAmp, omegamax, omega, 200,
                                   mainMass_amplificationFrequency_source, 
                                   topMass_amplificationFrequency_source,
                                   mainMass_phaseAngleFrequency_source,
                                   topMass_phaseAngleFrequency_source,
                                   Amplificaiton_range, 
                                   PhaseAngle_range, 
                                   Frequency_range,
                                  )
Calculate_Current_Amplification_PhaseAngle(
                                            m1, m2, k1, k2,
                                            c2, oscAmp, omegamax, omega,
                                            Amplification_current_source, PhaseAngle_current_source
                                          )
#Update_system()
#Update_current_state()


## Send to window
gp = gridplot([Amplification_Frequency_plot,PhaseAngle_Frequency_plot],ncols=1,plot_width=250,plot_height=250,merge_tools=True,toolbar_location="below",toolbar_options=dict(logo=None))
hspace = 20
curdoc().add_root(column(description,\
    row(column(row(column(Spacer(height=200),PlayStop_button,ClearResetTimeHistory_button,reset_button),Spacer(width=12),fig,Spacer(height=hspace),row(Spacer(width=12)),displacementTime_plot,Spacer(width=12),gp))), \
    row(mass_input,Spacer(width=hspace),Spacer(width=hspace),lam_input), \
    row(column(row(column(Spacer(height=20),omega_input,parameter_table))))))
   

    
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '