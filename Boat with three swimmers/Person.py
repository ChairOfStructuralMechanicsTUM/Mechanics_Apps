import numpy as np

class Person():
    
    def __init__( self, number, mass, standingShape, jumpingShape ):
        self.n = number
        self.mass = mass
        self.standingShape = standingShape
        self.jumpingShape  = jumpingShape
        
    def get_number(self):
        return self.n
        
    def get_mass(self):
        return self.mass
        
    def get_standingShape(self):
        return self.standingShape
        
    def get_jumpingShape(self):
        return self.jumpingShape

def create_default_person(N, initBoatCGx, initBoatCGy, L, personOneX, personOneY):
    print('a default person has been created')
    mass     = 75                             # Masses of the poeple on board
    #jumpSpeed = 0.25                               # Speed with respect to the moving boat
    
    listPeople = list()
    for i in range(N):
        listPeople.append( Person( 0,mass,[personOneX,personOneY] , [personOneX,personOneY] ) )
    
    return listPeople

def update_source(source,newPerson):
    print('the source has been updated')
    standingShape = newPerson.get_standingShape()
    source.data['x'].append(standingShape[0])
    source.data['y'].append(standingShape[1])
    source.data['c'].append('#FF33FF')
    
    print('source length now is : ', len(source.data['c']))