import matplotlib.pyplot as plt
from bokeh.models import ColumnDataSource
from MoveNodeTool import *
import numpy as np

'''
The particleSource, particleXPos, particleYPos are stored in this file because
they are used extensively by the functions inNode() and modify_location(), and
this use cannot be achieved without storing them here.
'''
                  
arrowsSource = list()

particlesXPos = [0,0]
particlesYPos = [0,0]

particleRadius = 0.5
xMin, xMax = 0,10
yMin, yMax = 0,10

currentNode=-1

rotatingWheelSource = list()
rotatingBaseSource  = 0
    
'''
The functions inNode() and modify_location() are concerned with the 
functionality of changing the position of the particle (ball) using the mouse.
For more information, get in touch with Emily Bourne, whom I got this code from.
'''
# find index of node in which coordinates are found
# (return -1 if not in a node)
def inNode (xPos,yPos):
    
    for i in range(0,len(particlesXPos)):
        if (abs(xPos-particlesXPos[i])<=0.3 and abs(yPos-particlesYPos[i])<=0.3):
                return i        
    return -1

# modify path by dragging nodes
def modify_location(attr, old, new):
    
    global currentNode, particlesSource, particlesXPos, particlesYPos
    
    # if there is a previous node (not first time the function is called)
    # and the node has not been released (new['x']=-1 on release to prepare for future calls)
    if (len(old)==1 and new[0][u'x']!=-1):
        # if first call for this node
        if (currentNode==-1):
            # determine which node and remember it
            XStart=old[0][u'x']
            YStart=old[0][u'y']

            currentNode =inNode(XStart,YStart)

        # if not first call then move node
        if (currentNode!=-1):
            if abs(new[0][u'x']+particleRadius-xMax) <= particleRadius or abs(new[0][u'x']-particleRadius-xMin) <= particleRadius:
                pass
            elif abs(new[0][u'y']+particleRadius-yMax) <= particleRadius or abs(new[0][u'y']-particleRadius-yMin) <= particleRadius:
                pass
            else:
                # update node position
                particlesSource[currentNode].data=dict(x=[new[0][u'x']],y=[new[0][u'y']])
                particlesXPos[currentNode]=new[0][u'x']
                particlesYPos[currentNode]=new[0][u'y']

                velocity = np.array([
                                    arrowsSource[currentNode].data['xe'][0] - arrowsSource[currentNode].data['xs'][0],
                                    arrowsSource[currentNode].data['ye'][0] - arrowsSource[currentNode].data['ys'][0]
                                   ])

                update_arrow_source(
                                    currentNode,
                                    particlesSource[currentNode],
                                    velocity
                                   )
                
        return 1
    else:
        # when node is released reset current node to -1
        # so a new node is moved next time
        currentNode=-1
        return -1

def construct_circle_source( center, radius ):
    global rotatingWheelSource
    
    rotatingWheelSource.append(
                               ColumnDataSource(
                                                data=dict(
                                                          x = [center[0]],
                                                          y = [center[1]],
                                                          r = [radius]
                                                         )
                                               )
                              )
    
def construct_wedges_source( radius ):
    global rotatingWheelSource
    
    center = [rotatingWheelSource[0].data['x'][0] , rotatingWheelSource[0].data['y'][0]]

    offset = 0.2
    center1 = [center[0]+offset , center[1]+offset]
    center2 = [center[0]-offset , center[1]+offset]
    center3 = [center[0]-offset , center[1]-offset]
    center4 = [center[0]+offset , center[1]-offset]

    rotatingWheelSource.append(
                               ColumnDataSource(
                                                data=dict(
                                                          x=[center1[0],center2[0],center3[0],center4[0]],
                                                          y=[center1[1],center2[1],center3[1],center4[1]],
                                                          start_angle=[0.0, np.pi/2, np.pi, 3*np.pi/2],
                                                          end_angle=[np.pi/2, np.pi, 3*np.pi/2, 0.0]
                                                         )
                                               )
                              )
                                                
def update_wedges_source( centerX, centerY, startAngle, endAngle ):
    global rotatingWheelSource
    
    rotatingWheelSource[1].data = dict(
                                        x = centerX,
                                        y = centerY,
                                        start_angle = startAngle,
                                        end_angle   = endAngle
                                      )
    
                                            
def get_circle_source():
    return rotatingWheelSource[0]
    
def get_wedges_source():
    return rotatingWheelSource[1]

def construct_rectangle_source( center ):
    global rotatingBaseSource
    
    rotatingBaseSource = ColumnDataSource(
                                          data=dict(
                                                    x = [center[0]],
                                                    y = [center[1]],
                                                   )
                                         )
                                         
def get_rectangle_source():
    return rotatingBaseSource

def push_away( caseID, particleID, amount ):
    global particlesXPos, particlesYPos
    '''
    Case ID represents which case the particle is facing right now. The case
    are listed as follows:
        ID = 1: particle is going to exceed the xMin border
        ID = 2: particle is going to exceed the xMax border
        ID = 3: particle is going to exceed the yMin border
        ID = 4: particle is going to exceed the yMax border
    '''
    if caseID == 1:
        particlesXPos[particleID] = particlesXPos[particleID] + amount
        particlesSource[currentNode].data['x'] = [particlesSource[currentNode].data['x'][0] + amount]
    elif caseID == 2:
        particlesXPos[particleID] = particlesXPos[particleID] - amount
        particlesSource[currentNode].data['x'] = [particlesSource[currentNode].data['x'][0] - amount]
    elif caseID == 3:
        particlesYPos[particleID] = particlesYPos[particleID] + amount
        particlesSource[currentNode].data['y'] = [particlesSource[currentNode].data['y'][0] + amount]
    else:
        particlesYPos[particleID] = particlesYPos[particleID] - amount
        particlesSource[currentNode].data['y'] = [particlesSource[currentNode].data['y'][0] - amount]