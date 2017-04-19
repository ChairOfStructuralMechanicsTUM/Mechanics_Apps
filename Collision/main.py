import numpy as np
from bokeh.io import curdoc
from bokeh.plotting import Figure, ColumnDataSource
import BarChart as BC
from bokeh.layouts import column, row
from bokeh.models import Button, Toggle, Slider
from bokeh.models import Arrow, OpenHead


# Define the figure (which corresponds to the play ground)
xMin, xMax = 0, 10
yMin, yMax = 0, 10

playGround = Figure(
                        plot_width = 600,
                        plot_height= 800,
                        x_range  =(xMin, xMax),
                        y_range  =(yMin, yMax),
                        title = 'Collision play ground'
                   )
playGround.grid.visible = False
playGround.xaxis.axis_label = 'X'
playGround.yaxis.axis_label = 'Y'

# Define the energy bar
eFig = BC.BarChart(
                       ["Green ball's kinetic energy",
                       "Red ball's kinetic energy",
                       "Total system's kinetic energy"],
                       [50,50,50],
                       ["#98C6EA","#A2AD00","#E37222"],
                       [1,1,1]
                  )
eFig.Width(300)
eFig.Height(650)
eFig.fig.yaxis.visible=False

# Define the initial location of the two colliding balls (in our 2D app, circles)
x1,x2 = 3,5
y1,y2 = 2,2
r1,r2 = 0.5,0.5
m1,m2 = 3,1
c1,c2 = '#33FF33','#FF3333'
#v1x,v1y,v2x,v2y = 1,-2,0,0
velocityVectorOne = np.array([1,0])
velocityVectorTwo = np.array([0,0])

circleOneSource = ColumnDataSource(
                                       data=dict(
                                                     m = np.array([m1]),
                                                     x = np.array([x1]),
                                                     y = np.array([y1]),
                                                     r = np.array([r1]),
                                                     c = np.array([c1]),
                                                     vx = np.array([velocityVectorOne[0]]),
                                                     vy = np.array([velocityVectorOne[1]])
                                                )
                                  )
circleTwoSource = ColumnDataSource(
                                       data=dict(
                                                     m = np.array([m2]),
                                                     x = np.array([x2]),
                                                     y = np.array([y2]),
                                                     r = np.array([r2]),
                                                     c = np.array([c2]),
                                                     vx = np.array([velocityVectorTwo[0]]),
                                                     vy = np.array([velocityVectorTwo[1]])
                                                )
                                  )
    
playGround.circle( x='x',y='y',radius='r',color='c',source=circleOneSource )
playGround.circle( x='x',y='y',radius='r',color='c',source=circleTwoSource )


sourceArrowOne = ColumnDataSource(
                                      data=dict(
                                                    xs=[circleOneSource.data['x'][0]],
                                                    ys=[circleOneSource.data['y'][0]],
                                                    xe=[circleOneSource.data['x'][0]+velocityVectorOne[0]],
                                                    ye=[circleOneSource.data['y'][0]+velocityVectorOne[1]]
                                               )
                                 ) 
sourceArrowTwo = ColumnDataSource(
                                      data=dict(
                                                    xs=[circleTwoSource.data['x'][0]],
                                                    ys=[circleTwoSource.data['y'][0]],
                                                    xe=[circleTwoSource.data['x'][0]+velocityVectorTwo[0]],
                                                    ye=[circleTwoSource.data['y'][0]+velocityVectorTwo[1]]
                                               )
                                 ) 

# Define the dynamic simulation parameters
dt = 0.01
tolerance = 0.1
velocityTolerance = 0.05

Active = True

# Collusion Parameters
Cr = 1.0

def compute_tranjectory():
    global velocityVectorOne, velocityVectorTwo
    # Compute the new position of the circles' center
    circleOneSource.data['x'] = ( circleOneSource.data['vx']*dt 
                                + circleOneSource.data['x']    )
    circleOneSource.data['y'] = ( circleOneSource.data['vy']*dt
                                + circleOneSource.data['y']    )
    
    circleTwoSource.data['x'] = ( circleTwoSource.data['vx']*dt 
                                + circleTwoSource.data['x']    )
    circleTwoSource.data['y'] = ( circleTwoSource.data['vy']*dt
                                + circleTwoSource.data['y']    )

    dx = circleOneSource.data['x'][0] - circleTwoSource.data['x'][0]
    dy = circleOneSource.data['y'][0] - circleTwoSource.data['y'][0]
    distance = np.sqrt( dx*dx + dy*dy )
    
    # Detect Walls
    if (   abs( circleOneSource.data['x'] + circleOneSource.data['r'] - xMax ) <= tolerance
        or abs( circleOneSource.data['x'] - circleOneSource.data['r'] - xMin ) <= tolerance):
        
        circleOneSource.data['vx'] *= -1
        
        if distance - abs(circleOneSource.data['r']  + circleTwoSource.data['r'] ) < tolerance:
            print('firstTogether')
            circleTwoSource.data['vx'] *= -1

    elif (   abs( circleTwoSource.data['x'] + circleTwoSource.data['r'] - xMax ) <= tolerance
          or abs( circleTwoSource.data['x'] - circleTwoSource.data['r'] - xMin ) <= tolerance):
        
        circleTwoSource.data['vx'] *= -1

        if distance - abs(circleOneSource.data['r']  + circleTwoSource.data['r'] ) < tolerance:
            circleOneSource.data['vx'] *= -1
    
    
    if (   abs( circleOneSource.data['y'] + circleOneSource.data['r'] - yMax ) <= tolerance 
        or abs( circleOneSource.data['y'] - circleOneSource.data['r'] - yMin ) <= tolerance):
        
        circleOneSource.data['vy'] *= -1

        if distance - abs(circleOneSource.data['r']  + circleTwoSource.data['r'] )  < tolerance:
            circleTwoSource.data['vy'] *= -1

    elif (   abs( circleTwoSource.data['y'] + circleTwoSource.data['r'] - yMax ) <= tolerance 
          or abs( circleTwoSource.data['y'] - circleTwoSource.data['r'] - yMin ) <= tolerance):
        
        circleTwoSource.data['vy'] *= -1

        if distance - abs(circleOneSource.data['r']  + circleTwoSource.data['r'] )  < tolerance:
            circleOneSource.data['vy'] *= -1

    # Detect each other
    # Calculate the distance between each others' centers
    dx = circleOneSource.data['x'][0]-circleTwoSource.data['x'][0]
    dy = circleOneSource.data['y'][0]-circleTwoSource.data['y'][0]
    distance = np.sqrt( dx*dx + dy*dy )

    # Unit vector aiming from ball 2 to ball 1
    normal2Vector = np.array( [-dx,-dy] )/distance

    # Determine the absolute speed of both balls
    v1Before = np.array( [circleOneSource.data['vx'][0],circleOneSource.data['vy'][0]] )
    v2Before = np.array( [circleTwoSource.data['vx'][0],circleTwoSource.data['vy'][0]] )
    
    # Determine the normal component of each ball's velocity (w.r.t previously 
    # computer normal vector)
    v1Normal = np.dot(v1Before,normal2Vector)
    v2Normal = np.dot(v2Before,normal2Vector)
    
    # Determine the tangential component of each ball's velocity
    v1TangentVector = v1Before - v1Normal*normal2Vector
    v2TangentVector = v2Before - v2Normal*normal2Vector

    # This if statement is excuted whenever the distance between the two balls 
    # is close "enough"
    seperation = abs(circleOneSource.data['r'][0]+circleTwoSource.data['r'][0])
    #print('abs(v1Normal+v2Normal) = ',abs(v1Normal+v2Normal))
    if (abs(distance - seperation) <= 0.1 and abs(v1Normal-v2Normal) >= 0.1):
        print('entered')

        m1 = circleOneSource.data['m']
        m2 = circleTwoSource.data['m']
        
        # Calculate the new normal velocity component of each ball according to
        # the law of collision
        v1NormalAfter = (Cr*m2*(v2Normal-v1Normal) + m1*v1Normal + m2*v2Normal)/(m1 + m2)
        v2NormalAfter = (Cr*m1*(v1Normal-v2Normal) + m1*v1Normal + m2*v2Normal)/(m1 + m2)
        
        # Updating the normal velocity of each ball
        v1Normal = v1NormalAfter
        v2Normal = v2NormalAfter
        
        # Getting the vector form of the normal velcoity after collision
        v1NormalVector = v1Normal*normal2Vector
        v2NormalVector = v2Normal*normal2Vector
        
        # Since the tangential velocity is maintained, it will be added to the 
        # new normal component to form the complete velocity vector after 
        # the collision
        v1After = v1NormalVector + v1TangentVector
        v2After = v2NormalVector + v2TangentVector
        
        # Update the source data file of both balls
        circleOneSource.data['vx'] = [v1After[0]] + 0*circleOneSource.data['vx']
        circleOneSource.data['vy'] = [v1After[1]] + 0*circleOneSource.data['vy']
        circleTwoSource.data['vx'] = [v2After[0]] + 0*circleTwoSource.data['vx']
        circleTwoSource.data['vy'] = [v2After[1]] + 0*circleTwoSource.data['vy']

        # Update velocity vectors
        velocityVectorOne = np.array(v1After)
        velocityVectorTwo = np.array(v2After)

    else:
        # Update velocity vectors
        velocityVectorOne = np.array(v1Before)
        velocityVectorTwo = np.array(v2Before)
    
    # Update the kinetic energies plotted by each bar according to the new ones 
    # calculated previously
    update_bars()
    updata_velocity_vectors()
    
def updata_velocity_vectors():
    
    sourceArrowOne.data=dict(
                                 xs=[circleOneSource.data['x'][0]],
                                 ys=[circleOneSource.data['y'][0]],
                                 xe=[circleOneSource.data['x'][0]+velocityVectorOne[0]],
                                 ye=[circleOneSource.data['y'][0]+velocityVectorOne[1]]
                            )
    
    sourceArrowTwo.data=dict(
                                 xs=[circleTwoSource.data['x'][0]],
                                 ys=[circleTwoSource.data['y'][0]],
                                 xe=[circleTwoSource.data['x'][0]+velocityVectorTwo[0]],
                                 ye=[circleTwoSource.data['y'][0]+velocityVectorTwo[1]]
                            )
def update_bars ():
    # Determine the new kinetic of both balls
    yellowBallKE = 0.5*circleOneSource.data['m'][0]*( circleOneSource.data['vx'][0]**2
                                                    + circleOneSource.data['vy'][0]**2)
    print('yellowBallKE = ',yellowBallKE)
    redBallKE = 0.5*circleTwoSource.data['m'][0]*( circleTwoSource.data['vx'][0]**2
                                                 + circleTwoSource.data['vy'][0]**2)
    print('redBallKE = ',redBallKE)
    
    totalKE = yellowBallKE + redBallKE
    
    # Update the bar heights accordingly
    eFig.setHeight(0,yellowBallKE)
    eFig.setHeight(1,redBallKE)
    eFig.setHeight(2,totalKE)
    
# Creating reset button
def Reset():
    global x1, x2, y1, y2

    # Update the source data file to the very initial data
    circleOneSource.data['x'] = [x1] + 0 *circleOneSource.data['x']
    circleTwoSource.data['x'] = [x2] + 0 *circleTwoSource.data['x']
    circleOneSource.data['y'] = [y1] + 0 *circleOneSource.data['y']
    circleTwoSource.data['y'] = [y2] + 0 *circleTwoSource.data['y']
    circleOneSource.data['vx'] = [1] + 0 *circleOneSource.data['vx']
    circleOneSource.data['vy'] = [1] + 0 *circleOneSource.data['vy']
    circleTwoSource.data['vx'] = [0] + 0 *circleTwoSource.data['vx']
    circleTwoSource.data['vy'] = [0] + 0 *circleTwoSource.data['vy']
    
    # Update the height of the bars accordingly
    update_bars()
    
reset_button = Button(label="Reset", button_type="success")
reset_button.on_click(Reset)

# Creating pause button
def pause (toggled):
    global Active
    # When active pause animation
    if (toggled):
        curdoc().remove_periodic_callback(compute_tranjectory)
        Active=False
    else:
        curdoc().add_periodic_callback(compute_tranjectory, 10)
        Active=True
        
pause_button = Toggle(label="Pause", button_type="success")
pause_button.on_click(pause)

# Creating play button
def play ():
    global Active
    # if inactive, reactivate animation
    if (pause_button.active):
        # deactivating pause button reactivates animation
        # (calling add_periodic_callback twice gives errors)
        pause_button.active=False
    elif (not Active):
        curdoc().add_periodic_callback(compute_tranjectory, 10)
        Active=True
        
play_button = Button(label="Play", button_type="success")
play_button.on_click(play)

def update_ballOne_x_position(attr,old,new):
    global Active
    
    if Active == False:
        circleOneSource.data['x'] = [new] + 0 *circleOneSource.data['x']
    else:
        pass
def update_ballOne_y_position(attr,old,new):
    global Active
    
    if Active == False:
        circleOneSource.data['y'] = [new] + 0 *circleOneSource.data['y']
    else:
        pass
def update_ballTwo_x_position(attr,old,new):
    global Active
    
    if Active == False:
        circleTwoSource.data['x'] = [new] + 0 *circleTwoSource.data['x']
    else:
        pass
def update_ballTwo_y_position(attr,old,new):
    global Active
    
    if Active == False:
        circleTwoSource.data['y'] = [new] + 0 *circleTwoSource.data['y']
    else:
        pass
def update_ballOne_VelocityDir(attr,old,new):
    global velocityVectorOne
    if Active == False:
        angle = new
        velocityMagnitude = np.sqrt( np.dot(velocityVectorOne, velocityVectorOne) )
        velocityVectorOne = velocityMagnitude * np.array([np.cos(np.deg2rad(angle)) , np.sin(np.deg2rad(angle))])
        xs = sourceArrowOne.data['xs'][0]
        ys = sourceArrowOne.data['ys'][0]
        xe = xs + velocityVectorOne[0]
        ye = ys + velocityVectorOne[1]
        
        sourceArrowOne.data = dict(
                                       xs = [xs],
                                       ys = [ys],
                                       xe = [xe],
                                       ye = [ye]
                                  )
        
        circleOneSource.data['vx'] = [velocityVectorOne[0]] + 0 *circleOneSource.data['vx']
        circleOneSource.data['vy'] = [velocityVectorOne[1]] + 0 *circleOneSource.data['vy']
    else:
        pass
def update_ballOne_VelocityMag(attr,old,new):
    global velocityVectorOne
    if Active == False:
        magnitude = new
        velocityMagnitude = np.sqrt( np.dot(velocityVectorOne, velocityVectorOne))
        if velocityMagnitude == 0:
            velocityVectorOne = np.array([1,0])
        else:
            velocityVectorOne *= 1/velocityMagnitude                        
        velocityVectorOne *= magnitude
        xs = sourceArrowOne.data['xs'][0]
        ys = sourceArrowOne.data['ys'][0]
        xe = xs + velocityVectorOne[0]
        ye = ys + velocityVectorOne[1]
        
        sourceArrowOne.data = dict(
                                       xs = [xs],
                                       ys = [ys],
                                       xe = [xe],
                                       ye = [ye]
                                  )
        
        circleOneSource.data['vx'] = [velocityVectorOne[0]] + 0 *circleOneSource.data['vx']
        circleOneSource.data['vy'] = [velocityVectorOne[1]] + 0 *circleOneSource.data['vy']
    else:
        pass
def update_ballTwo_VelocityDir(attr,old,new):
    global velocityVectorTwo
    if Active == False:
        angle = new
        velocityMagnitude = np.sqrt( np.dot(velocityVectorTwo, velocityVectorTwo) )
        velocityVectorTwo = velocityMagnitude * np.array([np.cos(np.deg2rad(angle)) , np.sin(np.deg2rad(angle))])
        xs = sourceArrowTwo.data['xs'][0]
        ys = sourceArrowTwo.data['ys'][0]
        xe = xs + velocityVectorTwo[0]
        ye = ys + velocityVectorTwo[1]
        
        sourceArrowTwo.data = dict(
                                       xs = [xs],
                                       ys = [ys],
                                       xe = [xe],
                                       ye = [ye]
                                  )
        
        circleTwoSource.data['vx'] = [velocityVectorTwo[0]] + 0 *circleTwoSource.data['vx']
        circleTwoSource.data['vy'] = [velocityVectorTwo[1]] + 0 *circleTwoSource.data['vy']
    else:
        pass
def update_ballTwo_VelocityMag(attr,old,new):
    global velocityVectorTwo
    if Active == False:
        magnitude = new
        velocityMagnitude = np.sqrt( np.dot(velocityVectorTwo, velocityVectorTwo))
        if velocityMagnitude == 0:
            velocityVectorTwo = np.array([1,0])
        else:
            velocityVectorTwo *= 1/velocityMagnitude                      
        velocityVectorTwo *= magnitude
        xs = sourceArrowTwo.data['xs'][0]
        ys = sourceArrowTwo.data['ys'][0]
        xe = xs + velocityVectorTwo[0]
        ye = ys + velocityVectorTwo[1]
        
        sourceArrowTwo.data = dict(
                                       xs = [xs],
                                       ys = [ys],
                                       xe = [xe],
                                       ye = [ye]
                                  )
        
        circleTwoSource.data['vx'] = [velocityVectorTwo[0]] + 0 *circleTwoSource.data['vx']
        circleTwoSource.data['vy'] = [velocityVectorTwo[1]] + 0 *circleTwoSource.data['vy']
    else:
        pass
    
def update_Cr_value(attr,old,new):
    global Cr
    Cr = new
    
ballOneXCoordSlider = Slider(title=u" Green ball x-coordinate ", value=0, start=xMin, end=xMax, step=0.25,width=300)
ballOneXCoordSlider.on_change('value',update_ballOne_x_position)

ballOneYCoordSlider = Slider(title=u" Green ball y-coorditate ", value=0, start=yMin, end=yMax, step=0.25,width=300)
ballOneYCoordSlider.on_change('value',update_ballOne_y_position)

ballTwoXCoordSlider = Slider(title=u" Red ball x-coordinate ", value=0, start=xMin, end=xMax, step=0.25,width=300)
ballTwoXCoordSlider.on_change('value',update_ballTwo_x_position)

ballTwoYCoordSlider = Slider(title=u" Red ball y-coordinate ", value=0, start=yMin, end=xMax, step=0.25,width=300)
ballTwoYCoordSlider.on_change('value',update_ballTwo_y_position)

playGround.add_layout( 
                      Arrow(end=OpenHead(line_color="black",line_width=3,size=10),
                            x_start=['xs'][0],
                            y_start=['ys'][0],
                            x_end=['xe'][0], 
                            y_end=['ye'][0], 
                            source = sourceArrowOne) 
                     )
playGround.add_layout( 
                      Arrow(end=OpenHead(line_color="black",line_width=3,size=10),
                            x_start=['xs'][0],
                            y_start=['ys'][0],
                            x_end=['xe'][0], 
                            y_end=['ye'][0], 
                            source = sourceArrowTwo) 
                     )

ballOneVelocityDirSlider = Slider(title=u" Green ball velocity direction ", value=0, start=0, end=360, step=1.0, width=300)
ballOneVelocityDirSlider.on_change('value',update_ballOne_VelocityDir)

ballOneVelocityMagSlider = Slider(title=u" Green ball veloccity magnitude ", value=0, start=0, end=5, step=0.1, width=300)
ballOneVelocityMagSlider.on_change('value',update_ballOne_VelocityMag)

ballTwoVelocityDirSlider = Slider(title=u" Red ball velocity direction ", value=0, start=0, end=360, step=1.0, width=300)
ballTwoVelocityDirSlider.on_change('value',update_ballTwo_VelocityDir)

ballTwoVelocityMagSlider = Slider(title=u" Red ball veloccity magnitude ", value=0, start=0, end=5, step=0.1, width=300)
ballTwoVelocityMagSlider.on_change('value',update_ballTwo_VelocityMag)


Cr_Slider = Slider(title=u" coefficient of restitution ", value=1, start=0, end=1, step=0.1,width=600)
Cr_Slider.on_change('value',update_Cr_value)
    
curdoc().add_periodic_callback( compute_tranjectory,10 )

curdoc().add_root(
                    row(
                            eFig.getFig(),
                            playGround,
                            column(
                                       reset_button,
                                       play_button,
                                       pause_button,
                                       row(
                                           column(
                                                   ballOneXCoordSlider,
                                                   ballOneYCoordSlider,
                                                   ballOneVelocityDirSlider,
                                                   ballOneVelocityMagSlider,                                                  
                                                 ),
                                           column(
                                                   ballTwoXCoordSlider,
                                                   ballTwoYCoordSlider,
                                                   ballTwoVelocityDirSlider,
                                                   ballTwoVelocityMagSlider                                                  
                                                 )
                                          ),
                                       Cr_Slider 
                                  )
                       )
                 )                       