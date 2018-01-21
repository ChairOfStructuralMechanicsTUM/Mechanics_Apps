import matplotlib.pyplot as plt
from bokeh.models import ColumnDataSource
from MoveNodeTool import *
import numpy as np
from timeit import default_timer as timer

class RotatingObject():
    
    def __init__(self):
        self.circleSource  = 0
        self.crossSource   = 0
        self.baseSource    = 0
        
        self.crossSpeed    = 0
        self.baseSpeed     = 0

    def construct_circle_source( self, center, radius, color ):
        centerX = list()
        centerY = list()
        for i in range(len(center)):
            centerX.append(center[i][0])
            centerY.append(center[i][1])
            
        self.circleSource = ColumnDataSource(
                                             data=dict(
                                                       x = centerX,
                                                       y = centerY,
                                                       radius = radius,
                                                       color = color,
                                                      )
                                            )
    def construct_cross_source(self):
        center = [self.circleSource.data['x'][0] , self.circleSource.data['y'][0]]

        self.crossSource = ColumnDataSource(
                                            data=dict(
                                                      x=[center[0], center[0]],
                                                      y=[center[1], center[1]],
                                                      angle = [0, np.pi/2]
                                                     )
                                           )   
                                            
    def update_cross_source( self, angle ):
        self.crossSource.data = dict(
                                     x=self.crossSource.data['x'],
                                     y=self.crossSource.data['y'],
                                     angle=[angle[0],angle[1]]
                                    ) 

    def construct_rectangle_source( self, center, width, height):
        self.baseSource = ColumnDataSource(
                                           data=dict(
                                                     x = [center[0]],
                                                     y = [center[1]],
                                                     width=[width],
                                                     height=[height],
                                                     angle = [0.0]
                                                    )
                                          ) 
                                           
    def update_rectangle_source( self, angle ):
        self.baseSource.data = dict(
                                    x=self.baseSource.data['x'],
                                    y=self.baseSource.data['y'],   
                                    width=self.baseSource.data['width'],
                                    height=self.baseSource.data['height'],
                                    angle=[angle]
                                   )    
        
    def set_velocity(self, value):

        self.crossSpeed = value 
        self.baseSpeed  =-value
        
    def get_velocity(self, objectName):
        
        if objectName == 'base':
            return self.baseSpeed
        elif objectName == 'circle':
            return self.crossSpeed
        else:
            raise Exception("This rotating object doesn't exist")
            
   
class MouseTouch():
    
    def __init__(self, domain, rotatingObject):
        self.domain         = domain
        self.rotatingObject = rotatingObject
        self.currentNode    = -1
        self.angles          = list()
        self.oldAngle = 0
        
    def inNode (self, click_position):
        
        baseWidth = self.rotatingObject.baseSource.data['width'][0]
        baseHeight = self.rotatingObject.baseSource.data['height'][0]

        xPos = click_position.x
        yPos = click_position.y
        
        if np.sqrt( xPos**2 + yPos**2 ) >= self.rotatingObject.circleSource.data['radius'][1]:
            self.rotatingObject.set_velocity(0)
            return 0
        else:
            return -1
    
    # modify path by dragging nodes
    def modify_location(self, click_position):
        
        self.currentNode = self.inNode(click_position)
        
        x = click_position.x
        y = click_position.y

        
        if self.currentNode == 0:
            newAngle = abs(np.arctan(y/x))
            if x > 0 and y > 0:
                pass
            elif x < 0 and y > 0:
                newAngle += 2*(np.pi - newAngle)
            elif x < 0 and y < 0:
                newAngle += np.pi
            else:
                newAngle += 2*(2*np.pi - newAngle)
            
            self.rotatingObject.update_rectangle_source( self.rotatingObject.baseSource.data['angle'][0] + newAngle - self.oldAngle )
            
            self.angles.append(newAngle)
                
        return 1

    def set_speed(self,event):
        # This equivalent value of the velocity is empirical (no basis)
        rotationSpeed = (self.angles[-3] - self.angles[-1] )*10

        self.angles = list()
        
        self.rotatingObject.set_velocity(rotationSpeed) 
        
        return 1
    
'''
The particleSource, particleXPos, particleYPos are stored in this file because
they are used extensively by the functions inNode() and modify_location(), and
this use cannot be achieved without storing them here.
'''

currentNode=-1

circleSource = list()
crossSource  = 0
baseSource  = 0

olderAngle = 0
oldAngle = 0
velocity = 0
    
'''
The functions inNode() and modify_location() are concerned with the 
functionality of changing the position of the particle (ball) using the mouse.
For more information, get in touch with Emily Bourne, whom I got this code from.
'''
# find index of node in which coordinates are found
# (return -1 if not in a node)
def inNode (xPos,yPos,new):
    
    baseWidth = 12
    baseHeight = 8
    if abs(xPos)<=(baseWidth/2) and abs(yPos)<=(baseHeight/2) and np.sqrt( new[0][u'x']**2 + new[0][u'y']**2 ) >= circleSource.data['radius'][1]:
        set_velocity(0)
        return 0
    else:
        return -1

# modify path by dragging nodes
def modify_location(attr, old, new):
    
    global currentNode, oldAngle, olderAngle, velocity
    
    # if there is a previous node (not first time the function is called)
    # and the node has not been released (new['x']=-1 on release to prepare for future calls)
    if (len(old)==1 and new[0][u'x']!=-1):
        # if first call for this node
        if (currentNode==-1):
            # determine which node and remember it
            XStart=old[0][u'x']
            YStart=old[0][u'y']
            XStart = new[0][u'x']
            YStart = new[0][u'y']

            currentNode =inNode(XStart,YStart,new)
            
            if currentNode == 0:
                newAngle = abs(np.arctan(YStart/XStart))
                if XStart > 0 and YStart > 0:
                    pass
                elif XStart < 0 and YStart > 0:
                    newAngle += 2*(np.pi - newAngle)
                elif XStart < 0 and YStart < 0:
                    newAngle += 2*np.pi
                else:
                    newAngle *= -1
                    
                oldAngle = newAngle

        # if not first call then move node
        else: 
            XStart = new[0][u'x']
            YStart = new[0][u'y']
            newAngle = abs(np.arctan(YStart/XStart))
            olderAngle = newAngle
            
            if XStart > 0 and YStart > 0:
                pass
            elif XStart < 0 and YStart > 0:
                newAngle += 2*(np.pi - newAngle)
            elif XStart < 0 and YStart < 0:
                newAngle += 2*np.pi
            else:
                newAngle *= -1
                
            update_rectangle_source( baseSource.data['angle'][0] + newAngle - oldAngle )
            oldAngle = newAngle
                
        return 1
    else:
        # when node is released reset current node to -1
        # so a new node is moved next time
        velocity = (oldAngle - olderAngle) 
        
        currentNode=-1
        return -1

def construct_circle_source( center, radius, color ):
    global circleSource
            
    centerX = list()
    centerY = list()
    for i in range(len(center)):
        centerX.append(center[i][0])
        centerY.append(center[i][1])
        
    circleSource = ColumnDataSource(
                                    data=dict(
                                              x = np.array(centerX),
                                              y = np.array(centerY),
                                              radius = np.array(radius),
                                              color = np.array(color),
                                             )
                                   )
    
def construct_cross_source():
    global crossSource
    
    center = [circleSource.data['x'][0] , circleSource.data['y'][0]]



    crossSource = ColumnDataSource(
                                    data=dict(
                                              x=[center[0], center[0]],
                                              y=[center[1], center[1]],
                                              angle = np.array([0, np.pi/2])
                                             )
                                  )                                           
            
def update_cross_source( angle ):
    global crossSource
    
    crossSource.data['angle'] = 0*crossSource.data['angle'] + angle
    
def update_circle_source( centerX, centerY, radius, color ):
    global circleSource
    
    circleSource.data['x'] = 0*circleSource.data['x'] + centerX
    circleSource.data['y'] = 0*circleSource.data['y'] + centerY
    circleSource.data['radius'] = 0*circleSource.data['radius'] + radius
    circleSource.data['color'] = 0*circleSource.data['color'] + color
                                                
def get_circle_source():
    return circleSource
    
def get_cross_source():
    return crossSource

def construct_rectangle_source( center ):
    global baseSource
    
    baseSource = ColumnDataSource(
                                  data=dict(
                                            x = [center[0]],
                                            y = [center[1]],
                                            angle = [0.0]
                                           )
                                 )
                                  
def update_rectangle_source( angle ):
    global baseSource
    
    baseSource.data['angle'] = 0*baseSource.data['angle'] + [angle]
                                         
def get_rectangle_source():
    return baseSource
    
def get_velocity(objectName):
    
    if objectName == 'base':
        return velocity
    elif objectName == 'circle':
        return -velocity
    else:
        raise Exception("This rotating object doesn't exist")
        
def set_velocity(value):
    global velocity
    velocity = value