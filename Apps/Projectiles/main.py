from __future__ import division
from bokeh.plotting import figure
from bokeh.models import Slider, Arrow, OpenHead, Select, Button, ColumnDataSource, Div
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc
from Projectiles_drawingFuncs import monkeyLetGo, monkeyGrab
from math import radians, cos, sin
from os.path import dirname, join, split
from Projectiles_drawable import Projectiles_Drawable
from copy   import deepcopy

#from os.path import dirname, join, split, abspath
#import sys, inspect
import yaml
#currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
#parentdir = join(dirname(currentdir), "shared/")
#sys.path.insert(0,parentdir) 
#from latex_support import LatexDiv, LatexSlider

# Using pathlib
import pathlib
import sys, inspect
shareddir = str(pathlib.Path(__file__).parent.parent.resolve() / "shared" ) + "/"
sys.path.insert(0,shareddir)
from latex_support import LatexDiv, LatexSlider

app_base_path = pathlib.Path(__file__).resolve().parents[0]


# change language
std_lang = 'en'
flags    = ColumnDataSource(data=dict(show=['off'], lang=[std_lang]))
strings  = yaml.safe_load(open(app_base_path/'static' / 'strings.json', encoding='utf-8'))

dropdown_list_text = dict(  en = ["Space", "Mercury", "Venus", "Earth", "Mars", "Ceres", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"],
                            de = ["Weltall", "Merkur", "Venus", "Erde", "Mars", "Ceres", "Jupiter", "Saturn", "Uranus", "Neptun", "Pluto"] )

change_language = ColumnDataSource(data=dict(active=[False]))

# initialise variables
aim_line      = ColumnDataSource(data=dict(x=[],y=[]))
hill_source   = ColumnDataSource(data=dict(x=[],y=[]))
PlanetGravity = dict(Space = 0.0, Mercury = 3.61, Venus = 8.83, Earth = 9.81, Mars = 3.75, Ceres = 0.27,
      Jupiter = 26.0, Saturn = 11.2, Uranus = 10.5, Neptune = 13.3, Pluto = 0.61)
PlanetHue     = dict(Space = "#696A8C", Mercury = "#EDD9FC", Venus = "#FCDDBB", Earth = "#D1F4FF", Mars = "#FF9E9E", Ceres = "#C4C4C4",
      Jupiter = "#FFE1AD", Saturn = "#F3FFC9", Uranus = "#46FAB2", Neptune = "#AFC0DB", Pluto = "#DBD0D0")
x_0 = 5.0
y_0 = 7.5
direction_arrow = ColumnDataSource(data=dict(xS=[],yS=[],xE=[],yE=[]))

glob_t        = ColumnDataSource(data=dict(val=[0]))
glob_g        = ColumnDataSource(data=dict(val=[9.81]))

glob_speed    = ColumnDataSource(data=dict(val=[50]))
glob_theta    = ColumnDataSource(data=dict(val=[radians(30)]))
glob_mass     = ColumnDataSource(data=dict(val=[0.7]))

glob_y0       = ColumnDataSource(data=dict(val=[y_0]))
glob_height   = ColumnDataSource(data=dict(val=[0]))

glob_active   = ColumnDataSource(data=dict(Active=[False]))
glob_done     = ColumnDataSource(data=dict(Done=[False]))
glob_callback = ColumnDataSource(data=dict(cid=[None]))

def init():
    updateTargetArrow()


def bananaPosition(t):
    """
    calculate banana position during trajectory
    :param t:
    :return:
    """
    [g]     = glob_g.data["val"]     # input/
    [speed] = glob_speed.data["val"] # input/
    [theta] = glob_theta.data["val"] # input/
    [y_0]   = glob_y0.data["val"]    # input/
    x = x_0 + speed*cos(theta)*t
    y = y_0 + speed*sin(theta)*t-g*t**2/2.0
    return (x,y)


def monkeyPosition(t):
    """
    calculate monkey position during fall
    :param t:
    :return:
    """
    [g] = glob_g.data["val"] # input/
    x = monkey_init_pos[0]
    y = monkey_init_pos[1] - g*t**2 * .5
    return (x,y)


def updateTargetArrow():
    """
    update directional indicator arrows
    :return:
    """
    [speed] = glob_speed.data["val"] # input/
    [theta] = glob_theta.data["val"] # input/
    [y_0]   = glob_y0.data["val"]    # input/
    # if speed = 0 then there is no arrow
    if (speed == 0):
        # define xE and yE so that the aim line is updated even if speed = 0
        xE=10*cos(theta)
        yE=10*sin(theta)
        direction_arrow.stream(dict(xS=[0],yS=[0],xE=[0],yE=[0]), rollover=1)
        aim_line.data = dict(x=[x_0,x_0+100*xE],y=[y_0,y_0+100*yE])
    else:
        # else the arrow is proportional to the speed
        xE=speed*cos(theta)
        yE=speed*sin(theta)
        direction_arrow.stream(dict(xS=[x_0], yS=[y_0], xE=[xE+x_0], yE=[yE+y_0]), rollover=1)
        # the dotted line is calculated from cos and sin as numerical errors
        # mean that a solution using tan does not lie on the direction arrow
        aim_line.data = dict(x=[x_0,x_0+100*xE],y=[y_0,y_0+100*yE])


def evolve():
    """
    function which makes banana and monkey move
    :return:
    """
    [t] = glob_t.data["val"] # input/output
    [g1Projectiles] = glob_callback.data["cid"] # input/

    t += 0.1
    glob_t.data = dict(val=[t])

    xM, yM = monkeyPosition(t)
    xB, yB = bananaPosition(t)
    banana.move_to((xB, yB))
    monkey.move_to((xM, yM))

    # if monkey is hit with banana then stop
    if xM < xB < xM+20 and yM < yB < yM+20:
        curdoc().remove_periodic_callback(g1Projectiles)
        glob_active.data = dict(Active=[False]) #      /output
        glob_done.data   = dict(Done=[True])    #      /output
    # else if the banana hit the floor then stop
    elif yB < 0 or yM < 0:
        curdoc().remove_periodic_callback(g1Projectiles)
        glob_active.data = dict(Active=[False]) #      /output
        glob_done.data   = dict(Done=[True])    #      /output
    # else if nothing is falling and the banana has exited the screen
    elif (grav_select.value == "Space" and yB > 105) or (grav_select.value == "Weltraum" and yB > 105):
        curdoc().remove_periodic_callback(g1Projectiles)
        glob_active.data = dict(Active=[False]) #      /output
        glob_done.data   = dict(Done=[True])    #      /output


# set up image
p = figure(tools="",x_range=(0,200),y_range=(0,100),width=900,height=450)
p.line(x='x',y='y',line_dash='dashed',source=aim_line,color="black")
p.line(x='x',y='y',source=hill_source,color="black")
arrow_glyph = Arrow(end=OpenHead(line_color="black",line_width=3,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', source=direction_arrow,
    line_color="black",line_width=3)
p.add_layout(arrow_glyph)

monkey          = Projectiles_Drawable(p, "static/images/monkey.png")
monkey_init_pos = (180, 68.8)
monkey.draw_at(x=monkey_init_pos[0], y=monkey_init_pos[1], w=20, h=25)

branch          = Projectiles_Drawable(p, "static/images/branch.png")
branch_init_pos = (150, 70)
branch.draw_at(x=branch_init_pos[0], y=branch_init_pos[1], w=50, h=25)

banana          = Projectiles_Drawable(p, "static/images/banana.png")
banana_init_pos = (8, 10)
banana.draw_at(x=banana_init_pos[0], y=banana_init_pos[1], w=5, h=5)

cannon          = Projectiles_Drawable(p, "static/images/cannon.png")
cannon.draw_at(x=1.8, y=4.7, h=9, w=10, pad_fraction=.25)
base            = Projectiles_Drawable(p, "static/images/base.png")
base.draw_at(x=0, y=0, w=10, h=6)

p.background_fill_color = PlanetHue["Earth"]
p.grid.visible = False
p.toolbar.logo = None

init()


def rotateCannon(angle):
    """
    rotates the cannon and moves the banana correspondingly
    :param angle:
    :return:
    """
    [height] = glob_height.data["val"] # input/
    # find points (in image coordinates) about which the image is rotated
    center = (4.7 * cannon.orig_size[0] / 15.0, 7.5 * cannon.orig_size[1] / 15.0)
    cannon.rotate_to(angle, center)
    cos_theta  = cos(angle)
    sin_theta  = sin(angle)
    pos_banana = (.2 + 4.8 * sin_theta + 5.5 * cos_theta, 4.5 + height + 4.8 * cos_theta - 5.5 * sin_theta)
    banana.move_to(pos_banana)


## slider/button/dropdown functions
def changeTheta(attr,old,new):
    [Active] = glob_active.data["Active"] # input/
    [theta]  = glob_theta.data["val"]     # input/output
    # if it has been modified during the simulation
    # move back == deactivated (does not exist in bokeh)
    if (Active and theta!=radians(new)):
        angle_slider.value=old
    else:
        # else update angle and update images
        glob_theta.data = dict(val=[radians(new)])
        rotateCannon(radians(30-new))
        updateTargetArrow()


# angle increment is large to prevent lag
angle_slider = LatexSlider(title="\\text{Angle \u0398} \\left[ \\mathrm{°} \\right]: ", value=30, start=0, end=65, step=5)
angle_slider.on_change('value',changeTheta)

def changeSpeed(attr,old,new):
    [Active] = glob_active.data["Active"] # input/
    [speed]  = glob_speed.data["val"]     # input/output
    # if it has been modified during the simulation
    # move back == deactivated (does not exist in bokeh)
    if (Active and speed!=new):
        speed_slider.value=old
    else:
        # else update speed and directional arrow
        glob_speed.data = dict(val=[new])
        updateTargetArrow()


speed_slider = LatexSlider(title="\\text{Velocity} \\left[ \\frac{\\mathrm{m}}{\\mathrm{s}} \\right]: ", value=50, start=0, end=120, step=5)
speed_slider.on_change('value', changeSpeed)

# mass is not necessary but function is needed to protect the integrity of the simulation
def massCheck(attr, old, new):
    [Active] = glob_active.data["Active"] # input/
    [mass]   = glob_mass.data["val"]      # input/output
    if (Active and mass!=new):
        mass_slider.value=old
    else:
        glob_mass.data = dict(val=[new])


mass_slider = LatexSlider(title="\\text{Mass} \\left[ \\mathrm{kg} \\right]: ", value=0.7, start=0, end=2, step=0.1)
mass_slider.on_change('value', massCheck)


def changeHeight(attr,old,new):
    [Active] = glob_active.data["Active"] # input/
    [height] = glob_height.data["val"]    # input/output
    [y_0]    = glob_y0.data["val"]        # input/output
    # if it has been modified during the simulation
    # move back == deactivated (does not exist in bokeh)
    if Active and height != new:
        height_slider.value = old
    else:
        # else change height and update drawings
        #Reset()
        height = new
        base.move_to((None, height))
        cannon.move_to((None, height + 2.3))
        banana.move_to((None, 10 + height))
        y_0+=(height-old)
        hill_source.data = dict(x=[0, 30, 30],y=[height, height, 0])
        glob_height.data = dict(val=[height])
        glob_y0.data     = dict(val=[y_0])
        updateTargetArrow()


height_slider = LatexSlider(title="\\text{Height of base} \\left[ \\mathrm{m} \\right]: ", value=0.0, start=0, end=60, step=5)
height_slider.on_change('value', changeHeight)

def changeGrav(attr,old,new):
    if not change_language.data['active'][0]:
        [lang] = flags.data["lang"]
        [Active] = glob_active.data["Active"] # input/
        [g]      = glob_g.data["val"]         # input/output
        # if it has been modified during the simulation
        # move back == deactivated (does not exist in bokeh)
        index = dropdown_list_text[lang].index(grav_select.value)
        g_new = list(PlanetGravity.values())[index]
        if (Active and g != g_new):
            grav_select.value=old
        else:
            # else reset and change gravity
            g           = g_new
            glob_g.data = dict(val=[g])
            p.background_fill_color = list(PlanetHue.values())[index]
            Reset()

grav_select = Select(title="Planet:", value="Earth",
    options=dropdown_list_text['en'], css_classes=['b_play'])
grav_select.on_change('value',changeGrav)

def Fire():
    [Active] = glob_active.data["Active"] # input/output
    [t]      = glob_t.data["val"]         # input/
    if not Active:
        if t!=0:
            Reset()
        # if simulation is not already started
        # release branch and start simulation
        space = True
        if grav_select.value == "Earth" or grav_select.value == "Erde":
            space = False
        monkeyLetGo(monkey, space)
        g1Projectiles=curdoc().add_periodic_callback(evolve, 50)
        glob_callback.data = dict(cid=[g1Projectiles]) #      /output
        glob_active.data   = dict(Active=[True])


fire_button = Button(label="Fire!",button_type="success")
fire_button.on_click(Fire)


def Reset():
    [Active]        = glob_active.data["Active"] # input/output
    [g1Projectiles] = glob_callback.data["cid"]  # input/
    [Done]          = glob_done.data["Done"]     # input/output
    # if simulation is in progress, stop simulation
    if Active:
        curdoc().remove_periodic_callback(g1Projectiles)
        glob_active.data = dict(Active=[False])
    elif Done:
        glob_done.data   = dict(Done=[False])
    # return banana, monkey and cannon to original positions
    banana_current_position = (banana_init_pos[0],banana_init_pos[1]+height_slider.value)
    banana.move_to(banana_current_position)
    monkey.move_to(monkey_init_pos)

    # make monkey grab branch again (also resets helmet)
    space = True
    if grav_select.value == "Earth" or grav_select.value == "Erde":
        space = False
    monkeyGrab(monkey, space )
    # reset time
    glob_t.data = dict(val=[0])


reset_button = Button(label="Reset",button_type="success")
reset_button.on_click(Reset)


######################################
# Change language
######################################

def changeLanguage():
    [lang] = flags.data["lang"]
    if lang == "en":
        setDocumentLanguage(lang, 'de')
    elif lang == "de":
        setDocumentLanguage(lang, 'en')

def setDocumentLanguage(old_lang, lang):
    flags.patch( {'lang':[(0,lang)]} )

    index = dropdown_list_text[old_lang].index(grav_select.value)

    change_language.data['active'][0] = True
    for s in strings:
        if 'checkFlag' in strings[s]:
            flag = flags.data[strings[s]['checkFlag']][0]
            exec( (s + '=\"' + strings[s][flag][lang] + '\"').encode(encoding='utf-8') )
        elif 'isCode' in strings[s] and strings[s]['isCode']:
            exec( (s + '=' + strings[s][lang]).encode(encoding='utf-8') )
        else:
            exec( (s + '=\"' + strings[s][lang] + '\"').encode(encoding='utf-8') )

    change_language.data['active'][0] = False

    grav_select.options = dropdown_list_text[lang]
    grav_select.value = dropdown_list_text[lang][index]

lang_button = Button(button_type="success", label="Zu Deutsch wechseln")
lang_button.on_click(changeLanguage)

######################################
# Page layout
######################################

# add app description
description_filename = str(app_base_path / "description.html")
description = Div(text=open(description_filename).read(), render_as_text=False, width=1000)

## Send to window
curdoc().add_root(column(row(Spacer(width=700),lang_button),description,
                         row(p,column(angle_slider,speed_slider,mass_slider,height_slider,grav_select,fire_button,reset_button))
                        )
                 )
curdoc().title = str(app_base_path.relative_to(app_base_path.parent)).replace("_"," ").replace("-"," ")  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '

