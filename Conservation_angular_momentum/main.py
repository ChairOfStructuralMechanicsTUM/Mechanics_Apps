'''
App describtion:
    This app is meant to demonstrate the law of conservation of angular moment-
    um by showing two objects that are rotating opposite to each other's rotat-
    ion direction in order to produce a net of zero angular momentum.
    
    The interactivity that is going to be applied in this app is to enable the
    user to see how the objects are rotating, their angular velocity, and the 
    ability of the user to change the angular velocity with which the objects
    rotate with by graping one of the objects and rotating it using the mouse.
'''

'''
################################# Imports #####################################
'''
import numpy as np
from bokeh.io import curdoc
from bokeh.plotting import Figure
import BarChart as BC
from bokeh.layouts import column, row
from bokeh.models import Button
from bokeh.models import Div
from Functions import *
from os.path import dirname, join, split

'''
######################## Define the plotting space ############################
'''
xMin, xMax = -10, 10
yMin, yMax = -10, 10

playGround = Figure(
                        plot_width = 600,
                        plot_height= 800,
                        x_range  =(xMin, xMax),
                        y_range  =(yMin, yMax),
                        #title = 'Conservation of Angular Momentum',
                        tools = ''
                   )

playGround.title.text_font_size = "25px"
playGround.title.align = "center"
playGround.grid.visible = False
playGround.xaxis.visible = False
playGround.yaxis.visible = False

# Define the energy bar
barsFig = BC.BarChart(
                      ["Wheel",
                      "Rectangular Base",
                      "Whole system"],
                      [15,15,15],
                      [-15,-15,-15],
                      ["#33FF33","#FF3333","#460BF8"],
                      [1,1,1]
                     )
barsFig.Width(300)
barsFig.Height(650)

rotation_speed_wheel = get_velocity('circle') # rad/sec
rotation_speed_base  = get_velocity('base') # rad/sec

J_circle = 1 # Angular moment of inertia of the wheel
J_base   = 2 # Angular moment of inertia of the rectangular base

dt = 0.01
Active = False

'''
#################### Define the objects to be rotating ########################

The objects include:
    (1) Rotating circle (Includes two circles at the top of each other and two
                         othogonal rectangles)
    (2) Rotating rectangle
'''
########################## (1) Rotating circle ################################
#construct_circle_source( 
#                        center=[ [0.0,0.0], [0.0,0.0] ], 
#                        radius=[ 4.0, 3.0 ], 
#                        color=[ "#33FF33","#FFFFFF" ]
#                       )
#construct_cross_source()
#
#circleSource = get_circle_source()
#crossSource = get_cross_source()

rotatingObject = RotatingObject()
rotatingObject.construct_circle_source( 
                                       [[0.0,0.0], [0.0,0.0]],
                                       [4.0, 3.0],
                                       ["#33FF33","#FFFFFF"]
                                      )
rotatingObject.construct_cross_source()

rect_width  = 12 
rect_height = 8

######################### (2) Rotating rectangle ##############################
#construct_rectangle_source( center=[0.0,0.0] )
rotatingObject.construct_rectangle_source([0.0,0.0],12,8)
mouseTouch = MouseTouch([[xMin,xMax],[yMin,yMax]], rotatingObject)
#rectangelSource = get_rectangle_source()

'''
####################### Define the evolution function #########################
'''
def compute_tranjectory():
    ######################## Rotate the inner wheel ###########################
    #crossSource = get_cross_source()

    angle = rotatingObject.crossSource.data['angle']

    rotation_speed_wheel = rotatingObject.get_velocity('circle') * J_base/J_circle # rad/sec
    angle = [angle[0]+rotation_speed_wheel * dt , angle[1]+rotation_speed_wheel * dt]
    
    rotatingObject.update_cross_source( angle )
    
    ###################### Rotate the rectangular base ########################
    #rectanguleSource = get_rectangle_source()
    
    angle = rotatingObject.baseSource.data['angle'][0]

    rotation_speed_base  = rotatingObject.get_velocity('base')  # rad/sec
    angle += rotation_speed_base * dt
    
    rotatingObject.update_rectangle_source( angle )    
    
    update_bars(rotation_speed_wheel, rotation_speed_base)
   
def update_bars(wheelVelocity, baseVelocity):
    
    wheelMomentum = J_circle * wheelVelocity
    baseMomentum  = J_base  * baseVelocity
    totalMomentum = wheelMomentum + baseMomentum
    
    barsFig.setHeight(0,wheelMomentum)
    barsFig.setHeight(1,baseMomentum)
    barsFig.setHeight(2,totalMomentum)
    
'''
########################## Define interactivities #############################
Include:
    (1) Reset button
    (2) Pause button
    (3) Play button
    (4) Mouse touch
'''
############################## (1) Reset button ###############################
periodicCallback = 0
def Reset():
    global Active, periodicCallback

    # The preiodic callback has been removed here because when the pause 
    # button is set to False, this reactivates the periodic callback
    if periodicCallback == 0 and Active == True:
        curdoc().remove_periodic_callback(compute_tranjectory)
        periodicCallback += 1
        rotatingObject.set_velocity(0)
        
        angle = np.array([0,np.pi/2])
        rotatingObject.update_cross_source( angle )
        rotatingObject.update_rectangle_source( angle=0 ) 
        update_bars(get_velocity('circle'), get_velocity('base'))
        
    else:
        pass
    
    Active = False
reset_button = Button(label="Reset", button_type="success")
reset_button.on_click(Reset)

############################## (2) Pause button ###############################
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

############################## (3) Play button ################################
def play ():
    global Active, periodicCallback
    
    if Active == False:
        curdoc().add_periodic_callback(compute_tranjectory, 10)
        Active=True
        periodicCallback = 0
    else:
        pass
        
play_button = Button(label="Play", button_type="success")
play_button.on_click(play)

############################## (4) Mouse touch ################################
playGround.add_tools(MoveNodeTool())

def on_mouse_move(attr, old, new):
    #global rotation_speed_wheel, rotation_speed_base

    if (mouseTouch.modify_location(old,new)==1) and Active == True:
        # if the path is changed then update the drawing
        pass
    
playGround.tool_events.on_change('geometries', on_mouse_move)

'''
########################### Plot the application ##############################
'''
# add app description
description_filename = join(dirname(__file__), "description.html")

description = Div(text=open(description_filename).read(), render_as_text=False, width=1200)

area_image = Div(text="""
<p>
<img src="/Conservation_angular_momentum/static/images/picture.jpg" width=500>
</p>
<p>
Angular Moment of Inertia pf the rotating bodies
</p>""", render_as_text=False, width=350)

playGround.rect(
                x = 'x',
                y = 'y',
                angle = 'angle',
                width ='width',
                height='height',
                source=rotatingObject.baseSource,
                color = "#F22633",
                height_units = 'data'
               )

playGround.circle(
                    x = 'x',
                    y = 'y',
                    radius  = 'radius',
                    color = 'color',
                    source = rotatingObject.circleSource,
                 )

playGround.rect(
                  x = 'x',
                  y = 'y',
                  angle = 'angle',
                  source = rotatingObject.crossSource,
                  width = 1,
                  height = 6,
                  color="#33FF33",
                  height_units="data"
               )

barChart = barsFig.getFig()
barChart.yaxis.axis_label="Angular Momentum ( kg*meter/second )"

curdoc().add_root(
                  column(
                         description,
                         row(
                              playGround,
                              column(
                                     reset_button, 
                                     play_button, 
                                     pause_button,
                                     barChart
                                    ),
                              area_image
                            )
                        )
                 )
                      
# get path of parent directory and only use the name of the Parent Directory 
# for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  