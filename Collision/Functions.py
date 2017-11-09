import matplotlib.pyplot as plt
from bokeh.models import ColumnDataSource
from MoveNodeTool import *
import numpy as np


class Particle():
    
    def __init__( self, mass, radius, color, position, velocity ):
        self.mass = mass
        self.radius = radius
        self.color = color
        self.position = position
        self.velocity = velocity
        
        # Column data sources
        self.positionInPlot = ColumnDataSource(data=dict(x=[0],y=[0]))
        self.velocityInPlot = ColumnDataSource(data=dict(xs=[0],ys=[0],xe=[0],ye=[0]))
        
    def update_position_source(self):
        self.positionInPlot.data = dict(x=[self.position[0]],y=[self.position[1]])
        
    def update_position(self, x, y):
        self.position[0] = x
        self.position[1] = y
        self.update_position_source()

    def construct_velocity_source(self):
        arrowTailPosition = np.array([ 
                                      self.positionInPlot.data['x'][0],
                                      self.positionInPlot.data['y'][0]
                                    ])
        arrowHeadPosition = np.array([
                                      self.positionInPlot.data['x'][0]+self.velocity[0],
                                      self.positionInPlot.data['y'][0]+self.velocity[1]
                                    ])
        self.velocityInPlot =  ColumnDataSource(
                                                  data=dict(
                                                            xs=[arrowTailPosition[0]],
                                                            ys=[arrowTailPosition[1]],
                                                            xe=[arrowHeadPosition[0]],
                                                            ye=[arrowHeadPosition[1]]
                                                           )
                                               )
        
    def update_velocity_source(self):
        arrowTailPosition = np.array([ 
                                      self.positionInPlot.data['x'][0],
                                      self.positionInPlot.data['y'][0]
                                    ])
        arrowHeadPosition = np.array([
                                      self.positionInPlot.data['x'][0]+self.velocity[0],
                                      self.positionInPlot.data['y'][0]+self.velocity[1]
                                    ])
        self.velocityInPlot.data = dict(
                                         xs=[arrowTailPosition[0]],
                                         ys=[arrowTailPosition[1]],
                                         xe=[arrowHeadPosition[0]],
                                         ye=[arrowHeadPosition[1]]
                                       ) 
        
    def update_velocity(self, vx, vy):
        self.velocity[0] = vx
        self.velocity[1] = vy
        self.update_velocity_source()

    def get_position_source(self):
        return self.positionInPlot
        
    def get_velocity_source(self):
        return self.velocityInPlot
        
class CollidingSystem():
    
    def __init__(self, domain, particles):
        self.particles = particles
        
        self.domain = domain # in form [[xmin,xmax],[ymin,ymax]]
        
        self.currentNode = -1
        
    def modify_location(self, click_position):
        
        self.currentNode = self.inNode(click_position)
        particleRadius = self.particles[0].radius
        # if the clicking happened over one of the particels (currentNode != -1)
        if (self.currentNode != -1):
            if abs(click_position.x+particleRadius-self.domain[0][1]) <= particleRadius or abs(click_position.x-particleRadius-self.domain[0][0]) <= particleRadius:
                pass
            elif abs(click_position.y+particleRadius-self.domain[1][1]) <= particleRadius or abs(click_position.y-particleRadius-self.domain[1][0]) <= particleRadius:
                pass
            else:
                # update node position
                self.particles[self.currentNode].update_position(click_position.x, click_position.y)

                self.particles[self.currentNode].update_velocity_source()
                    
        return 1 
        
    def inNode(self, click_position):
        counter = 0
        for particle in self.particles:
            if (abs(click_position.x-particle.position[0])<=particle.radius and abs(click_position.y-particle.position[1])<=particle.radius):
                    return counter
            counter += 1
        return -1
        
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