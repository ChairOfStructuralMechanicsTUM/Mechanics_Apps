import numpy as np
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.plotting import ColumnDataSource
from bokeh.models import Button, Slider, Div
from BwtS_Person import create_people
from BwtS_Person import create_arrows_velocityDiagram, reset_arrows_velocityDiagram, modify_swimmer_arrows
from bokeh.layouts import column, row
#import BwtS_BarChart as BC
from os.path import dirname, join, split
from bokeh.models.layouts import Spacer
#from bokeh.models import Arrow, OpenHead

'''
###############################################################################
Global variables as ColumnDataSources
###############################################################################
'''
glob_active     = ColumnDataSource(data=dict(Active=[False]))
glob_callback   = ColumnDataSource(data=dict(cid=[None])) # callback id
glob_boatSpeed  = ColumnDataSource(data=dict(val=[0]))
glob_listPeople = ColumnDataSource(data=dict(List=[None]))

'''
###############################################################################
Create the plotting domain
###############################################################################
'''
xMin , xMax = 0,40
yMin , yMax = 0,10
scene = figure(
                title="Water Scene with the Boat and its Swimmers",
                x_range=(xMin,xMax),
                y_range=(yMin,yMax),width=1200, height=400,
                tools=''
              )
scene.title.align          = "center"
scene.title.text_font_size = "25px"
scene.grid.visible         = False
scene.xaxis.visible        = False
scene.yaxis.visible        = False
scene.toolbar.logo         = None

bar_chart_data = {'objects':{'boat':600,'swimmer1':150}}

velocity_diagram = figure(
                            title="Velocity Diagram",
                            x_range=(0,35),
                            y_range=(-3,7),width=700, height=300,
                            tools=''
                         )
velocity_diagram.title.align          = "center"
velocity_diagram.title.text_font_size = "25px"
velocity_diagram.grid.visible         = True
velocity_diagram.xaxis.visible        = False
velocity_diagram.yaxis.axis_label     = "Velocity (m/s)"
velocity_diagram.yaxis.visible        = True
velocity_diagram.toolbar.logo         = None

'''
###############################################################################
Define the objects to be plotted within the plotting domain
 (1) Boat
 (2) Swimmers
###############################################################################
'''
# Dynamics parameters
dt = 0.05

# Water information
waterX = np.array( [xMin,xMin,xMax,xMax] )
waterY = np.array( [yMin,yMax/3,yMax/3,yMin] )
scene.patch(waterX, waterY, color="#0073CF")

# Boat information
mass = 300.0                           # Mass of the boat
L = 6.0                                # Length of the boat
initBoatCGx = xMax - L/2             # x-coordinat of the boat's CG
initBoatCGy = yMax/3 - 0.25          # y-coordinat of the boat's CG
boatX = np.array( [
                       initBoatCGx - 2.5, 
                       initBoatCGx - 3.0, 
                       initBoatCGx + 3.0, 
                       initBoatCGx + 2.5
                  ] )                # constant
boatY = np.array( [
                       initBoatCGy - 1.0,
                       initBoatCGy + 0.5,
                       initBoatCGy + 0.5,
                       initBoatCGy - 1.0
                  ] )                # constant
startBoatSpeed = 2.0                 # constant
glob_boatSpeed.data = dict(val=[startBoatSpeed])
boatColor  = '#DAD7CB'
boatSource = ColumnDataSource(data=dict(x = boatX,
                                        y = boatY,
                                        ))
scene.patch(x = 'x', y = 'y', color= boatColor, source = boatSource)

# People information

## Create the trace of jumping swimmers list
listSources = list()
for i in range(0,6):
    listSources.append(ColumnDataSource(data=dict(x=[],y=[])))
    
N = 1                                # Number of people on the boat
jumpSpeed = 0.25                     # Speed with respect to the moving boat

x = initBoatCGx                      # Points that define the center of the 
y = 1.85+initBoatCGy+0.5             # person to be drawn by default

jumpingPositionX = np.array( [x, x, x+0.3, x+0.5, x+0.5, x+0.25, x+0.25, x+0.5, 
                              x+1.0, x+1.1, x+0.5, x+0.3, x+0.3, x+1.0, x+0.5, 
                              x+0.25, x+0.6, x+0.1, x-0.3, x-0.9, x-0.8, x-0.4,
                              x-0.15, x-0.15, x-0.4, x-0.5, x-0.7, x-0.55, x] )

jumpingPositionY = np.array( [y+1.5, y+1.8, y+2.0, y+1.8, y+1.3, y+1.3, y+1.1,
                              y+0.6, y+0.9, y+0.7, y+0.3, y+0.5, y-0.1, y-0.65,
                              y-1.4, y-1.2, y-0.7, y-0.3, y-0.9, y-0.5, y-0.2,
                              y-0.5, y, y+0.8, y+0.7, y+0.25, y+0.3, y+0.95, 
                              y+1.15] )

standingPositionX = np.array([x, x+0.2, x+0.2, x+0.1, x+0.1, x+0.5, x+0.6, 
                              x+0.5, x+0.3, x+0.25, x+0.25, x+0.15, x+0.25,
                              x+0.05, x, x-0.05, x-0.25, x-0.15, x-0.25, 
                              x-0.25, x-0.3, x-0.5, x-0.6, x-0.5, x-0.1, x-0.1,
                              x-0.2,x-0.2])

standingPositionY = np.array([y+1.25, y+1.1, y+0.75, y+0.7, y+0.6, y+0.35,
                              y-0.55, y-0.6, y+0.15, y-0.4, y-0.7, y-1.7, 
                              y-1.85, y-1.85, y-1.7, y-1.85, y-1.85, y-1.7, 
                              y-0.7, y-0.4, y+0.15, y-0.6, y-0.55, y+0.35,
                              y+0.6, y+0.7, y+0.75,y+1.1])

listPeople = create_people( 
                               N, 
                               initBoatCGx, 
                               initBoatCGy, L, 
                               standingPositionX, standingPositionY,
                               jumpingPositionX, jumpingPositionY
                          )

listXCoords = list()
listYCoords = list()
for person in listPeople:
    listXCoords.append(person.standingPosition[0])
    listYCoords.append(person.standingPosition[1])
    #listSources.append(ColumnDataSource(data=person.jumpingPath))
glob_listPeople.data = dict(List=[listPeople]) #      /output
    
swimmers_colors = ['#E37222','#A2AD00','#64A0C8','#FFDC00','#C4071B']
    
personSource = ColumnDataSource(
                                data=dict(
                                          x=listXCoords, 
                                          y=listYCoords,
                                          c=[swimmers_colors[0]]
                                         )         
                               )

scene.patches(xs='x',ys='y',color='c',source = personSource )


boatArrows_sources, swimmerArrows_sources = create_arrows_velocityDiagram(velocity_diagram, swimmers_colors, startBoatSpeed)

'''
###############################################################################
Define the function that will develope the position of the boat and swimmers
through time
###############################################################################
'''
def move_boat():
    #global listSources
    [boatSpeed]  = glob_boatSpeed.data["val"]   # input/
    [listPeople] = glob_listPeople.data["List"] # input/output
    
    # Making the boat move
    dx = np.ones(4)*dt*boatSpeed
    boatSource.data['x'] = boatSource.data['x'] - dx

    # Making the people move
    dxStandting = np.ones(28)
    dxJumping   = np.ones(29)

    newListXCoords = list()
    newListYCoords = list()
    newListColor   = personSource.data['c']
    
    for i in range(len(personSource.data['x'])):
        if listPeople[i].jumping == True:
            # Determining the new position of the person according to his/her
            # own velocity
            newListXCoords.append(
                                  personSource.data['x'][i] 
                                + dxJumping*dt*listPeople[i].relativeVelocity[0] # relativeVelocity here is the absolute velovity
                                 )
            
            newListYCoords.append(
                                  personSource.data['y'][i] 
                                + dxJumping*dt*listPeople[i].relativeVelocity[1] # relativeVelocity here is the absolute velovity
                                 )

            # Plotting the path of the jumping person
            listSources[i].stream( dict(
                                                x = [newListXCoords[i][0]],
                                                y = [newListYCoords[i][0]]
                                 )     )
            
            # Change the vertical velocity of the person due to gravity
            listPeople[i].relativeVelocity[1] -= 9.81*dt
        else:
            newListXCoords.append(
                                      personSource.data['x'][i] 
                                    - dxStandting*dt*boatSpeed
                                 )
            newListYCoords.append(personSource.data['y'][i])

    # Updating the source file that defines the people figures
    personSource.data = dict(
                                 x=newListXCoords,
                                 y=newListYCoords,
                                 c=newListColor
                            )
    glob_listPeople.data = dict(List=[listPeople])
    
'''
###############################################################################
Add the interactive functionalities
###############################################################################
'''
##################### Creating numberPeopleSlider slider ######################
def updateNoPersons(attr,old,new):
    [Active]    = glob_active.data["Active"] # input/
    [boatSpeed] = glob_boatSpeed.data["val"] # input/
    
    # If the boat is moving, new people connot be added
    if Active == False:    
        # Acount for the displacement already carried out by the boat for
        # creating the new people on board
        displacement = ( boatX[2] - boatSource.data['x'][2] )
        dxStanding   = displacement * np.ones(28)
        dxJumping    = displacement * np.ones(29)
        
        # Creating people on the boat
        listPeople = create_people(
                                       new,
                                       initBoatCGx,
                                       initBoatCGy,
                                       L,
                                       standingPositionX - dxStanding, 
                                       standingPositionY,
                                       jumpingPositionX - dxJumping, 
                                       jumpingPositionY
                                  )  
        
        # Addinig the newly created people on board in the poeple source data 
        # file
        listXCoords = list()
        listYCoords = list()
        listColors  = list()
        counter = 0
        for person in listPeople:
            listXCoords.append(person.currentPosition[0])
            listYCoords.append(person.currentPosition[1])
            listColors.append(swimmers_colors[counter])
            counter += 1
        personSource.data    = dict(x=listXCoords, y=listYCoords,c=listColors) #      /output
        glob_listPeople.data = dict(List=[listPeople])                         #      /output
            
        reset_arrows_velocityDiagram( boatArrows_sources, swimmerArrows_sources, boatSpeed )
            
    else:
        pass
    
numberPersonsSlider = Slider(
                                 title=u" Number of swimmers on board ", 
                                 value=1, start=1, end=5, step=1,width=300
                            )
numberPersonsSlider.on_change('value',updateNoPersons)




########################### Creating pause button #############################
#def pause ():
#    global Active
#    # When active pause animation
#    if Active == True:
#        curdoc().remove_periodic_callback(move_boat)
#        Active=False
#    else:
#        pass
#        
#pause_button = Button(label="Pause", button_type="success")
#pause_button.on_click(pause)

########################### Creating play button ##############################
def play():
    [Active]                  = glob_active.data["Active"] # input/output
    [g1Boatwiththreeswimmers] = glob_callback.data["cid"]  # input/output
    # if inactive, reactivate animation
    if Active == True:
        jump_button.disabled = True
        g1Boatwiththreeswimmers=curdoc().remove_periodic_callback(g1Boatwiththreeswimmers)
        glob_active.data   = dict(Active=[False])
        glob_callback.data = dict(cid=[g1Boatwiththreeswimmers])
        play_button.label  = "Play"
    else:
        jump_button.disabled = False
        g1Boatwiththreeswimmers=curdoc().add_periodic_callback(move_boat, 50)
        glob_active.data   = dict(Active=[True])
        glob_callback.data = dict(cid=[g1Boatwiththreeswimmers])
        play_button.label  = "Pause"
    #update_bars()

play_button = Button(label="Play", button_type="success")
play_button.on_click(play)

########################### Creating reset button #############################
def reset():
    #global listSources
    [Active] = glob_active.data["Active"] # input/output
    
    for element in listSources:
        element.data = dict(x=[],y=[])
    
    # Make the app inactive and stop the ap from running
    if Active == False:
        pass
    else:
        [g1Boatwiththreeswimmers] = glob_callback.data["cid"]  # input/
        curdoc().remove_periodic_callback(g1Boatwiththreeswimmers)
        glob_active.data = dict(Active=[False])

    #Reset Play Button
    play_button.label = "Play"

    # Reset the coordinates defining the boat in its source data file
    boatSource.data     = dict(x = boatX, y = boatY)
    glob_boatSpeed.data = dict(val=[startBoatSpeed]) #      /output
    
    reset_arrows_velocityDiagram( boatArrows_sources, swimmerArrows_sources, startBoatSpeed )
    

    # Creating a new list of people with only one person as default
    listPeople = create_people(
                                   numberPersonsSlider.value,
                                   initBoatCGx,
                                   initBoatCGy,
                                   L,
                                   standingPositionX, standingPositionY,
                                   jumpingPositionX, jumpingPositionY
                              )    
        
    # Reseting the data inside the people source file 
    listXCoords = list()
    listYCoords = list()
    listColors  = list()
    counter = 0
    for person in listPeople:
        listXCoords.append(person.currentPosition[0])
        listYCoords.append(person.currentPosition[1])
        listColors.append(swimmers_colors[counter])
        counter += 1
    personSource.data    = dict(x=listXCoords, y=listYCoords,c=listColors) #      /output
    glob_listPeople.data = dict(List=[listPeople])                         #      /output
        
reset_button = Button(label="Reset", button_type="success")
reset_button.on_click(reset)

########################### Creating jump button ##############################
def jump():
    [Active]     = glob_active.data["Active"]   # input/
    [boatSpeed]  = glob_boatSpeed.data["val"]   # input/output
    [listPeople] = glob_listPeople.data["List"] # input/
    
    if Active == True:
        counter = 0
        for person in listPeople:
            #print("DBUG: counter = ", counter)
            if person.jumping == True:
                pass
            else:
                person.jumping = True
                # Change the speed of the boat
                people_still_onboard = 0
                for swimmer in listPeople:
                    if swimmer.jumping == False:
                        people_still_onboard += 1
                    else:
                        pass

                # calculate the increase in the boat velocity after the swimmer jumps
                velocity_increase = person.mass*person.relativeVelocity[0] / (person.mass*people_still_onboard + mass)
                modify_swimmer_arrows( boatArrows_sources, swimmerArrows_sources, person, velocity_increase, boatSpeed )
                
                # the relative velocity of the swimmer is converted to absolute by subtracting the boat's velocity
                person.relativeVelocity[0] -= boatSpeed

                # modify the boat velocity to account for the velocity_increase
                boatSpeed = boatSpeed + velocity_increase
                
                # Determining the total displacement carried so far by the people
                # on board
                totalDisplacement = np.ones(29) * (
                                                    personSource.data['x'][counter][0]
                                                  - person.jumpingPosition[0][0]
                                                  )
    
                # Copying the old list of coordinates defining people on board
                newPersonSourceX = personSource.data['x']
                newPersonSourceY = personSource.data['y']
                
                # Changing the shape of the jumping person to the jumping position
                newPersonSourceX[counter] = person.jumpingPosition[0]+totalDisplacement
                newPersonSourceY[counter] = person.jumpingPosition[1]
    
                # Updating the people (persons) source data file
                personSource.data = dict(
                                             x = newPersonSourceX,
                                             y = newPersonSourceY,
                                             c = personSource.data['c']
                                        )
                
                # Start plotting the path of the person's own jump
                scene.ellipse(
                              x='x',y='y',width=0.1,height=0.1,
                              color="#005293",
                              source=listSources[counter]
                             )
                break
            counter += 1
            if counter == numberPersonsSlider.value-1: # last person jumped
                jump_button.disabled = True
        #update_bars()

    else:
        pass
    glob_boatSpeed.data = dict(val=[boatSpeed])

jump_button = Button(label="Jump!", button_type="success", disabled=True)
jump_button.on_click(jump)
    

'''
###############################################################################
Add all the components together and initiate the app
###############################################################################
'''
# add app description
description_filename = join(dirname(__file__), "description.html")

description = Div(text=open(description_filename).read(), render_as_text=False, width=600)

area_image = Div(text="""
<h2>
Technical Information for Boat and Swimmers
</h2>
<p>
<img src="/Boat_with_three_swimmers/static/images/High_resolution_picture.png" width=400>
</p>
""", render_as_text=False, width=400)

curdoc().add_root(
                  column(
                         row(
                             description,
                             Spacer(width=100),
                             column(
                                    Spacer(height=100),
                                    area_image
                                   )
                            ),
                         Spacer(height=50),
                         scene,
                         Spacer(height=50),
                         row(
                             column(
                                    numberPersonsSlider,
                                    play_button,
                                    #pause_button,
                                    jump_button,
                                    reset_button
                                   ),
                             Spacer(width=100),
                             velocity_diagram,
                            )
                        )
                 )
# get path of parent directory and only use the name of the Parent Directory 
# for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  