from __future__ import division
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, Button, Toggle, Arrow, OpenHead, RadioGroup, Div
from bokeh.io import curdoc
from math import pi, sin, cos, radians, sqrt, atan2
from os.path import dirname, join, split

## Create all required variables
circle_axis_phi=[]
circle_axis_source=ColumnDataSource(data=dict(x=[[],[]],y=[[],[]]))
room_axis_phi=[]
room_axis_source=ColumnDataSource(data=dict(x=[[],[]],y=[[],[]]))
mass_source=ColumnDataSource(data=dict(x=[],y=[]))
mass_path_circ_coords=dict(rho=[],phi=[])
mass_path_source=ColumnDataSource(data=dict(x=[],y=[]))
mass_lab_path_source=ColumnDataSource(data=dict(x=[],y=[]))
mass_lab_path_circ=dict(rho=[],phi=[])
mass_pos=[8,3.0*pi/4.0];
Omega=radians(2)
speed=[2,-2];
OSpeed=[2,-2];
v0_source=ColumnDataSource(data=dict(xStart=[],xEnd=[],yStart=[],yEnd=[]))
startPos=[]
Active=False
OnTable=False
AtStart=True

## Functions
# give initial values (called by stop and reset, therefore does not re-initialise arrow)
def initialise ():
    global mass_source, mass_pos, mass_lab_path_source, mass_path_circ_coords, mass_path_source, mass_lab_path_circ
    global circle_axis_source, startPos, circle_axis_phi, room_axis_phi, room_axis_source, speed, OSpeed, AtStart
    # give room axis coordinates
    room_axis_phi=[0,pi/2.0]
    room_axis_source.data=dict(x=[[-12, 12], [0,0]],y=[[0,0], [-12,12]])
    # give mass position in circular coordinates
    mass_pos=[8,3.0*pi/4.0];
    # give mass position in cartesian coordinates (stored in startPos to prevent unnecessary function calls)
    mass_source.data=dict(x=[startPos[0]],y=[startPos[1]])
    # clear old paths
    mass_path_source.data=dict(x=[startPos[0]],y=[startPos[1]])
    mass_lab_path_source.data=dict(x=[startPos[0]],y=[startPos[1]])
    mass_lab_path_circ=dict(rho=[8],phi=[3.0*pi/4.0])
    mass_path_circ_coords=dict(rho=[8],phi=[3.0*pi/4.0])
    # reset disk orientation in circular and cartesian coordinates
    circle_axis_phi=[0,pi/2.0]
    circle_axis_source.data=dict(x=[[-8,8],[0,0]],y=[[0,0],[8,-8]])
    # reset speed if it has moved with the room
    speed=OSpeed
    # set up directional arrow
    v0_source.data=dict(xStart=[startPos[0]-speed[0]],xEnd=[startPos[0]],
        yStart=[startPos[1]-speed[1]],yEnd=[startPos[1]])
    AtStart=True

# convert 1 cartesian coordinate to a circular coordinate
def cart_to_circ (x,y):
    rho=sqrt(x**2+y**2)
    phi=atan2(y,x)
    return rho,phi

# convert 1 circular coordinate to a cartesian coordinate
def circ_to_cart_coord (rho,phi):
    X=rho*cos(phi)
    Y=rho*sin(phi)
    return X,Y

# convert circular coordinates to cartesian coordinates
def circ_to_cart (rho,phi):
    X=[]
    Y=[]
    for i in range(0,len(rho)):
        X.append(rho[i]*cos(phi[i]))
        Y.append(rho[i]*sin(phi[i]))
    return X,Y

def move():
    global mass_source, mass_pos, speed, mass_lab_path_source, mass_lab_path_circ, mass_path_circ_coords
    # use mass_pos because bokeh was occasionally modifying mass_source
    # no idea why!
    [X,Y]=circ_to_cart_coord(mass_pos[0],mass_pos[1])
    # update mass position
    X+=0.1*speed[0]
    Y+=0.1*speed[1]
    # save new position
    [mass_pos[0],mass_pos[1]]=cart_to_circ(X,Y)
    # if in table referential spin
    if (OnTable):
        end=[X+0.1*speed[0],Y+0.1*speed[1]]
        [rho,phi]=cart_to_circ(end[0],end[1])
        phi-=Omega
        mass_pos[1]-=Omega
        [X,Y]=circ_to_cart_coord(mass_pos[0],mass_pos[1])
        [X2,Y2]=circ_to_cart_coord(rho,phi)
        speed=[10*(X2-X),10*(Y2-Y)]
    mass_source.data=dict(x=[X],y=[Y])
    # copy mass_lab_path_source so the update works
    X2=list(mass_lab_path_source.data['x'])
    Y2=list(mass_lab_path_source.data['y'])
    # add new coordinates
    X2.append(X)
    Y2.append(Y)
    # update path in laboratory referential system
    mass_lab_path_source.data=dict(x=X2,y=Y2)
    mass_lab_path_circ['rho'].append(mass_pos[0])
    mass_lab_path_circ['phi'].append(mass_pos[1])
    # update path in disk referential system
    mass_path_circ_coords['rho'].append(mass_pos[0])
    mass_path_circ_coords['phi'].append(mass_pos[1])
    # spin the disk and all associated objects
    if (OnTable):
        spinRoom(mass_pos)
    else:
        spinTable(mass_pos)
    
def spinTable(mass_pos):
    global Omega, mass_path_source, Active, circle_axis_phi
    # give appearance of rotating main disk by rotating axes
    circle_axis_phi[0]+=Omega
    circle_axis_phi[1]+=Omega
    # calculate cartesian coordinates after rotation from cylindrical coordinates
    [X1,Y1]=circ_to_cart_coord(8,circle_axis_phi[0])
    [X2,Y2]=circ_to_cart_coord(8,circle_axis_phi[1])
    circle_axis_source.data=dict(x=[[X1,-X1], [X2,-X2]],y=[[Y1,-Y1], [Y2,-Y2]])
    # rotate old positions of mass with disk
    for i in range(0,len(mass_path_circ_coords['phi'])-1):
        mass_path_circ_coords['phi'][i]+=Omega
    # calculate cartesian coordinates after rotation from cylindrical coordinates
    [X,Y]=circ_to_cart(mass_path_circ_coords['rho'],mass_path_circ_coords['phi'])
    mass_path_source.data=dict(x=X,y=Y)
    # if ball has exited disk stop the animation
    if (mass_pos[0]>8):
        curdoc().remove_periodic_callback(move)
        Active=False

def spinRoom (mass_pos):
    global room_axis_phi, Omega, room_axis_source, mass_path_source, Active, circle_axis_phi#, speed
    # give appearance of rotating room by rotating axes
    room_axis_phi[0]-=Omega
    room_axis_phi[1]-=Omega
    # calculate cartesian coordinates after rotation from cylindrical coordinates
    [X1,Y1]=circ_to_cart_coord(15,room_axis_phi[0])
    [X2,Y2]=circ_to_cart_coord(15,room_axis_phi[1])
    room_axis_source.data=dict(x=[[X1,-X1], [X2,-X2]],y=[[Y1,-Y1], [Y2,-Y2]])
    # calculate cartesian coordinates on disk
    [X,Y]=circ_to_cart(mass_path_circ_coords['rho'],mass_path_circ_coords['phi'])
    mass_path_source.data=dict(x=X,y=Y)
    # rotate old positions of mass with room
    for i in range(0,len(mass_lab_path_circ['phi'])-1):
        mass_lab_path_circ['phi'][i]-=Omega
    # calculate cartesian coordinates after rotation from cylindrical coordinates
    [X,Y]=circ_to_cart(mass_lab_path_circ['rho'],mass_lab_path_circ['phi'])
    mass_lab_path_source.data=dict(x=X,y=Y)
    # move v0 arrow
    [rho,phi]=cart_to_circ(v0_source.data['xStart'][0],v0_source.data['yStart'][0])
    start=circ_to_cart_coord(rho,phi-Omega)
    [rho,phi]=cart_to_circ(v0_source.data['xEnd'][0],v0_source.data['yEnd'][0])
    end=circ_to_cart_coord(rho,phi-Omega)
    v0_source.data=dict(xStart=[start[0]],xEnd=[end[0]],
            yStart=[start[1]],yEnd=[end[1]])
    # if ball has exited disk stop the animation
    if (mass_pos[0]>8):
        curdoc().remove_periodic_callback(move)
        Active=False

## Slider functions
# Set rotation speed
def rotation_speed(attrname, old, new):
    global Omega
    Omega=radians(new)

# Set v0
def particle_speed_x (attrname,old,new):
    global speed, OSpeed, AtStart
    if (AtStart):
        speed=[new,OSpeed[1]];
        OSpeed=speed
        v0_source.data=dict(xStart=[startPos[0]-speed[0]],xEnd=[startPos[0]],
            yStart=[startPos[1]-speed[1]],yEnd=[startPos[1]])
    elif (new!=OSpeed[0]):
        global v0_input_x
        v0_input_x.value=OSpeed[0]

# Set v0
def particle_speed_y (attrname,old,new):
    global speed, OSpeed, AtStart
    if (AtStart):
        speed=[OSpeed[0],new];
        OSpeed=speed
        v0_source.data=dict(xStart=[startPos[0]-speed[0]],xEnd=[startPos[0]],
            yStart=[startPos[1]-speed[1]],yEnd=[startPos[1]])
    elif (new!=OSpeed[1]):
        global v0_input_y
        v0_input_y.value=OSpeed[1]

## Button functions
def reset_situation ():
    global pause_button, Active
    # only stop callback if there is a callback
    if (Active):
        curdoc().remove_periodic_callback(move)
        Active=False
    # put everything back to initial position
    initialise()

def BackToInitial ():
    global pause_button, Active
    # only stop callback if there is a callback
    if (Active):
        curdoc().remove_periodic_callback(move)
        Active=False
    # put speed back to original value
    v0_input_x.value=2.0
    v0_input_y.value=-2.0
    Omega_input.value=2.0
    # put everything back to initial position
    initialise()

def pause (toggled):
    global Active
    # When active pause animation
    if (toggled):
        curdoc().remove_periodic_callback(move)
        Active=False
    # only restart if still on table
    elif(mass_pos[0]<=8):
        curdoc().add_periodic_callback(move, 100)
        Active=True

def play ():
    global Active, AtStart
    # if inactive, reactivate animation
    if (pause_button.active==True):
        # deactivating pause button reactivates animation
        # (calling add_periodic_callback twice gives errors)
        pause_button.active=False
    # only restart if still on table
    elif (not Active and mass_pos[0]<=8):
        curdoc().add_periodic_callback(move, 100)
        Active=True
        AtStart=False

def chooseRef (attrname, old, new):
    global OnTable
    OnTable = (new==1);

# initialise the start position of the ball
# (these lines are not in initialise() as it is unnecessary to call "circ_to_cart" at every "stop" or "reset")
[X,Y]=circ_to_cart([mass_pos[0]],[mass_pos[1]]);
startPos=[X[0],Y[0]];
# initialise object positions
initialise()

## Create slider to rotate plate
Omega_input = Slider(title=u"\u03C9", value=2.0, start=0.0, end=10.0, step=0.1)
Omega_input.on_change('value',rotation_speed)

## Create slider to select v0-x
v0_input_x = Slider(title=u"v\u2092-x", value=2.0, start=-5.0, end=5.0, step=0.5)
v0_input_x.on_change('value',particle_speed_x)

## Create slider to select v0-y
v0_input_y = Slider(title=u"v\u2092-y", value=-2.0, start=-5.0, end=5.0, step=0.5)
v0_input_y.on_change('value',particle_speed_y)

## Create reset button
reset_button = Button(label="Reset", button_type="success")
reset_button.on_click(reset_situation)

## Create pause button
pause_button = Toggle(label="Pause", button_type="success")
pause_button.on_click(pause)

## Create re-initialise button
reinit_button = Button(label="Re-initialise", button_type="success")
reinit_button.on_click(BackToInitial)

## Create play button
play_button = Button(label="Play", button_type="success")
play_button.on_click(play)

## Create choice of referential button
Referential_button = RadioGroup(labels=["Reference frame: Room",
    "Reference frame: Disk"], active=0)
Referential_button.on_change('active',chooseRef)

## create drawing
p=figure(title="Rotating disk with non accelerated particle", tools="", x_range=(-12,12), y_range=(-12,12))
p.title.text_font_size="25px"
p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None
# draw room
p.multi_line('x','y',source=room_axis_source,line_color="#003359")
# draw disk
p.ellipse(0,0,16,16,fill_color="#98C6EA",line_color=None)
p.multi_line('x','y',source=circle_axis_source,line_color="#0065BD")
# draw old positions of the ball in circular and cartesian coordinates
p.line(x='x',y='y',source=mass_path_source,line_color="#E37222")
p.line(x='x',y='y',source=mass_lab_path_source,line_color="#A2AD00")
# draw ball
p.ellipse(x='x',y='y',width=0.5,height=0.5,source=mass_source,fill_color="#E37222",line_color=None)
# draw directional arrow
arrow_glyph = Arrow(end=OpenHead(line_color="black",line_width=2),
    x_start='xStart', y_start='yStart', x_end='xEnd', y_end='yEnd',source=v0_source)
p.add_layout(arrow_glyph)

# add app description
description_filename = join(dirname(__file__), "description.html")

description = Div(text=open(description_filename).read(), render_as_text=False, width=900)

## Send to window
curdoc().add_root(column(description,
                         row(p,column(Omega_input,v0_input_x,v0_input_y,play_button,pause_button,reset_button,reinit_button,Referential_button))
                         )
                  )
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
