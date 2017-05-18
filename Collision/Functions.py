import matplotlib.pyplot as plt
from bokeh.models import ColumnDataSource
from MoveNodeTool import *
import numpy as np

'''
The particleSource, particleXPos, particleYPos are stored in this file because
they are used extensively by the functions inNode() and modify_location(), and
this use cannot be achieved without storing them here.
'''
particlesSource = [
                   ColumnDataSource(data=dict(x=[0],y=[0])),
                   ColumnDataSource(data=dict(x=[0],y=[0]))
                  ]
                  
arrowsSource = list()

particlesXPos = [0,0]
particlesYPos = [0,0]

particleRadius = 0.5
xMin, xMax = 0,10
yMin, yMax = 0,10

currentNode=-1
    
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

'''
The following six functions are constructed here in order to pass the export 
particle source file here to the main file, and to reduce the number of lines
in the main file as well
'''
def update_particle_source(ID,x,y):
    global particlesXPos, particlesYPos, particlesSource

    particlesXPos[ID]=x
    particlesYPos[ID]=y
    particlesSource[ID].data = dict(x=[x],y=[y])

def get_particle_source(ID):
    return particlesSource[ID]

def update_particle_position(ID,x,y):
    global particlesXPos, particlesYPos
    particlesXPos[ID] = x
    particlesYPos[ID] = y

def get_arrow_source(ID):
    return arrowsSource[ID]
    
def construct_arrow_source(ID, tailPosition, tailHeadDistance ):
    global arrowsSource
    
    arrowTailPosition = np.array([ 
                                  tailPosition.data['x'][0],
                                  tailPosition.data['y'][0]
                                ])
    arrowHeadPosition = np.array([
                                  tailPosition.data['x'][0]+tailHeadDistance[0],
                                  tailPosition.data['y'][0]+tailHeadDistance[1]
                                ])
    arrowsSource.append( ColumnDataSource(
                                          data=dict(
                                                    xs=[arrowTailPosition[0]],
                                                    ys=[arrowTailPosition[1]],
                                                    xe=[arrowHeadPosition[0]],
                                                    ye=[arrowHeadPosition[1]]
                                                   )
                       )                  )

def update_arrow_source( ID, tailPosition, tailHeadDistance ):
    global arrowsSource
    
    arrowTailPosition = np.array([ 
                                  tailPosition.data['x'][0],
                                  tailPosition.data['y'][0]
                                ])
    arrowHeadPosition = np.array([
                                  tailPosition.data['x'][0]+tailHeadDistance[0],
                                  tailPosition.data['y'][0]+tailHeadDistance[1]
                                ])
    arrowsSource[ID].data = dict(
                                 xs=[arrowTailPosition[0]],
                                 ys=[arrowTailPosition[1]],
                                 xe=[arrowHeadPosition[0]],
                                 ye=[arrowHeadPosition[1]]
                                ) 

    
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