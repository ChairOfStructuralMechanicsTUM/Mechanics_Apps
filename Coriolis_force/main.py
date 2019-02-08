from __future__ import division
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, Button, Toggle, Arrow, OpenHead, RadioGroup
from bokeh.io import curdoc
from math import pi, sin, cos, radians, sqrt, atan2
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv

## Create all required variables
glob_circle_axis_phi       = ColumnDataSource(data=dict(phi1=[],phi2=[]))
glob_circle_axis_source    = ColumnDataSource(data=dict(x=[[],[]],y=[[],[]]))
glob_room_axis_phi         = ColumnDataSource(data=dict(phi1=[],phi2=[]))
glob_room_axis_source      = ColumnDataSource(data=dict(x=[[],[]],y=[[],[]]))
glob_mass_source           = ColumnDataSource(data=dict(x=[],y=[]))
glob_mass_path_circ_coords = ColumnDataSource(data=dict(rho=[],phi=[]))
glob_mass_path_source      = ColumnDataSource(data=dict(x=[],y=[]))
glob_mass_lab_path_circ    = ColumnDataSource(data=dict(rho=[],phi=[]))
glob_mass_lab_path_source  = ColumnDataSource(data=dict(x=[],y=[]))
glob_mass_pos              = ColumnDataSource(data=dict(pos=[[8,3.0*pi/4.0]])) #instead of rho and phi to avoid a lot of re-writing
glob_Omega                 = ColumnDataSource(data=dict(omega=[radians(2)]))
glob_speed                 = ColumnDataSource(data=dict(speed=[[2,-2]]))
glob_OSpeed                = ColumnDataSource(data=dict(speed=[[2,-2]]))
v0_source                  = ColumnDataSource(data=dict(xStart=[],xEnd=[],yStart=[],yEnd=[]))
glob_startPos              = ColumnDataSource(data=dict(sP=[]))
glob_active                = ColumnDataSource(data=dict(Active=[False]))
glob_OnTable               = ColumnDataSource(data=dict(oT=[False]))
glob_AtStart               = ColumnDataSource(data=dict(aS=[True]))
glob_callback              = ColumnDataSource(data=dict(cid=[None])) # callback id

## Functions
# give initial values (called by stop and reset, therefore does not re-initialise arrow)
def initialise ():
    [startPos] = glob_startPos.data["sP"] # input/
    [OSpeed]   = glob_OSpeed.data["speed"] # input
    # rest below is output (written in ColumnDataSource)
    
    # give room axis coordinates
    glob_room_axis_phi.data    = dict(phi1=[0], phi2=[pi/2.0])
    glob_room_axis_source.data = dict(x=[[-12, 12], [0,0]],y=[[0,0], [-12,12]])
    # give mass position in circular coordinates
    glob_mass_pos.data         = dict(pos=[[8,3.0*pi/4.0]])
    # give mass position in cartesian coordinates (stored in startPos to prevent unnecessary function calls)
    glob_mass_source.data      = dict(x=[startPos[0]],y=[startPos[1]])
    # clear old paths
    glob_mass_path_source.data      = dict(x=[startPos[0]], y=[startPos[1]])
    glob_mass_lab_path_source.data  = dict(x=[startPos[0]], y=[startPos[1]])
    glob_mass_lab_path_circ.data    = dict(rho=[8], phi=[3.0*pi/4.0])
    glob_mass_path_circ_coords.data = dict(rho=[8], phi=[3.0*pi/4.0])
    # reset disk orientation in circular and cartesian coordinates
    glob_circle_axis_phi.data       = dict(phi1=[0], phi2=[pi/2.0])
    glob_circle_axis_source.data    = dict(x=[[-8,8],[0,0]],y=[[0,0],[8,-8]])
    # reset speed if it has moved with the room
    speed=OSpeed
    # set up directional arrow
    v0_source.data    = dict(xStart=[startPos[0]-speed[0]],xEnd=[startPos[0]],
        yStart=[startPos[1]-speed[1]],yEnd=[startPos[1]])
    glob_speed.data   = dict(speed=[speed])
    glob_AtStart.data = dict(aS=[True]) 

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
    # use mass_pos because bokeh was occasionally modifying mass_source
    # no idea why! # maybe because you didn't save or load it at some point or forgot []
    [mass_pos] = glob_mass_pos.data["pos"] # input/output
    [speed]    = glob_speed.data["speed"]  # input/output
    [Omega]    = glob_Omega.data["omega"]  # input/
    [OnTable]  = glob_OnTable.data["oT"]   # input/
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
    glob_mass_source.data = dict(x=[X],y=[Y])
    # update path in laboratory referential system    
    glob_mass_lab_path_source.stream(dict(x=[X],y=[Y]))
    glob_mass_lab_path_circ.stream(dict(rho=[mass_pos[0]],phi=[mass_pos[1]]))
    # update path in disk referential system
    glob_mass_path_circ_coords.stream(dict(rho=[mass_pos[0]],phi=[mass_pos[1]]))
    # spin the disk and all associated objects
    if (OnTable):
        spinRoom(mass_pos)
    else:
        spinTable(mass_pos)
    glob_mass_pos.data = dict(pos=[mass_pos])
    glob_speed.data    = dict(speed=[speed])

def spinTable(mass_pos):
    [Omega]            = glob_Omega.data["omega"]          # input/
    [g1coriolisforce]  = glob_callback.data["cid"]         # input/
    [circle_axis_phi1] = glob_circle_axis_phi.data["phi1"] # input/output
    [circle_axis_phi2] = glob_circle_axis_phi.data["phi2"] # input/output
    mass_path_circ_coords_phi = list(glob_mass_path_circ_coords.data["phi"]) # input/output
    mass_path_circ_coords_rho = list(glob_mass_path_circ_coords.data["rho"]) # input/
    # give appearance of rotating main disk by rotating axes
    circle_axis_phi1  += Omega
    circle_axis_phi2  += Omega
    # calculate cartesian coordinates after rotation from cylindrical coordinates
    [X1,Y1]=circ_to_cart_coord(8,circle_axis_phi1)
    [X2,Y2]=circ_to_cart_coord(8,circle_axis_phi2)
    glob_circle_axis_phi.data = dict(phi1=[circle_axis_phi1], phi2=[circle_axis_phi2])
    glob_circle_axis_source.data=dict(x=[[X1,-X1], [X2,-X2]],y=[[Y1,-Y1], [Y2,-Y2]]) #      /output
    # rotate old positions of mass with disk
    for i in range(0,len(mass_path_circ_coords_phi)-1):
        mass_path_circ_coords_phi[i]+=Omega
    # calculate cartesian coordinates after rotation from cylindrical coordinates
    [X,Y]=circ_to_cart(mass_path_circ_coords_rho,mass_path_circ_coords_phi)
    glob_mass_path_circ_coords.data=dict(rho=mass_path_circ_coords_rho,phi=mass_path_circ_coords_phi)
    glob_mass_path_source.data=dict(x=X,y=Y) # maybe here it changes from [[]] to [] ?
    # if ball has exited disk stop the animation
    if (mass_pos[0]>8):
        curdoc().remove_periodic_callback(g1coriolisforce)
        glob_active.data=dict(Active=[False]) #      /output

def spinRoom (mass_pos):
    [Omega]           = glob_Omega.data["omega"]        # input/
    [g1coriolisforce] = glob_callback.data["cid"]       # input/
    [room_axis_phi1]  = glob_room_axis_phi.data["phi1"] # input/output
    [room_axis_phi2]  = glob_room_axis_phi.data["phi2"] # input/output
    mass_lab_path_circ_phi    = list(glob_mass_lab_path_circ.data["phi"]) # input/output
    mass_lab_path_circ_rho    = list(glob_mass_lab_path_circ.data["rho"]) # input/
    mass_path_circ_coords_phi = list(glob_mass_path_circ_coords.data["phi"]) # input/
    mass_path_circ_coords_rho = list(glob_mass_path_circ_coords.data["rho"]) # input/
    # give appearance of rotating room by rotating axes
    room_axis_phi1-=Omega
    room_axis_phi2-=Omega
    # calculate cartesian coordinates after rotation from cylindrical coordinates
    [X1,Y1]=circ_to_cart_coord(15,room_axis_phi1)
    [X2,Y2]=circ_to_cart_coord(15,room_axis_phi2)
    glob_room_axis_phi.data = dict(phi1=[room_axis_phi1], phi2=[room_axis_phi2])
    glob_room_axis_source.data=dict(x=[[X1,-X1], [X2,-X2]],y=[[Y1,-Y1], [Y2,-Y2]]) #      /outpout
    # calculate cartesian coordinates on disk
    [X,Y]=circ_to_cart(mass_path_circ_coords_rho,mass_path_circ_coords_phi)
    glob_mass_path_source.data=dict(x=X,y=Y) #     /output    # maybe change from []?
    # rotate old positions of mass with room
    for i in range(0,len(mass_lab_path_circ_phi)-1):
        mass_lab_path_circ_phi[i]-=Omega
    # calculate cartesian coordinates after rotation from cylindrical coordinates
    [X,Y]=circ_to_cart(mass_lab_path_circ_rho,mass_lab_path_circ_phi)
    glob_mass_lab_path_circ.data=dict(rho=mass_lab_path_circ_rho,phi=mass_lab_path_circ_phi)
    glob_mass_lab_path_source.data=dict(x=X,y=Y) #      /output
    # move v0 arrow
    [rho,phi]=cart_to_circ(v0_source.data['xStart'][0],v0_source.data['yStart'][0])
    start=circ_to_cart_coord(rho,phi-Omega)
    [rho,phi]=cart_to_circ(v0_source.data['xEnd'][0],v0_source.data['yEnd'][0])
    end=circ_to_cart_coord(rho,phi-Omega)
    v0_source.data=dict(xStart=[start[0]],xEnd=[end[0]],
            yStart=[start[1]],yEnd=[end[1]])
    # if ball has exited disk stop the animation
    if (mass_pos[0]>8):
        curdoc().remove_periodic_callback(g1coriolisforce)
        glob_active.data=dict(Active=[False]) #      /output

## Slider functions
# Set rotation speed
def rotation_speed(attrname, old, new):
    glob_Omega.data = dict(omega=[radians(new)]) #      /output

# Set v0
def particle_speed_x (attrname,old,new):
    [speed]    = glob_speed.data["speed"]  # input/output
    [OSpeed]   = glob_OSpeed.data["speed"] # input/output
    [AtStart]  = glob_AtStart.data["aS"]   # input/ 
    [startPos] = glob_startPos.data["sP"]  # input/
    if (AtStart):
        speed=[new,OSpeed[1]];
        OSpeed=speed
        v0_source.data=dict(xStart=[startPos[0]-speed[0]],xEnd=[startPos[0]],
            yStart=[startPos[1]-speed[1]],yEnd=[startPos[1]])
        glob_speed.data  = dict(speed=[speed])
        glob_OSpeed.data = dict(speed=[OSpeed])
    elif (new!=OSpeed[0]):
        v0_input_x.value=OSpeed[0]

# Set v0
def particle_speed_y (attrname,old,new):
    [speed]    = glob_speed.data["speed"]  # input/output
    [OSpeed]   = glob_OSpeed.data["speed"] # input/output
    [AtStart]  = glob_AtStart.data["aS"]   # input/ 
    [startPos] = glob_startPos.data["sP"]  # input/
    if (AtStart):
        speed=[OSpeed[0],new];
        OSpeed=speed
        v0_source.data=dict(xStart=[startPos[0]-speed[0]],xEnd=[startPos[0]],
            yStart=[startPos[1]-speed[1]],yEnd=[startPos[1]])
        glob_speed.data  = dict(speed=[speed])
        glob_OSpeed.data = dict(speed=[OSpeed])
    elif (new!=OSpeed[1]):
        v0_input_y.value=OSpeed[1]

## Button function

def reset_situation ():
    [g1coriolisforce] = glob_callback.data["cid"]  # input/
    [Active]          = glob_active.data["Active"] # input/output
    # only stop callback if there is a callback
    if (Active):
        curdoc().remove_periodic_callback(g1coriolisforce)
        glob_active.data=dict(Active=[False])
    # put everything back to initial position
    initialise()

def BackToInitial ():
    [g1coriolisforce] = glob_callback.data["cid"]  # input/
    [Active]          = glob_active.data["Active"] # input/output
    # only stop callback if there is a callback
    if (Active):
        curdoc().remove_periodic_callback(g1coriolisforce)
        glob_active.data=dict(Active=[False])
    # put speed back to original value
    v0_input_x.value=2.0
    v0_input_y.value=-2.0
    Omega_input.value=2.0
    # put everything back to initial position
    initialise()

def pause (toggled):
    [g1coriolisforce] = glob_callback.data["cid"]  # input/output
    [Active]          = glob_active.data["Active"] # input/output
    [mass_pos]        = glob_mass_pos.data["pos"]  # input/
    # When active pause animation
    if (toggled):
        curdoc().remove_periodic_callback(g1coriolisforce)
        glob_active.data=dict(Active=[False])
    # only restart if still on table
    elif(mass_pos[0]<=8):
        g1coriolisforce=curdoc().add_periodic_callback(move, 100)
        glob_callback.data=dict(cid=[g1coriolisforce])
        glob_active.data=dict(Active=[True])

def play ():
    [g1coriolisforce] = glob_callback.data["cid"]  # input/output
    [Active]          = glob_active.data["Active"] # input/output
    [mass_pos]        = glob_mass_pos.data["pos"]  # input/
    # if inactive, reactivate animation
    if (pause_button.active==True):
        # deactivating pause button reactivates animation
        # (calling add_periodic_callback twice gives errors)
        pause_button.active=False
    # only restart if still on table
    elif (not Active and mass_pos[0]<=8):
        g1coriolisforce=curdoc().add_periodic_callback(move, 100)
        glob_callback.data=dict(cid=[g1coriolisforce])
        glob_active.data=dict(Active=[True])
        glob_AtStart.data=dict(aS=[True]) #      /output

def chooseRef (attrname, old, new):
    glob_OnTable.data=dict(oT=[new==1]) #      /output

# initialise the start position of the ball
# (these lines are not in initialise() as it is unnecessary to call "circ_to_cart" at every "stop" or "reset")
[mass_pos] = glob_mass_pos.data["pos"] # input/
[X,Y]=circ_to_cart([mass_pos[0]],[mass_pos[1]])
glob_startPos.data=dict(sP=[[X[0],Y[0]]]) #      /output
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
p.toolbar.logo = None
# draw room
p.multi_line('x','y',source=glob_room_axis_source,line_color="#003359")
# draw disk
p.ellipse(0,0,16,16,fill_color="#98C6EA",line_color=None)
p.multi_line('x','y',source=glob_circle_axis_source,line_color="#0065BD")
# draw old positions of the ball in circular and cartesian coordinates
p.line(x='x',y='y',source=glob_mass_path_source,line_color="#E37222")
p.line(x='x',y='y',source=glob_mass_lab_path_source,line_color="#A2AD00")
# draw ball
p.ellipse(x='x',y='y',width=0.5,height=0.5,source=glob_mass_source,fill_color="#E37222",line_color=None)
# draw directional arrow
arrow_glyph = Arrow(end=OpenHead(line_color="black",line_width=2),
    x_start='xStart', y_start='yStart', x_end='xEnd', y_end='yEnd',source=v0_source)
p.add_layout(arrow_glyph)

# add app description
description_filename = join(dirname(__file__), "description.html")

description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=900)

## Send to window
curdoc().add_root(column(description,
                         row(p,column(Omega_input,v0_input_x,v0_input_y,play_button,pause_button,reset_button,reinit_button,Referential_button))
                         )
                  )
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
