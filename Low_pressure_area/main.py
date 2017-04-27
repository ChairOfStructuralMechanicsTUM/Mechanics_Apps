import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.io import curdoc
from Functions import get_contour_data, get_pressure_grad
from bokeh.models import Arrow, OpenHead

'''
Create the plotting domain
'''
xmin, xmax = -1,1
ymin, ymax = -1,1
plot = figure(
                  plot_width=800,
                  plot_height=800,
                  x_range=[xmin,xmax], 
                  y_range=[ymin,ymax]
             )

'''
Define the objects to be plotted within the plotting domain
 (1) Pressure contour lines
 (2) Travelling particle
 (3) Forces and velocity arrows
'''
### (1) Pressure contour lines ###
earthRotation = 0.1
N = 40                              # Number of points defining pressure field
x = np.linspace(-1, 1, N)           
y = np.linspace(-1, 1, N)
X, Y = np.meshgrid(x, y)            # Create a grid for the pressure plot
pressure = 0.1*(X**2 + Y**2)         # Define the function that determines the
                                    # pressure distribution
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

# Define the source file for pressure contour lines
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

### (2) Travelling particle ###
dt = 0.01
particleRadius = 0.05
particleMass   = 5
position = np.array([ (xmax+xmin)/2,-1 ]) # Initial particle's position
velocity = np.zeros(2)                    # Initial particle's velocity
paticleSource = ColumnDataSource(
                                       data=dict(
                                                     x = [position[0]],
                                                     y = [position[1]],
                                                )
                                  )
plot.circle(
                x = 'x',
                y = 'y',
                radius = particleRadius,
                color = '#33FF33',
                source = paticleSource
           )

### (3) Forces and velocity arrows ###
# Defining the velocity arrow
velocityArrowTailPosition = np.array([ 
                                      paticleSource.data['x'][0],
                                      paticleSource.data['y'][0]
                                    ])
velocityArrowHeadPosition = np.array([
                                      paticleSource.data['x'][0]+velocity[0],
                                      paticleSource.data['y'][0]+velocity[1]
                                    ])
velocityArrowSource = ColumnDataSource(
                                       data=dict(
                                                 xs=[velocityArrowTailPosition[0]],
                                                 ys=[velocityArrowTailPosition[1]],
                                                 xe=[velocityArrowHeadPosition[0]],
                                                 ye=[velocityArrowHeadPosition[1]]
                                                )
                                      ) 
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
presGradArrowTail = np.array([ 
                              paticleSource.data['x'][0],
                              paticleSource.data['y'][0]
                            ])
currentPressGrad = get_pressure_grad(
                                     [paticleSource.data['x'][0],
                                      paticleSource.data['y'][0]],
                                     X, Y,
                                     presGrad
                                    )

presGradArrowHead = np.array([
                              paticleSource.data['x'][0]+0.1*currentPressGrad[0],
                              paticleSource.data['y'][0]+0.1*currentPressGrad[1]
                            ])
presGradArrowSource = ColumnDataSource(
                                       data=dict(
                                                 xs=[presGradArrowTail[0]],
                                                 ys=[presGradArrowTail[1]],
                                                 xe=[presGradArrowHead[0]],
                                                 ye=[presGradArrowHead[1]]
                                                ) 
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
'''
rotationRadius = np.array([ paticleSource.data['x'][0], paticleSource.data['x'][0] ])
rotationRadiusMag = np.sqrt( np.dot(rotationRadius,rotationRadius) )
if rotationRadiusMag == 0:
    radialNormal = np.array([0.2,0])
else:
    radialNormal = rotationRadius / rotationRadiusMag
radialVelocity = np.dot(velocity,radialNormal)
tangentialVelocity = velocity - radialVelocity
tangentialVelocityMag = np.sqrt( np.dot(tangentialVelocity,tangentialVelocity) )
if rotationRadiusMag == 0:
    angularVelocityMag = 0
else:
    angularVelocityMag = tangentialVelocityMag / rotationRadiusMag
rotationNormal = np.array([ 0,0,1 ])  # In Z-axis direction
print('angularVelocityMag = ',angularVelocityMag)
'''
angularVelocity = earthRotation * np.array([ 0,0,1 ])
coriolisForce = -2*particleMass*np.cross(angularVelocity, np.array([velocity[0],velocity[1],0]))
coriolisForce = np.array([
                          coriolisForce[0],
                          coriolisForce[1]
                         ])

coriolisArrowTailPosition = np.array([ 
                                      paticleSource.data['x'][0],
                                      paticleSource.data['y'][0]
                                    ])
coriolisArrowHeadPosition = np.array([
                                      paticleSource.data['x'][0]+coriolisForce[0],
                                      paticleSource.data['y'][0]+coriolisForce[1]
                                    ])

coriolisForceArrowSource = ColumnDataSource(
                                           data=dict(
                                                     xs=[coriolisArrowTailPosition[0]],
                                                     ys=[coriolisArrowTailPosition[1]],
                                                     xe=[coriolisArrowHeadPosition[0]],
                                                     ye=[coriolisArrowHeadPosition[1]]
                                                    ) 
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

def compute_tranjectory():
    global velocity, position, coriolisForce, currentPressGrad
    acceleration = ( coriolisForce + currentPressGrad ) / particleMass
    velocity = velocity + acceleration*dt
    position = position + velocity*dt
    paticleSource.data = dict(
                              x = [position[0]],
                              y = [position[1]]
                             )
    coriolisForce = -2*particleMass*np.cross(angularVelocity, np.array([velocity[0],velocity[1],0]))
    coriolisForce = np.array([
                          coriolisForce[0],
                          coriolisForce[1]
                         ])

    currentPressGrad = get_pressure_grad(
                                     [paticleSource.data['x'][0],
                                      paticleSource.data['y'][0]],
                                     X, Y,
                                     presGrad
                                    )
    
    
    
curdoc().add_periodic_callback(compute_tranjectory,10)
curdoc().add_root(plot)