from DO_Spring import DO_Spring
from DO_Dashpot import DO_Dashpot
from DO_Mass import DO_CircularMass#, Mass, RectangularMass
from DO_Coord import DO_Coord
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import Slider, Button, Div, HoverTool, Range1d,ColumnDataSource
from os.path import dirname, join, split

# z = lam/(2*sqrt(k*m))
# z = 1 => crit damped
# z > 1 => over damped
# z < 1 => under damped

## initial values
initial_mass_value = 8
initial_kappa_value = 50
initial_lambda_value = 2
initial_velocity_value = 0
s=0
t=0
dt=0.03

mass = DO_CircularMass(initial_mass_value,0,9,2,2)
mass.changeInitV(initial_velocity_value)
spring = DO_Spring((-2,18),(-2,11),7,initial_kappa_value)
dashpot = DO_Dashpot((2,18),(2,11),initial_lambda_value)
mass.linkObj(spring,(-2,11))
mass.linkObj(dashpot,(2,11))
Bottom_Line = ColumnDataSource(data = dict(x=[-2,2],y=[11,11]))
Linking_Line = ColumnDataSource(data = dict(x=[0,0],y=[11,9]))
Position = ColumnDataSource(data = dict(t=[0],s=[0]))

# global variables
glob_active   = ColumnDataSource(data=dict(Active=[False]))
glob_callback = ColumnDataSource(data=dict(cid=[None])) # callback id
glob_t        = ColumnDataSource(data=dict(t=[t]))
glob_s        = ColumnDataSource(data=dict(s=[s]))
glob_mass     = ColumnDataSource(data=dict(m=[mass]))
glob_spring   = ColumnDataSource(data=dict(s=[spring]))
glob_dashpot  = ColumnDataSource(data=dict(d=[dashpot]))

def evolve():
    [t]    = glob_t.data['t']    # input/output
    [s]    = glob_s.data['s']    # input/output
    [mass] = glob_mass.data['m'] # input/output
    mass.FreezeForces()
    disp=mass.evolve(dt)
    s+=disp.y
    Bottom_Line.data=dict(x=[-2,2],y=[11+s, s+11]) #      /output
    Linking_Line.data=dict(x=[0,0],y=[11+s, 9+s])  #      /output
    t+=dt
    Position.stream(dict(t=[t],s=[s])) #      /output
    glob_t.data=dict(t=[t])
    glob_s.data=dict(s=[s])

title_box = Div(text="""<h2 style="text-align:center;">Spring pendulum</h2>""",width=1000)

# drawing
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
p.toolbar.logo=None

def change_mass(attr,old,new):
    [mass] = glob_mass.data['m'] # input/output
    mass.changeMass(new)

## Create slider to choose mass of blob
mass_input = Slider(title="Mass [kg]", value=initial_mass_value, start=0.5, end=10.0, step=0.5, width=400)
mass_input.on_change('value',change_mass)

def change_kappa(attr,old,new):
    [spring] = glob_spring.data['s'] # input/output
    spring.changeSpringConst(new)

## Create slider to choose spring constant
kappa_input = Slider(title="Spring stiffness [N/m]", value=initial_kappa_value, start=0.0, end=200, step=10,width=400)
kappa_input.on_change('value',change_kappa)

def change_lam(attr,old,new):
    [dashpot] = glob_dashpot.data['d'] # input/output
    dashpot.changeDamperCoeff(new)

## Create slider to choose damper coefficient
lam_input = Slider(title="Damping coefficient [Ns/m]", value=initial_lambda_value, start=0.0, end=60, step=1,width=400)
lam_input.on_change('value',change_lam)

def change_initV(attr,old,new):
    [mass]   = glob_mass.data['m']        # input/output
    [Active] = glob_active.data["Active"] # input/
    if (not Active):
        mass.changeInitV(new)

## Create slider to choose initial velocity
initV_input = Slider(title="Initial velocity [m/s]", value=initial_velocity_value, start=-10.0, end=10.0, step=0.5,width=400)
initV_input.on_change('value',change_initV)

def pause():
    [g1DampedOscilator] = glob_callback.data["cid"]  # input/
    [Active]            = glob_active.data["Active"] # input/output
    if (Active):
        curdoc().remove_periodic_callback(g1DampedOscilator)
        glob_active.data=dict(Active=[False])

def play():
    [Active] = glob_active.data["Active"] # input/output
    if (not Active):
        g1DampedOscilator  = curdoc().add_periodic_callback(evolve,dt*1000) #dt in milliseconds
        glob_callback.data = dict(cid=[g1DampedOscilator]) #      /output
        glob_active.data   = dict(Active=[True])

def stop():
    [mass]    = glob_mass.data['m']    # input/output
    [spring]  = glob_spring.data['s']  # input/output
    [dashpot] = glob_dashpot.data['d'] # input/output
    pause()
    glob_t.data=dict(t=[0])                     #      /output
    glob_s.data=dict(s=[0])                     #      /output
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
    
def reset():
    stop()
    [mass] = glob_mass.data['m'] # input/output
    mass_input.value = initial_mass_value
    kappa_input.value = initial_kappa_value
    lam_input.value = initial_lambda_value
    initV_input.value = initial_velocity_value
    mass.changeInitV(initial_velocity_value)

    #this could reset also the plot, but needs the selenium package:
    #reset_button = selenium.find_element_by_class_name('bk-tool-icon-reset')
    #click_element_at_position(selenium, reset_button, 10, 10)

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
    row(mass_input,Spacer(width=10),kappa_input),row(lam_input,Spacer(width=10),initV_input)))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
