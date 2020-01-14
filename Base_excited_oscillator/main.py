from Spring import *
from Dashpot import *
from Mass import *
from bokeh.plotting import figure, output_file
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import Slider, Button, Div
from math import sin, radians
from os.path import dirname, join, split

from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv, LatexSlider


# z = lam/(2*sqrt(k*m))
# z = 1 => crit damped
# z > 1 => over damped
# z < 1 => under damped

## initial values
initial_mass_value = 5.0
initial_kappa_value = 100.0
initial_lambda_value = 5.0

mass = RectangularMass(initial_mass_value,-4,16,8,2)     # an object of RectangularMass class (mass, x, y, w, h)
spring = Spring((-2,16),(-2,9),7,initial_kappa_value)   # an object of Spring class (start,end,x0,kappa,spacing)
dashpot = Dashpot((2,16),(2,9),initial_lambda_value)       # an object of Dashpot class (start,end,lam)

oldBase = 9     # initial y coordinate of the horizontal line 
mass.linkObj(spring,(-2,16))    # Link spring to mass
mass.linkObj(dashpot,(2,16))    # Link dashpot to mass
Bottom_Line = ColumnDataSource(data = dict(x=[-2,2],y=[9,9]))   # Horizontal line
Linking_Line = ColumnDataSource(data = dict(x=[0,0],y=[9,5]))   # Vertical line
Position = ColumnDataSource(data = dict(t=[0],s=[0]))
Wheel_source = ColumnDataSource(data = dict(x=[0],y=[5]))
Floor = dict(x=[],y=[])
Floor_source = ColumnDataSource(data = dict(x=[],y=[]))
dt=0.0075
t=0     # time = 0
s=0     # mass displacement = 0
sOld=0  # used to calculate the relative displacement
Floor_angle=561
Active=False
maxX=20

# Defining Floor
def InitialFloor():
    global Floor, Floor_source, oldBase, Floor_angle
    #x_range = (-7,7)
    Floor = dict(x=[],y=[])
    #for x in (-7,2)    
    for i in range(0,360):
        Floor['x'].append((i/40.0) - 7.0)
        Floor['y'].append(4)
    #for x in (2,7)
    for i in range(361,561):
        Floor['x'].append((i/40.0) - 7.0)
        Floor['y'].append(4-sin(radians(i))) 

    Floor_source.data = deepcopy(dict(Floor))
    stable_pos= 16 - 9.81*float(mass_input.value)/float(kappa_input.value) # Find position of static equilibrium
    mass.moveTo(-4,stable_pos,8,2)      # moveTo method (x,y,w,h) 
    spring.compressTo(Coord(-2,stable_pos),Coord(-2,9)) # compressTo method (start,end)
    dashpot.compressTo(Coord(2,stable_pos),Coord(2,9),0)
    mass.resetLinks(spring,(-2,stable_pos))     # move spring's upper end to the position of static equilibrium
    mass.resetLinks(dashpot,(2,stable_pos))     # move dashpot's upper end to the position of static equilibrium
    oldBase=9
    Floor_angle=561



# Update Floor
def updateFloor():
    global Floor, Floor_source, Floor_angle
    Floor['y'].pop(0)   # removes the first element of Floor['y'] list
    Floor['y'].append(4-sin(radians(Floor_angle)))  # update the y coordinate at x=7
    Floor_source.data = deepcopy(dict(Floor))   # deep copy creates a new object and recursively adds the copies
    Floor_angle+=1  # update floor angle

# Evolve problem
def evolve():
    global mass, Bottom_Line, Linking_Line, t, s, sOld, oldBase
    updateFloor()
    baseShift=Floor['y'][280]-4 # (y value at x=0) - 4
    Bottom_Line.data=dict(x=[-2,2],y=[9+baseShift,9+baseShift]) # Update horizontal line position
    Linking_Line.data=dict(x=[0,0],y=[9+baseShift,5+baseShift]) # Update vertical line position
    Wheel_source.data=dict(x=[0],y=[5+baseShift]) # Update Wheel position
    
    # moveVect: compare position of static equilibrium (9) with oldBase and current baseShift
    spring.movePoint(Coord(-2,oldBase),Coord(0,(9+baseShift)-oldBase)) # movePoint(start,moveVect)
    dashpot.movePoint(Coord(2,oldBase),Coord(0,(9+baseShift)-oldBase)) # movePoint(start,moveVect)
    oldBase+=baseShift  # update y coordinate of the horizontal line 
    
    mass.FreezeForces()
    disp=mass.EvolveMass(dt)
    s=sOld
    s+=disp.y # update mass displacement
    sOld=s
    s-=Floor['y'][280]-4 # subtract base displacement from absolute displacement
    t+=0.0075 # update time
    
    Position.stream(dict(t=[t],s=[s]))

def change_mass(attr,old,new):
    global mass,t 
    mass.changeMass(new)
    if (t==0):
        InitialFloor()  # update position of static equilibrium for the new mass
## Create slider to choose mass of blob
mass_input = LatexSlider(title="\\text{Mass} \\left[ \\mathrm{kg} \\right]: ", value=5, start=0.3, end=10.0, step=0.1, width=400)
mass_input.on_change('value',change_mass)

def change_kappa(attr,old,new):
    global spring,t
    spring.changeSpringConst(new)
    if (t==0):
        InitialFloor()  # update position of static equilibrium for the new mass
## Create slider to choose spring constant
kappa_input = LatexSlider(title="\\text{Spring stiffness} \\left[ \\frac{\\mathrm{N}}{\\mathrm{m}} \\right]: ", value=100, start=10.0, end=200, step=10, width=400)
kappa_input.on_change('value',change_kappa)

def change_lam(attr,old,new):
    global dashpot,t
    dashpot.changeDamperCoeff(new)
    if (t==0):
        InitialFloor()  # update position of static equilibrium for the new mass
## Create slider to choose damper coefficient
lam_input = LatexSlider(title="\\text{Damper Coefficient} \\left[ \\frac{\\mathrm{Ns}}{\\mathrm{m}} \\right]: ", value=5, start=0.0, end=10, step=0.1, width=400)
lam_input.on_change('value',change_lam)

InitialFloor() # call floor definition after defining necessary variables

def disable_all_sliders(d=True):
    mass_input.disabled = d
    kappa_input.disabled = d
    lam_input.disabled = d

def play_pause():
    if play_pause_button.label == "Play":
        play()
    else: 
        pause()

def pause():
    global Active, g1BaseOscillator
    if (Active):
        curdoc().remove_periodic_callback(g1BaseOscillator)
        play_pause_button.label = "Play"
        Active=False

def play():
    global Active, g1BaseOscillator
    if (not Active):
        disable_all_sliders(True) # while the app is running, it's not possible to change any values
         # Add a callback to be invoked on a session periodically
        g1BaseOscillator = curdoc().add_periodic_callback(evolve,dt*1000)
        play_pause_button.label = "Pause"
        Active=True

def stop():
    # set everything except mass value, lam value and kappa value to initial settings
    global t, s, sOld
    disable_all_sliders(False)
    pause()
    t=0                     
    s=0
    sOld=0                    
    Position.data=dict(t=[0],s=[0])            
    Bottom_Line.data = dict(x=[-2,2],y=[9,9]) 
    Linking_Line.data = dict(x=[0,0],y=[9,5])  
    Wheel_source.data = dict(x=[0],y=[5])
    InitialFloor()
    mass.nextStepForces=[]
    mass.nextStepObjForces=[]   
    mass.changeInitV(0.0)   
    maxX=20
    p.x_range.end=maxX

def reset():
    global Position, t, s, Bottom_Line, Linking_Line, spring, mass, dashpot, maxX
    
    mass_input.value=5.0
    lam_input.value=5.0
    kappa_input.value=100.0
    stop()

title_box = Div(text="",width=1000)

# Plot evolution of elements
fig = figure(title="", tools="", x_range=(-7,7), y_range=(0,20),width=350,height=500)
fig.title.text_font_size="20pt"
fig.xaxis.visible = False
fig.grid.visible = False
fig.outline_line_color = None
spring.plot(fig,width=2)
dashpot.plot(fig,width=2)
fig.line(x='x',y='y',source=Bottom_Line,color="black",line_width=3)
fig.line(x='x',y='y',source=Linking_Line,color="black",line_width=3)
fig.line(x='x',y='y',source=Floor_source,color="black",line_width=1)
fig.ellipse(x='x',y='y',width=2,height=2,source=Wheel_source,line_color="#E37222",fill_color=None,line_width=2)
mass.plot(fig)
fig.toolbar.logo = None

# Plot Mass-Displacement.vs.Time graph
p = figure(title="", tools=["ywheel_zoom,xwheel_pan,pan,reset"], y_range=(-5,5), x_range=(0,maxX),height=500)
p.line(x='t',y='s',source=Position,color="black")
p.axis.major_label_text_font_size="12pt"
p.axis.axis_label_text_font_style="normal"
p.axis.axis_label_text_font_size="14pt"
p.xaxis.axis_label="Time [s]"
p.yaxis.axis_label="Relative Displacement [m]"
p.toolbar.logo = None




# Define buttons and what happens when clicked
play_pause_button = Button(label="Play", button_type="success",width=100)
play_pause_button.on_click(play_pause)
reset_button = Button(label="Reset", button_type="success",width=100)
reset_button.on_click(reset)
stop_button = Button(label="Stop", button_type="success",width=100)
stop_button.on_click(stop)


## Send to window
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1010)
curdoc().add_root(column(
    description))

curdoc().add_root(column(title_box,row(column(Spacer(height=100),play_pause_button,stop_button,reset_button),Spacer(width=10),fig,p),
    row(mass_input),row(kappa_input),row(lam_input)))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '



