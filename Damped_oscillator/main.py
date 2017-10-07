from Spring import *
from Dashpot import *
from Mass import *
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import Slider, Button, Div, HoverTool, Range1d, Div
from os.path import dirname, join, split

# z = lam/(2*sqrt(k*m))
# z = 1 => crit damped
# z > 1 => over damped
# z < 1 => under damped

## initial values
initial_mass_value = 8
initial_kappa_value = 50
initial_lambda_value = 2
initial_velocity_value = -5
s=0
t=0
dt=0.03

mass_center_x = 0
mass_center_y = 15
mass_width    = 2
mass_height   = 2
mass = CircularMass(
                    initial_mass_value,
                    mass_center_x,
                    mass_center_y,
                    mass_width,
                    mass_height
                   )
mass.changeInitV(initial_velocity_value)

spring_start_coord = (mass_center_x-mass_width , 0)
spring_end_coord   = (mass_center_x-mass_width , mass_center_y-mass_height)
spring_length      = 11
spring = Spring(
                spring_start_coord,
                spring_end_coord,
                spring_length,
                initial_kappa_value
               )
mass.linkObj(spring,(mass_center_x-mass_width , mass_center_y-mass_height))

dashpot_start_coord = (mass_center_x+mass_width , 0)
dashpot_end_coord   = (mass_center_x+mass_width , mass_center_y-mass_height)
dashpot = Dashpot(
                  dashpot_start_coord,
                  dashpot_end_coord,
                  initial_lambda_value
                 )
mass.linkObj(dashpot,(mass_center_x+mass_width , mass_center_y-mass_height))

Bottom_Line = ColumnDataSource(
                               data = dict(
                                           x=[mass_center_x-mass_width , mass_center_x+mass_width],
                                           y=[spring_end_coord[1] , spring_end_coord[1]]
                                          )
                              )

Linking_Line = ColumnDataSource(
                                data = dict(
                                            x=[mass_center_x , mass_center_x],
                                            y=[spring_end_coord[1] , spring_end_coord[1]+2]
                                           )
                               )

Position = ColumnDataSource(data = dict(t=[0],s=[0]))

initial_velocity_value=-5.0
Active=False

def evolve():
    global mass, Bottom_Line, Linking_Line, t, s, y_range_plot, x_range_plot
    mass.FreezeForces()
    disp=mass.evolve(dt)
    s+=disp.y
    Bottom_Line.data=dict(
                          x=[mass_center_x-mass_width , mass_center_x+mass_width],
                          y=[spring_end_coord[1]+s , spring_end_coord[1]+s]
                         )
    Linking_Line.data=dict(
                           x=[mass_center_x , mass_center_x],
                           y=[spring_end_coord[1]+s , spring_end_coord[1]+2+s]
                          )
    t+=dt
    Position.stream(dict(t=[t],s=[s]))
    
    # Change boundaries of displacement-time plot if exceeded
    if abs(s) > abs(y_range_plot.start):
        y_range_plot.start = -abs(s)*1.1 
        y_range_plot.end =  abs(s)*1.1  # multiplied by 1.1 for having an adsmall margin
        
    if t > x_range_plot.end:
        x_range_plot.end = t*2

title_box = Div(text="""<h2 style="text-align:center;">Spring pendulum</h2>""",width=1000)

# drawing
fig = figure(title="", tools="", x_range=(-7,7), y_range=(-5,20),width=350,height=500)
fig.title.text_font_size="20pt"
fig.axis.visible = True
fig.grid.visible = False
fig.outline_line_color = None
spring.plot(fig,width=2)
dashpot.plot(fig,width=2)

# Define the ground base for both the spring and the dashpot
fig.line(
         x=[mass_center_x-mass_width , mass_center_x+mass_width],
         y=[spring_start_coord[1] , spring_start_coord[1]],
         color="black",line_width=3
        )
fig.line(
         x=[mass_center_x , mass_center_x],
         y=[spring_start_coord[1]-1 , spring_start_coord[1]],
         color="black",line_width=3
        )
fig.line(
         x=[mass_center_x-mass_width , mass_center_x+mass_width],
         y=[spring_start_coord[1]-1 , spring_start_coord[1]-1],
         color="black",line_width=3
        )
fig.multi_line(
               xs=[
                   [mass_center_x-2 , mass_center_x-2-0.75],
                   [mass_center_x-1 , mass_center_x-1-0.75],
                   [mass_center_x-0 , mass_center_x-0-0.75],
                   [mass_center_x+1 , mass_center_x+1-0.75],
                   [mass_center_x+2 , mass_center_x+2-0.75]
                  ],
               ys=[
                   [spring_start_coord[1]-1 , spring_start_coord[1]-1-0.75],
                   [spring_start_coord[1]-1 , spring_start_coord[1]-1-0.75],
                   [spring_start_coord[1]-1 , spring_start_coord[1]-1-0.75],
                   [spring_start_coord[1]-1 , spring_start_coord[1]-1-0.75],
                   [spring_start_coord[1]-1 , spring_start_coord[1]-1-0.75]
                  ],
               color="black",
               line_width=3
              )


fig.line(x='x',y='y',source=Bottom_Line,color="black",line_width=3)
fig.line(x='x',y='y',source=Linking_Line,color="black",line_width=3)
mass.plot(fig)

# plot
x_range_plot = Range1d(0,10)
y_range_plot = Range1d(-5,5)
hover = HoverTool(tooltips=[("time","@t s"), ("displacement","@s m")])
p = figure(
           title="",
           y_range = y_range_plot, 
           x_range = x_range_plot, 
           height=500, \
           toolbar_location="right", 
           tools=[hover,"ywheel_zoom,xwheel_pan,pan,reset"]
          ) #ywheel_zoom,xwheel_pan,reset,
p.line(x='t',y='s',source=Position,color="black")
p.axis.major_label_text_font_size="12pt"
p.axis.axis_label_text_font_style="normal"
p.axis.axis_label_text_font_size="14pt"
p.xaxis.axis_label="Time [s]"
p.yaxis.axis_label="Displacement [m]"

def change_mass(attr,old,new):
    global mass
    mass.changeMass(new)

## Create slider to choose mass of blob
mass_input = Slider(title="Mass [kg]", value=initial_mass_value, start=0.5, end=10.0, step=0.5, width=400)
mass_input.on_change('value',change_mass)

def change_kappa(attr,old,new):
    global spring
    spring.changeSpringConst(new)

## Create slider to choose spring constant
kappa_input = Slider(title="Spring stiffness [N/m]", value=initial_kappa_value, start=0.0, end=200, step=10,width=400)
kappa_input.on_change('value',change_kappa)

def change_lam(attr,old,new):
    global dashpot
    dashpot.changeDamperCoeff(new)

## Create slider to choose damper coefficient
lam_input = Slider(title="Damping coefficient [Ns/m]", value=initial_lambda_value, start=0.0, end=10, step=0.1,width=400)
lam_input.on_change('value',change_lam)

def change_initV(attr,old,new):
    global mass, Active, initial_velocity_value, initV_input
    if (not Active):
        mass.changeInitV(new)

## Create slider to choose damper coefficient
initV_input = Slider(title="Initial velocity [m/s]", value=initial_velocity_value, start=-10.0, end=10.0, step=0.5,width=400)
initV_input.on_change('value',change_initV)

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

#def stop():
#    global Position, t, s, Bottom_Line, Linking_Line, spring, mass, dashpot
#    pause()
#    t=0
#    s=0
#    Position.data=dict(t=[0],s=[0])
#    Bottom_Line.data = dict(
#                               x=[mass_center_x-mass_width , mass_center_x+mass_width],
#                               y=[spring_end_coord[1] , spring_end_coord[1]]
#                           )
#
#    Linking_Line.data = dict(
#                                x=[mass_center_x , mass_center_x],
#                                y=[spring_end_coord[1] , spring_end_coord[1]+2]
#                            )
#    
#    spring.compressTo(
#                      Coord(spring_start_coord[0] , spring_start_coord[1]),
#                      Coord(spring_end_coord[0] , spring_end_coord[0])
#                     )
#    
#    dashpot.compressTo(
#                       Coord(d,18),
#                       Coord(2,11)
#                      )
#    mass.moveTo((mass_center_x , mass_center_y))
#    mass.resetLinks(spring,(-2,11))
#    mass.resetLinks(dashpot,(2,11))
#    mass.changeInitV(initV_input.value)

def reset():
    global Position, t, s, Bottom_Line, Linking_Line, spring, mass, dashpot
    
    mass_input.value = initial_mass_value
    kappa_input.value = initial_kappa_value
    lam_input.value = initial_lambda_value
    initV_input.value = initial_velocity_value
    mass.changeInitV(initV_input.value)
    pause()
    t=0
    s=0
    Position.data=dict(t=[0],s=[0])
    Bottom_Line.data = dict(
                               x=[mass_center_x-mass_width , mass_center_x+mass_width],
                               y=[spring_end_coord[1] , spring_end_coord[1]]
                           )

    Linking_Line.data = dict(
                                x=[mass_center_x , mass_center_x],
                                y=[spring_end_coord[1] , spring_end_coord[1]+2]
                            )
    
    spring.compressTo(
                      Coord(spring_start_coord[0] , spring_start_coord[1]),
                      Coord(spring_end_coord[0] , spring_end_coord[1])
                     )
    
    dashpot.compressTo(
                       Coord(dashpot_start_coord[0] , dashpot_start_coord[1]),
                       Coord(dashpot_end_coord[0] , dashpot_end_coord[1])
                      )
    mass.moveTo((mass_center_x , mass_center_y))
    
    mass.resetLinks(spring,(mass_center_x-mass_width , mass_center_y-mass_height))
    mass.resetLinks(dashpot,(mass_center_x+mass_width , mass_center_y-mass_height))

    #this could reset also the plot, but needs the selenium package:
    #reset_button = selenium.find_element_by_class_name('bk-tool-icon-reset')
    #click_element_at_position(selenium, reset_button, 10, 10)

play_button = Button(label="Play", button_type="success",width=100)
play_button.on_click(play)
pause_button = Button(label="Pause", button_type="success",width=100)
pause_button.on_click(pause)
#stop_button = Button(label="Stop", button_type="success", width=100)
#stop_button.on_click(stop)
reset_button = Button(label="Reset", button_type="success",width=100)
reset_button.on_click(reset)

# add app description
description_filename = join(dirname(__file__), "description.html")
description = Div(text=open(description_filename).read(), render_as_text=False, width=1200)

## Send to window
curdoc().add_root(column(description, \
    row(column(Spacer(height=100),play_button,pause_button,reset_button),Spacer(width=10),fig,p), \
    row(mass_input,kappa_input),row(lam_input,initV_input)))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
