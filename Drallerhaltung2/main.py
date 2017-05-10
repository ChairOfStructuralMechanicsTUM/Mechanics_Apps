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
from bokeh.plotting import Figure, ColumnDataSource
#import BarChart as BC
from bokeh.layouts import column, row
from bokeh.models import Button, Toggle, Slider
from bokeh.models import Arrow, OpenHead
from Functions import *

'''
######################## Define the plotting space ############################
'''
xMin, xMax = 0, 10
yMin, yMax = 0, 10

playGround = Figure(
                        plot_width = 600,
                        plot_height= 800,
                        x_range  =(xMin, xMax),
                        y_range  =(yMin, yMax),
                        title = 'Angular Momnetum'
                   )

playGround.title.text_font_size = "25px"
playGround.title.align = "center"
playGround.grid.visible = True
playGround.xaxis.visible = True
playGround.yaxis.visible = True

rotation_speed = 1 # rad/sec
dt = 0.1
Active = False
'''
#################### Define the objects to be rotating ########################

The objects include:
    (1) Rotating circle (Includes two circles at the top of each other and four
                         quarter circular wedges)
    (2) Rotating rectangle
'''
########################## (1) Rotating circle ################################
construct_circle_source( center=[1,1], radius=1 )
construct_wedges_source( radius=0.7 )

circleSource = get_circle_source()
wedgesSource = get_wedges_source()

######################### (2) Rotating rectangle ##############################
construct_rectangle_source( center=[1,1] )

rectangelSource = get_rectangle_source()

'''
####################### Define the evolution function #########################
'''
def compute_tranjectory():
    global rotation_speed, dt
    
    circleSource = get_circle_source()
    wedgesSource = get_wedges_source()
    
    rectangelSource = get_rectangle_source()
    
    rotation_center = np.array([
                                circleSource.data['x'][0],
                                circleSource.data['y'][0] 
                              ])
    
    centerX, centerY, startAngle, endAngle = list(), list(), list(), list()
    for counter in range(len(wedgesSource.data['x'])):

        x = wedgesSource.data['x'][counter]-rotation_center[0]
        y = wedgesSource.data['y'][counter]-rotation_center[1]
        angle = abs( np.arctan( y/x ) )
        '''
        if x>=0 and y>=0:
            pass
        elif x<=0 and y>=0:
            angle -= 2*np.pi
        elif x<=0 and y<=0:
            angle += 2*np.pi
        else:
            angle *= -1
            
        '''
        angle += dt*rotation_speed
        
        x_shift = abs(0.28284271247*np.cos(angle))
        y_shift = abs(0.28284271247*np.sin(angle))
        print('counter: ',counter)
        print('x_shift= ',x_shift)
        print('y_shift= ',y_shift)
        if x>=0 and y>=0:
            centerX.append( x_shift + rotation_center[0])
            centerY.append( y_shift + rotation_center[1])
        elif x<=0 and y>=0:
            centerX.append( -x_shift + rotation_center[0])
            centerY.append( y_shift + rotation_center[1])
        elif x<=0 and y<=0:
            centerX.append( -x_shift + rotation_center[0])
            centerY.append( -y_shift + rotation_center[1])
        else:
            centerX.append( x_shift + rotation_center[0])
            centerY.append( -y_shift + rotation_center[1])
        
        #centerX.append( 0.28284271247*np.cos(angle) + rotation_center[0])
        #centerY.append( 0.28284271247*np.sin(angle) + rotation_center[1])

        startAngle.append( wedgesSource.data['start_angle'][counter] + rotation_speed * dt )
        endAngle.append( wedgesSource.data['end_angle'][counter] + rotation_speed * dt )
        
    update_wedges_source( centerX, centerY, startAngle, endAngle )
    
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
        curdoc().add_periodic_callback(compute_tranjectory, 100)
        Active=True
        periodicCallback = 0
    else:
        pass
        
play_button = Button(label="Play", button_type="success")
play_button.on_click(play)

'''
########################### Plot the application ##############################
'''
playGround.rect(
                x = 'x',
                y = 'y',
                width = 5,
                height = 3,
                color = "#FF2233",
                source=rectangelSource
               )
playGround.circle(
                   x = 'x',
                   y = 'y',
                   radius = 'r',
                   source = circleSource
                 )
playGround.wedge(
                  x = 'x',
                  y = 'y',
                  radius = 0.6,
                  start_angle = 'start_angle',
                  end_angle   = 'end_angle',
                  #radius_units="screen",
                  color="#FFFFFF",
                  source = wedgesSource
                )
curdoc().title = "Collision"
curdoc().add_root(row(playGround,column(reset_button, play_button, pause_button)))