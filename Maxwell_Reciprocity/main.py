from bokeh.plotting import Figure#, output_file , show
from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, NormalHead, Arrow#, Div
from bokeh.layouts import column, row#, widgetbox
from bokeh.models.widgets import Button
from bokeh.models.glyphs import Text
from bokeh.io import curdoc
#import numpy as np
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv

# external files
from Maxwell_Frame import Maxwell_Frame
import Maxwell_Constants as glc
import Maxwell_BettyDisplacements as MBD
from Maxwell_Frame_Functions import create_prof, create_shift, create_wdline

#################################################################################
##global constants:
#################################################################################
# see Maxwell_Constants.py

################################################################################
###Creation of frames
################################################################################
orig        = Maxwell_Frame("o","0")                                                    #Creation of original frame. This frame is a reference of the original location
default     = dict(x = [0.1,0.8], y = [0.1,0.1], size = [glc.tri_size,glc.tri_size])    #Creation of triangle of original frame
t_line      = dict(x=[0.7,0.9], y=[glc.ground,glc.ground])                              #Creation of Line
# frame 1 and 2 are created in Maxwell_BettyDisplacements


################################################################################
###Sliders and buttons
################################################################################

#Magnitude of load slider:
mag_start   = -100
mag_end     = 100
mag_val     = 0
mag_slider  = Slider(title="Magnitude", value=mag_val,
    start=mag_start, end=mag_end, step=1)

#Position of load slider:
loc_start = 0
loc_end = 100
loc_val = 50
loc_slider = Slider(title="Position", value=loc_val,
    start=loc_start, end=loc_end, step=1)

#Toggle buttons:
button = Button(label="Save Deformed Frame", button_type="success")             #Button to save the deformed frain. Calls function
rbutton = Button(label="Reset", button_type="success")                          #Reset button. Calls init function


################################################################################
###Functions
################################################################################

def create_orig(o):
    '''Creates stationary original frame'''
    x = [o.x0,o.x0,o.xf,o.xf]
    y = [o.y0,o.yf,o.yf,o.y0]
    o.pts.data = dict(x = x, y = y)



def update_fun(attr,old,new):
    '''This is the function that is called each time the sliders are used. It
    Changes the values of the frames and moves them. Most of the functions are
    called in update_fun
    changer == 0 means that the 'save deformed frame' button has not been
    pressed yet.
    changer == 1 is when the button has been pressed and MBD.f2 is created'''
    [changer] = glc.glob_changer.data["val"] # input/
    if changer == 0:
        MBD.f1.set_param(loc_slider.value)
        MBD.f1.set_mag(mag_slider.value)
        MBD.f2.p_mag = MBD.f1.p_mag 
        create_prof(MBD.f1)
        create_shift(MBD.f1)
        MBD.f1.tri.data = dict(x = [0.1,MBD.f1.pts.data["x"][-1]], y = [0.1,0.1], size = [glc.tri_size,glc.tri_size])
        create_wdline(MBD.f1)

    elif changer != 0:
        MBD.f2.set_param(loc_slider.value)
        create_prof(MBD.f2)
        create_shift(MBD.f2)
        MBD.f2.p_mag = MBD.f1.p_mag 

        #EDIT Start
        MBD.calc_betty_displacements12(MBD.f2)
        MBD.calc_betty_displacements21(MBD.f2)
        MBD.f2.tri.data = dict(x = [0.1,MBD.f2.pts.data["x"][-1]], y = [0.1,0.1], size = [glc.tri_size,glc.tri_size])
        create_wdline(MBD.f2)
        MBD.f1.tri.data = dict(x = [0.1,MBD.f1.pts.data["x"][-1]], y = [0.1,0.1], size = [glc.tri_size,glc.tri_size])
        #EDIT End

def button_fun():
    '''Function called when the 'save deformed frame' function is clicked.
    This button changes the changer value to 1, which affects update_fun
    (see update_fun for more details.) it also switches MBD.f2 to MBD.f1 if MBD.f2 already
    exists.'''
    glc.glob_changer.data=dict(val=[1]) #      /output
    MBD.f1.set_param(loc_slider.value)
    MBD.f1.set_mag(mag_slider.value)
    create_prof(MBD.f1)
    create_shift(MBD.f1)
    create_wdline(MBD.f1)
    loc_slider.value    = loc_val
    MBD.f2.p_mag        = MBD.f1.p_mag
    mag_slider.disabled = True
    button.disabled     = True
    

def initial():
    '''Function that initializes everything'''
    glc.glob_changer.data = dict(val=[0]) #      /output
    mag_slider.value  = mag_val
    loc_slider.value  = loc_val
    clearMBDf1()
    clearMBDf2()
    mag_slider.disabled = False
    button.disabled     = False

def clearMBDf1():
    '''Clears the MBD.f1 frame'''
    MBD.f1.pts.data             = dict(x = [], y = [] )
    MBD.f1.label.data           = dict(x=[0.45] , y=[0.62], name = [ "F"u"\u2081"])
    #MBD.f1.arrow_source.data    = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    MBD.f1.arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=-1)
    #MBD.f1.pts.data             = dict(x = [], y = [] )
    MBD.f1.e_s.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=-1)
    MBD.f1.tri.data             = dict(x = [], y = [], size = [])
    MBD.f1.seg.data             = dict(x0=[], x1=[], y0=[], y1=[])
    MBD.f1.dline.data           = dict(x=[], y=[])
    MBD.f1.dlabel.data          = dict(x=[] , y=[], name = [])
    #MBD.f1.w1.data              = dict(xS=[], xE=[], yS=[], yE=[], name = [])
    #MBD.f1.w2.data              = dict(xS=[], xE=[], yS=[], yE=[])
    MBD.f1.w1.stream(dict(xS=[], xE=[], yS=[], yE=[], name = []),rollover=-1)
    MBD.f1.w2.stream(dict(xS=[], xE=[], yS=[], yE=[]),rollover=-1)
    #MBD.f1.wdline.data          = dict(x1=[], x2 =[], y1 = [], y2=[])
    MBD.f1.wdline.stream(dict(x1=[], x2 =[], y1 = [], y2=[]),rollover=-1)

def clearMBDf2():
    '''Clears the MBD.f2 frame'''
    MBD.f2.pts.data             = dict(x = [], y = [] )
    MBD.f2.label.data           = dict(x=[] , y=[], name = [])
    #MBD.f2.arrow_source.data    = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    MBD.f2.arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=-1)    
    MBD.f2.tri.data             = dict(x = [], y = [], size = [])
    MBD.f2.e_s.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=-1)
    MBD.f2.set_param(loc_val)
    MBD.f2.set_mag(mag_val)
    MBD.f2.seg.data             = dict(x0=[], x1=[], y0=[], y1=[])
    MBD.f2.dline.data           = dict(x=[], y=[])
    MBD.f2.dlabel.data          = dict(x=[] , y=[], name = [])
    #MBD.f2.w1.data              = dict(xS=[], xE=[], yS=[], yE=[], name = [])
    MBD.f2.w1.stream(dict(xS=[], xE=[], yS=[], yE=[], name = []),rollover=-1)
    MBD.f2.w2.stream(dict(xS=[], xE=[], yS=[], yE=[]),rollover=-1)
    #MBD.f2.w2.data              = dict(xS=[], xE=[], yS=[], yE=[])
    MBD.f1.w1.stream(dict(xS=[], xE=[], yS=[], yE=[], name = []),rollover=-1)
    #print(MBD.f1.w2.data)
    MBD.f1.w2.stream(dict(xS=[], xE=[], yS=[], yE=[]),rollover=-1)
    #print(MBD.f1.w2.data)
    #EDIT Start
    #MBD.f2.w12.data             = dict(xS=[], xE=[], yS=[], yE=[], name = [])
    #MBD.f2.w12_11.data             = dict(xS=[], xE=[], yS=[], yE=[])
    #MBD.f2.w12_12.data           = dict(xS=[], xE=[], yS=[], yE=[])
    #MBD.f2.w21.data           = dict(xS=[], xE=[], yS=[], yE=[], name = [])
    MBD.f2.w12.stream(dict(xS=[], xE=[], yS=[], yE=[], name = []),rollover=-1)
    MBD.f2.w12_11.stream(dict(xS=[], xE=[], yS=[], yE=[]),rollover=-1)
    MBD.f2.w12_12.stream(dict(xS=[], xE=[], yS=[], yE=[]),rollover=-1)
    MBD.f2.w21.stream(dict(xS=[], xE=[], yS=[], yE=[], name = []),rollover=-1)
    #MBD.f2.w21_11.data           = dict(xS=[], xE=[], yS=[], yE=[])
    #MBD.f2.w21_12.data           = dict(xS=[], xE=[], yS=[], yE=[])
    MBD.f2.w21_11.stream(dict(xS=[], xE=[], yS=[], yE=[]),rollover=-1)
    MBD.f2.w21_12.stream(dict(xS=[], xE=[], yS=[], yE=[]),rollover=-1)
    #MBD.f2.wdline.data          = dict(x1=[], x2 =[], y1 = [], y2=[])
    MBD.f2.wdline.stream(dict(x1=[], x2 =[], y1 = [], y2=[]),rollover=-1)
    #MBD.f2.wdline12.data          = dict(x1=[], x2 =[], y1 = [], y2=[])   
    #MBD.f2.wdline21.data          = dict(x1=[], x2 =[], y1 = [], y2=[])
    MBD.f2.wdline12.stream(dict(x1=[], x2 =[], y1 = [], y2=[]),rollover=-1)   
    MBD.f2.wdline21.stream(dict(x1=[], x2 =[], y1 = [], y2=[]),rollover=-1)
    #EDIT End

button.on_click(button_fun)
rbutton.on_click(initial)
loc_slider.on_change('value', update_fun)
mag_slider.on_change('value', update_fun)

################################################################################
###Main section
################################################################################

create_orig(orig)                                                               #Stationary frame is created
initial()


################################################################################
###Plot Section
################################################################################

#Plot constants
abshift = 0.02                                                                  #this is the size of the end-lines of the scale parameters a and b
xb      = -0.015                                                                #xb shift used in a and b creation
MBD.f1color = "#0065BD"                                                             #TUM approved color for MBD.f1 (blue)
MBD.f2color = "#E37222"                                                             #TUM approved color for MBD.f2 (orange)

########Main PLot:
plot = Figure(tools = "", x_range=(glc.plotx0,glc.plotxf),
        y_range=(glc.ploty0,glc.plotyf),plot_width=750, plot_height=650)
#Plot properties:
plot.axis.visible = False
plot.grid.visible = False
plot.toolbar.logo = None
plot.outline_line_width = 1
plot.outline_line_alpha = 0.3
plot.outline_line_color = "Black"
plot.title.text_color = "black"
plot.title.text_font_style = "bold"
plot.title.align = "center"
#########

#Plot of frames
plot.line(x='x', y='y', source=orig.pts, color="grey",line_width=3)             #Original stationary frame
plot.line(x='x', y='y', source=MBD.f1.pts, color=MBD.f1color,line_width=5)              #Frame 1
plot.line(x='x', y='y', source=MBD.f2.pts, color=MBD.f2color,line_width=5)              #Frame 2
plot.line(x='x', y='y', source=t_line, color="Black",line_width=5)              #Black line under frame righthandside

###Dashed Lines:

#dashed line that follows the deformations:
plot.line(x = 'x1' , y = 'y1',source = MBD.f1.wdline, color="Black",
        line_width=2,line_dash = 'dashed',line_alpha = 0.3)
plot.line(x = 'x2' , y = 'y2',source = MBD.f1.wdline, color="Black",
        line_width=2,line_dash = 'dashed',line_alpha = 0.3)
plot.line(x = 'x1' , y = 'y1',source = MBD.f2.wdline, color="Black",
        line_width=2,line_dash = 'dashed',line_alpha = 0.3)
plot.line(x = 'x2' , y = 'y2',source = MBD.f2.wdline, color="Black",
        line_width=2,line_dash = 'dashed',line_alpha = 0.3)

#EDIT Start
plot.line(x = 'x1' , y = 'y1',source = MBD.f2.wdline12, color=MBD.f1color,
        line_width=2,line_dash = 'dashed',line_alpha = 0.5)
plot.line(x = 'x2' , y = 'y2',source = MBD.f2.wdline12, color=MBD.f1color,
        line_width=2,line_dash = 'dashed',line_alpha = 0.5)
plot.line(x = 'x1' , y = 'y1',source = MBD.f2.wdline21, color=MBD.f2color,
        line_width=2,line_dash = 'dashed',line_alpha = 0.3)
plot.line(x = 'x2' , y = 'y2',source = MBD.f2.wdline21, color=MBD.f2color,
        line_width=2,line_dash = 'dashed',line_alpha = 0.3)      
 #EDIT End   

#creation of the a and b scale reference things:
plot.multi_line( [ [orig.x0, orig.xf],[orig.x0,orig.x0],[orig.xf,orig.xf] ],
        [ [0,0] ,[0-abshift,0+abshift] , [0-abshift,0+abshift] ],
        color=["black", "black","black"], line_width=1)
plot.multi_line( [ [xb,xb],[xb-abshift,xb+abshift],[xb-abshift,xb+abshift] ],
        [ [orig.y0,orig.yf], [orig.y0,orig.y0], [orig.yf,orig.yf] ],
        color=["black", "black","black"], line_width=1)

#Frame bases
plot.triangle(x='x', y='y', size = 'size', source= default,color="grey", line_width=2)
plot.triangle(x='x', y='y', size = 'size', source= MBD.f1.tri,color=MBD.f1color, line_width=2)
plot.triangle(x='x', y='y', size = 'size', source= MBD.f2.tri,color=MBD.f2color, line_width=2)



#######labels
labels1 = LabelSet(x='x', y='y', text='name', level='glyph',
              x_offset=0, y_offset=0, source=MBD.f1.label, text_color=MBD.f1color,
              text_font_size = '16pt',  render_mode='canvas')
labels2 = LabelSet(x='x', y='y', text='name', level='glyph',
              x_offset=0, y_offset=0, source=MBD.f2.label,text_color=MBD.f2color,
              text_font_size = '16pt', render_mode='canvas')
labelsn1 = LabelSet(x='x', y='y', text='name', level='glyph',
              x_offset=0, y_offset=-20, source=MBD.f1.dlabel,text_color=MBD.f1color,
              text_font_size = '10pt', render_mode='canvas')
labelsn2 = LabelSet(x='x', y='y', text="name", level='glyph',
              x_offset=0, y_offset=-20, source=MBD.f2.dlabel,text_color=MBD.f2color,
              text_font_size = '10pt', render_mode='canvas')

labelsw1 = LabelSet(x='xS', y = 'yS', text='name', level='glyph',
                x_offset=0, y_offset=-20,source = MBD.f1.w1, text_color=MBD.f1color,
                text_font_size = '12pt', render_mode='canvas')
labelsw2 = LabelSet(x='xE', y = 'yS', text='name', level='glyph',
                x_offset=0, y_offset=10,source = MBD.f2.w1, text_color=MBD.f2color,
                text_font_size = '12pt', render_mode='canvas')

#EDIT Start
labelsw12 = LabelSet(x='xS', y = 'yS', text='name', level='glyph',
                x_offset=0, y_offset=-20,source = MBD.f2.w12, text_color=MBD.f1color,
                text_font_size = '12pt', render_mode='canvas')
labelsw21 = LabelSet(x='xS', y = 'yS', text='name', level='glyph',
                x_offset=0, y_offset=-20,source = MBD.f2.w21, text_color=MBD.f2color,
                text_font_size = '12pt', render_mode='canvas')                
#EDIT End

absource = ColumnDataSource(dict(x=[ (orig.x0+orig.xf)/2,
        (0-0.05)], y=[ (0-0.05), (orig.y0+orig.yf)/2 ], text=['a','b']))

abtext_glyph = Text( x='x' , y='y', text='text' ,text_color="Black",
        text_font_size="16pt",text_font_style = "italic")



########

#######Arrows:
#P arrow:
p1_arrow_glyph = Arrow(end=NormalHead(line_color=MBD.f1color,line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=MBD.f1.arrow_source,line_color=MBD.f1color)
p2_arrow_glyph = Arrow(end=NormalHead(line_color=MBD.f2color,line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=MBD.f2.arrow_source,line_color=MBD.f2color)

#e arrow:
e1_arrow_glyph = Arrow(end=OpenHead(line_color=MBD.f1color,line_width= 3, size=6,line_alpha = 0.5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= 4, source=MBD.f1.e_s,line_color=MBD.f1color,line_alpha = 0.5)
e2_arrow_glyph = Arrow(end=OpenHead(line_color=MBD.f2color,line_width= 3, size=6,line_alpha = 0.5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= 4, source=MBD.f2.e_s,line_color=MBD.f2color,line_alpha = 0.5)

#MBD.f1 w11 arrow
w11_arrow_glyph = Arrow(end=OpenHead(line_color=MBD.f1color,line_width= 3, size=6,line_alpha = 0.3),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= 4, source=MBD.f1.w1,line_color=MBD.f1color,line_alpha = 0.3)
w12_arrow_glyph = Arrow(end=OpenHead(line_color=MBD.f1color,line_width= 3, size=6,line_alpha = 0.3),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= 4, source=MBD.f1.w2,line_color=MBD.f1color,line_alpha = 0.3)

#EDIT Start
#MBD.f1 w12 arrow
w12_11_arrow_glyph = Arrow(end=OpenHead(line_color=MBD.f1color,line_width= 3, size=6,line_alpha = 0.5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= 4, source=MBD.f2.w12_11,line_color=MBD.f1color,line_alpha = 0.5)
w12_12_arrow_glyph = Arrow(end=OpenHead(line_color=MBD.f1color,line_width= 3, size=6,line_alpha = 0.5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= 4, source=MBD.f2.w12_12,line_color=MBD.f1color,line_alpha = 0.5)
#EDIT End

#MBD.f2 w22 arrow
w21_arrow_glyph = Arrow(end=OpenHead(line_color=MBD.f2color,line_width= 3, size=6,line_alpha = 0.3),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= 4, source=MBD.f2.w1,line_color=MBD.f2color,line_alpha = 0.3)
w22_arrow_glyph = Arrow(end=OpenHead(line_color=MBD.f2color,line_width= 3, size=6,line_alpha = 0.3),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= 4, source=MBD.f2.w2,line_color=MBD.f2color,line_alpha = 0.3)

#EDIT Start
#MBD.f2 w21 arrow
w21_11_arrow_glyph = Arrow(end=OpenHead(line_color=MBD.f2color,line_width= 3, size=6,line_alpha = 0.5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= 4, source=MBD.f2.w21_11,line_color=MBD.f2color,line_alpha = 0.5)
w21_12_arrow_glyph = Arrow(end=OpenHead(line_color=MBD.f2color,line_width= 3, size=6,line_alpha = 0.5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= 4, source=MBD.f2.w21_12,line_color=MBD.f2color,line_alpha = 0.5)
#EDIT End
########


########Layout adding
#Adding the arrows and labels to the plot:
plot.add_layout(p1_arrow_glyph)
plot.add_layout(p2_arrow_glyph)
plot.add_layout(e1_arrow_glyph)
plot.add_layout(e2_arrow_glyph)
plot.add_layout(w11_arrow_glyph)
plot.add_layout(w12_arrow_glyph)
plot.add_layout(w21_arrow_glyph)
plot.add_layout(w22_arrow_glyph)

#EDIT Start
plot.add_layout(w12_11_arrow_glyph)
plot.add_layout(w12_12_arrow_glyph)
plot.add_layout(w21_11_arrow_glyph)
plot.add_layout(w21_12_arrow_glyph)
#EDIT End

plot.add_glyph(absource,abtext_glyph)
plot.add_layout(labels1)
plot.add_layout(labels2)
#plot.add_layout(labelsn1)
#plot.add_layout(labelsn2)
plot.add_layout(labelsw1)
plot.add_layout(labelsw2)

#EDIT Start
plot.add_layout(labelsw12)
plot.add_layout(labelsw21)
#EDIT End

#########


################################################################################
###add app description
################################################################################
description_filename = join(dirname(__file__), "description.html")
description1_filename = join(dirname(__file__), "description1.html")

description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=750)
description1 = LatexDiv(text=open(description1_filename).read(), render_as_text=False, width=750)

################################################################################
###Send to the browser
################################################################################
curdoc().add_root( column(description,column(plot,row(mag_slider, loc_slider), row(button,rbutton), description1 ) ))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
