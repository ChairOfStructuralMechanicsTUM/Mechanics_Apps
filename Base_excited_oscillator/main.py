from beo_spring import Spring
from beo_dashpot import Dashpot
from beo_mass import RectangularMass
from beo_coord import Coord

from bokeh.plotting import figure, output_file
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import Slider, Button, Div, ColumnDataSource

from math import sin, radians, sqrt, pi, pow, atan2
from copy import deepcopy
import numpy as np
import yaml

from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv, LatexSlider



# change language
std_lang = 'en'
flags    = ColumnDataSource(data=dict(show=['off'], lang=[std_lang]))
strings  = yaml.safe_load(open('Base_excited_oscillator/static/strings.json', encoding='utf-8'))

glob_active = ColumnDataSource(data=dict(Active=[False]))

# z = lam/(2*sqrt(k*m))
# z = 1 => crit damped
# z > 1 => over damped
# z < 1 => under damped

## initial values
initial_mass_value = 5.0
initial_kappa_value = 100.0
initial_lambda_value = 5.0
Omega = 20*pi/27 #Excitation Frequency Omega = (2*pi/9)*(10/3)
eta = np.linspace(0,3,301)
V = []
PhaseShift = []
current_eta = Omega/sqrt(initial_kappa_value/initial_mass_value)
for i in range (0,301):
    x = eta[i]
    V.append(pow(x,2)/sqrt(pow(1-pow(x,2),2)+pow(2*x*initial_lambda_value/(2*sqrt(initial_mass_value*initial_kappa_value)),2)))
    PhaseShift.append(abs(atan2(-initial_lambda_value*x/sqrt(initial_mass_value*initial_kappa_value), 1-pow(x,2))))
current_V = pow(current_eta,2)/sqrt(pow(1-pow(current_eta,2),2)+pow(2*current_eta*initial_lambda_value/(2*sqrt(initial_mass_value*initial_kappa_value)),2))
current_PhaseShift = abs(atan2(-initial_lambda_value*current_eta/sqrt(initial_mass_value*initial_kappa_value), 1-pow(current_eta,2)))

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
Floor = ColumnDataSource(data = dict(x=[],y=[]))
Floor_source = ColumnDataSource(data = dict(x=[],y=[]))
amplification_function = ColumnDataSource(data = dict(eta=eta, V=V))
current_eta_V = ColumnDataSource(data = dict(eta=[current_eta], V=[current_V]))
phase_angle = ColumnDataSource(data = dict(eta=eta, PhaseShift=PhaseShift))
current_eta_PhaseShift = ColumnDataSource(data = dict(eta=[current_eta], PhaseShift=[current_PhaseShift]))

dt=0.0075
t=0     # time = 0
s=0     # mass displacement = 0
sOld=0  # used to calculate the relative displacement
Floor_angle=561
maxX=20

glob_g1BaseOscillator = ColumnDataSource(data = dict(g1BaseOscillator = [None]))
glob_t = ColumnDataSource(data = dict(t = [t]))
glob_s = ColumnDataSource(data = dict(s = [s]))
glob_sOld = ColumnDataSource(data = dict(sOld = [sOld]))
glob_oldBase = ColumnDataSource(data = dict(oldBase = [oldBase]))
glob_Floor_angle = ColumnDataSource(data = dict(Floor_angle = [Floor_angle]))


# Defining Floor
def InitialFloor():
    [Floor_angle] = glob_Floor_angle.data["Floor_angle"]
    [oldBase] = glob_oldBase.data["oldBase"]
    #x_range = (-7,7)
    Floor.data = dict(x=[],y=[])
    #for x in (-7,2)    
    for i in range(0,360):
        Floor.data['x'].append((i/40.0) - 7.0)
        Floor.data['y'].append(4)
    #for x in (2,7)
    for i in range(361,561):
        Floor.data['x'].append((i/40.0) - 7.0)
        Floor.data['y'].append(4-sin(radians(i))) 

    Floor_source.data = deepcopy(dict(Floor.data))
    stable_pos= 16 - 9.81*float(mass_input.value)/float(kappa_input.value) # Find position of static equilibrium
    mass.moveTo(-4,stable_pos,8,2)      # moveTo method (x,y,w,h) 
    spring.compressTo(Coord(-2,stable_pos),Coord(-2,9)) # compressTo method (start,end)
    dashpot.compressTo(Coord(2,stable_pos),Coord(2,9),0)
    mass.resetLinks(spring,(-2,stable_pos))     # move spring's upper end to the position of static equilibrium
    mass.resetLinks(dashpot,(2,stable_pos))     # move dashpot's upper end to the position of static equilibrium
    oldBase=9
    Floor_angle=561

    glob_Floor_angle.data = dict(Floor_angle = [Floor_angle])
    glob_oldBase.data = dict(oldBase = [oldBase])


# Update Floor
def updateFloor():
    [Floor_angle] = glob_Floor_angle.data["Floor_angle"]
    Floor.data['y'].pop(0)   # removes the first element of Floor['y'] list
    Floor.data['y'].append(4-sin(radians(Floor_angle)))  # update the y coordinate at x=7
    Floor_source.data = deepcopy(dict(Floor.data))   # deep copy creates a new object and recursively adds the copies
    Floor_angle+=1  # update floor angle

    glob_Floor_angle.data = dict(Floor_angle = [Floor_angle])

# Evolve problem
def evolve():
    [t] = glob_t.data["t"]                 
    [s] = glob_s.data["s"] 
    [sOld] = glob_sOld.data["sOld"]
    [oldBase] = glob_oldBase.data["oldBase"]

    updateFloor()
    baseShift=Floor.data['y'][280]-4 # (y value at x=0) - 4
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
    s-=Floor.data['y'][280]-4 # subtract base displacement from absolute displacement
    t+=0.0075 # update time
    
    Position.stream(dict(t=[t],s=[s]))

    glob_t.data = dict(t = [t])
    glob_s.data = dict(s = [s])
    glob_sOld.data = dict(sOld = [sOld])
    glob_oldBase.data = dict(oldBase = [oldBase])


def change_mass(attr,old,new):
    mass.changeMass(new)
    if (t==0):
        InitialFloor()  # update position of static equilibrium for the new mass
    update_current_ratio()
    update_amplification_function()
    update_phase_angle()
## Create slider to choose mass of blob
mass_input = LatexSlider(title="\\text{Mass} \\left[ \\mathrm{kg} \\right]: ", value=5, start=0.3, end=10.0, step=0.1, width=400)
mass_input.on_change('value',change_mass)

def change_kappa(attr,old,new):
    spring.changeSpringConst(new)
    if (t==0):
        InitialFloor()  # update position of static equilibrium for the new mass
    update_current_ratio()
    update_amplification_function()
    update_phase_angle()
## Create slider to choose spring constant
kappa_input = LatexSlider(title="\\text{Spring stiffness} \\left[ \\frac{\\mathrm{N}}{\\mathrm{m}} \\right]: ", value=100, start=10.0, end=200, step=10, width=400)
kappa_input.on_change('value',change_kappa)

def change_lam(attr,old,new):
    dashpot.changeDamperCoeff(new)
    if (t==0):
        InitialFloor()  # update position of static equilibrium for the new mass
    update_current_ratio()
    update_amplification_function()
    update_phase_angle()
## Create slider to choose damper coefficient
lam_input = LatexSlider(title="\\text{Damper Coefficient} \\left[ \\frac{\\mathrm{Ns}}{\\mathrm{m}} \\right]: ", value=5, start=0.0, end=10, step=0.1, width=400)
lam_input.on_change('value',change_lam)

InitialFloor() # call floor definition after defining necessary variables

def update_current_ratio():
    [current_eta] = current_eta_V.data["eta"] 
    [current_V] = current_eta_V.data["V"] 
    [current_PhaseShift] = current_eta_PhaseShift.data["PhaseShift"]
    current_eta = Omega/sqrt(kappa_input.value/mass_input.value)
    if current_eta == 1 and lam_input.value == 0:
        current_V = 1000
        current_PhaseShift = pi/2
    else:
        current_V = pow(current_eta,2)/sqrt(pow(1-pow(current_eta,2),2)+pow(2*current_eta*lam_input.value/(2*sqrt(mass_input.value*kappa_input.value)),2))
        current_PhaseShift = abs(atan2(-lam_input.value*current_eta/sqrt(mass_input.value*kappa_input.value), 1-pow(current_eta,2)))
    current_eta_V.data = dict(eta=[current_eta], V=[current_V])
    current_eta_PhaseShift.data = dict(eta=[current_eta], PhaseShift=[current_PhaseShift])

def update_amplification_function():
    V = amplification_function.data["V"]
    for i in range (0,301):
        x = eta[i]
        if x == 1 and lam_input.value == 0:
            V[i] = 1000
        else: 
            V[i] = pow(x,2)/sqrt(pow(1-pow(x,2),2)+pow(2*x*lam_input.value/(2*sqrt(mass_input.value*kappa_input.value)),2))
    amplification_function.data = dict(eta=eta, V=V)

def update_phase_angle():
    PhaseShift = phase_angle.data["PhaseShift"]
    for i in range (0,301):
        x = eta[i]
        if x == 1 and lam_input.value == 0:
            PhaseShift[i] = pi/2
        else:
            PhaseShift[i] = abs(atan2(-lam_input.value*x/sqrt(mass_input.value*kappa_input.value), 1-pow(x,2)))
    phase_angle.data = dict(eta=eta, PhaseShift=PhaseShift)

def disable_all_sliders(d=True):
    mass_input.disabled = d
    kappa_input.disabled = d
    lam_input.disabled = d

def play_pause():
    glob_active.data["Active"][0] = not glob_active.data["Active"][0]

    if glob_active.data["Active"][0]:
        play()
    else: 
        pause()

def pause():
    [g1BaseOscillator] = glob_g1BaseOscillator.data["g1BaseOscillator"]
    [lang] = flags.data["lang"]
    play_pause_button.label = strings["play_pause_button.label"]['off'][lang]
    try:
        curdoc().remove_periodic_callback(g1BaseOscillator)
    except ValueError:
        print("WARNING: callback_id was already removed - this can happen if stop was pressed after pause, usually no serious problem; if stop was not called this part should be changed")
        # callback_id is not set to None or similar, the object hex-code stays -> no if == None possible -> use try/except
    except:
        print("This error is not covered: ", sys.exc_info()[0])
        raise

def play():
    [g1BaseOscillator] = glob_g1BaseOscillator.data["g1BaseOscillator"]
    [lang] = flags.data["lang"]
    play_pause_button.label = strings["play_pause_button.label"]['on'][lang]
    disable_all_sliders(True) # while the app is running, it's not possible to change any values
    # Add a callback to be invoked on a session periodically
    g1BaseOscillator = curdoc().add_periodic_callback(evolve,dt*1000)
    glob_g1BaseOscillator.data = dict(g1BaseOscillator = [g1BaseOscillator])

def stop():
    # set everything except mass value, lam value and kappa value to initial settings
    glob_active.data["Active"][0] = False
    [t] = glob_t.data["t"]                 
    [s] = glob_s.data["s"] 
    [sOld] = glob_sOld.data["sOld"]
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

    glob_t.data = dict(t = [t])
    glob_s.data = dict(s = [s])
    glob_sOld.data = dict(sOld = [sOld])

def reset():
    # set everything to initial settings
    glob_active.data["Active"][0] = False
    stop()
    mass_input.value=5.0
    lam_input.value=5.0
    kappa_input.value=100.0

# Plot evolution of elements
fig = figure(title="", tools="", x_range=(-7,7), y_range=(0,20),width=315,height=450)
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
p = figure(title="", tools=["ywheel_zoom,xwheel_pan,pan,reset"], y_range=(-5,5), x_range=(0,maxX),width=450,height=450)
p.tools.disabled = True
p.line(x='t',y='s',source=Position,color="black")
p.axis.major_label_text_font_size="12pt"
p.axis.axis_label_text_font_style="normal"
p.axis.axis_label_text_font_size="14pt"
p.xaxis.axis_label="Time [s]"
p.yaxis.axis_label="Relative Displacement [m]"
p.toolbar.logo = None

# Plot amplification function
amp = figure(title="", tools="", x_range=(0,3.0), y_range=(0,5), width=250, height=218)
amp.line(x="eta", y="V", source=amplification_function, color="#a2ad00")
amp.circle(x='eta', y='V', size=10, color="#e37222", source=current_eta_V)
amp.yaxis.axis_label="Amplification"
amp.toolbar.logo = None #removes bokeh logo
amp.axis.axis_label_text_font_style="normal"

# Plot phase angle
pa = figure(title="", tools="", x_range=(0,3.0), y_range=(0,3.5), width=250, height=218)
pa.line(x="eta", y="PhaseShift", source=phase_angle, color="#a2ad00")
pa.circle(x='eta', y='PhaseShift', size=10, color="#e37222", source=current_eta_PhaseShift)
pa.yaxis.axis_label="Phase angle [rad]"
pa.toolbar.logo = None #removes bokeh logo
pa.xaxis.axis_label="Excitation Frequency Ratio"
pa.axis.axis_label_text_font_style="normal"

# Define buttons and what happens when clicked
play_pause_button = Button(label="Play", button_type="success",width=100)
play_pause_button.on_click(play_pause)
reset_button = Button(label="Reset", button_type="success",width=100)
reset_button.on_click(reset)
stop_button = Button(label="Stop", button_type="success",width=100)
stop_button.on_click(stop)


######################################
# Change language
######################################

def changeLanguage():
    [lang] = flags.data["lang"]
    if lang == "en":
        setDocumentLanguage('de')
    elif lang == "de":
        setDocumentLanguage('en')

def setDocumentLanguage(lang):
    flags.patch( {'lang':[(0,lang)]} )
    for s in strings:
        if 'checkFlag' in strings[s]:
            flag = flags.data[strings[s]['checkFlag']][0]
            exec( (s + '=\"' + strings[s][flag][lang] + '\"').encode(encoding='utf-8') )
        elif 'isCode' in strings[s] and strings[s]['isCode']:
            exec( (s + '=' + strings[s][lang]).encode(encoding='utf-8') )
        else:
            exec( (s + '=\"' + strings[s][lang] + '\"').encode(encoding='utf-8') )
    
    [Active] = glob_active.data["Active"]
    if Active:
        play_pause_button.label = strings["play_pause_button.label"]['on'][lang]
    else:
        play_pause_button.label = strings["play_pause_button.label"]['off'][lang]

lang_button = Button(button_type="success", label="Zu Deutsch wechseln")
lang_button.on_click(changeLanguage)


######################################
# Page layout
######################################

## Send to window
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1010)

curdoc().add_root(column(row(Spacer(width=700),lang_button), description,row(column(Spacer(height=100),play_pause_button,stop_button,reset_button),Spacer(width=10),fig,p, column(amp, Spacer(height=1), pa)),
    row(mass_input),row(kappa_input),row(lam_input)))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '



