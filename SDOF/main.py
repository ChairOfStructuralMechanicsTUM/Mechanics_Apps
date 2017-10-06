from Spring import *
from Dashpot import *
from Mass import *

from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import Slider, Button, Div, HoverTool, Range1d, Div

from os.path import dirname, join, split
from math import sqrt, exp, pow, sin , cos

# z = lam/(2*sqrt(k*m))
# z = 1 => crit damped
# z > 1 => over damped
# z < 1 => under damped

## initial values
initial_mass_value = 8
initial_spring_constant_value = 50
initial_damping_coefficient_value = 2

## input parameters for the analytic solution
initial_velocity_value = -5
initial_displacement_value = 1
frequency_ratio_value = 0.5
force_value = 100
ef = sqrt(initial_spring_constant_value/initial_mass_value)
D = initial_damping_coefficient_value / (2*initial_mass_value*ef)
damped_ef = ef * sqrt(1-pow(D,2))
excitation_frequency_value = frequency_ratio_value * ef

s=0
t=0
dt=0.03

mass = CircularMass(initial_mass_value,0,9,2,2)
mass.changeInitV(initial_velocity_value)
spring = Spring((-2,18),(-2,11),7,initial_spring_constant_value)
damper = Dashpot((2,18),(2,11),initial_damping_coefficient_value)
mass.linkObj(spring,(-2,11))
mass.linkObj(damper,(2,11))
Bottom_Line = ColumnDataSource(data = dict(x=[-2,2],y=[11,11]))
Linking_Line = ColumnDataSource(data = dict(x=[0,0],y=[11,9]))
Position = ColumnDataSource(data = dict(t=[0],s=[0]))

initial_velocity_value=-5.0
Active=False

def evolve():
    global Bottom_Line, Linking_Line, t, s
    global mass, spring, damper, initial_velocity_value, initial_displacement_value, frequency_ratio_value, force_value
    global ef, damped_ef, D, excitation_frequency_value
    # mass.FreezeForces()
    # disp=mass.evolve(dt)

    #########
    k = spring.getSpringConstant
    # particular (steady-state) part
    s_p = force_value / ( k * pow(1-pow(frequency_ratio_value,2),2) + pow(2*D*frequency_ratio_value,2) ) \
        * ( ( 1-pow(D,2) ) * sin(excitation_frequency_value*t) - 2*D*frequency_ratio_value*cos(excitation_frequency_value*t) )
    # homogeneous (transient) part
    s_h = exp(-D*ef*t) * ( initial_displacement_value * cos(damped_ef*t) + (initial_velocity_value + initial_displacement_value * ef * D)/damped_ef * sin(damped_ef*t) ) \
        + force_value * exp(-D*ef*t) / ( k * pow(1-pow(frequency_ratio_value,2),2) + pow(2*D*frequency_ratio_value,2) ) \
        * ( 2*D*frequency_ratio_value*cos(damped_ef*t) + ef/damped_ef * ( 2*frequency_ratio_value*pow(D,2) - frequency_ratio_value * (1-pow(frequency_ratio_value,2)) ) * sin(damped_ef*t) )
    #########

    # s+=disp.y
    s = s_p + s_h
    Bottom_Line.data=dict(x=[-2,2],y=[11+s, s+11])
    Linking_Line.data=dict(x=[0,0],y=[11+s, 9+s])
    t+=dt
    Position.stream(dict(t=[t],s=[s]))

title_box = Div(text="""<h2 style="text-align:center;">Spring pendulum</h2>""",width=1000)

# drawing
fig = figure(title="", tools="", x_range=(-7,7), y_range=(0,20),width=350,height=500)
fig.title.text_font_size="20pt"
fig.axis.visible = False
fig.grid.visible = False
fig.outline_line_color = None
spring.plot(fig,width=2)
damper.plot(fig,width=2)
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

# plot
hover = HoverTool(tooltips=[("time","@t s"), ("displacement","@s m")])
p = figure(title="", y_range=(-5,5), x_range=Range1d(bounds=(0,1000), start=0, end=20), height=500, \
    toolbar_location="right", tools=[hover,"ywheel_zoom,xwheel_pan,pan,reset"]) #ywheel_zoom,xwheel_pan,reset,
p.line(x='t',y='s',source=Position,color="black")
p.axis.major_label_text_font_size="12pt"
p.axis.axis_label_text_font_style="normal"
p.axis.axis_label_text_font_size="14pt"
p.xaxis.axis_label="Time [s]"
p.yaxis.axis_label="Displacement [m]"

## Create slider to choose mass
def change_mass(attr,old,new):
    global mass
    mass.changeMass(new)
    updateParameters()
    

mass_input = Slider(title="Mass [kg]", value=initial_mass_value, start=0.5, end=10.0, step=0.5, width=400)
mass_input.on_change('value',change_mass)

## Create slider to choose spring constant
def change_spring_constant(attr,old,new):
    global spring
    spring.changeSpringConst(new)
    updateParameters()

spring_constant_input = Slider(title="Spring stiffness [N/m]", value=initial_spring_constant_value, start=0.0, end=200, step=10,width=400)
spring_constant_input.on_change('value',change_spring_constant)

## Create slider to choose damping coefficient
def change_damping_coefficient(attr,old,new):
    global damper
    damper.changeDamperCoeff(new)
    updateParameters()    

damping_coefficient_input = Slider(title="Damping coefficient [Ns/m]", value=initial_damping_coefficient_value, start=0.0, end=10, step=0.1,width=400)
damping_coefficient_input.on_change('value',change_damping_coefficient)

## Create slider to choose initial velocity
def change_initV(attr,old,new):
    global mass, Active, initial_velocity_value, initial_velocity_input
    if (not Active):
        mass.changeInitV(new)

initial_velocity_input = Slider(title="Initial velocity [m/s]", value=initial_velocity_value, start=-10.0, end=10.0, step=0.5,width=400)
initial_velocity_input.on_change('value',change_initV)

## Create slider to choose initial displacement
def change_initial_displacement(attr,old,new):
    global Active, initial_displacement_value
    if (not Active):
        initial_displacement_value = new

initial_displacement_input = Slider(title="Initial velocity [m/s]", value=initial_velocity_value, start=-10.0, end=10.0, step=0.5,width=400)
initial_displacement_input.on_change('value',change_initial_displacement)

## Create slider to choose the frequency ratio
def change_frequency_ratio(attr,old,new):
    global Active, frequency_ratio_value
    if (not Active):
        frequency_ratio_value = new
        updateParameters()

frequency_ratio_input = Slider(title="Initial velocity [m/s]", value=initial_velocity_value, start=-10.0, end=10.0, step=0.5,width=400)
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

def stop():
    global Position, t, s, Bottom_Line, Linking_Line, spring, mass, damper
    pause()
    t=0
    s=0
    Position.data=dict(t=[0],s=[0])
    Bottom_Line.data = dict(x=[-2,2],y=[11,11])
    Linking_Line.data = dict(x=[0,0],y=[11,9])
    spring.compressTo(Coord(-2,18),Coord(-2,11))
    damper.compressTo(Coord(2,18),Coord(2,11))
    mass.moveTo((0,9))
    mass.resetLinks(spring,(-2,11))
    mass.resetLinks(damper,(2,11))
    mass.changeInitV(initial_velocity_input.value)

def reset():
    stop()
    mass_input.value = initial_mass_value
    spring_constant_input.value = initial_spring_constant_value
    damping_coefficient_input.value = initial_damping_coefficient_value
    initial_velocity_input.value = initial_velocity_value
    mass.changeInitV(initial_velocity_input.value)

    #this could reset also the plot, but needs the selenium package:
    #reset_button = selenium.find_element_by_class_name('bk-tool-icon-reset')
    #click_element_at_position(selenium, reset_button, 10, 10)

def updateParameters():
    #input
    global mass, spring, damper, initial_velocity_value, initial_displacement_value, frequency_ratio_value, force_value
    #output
    global ef, damped_ef, D, excitation_frequency_value
    m = mass.getMass
    k = spring.getSpringConstant
    c = damper.getDampingCoefficient
    ef = sqrt(k/m)
    D = c / (2*m*ef)
    damped_ef = ef * sqrt(1-pow(D,2))
    excitation_frequency_value = frequency_ratio_value * ef


play_button = Button(label="Play", button_type="success",width=100)
play_button.on_click(play)
pause_button = Button(label="Pause", button_type="success",width=100)
pause_button.on_click(pause)
stop_button = Button(label="Stop", button_type="success", width=100)
stop_button.on_click(stop)
reset_button = Button(label="Reset", button_type="success",width=100)
reset_button.on_click(reset)

# add app description
description_filename = join(dirname(__file__), "description.html")
description = Div(text=open(description_filename).read(), render_as_text=False, width=1200)

## Send to window
curdoc().add_root(column(description, \
    row(column(Spacer(height=100),play_button,pause_button,stop_button,reset_button),Spacer(width=10),fig,p), \
    row(mass_input,spring_constant_input),row(damping_coefficient_input,initial_velocity_input)))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
