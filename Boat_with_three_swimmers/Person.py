import numpy as np
from bokeh.plotting import ColumnDataSource

class Person():
    
    def __init__( self, number, mass, standingPosition, jumpingPosition ):
        self.n = number
        self.mass = mass
        self.standingPosition = standingPosition
        self.jumpingPosition  = jumpingPosition
        self.currentPosition = self.standingPosition
        self.jumping = False
        self.relativeVelocity = [3,3]
        self.jumpingPath = dict(x=[],y=[])
        
    def get_number(self):
        return self.n
        
    def get_mass(self):
        return self.mass
        
    def get_standingShape(self):
        return self.standingPosition
        
    def get_jumpingShape(self):
        return self.jumpingPosition

def create_people(
                      N,
                      initBoatCGx,
                      initBoatCGy,
                      L,
                      standingPositionX, standingPositionY,
                      jumpingPositionX, jumpingPositionY
                 ):

    mass = 75
    
    if N == 1:
        separatingDistance = 0
    else:
        separatingDistance = (L-1)/(N-1)
    standingShiftingList = np.ones((N,28))
    jumpingShiftingList = np.ones((N,29))
    
    distanceList = np.zeros(N)
    
    counter = N/2 - 0.5 
    for i in range(0,N):
        distanceList[i] += counter
        counter -= 1
    for i in range(0,N):
        standingShiftingList[i,:] *= distanceList[i] *separatingDistance
        jumpingShiftingList[i,:] *= distanceList[i] *separatingDistance
            
    listPeople = list()
    for i in range(N):
        listPeople.append( Person( 
                                      i, 
                                      mass, 
                                      [standingPositionX+standingShiftingList[i,:],standingPositionY],
                                      [jumpingPositionX+jumpingShiftingList[i,:] , jumpingPositionY]
                         )       )
    
    return listPeople

def update_source(source,newPerson):
    print('the source has been updated')
    standingShape = newPerson.get_standingShape()
    source.data['x'].append(standingShape[0])
    source.data['y'].append(standingShape[1])
    source.data['c'].append('#FF33FF')
    
    print('source length now is : ', len(source.data['c']))