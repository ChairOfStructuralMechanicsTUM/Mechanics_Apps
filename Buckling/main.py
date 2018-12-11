#Knickung (buckling) animation:
#This animation creates 4 columns.
#   All columns are of the same height
#   All columns have the same material properties
#   Each column has different boundary conditions
#   Each columns buckle at a different F-ratio value

#Import libraries:
from bokeh.plotting import Figure
from bokeh.models import ColumnDataSource, Slider, LabelSet, Arrow, NormalHead, Button
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc
import numpy as np
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv, LatexLabelSet

#Global constant numbers:
score           = 30
factor          = 1.2
xf              = 0.0
window          = 18
xstart          = 0.02 * window
zstart          = 0.1 * window  #height of floor
step            = 0.01
f_end           = 5.0 #1.5
w_end           = 0.15

L               = 10.0
fcrit_2         = 1.0  # reference for critical force is second column

# replaces global var
global_old_slide_val = ColumnDataSource(data=dict(val=[0]))


#Class created for the columns:
class Column(object):
    def __init__(self,name,h,fcrit):
        self.pts        = ColumnDataSource(data=dict(x=[] , y=[]))              #pts contains the x and y coordinates of the column
        self.h          = h                                                     #The height of the column
        self.hi         = h                                                     #Initial height of column
        self.name       = name                                                  #Name of column
        self.deflection = 0                                                     #Calculated Deflection
        self.defi       = 0                                                     #Initial Deflection (should be 0)
        self.fcrit      = fcrit                                                 #Critical Force. Value where buckling begins
        self.xstart     = 0                                                     #x-coordinate of the bottom of the column
        self.floor      = dict(x = [] , y = [])                                 #coordinates for floor of column
        self.arrow      = ColumnDataSource(data=dict(xS=[], xE=[],              #Force arrow of column
        yS=[], yE=[], lW = []))
        self.labels     = ColumnDataSource(data=dict(x=[] , y=[], name = []))   #Force arrows labels
        self.sk         = ColumnDataSource(data=dict(x=[] , y=[]))              #buckling length (visual)
        self.sk_labels  = ColumnDataSource(data=dict(x=[] , y=[], name = []))   #buckling length (visual)

    def reset(self):
        '''Member function made to reset the column to orginal position'''
        self.h              = self.hi
        self.deflection     = self.defi
        self.arrow.data     = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        self.labels.data    = dict(x=[], y=[], name = [])
        self.pts.data       = dict(x=[self.xstart, self.xstart], y=[zstart, zstart+self.hi])
        self.sk.data        = dict(x=[], y=[])
        self.sk_labels.data = dict(x=[], y=[], name = [])

    def fun_floor(self):
        '''Member function: creates the floor line for the column'''
        self.floor = dict(x = [self.xstart-1,self.xstart+1], y = [zstart, zstart])

    def fun_arrow(self):
        '''Member function: Creates Force arrow'''
        # stop adding force if critial force is reached
        if weight_slide.value < self.fcrit:
            arrow_length = weight_slide.value * fcrit_2
        else:
            arrow_length = self.fcrit
            
        #arrow_length *= 2.0 # scale arrow length  # could also be scaled with fcrit_2
        arrow_length += 0.38 # offset so that the arrow head glyph does not cover a small vector
        
        # add a bit for the starting case so that the glyphs point to the right direction (downwards)
        if np.isclose(arrow_length,0):
            arrow_length = 0.001
        
        xS = [self.pts.data['x'][-1]] # starting point x-coordinate
        xE = [self.pts.data['x'][-1]] # end point x-coordinate
        yS = [self.h + zstart + 0.5 + arrow_length] # starting point y-coordinate
        yE = [self.h + zstart + 0.5] # end point y-coordinate
        lW = [3] # line width
        self.arrow.data = dict(xS = xS, xE = xE , yS = yS, yE = yE, lW = lW)

    def fun_labels(self):
        '''Member Function: Creates labels of force arrows'''
        x                   = [self.pts.data['x'][-1]+1, self.xstart-.5]
        y                   = [self.h + zstart + 2  , 0]
        name                = ["F",self.name]
        self.labels.data    = dict(x = x, y = y, name = name)

weight_slide = Slider(title="Force Ratio (F/Fcrit)", value=0, start=0, end=f_end, step=step, width=450)    #slider created to change weight on columns

def drange(start,stop,step):
    '''Function created to provide float range'''
    r = start
    while r < stop:
        yield r
        r += step


col1 = Column("Free-Fixed",L,0.25*fcrit_2)                                      #beam: "Free-Fixed" Column
col2 = Column("Pinned-Pinned",L,fcrit_2)                                        #beam: "Pinned-Pinned" Column
col3 = Column("Pinned-Fixed",L,2.0*fcrit_2)                                     #beam: "Pinned-Fixed" Column
col4 = Column("Fixed-Fixed",L,4.0*fcrit_2)                                      #beam: "Fixed-Fixed" Column


#where the columns start on the graph:
col1.xstart = xstart
col2.xstart = xstart + 5.0
col3.xstart = xstart + 10.0
col4.xstart = xstart + 15.0

col1.pts.data=dict(x=[col1.xstart, col1.xstart], y=[zstart, zstart+col1.h])
col2.pts.data=dict(x=[col2.xstart, col2.xstart], y=[zstart, zstart+col2.h])
col3.pts.data=dict(x=[col3.xstart, col3.xstart], y=[zstart, zstart+col3.h])
col4.pts.data=dict(x=[col4.xstart, col4.xstart], y=[zstart, zstart+col4.h])


#, "name" = ["L","2L","3L","4L"]
#creation of the floors of the columns:
col1.fun_floor()
col2.fun_floor()
col3.fun_floor()
col4.fun_floor()
#col2.floor = dict(x = [col2.xstart-1,col2.xstart+1], y = [zstart-0.75,zstart-0.75])


#Creation of the pins, fixed upper boundary, walls, and horizontal arrow of w
col2.cir1   = dict(x = [col2.xstart] , y = [zstart])
col2.cir2   = ColumnDataSource(data=dict(x=[] , y=[]))
col3.cir2   = ColumnDataSource(data=dict(x=[] , y=[]))
col2.tri1   = dict(x = [col2.xstart] , y = [zstart-0.5])
col2.tri2   = ColumnDataSource(data=dict(x=[] , y=[]))
col3.tri2   = ColumnDataSource(data=dict(x=[] , y=[]))

col4.square = ColumnDataSource(data=dict(x=[] , y=[]))

col2.wall   = dict(x = [col2.xstart+1,col2.xstart+1] , y = [zstart+col2.hi+1,zstart+col2.hi-1])
col3.wall   = dict(x = [col3.xstart+1,col3.xstart+1] , y = [zstart+col3.hi+1,zstart+col3.hi-1])
col4.wall   = dict(x = [ [col4.xstart+0.5,col4.xstart+0.5] , [col4.xstart-0.5,col4.xstart-0.5] ],
y = [ [zstart+col4.hi+1,zstart+col4.hi-1] , [zstart+col4.hi+1,zstart+col4.hi-1] ] )
    


def fun_col1(x0,y0):
    '''Function: Calculates deflection in column 1'''
    y = np.linspace(0,col1.h,30)
    x = np.cos(np.pi/(2*col1.h)*y)-1
    col1.pts.data = dict(x = x0 + x, y = y0 + y) 
    col1.sk.data = dict(x=[col1.xstart+1.2, col1.xstart+1.8, col1.xstart+1.5, col1.xstart+1.5, col1.xstart+1.2, col1.xstart+1.8], y=[zstart, zstart, zstart, zstart+col1.h, zstart+col1.h, zstart+col1.h])
    #col1.sk_labels.data = dict(x=[col1.xstart+1.7], y=[zstart+0.5*col1.h], name=["sk/2 = L"])
    col1.sk_labels.data = dict(x=[col1.xstart+1.7], y=[zstart+0.5*col1.h], name=["\\frac{s_k}{2} = L"])

def fun_col2(x0,y0):
    '''Function: Calculates deflection in column 2'''
    y = np.linspace(0,col2.h,30)
    x = np.sin(np.pi/col2.h*y)
    col2.pts.data = dict(x = x0 + x, y = y0 + y)
    col2.sk.data = dict(x=[col2.xstart+1.2, col2.xstart+1.8, col2.xstart+1.5, col2.xstart+1.5, col2.xstart+1.2, col2.xstart+1.8], y=[zstart, zstart, zstart, zstart+col2.h, zstart+col2.h, zstart+col2.h])
    col2.sk_labels.data = dict(x=[col2.xstart+1.7], y=[zstart+0.5*col2.h], name=["s_k = L"])

def fun_col3(x0,y0):
    '''Function: Calculates deflection in column 3'''
    alph = 4.49/col3.h
    y = np.linspace(0,col3.h,30)
    x = np.cos(alph*y)-np.sin(alph*y)/(alph*col3.h) + y/col3.h -1
    col3.pts.data = dict(x = x0 + x, y = y0 + y)
    col3.sk.data = dict(x=[col3.xstart+1.2, col3.xstart+1.8, col3.xstart+1.5, col3.xstart+1.5, col3.xstart+1.2, col3.xstart+1.8], y=[zstart+0.3*col3.h, zstart+0.3*col3.h, zstart+0.3*col3.h, zstart+col3.h, zstart+col3.h, zstart+col3.h])
    #col3.sk_labels.data = dict(x=[col3.xstart+1.7], y=[zstart+0.5*col3.h], name=["sk = 0.7"u"\u00B7L"])
    col3.sk_labels.data = dict(x=[col3.xstart+1.7], y=[zstart+0.5*col3.h], name=["s_k = 0.7 \\cdot L"])

def fun_col4(x0,y0):
    '''Function: Calculates deflection in column 4'''
    y = np.linspace(0,col4.h,30)
    x = np.cos(2*np.pi/col4.h*y)-1
    col4.pts.data = dict(x = x0 + x, y = y0 + y)
    col4.sk.data = dict(x=[col4.xstart+1.2, col4.xstart+1.8, col4.xstart+1.5, col4.xstart+1.5, col4.xstart+1.2, col4.xstart+1.8], y=[zstart+0.25*col4.h, zstart+0.25*col4.h, zstart+0.25*col4.h, zstart+0.75*col4.h, zstart+0.75*col4.h, zstart+0.75*col4.h])
    #col4.sk_labels.data = dict(x=[col4.xstart+1.7], y=[zstart+0.5*col4.h], name=["sk = 0.5"u"\u00B7L"])
    col4.sk_labels.data = dict(x=[col4.xstart+1.7], y=[zstart+0.5*col4.h], name=["s_k = 0.5 \\cdot L"])

def fun_figures():
    '''Function: moves the figures in plot when columns buckle'''
    col2.cir2.data = dict(x= [ col2.pts.data['x'][-1] ], y=[col2.pts.data['y'][-1]])
    col3.cir2.data = dict(x=[col3.pts.data['x'][-1]], y=[col3.pts.data['y'][-1]])
    col2.tri2.data = dict(x=[col2.pts.data['x'][-1]+0.6], y=[col2.pts.data['y'][-1]])
    col3.tri2.data = dict(x=[col3.pts.data['x'][-1]+0.6], y=[col3.pts.data['y'][-1]])
    col4.square.data = dict(x=[col4.pts.data['x'][-1]], y=[col4.pts.data['y'][-1]-.2])

def init():
    '''Initializes plot. When Reset button is clicked, this is the function that is called'''
    global_old_slide_val.data = dict(val=[0])
    weight_slide.value    = 0
    col1.reset()
    col2.reset()
    col3.reset()
    col4.reset()
    fun_update(None,None,None)

def fun_check1(attr,old,new):
    '''fun_check1 checks whether slider value is less than previous slider value. If
    so, then the slider is kept at older value.'''
    [old_slide_val] = global_old_slide_val.data["val"]
    if weight_slide.value <= old_slide_val:
        weight_slide.value = old_slide_val
    elif weight_slide.value > old_slide_val:
        fun_update(attr,old,new)
    else:
        print "does not work"
    

def fun_update(attr,old,new):
    '''Function: Updates the plot when the weight slider is used'''
    
    #'abs(value -fcrit)<5*step' to avoid unnecessary function calls is still too fine
    # compare with '<' only
    #print(weight_slide.value)
    if weight_slide.value > col1.fcrit:
        fun_col1(col1.xstart,zstart)
    if weight_slide.value > col2.fcrit:
        fun_col2(col2.xstart,zstart)
    if weight_slide.value > col3.fcrit:
        fun_col3(col3.xstart,zstart)
    if weight_slide.value > col4.fcrit:
        fun_col4(col4.xstart,zstart)
    
    col1.fun_arrow()
    col2.fun_arrow()
    col3.fun_arrow()
    col4.fun_arrow()
    col1.fun_labels()
    col2.fun_labels()
    col3.fun_labels()
    col4.fun_labels()
    fun_figures()
    global_old_slide_val.data = dict(val=[weight_slide.value])
    


################################################################################
####Plotting section:
################################################################################


#Main plot:
plot = Figure(tools = "", x_range=(-2,window), y_range=(-.5,window))
# original position
plot.line(x=[col1.xstart,col1.xstart], y=[zstart,zstart+col1.h], color='gray',line_width=5, line_dash="6 4 2 4")
plot.line(x=[col2.xstart,col2.xstart], y=[zstart,zstart+col2.h], color='gray',line_width=5, line_dash="6 4 2 4")
plot.line(x=[col3.xstart,col3.xstart], y=[zstart,zstart+col3.h], color='gray',line_width=5, line_dash="6 4 2 4")
plot.line(x=[col4.xstart,col4.xstart], y=[zstart,zstart+col4.h], color='gray',line_width=5, line_dash="6 4 2 4")
# current column form
plot.line(x='x', y='y', source = col1.pts, color='#003359',line_width=5)        #Column 1
plot.line(x='x', y='y', source = col2.pts, color='#003359',line_width=5)        #Column 2
plot.line(x='x', y='y', source = col3.pts, color='#003359',line_width=5)        #Column 3
plot.line(x='x', y='y', source = col4.pts, color='#003359',line_width=5)        #Column 4
#Create the floors for each column:
plot.line(x='x', y='y', source = col1.floor, color='black',line_width=6)
plot.line(x='x', y='y', source = col2.floor, color='black',line_width=6)
plot.line(x='x', y='y', source = col3.floor, color='black',line_width=6)
plot.line(x='x', y='y', source = col4.floor, color='black',line_width=6)
#Create walls for columns that require a wall:
plot.line(x='x', y='y', source = col2.wall, color='black',line_width=6)
plot.line(x='x', y='y', source = col3.wall, color='black',line_width=6)
plot.multi_line(xs='x', ys='y', source = col4.wall, color='black',line_width=6)
#Create circles for columns that have pins:
plot.circle(x='x', y='y', source = col2.cir1, color='black',size = 10)
plot.circle(x='x', y='y', source = col2.cir2, color='black',size = 10)
plot.circle(x='x', y='y', source = col3.cir2, color='black',size = 10)
#Create the shapes of the ends of the columns:
plot.triangle(x='x', y='y', source = col2.tri1, color='black',angle =0.0,fill_alpha =0, size = 20)
plot.triangle(x='x', y='y', source = col2.tri2, color='black',angle =np.pi/2,fill_alpha =0, size = 20)
plot.triangle(x='x', y='y', source = col3.tri2, color='black',angle =np.pi/2,fill_alpha = 0, size = 20)
plot.square(x='x', y='y', source = col4.square, color='black',size = 20)
# Plot buckling lenghts
plot.line(x='x', y='y', source = col1.sk, color='orange',line_width=2)
plot.line(x='x', y='y', source = col2.sk, color='orange',line_width=2)
plot.line(x='x', y='y', source = col3.sk, color='orange',line_width=2)
plot.line(x='x', y='y', source = col4.sk, color='orange',line_width=2)

#Main plot properties:
plot.axis.visible = False
plot.grid.visible = False
plot.toolbar.logo = None
plot.outline_line_width = 1
plot.outline_line_alpha = 0.5
plot.outline_line_color = "Black"
plot.title.text_font_size = "18pt"
#plot.width = 900

#Arrow Glyph Section:
col1_a = Arrow(end=NormalHead(line_color="#A2AD00",line_width= 4, size=10),
x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=col1.arrow,line_color="#A2AD00")
col2_a = Arrow(end=NormalHead(line_color="#A2AD00",line_width= 4, size=10),
x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=col2.arrow,line_color="#A2AD00")
col3_a = Arrow(end=NormalHead(line_color="#A2AD00",line_width= 4, size=10),
x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=col3.arrow,line_color="#A2AD00")
col4_a = Arrow(end=NormalHead(line_color="#A2AD00",line_width= 4, size=10),
x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=col4.arrow,line_color="#A2AD00")

#Labels section:
# F and column name
labels1 = LabelSet(x='x', y='y', text='name', level='glyph',
              x_offset=-20, y_offset=0, source=col1.labels, render_mode='canvas')
labels2 = LabelSet(x='x', y='y', text='name', level='glyph',
              x_offset=-20, y_offset=0, source=col2.labels, render_mode='canvas')
labels3 = LabelSet(x='x', y='y', text='name', level='glyph',
              x_offset=-20, y_offset=0, source=col3.labels, render_mode='canvas')
labels4 = LabelSet(x='x', y='y', text='name', level='glyph',
              x_offset=-20, y_offset=0, source=col4.labels, render_mode='canvas')

# buckling length
sk_l1 = LatexLabelSet(x='x', y='y', text='name', level='glyph', angle=np.pi*0.5, text_color="orange",
              x_offset=-12, y_offset=15,    source=col1.sk_labels, render_mode='canvas', display_mode=True)
sk_l2 = LatexLabelSet(x='x', y='y', text='name', level='glyph', angle=np.pi*0.5, text_color="orange",
              x_offset=-12, y_offset=15,    source=col2.sk_labels, render_mode='canvas', display_mode=True)
sk_l3 = LatexLabelSet(x='x', y='y', text='name', level='glyph', angle=np.pi*0.5, text_color="orange",
              x_offset=-28, y_offset=50,    source=col3.sk_labels, render_mode='canvas', display_mode=True)
sk_l4 = LatexLabelSet(x='x', y='y', text='name', level='glyph', angle=np.pi*0.5, text_color="orange",
              x_offset=-28, y_offset=2,    source=col4.sk_labels, render_mode='canvas', display_mode=True)
#sk_l1 = LabelSet(x='x', y='y', text='name', level='glyph', angle=np.pi*0.5, text_color="orange",
#              x_offset=-10, y_offset=0,    source=col1.sk_labels, render_mode='canvas')
#sk_l2 = LabelSet(x='x', y='y', text='name', level='glyph', angle=np.pi*0.5, text_color="orange",
#              x_offset=+11, y_offset=0,    source=col2.sk_labels, render_mode='canvas')
#sk_l3 = LabelSet(x='x', y='y', text='name', level='glyph', angle=np.pi*0.5, text_color="orange",
#              x_offset=-10, y_offset=0,    source=col3.sk_labels, render_mode='canvas')
#sk_l4 = LabelSet(x='x', y='y', text='name', level='glyph', angle=np.pi*0.5, text_color="orange",
#              x_offset=-10, y_offset=0,    source=col4.sk_labels, render_mode='canvas')

#label properties
labels1.text_font_size = '10pt'
labels2.text_font_size = '10pt'
labels3.text_font_size = '10pt'
labels4.text_font_size = '10pt'

sk_l1.text_font_size = '10pt'
sk_l2.text_font_size = '10pt'
sk_l3.text_font_size = '10pt'
sk_l4.text_font_size = '10pt'

#Add layouts of arrows and labels in to plot:
plot.add_layout(col1_a)
plot.add_layout(col2_a)
plot.add_layout(col3_a)
plot.add_layout(col4_a)

plot.add_layout(labels1)
plot.add_layout(labels2)
plot.add_layout(labels3)
plot.add_layout(labels4)

plot.add_layout(sk_l1)
plot.add_layout(sk_l2)
plot.add_layout(sk_l3)
plot.add_layout(sk_l4)


################################################################################

#Create Reset Button:
button = Button(label="Reset", button_type="success", width=50)

#Let program know what functions button calls when clicked:
weight_slide.on_change('value', fun_check1)
button.on_click(init)

#Initialization at the beginning:
init()

# add app description
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)

description1_filename = join(dirname(__file__), "description1.html")
description1 = LatexDiv(text=open(description1_filename).read(), render_as_text=False, width=1200)

################################################################################
####Output section
################################################################################
#Output to the browser:
curdoc().add_root(column(description1, plot, row(weight_slide, Spacer(width=50), button), description))

curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
