"""
Damped oscillator - shows the motion of a damped oscillator depending on different parameters

"""
# general imports

# bokeh imports
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import Button, HoverTool, Range1d, ColumnDataSource
from bokeh.layouts import column, row, Spacer

# internal imports
from DO_Spring import DO_Spring
from DO_Dashpot import DO_Dashpot
from DO_Mass import DO_CircularMass
from DO_Coord import DO_Coord

# latex integration
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv, LatexSlider

#---------------------------------------------------------------------#

# z = lam/(2*sqrt(k*m))
# z = 1 => crit damped
# z > 1 => over damped
# z < 1 => under damped

## initial values
initial_mass_value     = 8
initial_kappa_value    = 50
initial_lambda_value   = 2
initial_velocity_value = 0
s  = 0
t  = 0
dt = 0.03

mass = DO_CircularMass(initial_mass_value,0,9,2,2)
mass.changeInitV(initial_velocity_value)
spring  = DO_Spring((-2,18),(-2,11),7,initial_kappa_value)
dashpot = DO_Dashpot((2,18),(2,11),initial_lambda_value)
mass.linkObj(spring,(-2,11))
mass.linkObj(dashpot,(2,11))
Bottom_Line  = ColumnDataSource(data = dict(x=[-2,2],y=[11,11]))
Linking_Line = ColumnDataSource(data = dict(x=[0,0],y=[11,9]))
Position     = ColumnDataSource(data = dict(t=[0],s=[0]))

## global variables
glob_vars = dict(cid     = None,  # callback id
                 t       = t,     # time
                 s       = s,     # posiition
                 mass    = mass,
                 spring  = spring,
                 dashpot = dashpot)


# callback function when simulation is running
def evolve():
    t    = glob_vars['t']    # input/output
    s    = glob_vars['s']    # input/output
    mass = glob_vars['mass'] # input/output
    mass.FreezeForces()
    disp = mass.evolve(dt)
    s += disp.y
    Bottom_Line.data  = dict(x=[-2,2],y=[11+s, s+11]) #      /output
    Linking_Line.data = dict(x=[0,0],y=[11+s, 9+s])   #      /output
    t += dt
    Position.stream(dict(t=[t],s=[s])) #      /output
    glob_vars['t'] = t
    glob_vars['s'] = s

########################
#  figure definitions  #
########################

# drawing of the oscillator / SDOF system
fig = figure(title="", tools="", x_range=(-7,7), y_range=(0,20),width=350,height=500)
fig.title.text_font_size="20pt"
fig.axis.visible = False
fig.grid.visible = False
fig.outline_line_color = None
fig.toolbar.logo = None
spring.plot(fig,width=2)
dashpot.plot(fig,width=2)
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

# plot - displacement vs. time
hover = HoverTool(tooltips=[("time","@t s"), ("displacement","@s m")])
p = figure(title="", y_range=(-5,5), x_range=Range1d(bounds=(0,1000), start=0, end=20), height=500, \
    toolbar_location="right", tools=[hover,"ywheel_zoom,xwheel_pan,pan,reset"]) #ywheel_zoom,xwheel_pan,reset,
p.line(x='t',y='s',source=Position,color="black")
p.axis.major_label_text_font_size="12pt"
p.axis.axis_label_text_font_style="normal"
p.axis.axis_label_text_font_size="14pt"
p.xaxis.axis_label="Time [s]"
p.yaxis.axis_label="Displacement [m]"
p.toolbar.logo=None

########################
#  slider definitions  #
########################

def change_mass(attr,old,new):
    mass = glob_vars['mass'] # input/output
    mass.changeMass(new)

## Create slider to choose mass of blob
mass_input = LatexSlider(title="\\text{Mass } \\left[ \mathrm{kg} \\right]: ", value=initial_mass_value, start=0.5, end=10.0, step=0.5, width=400)
mass_input.on_change('value',change_mass)

def change_kappa(attr,old,new):
    spring = glob_vars['spring'] # input/output
    spring.changeSpringConst(new)

## Create slider to choose spring constant
kappa_input = LatexSlider(title="\\text{Spring stiffness } \\left[ \\frac{N}{m} \\right]: ", value=initial_kappa_value, start=0.0, end=200, step=10,width=400)
kappa_input.on_change('value',change_kappa)

def change_lam(attr,old,new):
    dashpot = glob_vars['dashpot'] # input/output
    dashpot.changeDamperCoeff(new)

## Create slider to choose damper coefficient
lam_input = LatexSlider(title="\\text{Damping coefficient } \\left[ \\frac{Ns}{m} \\right]: ", value=initial_lambda_value, start=0.0, end=60, step=1,width=400)
lam_input.on_change('value',change_lam)

def change_initV(attr,old,new):
    mass   = glob_vars['mass']   # input/output
    mass.changeInitV(new)

## Create slider to choose initial velocity
initV_input = LatexSlider(title="\\text{Initial velocity } \\left[ \\frac{m}{s} \\right]: ", value=initial_velocity_value, start=-10.0, end=10.0, step=0.5,width=400)
initV_input.on_change('value',change_initV)

########################
#  button definitions  #
########################

def play_pause():
    if play_pause_button.label == "Play":
        glob_vars["cid"] = curdoc().add_periodic_callback(evolve,dt*1000)
        play_pause_button.label = "Pause"
        initV_input.disabled = True # disable initial velocity slider during simulation
    elif play_pause_button.label == "Pause":
        curdoc().remove_periodic_callback(glob_vars["cid"])
        play_pause_button.label = "Play"


def stop():
    mass    = glob_vars['mass']    # input/output
    spring  = glob_vars['spring']  # input/output
    dashpot = glob_vars['dashpot'] # input/output
    # if stop is pressed before pause, i.e. while the callback is still in use
    if curdoc().session_callbacks:
        curdoc().remove_periodic_callback(glob_vars["cid"])
        play_pause_button.label = "Play"
    glob_vars['t'] = 0                          #      /output
    glob_vars['s'] = 0                          #      /output
    Position.data=dict(t=[0],s=[0])             #      /output
    Bottom_Line.data = dict(x=[-2,2],y=[11,11]) #      /output
    Linking_Line.data = dict(x=[0,0],y=[11,9])  #      /output
    spring.compressTo(DO_Coord(-2,18),DO_Coord(-2,11))
    dashpot.compressTo(DO_Coord(2,18),DO_Coord(2,11))
    mass.moveTo((0,9))
    mass.resetLinks(spring,(-2,11))
    mass.resetLinks(dashpot,(2,11))
    mass.changeInitV(initV_input.value)
    mass.nextStepForces=[]
    mass.nextStepObjForces=[]
    initV_input.disabled = False # enable initial velocity slider after the simulation
    
def reset():
    stop()
    mass = glob_vars['mass'] # input/output
    mass_input.value = initial_mass_value
    kappa_input.value = initial_kappa_value
    lam_input.value = initial_lambda_value
    initV_input.value = initial_velocity_value
    mass.changeInitV(initial_velocity_value)

    #this could reset also the plot, but needs the selenium package:
    #reset_button = selenium.find_element_by_class_name('bk-tool-icon-reset')
    #click_element_at_position(selenium, reset_button, 10, 10)

play_pause_button = Button(label="Play", button_type="success",width=100)
play_pause_button.on_click(play_pause)
stop_button = Button(label="Stop", button_type="success", width=100)
stop_button.on_click(stop)
reset_button = Button(label="Reset", button_type="success",width=100)
reset_button.on_click(reset)


########################
#  layout definitions  #
########################

# add app description
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)

## Send to window
curdoc().add_root(column(description, \
    row(column(Spacer(height=100),play_pause_button,stop_button,reset_button),Spacer(width=10),fig,p), \
    row(mass_input,Spacer(width=10),kappa_input), \
    Spacer(height=30), \
    row(lam_input,Spacer(width=10),initV_input)))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
