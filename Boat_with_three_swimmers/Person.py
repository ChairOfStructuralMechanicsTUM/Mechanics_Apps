import numpy as np
from bokeh.plotting import ColumnDataSource
from bokeh.models import Arrow, OpenHead, LabelSet, Label

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

    mass = 75.0
    
    if N == 1:
        separatingDistance = 0.0
    else:
        separatingDistance = (L-1.0)/(float(N)-1.0)

    standingShiftingList = np.ones((N,28))
    jumpingShiftingList = np.ones((N,29))
    
    distanceList = np.zeros(N)
    
    counter = float(N)/2.0 - 0.5 
    for i in range(0,N):
        distanceList[i] += float(counter)
        counter -= 1
        
    for i in range(0,N):
        for j in range(0,28):
            standingShiftingList[i,j] = distanceList[i] *separatingDistance
        for j in range(0,29):
            jumpingShiftingList[i,j] = distanceList[i] *separatingDistance
            
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
    
def create_arrows_velocityDiagram( diagram, colors, boatSpeed ):
    # Create arrows for the boat
    boatArrows_sources = list()
    boatArrows_intities = list()
    
    boatColors = ['#000000']+colors
    for i in range(0,6):
        boatArrows_sources.append(ColumnDataSource(data=dict(xs=[5],ys=[0],xe=[5],ye=[0])))
        boatArrows_intities.append(
                                   Arrow(    
                                            end=OpenHead(
                                                         line_color=boatColors[i],
                                                         line_width=3,
                                                         size=5
                                                        ),
                                            x_start=['xs'][0],
                                            y_start=['ys'][0],
                                            x_end=['xe'][0], 
                                            y_end=['ye'][0], 
                                            line_color=boatColors[i],
                                            source=boatArrows_sources[i]
                                        ) 
                                  )
        diagram.add_layout( boatArrows_intities[i] )                      
        
    boatArrows_sources[0].data = dict(
                                        xs=[5],ys=[0],xe=[5],ye=[boatSpeed]
                                     )
                                            
    # Create arrows for the swimmers
    swimmerArrows_sources = list()
    swimmerArrows_intities = list()
    
    for i in range(0,5):
        xPos = float(i*5+10)
        swimmerArrows_sources.append(
                                     [ ColumnDataSource(data=dict(xs=[xPos],ys=[boatSpeed],xe=[xPos],ye=[boatSpeed])),
                                       ColumnDataSource(data=dict(xs=[xPos+0.5],ys=[0],xe=[xPos+0.5],ye=[0])),
                                       ColumnDataSource(data=dict(xs=[xPos-0.5],ys=[0],xe=[xPos-0.5],ye=[boatSpeed])) ]
                                    )
        
        relativeVelocityArrow = Arrow(    
                                            end=OpenHead(
                                                         line_color="#FFCC00",
                                                         line_width=3,
                                                         size=5
                                                        ),
                                            x_start=['xs'][0],
                                            y_start=['ys'][0],
                                            x_end=['xe'][0], 
                                            y_end=['ye'][0], 
                                            line_color = "#FFCC00",
                                            source=swimmerArrows_sources[i][0]
                                        ) 
        absoluteVelocityArrow = Arrow(    
                                            end=OpenHead(
                                                         line_color=colors[i],
                                                         line_width=3,
                                                         size=5
                                                        ),
                                            x_start=['xs'][0],
                                            y_start=['ys'][0],
                                            x_end=['xe'][0], 
                                            y_end=['ye'][0],
                                            line_color=colors[i],
                                            source=swimmerArrows_sources[i][1]
                                        ) 
                                            
        startingVelocityArrow = Arrow(    
                                            end=OpenHead(
                                                         line_color="#000000",
                                                         line_width=3,
                                                         size=5
                                                        ),
                                            x_start=['xs'][0],
                                            y_start=['ys'][0],
                                            x_end=['xe'][0], 
                                            y_end=['ye'][0], 
                                            line_color = "#000000",
                                            source=swimmerArrows_sources[i][2]
                                        ) 
                                            
        swimmerArrows_intities.append( [relativeVelocityArrow, absoluteVelocityArrow, startingVelocityArrow] )
                                            
        diagram.add_layout( relativeVelocityArrow )
        diagram.add_layout( absoluteVelocityArrow )
        diagram.add_layout( startingVelocityArrow )
    
    # Create labels for both the boat and the swimmers
    diagram.add_layout( Label(
                                  x=5, y=-2,
                                  text='Boat',
                                  text_color='black',text_font_size="8pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                              ))
    diagram.add_layout( Label(
                                  x=10, y=-2,
                                  text='Black Swimmer',
                                  text_color='black',text_font_size="8pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                              ))
    diagram.add_layout( Label(
                                  x=15, y=-2,
                                  text='Red Swimmer',
                                  text_color='black',text_font_size="8pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                              ))
    diagram.add_layout( Label(
                                  x=20, y=-2,
                                  text='Orange Swimmer',
                                  text_color='black',text_font_size="8pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                              ))
    diagram.add_layout( Label(
                                  x=25, y=-2,
                                  text='Blue Swimmer',
                                  text_color='black',text_font_size="8pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                              ))
    diagram.add_layout( Label(
                                  x=30, y=-2,
                                  text='Grey Swimmer',
                                  text_color='black',text_font_size="8pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                              ))
    '''
    swimmersLabels = list()
    for i in range(0,5):
        xPos = i*5+10
        swimmersLabels.append(
                               LabelSet(
                                          x=xPos, y=-2,
                                          text='f',
                                          text_color='black',text_font_size="15pt",
                                          level='glyph',text_baseline="middle",text_align="center",
                                       )
                             )
        diagram.add_layout( swimmersLabels[i] )
    '''
    return boatArrows_sources, swimmerArrows_sources
        
def reset_arrows_velocityDiagram( boatArrows_sources, swimmerArrows_sources, boatSpeed ):
    for i in range(0,6):
        boatArrows_sources[i].data=dict(xs=[5],ys=[0],xe=[5],ye=[0])
        
    boatArrows_sources[0].data = dict(
                                    xs=[5],ys=[0],xe=[5],ye=[boatSpeed]
                                 )
    
    for i in range(0,5):
        xPos = float(i*5+10)
        swimmerArrows_sources[i][0].data=dict(xs=[xPos],ys=[boatSpeed],xe=[xPos],ye=[boatSpeed])
        swimmerArrows_sources[i][1].data=dict(xs=[xPos+0.5],ys=[0],xe=[xPos+0.5],ye=[0])
        swimmerArrows_sources[i][2].data=dict(xs=[xPos-0.5],ys=[0],xe=[xPos-0.5],ye=[boatSpeed])
        
def modify_swimmer_arrows( boatArrows_sources, swimmerArrows_sources, swimmer, velocityIncrease, boatSpeed ):
    currentBoatSpeed = boatSpeed

    # Modify the swimmer's arrows
    position = float(swimmer.n*5 + 10)
    
    swimmerArrows_sources[swimmer.n][0].data = dict(
                                                    xs = [position],
                                                    ys = [currentBoatSpeed],
                                                    xe = [position],
                                                    ye = [currentBoatSpeed - swimmer.relativeVelocity[0]]
                                                   )
    
    swimmerArrows_sources[swimmer.n][1].data = dict(
                                                    xs = [position+0.5],
                                                    ys = [0],
                                                    xe = [position+0.5],
                                                    ye = [currentBoatSpeed - swimmer.relativeVelocity[0]]
                                                  )
    
    swimmerArrows_sources[swimmer.n][2].data = dict(
                                                    xs = [position-0.5],
                                                    ys = [0],
                                                    xe = [position-0.5],
                                                    ye = [currentBoatSpeed]
                                                   )
    
    for i in range(0,5):
        if i > swimmer.n:
            position = float(i*5 + 10)
            swimmerArrows_sources[i][2].data = dict(
                                                    xs = [position-0.5],
                                                    ys = [0],
                                                    xe = [position-0.5],
                                                    ye = [currentBoatSpeed]
                                                   )
            swimmerArrows_sources[i][0].data = dict(
                                                    xs = [position],
                                                    ys = [currentBoatSpeed],
                                                    xe = [position],
                                                    ye = [currentBoatSpeed]
                                                   )
        else:
            pass

    # Modify the boat's arrow
    boatArrows_sources[swimmer.n + 1].data = dict(
                                                    xs = [5],
                                                    ys = [boatArrows_sources[swimmer.n].data['ye'][0]],
                                                    xe = [5],
                                                    ye = [boatArrows_sources[swimmer.n].data['ye'][0] + velocityIncrease]
                                                 )