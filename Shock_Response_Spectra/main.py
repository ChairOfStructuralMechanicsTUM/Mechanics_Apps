from __future__ import division
from Spring import *
from Dashpot import *
from Mass import *


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
from latex_support import LatexDiv
from math import sqrt, exp, pow, sin , cos, ceil, pi, atan2, sinh, cosh
from numpy import convolve 
import numpy 

## initial values
initial_spring_constant_value = 1.
initial_damping_coefficient_value = 0.5
initial_displacement_value = 0
TimePeriodRatio = 5
force_value = 1.
Force_duration = 1
ForceInput = ""
h = []
FI =[]
final = []

## input parameters for the analytic solution
Te = Force_duration/TimePeriodRatio   

W = 2*pi/Te
initial_mass_value = initial_spring_constant_value /pow(W,2)
D = initial_damping_coefficient_value
WD = W * sqrt(1-pow(D,2))

s=0
t=0
dt=0.02

mass = CircularMass(initial_mass_value,0,10,2,2)
spring = Spring((-2,.75),(-2,8),7,initial_spring_constant_value)
damper = Dashpot((2,.75),(2,8),initial_damping_coefficient_value)

Bottom_Line = ColumnDataSource(data = dict(x=[-2,2],y=[8,8]))
Linking_Line = ColumnDataSource(data = dict(x=[0,0],y=[8,10]))

displacement = ColumnDataSource(data = dict(t=[0],s=[initial_displacement_value]))

arrow_line = ColumnDataSource(data = dict(x1=[0],y1=[15],x2=[0],y2=[12]))
omega_max = ColumnDataSource(data = dict(beta=[0],phi=[0]))
t_max = ColumnDataSource(data = dict(beta=[0],phi=[0]))
Force_input = ColumnDataSource(data = dict(beta=[0],phi=[0]))

Force_input.stream(dict(beta=[0],phi=[1]))
Force_input.stream(dict(beta=[1],phi=[1]))
Force_input.stream(dict(beta=[1.0001],phi=[0]))
Force_input.stream(dict(beta=[2],phi=[0]))

parameters = ColumnDataSource(data = dict(names1=[u'\u03c9',"Te"],names2=["D",u'\u03c9*'],values1=[round(W,4),round(Te,4)],values2=[round(D,4),round(WD,4)]))
Active=False

def InputForce(t):
    if (ForceInput == "Rectangular"):
        return rect(t)
    elif (ForceInput == "Triangular"):
        return Triangular(t)
def rect(t):
    return where(t<=1, 1, 0)
def Triangular(t):
    return where(t<=1, t, 0)

def evolve():
    global Bottom_Line, Linking_Line, t 
    global mass, spring, damper, initial_displacement_value, TimePeriodRatio, force_value
    global W, WD, D, Te
    global ForceInput, h, FI, final
    
    #########
    k = spring.getSpringConstant
    print("Values used in plot")
    print(k)
    print(W)
    print(WD)
    print(D)
    
    if(t==0):
        for i in range(0,1000,1): # making rectangular function 
            T= i*0.02
            if (T<=1):
                FI.append(1) 
            else:
                FI.append(0)

            x=(1/(float(mass.Getmass())*WD))*exp(-D*W*T)*sin(WD*T) 
            h.append(x)
        final = convolve(FI,h,mode='full')
        print("convolution done")
    
    Tiii =int(t/0.02)
    move_system(-final[Tiii])
    displacement.stream(dict(t=[t],s=[final[Tiii]]))
    t+=dt

title_box = Div(text="""<h2 style="text-align:center;">Shock response spectra </h2>""",width=1000)

# sdof drawing
fig = figure(title="", tools="", x_range=(-7,7), y_range=(0,20),width=270,height=225)
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
p = figure(title="", y_range=(20,-20), x_range=Range1d(bounds=(0,1000), start=0, end=20), height=550, \
    toolbar_location="right", tools=[hover,"ywheel_zoom,xwheel_pan,pan,reset"]) #ywheel_zoom,xwheel_pan,reset,
p.line(x='t',y='s',source=displacement,color="#e37222",line_width=2,legend="Total Displacement",muted_color="#e37222",muted_alpha=0.2)
p.axis.major_label_text_font_size="12pt"
p.axis.axis_label_text_font_style="normal"
p.axis.axis_label_text_font_size="14pt"
p.xaxis.axis_label="Time [s]"
p.yaxis.axis_label="Displacement [u/(F/k)]"
p.legend.location="top_right"
p.legend.click_policy="mute"


p_af = figure(title="", tools="", x_range=(0,3.0), y_range=(0,5), width=300, height=300)
p_af.line(x='beta', y='phi', source=omega_max, color="#a2ad00")
p_af.yaxis.axis_label="w_max"
p_pa = figure(title="", tools="", x_range=(0,3.0), y_range=(0,180), width=300, height=300)
p_pa.line(x='beta', y='phi', source=t_max, color="#a2ad00")
p_pa.xaxis.axis_label="Tmax to T0 ratio"
p_pa.yaxis.axis_label="t_max"
p_pa.yaxis.ticker = FixedTicker(ticks=[0,90,180])

InputForce = figure(title="", tools="", x_range=(0,3.0), y_range=(0,2), width=300, height=150)
InputForce.line(x='beta', y='phi', source=Force_input, color="#a2ad00")
InputForce.xaxis.axis_label="Time(s)"
InputForce.yaxis.axis_label="Force(N)"
InputForce.yaxis.ticker = FixedTicker(ticks=[0,90,180])

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


## Create slider to choose damping coefficient
def change_damping_coefficient(attr,old,new):
    global damper
    damper.changeDamperCoeff(float(new))
    updateParameters()

damping_coefficient_input = Slider(title="Damping coefficient [Ns/m]", value=initial_damping_coefficient_value, callback_policy="mouseup", start=0.0, end=1, step=0.05,width=400)
damping_coefficient_input.on_change('value',change_damping_coefficient)

## Create slider to choose the frequency ratio
def change_frequency_ratio(attr,old,new):
    global Active, TimePeriodRatio
    if (not Active):
        TimePeriodRatio = new
        updateParameters()
        

frequency_ratio_input = Slider(title="Impulse duration to natural period ratio", value=TimePeriodRatio, start=0.1, end=3.0, step=0.1,width=400)
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
    global displacement, t, s, Bottom_Line, Linking_Line, spring, mass, damper, initial_displacement_value, force_value
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

def reset():
    stop()
    mass_input.value = initial_mass_value
    spring_constant_input.value = initial_spring_constant_value
    damping_coefficient_input.value = initial_damping_coefficient_value
    initial_displacement_input.value = initial_displacement_value
    t=0
    s=0

    #this could reset also the plot, but needs the selenium package:
    #reset_button = selenium.find_element_by_class_name('bk-tool-icon-reset')
    #click_element_at_position(selenium, reset_button, 10, 10)

def updateParameters():
    #input
    global mass, spring, damper, initial_displacement_value, TimePeriodRatio, force_value,initial_spring_constant_value,Force_duration
    #output
    global W, WD, D, Te, displacement, amplification_function, parameters, FI, final, h
    
    Te = Force_duration/TimePeriodRatio   
    W = 2*pi/Te
    mass.changeMass(initial_spring_constant_value /pow(W,2))
    D = float(damper.getDampingCoefficient)
    WD = W * sqrt(1-pow(D,2))  
    print("new WD",WD)   
    FI *= 0
    final *= 0
    h *= 0
    for i in range(0,1000,1): # making rectangular function 
        T= i*0.02
        if (T<=1):
            FI.append(1) 
        else:
            FI.append(0)

        x=(1/(mass.Getmass()*WD))*exp(-D*W*T)*sin(WD*T) 
        h.append(x)
    final = convolve(FI,h,mode='full')

    parameters.data = dict(names1=[u'\u03c9',"Te"],names2=["D",u'\u03c9*'],values1=[round(W,4),round(Te,4)],values2=[round(D,4),round(WD,4)])

play_button = Button(label="Play", button_type="success",width=100)
play_button.on_click(play)
pause_button = Button(label="Pause", button_type="success",width=100)
pause_button.on_click(pause)
stop_button = Button(label="Reset", button_type="success", width=100)
stop_button.on_click(stop)
# reset_button = Button(label="Reset", button_type="success",width=100)
# reset_button.on_click(reset)

def ChangeForce(forcetype):
    if forcetype == "Triangular":
        ForceInput = "Triangular"
        Force_input.data=dict(beta=[0],phi=[0])
        Force_input.stream(dict(beta=[0],phi=[0]))
        Force_input.stream(dict(beta=[1],phi=[1]))
        Force_input.stream(dict(beta=[1.0001],phi=[0]))
        Force_input.stream(dict(beta=[2],phi=[0]))
    elif forcetype == "Rectangular":
        ForceInput = "Rectangular"
        Force_input.data=dict(beta=[0],phi=[0])
        Force_input.stream(dict(beta=[0],phi=[1]))
        Force_input.stream(dict(beta=[1],phi=[1]))
        Force_input.stream(dict(beta=[1.0001],phi=[0]))
        Force_input.stream(dict(beta=[2],phi=[0]))
    else:
        ForceInput = "Sinusoidal" 
        print("Sinusoidal")

def ForceSelection(attr,old,new):   
    ChangeForce(new)
    
Force_select = Select(title="Force:", value="Triangular",
    options=["Triangular", "Rectangular", "Sinusoidal"])
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
    row(column(row(column(row(column(fig,column(play_button,Spacer(width = 10),pause_button,column(Spacer(width = 10),stop_button))),column(Force_select,InputForce,parameter_table)),Spacer(height=10),p)),Spacer(height=hspace)),Spacer(width=10),\
    column(damping_coefficient_input,frequency_ratio_input,Spacer(height=hspace),gridplot([p_af,p_pa],ncols=1,plot_width=400,plot_height=350,merge_tools=True,toolbar_location="below"))\
    ), \
     ))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '