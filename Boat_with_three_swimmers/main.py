import numpy as np
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.plotting import ColumnDataSource
from bokeh.models import Button, Toggle, Slider
from Person import Person, create_people, update_source
from bokeh.layouts import column, row

## Plotting diagram construction ##
xMin , xMax = 0,40
yMin , yMax = 0,10
scene = figure(
                    title="test person",
                    x_range=(xMin,xMax),
                    y_range=(yMin,yMax),width=1600, height=400
               )
Active = False
## Initialization data ##
# Dynamics parameters
dt = 0.05

# Water information
waterX = np.array( [xMin,xMin,xMax,xMax] )
waterY = np.array( [yMin,yMax/3,yMax/3,yMin] )
scene.patch(waterX, waterY, fill_color="#0033cc")

# Boat information
mass = 300                           # Mass of the boat
L = 6                                # Length of the boat
initBoatCGx = xMax - L/2             # x-coordinat of the boat's CG
initBoatCGy = yMax/3 - 0.25          # y-coordinat of the boat's CG
boatX = np.array( [
                       initBoatCGx - 2.5, 
                       initBoatCGx - 3.0, 
                       initBoatCGx + 3.0, 
                       initBoatCGx + 2.5
                  ] )
boatY = np.array( [
                       initBoatCGy - 1.0,
                       initBoatCGy + 0.5,
                       initBoatCGy + 0.5,
                       initBoatCGy - 1.0
                  ] )
boatSpeed = 2
boatColor = '#cc9900'
boatSource = ColumnDataSource(data=dict(x = boatX,
                                        y = boatY,
                                        ))
scene.patch(x = 'x', y = 'y', fill_color= boatColor, source = boatSource)

# People information
listSources = list()
N = 1                                # Number of people on the boat
jumpSpeed = 0.25                     # Speed with respect to the moving boat

x = initBoatCGx
y = 1.85+initBoatCGy+0.5

jumpingPersonX = np.array( [x, x, x+0.3, x+0.5, x+0.5, x+0.25, x+0.25, x+0.5, x+1.0,
                       x+1.1, x+0.5, x+0.3, x+0.3, x+1.0, x+0.5, x+0.25, x+0.6,
                       x+0.1, x-0.3, x-0.9, x-0.8, x-0.4, x-0.15, x-0.15, 
                       x-0.4, x-0.5, x-0.7, x-0.55, x] )

jumpingPersonY = np.array( [y+1.5, y+1.8, y+2.0, y+1.8, y+1.3, y+1.3, y+1.1, y+0.6,
                        y+0.9, y+0.7, y+0.3, y+0.5, y-0.1, y-0.65, y-1.4, y-1.2,
                        y-0.7, y-0.3, y-0.9, y-0.5, y-0.2, y-0.5, y, y+0.8, 
                        y+0.7, y+0.25, y+0.3, y+0.95, y+1.15] )

standingPersonX = np.array([x,x+0.2,x+0.2,x+0.1,x+0.1,x+0.5,x+0.6,x+0.5,x+0.3,x+0.25,
                       x+0.25,x+0.15,x+0.25,x+0.05,x,x-0.05,x-0.25,x-0.15,x-0.25,
                       x-0.25,x-0.3,x-0.5,x-0.6,x-0.5,x-0.1,x-0.1,x-0.2,x-0.2])

standingPersonY = np.array([y+1.25,y+1.1,y+0.75,y+0.7,y+0.6,y+0.35,y-0.55,y-0.6,y+0.15,
                       y-0.4,y-0.7,y-1.7,y-1.85,y-1.85,y-1.7,y-1.85,y-1.85,y-1.7,
                       y-0.7,y-0.4,y+0.15,y-0.6,y-0.55,y+0.35,y+0.6,y+0.7,
                       y+0.75,y+1.1])

listPeople = create_people( 
                               N, 
                               initBoatCGx, 
                               initBoatCGy, L, 
                               standingPersonX, standingPersonY,
                               standingPersonX, standingPersonY
                          )

#shape = listPeople[0].get_standingShape()
listXCoords = list()
listYCoords = list()
for person in listPeople:
    listXCoords.append(person.standingPosition[0])
    listYCoords.append(person.standingPosition[1])
    
personSource = ColumnDataSource(data=dict(x=listXCoords, y=listYCoords,c=["#CCCCC6"]))
scene.patches(xs='x',ys='y',fill_color='c',source =personSource )


def move_boat():
    global boatSpeed, listPeople, dt, personSource, listSources
    
    # Moving the boat
    dx = np.ones(4)*dt*boatSpeed
    boatSource.data['x'] = boatSource.data['x'] - dx

    # Moving the person
    size = len(personSource.data['x'][0])
    dx = np.ones(size)

    newListXCoords = list()
    newListYCoords = list()
    newListColor   = personSource.data['c']
    for i in range(len(personSource.data['x'])):
        if listPeople[i].jumping == True:
            newListXCoords.append(personSource.data['x'][i] - dx*dt*boatSpeed
                                  +dx*dt*listPeople[i].relativeVelocity[0])
            newListYCoords.append(personSource.data['y'][i] + dx*dt*listPeople[i].relativeVelocity[1])
            
            listSources[i].stream( dict(
                                                x = [newListXCoords[i][0]],
                                                y = [newListYCoords[i][0]]
                                           ) )
            
            listPeople[i].relativeVelocity[1] -= 9.81*dt
        else:
            newListXCoords.append(personSource.data['x'][i] - dx*dt*boatSpeed)
            newListYCoords.append(personSource.data['y'][i])

    personSource.data = dict(
                                 x=newListXCoords,
                                 y=newListYCoords,
                                 c=newListColor
                            )

def updateNoPersons(attr,old,new):
    global Active, listSources
    if Active == False:
        global listPeople
    
        listPeople = create_people(
                                       new,
                                       initBoatCGx,
                                       initBoatCGy,
                                       L,
                                       standingPersonX, standingPersonY,
                                       jumpingPersonX, jumpingPersonY
                                  )    
        listXCoords = list()
        listYCoords = list()
        listColors  = list()
        for person in listPeople:
            listXCoords.append(person.standingPosition[0])
            listYCoords.append(person.standingPosition[1])
            listColors.append('#33FF33')
        
        personSource.data = dict(x=listXCoords, y=listYCoords,c=listColors)
        
        listSources = list()
        for person in listPeople:
            listSources.append(ColumnDataSource(data=person.jumpingPath))
    else:
        pass
  
numberPersonsSlider = Slider(title=u" Number of People on board ", value=1, start=1, end=5, step=1,width=350)
numberPersonsSlider.on_change('value',updateNoPersons)

# Create pause button
def pause (toggled):
    global Active
    # When active pause animation
    if (toggled):
        curdoc().remove_periodic_callback(move_boat)
        Active=False
    else:
        curdoc().add_periodic_callback(move_boat, 50)
        Active=True
pause_button = Toggle(label="Pause", button_type="success")
pause_button.on_click(pause)

# Create play button
def play ():
    global Active
    # if inactive, reactivate animation
    if (pause_button.active):
        # deactivating pause button reactivates animation
        # (calling add_periodic_callback twice gives errors)
        pause_button.active=False
    elif (not Active):
        curdoc().add_periodic_callback(move_boat, 50)
        Active=True
play_button = Button(label="Play", button_type="success")
play_button.on_click(play)

# Create play button
def jump ():
    global Active, boatSpeed, mass, listPeople, listSources
    # if inactive, reactivate animation
    counter = 0
    for person in listPeople:
        if person.jumping == True:
            pass
        else:
            # Change the speed of the boat
            print('person #',person.n,' has jumped')
            boatSpeed = boatSpeed + person.mass*person.relativeVelocity[0]/mass
            person.jumping = True
            scene.ellipse(x='x',y='y',width=0.1,height=0.1,color="#0065BD",source=listSources[counter])
            break
        counter += 1

jump_button = Button(label="jump", button_type="success")
jump_button.on_click(jump)

#curdoc().add_periodic_callback( move_boat,10 )

curdoc().add_root(column(scene,row(numberPersonsSlider,play_button,pause_button,jump_button)))