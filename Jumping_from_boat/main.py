import numpy as np
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.plotting import ColumnDataSource
from bokeh.models import Button, Slider
from Person import Person, create_default_person, update_source
from bokeh.layouts import column, row

## Plotting diagram construction
xMin , xMax = 0,40
yMin , yMax = 0,10
scene = figure(
                    title="test person",
                    tools="",
                    x_range=(xMin,xMax),
                    y_range=(yMin,yMax),width=1600, height=400
               )

## Initialization data ##
# Dynamics parameters
dt = 0.1

# Water information
waterX = np.array( [xMin,xMin,xMax,xMax] )
waterY = np.array( [yMin,yMax/3,yMax/3,yMin] )
scene.patch(waterX, waterY, fill_color="#0033cc")

# Boat information
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
boatSpeed = 0.5
boatColor = '#cc9900'
boatSource = ColumnDataSource(data=dict(x = boatX,
                                        y = boatY,
                                        ))
scene.patch(x = 'x', y = 'y', fill_color= boatColor, source = boatSource)

# People information
N = 1                                # Number of people on the boat
jumpSpeed = 0.25                     # Speed with respect to the moving boat

x = initBoatCGx
personOneX = np.array( [x, x, x+0.3, x+0.5, x+0.5, x+0.25, x+0.25, x+0.5, x+1.0,
                       x+1.1, x+0.5, x+0.3, x+0.3, x+1.0, x+0.5, x+0.35, x+0.6,
                       x+0.25, x-0.3, x-0.9, x-0.8, x-0.4, x-0.15, x-0.15, 
                       x-0.4, x-0.5, x-0.7, x-0.55, x] )
y = initBoatCGy+0.5
personOneY = np.array( [y+1.5, y+1.8, y+2.0, y+1.8, y+1.3, y+1.3, y+1.1, y+0.6,
                        y+0.9, y+0.7, y+0.3, y+0.5, y-0.1, y-0.65, y-1.4, y-1.3,
                        y-0.8, y-0.5, y-0.9, y-0.5, y-0.2, y-0.5, y, y+0.8, 
                        y+0.7, y+0.25, y+0.3, y+0.95, y+1.15] )

listPeople = create_default_person( N, initBoatCGx, initBoatCGy, L, personOneX, personOneY )
print('initial Length of list of people is: ',len(listPeople))
shape = listPeople[0].get_standingShape()
personSource = ColumnDataSource(data=dict(x=[shape[0]], y=[shape[1]],c=["#CCCCC6"]))
scene.patches(xs='x',ys='y',fill_color='c',source =personSource )

'''
def move_boat():
    global boatSpeed
    
    # Moving the boat
    dx = np.ones(4)*dt*boatSpeed
    boatSource.data['x'] = boatSource.data['x'] - dx

    # Moving the person
    size = len(personSource.data['x'])
    dx = np.ones(size)*dt*boatSpeed
    personSource.data['x'] = personSource.data['x'] - dx

## Create jump button
def jump ():
    curdoc().add_periodic_callback(compute_tranjectory, 10)

def Reset():
    
reset_button = Button(label="Reset", button_type="success")
reset_button.on_click(Reset)

## Create pause button
def pause (toggled):
    global Active
    # When active pause animation
    if (toggled):
        curdoc().remove_periodic_callback(compute_tranjectory)
        Active=False
    else:
        curdoc().add_periodic_callback(compute_tranjectory, 10)
        Active=True
pause_button = Toggle(label="Pause", button_type="success")
pause_button.on_click(pause)

## Create play button
def play ():
    global Active
    # if inactive, reactivate animation
    if (pause_button.active):
        # deactivating pause button reactivates animation
        # (calling add_periodic_callback twice gives errors)
        pause_button.active=False
    elif (not Active):
        curdoc().add_periodic_callback(compute_tranjectory, 10)
        Active=True
play_button = Button(label="Play", button_type="success")
play_button.on_click(play)


play_button = Button(label="jump", button_type="success")
play_button.on_click(jump)
'''
def updateNoPersons(attr,old,new):
    print('the number of people on board has been increased!')
    global listPeople, personSource
    addedNoPersons = new
    
    dx = np.ones(len(personOneX))*(addedNoPersons-1)
    # Loop to add new persons
    for i in range(addedNoPersons):
        n = len(listPeople)
        listPeople.append(  Person( n,75,[personOneX+dx,personOneY] , [personOneX+dx,personOneY] )  ) # here, the default mass is 75 kg
    
    standingShape = listPeople[len(listPeople)-1].get_standingShape()
    personSource.data['x'].append(standingShape[0])
    personSource.data['y'].append(standingShape[1])
    personSource.data['c'].append('#FF33FF')
    
    print(personSource.data['x'])

    
    
numberPersonsSlider = Slider(title=u" Number of People on board ", value=1, start=1, end=5, step=1,width=350)
numberPersonsSlider.on_change('value',updateNoPersons)

#curdoc().add_periodic_callback( move_boat,10 )

curdoc().add_root(column(scene,numberPersonsSlider))