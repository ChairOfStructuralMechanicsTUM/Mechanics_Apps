from SDOF_Coord import SDOF_Coord
from SDOF_Spring import SDOF_Spring
from SDOF_Dashpot import SDOF_Dashpot
from SDOF_Mass import SDOF_CircularMass

from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer, gridplot
from bokeh.io import curdoc
from bokeh.models import Slider, Button, Div, HoverTool, Range1d, Arrow, NormalHead, ColumnDataSource
from bokeh.models.tickers import FixedTicker
from bokeh.models.widgets import DataTable, TableColumn

from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv
from math import sqrt, exp, pow, sin , cos, pi, atan2, sinh, cosh

## initial values
initial_mass_value                = 8.
initial_spring_constant_value     = 50.
initial_damping_coefficient_value = 1.5
initial_velocity_value            = 0.
initial_displacement_value        = 0.
frequency_ratio_value             = 0.5
force_value                       = 1.

## input parameters for the analytic solution
ef        = sqrt(initial_spring_constant_value/initial_mass_value)
D         = initial_damping_coefficient_value / (2.0*initial_mass_value*ef)
damped_ef = ef * sqrt(1-pow(D,2))
excitation_frequency_value = frequency_ratio_value * ef

s  = 0
t  = 0
dt = 0.03

mass   = SDOF_CircularMass(initial_mass_value,0,10,2,2)
spring = SDOF_Spring((-2,.75),(-2,8),7,initial_spring_constant_value)
damper = SDOF_Dashpot((2,.75),(2,8),initial_damping_coefficient_value)

Bottom_Line  = ColumnDataSource(data = dict(x=[-2,2],y=[8,8]))
Linking_Line = ColumnDataSource(data = dict(x=[0,0],y=[8,10]))

displacement = ColumnDataSource(data = dict(t=[0],s=[initial_displacement_value]))
displacement_particular  = ColumnDataSource(data = dict(t=[0],s=[0]))
displacement_homogeneous = ColumnDataSource(data = dict(t=[0],s=[0]))

arrow_line   = ColumnDataSource(data = dict(x1=[0],y1=[15],x2=[0],y2=[12]))
arrow_offset = ColumnDataSource(data = dict(x1=[0],y1=[12],x2=[0],y2=[11.9]))
phase_angle  = ColumnDataSource(data = dict(beta=[0],phi=[0]))
amplification_function = ColumnDataSource(data = dict(beta=[0],V=[1]))
for beta in range(1,75):
    amplification_function.stream(dict(beta=[beta/25.0],V=[1]))
    phase_angle.stream(dict(beta=[beta/25.0],phi=[1]))
current_ratio = ColumnDataSource(data = dict(beta=[0],V=[1],phi=[0]))
parameters    = ColumnDataSource(data = dict(names1=[u'\u03c9',u"\u03a9"],names2=["D",u'\u03c9*'],values1=[round(ef,4),round(excitation_frequency_value,4)],values2=[round(D,4),round(damped_ef,4)]))

## global variables
glob_t         = ColumnDataSource(data = dict(t = [t]))
glob_s         = ColumnDataSource(data = dict(s = [s]))
glob_D         = ColumnDataSource(data = dict(D = [D]))
glob_ef        = ColumnDataSource(data = dict(ef = [ef]))
glob_damped_ef = ColumnDataSource(data = dict(damped_ef = [damped_ef]))

glob_mass      = ColumnDataSource(data = dict(mass = [mass]))
glob_spring    = ColumnDataSource(data = dict(spring = [spring]))
glob_damper    = ColumnDataSource(data = dict(damper = [damper]))

glob_initial_displacement_value = ColumnDataSource(data = dict(initial_displacement_value = [initial_displacement_value]))
glob_initial_velocity_value = ColumnDataSource(data = dict(initial_velocity_value = [initial_velocity_value]))

glob_force_value = ColumnDataSource(data = dict(force_value = [force_value]))
glob_frequency_ratio_value = ColumnDataSource(data = dict(frequency_ratio_value = [frequency_ratio_value]))
glob_excitation_frequency_value = ColumnDataSource(data = dict(excitation_frequency_value = [excitation_frequency_value]))

glob_callback_id = ColumnDataSource(data = dict(callback_id = [None]))

def evolve():
    # extract global variables
    [t]         = glob_t.data["t"]                 # input/output
    [s]         = glob_s.data["s"]                 #      /output
    [D]         = glob_D.data["D"]                 # input/
    [ef]        = glob_ef.data["ef"]               # input/
    [damped_ef] = glob_damped_ef.data["damped_ef"] # input/
    [spring]    = glob_spring.data["spring"]       # input/
    
    [initial_displacement_value] = glob_initial_displacement_value.data["initial_displacement_value"] # input/
    [initial_velocity_value]     = glob_initial_velocity_value.data["initial_velocity_value"]         # input/
    [frequency_ratio_value]      = glob_frequency_ratio_value.data["frequency_ratio_value"]           # input/
    [force_value]                = glob_force_value.data["force_value"]                               # input/
    [excitation_frequency_value] = glob_excitation_frequency_value.data["excitation_frequency_value"] # input/
    
    #########
    k = spring.getSpringConstant

    if force_value > 0:
        if D == 0 and frequency_ratio_value == 1:
            s_p = -force_value/ (2*k) * ef*t*cos(ef*t)
            s_h = initial_displacement_value * cos(ef*t)+initial_velocity_value/ef * sin(ef*t) + force_value/ (2*k) * sin(ef*t)
        else:
            # particular (steady-state) part
            s_p = force_value / ( k * (pow(1-pow(frequency_ratio_value,2),2) + pow(2*D*frequency_ratio_value,2)) ) \
                * ( ( 1-pow(frequency_ratio_value,2) ) * sin(excitation_frequency_value*t) - 2*D*frequency_ratio_value*cos(excitation_frequency_value*t) )
            # homogeneous (transient) part
            if D<1: 
                s_h = exp(-D*ef*t) * ( initial_displacement_value * cos(damped_ef*t) + (initial_velocity_value + initial_displacement_value * ef * D)/damped_ef * sin(damped_ef*t) ) \
                    + force_value * exp(-D*ef*t) / ( k * (pow(1-pow(frequency_ratio_value,2),2) + pow(2*D*frequency_ratio_value,2)) ) \
                    * ( 2*D*frequency_ratio_value*cos(damped_ef*t) + ef/damped_ef * ( 2*frequency_ratio_value*pow(D,2) - frequency_ratio_value * (1-pow(frequency_ratio_value,2)) ) * sin(damped_ef*t) )
            else:
                print("how did we get there?") # even if this place is reached, there should be no bug
                s_h = 0
                play_pause_button.disabled = True
                pause()
                
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
    
    # save updated global variables
    glob_t.data = dict(t = [t])
    glob_s.data = dict(s = [s])
    

title_box = Div(text="""<h2 style="text-align:center;">Single degree-of-freedom system</h2>""",width=1000)

# sdof drawing
fig = figure(title="", tools="", x_range=(-7,7), y_range=(0,20),width=350,height=450)
fig.title.text_font_size = "20pt"
fig.axis.visible         = False
fig.grid.visible         = False
fig.outline_line_color   = None
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
fig.add_layout(Arrow(end=None, line_color="red", line_width=2,
    x_start='x1', y_start='y1', x_end='x2', y_end='y2', source=arrow_line))
fig.add_layout(Arrow(end=NormalHead(fill_color="red"), line_color="red", line_width=2,
    x_start='x1', y_start='y1', x_end='x2', y_end='y2', source=arrow_offset))
fig.toolbar.logo = None #removes bokeh logo

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
p.toolbar.logo = None #removes bokeh logo

# amplification function plot
def compute_amp_and_phase_angle():
    # extract global variables
    [D] = glob_D.data["D"] # input/
    
    # beta scaled with 25!
    for beta in range(0,75):
        if D == 0 and beta == 25:
            V = 1000
        else:
            V = 1.0 / sqrt( pow(1-pow(beta/25.0,2),2) + pow(2*D*beta/25.0,2) )

        if D == 0 and beta < 25:
            phi = 0
        elif D == 0 and beta > 25:
            phi = 180
        elif beta == 25:
            phi = 90
        else:
            phi = atan2( 2.0*D*beta/25.0, 1.0-pow(beta/25.0,2) ) * 180.0 / pi
        amplification_function.patch({ 'V':[(beta,V)] })
        phase_angle.patch({ 'phi':[(beta,phi)] })
    
    plot_current_ratio()

def plot_current_ratio():
    # extract global variables
    [frequency_ratio_value] = glob_frequency_ratio_value.data["frequency_ratio_value"] # input/
    [D] = glob_D.data["D"] # input/
    
    
    if D == 0 and frequency_ratio_value == 1:
        V = 1000
    else:
        V = 1.0 / sqrt( pow(1.0-pow(frequency_ratio_value,2),2) + pow(2.0*D*frequency_ratio_value,2) )

    if D == 0 and frequency_ratio_value < 1:
        phi = 0
    elif frequency_ratio_value == 1:
        phi = 90
    elif D == 0 and frequency_ratio_value > 1:
        phi = 180
    else:
        phi = atan2( 2.0*D*frequency_ratio_value, 1.0-pow(frequency_ratio_value,2) ) * 180.0 / pi

    current_ratio.data=dict(beta=[frequency_ratio_value],V=[V],phi=[phi])
    
    
compute_amp_and_phase_angle()
p_af = figure(title="", tools="", x_range=(0,3.0), y_range=(0,5), width=300, height=300)
p_af.line(x='beta', y='V', source=amplification_function, color="#a2ad00")
p_af.circle(x='beta', y='V', size=10, color="#e37222", source=current_ratio)
p_af.yaxis.axis_label="Amplification"
p_af.toolbar.logo = None #removes bokeh logo
p_pa = figure(title="", tools="", x_range=(0,3.0), y_range=(0,180), width=300, height=300)
p_pa.line(x='beta', y='phi', source=phase_angle, color="#a2ad00")
p_pa.circle(x='beta', y='phi', size=10, color="#e37222", source=current_ratio)
p_pa.xaxis.axis_label="Frequency ratio"
p_pa.yaxis.axis_label="Phase angle"
p_pa.yaxis.ticker = FixedTicker(ticks=[0,90,180])
p_pa.toolbar.logo = None #removes bokeh logo

def move_system(disp):
    # extract global variables
    [mass] = glob_mass.data["mass"] # input/ouput -> class
    [spring] = glob_spring.data["spring"] # input/ouput -> class
    [damper] = glob_damper.data["damper"] # input/ouput -> class
    [force_value] = glob_force_value.data["force_value"] # input/
    [excitation_frequency_value] = glob_excitation_frequency_value.data["excitation_frequency_value"] # input/
    
    mass.moveTo((0,10+disp))
    spring.draw(SDOF_Coord(-2,.75),SDOF_Coord(-2,8+disp))
    damper.draw(SDOF_Coord(2,.75),SDOF_Coord(2,8+disp))
    Bottom_Line.data=dict(x=[-2,2],y=[8+disp, 8+disp])
    Linking_Line.data=dict(x=[0,0],y=[8+disp, 10+disp])
    if force_value > 0:
        t = displacement.data["t"][-1]
        F_length = force_value*sin(excitation_frequency_value*t)
        #arrow_line.data=dict(x1=[0],x2=[0],y1=[15],y2=[15-F_length*3])
        arrow_line.stream(dict(x1=[0],x2=[0],y1=[15],y2=[15-F_length*3]),rollover=-1)
        #arrow_offset.data=dict(x1=[0],x2=[0],y1=[15-F_length*3],y2=[15-F_length*3 - (2*(F_length>0)-1)*1.0])
        arrow_offset.stream(dict(x1=[0],x2=[0],y1=[15-F_length*3],y2=[15-F_length*3 - (2*(F_length>0)-1)*1.0]),rollover=-1)        
    else:
        arrow_line.stream(dict(x1=[0],x2=[0],y1=[35+disp],y2=[32+disp]),rollover=-1)

## Create slider to choose mass
def change_mass(attr,old,new):
    [mass] = glob_mass.data["mass"] #input/ouput -> class
    mass.changeMass(new)
    updateParameters()
    compute_amp_and_phase_angle()

mass_input = Slider(title="Mass [kg]", value=initial_mass_value, start=0.5, end=10.0, step=0.5, width=400)
mass_input.on_change('value',change_mass)

## Create slider to choose spring constant
def change_spring_constant(attr,old,new):
    [spring] = glob_spring.data["spring"] # input/ouput -> class
    spring.changeSpringConst(float(new))
    updateParameters()

spring_constant_input = Slider(title="Spring stiffness [N/m]", value=initial_spring_constant_value, start=10.0, end=200, step=10,width=400)
spring_constant_input.on_change('value',change_spring_constant)

## Create slider to choose damping coefficient
def change_damping_coefficient(attr,old,new):
    [damper] = glob_damper.data["damper"] # input/ouput -> class
    damper.changeDamperCoeff(float(new))
    updateParameters()
    compute_amp_and_phase_angle()

damping_coefficient_input = Slider(title="Damping coefficient [Ns/m]", value=initial_damping_coefficient_value, callback_policy="mouseup", start=0.0, end=10, step=0.5,width=400)
damping_coefficient_input.on_change('value',change_damping_coefficient)

## Create slider to choose initial velocity
def change_initV(attr,old,new):
    # extract global variables
    [initial_velocity_value] = glob_initial_velocity_value.data["initial_velocity_value"] # input/output
    [spring]                 = glob_spring.data["spring"] # input/ouput -> class
    
    initial_velocity_value           = float(new) / spring.getSpringConstant
    glob_initial_velocity_value.data = dict(initial_velocity_value = [initial_velocity_value])


initial_velocity_input = Slider(title="Initial velocity [m/s]", value=initial_velocity_value, start=-10.0, end=10.0, step=0.5,width=400)
initial_velocity_input.on_change('value',change_initV)

## Create slider to choose initial displacement
def change_initial_displacement(attr,old,new):
    # extract global variables
    [initial_displacement_value] = glob_initial_displacement_value.data["initial_displacement_value"] # input/output
    [spring]                     = glob_spring.data["spring"] # input/ouput -> class
    
    initial_displacement_value           = float(new) / spring.getSpringConstant
    glob_initial_displacement_value.data = dict(initial_displacement_value = [initial_displacement_value])
    move_system(-new)
    updateParameters()

initial_displacement_input = Slider(title="Initial displacement [m]", value=initial_displacement_value, start=-2.0, end=2.0, step=0.5,width=400)
initial_displacement_input.on_change('value',change_initial_displacement)

## Create slider to choose the frequency ratio
def change_frequency_ratio(attr,old,new):
    # extract global variables
    [frequency_ratio_value] = glob_frequency_ratio_value.data["frequency_ratio_value"] # input/output
    
    frequency_ratio_value           = new
    glob_frequency_ratio_value.data = dict(frequency_ratio_value = [frequency_ratio_value])
    updateParameters()
    plot_current_ratio()

frequency_ratio_input = Slider(title="Frequency ratio", value=frequency_ratio_value, start=0.1, end=3.0, step=0.1,width=400)
frequency_ratio_input.on_change('value',change_frequency_ratio)

## Create slider to choose the frequency ratio
def change_force_value(attr,old,new):
    # extract global variables
    [force_value] = glob_force_value.data["force_value"] # input/output
    
    force_value           = new
    glob_force_value.data = dict(force_value = [force_value])
    current_y1            = arrow_line.data["y1"][0]
    current_y2            = arrow_line.data["y2"][0]
    updateParameters()
    if new == 1:
        arrow_line.data   = dict(x1=[0],x2=[0],y1=[current_y1-20],y2=[current_y2-20])
        arrow_offset.data = dict(x1=[0],y1=[current_y1-23],x2=[0],y2=[current_y2-20.1])
    else:
        arrow_line.data   = dict(x1=[0],x2=[0],y1=[current_y1+20],y2=[current_y2+20])
        arrow_offset.data = dict(x1=[0],x2=[0],y1=[current_y1+20],y2=[current_y2+20])
    
force_value_input = Slider(title="Force", value=force_value, start=0, end=1.0, step=1,width=400)
force_value_input.on_change('value',change_force_value)
#<<<<<<< HEAD -> Irfan
# g1SDOF=None
# def pause():
    # global Active
    # if (Active):
        # curdoc().remove_periodic_callback(g1SDOF)
        # Active=False

# def play():
    # global Active,g1SDOF
    # if (not Active):
        # g1SDOF=curdoc().add_periodic_callback(evolve,dt*1000) #dt in milliseconds
        # Active=True

#=======

#steer activity of sliders
def disable_all_sliders(d=True):
    mass_input.disabled                 = d
    spring_constant_input.disabled      = d
    damping_coefficient_input.disabled  = d
    initial_displacement_input.disabled = d
    initial_velocity_input.disabled     = d
    frequency_ratio_input.disabled      = d
    force_value_input.disabled          = d

def play_pause():
    # keep separate play and pause function since they are also called from other functions
    if play_pause_button.label == "Play":
        play()
    else:
        pause()
        
def pause():
    [callback_id] = glob_callback_id.data["callback_id"] # input/
    play_pause_button.label = "Play"
    try:
        curdoc().remove_periodic_callback(callback_id)
    except ValueError:
        print("WARNING: callback_id was already removed - this can happen if stop was pressed after pause, usually no serious problem; if stop was not called this part should be changed")
        # callback_id is not set to None or similar, the object hex-code stays -> no if == None possible -> use try/except
    except:
        print("This error is not covered: ", sys.exc_info()[0])
        raise
    
def play():
    [callback_id] = glob_callback_id.data["callback_id"] # input/output    
    disable_all_sliders(True) # disable sliders if graph is being plotted
    play_pause_button.label = "Pause"
    callback_id = curdoc().add_periodic_callback(evolve,dt*1000) #dt in milliseconds
    glob_callback_id.data = dict(callback_id = [callback_id])
    
#>>>>>>> master -> Matthias
def stop():
    # extract global variables
    [t] = glob_t.data["t"] # input/output
    [s] = glob_s.data["s"] # input/output
    [spring] = glob_spring.data["spring"] # input/
    [initial_displacement_value] = glob_initial_displacement_value.data["initial_displacement_value"] # input/
    [force_value] = glob_force_value.data["force_value"] # input/
    
    disable_all_sliders(False) #enable all sliders for new settings
    pause()
    glob_t.data = dict(t = [0]) # t=0
    glob_s.data = dict(s = [0]) # s=0
    
    displacement.data=dict(t=[0],s=[initial_displacement_value])
    displacement_particular.data=dict(t=[0],s=[0])
    displacement_homogeneous.data=dict(t=[0],s=[0])
    
    drawing_displacement = -initial_displacement_value * spring.getSpringConstant
    move_system(drawing_displacement)
    if force_value > 0:
        arrow_line.data=dict(x1=[0],x2=[0],y1=[15+drawing_displacement],y2=[12+drawing_displacement])
        arrow_offset.data=dict(x1=[0],x2=[0],y1=[12+drawing_displacement],y2=[12+(drawing_displacement-0.1)*1.1])
    else:
        arrow_line.data=dict(x1=[0],x2=[0],y1=[35+drawing_displacement],y2=[32+drawing_displacement])
        arrow_offset.data=dict(x1=[0],x2=[0],y1=[35+drawing_displacement],y2=[32+drawing_displacement])

def reset():
    stop()
    mass_input.value                 = initial_mass_value
    spring_constant_input.value      = initial_spring_constant_value
    damping_coefficient_input.value  = initial_damping_coefficient_value
    initial_velocity_input.value     = initial_velocity_value
    initial_displacement_input.value = initial_displacement_value
    frequency_ratio_input.value      = frequency_ratio_value
    force_value_input.value          = force_value


def updateParameters():
    # extract global variables
    # input
    [mass]   = glob_mass.data["mass"] # input/
    [spring] = glob_spring.data["spring"] # input/
    [damper] = glob_damper.data["damper"] # input/
    [frequency_ratio_value] = glob_frequency_ratio_value.data["frequency_ratio_value"] # input/
    [force_value] = glob_force_value.data["force_value"] # input/
    
    #output
    [D]                          = glob_excitation_frequency_value.data["excitation_frequency_value"] # input/output
    [ef]                         = glob_excitation_frequency_value.data["excitation_frequency_value"] # input/output
    [damped_ef]                  = glob_excitation_frequency_value.data["excitation_frequency_value"] # input/output
    [excitation_frequency_value] = glob_excitation_frequency_value.data["excitation_frequency_value"] # input/output
    
    m  = mass.getMass
    k  = spring.getSpringConstant
    c  = damper.getDampingCoefficient
    ef = sqrt(k/m)
    D  = c / (2*m*ef)
    if D < 1:
        damped_ef = ef * sqrt(1-pow(D,2))
    else:
        damped_ef = ef * sqrt(pow(D,2)-1)
    excitation_frequency_value = frequency_ratio_value * ef
    parameters.data = dict(names1=[u'\u03c9',u"\u03a9"],names2=["D",u'\u03c9*'],values1=[round(ef,4),round(excitation_frequency_value,4)],values2=[round(D,4),round(damped_ef,4)])
    glob_D.data     = dict(D = [D])
    glob_ef.data    = dict(ef = [ef])
    glob_damped_ef.data = dict(damped_ef = [damped_ef])
    glob_excitation_frequency_value.data = dict(excitation_frequency_value = [excitation_frequency_value])
    # deactivate play button if there exists no solution for these configurations
    if force_value > 0 and D>=1:
        play_pause_button.disabled = True
        pause()
    else:
        play_pause_button.disabled = False
        

play_pause_button = Button(label="Play", button_type="success",width=100)
play_pause_button.on_click(play_pause)
    
stop_button = Button(label="Stop", button_type="success", width=100)
stop_button.on_click(stop)

reset_button = Button(label="Reset", button_type="success",width=100)
reset_button.on_click(reset)

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

# grid plot of phase angle and amplification
gp = gridplot([p_af,p_pa],ncols=1,plot_width=250,plot_height=250,merge_tools=True,toolbar_location="below",toolbar_options=dict(logo=None))  # for gridpot we need to disable logo again

## Send to window
hspace = 20
curdoc().add_root(column(description,\
    row(column(row(column(Spacer(height=200),play_pause_button,stop_button,reset_button),Spacer(width=10),fig),Spacer(height=hspace),row(Spacer(width=100),parameter_table)),p,Spacer(width=10),gp), \
    row(mass_input,Spacer(width=hspace),spring_constant_input,Spacer(width=hspace),damping_coefficient_input), \
    row(initial_displacement_input,Spacer(width=hspace),initial_velocity_input), \
    row(frequency_ratio_input,Spacer(width=hspace),force_value_input) ))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '