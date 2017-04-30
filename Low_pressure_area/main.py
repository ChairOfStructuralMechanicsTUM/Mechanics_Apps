import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.io import curdoc
from Functions import *
from bokeh.models import Arrow, OpenHead, Button, Toggle, Slider
from bokeh.core.properties import Instance, List
from bokeh.layouts import column, row

Active = True

'''
Create the plotting domain (the low pressure area!)
'''
xmin, xmax = -1,1
ymin, ymax = -1,1
plot = figure(
                  plot_width=800,
                  plot_height=800,
                  x_range=[xmin,xmax], 
                  y_range=[ymin,ymax],
                  tools=""
             )

'''
Define the objects to be plotted within the plotting domain
 (1) Pressure contour lines
 (2) Travelling particle
 (3) Forces and velocity arrows
'''
######################## (1) Pressure contour lines ###########################
earthRotation = 1
N = 40                              # Number of points defining pressure field
x = np.linspace(-1, 1, N)           
y = np.linspace(-1, 1, N)
X, Y = np.meshgrid(x, y)            # Create a grid for the pressure plot
pressure = (X**2 + Y**2)            # Define the function that determines the
                                    # pressure field
                                    
# Create the grid of pressure gradient
presGrad = [0]*N
presGradX = 2*X
presGradY = 2*Y
for i in range(N):
    for j in range(N):
        if i == 0:
            presGrad[j] = [np.array([-presGradX[i,j] , -presGradY[i,j]])]
        else:
            presGrad[j].append(np.array([-presGradX[i,j] , -presGradY[i,j]]))
        
presGrad = np.array(presGrad)

# Define the source file for pressure contour lines plot
pressureContourSource = get_contour_data(X,Y,pressure)
plot.multi_line(
                    xs='xs',
                    ys='ys', 
                    line_color='line_color',
                    source=pressureContourSource
               )
plot.text(
              x='xt',
              y='yt',
              text='text',
              source=pressureContourSource,
              text_baseline='middle',
              text_align='center'
         )

######################## (2) Travelling particle ##############################
dt = 0.01
particleRadius = 0.1
particleMass   = 20
update_particle_position(x=0,y=-0.5)         # Initial particle's position
velocity = np.array([0,0])                   # Initial particle's velocity

position = get_particle_position()
update_particle_source(position[0],position[1])

plot.circle(
                x = 'x',
                y = 'y',
                radius = particleRadius,
                color = '#33FF33',
                source = get_particle_source()
           )

###################### (3) Forces and velocity arrows #########################
# Defining the velocity arrow
particleSource = get_particle_source()

velocityArrowSource = construct_arrow_source( particleSource, velocity )

plot.add_layout( 
                Arrow(    
                      end=OpenHead(
                                   line_color="yellow",
                                   line_width=3,
                                   size=10
                                  ),
                      x_start=['xs'][0],
                      y_start=['ys'][0],
                      x_end=['xe'][0], 
                      y_end=['ye'][0], 
                      line_color="yellow",
                      source = velocityArrowSource
                     ) 
                )

# Defining the pressure gradient force arrow                               
currentPressGrad = get_pressure_grad(
                                     get_particle_position(),
                                     X, 
                                     Y,
                                     presGrad
                                    )

presGradArrowSource = construct_arrow_source( 
                                             particleSource, 
                                             0.1*currentPressGrad 
                                            )
                                    
plot.add_layout( 
                Arrow(    
                      end=OpenHead(
                                   line_color="black",
                                   line_width=3,
                                   size=10
                                  ),
                      x_start=['xs'][0],
                      y_start=['ys'][0],
                      x_end=['xe'][0], 
                      y_end=['ye'][0], 
                      line_color="black",
                      source = presGradArrowSource
                     ) 
                )
         
# Defining the coriolis force arrow
angularVelocity = earthRotation * np.array([ 0,-1,0.2 ])
coriolisForce = -2 * particleMass * np.cross(
                                             angularVelocity, 
                                             np.array([ velocity[0], velocity[1], 0 ])
                                            )
coriolisForce = np.array([
                          coriolisForce[0],
                          coriolisForce[1]
                         ])

coriolisForceArrowSource = construct_arrow_source( 
                                                  particleSource,
                                                  coriolisForce 
                                                 )

plot.add_layout( 
                Arrow(    
                      end=OpenHead(
                                   line_color="red",
                                   line_width=3,
                                   size=10
                                  ),
                      x_start=['xs'][0],
                      y_start=['ys'][0],
                      x_end=['xe'][0], 
                      y_end=['ye'][0], 
                      line_color="red",
                      source = coriolisForceArrowSource
                     ) 
                )

'''
Define the function that will develope the position of the particle through
time
'''
def compute_tranjectory():
    global velocity, position, coriolisForce, currentPressGrad
    
    particleSource = get_particle_source()
    position = get_particle_position()
    
    coriolisForce = np.array([
                              coriolisForce[0],
                              coriolisForce[1]
                            ])
    
    currentPressGrad = get_pressure_grad(
                                         [particleSource.data['x'][0],
                                          particleSource.data['y'][0]],
                                         X, Y,
                                         presGrad
                                        )
    acceleration = ( coriolisForce + currentPressGrad ) / particleMass
    velocity = velocity + acceleration*dt
    position = np.array([particleSource.data['x'][0],particleSource.data['y'][0]]) + velocity*dt
                        
    update_particle_source(position[0],position[1])
    update_particle_position( x=position[0] , y=position[1] )
    
    particleSource = get_particle_source()
    #coriolisForce = -2*particleMass*np.cross(angularVelocity, np.array([velocity[0],velocity[1],0]))
    coriolisForce = np.array([ particleSource.data['x'][0], 0 ])

    velocityArrowSource.data = update_arrow_source( particleSource, velocity )
    
    coriolisForceArrowSource.data = update_arrow_source( particleSource, 0.1*coriolisForce )
    
    presGradArrowSource.data = update_arrow_source( particleSource, 0.1*currentPressGrad )
    
'''
Add the interactive functionalities
'''
#################### Moving the ball through the mouse ########################
plot.add_tools(MoveNodeTool())

def on_mouse_move(attr, old, new):

    if (modify_path(attr,old,new)==1):
        # if the path is changed then update the drawing
        pass

plot.tool_events.on_change('geometries', on_mouse_move)

########################### Creating pause button #############################
def pause (toggled):
    global Active

    if (toggled):
        curdoc().remove_periodic_callback(compute_tranjectory)
        Active=False

    else:
        curdoc().add_periodic_callback(compute_tranjectory, 10)
        Active=True
        
pause_button = Toggle(label="Pause", button_type="success")
pause_button.on_click(pause) 
########################### Creating play button ##############################
def play ():
    global Active
    # if inactive, reactivate animation
    if (pause_button.active):
        # deactivating pause button reactivates animation
        # (calling add_periodic_callback twice gives errors)
        pause_button.active=False
    elif Active == False:
        curdoc().add_periodic_callback(compute_tranjectory, 10)
        Active=True
        
play_button = Button(label="Play", button_type="success")
play_button.on_click(play)
########################### Creating reset button #############################
def Reset():
    global velocity
    
    position = np.array([ 0,-1 ])
    velocity = np.array([ 0,0  ])

    update_particle_source(position[0],position[1])
    update_particle_position( x=position[0] , y=position[1] )
    
    velocityArrowSource.data = update_arrow_source( particleSource, velocity )
    
    coriolisForce = np.array([ particleSource.data['x'][0], 0 ])
    coriolisForceArrowSource.data = update_arrow_source( particleSource, 0.1*coriolisForce )
    
    currentPressGrad = get_pressure_grad(
                                         [particleSource.data['x'][0],
                                          particleSource.data['y'][0]],
                                         X, 
                                         Y,
                                         presGrad
                                        )
    presGradArrowSource.data = update_arrow_source( particleSource, 0.1*currentPressGrad )

reset_button = Button(label="Reset", button_type="success")
reset_button.on_click(Reset)
    
'''
Add all the components together and initiate the app
'''
curdoc().add_periodic_callback(compute_tranjectory,10)
curdoc().add_root(
                  row(
                      plot,
                      column(
                             pause_button,
                             play_button,
                             reset_button
                            )
                     )
                 )