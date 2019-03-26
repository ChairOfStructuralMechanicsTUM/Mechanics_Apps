from __future__ import division
#Importing spring,damper and mass
from Spring import *
from Dashpot import *
from Mass import *
#importing plotting objects from bokeh
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer, gridplot
from bokeh.io import curdoc
from bokeh.models import Select,Slider, Button, Div, HoverTool, Range1d, Div, Arrow, NormalHead, CDSView, IndexFilter
from bokeh.models.tickers import FixedTicker
from bokeh.models.callbacks import CustomJS
from bokeh.models.widgets import DataTable, TableColumn

from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv,LatexLabel,LatexLabelSet
from math import sqrt, exp, pow, sin , cos, ceil, pi, atan2, sinh, cosh
from numpy import convolve, amax, argmax
import numpy 

## defining global variables required
initial_spring_constant_value = 1.
initial_damping_ratio = 0.1
initial_displacement_value = 0
TimePeriodRatio = 1
force_value = 1.
Force_duration = 1
ForceInput = ""
h = [] 
FI =[]
final = []
Te = Force_duration/TimePeriodRatio   
W = 0
initial_mass_value = 0
D = 0
WD = 0
s=0
t=0
dt=0

mass = CircularMass(initial_mass_value,0,10,2,2)
spring = Spring((-2,.75),(-2,8),7,initial_spring_constant_value)
damping_coeffcient=initial_damping_ratio*2*sqrt(initial_spring_constant_value*initial_mass_value)
damper = Dashpot((2,.75),(2,8),damping_coeffcient)

def Initialise():
    global initial_spring_constant_value,initial_damping_ratio,initial_displacement_value,TimePeriodRatio
    global force_value,Force_duration,Te,W,initial_mass_value,D,initial_damping_ratio,WD,W
    global s, t, dt, mass, FI, final, h
    
    initial_spring_constant_value = 1.
    initial_damping_ratio = 0.1
    initial_displacement_value = 0
    TimePeriodRatio = 1
    force_value = 1.
    Force_duration = 1## input parameters for the analytic solution
    Te = Force_duration/TimePeriodRatio   

    W = 2*pi/Te
    initial_mass_value = initial_spring_constant_value /pow(W,2)
    D = initial_damping_ratio
    WD = W * sqrt(1-pow(D,2))
    mass.changeMass(initial_mass_value)
    spring.changeSpringConst(initial_spring_constant_value)
    damping_coeffcient=D*2*sqrt(initial_spring_constant_value*initial_mass_value)
    damper.changeDamperCoeff(damping_coeffcient)
    
    s=0
    t=0
    dt=0.02    
    for i in range(0,1000,1): # making rectangular function 
        T= i*dt
        if (T<=1):
            FI.append(1) 
        else:
            FI.append(0)        
        x=(1/(float(mass.Getmass())*WD))*exp(-D*W*T)*sin(WD*T) 
        h.append(x)
    final = dt*convolve(FI,h,mode='full')
    
Initialise()

Bottom_Line = ColumnDataSource(data = dict(x=[-2,2],y=[8,8]))
Linking_Line = ColumnDataSource(data = dict(x=[0,0],y=[8,10]))

displacement = ColumnDataSource(data = dict(t=[0],s=[initial_displacement_value]))

arrow_line = ColumnDataSource(data = dict(x1=[0],y1=[15],x2=[0],y2=[12]))
omega_max = ColumnDataSource(data = dict(time=[0],omega=[0]))
t_max = ColumnDataSource(data = dict(time=[0],tmax=[0]))
Force_input = ColumnDataSource(data = dict(beta=[0],phi=[0]))

Force_input.stream(dict(beta=[0],phi=[1]))
Force_input.stream(dict(beta=[1],phi=[1]))
Force_input.stream(dict(beta=[1.0001],phi=[0]))
Force_input.stream(dict(beta=[2],phi=[0]))

parameters = ColumnDataSource(data = dict(names1=[u'\u03c9',"Te"],names2=["D",u'\u03c9*'],values1=[round(W,4),round(Te,4)],values2=[round(D,4),round(WD,4)]))
Active=False

def evolve():
    global Bottom_Line, Linking_Line, t ,dt
    global mass, spring, damper, initial_displacement_value, TimePeriodRatio, force_value
    global W, WD, D, Te
    global ForceInput, h, FI, final
    global omega_max
    
    #########
    k = spring.getSpringConstant
    maximum = 0
    maximumat = 0
    if(t==0):
        final*=0 # reset the list 
        for i in range(0,1000,1): # finding unit response function and store
            T= i*dt
            x=(1/(float(mass.Getmass())*WD))*exp(-D*W*T)*sin(WD*T) 
            h[i] = x
        final = dt*convolve(FI,h,mode='full')
    
    maximum = amax(final)
    maximumat = dt*argmax(final)

    omega_max.stream(dict(time=[TimePeriodRatio],omega=[maximum]))
    t_max.stream(dict(time=[TimePeriodRatio],tmax=[maximumat]))
    
    time =int(t/dt)
    move_system(-final[time])
    displacement.stream(dict(t=[t],s=[final[time]]))
    t+=dt

title_box = Div(text="""<h2 style="text-align:center;">Shock response spectra </h2>""",width=1000)

# sdof drawing
fig = figure(title="", tools="", x_range=(-7,7), y_range=(0,20),width=270,height=225)
fig.title.text_font_size="20pt"
fig.axis.visible = False
fig.grid.visible = False
fig.outline_line_color = None
fig.line(x=[-2,2],y=[.75,.75],color="black",line_width=3)
fig.multi_line(xs=[[-2.75,-2],[-1.75,-1.0],[-0.75,0],[.25,1],[1.25,2]],
    ys=[[0,0.75],[0,0.75],[0,0.75],[0,0.75],[0,0.75]],
    color="black",
    line_width=3)
fig.line(x='x',y='y',source=Bottom_Line,color="black",line_width=3)
fig.line(x='x',y='y',source=Linking_Line,color="black",line_width=3)
spring.plot(fig,width=2)
damper.plot(fig,width=2)
mass.plot(fig)
arrow = fig.add_layout(Arrow(end=NormalHead(fill_color="red"), line_color="red", line_width=2,
    x_start='x1', y_start='y1', x_end='x2', y_end='y2', source=arrow_line))

# time plot
hover = HoverTool(tooltips=[("time","@t s"), ("displacement","@s m")])
Displacement = figure(title="", y_range=(2,-2), x_range=Range1d(bounds=(0,1000), start=0, end=20), height=550, \
    toolbar_location="right", tools=[hover,"ywheel_zoom,xwheel_pan,pan,reset"]) #ywheel_zoom,xwheel_pan,reset,
Displacement.line(x='t',y='s',source=displacement,color="#e37222",line_width=2,legend="Total Displacement",muted_color="#e37222",muted_alpha=0.2)
Displacement.axis.major_label_text_font_size="12pt"
Displacement.axis.axis_label_text_font_style="normal"
Displacement.axis.axis_label_text_font_size="14pt"
Displacement.xaxis.axis_label="Time [s]"
Displacement.yaxis.axis_label="Displacement [u/(F/k)]"
Displacement.legend.location="top_right"
Displacement.legend.click_policy="mute"


Dis_max = figure(title="", tools="", x_range=(0,3.0), y_range=(0,4), width=600, height=600)
Dis_max.circle(x='time', y='omega', source=omega_max, color="#a2ad00")
FigureMoving_Label_source   = ColumnDataSource(data=dict(x=[-0.45,1.7], y=[2.5, -0.4], names=[ "\dfrac{W_{max}}{\dfrac{F}{K}}","\dfrac{T_0}{T_e}"]))
D_max_label = LatexLabelSet(x='x', y='y', text='names', source=FigureMoving_Label_source, text_color = 'black', level='glyph', x_offset= 0, y_offset=0)
Dis_max.add_layout(D_max_label)

T_max = figure(title="", tools="", x_range=(0,3.0), y_range=(0,5), width=600, height=600)
T_max.circle(x='time', y='tmax', source=t_max, color="#a2ad00") 
Figure2Moving_Label_source   = ColumnDataSource(data=dict(x=[-0.45,1.7], y=[2.5, -0.4], names=["\dfrac{T_{max}}{T_0}", "T_{max}"]))
T_max_label = LatexLabelSet(x='x', y='y', text='names', source=Figure2Moving_Label_source, text_color = 'black', level='glyph', x_offset= 0, y_offset=0)
T_max.add_layout(T_max_label)

InputForce = figure(title="", tools="", x_range=(0,3.0), y_range=(0,2), width=300, height=150)
InputForce.line(x='beta', y='phi', source=Force_input, color="#a2ad00")
InputForce.xaxis.axis_label="Time(s)"
InputForce.yaxis.axis_label="Force(N)"
InputForce.yaxis.ticker = FixedTicker(ticks=[0,90,180])

def move_system(disp): # for moving the spring damper mass image according to the displacement of mass
    global mass, spring, damper, Bottom_Line, Linking_Line, force_value
    mass.moveTo((0,10+disp))
    spring.draw(Coord(-2,.75),Coord(-2,8+disp))
    damper.draw(Coord(2,.75),Coord(2,8+disp))
    Bottom_Line.data=dict(x=[-2,2],y=[8+disp, 8+disp])
    Linking_Line.data=dict(x=[0,0],y=[8+disp, 10+disp])
    if force_value > 0:
        arrow_line.data=dict(x1=[0],x2=[0],y1=[15+disp],y2=[12+disp])
    else:
        arrow_line.data=dict(x1=[0],x2=[0],y1=[35+disp],y2=[32+disp])


## Create slider to choose damping coefficient
def change_damping_coefficient(attr,old,new):
    global damper,initial_spring_constant_value,initial_mass_value
    damper.changeDamperCoeff(float(new*2*sqrt(initial_spring_constant_value*initial_mass_value)))
    updateParameters()
damping_coefficient_input = Slider(title="Damping coefficient [Ns/m]", value=initial_damping_ratio, callback_policy="mouseup", start=0.0, end=1, step=0.05,width=600)
damping_coefficient_input.on_change('value',change_damping_coefficient)

## Create slider to choose the frequency ratio
def change_frequency_ratio(attr,old,new):
    global Active, TimePeriodRatio
    if (not Active):
        TimePeriodRatio = new
        updateParameters()
frequency_ratio_input = Slider(title="Impulse duration to natural period ratio", value=TimePeriodRatio, start=0.1, end=3.0, step=0.1,width=600)
frequency_ratio_input.on_change('value',change_frequency_ratio)

def pause():
    global Active
    if (Active):
        curdoc().remove_periodic_callback(evolve)
        Active=False

def play():
    global Active
    if (not Active):
        curdoc().add_periodic_callback(evolve,dt*1000) #dt in milliseconds
        Active=True

def reset(): # resets values to initial cofiguration
    global displacement, t, s, Bottom_Line, Linking_Line, spring, mass, damper, initial_displacement_value, force_value, damping_coefficient_input
    pause()
    t=0
    s=0
    displacement.data=dict(t=[0],s=[initial_displacement_value])
    drawing_displacement = -initial_displacement_value * spring.getSpringConstant
    move_system(drawing_displacement)
    if force_value > 0:
        arrow_line.data=dict(x1=[0],x2=[0],y1=[15+drawing_displacement],y2=[12+drawing_displacement])
    else:
        arrow_line.data=dict(x1=[0],x2=[0],y1=[35+drawing_displacement],y2=[32+drawing_displacement])
    updateParameters()

def reset_OmegaMax_plot():
    global omega_max,time,omega
    pause()
    time = 0
    omega = 0
    omega_max.data=dict(time=[0],omega=[0])
    updateParameters()

def reset_Tmax_plot():
    global t_max,time,tmax
    pause()
    time = 0
    tmax =0
    t_max.data=dict(time=[0],tmax=[0])
    updateParameters()

reset_button_p_af = Button(label="Reset", button_type="success", width=50)
reset_button_p_af.on_click(reset_OmegaMax_plot)
reset_button_p_pa = Button(label="Reset", button_type="success", width=50)
reset_button_p_pa.on_click(reset_Tmax_plot)

def updateParameters():
    #input
    global mass, spring, damper, initial_displacement_value, TimePeriodRatio, force_value,initial_spring_constant_value,Force_duration
    #output
    global W, WD, D, Te, displacement, amplification_function, parameters, FI, final, h
    
    Te = Force_duration/TimePeriodRatio   
    W = 2*pi/Te
    initial_mass_value = initial_spring_constant_value /pow(W,2)
    mass.changeMass(initial_mass_value)
    D = (float(damper.getDampingCoefficient))/(2*sqrt(initial_spring_constant_value*initial_mass_value))
    WD = W * sqrt(1-pow(D,2))  
 
    final *= 0
    for i in range(0,1000,1): # making rectangular function 
        T= i*0.02
        x=(1/(mass.Getmass()*WD))*exp(-D*W*T)*sin(WD*T) 
        h[i] = x
    final = convolve(FI,h,mode='full')

    parameters.data = dict(names1=[u'\u03c9',"Te"],names2=["D",u'\u03c9*'],values1=[round(W,4),round(Te,4)],values2=[round(D,4),round(WD,4)])

play_button = Button(label="Play", button_type="success",width=100)
play_button.on_click(play)
pause_button = Button(label="Pause", button_type="success",width=100)
pause_button.on_click(pause)
reset_button = Button(label="Reset", button_type="success", width=100)
reset_button.on_click(reset)

def ChangeForce(forcetype):
    global FI,final
    if forcetype == "Triangular":
        Force_input.data=dict(beta=[0],phi=[0])
        Force_input.stream(dict(beta=[0],phi=[0]))
        Force_input.stream(dict(beta=[1],phi=[1]))
        Force_input.stream(dict(beta=[1.0001],phi=[0]))
        Force_input.stream(dict(beta=[2],phi=[0]))
        final *= 0
        FI *= 0
        for i in range(0,1000,1): # making triangular function 
            T= i*0.02
            if (T<=1):
                FI.append(T) 
            else:
                FI.append(0)
    elif forcetype == "Rectangular":
        Force_input.data=dict(beta=[0],phi=[0])
        Force_input.stream(dict(beta=[0],phi=[1]))
        Force_input.stream(dict(beta=[1],phi=[1]))
        Force_input.stream(dict(beta=[1.0001],phi=[0]))
        Force_input.stream(dict(beta=[2],phi=[0]))
        final *= 0
        FI *= 0
        for i in range(0,1000,1): # making rectangular function 
            T= i*0.02
            if (T<=1):
                FI.append(1) 
            else:
                FI.append(0)
    else:
        Force_input.data=dict(beta=[0],phi=[0])
        for i in range(0,100,1):
            Force_input.stream(dict(beta=[0.01*i],phi=[sin(0.01*i*pi)]))
        final *= 0
        FI *= 0
        for i in range(0,1000,1): # making sinusoidal functions
            T= i*0.02
            if (T<=1):
                FI.append(sin(T*pi)) 
            else:
                FI.append(0)

def ForceSelection(attr,old,new):   
    ChangeForce(new)
    
Force_select = Select(title="Force:", value="Rectangular",
    options=["Rectangular", "Triangular", "Sinusoidal"])
Force_select.on_change('value',ForceSelection)

# add parameter output
columns = [
    TableColumn(field="names1", title="Parameter"),
    TableColumn(field="values1", title="Value"),
    TableColumn(title=""),
    TableColumn(field="names2", title="Parameter"),
    TableColumn(field="values2", title="Value")
]
parameter_table = DataTable(source=parameters, columns=columns, reorderable=False, sortable=False, selectable=False, index_position=None, width=300, height=100)

# add app description
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)

## Send to window
hspace = 20
curdoc().add_root(column(description,\
    row(column(row(column(row(column(fig,column(play_button,Spacer(width = 10),\
    pause_button,column(Spacer(width = 10),reset_button))),column(Force_select,InputForce,parameter_table)),\
    Spacer(height=10),Displacement)),Spacer(height=hspace)),Spacer(width=30),\
    column(damping_coefficient_input,frequency_ratio_input,Spacer(height=hspace),\
    row(gridplot([Dis_max,Spacer(height=3 *hspace),T_max],ncols=1,plot_width=480,plot_height=420,merge_tools=True,toolbar_location="below"),\
    column(Spacer(height=160),reset_button_p_af,Spacer(height=370),reset_button_p_pa)))\
    ),))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  
# get path of parent directory and only use the name of the Parent Directory for the tab name. 
# Replace underscores '_' and minuses '-' with blanks ' '