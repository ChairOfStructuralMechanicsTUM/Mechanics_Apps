import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.io import curdoc
from Functions import *
from bokeh.models import Arrow, OpenHead, Button
from bokeh.layouts import column, row
from os.path import dirname, join, split

'''
###############################################################################
Create the plotting domain (the low pressure area!)
###############################################################################
'''
xmin, xmax = -1200,1200
ymin, ymax = -1200,1200
plot = figure(
              plot_width=800,
              plot_height=800,
              x_range=[xmin,xmax], 
              y_range=[ymin,ymax],
              tools="",
              title = 'Tiefdruckgebiet (Low-pressure area)',
             )
plot.title.text_font_size = "25px"
plot.title.align = "center"
plot.grid.visible=False
plot.xaxis.visible=False
plot.yaxis.visible=False

Active = True

'''
###############################################################################
Define the objects to be plotted within the plotting domain
 (1) Pressure contour lines
 (2) Travelling particle
 (3) Forces and velocity arrows
###############################################################################
'''
######################## (1) Pressure contour lines ###########################
earthRotation = 1
N = 40                              # Number of points defining pressure field
x = np.linspace(xmin, xmax, N)           
y = np.linspace(ymin, ymax, N)
X, Y = np.meshgrid(x, y)            # Create a grid for the pressure plot
pressure = np.sqrt((20/980*X)**2 + (20/980*Y)**2)+980            # Define the function that determines the
                                    # pressure field
                                    
# Create the grid of pressure gradient
presGrad = [0]*N
presGradX =  10000*X*(20/980)**2 / np.sqrt((20/980*X)**2 + (20/980*Y)**2)
presGradY = 10000*Y*(20/980)**2 / np.sqrt((20/980*X)**2 + (20/980*Y)**2)
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
dt = 0.1
particleRadius = 50
particleMass   = 20
update_particle_position(x=0.0,y=1.0)         # Initial particle's position
velocity = np.array([0,0])                   # Initial particle's velocity

position = get_particle_position()
print('position = [',position[0],',',position[1],']')
update_particle_source(position[0],position[1])

plot.circle(
            x = 'x',
            y = 'y',
            radius = particleRadius,
            color = '#33FF33',
            source = get_particle_source()
           )
traceSource = ColumnDataSource(data = dict(x=[],y=[]) )
plot.ellipse(
             x='x',y='y',width=0.5,height=0.5,
             color="#0065BD",
             source=traceSource
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
angularVelocity = earthRotation * np.array([ 0,0,0.2 ])
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
###############################################################################
Define the function that will develope the position of the particle through
time
###############################################################################
'''
rKlein = 200.0
rGross = 1000.0
lamda  = 0.02
omega  = 1.0
phi0   = -np.pi/2
paramDouble1 = -1.5708

def compute_tranjectory():
    global velocity, position, coriolisForce, currentPressGrad
    
    particleSource = get_particle_source()
    position = get_particle_position()
    
    theta = np.arccos(position[0]/np.sqrt(position[0]**2 + position[1]**2))
    XStart = position[0]
    YStart = position[1]

    if XStart >= 0 and YStart >= 0:
        #print('Q1')
        pass
    elif XStart <= 0 and YStart >= 0:
        #print('Q2')
        theta += 2*(np.pi/2 - theta)
    elif XStart <= 0 and YStart <= 0:
        #print('Q3')
        theta -= np.pi
    else:
        #print('Q4')
        theta *= -1
    paramDouble1 = theta
    print('theta = ',theta)

    d5 = rKlein + (rGross-rKlein)*np.exp(-4.0*lamda*paramDouble1)
    #print('d5 = ', d5)
    d6 = phi0 + omega*(paramDouble1 + 1.0/lamda*(np.exp(-lamda*paramDouble1) - 1.0))
    #print('d6 = ',d6)
    d7 = -(rGross-rKlein) * 4.0 * lamda * np.exp(-4.0 * lamda * paramDouble1)
    d8 = omega * (1.0 - np.exp(-lamda*paramDouble1))
    
    d1 = np.sqrt(d7*d7 + d8*d5*d8*d5)
    d2 = np.arccos(d8*d5/d1)
    d4 = 200.0 * np.exp(-d5*d5 / 600.0 / 600.0) * 2.0 * d5 / 600.0
    d10 = -np.sin(d2-paramDouble1)*d4
    d11 = -np.cos(d2-paramDouble1)*d4
    
    d12 = d7*np.sin(d6) + d5*d8*np.cos(d6) 

    #coriolisForce = np.array([
    #                          coriolisForce[0],
    #                          coriolisForce[1]
    #                        ])
    coriolisForce = np.array([
                              1.5*d12,
                              0.0
                             ])
    
#    currentPressGrad = get_pressure_grad(
#                                         [particleSource.data['x'][0],
#                                          particleSource.data['y'][0]],
#                                         X, Y,
#                                         presGrad
#                                        )
    currentPressGrad = np.array([ 1.5*d10, 1.5*d11 ])
#    acceleration = ( coriolisForce + currentPressGrad ) / particleMass
#    velocity = velocity + acceleration*dt
#    position = np.array([particleSource.data['x'][0],particleSource.data['y'][0]]) + velocity*dt
    position[0] = d5*np.cos(d6) 
    position[1] = d5*np.sin(d6) 
    #print("position = [",position[0],",",position[1],"]")

    # Safety checks to prevent the particle from getting outside the domain
    if position[0] > xmax :
        position[0] -= xmax/50
        velocity[0]  *= -1
    elif position[0] < xmin:
        position[0] += xmax/50
        velocity[0]  *= -1
    elif position[1] > ymax :
        position[1] -= ymax/50
        velocity[1]  *= -1
    elif position[1] < ymin:
        position[1] += ymax/50
        velocity[1]  *= -1

    traceSource.stream( 
                          dict(
                               x = [position[0]],
                               y = [position[1]]
                              )
                      )
    if len(traceSource.data['x']) == 100:
        traceSource.data = dict(
                                x=traceSource.data['x'][1:100],
                                y=traceSource.data['y'][1:100]
                               )
                
    update_particle_source(position[0],position[1])
    update_particle_position( x=position[0] , y=position[1] )
    
    particleSource = get_particle_source()
   # coriolisForce = -2*particleMass*np.cross(
   #                                          angularVelocity, 
   #                                          np.array([ velocity[0],velocity[1],0 ])
    #                                        )
    #coriolisForce = np.array([ particleSource.data['x'][0], 0 ])

    velocityArrowSource.data = update_arrow_source( particleSource, velocity )
    
    coriolisForceArrowSource.data = update_arrow_source( 
                                                        particleSource, 
                                                        coriolisForce
                                                       )
    
    presGradArrowSource.data = update_arrow_source( 
                                                   particleSource,
                                                   currentPressGrad
                                                  )
    
'''
###############################################################################
Add the interactive functionalities
###############################################################################
'''
#################### Moving the ball through the mouse ########################
plot.add_tools(MoveNodeTool())

def on_mouse_move(attr, old, new):

    if (modify_location(attr,old,new)==1):
        # if the path is changed then update the drawing
        pass

plot.tool_events.on_change('geometries', on_mouse_move)

########################### Creating pause button #############################
def pause ():
    global Active
    # When active pause animation
    if Active == True:
        curdoc().remove_periodic_callback(compute_tranjectory)
        Active=False
    else:
        pass
        
pause_button = Button(label="Pause", button_type="success")
pause_button.on_click(pause)
########################### Creating play button ##############################
def play ():
    global Active, periodicCallback
    
    if Active == False:
        curdoc().add_periodic_callback(compute_tranjectory, 50)
        Active=True
        periodicCallback = 0
    else:
        pass
        
play_button = Button(label="Play", button_type="success")
play_button.on_click(play)
########################### Creating reset button #############################
periodicCallback = 0
def Reset():
    global velocity, Active, periodicCallback
    
    #jumpingSource.data = dict(x=[],y=[]) 
    
    position = np.array([ 0,-1 ])
    velocity = np.array([ 0,0  ])

    update_particle_source(position[0],position[1])
    update_particle_position( x=position[0] , y=position[1] )
    
    velocityArrowSource.data = update_arrow_source( particleSource, velocity )
    
    coriolisForce = np.array([ particleSource.data['x'][0], 0 ])
    coriolisForceArrowSource.data = update_arrow_source( 
                                                        particleSource,
                                                        0.1*coriolisForce 
                                                       )
    
    currentPressGrad = get_pressure_grad(
                                         [particleSource.data['x'][0],
                                          particleSource.data['y'][0]],
                                         X, 
                                         Y,
                                         presGrad
                                        )
    presGradArrowSource.data = update_arrow_source( 
                                                   particleSource, 
                                                   0.1*currentPressGrad
                                                  )

    # The preiodic callback has been removed here because when the pause 
    # button is set to False, this reactivates the periodic callback
    if periodicCallback == 0 and Active == True:
        curdoc().remove_periodic_callback(compute_tranjectory)
        periodicCallback += 1

    else:
        pass
    
    Active = False
        
reset_button = Button(label="Reset", button_type="success")
reset_button.on_click(Reset)
    
'''
###############################################################################
Add all the components together and initiate the app
###############################################################################
'''
curdoc().add_periodic_callback(compute_tranjectory,500)
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
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '