from bokeh.models import ColumnDataSource
from math import floor
import numpy as np


class Collision_Particle():
    
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
        self.positionInPlot.stream(dict(x=[self.position[0]],y=[self.position[1]]),rollover=1)
        
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
        self.velocityInPlot.stream(dict(
                                         xs=[arrowTailPosition[0]],
                                         ys=[arrowTailPosition[1]],
                                         xe=[arrowHeadPosition[0]],
                                         ye=[arrowHeadPosition[1]]
                                       ),rollover=1)
        
    def update_velocity(self, vx, vy):
        self.velocity[0] = vx
        self.velocity[1] = vy
        self.update_velocity_source()

    def get_direction(self):
        direction = floor(np.arctan2(self.velocity[1],self.velocity[0])/np.pi*180)
        if direction < 0:
            direction += 360
        return direction

    def get_velocity_magnitude(self):
        velocityMagnitude = np.sqrt( np.dot(self.velocity, self.velocity))
        return round(velocityMagnitude,1)

    def get_position_source(self):
        return self.positionInPlot
        
    def get_velocity_source(self):
        return self.velocityInPlot
        
class Collision_CollidingSystem():
    
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
