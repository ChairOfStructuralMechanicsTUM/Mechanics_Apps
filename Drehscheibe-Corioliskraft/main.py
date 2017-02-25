from __future__ import division
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, Button, Toggle, Arrow, OpenHead
from bokeh.io import curdoc
from math import pi, sin, cos, radians, sqrt, atan2

circle_axis_circ_coords=dict(rho=[[],[]],phi=[[],[]])
circle_axis_source=ColumnDataSource(data=dict(x=[[],[]],y=[[],[]]))
mass_source=ColumnDataSource(data=dict(x=[],y=[]))
mass_path_circ_coords=dict(rho=[],phi=[])
mass_path_source=ColumnDataSource(data=dict(x=[],y=[]))
mass_lab_path_source=ColumnDataSource(data=dict(x=[],y=[]))
mass_pos=[8,3.0*pi/4.0];
Omega=radians(2)
speed=[2,-2];
v0_source=ColumnDataSource(data=dict(xStart=[],xEnd=[],yStart=[],yEnd=[]))
startPos=[]
Active=False

def initialise ():
    global mass_source, mass_pos, mass_lab_path_source, mass_path_circ_coords, mass_path_source
    global circle_axis_circ_coords, circle_axis_source, startPos
    mass_pos=[8,3.0*pi/4.0];
    mass_source.data=dict(x=[startPos[0]],y=[startPos[1]])
    mass_path_source.data=dict(x=[],y=[])
    mass_lab_path_source.data=dict(x=[startPos[0]],y=[startPos[1]])
    mass_path_circ_coords=dict(rho=[8],phi=[3.0*pi/4.0])
    circle_axis_circ_coords=dict(rho=[[8,8],[8,8]],phi=[[0,pi],[pi/2.0,-pi/2.0]])
    circle_axis_source.data=dict(x=[[-8,8],[0,0]],y=[[0,0],[8,-8]])
    v0_source.data=dict(xStart=[startPos[0]-speed[0]],xEnd=[startPos[0]],
        yStart=[startPos[1]-speed[1]],yEnd=[startPos[1]])

def rotation_speed(attrname, old, new):
    global Omega
    Omega=radians(new)

def cart_to_circ (x,y):
    rho=sqrt(x**2+y**2)
    phi=atan2(y,x)
    return rho,phi

def circ_to_cart_coord (rho,phi):
    X=rho*cos(phi)
    Y=rho*sin(phi)
    return X,Y

def circ_to_cart (rho,phi):
    X=[]
    Y=[]
    for i in range(0,len(rho)):
        X.append(rho[i]*cos(phi[i]))
        Y.append(rho[i]*sin(phi[i]))
    return X,Y

def move():
    global mass_source, mass_pos, speed, mass_lab_path_source
    # use mass_pos because bokeh was occasionally modifying mass_source
    # no idea why!
    [X,Y]=circ_to_cart_coord(mass_pos[0],mass_pos[1])
    Xtemp=X
    X+=0.1*speed[0]
    Y+=0.1*speed[1]
    mass_source.data=dict(x=[X],y=[Y])
    X2=list(mass_lab_path_source.data['x'])
    Y2=list(mass_lab_path_source.data['y'])
    X2.append(X)
    Y2.append(Y)
    mass_lab_path_source.data=dict(x=X2,y=Y2)
    mass_pos=cart_to_circ(X,Y);
    spin(mass_pos)
    
def spin(mass_pos):
    global circle_axis_circ_coords, Omega, mass_path_source, Active
    circle_axis_circ_coords['phi'][0][0]+=Omega
    circle_axis_circ_coords['phi'][0][1]+=Omega
    circle_axis_circ_coords['phi'][1][0]+=Omega
    circle_axis_circ_coords['phi'][1][1]+=Omega
    [X1,Y1]=circ_to_cart(circle_axis_circ_coords['rho'][0],circle_axis_circ_coords['phi'][0])
    [X2,Y2]=circ_to_cart(circle_axis_circ_coords['rho'][1],circle_axis_circ_coords['phi'][1])
    circle_axis_source.data=dict(x=[X1, X2],y=[Y1, Y2])
    for i in range(0,len(mass_path_circ_coords['phi'])):
        mass_path_circ_coords['phi'][i]+=Omega
    mass_path_circ_coords['rho'].append(mass_pos[0])
    mass_path_circ_coords['phi'].append(mass_pos[1])
    [X,Y]=circ_to_cart(mass_path_circ_coords['rho'],mass_path_circ_coords['phi'])
    mass_path_source.data=dict(x=X,y=Y)
    if (mass_pos[0]>8):
        curdoc().remove_periodic_callback(move)
        Active=False

def particle_speed_x (attrname,old,new):
    global speed
    speed=[new,speed[1]];
    v0_source.data=dict(xStart=[startPos[0]-speed[0]],xEnd=[startPos[0]],
        yStart=[startPos[1]-speed[1]],yEnd=[startPos[1]])

def particle_speed_y (attrname,old,new):
    global speed
    speed=[speed[0],new];
    v0_source.data=dict(xStart=[startPos[0]-speed[0]],xEnd=[startPos[0]],
        yStart=[startPos[1]-speed[1]],yEnd=[startPos[1]])

def reset_situation ():
    global pause_button, Active
    if (Active):
        curdoc().remove_periodic_callback(move)
        Active=False
    initialise()
    if (pause_button.active==True):
        pause_button.active=False
    else :
        curdoc().add_periodic_callback(move, 100)
        Active=True

def stop ():
    global pause_button, Active
    if (Active):
        curdoc().remove_periodic_callback(move)
        Active=False
    v0_input_x.value=2.0
    v0_input_y.value=-2.0
    initialise()

def pause (toggled):
    global Active
    if (toggled):
        curdoc().remove_periodic_callback(move)
        Active=False
    else:
        curdoc().add_periodic_callback(move, 100)
        Active=True

def play ():
    global Active
    if (pause_button.active==True):
        pause_button.active=False
    elif (not Active):
        curdoc().add_periodic_callback(move, 100)
        Active=True

[X,Y]=circ_to_cart([mass_pos[0]],[mass_pos[1]]);
startPos=[X[0],Y[0]];
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

## Create stop button
stop_button = Button(label="Stop", button_type="success")
stop_button.on_click(stop)

## Create play button
play_button = Button(label="Play", button_type="success")
play_button.on_click(play)

p=figure(title="Drehscheibe-Corioliskraft (Coriolis Force)", tools="", x_range=(-12,12), y_range=(-12,12))
p.title.text_font_size="20pt"
p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None
p.ellipse(0,0,16,16,fill_color="#74CFED",line_color=None)
p.multi_line('x','y',source=circle_axis_source,line_color="#0099CC")
p.line(x='x',y='y',source=mass_path_source,line_color="red")
p.line(x='x',y='y',source=mass_lab_path_source,line_color="green")
p.ellipse(x='x',y='y',width=0.5,height=0.5,source=mass_source,fill_color="red",line_color=None)
#p.line(x='x',y='y',source=v0_source,line_color="black")
arrow_glyph = Arrow(end=OpenHead(line_color="black",line_width=2),
    x_start='xStart', y_start='yStart', x_end='xEnd', y_end='yEnd',source=v0_source)
p.add_layout(arrow_glyph)

# regularly update user view
#curdoc().add_periodic_callback(move, 100)

## Send to window
curdoc().add_root(row(p,column(Omega_input,v0_input_x,v0_input_y,reset_button,pause_button,stop_button,play_button)))
curdoc().title = "Drehscheibe-Corioliskraft"
