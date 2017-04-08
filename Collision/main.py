'''
    Main file for the collision App
    
'''
import numpy as np
from bokeh.io import curdoc
from bokeh.plotting import Figure, ColumnDataSource,show,output_file
import BarChart as BC
from bokeh.layouts import column, row
from bokeh.models import Button, Toggle, Slider
'''
from bokeh.plotting import figure, output_file, show
output_file("circles.html")
plot = figure(width=300, height=300)
plot.circle(x=[1, 2, 3], y=[1, 2, 3], size=20)

curdoc().add_root(plot)
#show(plot)
'''
# Define the figure (which corresponds to the play ground)
xMin, xMax = 0, 10
yMin, yMax = 0, 10

playGround = Figure(
                        plot_width = 800,
                        plot_height= 800,
                        x_range  =(xMin, xMax),
                        y_range  =(yMin, yMax),
                        title = 'Collision play ground'
                   )
eFig = BC.BarChart(["Yello ball's kinetic energy","Red ball's kinetic energy","Total system's kinetic energy"],
    [28,28,0],["#98C6EA","#A2AD00","#E37222"],[1,1,1])
eFig.Width(300)
eFig.Height(650)
eFig.fig.yaxis.visible=False

# Define the location of the two colliding balls (in our 2D app, circles)
x1,x2 = 3,5
y1,y2 = 2,2
r1,r2 = 0.5,0.5
m1,m2 = 3,1
c1,c2 = '#33FF33','#FF3333'
v1x,v1y,v2x,v2y = 1,-2,0,0
dt = 0.05
tolerance = 0.01  
velocityTolerance = 0.01

Active = True

# Collusion Parameters
Cr = 1.0


circleOneSource = ColumnDataSource(
                                       data=dict(
                                                     m = np.array([m1]),
                                                     x = np.array([x1]),
                                                     y = np.array([y1]),
                                                     r = np.array([r1]),
                                                     c = np.array([c1]),
                                                     vx = np.array([v1x]),
                                                     vy = np.array([v1y])
                                                )
                                  )
circleTwoSource = ColumnDataSource(
                                       data=dict(
                                                     m = np.array([m2]),
                                                     x = np.array([x2]),
                                                     y = np.array([y2]),
                                                     r = np.array([r2]),
                                                     c = np.array([c2]),
                                                     vx = np.array([v2x]),
                                                     vy = np.array([v2y])
                                                )
                                  )
#output_file("circles.html")
playGround.circle( x='x',y='y',radius='r',color='c',source=circleOneSource )
playGround.circle( x='x',y='y',radius='r',color='c',source=circleTwoSource )

tolerance = 0.251243

def compute_tranjectory():
    # Compute the new position of the circles' center
    circleOneSource.data['x'] = circleOneSource.data['vx']*dt + circleOneSource.data['x']
    circleOneSource.data['y'] = circleOneSource.data['vy']*dt + circleOneSource.data['y']
    
    circleTwoSource.data['x'] = circleTwoSource.data['vx']*dt + circleTwoSource.data['x']
    circleTwoSource.data['y'] = circleTwoSource.data['vy']*dt + circleTwoSource.data['y']

    dx = circleOneSource.data['x'][0]-circleTwoSource.data['x'][0]
    dy = circleOneSource.data['y'][0]-circleTwoSource.data['y'][0]
    distance = np.sqrt( dx*dx + dy*dy )
    
    # Detect Walls
    if (abs( circleOneSource.data['x'] + circleOneSource.data['r'] - xMax ) <= tolerance
        or abs( circleOneSource.data['x'] - circleOneSource.data['r'] - xMin ) <= tolerance):
        circleOneSource.data['vx'] *= -1
        print('first')
        if distance - abs(circleOneSource.data['r']  + circleTwoSource.data['r'] ) < tolerance:
            print('firstTogether')
            circleTwoSource.data['vx'] *= -1

    elif (abs( circleTwoSource.data['x'] + circleTwoSource.data['r'] - xMax ) <= tolerance
        or abs( circleTwoSource.data['x'] - circleTwoSource.data['r'] - xMin ) <= tolerance):
        circleTwoSource.data['vx'] *= -1
        print('second')
        if distance - abs(circleOneSource.data['r']  + circleTwoSource.data['r'] ) < tolerance:
            print('secondTogether')
            circleOneSource.data['vx'] *= -1
    
    
    if (abs( circleOneSource.data['y'] + circleOneSource.data['r'] - yMax ) <= tolerance 
        or abs( circleOneSource.data['y'] - circleOneSource.data['r'] - yMin ) <= tolerance):
        circleOneSource.data['vy'] *= -1
        print('third')
        if distance - abs(circleOneSource.data['r']  + circleTwoSource.data['r'] )  < tolerance:
            print('thirdTogether')
            circleTwoSource.data['vy'] *= -1

    elif (abs( circleTwoSource.data['y'] + circleTwoSource.data['r'] - yMax ) <= tolerance 
        or abs( circleTwoSource.data['y'] - circleTwoSource.data['r'] - yMin ) <= tolerance):
        circleTwoSource.data['vy'] *= -1
        print('forth')
        if distance - abs(circleOneSource.data['r']  + circleTwoSource.data['r'] )  < tolerance:
            print('forthTogether')
            circleOneSource.data['vy'] *= -1

    # Detec each other!     
    dx = circleOneSource.data['x'][0]-circleTwoSource.data['x'][0]
    dy = circleOneSource.data['y'][0]-circleTwoSource.data['y'][0]
    distance = np.sqrt( dx*dx + dy*dy )
    #normal1Vector = np.array( [ dx, dy] )/distance
    normal2Vector = np.array( [-dx,-dy] )/distance
    #tangentVector  = np.array( [-dy,dx] )/distance
    
    v1Before = np.array( [circleOneSource.data['vx'][0],circleOneSource.data['vy'][0]] )
    v2Before = np.array( [circleTwoSource.data['vx'][0],circleTwoSource.data['vy'][0]] )
    
    v1Normal = np.dot(v1Before,normal2Vector)
    v2Normal = np.dot(v2Before,normal2Vector)
    
    v1TangentVector = v1Before - v1Normal*normal2Vector
    v2TangentVector = v2Before - v2Normal*normal2Vector
    

    
    if (distance <= abs(circleOneSource.data['r'][0]+circleTwoSource.data['r'][0])):
       ## print('collision')
        #v1Normal = -1 * v1Normal
        #v2Normal = -1 * v2Normal
        m1 = circleOneSource.data['m']
        m2 = circleTwoSource.data['m']
        
        v1NormalAfter = (Cr*m2*(v2Normal-v1Normal) + m1*v1Normal + m2*v2Normal)/(m1 + m2)
        v2NormalAfter = (Cr*m1*(v1Normal-v2Normal) + m1*v1Normal + m2*v2Normal)/(m1 + m2)
        
        v1Normal = v1NormalAfter
        v2Normal = v2NormalAfter
        
        v1NormalVector = v1Normal*normal2Vector
        v2NormalVector = v2Normal*normal2Vector
        
        v1After = v1NormalVector + v1TangentVector
        v2After = v2NormalVector + v2TangentVector
        
        circleOneSource.data['vx'] = [v1After[0]] + 0*circleOneSource.data['vx']
        circleOneSource.data['vy'] = [v1After[1]] + 0*circleOneSource.data['vy']
        circleTwoSource.data['vx'] = [v2After[0]] + 0*circleTwoSource.data['vx']
        circleTwoSource.data['vy'] = [v2After[1]] + 0*circleTwoSource.data['vy']

    else:
        pass
    
    update_bars()
    
def update_bars ():
    yellowBallKE = 0.5*circleOneSource.data['m'][0]*( circleOneSource.data['vx'][0]*circleOneSource.data['vx'][0]
                                                 + circleOneSource.data['vy'][0]*circleOneSource.data['vy'][0])
    redBallKE = 0.5*circleTwoSource.data['m'][0]*( circleTwoSource.data['vx'][0]*circleTwoSource.data['vx'][0]
                                                 + circleTwoSource.data['vy'][0]*circleTwoSource.data['vy'][0])
    totalKE = yellowBallKE + redBallKE
    
    eFig.setHeight(0,yellowBallKE)
    eFig.setHeight(1,redBallKE)
    eFig.setHeight(2,totalKE)
    
def Reset():
    global x1, x2, y1, y2, v1x, v2x, v1y, v2y

    circleOneSource.data['x'] = [x1] + 0 *circleOneSource.data['x']
    circleTwoSource.data['x'] = [x2] + 0 *circleTwoSource.data['x']
    circleOneSource.data['y'] = [y1] + 0 *circleOneSource.data['y']
    circleTwoSource.data['y'] = [y2] + 0 *circleTwoSource.data['y']
    circleOneSource.data['vx'] = [v1x] + 0 *circleOneSource.data['vx']
    circleOneSource.data['vy'] = [v1y] + 0 *circleOneSource.data['vy']
    circleTwoSource.data['vx'] = [v2x] + 0 *circleTwoSource.data['vx']
    circleTwoSource.data['vy'] = [v2y] + 0 *circleTwoSource.data['vy']
    
    update_bars()
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

def update_ballOne_x_position(attr,old,new):
    global Active
    
    if Active == False:
        circleOneSource.data['x'] = [new] + 0 *circleOneSource.data['x']
    else:
        pass
def update_ballOne_y_position(attr,old,new):
    global Active
    
    if Active == False:
        circleOneSource.data['y'] = [new] + 0 *circleOneSource.data['y']
    else:
        pass
def update_ballTwo_x_position(attr,old,new):
    global Active
    
    if Active == False:
        circleTwoSource.data['x'] = [new] + 0 *circleTwoSource.data['x']
    else:
        pass
def update_ballTwo_y_position(attr,old,new):
    global Active
    
    if Active == False:
        circleTwoSource.data['y'] = [new] + 0 *circleTwoSource.data['y']
    else:
        pass
    
ballOneXCoordSlider = Slider(title=u" Green ball x-coordinate ", value=0, start=xMin, end=xMax, step=0.25,width=350)
ballOneXCoordSlider.on_change('value',update_ballOne_x_position)

ballOneYCoordSlider = Slider(title=u" Green ball y-coorditate ", value=0, start=yMin, end=yMax, step=0.25,width=350)
ballOneYCoordSlider.on_change('value',update_ballOne_y_position)

ballTwoXCoordSlider = Slider(title=u" Red ball x-coordinate ", value=0, start=xMin, end=xMax, step=0.25,width=350)
ballTwoXCoordSlider.on_change('value',update_ballTwo_x_position)

ballTwoYCoordSlider = Slider(title=u" Red ball y-coordinate ", value=0, start=yMin, end=xMax, step=0.25,width=350)
ballTwoYCoordSlider.on_change('value',update_ballTwo_y_position)

    
curdoc().add_periodic_callback( compute_tranjectory,10 )

curdoc().add_root(row(eFig.getFig(),playGround,column(reset_button,play_button,pause_button,ballOneXCoordSlider,ballOneYCoordSlider,ballTwoXCoordSlider,ballTwoYCoordSlider)))                       