import matplotlib.pyplot as plt
from bokeh.models import ColumnDataSource
from MoveNodeTool import *
import numpy as np

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

    source = ColumnDataSource(data={'xs': xs, 'ys': ys, 'line_color': col,'xt':xt,'yt':yt,'text':text})
    return source
    
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
            # I am comparing with, the next line will indicate a percentage  
            # how this position is situated between
            percentageX = (position[0] - Xgrid[0,counter]) / (Xgrid[0,counter+1] - Xgrid[0,counter])
            #print('percentageX = ',percentageX)
        else:
            pass
        counter += 1
        
    # finding the y position index
    counter = 0
    for i in Ygrid[:,0]:
        if i == Ygrid[-1,0]:
            pass
        elif position[1] >= Ygrid[counter,0] and position[1] < Ygrid[counter+1,0]:
            yPosIndex = counter
            
            percentageY = (position[1] - Ygrid[counter,0]) / (Ygrid[counter+1,0] - Ygrid[counter,0])
            #print('percentageY = ',percentageY)
        else:
            pass
        counter += 1
        
    return xPosIndex, yPosIndex, percentageX, percentageY
    
def get_pressure_grad( position, Xgrid, Ygrid, presGrad ):
    
    xPosIndex, yPosIndex, percentageX, percentageY= get_index( position, Xgrid, Ygrid )
    
    presGrad00 = presGrad[ xPosIndex][yPosIndex ]
    presGrad10 = presGrad[ xPosIndex+1][yPosIndex ]
    presGrad01 = presGrad[ xPosIndex][yPosIndex+1 ]
    presGrad11 = presGrad[ xPosIndex+1][yPosIndex+1 ]

    # Linear interpolation formula
    presGradActual = (
                      presGrad00 * (1-percentageX) * (1-percentageY)
                     +presGrad10 * (percentageX  ) * (1-percentageY)
                     +presGrad01 * (1-percentageX) * (percentageY  )
                     +presGrad11 * (percentageX  ) * (percentageY  )
                     )
    
    return presGradActual
    
# find index of node in which coordinates are found
# (return -1 if not in a node)
def inNode (xPos,yPos):
    print('inNode() has been accessed')
    print('particleXPos: ',particleXPos)
    print('particleYPos: ',particleYPos)
    global particleXPos, particleYPos
    for i in range(0,len(particleXPos)):
        if (abs(xPos-particleXPos[i])<=0.1 and abs(yPos-particleYPos[i])<=0.1):
            return i
    return -1

# modify path by dragging nodes
def modify_path(attr, old, new):
    #print('old: ',old)
    #print('new: ',new)
    #print('currentNode: ',currentNode)
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