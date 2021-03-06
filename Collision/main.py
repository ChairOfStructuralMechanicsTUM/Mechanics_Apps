"""
Collision - simulate elastic and inelastic collisions of two masses

"""
# general imports
import numpy as np
import yaml

# bokeh imports
from bokeh.io import curdoc
from bokeh.plotting import Figure
from bokeh.models import Button, Slider, Arrow, OpenHead, Div, ColumnDataSource
from bokeh.models.tools import ResetTool, BoxZoomTool
from bokeh.layouts import column, row, widgetbox, Spacer
from bokeh.events import Pan

# internal imports
import Collision_BarChart as BC
import Collision_Functions

# latex integration
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexSlider

# change language
std_lang = 'en'
flags    = ColumnDataSource(data=dict(show=['off'], lang=[std_lang]))
strings  = yaml.safe_load(open('Collision/static/strings.json', encoding='utf-8'))

'''
###############################################################################
Global variables
###############################################################################
'''
glCollision = dict(Crval=1.0, cid=None) # collision parameter and callback id
slider_width = 300 # constant width for velocity sliders
glob_active = ColumnDataSource(data=dict(Active=[False]))
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
playGround.title.align          = "center"
playGround.grid.visible         = False
playGround.xaxis.visible        = False
playGround.yaxis.visible        = False
playGround.toolbar.logo         = None


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

if dirTwo < 0:
    dirTwo += 360

# initial magnitude of velocity vector
magOne = np.sqrt( v_x1 ** 2 + v_y1 ** 2 )
magTwo = np.sqrt( v_x2 ** 2 + v_y2 ** 2 )

velocityVectorOne = np.array([v_x1,v_y1])
velocityVectorTwo = np.array([v_x2,v_y2])

# Define the dynamic simulation parameters
dt = 0.01
tolerance = 0.1
velocityTolerance = 0.05

# Construct particles
particleOne = Collision_Functions.Collision_Particle(m1, r1, c1, np.array([x1,y1]), velocityVectorOne)
particleTwo = Collision_Functions.Collision_Particle(m2, r2, c2, np.array([x2,y2]), velocityVectorTwo)

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
                            
system = Collision_Functions.Collision_CollidingSystem([[xMin,xMax],[yMin,yMax]], [particleOne, particleTwo])

'''
##  Define the energy bar
'''

barsFig = BC.Collision_BarChart(
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
barsFig.fig.add_tools(BoxZoomTool())
barsFig.fig.add_tools(ResetTool())


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
    glCollisionCr_val = glCollision["Crval"] # input/
    
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
                             glCollisionCr_val*m2*(v2Normal-v1Normal) 
                           + m1*v1Normal + m2*v2Normal
                        ) / (m1 + m2)
        
        v2NormalAfter = (
                             glCollisionCr_val*m1*(v1Normal-v2Normal) 
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
    glCollision_id = glCollision["cid"] # input/
    if curdoc().session_callbacks:
        #for c in curdoc().session_callbacks:
        curdoc().remove_periodic_callback(glCollision_id)
    
    # Return the solider to their default values
    ballOneVelocityDirSlider.value = dirOne
    ballTwoVelocityDirSlider.value = dirTwo
    ballOneVelocityMagSlider.value = magOne
    ballTwoVelocityMagSlider.value = magTwo

    # Update the source data file to the very initial data
    particleOne.update_position(x1,y1)
    particleTwo.update_position(x2,y2)
    
    # Update the velocity vectors
    particleOne.update_velocity(v_x1, v_y1)
    particleTwo.update_velocity(v_x2, v_y2)

    [lang] = flags.data["lang"]
    glob_active.data["Active"][0] = False
    playpause_button.label = strings["playpause_button.label"]['on'][lang]
    ballOneVelocityDirSlider.disabled = False
    ballOneVelocityMagSlider.disabled = False
    ballTwoVelocityDirSlider.disabled = False
    ballTwoVelocityMagSlider.disabled = False
    crSlider.disabled                 = False

    # Update the height of the bars accordingly
    update_bars()

reset_button = Button(label="Reset", button_type="success")
reset_button.on_click(Reset)

########################### Creating play-pause button ##############################
def playpause():
    [lang] = flags.data["lang"]
    glCollision_id = glCollision["cid"] # input/output
    if not glob_active.data["Active"][0]:
        glCollision_id = curdoc().add_periodic_callback(compute_trajectory, 10)
        glob_active.data["Active"][0] = True
        playpause_button.label = strings["playpause_button.label"]['off'][lang]
        ballOneVelocityDirSlider.disabled = True
        ballOneVelocityMagSlider.disabled = True
        ballTwoVelocityDirSlider.disabled = True    
        ballTwoVelocityMagSlider.disabled = True
       # crSlider.disabled = True  # We can leave the Cr Slider enabled while the app is running, changing Cr on the fly is anice feature and has no impact on performance
        crSlider.disabled = True
    else: # "Pause"
        #for c in curdoc().session_callbacks:
        curdoc().remove_periodic_callback(glCollision_id)
        glob_active.data["Active"][0] = False
        playpause_button.label = strings["playpause_button.label"]['on'][lang]

        #update sliders
        ballOneVelocityDirSlider.value = particleOne.get_direction()
        ballTwoVelocityDirSlider.value = particleTwo.get_direction()
        ballOneVelocityMagSlider.value = particleOne.get_velocity_magnitude()
        ballTwoVelocityMagSlider.value = particleTwo.get_velocity_magnitude()

        ballOneVelocityDirSlider.disabled = False
        ballOneVelocityMagSlider.disabled = False
        ballTwoVelocityDirSlider.disabled = False
        ballTwoVelocityMagSlider.disabled = False
        crSlider.disabled = False
       
    glCollision['cid'] = glCollision_id

playpause_button = Button(label="Play", button_type="success")
playpause_button.on_click(playpause)

##################### Creating velocity direction slider ######################
def update_ballOne_VelocityDir(attr,old,new):
    angle = new
    velocityMagnitude = particleOne.get_velocity_magnitude()
    
    if velocityMagnitude == 0:
        # Create some default velocity vector
        newVelocityVectorOne = np.array([0.1,0.0])
        # Update respective Magnitude slider
        ballOneVelocityMagSlider.value = 0.1
    else:
        newVelocityVectorOne = velocityMagnitude * np.array([
                                                            np.cos(np.deg2rad(angle)),
                                                            np.sin(np.deg2rad(angle))
                                                        ])
        
    particleOne.update_velocity(newVelocityVectorOne[0], newVelocityVectorOne[1])
    
ballOneVelocityDirSlider = LatexSlider(
                                  title="\\text{Green Ball Velocity Direction [deg]:} ",
                                  value=dirOne , start=0, end=360, step=1.0, width=slider_width
                                 )
ballOneVelocityDirSlider.on_change('value',update_ballOne_VelocityDir)

##################### Creating velocity magnitude slider ######################
def update_ballOne_VelocityMag(attr,old,new):
    magnitude = new
    velocityMagnitude = particleOne.get_velocity_magnitude()
    if velocityMagnitude == 0.0:
        # Create some default velocity vector
        newVelocityVectorOne = np.array([0.1,0.0])
    else:
        newVelocityVectorOne = particleOne.velocity
        newVelocityVectorOne *= 1/velocityMagnitude                        
        newVelocityVectorOne *= magnitude
        
    particleOne.update_velocity(newVelocityVectorOne[0],newVelocityVectorOne[1])

    #Reset respective direction Slider if magnitude == 0
    if magnitude == 0.0:
        ballOneVelocityDirSlider.value = 0
    else:
        pass

    update_bars()
   
ballOneVelocityMagSlider = LatexSlider(
                                  title="\\text{Green Ball Velocity Magnitude} \\left[ \\frac{m}{s} \\right] :",
                                  value=magOne, start=0, end=5, step=0.1, width=slider_width
                                 )
ballOneVelocityMagSlider.on_change('value',update_ballOne_VelocityMag)

##################### Creating velocity direction slider ######################
def update_ballTwo_VelocityDir(attr,old,new):
    angle = new
    velocityMagnitude = particleTwo.get_velocity_magnitude()
    
    if velocityMagnitude == 0:
        # Create some default velocity vector
        newVelocityVectorTwo = np.array([0.1,0.0])
        # Update respective Magnitude slider
        ballTwoVelocityMagSlider.value = 0.1
    else:
        newVelocityVectorTwo = velocityMagnitude * np.array([
                                                            np.cos(np.deg2rad(angle)),
                                                            np.sin(np.deg2rad(angle))
                                                        ]) 
        
    particleTwo.update_velocity(newVelocityVectorTwo[0],newVelocityVectorTwo[1])
    
ballTwoVelocityDirSlider = LatexSlider(  
                                  title="\\text{Orange Ball Velocity Direction [deg]:}",
                                  value=dirTwo, start=0, end=360, step=1.0, width=slider_width
                                 )
ballTwoVelocityDirSlider.on_change('value',update_ballTwo_VelocityDir)

##################### Creating velocity magnitude slider ######################
def update_ballTwo_VelocityMag(attr,old,new):
    magnitude = new
    velocityMagnitude = particleTwo.get_velocity_magnitude()
    if velocityMagnitude == 0:
        # Create some default velocity vector
        newVelocityVectorTwo = np.array([0.1,0.0])
    else:
        newVelocityVectorTwo = particleTwo.velocity
        newVelocityVectorTwo *= 1/velocityMagnitude                      
        newVelocityVectorTwo *= magnitude
        
    particleTwo.update_velocity(newVelocityVectorTwo[0],newVelocityVectorTwo[1])

    # Reset respective direction Slider if magnitude == 0
    if magnitude == 0.0:
        ballTwoVelocityDirSlider.value = 0
    else:
        pass

    update_bars()
    
ballTwoVelocityMagSlider = LatexSlider(
                                  title="\\text{Orange Ball Velocity Magnitude} \\left[ \\frac{m}{s} \\right] : ",
                                  value=magTwo, start=0, end=5, step=0.1, width=slider_width
                                 )
ballTwoVelocityMagSlider.on_change('value',update_ballTwo_VelocityMag)

################# Creating coefficient of restitution slider ##################
def update_Cr_value(attr,old,new):
    glCollision['Crval'] = new #      /output

crSlider = LatexSlider(
                   title="\\text{Coefficient of Restitution:}",
                   value=1, start=0, end=1, step=0.1,width=2*slider_width+10
                  )
crSlider.on_change('value',update_Cr_value)

#################### Moving the balls through the mouse #######################

def on_mouse_move(event):
    if not glob_active.data["Active"][0]:
        system.modify_location(event)

playGround.on_event(Pan, on_mouse_move)


'''
###############################################################################
Change language
###############################################################################
'''
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
        playpause_button.label = strings["playpause_button.label"]['off'][lang]
    else:
        playpause_button.label = strings["playpause_button.label"]['on'][lang]

    barsFig.change_label()

    

lang_button = Button(button_type="success", label="Zu Deutsch wechseln")
lang_button.on_click(changeLanguage)


'''
###############################################################################
Add all the components together and initiate the app
###############################################################################
'''
# add app description
description_filename = join(dirname(__file__), "description.html")
description = Div(text=open(description_filename).read(), render_as_text=False, width=1000)

particles_parameters_filename = join(dirname(__file__), "particles_parameters.html")
particles_parameters = Div(text=open(particles_parameters_filename).read(), render_as_text=False, width=450)


curdoc().add_root(
    column(
        row(Spacer(width=700),lang_button),
        description,
        row(
            playGround,
            Spacer(width=130),
            barsFig.fig
        ),
        row(
            column(
                row(
                    widgetbox(playpause_button, width=225),
                    widgetbox(reset_button, width=225)
                ),
                column(particles_parameters)),
            column(
                row(
                    ballOneVelocityDirSlider,
                    Spacer(width=10),
                    ballOneVelocityMagSlider,
                ), Spacer(height=20), 
                row(
                    ballTwoVelocityDirSlider,
                    Spacer(width=10),
                    ballTwoVelocityMagSlider
                ), Spacer(height=20),
                crSlider,
            )
        )
    )
)
                                    
# get path of parent directory and only use the name of the Parent Directory 
# for the tab name. Replace underscores '_' and minuses '-' with blanks ' '				 
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')