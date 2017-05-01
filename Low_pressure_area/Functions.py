import matplotlib.pyplot as plt
from bokeh.models import ColumnDataSource
from MoveNodeTool import *
import numpy as np

'''
The particleSource, particleXPos, particleYPos are stored in this file because
they are used extensively by the functions inNode() and modify_location(), and
this use cannot be achieved without storing them here.
This piece of code responsible for the contour plot has been brough from the 
user: http://stackoverflow.com/users/5158031/br123
'''
particleSource = ColumnDataSource(data=dict(x=[],y=[]))
particleXPos = [0]
particleYPos = [0]
currentNode=-1

def get_contour_data(X, Y, Z):
    cs = plt.contour(X, Y, Z)
    xs = []
    ys = []
    xt = []
    yt = []
    col = []
    text = []
    isolevelid = 0
    for isolevel in cs.collections:
        isocol = isolevel.get_color()[0]
        thecol = 3 * [None]
        theiso = str(cs.get_array()[isolevelid])
        isolevelid += 1
        for i in range(3):
            thecol[i] = int(255 * isocol[i])
        thecol = '#%02x%02x%02x' % (thecol[0], thecol[1], thecol[2])

        for path in isolevel.get_paths():
            v = path.vertices
            x = v[:, 0]
            y = v[:, 1]
            xs.append(x.tolist())
            ys.append(y.tolist())
            xt.append(x[int( len(x) / 2 )])
            yt.append(y[int( len(y) / 2 )])
            text.append(theiso)
            col.append(thecol)

    source = ColumnDataSource(
                              data={
                                    'xs': xs, 
                                    'ys': ys, 
                                    'line_color': col,
                                    'xt':xt,
                                    'yt':yt,
                                    'text':text
                                   }
                             )
    return source
    
'''
This function gets for a certain position of the ball within the plot its 
corresponding index within the position grid created in the main file under
the name X, Y
'''
def get_index( position, Xgrid, Ygrid ):
    # finding the x position index
    xPosIndex,yPosIndex = 0,0
    percentageX, percentageY = 0,0
    counter = 0
    for i in Xgrid[0,:]:
        if i == Xgrid[0,-1]:
            pass
        
        elif position[0] >= Xgrid[0,counter] and position[0] < Xgrid[0,counter+1]:
            xPosIndex = counter
            
            # If the actual position is in between the two coordinate points
            # I am comparing with, the following line will indicate a   
            # percentage of how this position is situated in between
            percentageX = (position[0] - Xgrid[0,counter]) / (Xgrid[0,counter+1] - Xgrid[0,counter])
           
        counter += 1
        
    # finding the y position index
    counter = 0
    for i in Ygrid[:,0]:
        if i == Ygrid[-1,0]:
            pass
        
        elif position[1] >= Ygrid[counter,0] and position[1] < Ygrid[counter+1,0]:
            yPosIndex = counter
            percentageY = (position[1] - Ygrid[counter,0]) / (Ygrid[counter+1,0] - Ygrid[counter,0])
         
        counter += 1
        
    return xPosIndex, yPosIndex, percentageX, percentageY
    
'''
This function calculates the pressure gradient based on the indeces determined
by the get_index() function; furthermore, it considers the percentages retuned
by get_index() in order to do linear interpolation and gets an accurate 
continuous determination of the actual pressure gradient at that specific 
location (which is determined by the indeces)
'''
def get_pressure_grad( position, Xgrid, Ygrid, presGrad ):
    
    xPosIndex, yPosIndex, percentageX, percentageY= get_index( position, Xgrid, Ygrid )
    
    presGrad00 = presGrad[ xPosIndex][yPosIndex ]
    presGrad10 = presGrad[ xPosIndex+1][yPosIndex ]
    presGrad01 = presGrad[ xPosIndex][yPosIndex+1 ]
    presGrad11 = presGrad[ xPosIndex+1][yPosIndex+1 ]

    # Linear interpolation formula
    presGradActual = (
                       presGrad00 * (1-percentageX) * (1-percentageY)
                     + presGrad10 * (percentageX  ) * (1-percentageY)
                     + presGrad01 * (1-percentageX) * (percentageY  )
                     + presGrad11 * (percentageX  ) * (percentageY  )
                     )
    
    return presGradActual
    
'''
The functions inNode() and modify_location() are concerned with the 
functionality of changing the position of the particle (ball) using the mouse.
For more information, get in touch with Emily Bourne, whom I got this code from.
'''
# find index of node in which coordinates are found
# (return -1 if not in a node)
def inNode (xPos,yPos):
    global particleXPos, particleYPos
    for i in range(0,len(particleXPos)):
        if (abs(xPos-particleXPos[i])<=0.1 and abs(yPos-particleYPos[i])<=0.1):
            return i
    return -1

# modify path by dragging nodes
def modify_location(attr, old, new):

    global currentNode, particleSource, particleXPos, particleYPos
    # if there is a previous node (not first time the function is called)
    # and the node has not been released (new['x']=-1 on release to prepare for future calls)
    if (len(old)==1 and new[0][u'x']!=-1):
        # if first call for this node
        if (currentNode==-1):
            # determine which node and remember it
            XStart=old[0][u'x']
            YStart=old[0][u'y']
            currentNode=inNode(XStart,YStart)
        # if not first call then move node
        if (currentNode!=-1):
            # update node position
            particleSource.data=dict(x=[new[0][u'x']],y=[new[0][u'y']])
            particleXPos[currentNode]=new[0][u'x']
            particleYPos[currentNode]=new[0][u'y']
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
def update_particle_source(x,y):
    global particleXPos, particleYPos, particleSource
    #print('update_particle_positions() has been accessed')
    particleXPos[0]=x
    particleYPos[0]=y
    particleSource.data = dict(x=[x],y=[y])

def get_particle_source():
    return particleSource

def update_particle_position(x,y):
    global particleXPos, particleYPos
    particleXPos[0] = x
    particleYPos[0] = y

def get_particle_position():
    return np.array([ particleXPos[0] , particleYPos[0] ])
    
def construct_arrow_source( tailPosition, tailHeadDistance ):
    arrowTailPosition = np.array([ 
                                  tailPosition.data['x'][0],
                                  tailPosition.data['y'][0]
                                ])
    arrowHeadPosition = np.array([
                                  tailPosition.data['x'][0]+tailHeadDistance[0],
                                  tailPosition.data['y'][0]+tailHeadDistance[1]
                                ])
    arrowSource = ColumnDataSource(
                                   data=dict(
                                             xs=[arrowTailPosition[0]],
                                             ys=[arrowTailPosition[1]],
                                             xe=[arrowHeadPosition[0]],
                                             ye=[arrowHeadPosition[1]]
                                            )
                                  ) 
    return arrowSource
    
def update_arrow_source( tailPosition, tailHeadDistance ):
    arrowTailPosition = np.array([ 
                                  tailPosition.data['x'][0],
                                  tailPosition.data['y'][0]
                                ])
    arrowHeadPosition = np.array([
                                  tailPosition.data['x'][0]+tailHeadDistance[0],
                                  tailPosition.data['y'][0]+tailHeadDistance[1]
                                ])
    arrowSourceData = dict(
                             xs=[arrowTailPosition[0]],
                             ys=[arrowTailPosition[1]],
                             xe=[arrowHeadPosition[0]],
                             ye=[arrowHeadPosition[1]]
                          ) 
    return arrowSourceData