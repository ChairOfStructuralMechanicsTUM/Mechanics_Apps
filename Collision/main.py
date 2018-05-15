import numpy as np
from bokeh.io import curdoc
from bokeh.plotting import Figure
import BarChart as BC
from bokeh.layouts import column, row, widgetbox
from bokeh.models import Button, Slider, Arrow, OpenHead, Div
from bokeh.models.layouts import Spacer
import Functions
from os.path import dirname, join, split
from bokeh.events import Pan

'''
###############################################################################
Create the plotting domain
###############################################################################
'''
# Define the figure (which corresponds to the play ground)
xMin, xMax = 0, 10
yMin, yMax = 0, 10

playGround = Figure(
                        plot_width = 600,
                        plot_height= 650,
                        x_range  =(xMin, xMax),
                        y_range  =(yMin, yMax),
                        title = 'Collision Play Ground',
                        tools=''
                   )

playGround.title.text_font_size = "25px"
playGround.title.align = "center"
playGround.grid.visible = False
playGround.xaxis.visible = False
playGround.yaxis.visible = False




'''
###############################################################################
Define the objects to be plotted within the plotting domain
 (1) Travelling balls
 (2) Velocity arrows
###############################################################################
'''
# Define the initial parameters of the two colliding balls (in our 2D app, circles)
x1,x2 = 4.0,6.0
y1,y2 = 2.0,2.0
r1,r2 = 0.5,0.35
m1,m2 = 2,1
c1,c2 = '#A2AD00','#E37222'

# initial velocity vector
v_x1,v_y1 = 0.0,0.0
v_x2,v_y2 = 3.0,0.0

# initial  direction of velocity vector
dirOne = np.arctan2(v_y1,v_x1)/np.pi*180
dirTwo = np.arctan2(v_y2,v_x2)/np.pi*180

if dirOne < 0:
    dirOne += 360
else:
    pass

if dirTwo < 0:
    dirTwo += 360
else:
    pass

# initial magnitude of velocity vector
magOne = np.sqrt( v_x1 ** 2 + v_y1 ** 2 )
magTwo = np.sqrt( v_x2 ** 2 + v_y2 ** 2 )



velocityVectorOne = np.array([v_x1,v_y1])
velocityVectorTwo = np.array([v_x2,v_y2])

# Collision Parameters
Cr = 1.0

# Define the dynamic simulation parameters
dt = 0.01
tolerance = 0.1
velocityTolerance = 0.05
Active = False

# Construct particles
particleOne = Functions.Particle(m1, r1, c1, np.array([x1,y1]), velocityVectorOne)
particleTwo = Functions.Particle(m2, r2, c2, np.array([x2,y2]), velocityVectorTwo)

# Construct source files
particleOne.update_position_source()
particleTwo.update_position_source()

particleOne.construct_velocity_source()
particleTwo.construct_velocity_source()
  
# Add figures to the play ground
playGround.circle( x='x', y='y', source=particleOne.get_position_source(), color=particleOne.color, radius=particleOne.radius )
playGround.circle( x='x', y='y', source=particleTwo.get_position_source(), color=particleTwo.color, radius=particleTwo.radius )

playGround.add_layout( 
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
                            source = particleOne.get_velocity_source()
                           ) 
                     )
playGround.add_layout( 
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
                            source = particleTwo.get_velocity_source()
                           ) 
                     )
                            
system = Functions.CollidingSystem([[xMin,xMax],[yMin,yMax]], [particleOne, particleTwo])

'''
##  Define the energy bar
'''

barsFig = BC.BarChart(
                      ["Green ball",
                      "Orange ball",
                      "Whole system"],
                      [50,50,50],
                      ["#A2AD00","#E37222","#003359"],
                      [1,1,1]
                     )
barsFig.Width(300)
barsFig.Height(650)
barsFig.values='timing'


def update_bars():
    # Determine the new kinetic energy of both balls
    yellowBallKE = 0.5 * m1 * (
        particleOne.velocity[0] ** 2
        + particleOne.velocity[1] ** 2
    )

    redBallKE = 0.5 * m2 * (
        particleTwo.velocity[0] ** 2
        + particleTwo.velocity[1] ** 2
    )

    totalKE = yellowBallKE + redBallKE

    # Update the bar heights accordingly
    barsFig.setHeight(0, yellowBallKE)
    barsFig.setHeight(1, redBallKE)
    barsFig.setHeight(2, totalKE)

update_bars()

'''
###############################################################################
Define the function that will develope the position of the balls and bar chart
through time
###############################################################################
'''
# Calculate the new location of the two balls
def compute_trajectory():
    # Compute the new position of the circles' center
    particleOne.position[0] += particleOne.velocity[0]*dt
    particleOne.position[1] += particleOne.velocity[1]*dt
    particleOne.update_position_source()
    
    particleTwo.position[0] += particleTwo.velocity[0]*dt
    particleTwo.position[1] += particleTwo.velocity[1]*dt
    particleTwo.update_position_source()


    # Detect Walls
    if (   abs( particleOne.position[0] + particleOne.radius - xMax ) <= abs(particleOne.velocity[0])*dt + tolerance
        or abs( particleOne.position[0] - particleOne.radius - xMin ) <= abs(particleOne.velocity[0])*dt + tolerance):
        
        # The negative sign is to reflect the ball
        particleOne.velocity[0] *= -1

    elif (   abs( particleTwo.position[0] + particleTwo.radius - xMax ) <= abs(particleTwo.velocity[0])*dt + tolerance
          or abs( particleTwo.position[0] - particleTwo.radius - xMin ) <= abs(particleTwo.velocity[0])*dt + tolerance):
        
        particleTwo.velocity[0] *= -1

    if (   abs( particleOne.position[1] + particleOne.radius - yMax ) <= abs(particleOne.velocity[1])*dt + tolerance 
        or abs( particleOne.position[1] - particleOne.radius - yMin ) <= abs(particleOne.velocity[1])*dt + tolerance):
        
        particleOne.velocity[1] *= -1

    elif (   abs( particleTwo.position[1] + particleOne.radius - yMax ) <= abs(particleTwo.velocity[1])*dt + tolerance
          or abs( particleTwo.position[1] - particleOne.radius - yMin ) <= abs(particleTwo.velocity[1])*dt + tolerance):
        
        particleTwo.velocity[1] *= -1

    # Detect each other
    # Calculate the distance between each others' centers
    dx = particleOne.position[0]-particleTwo.position[0]
    dy = particleOne.position[1]-particleTwo.position[1]
    distance = np.sqrt( dx*dx + dy*dy )

    # Unit vector aiming from ball 1 to ball 2
    normal2Vector = np.array( [-dx,-dy] )/distance

    # Determine the pre-collision speed of both balls
    v1Before = particleOne.velocity #array
    v2Before = particleTwo.velocity
    
    # Determine the normal component of each ball's velocity (w.r.t previously 
    # computed normal vector)
    v1Normal = np.dot(v1Before,normal2Vector) #scalar
    v2Normal = np.dot(v2Before,normal2Vector)
    
    # Determine the tangential component of each ball's velocity
    v1TangentVector = v1Before - v1Normal*normal2Vector #array
    v2TangentVector = v2Before - v2Normal*normal2Vector

    # This list of if statements determines the cases where collision can take
    # place
    collision = False                      # Collision boolean variable
                                           # True: collision happens
                                           # False: collision can't happen
    # Case where balls are moving in the same direction 
    # (against the normal vector's direction)
    if v1Normal <= 0 and  v2Normal <= 0 :
        if abs(v2Normal)-abs(v1Normal) > 0:
            collision = True
        else:
            collision = False
    # Case where balls are moving in the same direction 
    # (in the normal vector's direction)
    elif v1Normal >= 0 and v2Normal >= 0 :
        if abs(v1Normal)-abs(v2Normal) > 0:
            collision = True
        else:
            collision = False
    # Case where balls are moving away from each other
    elif v1Normal <= 0 and v2Normal >= 0:
        collision = False
    # Case where balls are moving against each other
    elif v1Normal >= 0 and v2Normal <= 0:
        collision = True

    # This if statement is executed whenever the distance between the two balls
    # is close "enough" and the collision boolean variable is True
    separation = abs(r1+r2)
    
    if (abs(distance - separation) <= tolerance and collision == True):
        
        # Calculate the new normal velocity component of each ball according to
        # the law of collision
        v1NormalAfter = (
                             Cr*m2*(v2Normal-v1Normal) 
                           + m1*v1Normal + m2*v2Normal
                        ) / (m1 + m2)
        
        v2NormalAfter = (
                             Cr*m1*(v1Normal-v2Normal) 
                           + m1*v1Normal + m2*v2Normal
                        ) / (m1 + m2)
        
        # Updating the normal velocity of each ball
        v1Normal = v1NormalAfter
        v2Normal = v2NormalAfter
        
        # Getting the vector form of the normal velocity after collision
        v1NormalVector = v1Normal*normal2Vector
        v2NormalVector = v2Normal*normal2Vector
        
        # Since the tangential velocity is maintained, it will be added to the 
        # new normal component to form the complete velocity vector after 
        # the collision
        v1After = v1NormalVector + v1TangentVector
        v2After = v2NormalVector + v2TangentVector
        
        # Update the source data file of both balls
        particleOne.velocity = v1After
        particleTwo.velocity = v2After

    else:
        pass
    
    # Update the kinetic energies and velocity arrows plotted by each bar 
    # according to the new velocities calculated previously
    update_bars()
    
    particleOne.update_velocity_source()
    particleTwo.update_velocity_source()
    
    particleOne.update_position_source()
    particleTwo.update_position_source()
    

    
'''
###############################################################################
Add the interactive functionalities
###############################################################################
'''
########################### Creating reset button #############################
def Reset():
    if curdoc().session_callbacks:
        for c in curdoc().session_callbacks:
            curdoc().remove_periodic_callback(c)
    
    # Return the solider to their default values
    ballOneVelocityDirSlider.value = dirOne
    ballTwoVelocityDirSlider.value = dirTwo
    ballOneVelocityMagSlider.value = magOne
    ballTwoVelocityMagSlider.value = magTwo

    # Update the source data file to the very initial data
    particleOne.update_position(x1,y1)
    #particleOne.update_position_source() #- > not necessary anymore - already implied in particle.update_position()
    
    particleTwo.update_position(x2,y2)
    #particleTwo.update_position_source() #- > not necessary anymore - already implied in particle.update_position()
    
    # Update the velocity vectors
    particleOne.update_velocity(v_x1, v_y1)
    particleTwo.update_velocity(v_x2, v_y2)

    # Update the velocity arrows' source file - > not necessary anymore - already implied in particle.update_velocity()
    #particleOne.update_velocity_source()
    #particleTwo.update_velocity_source()

    playpause_button.label = "Play"

    # Update the height of the bars accordingly
    update_bars()
    


reset_button = Button(label="Reset", button_type="success")
reset_button.on_click(Reset)

########################### Creating pause button #############################
# def pause():
#     global Active
#     # When active pause animation
#     if Active == True:
#         curdoc().remove_periodic_callback(compute_trajectory)
#         Active=False
#     else:
#         pass
#
# pause_button = Button(label="Pause", button_type="success")
# pause_button.on_click(pause)

########################### Creating play button ##############################
# def play():
#     global Active, periodicCallback
#
#     if Active == False:
#         curdoc().add_periodic_callback(compute_trajectory, 10)
#         Active=True
#         periodicCallback = 0
#     else:
#         pass
#
# play_button = Button(label="Play", button_type="success")
# play_button.on_click(play)


########################### Creating play-pause button ##############################
def playpause():
    if playpause_button.label == "Play":
        curdoc().add_periodic_callback(compute_trajectory, 10)
        playpause_button.label = "Pause"
    else:
        for c in curdoc().session_callbacks:
            curdoc().remove_periodic_callback(c)
        playpause_button.label = "Play"


playpause_button = Button(label="Play", button_type="success")
playpause_button.on_click(playpause)

##################### Creating velocity direction slider ######################
def update_ballOne_VelocityDir(attr,old,new):
    angle = new
    velocityMagnitude = np.sqrt( np.dot(particleOne.velocity, particleOne.velocity) )
    
    if velocityMagnitude == 0:
        # Create some default velocity vector
        newVelocityVectorOne = np.array([1.0,0.0])
        # Update respective Magnitude slider
        ballOneVelocityMagSlider.value = 1
    else:
        newVelocityVectorOne = velocityMagnitude * np.array([
                                                            np.cos(np.deg2rad(angle)),
                                                            np.sin(np.deg2rad(angle))
                                                        ])
        
    particleOne.update_velocity(newVelocityVectorOne[0], newVelocityVectorOne[1])
    
ballOneVelocityDirSlider = Slider(
                                  title=u" Green Ball Velocity Direction (deg) ",
                                  value=dirOne , start=0, end=360, step=1.0, width=260
                                 )
ballOneVelocityDirSlider.on_change('value',update_ballOne_VelocityDir)

##################### Creating velocity magnitude slider ######################
def update_ballOne_VelocityMag(attr,old,new):
    magnitude = new
    velocityMagnitude = np.sqrt( np.dot(particleOne.velocity, particleOne.velocity))
    if velocityMagnitude == 0.0:
        # Create some default velocity vector
        newVelocityVectorOne = np.array([1.0,0.0])
    else:
        vx, vy = particleOne.get_velocity()
        newVelocityVectorOne = np.array([vx,vy])
        newVelocityVectorOne *= 1/velocityMagnitude                        
        newVelocityVectorOne *= magnitude
        
    particleOne.update_velocity(newVelocityVectorOne[0],newVelocityVectorOne[1])

    #Reset respective direction Slider if magnitude == 0
    if magnitude == 0.0:
        ballOneVelocityDirSlider.value = 0
    else:
        pass

    update_bars()
   
ballOneVelocityMagSlider = Slider(
                                  title=u" Green Ball Velocity Magnitude (m/s) ",
                                  value=magOne, start=0, end=5, step=0.1, width=260
                                 )
ballOneVelocityMagSlider.on_change('value',update_ballOne_VelocityMag)

##################### Creating velocity direction slider ######################
def update_ballTwo_VelocityDir(attr,old,new):
    angle = new
    velocityMagnitude = np.sqrt( np.dot(particleTwo.velocity, particleTwo.velocity) )
    
    if velocityMagnitude == 0:
        # Create some default velocity vector
        newVelocityVectorTwo = np.array([1.0,0.0])
        # Update respective Magnitude slider
        ballTwoVelocityMagSlider.value = 1
    else:
        newVelocityVectorTwo = velocityMagnitude * np.array([
                                                            np.cos(np.deg2rad(angle)),
                                                            np.sin(np.deg2rad(angle))
                                                        ]) 
        
    particleTwo.update_velocity(newVelocityVectorTwo[0],newVelocityVectorTwo[1])
    
ballTwoVelocityDirSlider = Slider(  
                                  title=u" Orange Ball Velocity Direction (deg) ",
                                  value=dirTwo, start=0, end=360, step=1.0, width=260
                                 )
ballTwoVelocityDirSlider.on_change('value',update_ballTwo_VelocityDir)

##################### Creating velocity magnitude slider ######################
def update_ballTwo_VelocityMag(attr,old,new):
    magnitude = new
    velocityMagnitude = np.sqrt( np.dot(particleTwo.velocity, particleTwo.velocity))
    if velocityMagnitude == 0:
        # Create some default velocity vector
        newVelocityVectorTwo = np.array([1.0,0.0])
    else:
        vx, vy = particleTwo.get_velocity()
        newVelocityVectorTwo = np.array([vx,vy])
        newVelocityVectorTwo *= 1/velocityMagnitude                      
        newVelocityVectorTwo *= magnitude
        
    particleTwo.update_velocity(newVelocityVectorTwo[0],newVelocityVectorTwo[1])

    # Reset respective direction Slider if magnitude == 0
    if magnitude == 0.0:
        ballTwoVelocityDirSlider.value = 0
    else:
        pass

    update_bars()
    
ballTwoVelocityMagSlider = Slider(
                                  title=u" Orange Ball Velocity Magnitude (m/s) ",
                                  value=magTwo, start=0, end=5, step=0.1, width=260
                                 )
ballTwoVelocityMagSlider.on_change('value',update_ballTwo_VelocityMag)

################# Creating coefficient of restitution slider ##################
def update_Cr_value(attr,old,new):
    global Cr
    Cr = new

Cr_Slider = Slider(
                   title=u" Coefficient of Restitution ",
                   value=1, start=0, end=1, step=0.1,width=530
                  )
Cr_Slider.on_change('value',update_Cr_value)

#################### Moving the balls through the mouse #######################

def on_mouse_move(event):
    if Active == False:
        if (system.modify_location(event)==1):
            # if the path is changed then update the drawing
            pass
    else:
        pass

playGround.on_event(Pan, on_mouse_move)

'''
###############################################################################
Add all the components together and initiate the app
###############################################################################
'''
# add app description
description_filename = join(dirname(__file__), "description.html")

description = Div(text=open(description_filename).read(), render_as_text=False, width=1000)

area_image = Div(text="""
<h2>
Particles' Parameters:
</h2>
<p>
<img src="/Collision/static/images/particles_information.png" width=450>
</p>
""", render_as_text=False, width=450)

#buttons = widgetbox(reset_button, play_button, pause_button,width=150)

curdoc().add_root(	
                  column(
                         description,
                         row(
                             playGround,
                             barsFig.getFig()
                         ),
                         row(
                             column(
                                    row(
                                        widgetbox(playpause_button,width=225),
                                        #widgetbox(pause_button,width=150),
                                        widgetbox(reset_button,width=225)
                             ),
                                     area_image),
                             column(
                                    row(
                                        ballOneVelocityDirSlider,
                                        Spacer(width=10),
                                        ballOneVelocityMagSlider,
                                        ),
                                    row(
                                        ballTwoVelocityDirSlider,
                                        Spacer(width=10),
                                        ballTwoVelocityMagSlider
                                        ),
                                    Cr_Slider,
                             )

                        )
                 )
)
                                    
# get path of parent directory and only use the name of the Parent Directory 
# for the tab name. Replace underscores '_' and minuses '-' with blanks ' '				 
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  