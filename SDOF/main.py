from Spring import *
from Dashpot import *
from Mass import *

from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer, gridplot
from bokeh.io import curdoc
from bokeh.models import Slider, Button, Div, HoverTool, Range1d, Div, Arrow, NormalHead, CDSView, IndexFilter
from bokeh.models.tickers import FixedTicker
from bokeh.models.callbacks import CustomJS
from bokeh.models.widgets import DataTable, TableColumn

from os.path import dirname, join, split
from math import sqrt, exp, pow, sin , cos, ceil, pi, atan2, sinh, cosh

## initial values
initial_mass_value = 8.
initial_spring_constant_value = 50.
initial_damping_coefficient_value = 1.5
initial_velocity_value = 0.
initial_displacement_value = 0.
frequency_ratio_value = 0.5
force_value = 1.

## input parameters for the analytic solution
ef = sqrt(initial_spring_constant_value/initial_mass_value)
D = initial_damping_coefficient_value / (2.0*initial_mass_value*ef)
damped_ef = ef * sqrt(1-pow(D,2))
excitation_frequency_value = frequency_ratio_value * ef

s=0
t=0
dt=0.03

mass = CircularMass(initial_mass_value,0,10,2,2)
spring = Spring((-2,.75),(-2,8),7,initial_spring_constant_value)
damper = Dashpot((2,.75),(2,8),initial_damping_coefficient_value)

Bottom_Line = ColumnDataSource(data = dict(x=[-2,2],y=[8,8]))
Linking_Line = ColumnDataSource(data = dict(x=[0,0],y=[8,10]))

displacement = ColumnDataSource(data = dict(t=[0],s=[initial_displacement_value]))
displacement_particular = ColumnDataSource(data = dict(t=[0],s=[0]))
displacement_homogeneous = ColumnDataSource(data = dict(t=[0],s=[0]))

arrow_line = ColumnDataSource(data = dict(x1=[0],y1=[15],x2=[0],y2=[12]))
amplification_function = ColumnDataSource(data = dict(beta=[0],V=[1]))
phase_angle = ColumnDataSource(data = dict(beta=[0],phi=[0]))
for beta in range(1,75):
    amplification_function.stream(dict(beta=[beta/25.0],V=[1]))
    phase_angle.stream(dict(beta=[beta/25.0],phi=[1]))
current_ratio = ColumnDataSource(data = dict(beta=[0],V=[1],phi=[0]))
parameters = ColumnDataSource(data = dict(names1=[u'\u03c9',u"\u03a9"],names2=["D",u'\u03c9*'],values1=[round(ef,4),round(excitation_frequency_value,4)],values2=[round(D,4),round(damped_ef,4)]))
Active=False

def evolve():
    global Bottom_Line, Linking_Line, t, s
    global mass, spring, damper, initial_velocity_value, initial_displacement_value, frequency_ratio_value, force_value
    global ef, damped_ef, D, excitation_frequency_value
    
    #########
    k = spring.getSpringConstant

    if force_value > 0:
        if D < 1 and not frequency_ratio_value == 1:
            # particular (steady-state) part
            s_p = force_value / ( k * (pow(1-pow(frequency_ratio_value,2),2) + pow(2*D*frequency_ratio_value,2)) ) \
                * ( ( 1-pow(frequency_ratio_value,2) ) * sin(excitation_frequency_value*t) - 2*D*frequency_ratio_value*cos(excitation_frequency_value*t) )
            # homogeneous (transient) part
            s_h = exp(-D*ef*t) * ( initial_displacement_value * cos(damped_ef*t) + (initial_velocity_value + initial_displacement_value * ef * D)/damped_ef * sin(damped_ef*t) ) \
                + force_value * exp(-D*ef*t) / ( k * (pow(1-pow(frequency_ratio_value,2),2) + pow(2*D*frequency_ratio_value,2)) ) \
                * ( 2*D*frequency_ratio_value*cos(damped_ef*t) + ef/damped_ef * ( 2*frequency_ratio_value*pow(D,2) - frequency_ratio_value * (1-pow(frequency_ratio_value,2)) ) * sin(damped_ef*t) )
        elif D == 0 and frequency_ratio_value == 1:
            s_p = 0.5 * (initial_displacement_value * cos(ef*t) + initial_velocity_value/ef * sin(ef*t) + force_value/ (2*k) * (sin(ef*t) - ef*t*cos(ef*t)))
            s_h = s_p
        else:
            s_p = 0
            s_h = 0

    else:
        if D < 1:
            s_h = exp(-ef*D*t) * ( initial_displacement_value * cos(damped_ef*t) + (initial_velocity_value + initial_displacement_value * ef * D)/damped_ef * sin(damped_ef*t) )
        elif D == 1:
            s_h = exp(-ef*t) * ( initial_displacement_value + ( initial_velocity_value + ef * initial_displacement_value ) * t )
        elif D > 1:
            s_h = exp(-ef*D*t) * ( initial_displacement_value * cosh(damped_ef*t) + (initial_velocity_value + initial_displacement_value * ef * D)/damped_ef * sinh(damped_ef*t) )
        s_p = 0

    #########

    # scale with 1/stiffness
    s_p = s_p * k
    s_h = s_h * k
    s = s_p + s_h
    
    move_system(-s)
    displacement.stream(dict(t=[t],s=[s]))
    displacement_particular.stream(dict(t=[t],s=[s_p]))
    displacement_homogeneous.stream(dict(t=[t],s=[s_h]))
    t+=dt

title_box = Div(text="""<h2 style="text-align:center;">Single degree-of-freedom system</h2>""",width=1000)

# sdof drawing
fig = figure(title="", tools="", x_range=(-7,7), y_range=(0,20),width=350,height=450)
fig.title.text_font_size="20pt"
fig.axis.visible = False
fig.grid.visible = False
fig.outline_line_color = None
# fig.line(x=[-7,7],y=[9,9],color="blue",line_width=3)
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
p = figure(title="", y_range=(2,-2), x_range=Range1d(bounds=(0,1000), start=0, end=20), height=550, \
    toolbar_location="right", tools=[hover,"ywheel_zoom,xwheel_pan,pan,reset"]) #ywheel_zoom,xwheel_pan,reset,
p.line(x='t',y='s',source=displacement,color="#e37222",line_width=2,legend="Total Displacement",muted_color="#e37222",muted_alpha=0.2)
p.line(x='t',y='s',source=displacement_particular,color="#a2ad00",legend="Particular Solution",muted_color="#98c6ea",muted_alpha=0.2)
p.line(x='t',y='s',source=displacement_homogeneous,color="#64a0c8",legend="Homogeneous Solution",muted_color="#64a0c8",muted_alpha=0.2)
p.axis.major_label_text_font_size="12pt"
p.axis.axis_label_text_font_style="normal"
p.axis.axis_label_text_font_size="14pt"
p.xaxis.axis_label="Time [s]"
p.yaxis.axis_label="Displacement [u/(F/k)]"
p.legend.location="top_right"
p.legend.click_policy="mute"

# amplification function plot
def compute_amp_and_phase_angle():
    global amplification_function, phase_angle, D, frequency_ratio_value, current_ratio
    # beta scaled with 25!
    for beta in range(0,75):
        if D == 0 and beta == 25:
            V = 1000
        else:
            V = 1 / sqrt( pow(1-pow(beta/25.0,2),2) + pow(2*D*beta/25.0,2) )

        if D == 0 and beta < 25:
            phi = 0
        elif D == 0 and beta > 25:
            phi = 180
        elif beta == 25:
            phi = 90
        else:
            phi = atan2( 2*D*beta/25.0, 1-pow(beta/25.0,2) ) * 180.0 / pi
        amplification_function.patch({ 'V':[(beta,V)] })
        phase_angle.patch({ 'phi':[(beta,phi)] })

    plot_current_ratio()

def plot_current_ratio():
    global amplification_function, frequency_ratio_value, current_ratio
    if D == 0 and frequency_ratio_value == 1:
        V = 1000
    else:
        V = 1 / sqrt( pow(1-pow(frequency_ratio_value,2),2) + pow(2*D*frequency_ratio_value,2) )

    if D == 0 and frequency_ratio_value < 1:
        phi = 0
    elif frequency_ratio_value == 1:
        phi = 90
    elif D == 0 and frequency_ratio_value > 1:
        phi = 180
    else:
        phi = atan2( 2*D*frequency_ratio_value, 1-pow(frequency_ratio_value,2) ) * 180 / pi

    current_ratio.data=dict(beta=[frequency_ratio_value],V=[V],phi=[phi])

compute_amp_and_phase_angle()
p_af = figure(title="", tools="", x_range=(0,3.0), y_range=(0,5), width=300, height=300)
p_af.line(x='beta', y='V', source=amplification_function)
p_af.circle(x='beta', y='V', size=10, color="#e37222", source=current_ratio)
p_af.yaxis.axis_label="Amplification"
p_pa = figure(title="", tools="", x_range=(0,3.0), y_range=(0,180), width=300, height=300)
p_pa.line(x='beta', y='phi', source=phase_angle)
p_pa.circle(x='beta', y='phi', size=10, color="#e37222", source=current_ratio)
p_pa.xaxis.axis_label="Frequency ratio"
p_pa.yaxis.axis_label="Phase angle"
p_pa.yaxis.ticker = FixedTicker(ticks=[0,90,180])

def move_system(disp):
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

## Create slider to choose mass
def change_mass(attr,old,new):
    global mass
    mass.changeMass(new)
    updateParameters()
    compute_amp_and_phase_angle()

mass_input = Slider(title="Mass [kg]", value=initial_mass_value, start=0.5, end=10.0, step=0.5, width=400)
mass_input.on_change('value',change_mass)

## Create slider to choose spring constant
def change_spring_constant(attr,old,new):
    global spring
    spring.changeSpringConst(float(new))
    updateParameters()

spring_constant_input = Slider(title="Spring stiffness [N/m]", value=initial_spring_constant_value, start=10.0, end=200, step=10,width=400)
spring_constant_input.on_change('value',change_spring_constant)

## Create slider to choose damping coefficient
def change_damping_coefficient(attr,old,new):
    global damper
    damper.changeDamperCoeff(float(new))
    updateParameters()
    compute_amp_and_phase_angle()

damping_coefficient_input = Slider(title="Damping coefficient [Ns/m]", value=initial_damping_coefficient_value, callback_policy="mouseup", start=0.0, end=10, step=0.5,width=400)
damping_coefficient_input.on_change('value',change_damping_coefficient)

## Create slider to choose initial velocity
def change_initV(attr,old,new):
    global Active, initial_velocity_value, spring
    if (not Active):
        initial_velocity_value = float(new) / spring.getSpringConstant
        print(new,spring.getSpringConstant,initial_velocity_value)

initial_velocity_input = Slider(title="Initial velocity [m/s]", value=initial_velocity_value, start=-10.0, end=10.0, step=0.5,width=400)
initial_velocity_input.on_change('value',change_initV)

## Create slider to choose initial displacement
def change_initial_displacement(attr,old,new):
    global Active, initial_displacement_value, spring
    if (not Active):
        initial_displacement_value = float(new) / spring.getSpringConstant
        move_system(-new)
        updateParameters()

initial_displacement_input = Slider(title="Initial displacement [m]", value=initial_displacement_value, start=-2.0, end=2.0, step=0.5,width=400)
initial_displacement_input.on_change('value',change_initial_displacement)

## Create slider to choose the frequency ratio
def change_frequency_ratio(attr,old,new):
    global Active, frequency_ratio_value
    if (not Active):
        frequency_ratio_value = new
        updateParameters()
        plot_current_ratio()
        

frequency_ratio_input = Slider(title="Frequency ratio", value=frequency_ratio_value, start=0.1, end=3.0, step=0.1,width=400)
frequency_ratio_input.on_change('value',change_frequency_ratio)

## Create slider to choose the frequency ratio
def change_force_value(attr,old,new):
    global Active, force_value, arrow_line
    if (not Active):
        force_value = new
        current_y1 = arrow_line.data["y1"][0]
        current_y2 = arrow_line.data["y2"][0]
        if new == 1:
            arrow_line.data=dict(x1=[0],x2=[0],y1=[current_y1-20],y2=[current_y2-20])
        else:
            arrow_line.data=dict(x1=[0],x2=[0],y1=[current_y1+20],y2=[current_y2+20])

force_value_input = Slider(title="Force", value=force_value, start=0, end=1.0, step=1,width=400)
force_value_input.on_change('value',change_force_value)

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
    global displacement, t, s, Bottom_Line, Linking_Line, spring, mass, damper, initial_displacement_value, force_value
    pause()
    t=0
    s=0
    
    displacement.data=dict(t=[0],s=[initial_displacement_value])
    displacement_particular.data=dict(t=[0],s=[0])
    displacement_homogeneous.data=dict(t=[0],s=[0])
    
    drawing_displacement = -initial_displacement_value * spring.getSpringConstant
    move_system(drawing_displacement)
    if force_value > 0:
        arrow_line.data=dict(x1=[0],x2=[0],y1=[15+drawing_displacement],y2=[12+drawing_displacement])
    else:
        arrow_line.data=dict(x1=[0],x2=[0],y1=[35+drawing_displacement],y2=[32+drawing_displacement])

def reset():
    stop()
    mass_input.value = initial_mass_value
    spring_constant_input.value = initial_spring_constant_value
    damping_coefficient_input.value = initial_damping_coefficient_value
    initial_velocity_input.value = initial_velocity_value
    initial_displacement_input.value = initial_displacement_value

    #this could reset also the plot, but needs the selenium package:
    #reset_button = selenium.find_element_by_class_name('bk-tool-icon-reset')
    #click_element_at_position(selenium, reset_button, 10, 10)

def updateParameters():
    #input
    global mass, spring, damper, initial_velocity_value, initial_displacement_value, frequency_ratio_value, force_value
    #output
    global ef, damped_ef, D, excitation_frequency_value, displacement, amplification_function, parameters
    m = mass.getMass
    k = spring.getSpringConstant
    c = damper.getDampingCoefficient
    ef = sqrt(k/m)
    D = c / (2*m*ef)
    if D < 1:
        damped_ef = ef * sqrt(1-pow(D,2))
    else:
        damped_ef = ef * sqrt(pow(D,2)-1)
    excitation_frequency_value = frequency_ratio_value * ef
    parameters.data = dict(names1=[u'\u03c9',u"\u03a9"],names2=["D",u'\u03c9*'],values1=[round(ef,4),round(excitation_frequency_value,4)],values2=[round(D,4),round(damped_ef,4)])

play_button = Button(label="Play", button_type="success",width=100)
play_button.on_click(play)
pause_button = Button(label="Pause", button_type="success",width=100)
pause_button.on_click(pause)
stop_button = Button(label="Stop", button_type="success", width=100)
stop_button.on_click(stop)
# reset_button = Button(label="Reset", button_type="success",width=100)
# reset_button.on_click(reset)

# add parameter output
columns = [
    TableColumn(field="names1", title="Parameter"),
    TableColumn(field="values1", title="Value"),
    TableColumn(title=""),
    TableColumn(field="names2", title="Parameter"),
    TableColumn(field="values2", title="Value")
]
parameter_table = DataTable(source=parameters, columns=columns, reorderable=False, sortable=False, selectable=False, row_headers=False, width=300, height=100)

# add app description
description_filename = join(dirname(__file__), "description.html")
description = Div(text=open(description_filename).read(), render_as_text=False, width=1200)

## Send to window
hspace = 20
curdoc().add_root(column(description,\
    row(column(row(column(Spacer(height=200),play_button,pause_button,stop_button),Spacer(width=10),fig),Spacer(height=hspace),row(Spacer(width=100),parameter_table)),p,Spacer(width=10),gridplot([p_af,p_pa],ncols=1,plot_width=250,plot_height=250,merge_tools=True,toolbar_location="below")), \
    row(mass_input,Spacer(width=hspace),spring_constant_input,Spacer(width=hspace),damping_coefficient_input), \
    row(initial_displacement_input,Spacer(width=hspace),initial_velocity_input), \
    row(frequency_ratio_input,Spacer(width=hspace),force_value_input) ))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '