'''
    Main file for the collision App
    
'''
import numpy as np
from bokeh.io import curdoc
from bokeh.plotting import Figure, ColumnDataSource,show,output_file
#from bokeh.document import add_periodic_callback
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

# Define the location of the two colliding balls (in our 2D app, circles)
x1,x2 = 3,5
y1,y2 = 2,5
r1,r2 = 1,1
c1,c2 = '#33FF33','#FF3333'
v1x,v1y,v2x,v2y = 1,0.5,0.3,1
dt = 0.1
tolerance = 0.1  
circleOneSource = ColumnDataSource(
                                       data=dict(
                                                     x = np.array([x1],dtype=np.float64),
                                                     y = np.array([y1],dtype=np.float64),
                                                     r = np.array([r1]),
                                                     c = np.array([c1]),
                                                     vx = np.array([v1x],dtype=np.float64),
                                                     vy = np.array([v1y],dtype=np.float64)
                                                )
                                  )
circleTwoSource = ColumnDataSource(
                                       data=dict(
                                                     x = np.array([x2],dtype=np.float64),
                                                     y = np.array([y2],dtype=np.float64),
                                                     r = np.array([r2]),
                                                     c = np.array([c2]),
                                                     vx = np.array([v2x],dtype=np.float64),
                                                     vy = np.array([v2y],dtype=np.float64)
                                                )
                                  )
#output_file("circles.html")
playGround.circle( x='x',y='y',radius='r',color='c',source=circleOneSource )
playGround.circle( x='x',y='y',radius='r',color='c',source=circleTwoSource )

def compute_tranjectory():
    # Compute the new position of the circles' center
    circleOneSource.data['x'] = circleOneSource.data['vx']*dt + circleOneSource.data['x']
    circleOneSource.data['y'] = circleOneSource.data['vy']*dt + circleOneSource.data['y']
    
    circleTwoSource.data['x'] = circleTwoSource.data['vx']*dt + circleTwoSource.data['x']
    circleTwoSource.data['y'] = circleTwoSource.data['vy']*dt + circleTwoSource.data['y']

    # Detect Walls
    if (abs( circleOneSource.data['x'] + circleOneSource.data['r'] - xMax ) <= abs(circleOneSource.data['vx']*dt) 
        or abs( circleOneSource.data['x'] - circleOneSource.data['r'] - xMin ) <= abs(circleOneSource.data['vx']*dt)):
        circleOneSource.data['vx'] *= -1
    elif (abs( circleTwoSource.data['x'] + circleTwoSource.data['r'] - xMax ) <= abs(circleTwoSource.data['vx']*dt) 
        or abs( circleTwoSource.data['x'] - circleTwoSource.data['r'] - xMin ) <= abs(circleTwoSource.data['vx']*dt)):
        circleTwoSource.data['vx'] *= -1
    
    if (abs( circleOneSource.data['y'] + circleOneSource.data['r'] - yMax ) <= abs(circleOneSource.data['vy']*dt) 
        or abs( circleOneSource.data['y'] - circleOneSource.data['r'] - yMin ) <= abs(circleOneSource.data['vy']*dt)):
        circleOneSource.data['vy'] *= -1
    elif (abs( circleTwoSource.data['y'] + circleTwoSource.data['r'] - yMax ) <= abs(circleTwoSource.data['vy']*dt) 
        or abs( circleTwoSource.data['y'] - circleTwoSource.data['r'] - yMin ) <= abs(circleTwoSource.data['vy']*dt)):
        circleTwoSource.data['vy'] *= -1
    # Detec each other!
        # Distance between the two balls is denoted by distance      
    dx = circleOneSource.data['x']-circleOneSource.data['x']
    dy = circleOneSource.data['y']-circleOneSource.data['y']
    distance = np.sqrt( dx*dx + dy*dy )
    if distance <= tolerance
        circleOneSource.data['vx'] *= -1

curdoc().add_periodic_callback( compute_tranjectory,10 )

curdoc().add_root(playGround)                             