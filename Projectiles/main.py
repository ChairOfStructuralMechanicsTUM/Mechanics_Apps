from __future__ import division
from bokeh.plotting import figure
from bokeh.models import Slider, Arrow, OpenHead, Select, Button, ColumnDataSource, Div
from bokeh.layouts import column, row
from bokeh.io import curdoc
from drawingFuncs import monkeyLetGo, monkeyGrab
from math import radians, cos, sin
from os.path import dirname, join, split
from drawable import Drawable

# initialise variables
aim_line = ColumnDataSource(data=dict(x=[],y=[]))
hill_source = ColumnDataSource(data=dict(x=[],y=[]))
theta = radians(30)
speed = 50
g = 9.81
PlanetGravity = dict(Space = 0.0, Mercury = 3.61, Venus = 8.83, Earth = 9.81, Mars = 3.75, Ceres = 0.27,
    Jupiter = 26.0, Saturn = 11.2, Uranus = 10.5, Neptune = 13.3, Pluto = 0.61)
PlanetHue = dict(Space = "#696A8C", Mercury = "#EDD9FC", Venus = "#FCDDBB", Earth = "#D1F4FF", Mars = "#FF9E9E", Ceres = "#C4C4C4",
    Jupiter = "#FFE1AD", Saturn = "#F3FFC9", Uranus = "#46FAB2", Neptune = "#AFC0DB", Pluto = "#DBD0D0")
x_0 = 5.0
y_0 = 7.5
direction_arrow = ColumnDataSource(data=dict(xS=[],yS=[],xE=[],yE=[]))
t=0
Active = False
Done = False
height = 0
mass = 0.7


def init ():
    updateTargetArrow()


def bananaPosition(t):
    """
    calculate banana position during trajectory
    :param t:
    :return:
    """
    x = x_0 + speed*cos(theta)*t
    y = y_0 + speed*sin(theta)*t-g*t**2/2.0
    return (x,y)


def monkeyPosition(t):
    """
    calculate monkey position during fall
    :param t:
    :return:
    """
    x = monkey_init_pos[0]
    y = monkey_init_pos[1] - g*t**2 * .5
    return (x,y)


def updateTargetArrow():
    """
    update directional indicator arrows
    :return:
    """
    # if speed = 0 then there is no arrow
    if (speed == 0):
        direction_arrow.data = dict(xS=[],yS=[],xE=[],yE=[])
    else:
        # else the arrow is proportional to the speed
        xE=speed*cos(theta)
        yE=speed*sin(theta)
        direction_arrow.data = dict(xS=[x_0], yS=[y_0], xE=[xE+x_0], yE=[yE+y_0])
        # the dotted line is calculated from cos and sin as numerical errors
        # mean that a solution using tan does not lie on the direction arrow
        aim_line.data = dict(x=[x_0,100*xE],y=[y_0,y_0+100*yE])


def evolve():
    """
    function which makes banana and monkey move
    :return:
    """
    global t, Active, Done

    t += 0.1

    xM, yM = monkeyPosition(t)
    xB, yB = bananaPosition(t)
    banana.move_to((xB, yB))
    monkey.move_to((xM, yM))

    # if monkey is hit with banana then stop
    if xM < xB < xM+20 and yM < yB < yM+20:
        curdoc().remove_periodic_callback(callback_id)
        Active = False
        Done = True
    # else if the banana hit the floor then stop
    elif yB < 0 or yM < 0:
        curdoc().remove_periodic_callback(callback_id)
        Active = False
        Done = True
    # else if nothing is falling and the banana has exited the screen
    elif grav_select.value == "Space" and yB > 105:
        curdoc().remove_periodic_callback(callback_id)
        Active = False
        Done = True


# set up image
p = figure(tools="",x_range=(0,200),y_range=(0,100),width=900,height=450)
p.line(x='x',y='y',line_dash='dashed',source=aim_line,color="black")
p.line(x='x',y='y',source=hill_source,color="black")
arrow_glyph = Arrow(end=OpenHead(line_color="black",line_width=3,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=direction_arrow,
    line_color="black",line_width=3)
p.add_layout(arrow_glyph)

monkey = Drawable(p, "Images/monkey.png")
monkey_init_pos = (180, 70)
monkey.draw_at(x=monkey_init_pos[0], y=monkey_init_pos[1], w=20, h=20)

branch = Drawable(p, "Images/branch.png")
branch_init_pos = (150, 70)
branch.draw_at(x=branch_init_pos[0], y=branch_init_pos[1], w=50, h=25)

banana = Drawable(p, "Images/banana.png")
banana_init_pos = (8, 10)
banana.draw_at(x=banana_init_pos[0], y=banana_init_pos[1], w=5, h=5)

cannon = Drawable(p, "Images/cannon.png")
cannon.draw_at(x=2.8, y=3.0, h=10, w=10, pad_fraction=.25)
base = Drawable(p, "Images/base.png")
base.draw_at(x=0, y=0, w=10, h=10)

p.background_fill_color = PlanetHue["Earth"]
p.grid.visible=False

init()


def rotateCannon(angle):
    """
    rotates the cannon and moves the banana correspondingly
    :param angle:
    :return:
    """
    # find points (in image coordinates) about which the image is rotated
    center = (4.7 * cannon.orig_size[0] / 15.0, 7.5 * cannon.orig_size[1] / 15.0)
    cannon.rotate_to(angle, center)
    cos_theta = cos(angle)
    sin_theta = sin(angle)
    pos_banana = (.2 + 4.8 * sin_theta + 5.5 * cos_theta, 4.5 + height + 4.8 * cos_theta - 5.5 * sin_theta)
    banana.move_to(pos_banana)


## slider/button/dropdown functions
def changeTheta(attr,old,new):
    global theta, Active
    # if it has been modified during the simulation
    # move back == deactivated (does not exist in bokeh)
    if (Active and theta!=radians(new)):
        angle_slider.value=old
    else:
        # else update angle and update images
        theta=radians(new)
        rotateCannon(radians(30-new))
        updateTargetArrow()


# angle increment is large to prevent lag
angle_slider = Slider(title=u"Angle \u0398 (\u00B0)",value=30,start=0,end=65,step=5)
angle_slider.on_change('value',changeTheta)


def changeSpeed(attr,old,new):
    global speed, Active
    # if it has been modified during the simulation
    # move back == deactivated (does not exist in bokeh)
    if (Active and speed!=new):
        speed_slider.value=old
    else:
        # else update speed and directional arrow
        speed=new
        updateTargetArrow()


speed_slider = Slider(title="Velocity (m/s)", value=50, start=0, end=120, step=5)
speed_slider.on_change('value', changeSpeed)


# mass is not necessary but function is needed to protect the integrity of the simulation
def massCheck(attr, old, new):
    global Active, mass
    if (Active and mass!=new):
        mass_slider.value=old
    else:
        mass=new


mass_slider = Slider(title="Mass (kg)",value=mass,start=0,end=2,step=0.1)
mass_slider.on_change('value',massCheck)


def changeHeight(attr,old,new):
    global y_0, height
    # if it has been modified during the simulation
    # move back == deactivated (does not exist in bokeh)
    if Active and height != new:
        height_slider.value = old
    else:
        # else change height and update drawings
        Reset()
        height = new
        base.move_to((None, height))
        cannon.move_to((None, height + 0.5))
        banana.move_to((None, 10 + height))
        y_0+=(height-old)
        updateTargetArrow()
        hill_source.data = dict(x=[0, 30, 30],y=[height, height, 0])


height_slider = Slider(title="Height of base (m)",value=0.0,start=0,end=60,step=5)
height_slider.on_change('value',changeHeight)


def changeGrav(attr,old,new):
    global g
    # if it has been modified during the simulation
    # move back == deactivated (does not exist in bokeh)
    if (Active and g != PlanetGravity[new]):
        grav_select.value=old
    else:
        # else reset and change gravity
        g=PlanetGravity[new]
        p.background_fill_color = PlanetHue[new]
        Reset()


grav_select = Select(title="Planet:", value="Earth",
    options=["Space", "Mercury", "Venus", "Earth", "Mars", "Ceres", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"])
grav_select.on_change('value',changeGrav)

callback_id=None
def Fire():
    global Active,callback_id
    if not Active:
        if t!=0:
            Reset()
        # if simulation is not already started
        # release branch and start simulation
        monkeyLetGo(monkey, grav_select.value!="Earth")
        callback_id=curdoc().add_periodic_callback(evolve, 50)
        Active = True


fire_button = Button(label="Fire!",button_type="success")
fire_button.on_click(Fire)


def Reset():
    global Active, Done, t
    # if simulation is in progress, stop simulation
    if Active:
        curdoc().remove_periodic_callback(callback_id)
        Active = False
    elif Done:
        Done = False
    # return banana, monkey and cannon to original positions
    banana_current_position = (banana_init_pos[0],banana_init_pos[1]+height_slider.value)
    banana.move_to(banana_current_position)
    monkey.move_to(monkey_init_pos)

    # make monkey grab branch again (also resets helmet)
    monkeyGrab(monkey, grav_select.value != "Earth")
    # reset time
    t=0


reset_button = Button(label="Reset",button_type="success")
reset_button.on_click(Reset)

# add app description
description_filename = join(dirname(__file__), "description.html")
description = Div(text=open(description_filename).read(), render_as_text=False, width=1000)

## Send to window
curdoc().add_root(column(description,
                         row(p,column(angle_slider,speed_slider,mass_slider,height_slider,grav_select,fire_button,reset_button))
                        )
                 )
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
