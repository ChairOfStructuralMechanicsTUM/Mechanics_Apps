#main file:

from bokeh.plotting import Figure, output_file , show
from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, Arrow
from bokeh.models.glyphs import ImageURL
from bokeh.models.layouts import Spacer
from bokeh.layouts import column, row, widgetbox
from bokeh.io import curdoc
from bokeh.models.widgets import Button, CheckboxGroup
import numpy as np
from os.path import dirname, join, split

#Global Beam Properties:
resol = 100             #EDIT: resolution?
x0 = 0                  #starting value of beam
xf = 10                 #ending value of beam
E  = 500.0e1            #modulus of elasticity
I  = 30                 #moment of inertia
length  = xf-x0         #length of beam
p_mag = 0.5               #initialize the p force
p_magi = 0.5
p_loci = xf/2
f2_loci = xf
lthi = 2
plotwidth = 20
#Sources:
#Plot source:
plot_source = ColumnDataSource(data=dict(x = np.linspace(x0,xf,resol), y = np.ones(resol) * 0 ))
#Moment Source:
mom_source = ColumnDataSource(data=dict(x=[] , y=[]))
#Shear Source:
shear_source = ColumnDataSource(data=dict(x=[] , y=[]))
#Arrow Sources:
p_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
f2_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
f1_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
#label_source:
labels_source = ColumnDataSource(data=dict(x=[] , y=[],name = []))
#Support Source:
support1 = "Balken_AD/static/images/auflager02.svg"
support2 = "Balken_AD/static/images/auflager01.svg"
support_source1 = ColumnDataSource(data=dict(sp1=[], x=[] , y=[]))
support_source2 = ColumnDataSource(data=dict(sp2=[], x=[] , y=[]))
#Triangle source:
#triangle_source = ColumnDataSource(data=dict(x= [], y= [], size = []))
#Cantilever rectangle source:
quad_source = ColumnDataSource(data=dict(top= [], bottom= [],left = [], right =[]))
segment_source = ColumnDataSource(data=dict(x0= [], y0= [],x1 = [], y1 =[]))
#Sliders:
p_loc_slide= Slider(title="Load Position",value= p_loci,start = x0, end = xf, step = 1)
p_mag_slide = Slider(title="Load Amplitude", value=p_mag, start=-2*p_mag, end=2*p_mag, step=.1)
f2_loc_slide = Slider(title="Support Position",value=f2_loci,start = x0, end = xf, step = 1)
lth_slide = Slider(title="Beam-Height",value=lthi ,start = 2, end = 20, step = 1)

#FUNCTION: Calculate Force at Support 1
def Fun_F(p_mag,b,l):
    f1_mag = -1.0 * (p_mag *b) / l
    return f1_mag

#FUNCTION: Calculation of Max MOMENT
def Fun_Moment(p,a,b,l):
    mom_max = -(p * a * b ) / l
    #x is 0, pcoord, f2_coord
    #y is 0, mom_max, 0
    return mom_max

#FUNCTION: Calculation of deflection:
def Fun_Deflection(a,b,l,p,x):
    ynew = []
    ynew1 = []
    ynew2 = []
    for i in range(0,int(l*(resol/10) ) ):
        if a > l:
            dy = ( ( p * b * x[i]) / (6 * E * I * l) ) * ( (l**2) - (x[i]**2) )
        else:
            if x[i] < a:
                dy = ( ( p * b * x[i]) / (6 * E * I * l) ) * ( (l**2) - (b**2) - (x[i]**2) )
            elif x[i] == a:
                dy = ( p * (a**2) * (b**2) ) / (3 * E * I * l)
            elif x[i] > a and x[i] <= l:
                dy = ( (p * a * (l-x[i]) ) / (6 * E * I * l) ) * ( (2*l*x[i]) - (x[i]**2) - (a**2) )

        ynew1.append(dy)

    new_range = int(resol - l*10)
    for i in range(0,new_range):
        dy1 = -1 *( ( (p * a * b * x[i]) / (6 * E * I * l) ) * (l + a) )
        ynew2.append(dy1)

    ynew = ynew1 + ynew2
    return ynew



#FUNCTION: Cantilever Deflection function:
def Fun_C_Deflection(p,b,x):
    '''Calculates the deflection of the beam when it is cantilever'''
    #b is the distance from the wall to the concentrated load

    ynew = []
    a = xf - b;     #The a for cantilever is the distance between
                    #the free end and the concentrated load.
    for i in range(0,resol):
        if x[i] < a:
            #dy = (  ( p * ( ( xf - x[i])**2 ) ) / (6 * E * I) ) * ( (3*b) - xf + x[i] )
            dy = (  ( p * (b**2) ) / (6 * E * I)  ) * ( (3*xf) - (3*x[i]) - b )
        elif x[i] == a:
            dy = ( p * (b**3) ) / (3 * E * I)
        elif x[i] > a:
            #dy = (  ( p * (a**2) ) / (6 * E * I)  ) * ( (3*xf) - (3*x[i]) - a )
            dy = (  ( p * ( ( xf - x[i])**2 ) ) / (6 * E * I) ) * ( (3*b) - xf + x[i] )
        ynew.append(dy)

    return list(reversed(ynew))     #need to reverse because x is calculated in the opposite direction

#FUNCTION: Function that's called when mitschub is checked:
def Fun_WithShear():
#4.0 * (Mq(x, q) + MF(x, F)) / (l_h ^2);
    pass

#FUNCTION: Cantilever function:
#When position 2 is 0, this function is called:
def Fun_Cantilever():
    #triangle_source.data = dict(x = [], y = [], size = [])
    f1_arrow_source.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [])
    f2_arrow_source.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [])
    top = 2
    bottom  = -top
    left = -1
    right = 0
    clines = 40
    quad_source.data = dict(top = [top], bottom = [bottom], left = [left] , right = [right])
    xseg = np.ones(clines) * left
    yseg = np.linspace(bottom,top-0.2,clines)
    x1seg = np.ones(clines) * right
    y1seg = np.linspace(bottom+0.2,top,clines)
    segment_source.data = dict(x0= xseg, y0= yseg,x1 = x1seg, y1 =y1seg)
    ###
    support_source2.data = dict(sp2=[], x = [] , y = [])
    support_source1.data = dict(sp1=[], x = [] , y = [])

#FUNCTION: Update:
def Fun_Update(attrname, old, new):
    #values used by both cases:
    my_line.glyph.line_width = 15
    a = p_loc_slide.value
    f2_coord = f2_loc_slide.value
    b = f2_coord - a
    p_coord = p_loc_slide.value
    p_mag = p_mag_slide.value
    l = f2_coord
    x1 = xf - l

    if f2_coord == 0:
        xcan = x0
        Fun_Cantilever()

        if (p_mag<0):
            p_arrow_source.data = dict(xS= [p_coord], xE= [p_coord], yS= [1-(p_mag/1.0)], yE=[1], lW = [2] )
            labels_source.data = dict(x = [p_coord] , y = [1],name = ['F'])
        else:
            p_arrow_source.data = dict(xS= [p_coord], xE= [p_coord], yS= [-1-(p_mag/1.0)], yE=[-1], lW = [2] )
            labels_source.data = dict(x = [p_coord] , y = [-1],name = ['F'])

        #cantilever moment calculation:
        #max moment at fixed end x0. Moment max = P*l
        m_max = (p_mag * a)/6
        mom_source.data = dict(x=[xcan,a,xf] , y=[m_max,0,0])
        shear_source.data = dict(x=[xcan,a,a,xf], y=[p_mag,p_mag,0,0])

        if checkbox.active == [0]:
            ynew = Fun_C_Deflection(p_mag,a,plot_source.data['x'])
            plot_source.data = dict(x = np.linspace(x0,xf,resol), y = ynew)
        elif checkbox.active == []:
            plot_source.data= dict( x = np.linspace(x0,xf,resol) , y = np.ones(resol) * 0)
        # elif checkbox.active == [1]:
        #     checkbox.active = []
        # elif checkbox.active == [0,1]:
        #     ynew = Fun_C_Deflection(p_mag,a,plot_source.data['x'])
        #     plot_source.data = dict(x = np.linspace(x0,xf,resol), y = ynew)
        #     print 'this would be mit schub'
        else:
            print 'fatal error'

#####################
    else: ##this else is what determines whether or not the figure is in cantilever mode
#####################
        quad_source.data = dict(top = [], bottom = [], left = [] , right = [])
        segment_source.data = dict(x0= [], y0= [],x1 = [], y1 =[])

        f1_mag = Fun_F(p_mag_slide.value,b,l)
        f2_mag = Fun_F(p_mag_slide.value,a,l)
        ynew = Fun_Deflection(a,b,l,p_mag,plot_source.data['x'])
        plot_source.data = dict(x = np.linspace(x0,xf,resol), y = ynew)
        # if checkbox.active == [0]:
        #     ynew = Fun_Deflection(a,b,l,p_mag,plot_source.data['x'])
        #     plot_source.data = dict(x = np.linspace(x0,xf,resol), y = ynew)
        # elif checkbox.active == []:
        #     plot_source.data= dict( x = np.linspace(x0,xf,resol) , y = np.ones(resol) * 0)
        # elif checkbox.active == [1]:
        #     checkbox.active = []
        # elif checkbox.active == [0,1]:
        #     ynew = Fun_Deflection(a,b,l,p_mag,plot_source.data['x'])
        #     plot_source.data = dict(x = np.linspace(x0,xf,resol), y = ynew)
        #     print 'this would be mit schub'
        # else:
        #     print 'fatal error'

        #print plot_source.data['y']

        move_tri = -0.4
        #triangle_source.data = dict(x = [0.0,f2_loc_slide.value], y = [0+move_tri, 0+move_tri], size = [20,20])

        #moment and shear:
        m_max = Fun_Moment(p_mag_slide.value,a,b,l)
        if (l >= a):
            mom_source.data = dict(x=[0,a,l,xf] , y=[0,m_max,0,0])
            shear_source.data = dict(x=[0,a,a,l,xf], y=[f1_mag,f1_mag,-f2_mag,-f2_mag,-f2_mag])
        else:
            mom_source.data = dict(x=[0,l,a,xf] , y=[0,m_max,0,0])
            shear_source.data = dict(x=[0,l,l,a,xf], y=[f1_mag,f1_mag,-p_mag,-p_mag,-p_mag])

        #p_arrow and labels:
        if (p_mag<0):
            p_arrow_source.data = dict(xS= [p_coord], xE= [p_coord], yS= [1-(p_mag/1.0)], yE=[1], lW = [2] )
            labels_source.data = dict(x = [p_coord,0,f2_coord-0.2] , y = [1,move_tri,move_tri],name = ['F','A','B'])
            support_source2.data = dict(sp2=[support2], x = [f2_coord-0.33] , y = [-0.1])
            support_source1.data = dict(sp1=[support1], x= [-0.325], y= [-0.1])
        else:
            p_arrow_source.data = dict(xS= [p_coord], xE= [p_coord], yS= [-1-(p_mag/1.0)], yE=[-1], lW = [2] )
            labels_source.data = dict(x = [p_coord,-0.2,f2_coord-0.2] , y = [-1,move_tri,move_tri],name = ['F','A','B'])
            support_source2.data = dict(sp2=[support2], x = [f2_coord-0.33] , y = [-0.1])
            support_source1.data = dict(sp1=[support1], x= [-0.325], y= [-0.1])
        #f1_arrow:
        #if (f1_mag==0):
            #f1_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        if (f1_mag<=-p_magi):
            f1_arrow_source.data = dict(xS= [0], xE= [0], yS= [1-(f1_mag/1)], yE=[0.8], lW = [2])
        elif ( f1_mag>-p_magi ) & ( f1_mag<=0 ):
            f1_arrow_source.data = dict(xS= [0], xE= [0], yS= [1-(f1_mag/1)], yE=[0.8], lW = [2])
        elif (f1_mag > 0) & ( f1_mag < p_magi ):
            f1_arrow_source.data = dict(xS= [0], xE= [0], yS= [-1-(f1_mag/1)], yE=[-0.8], lW = [2] )
        else:
            f1_arrow_source.data = dict(xS= [0], xE= [0], yS= [-1-(f1_mag/1)], yE=[-0.8], lW = [2] )

        #f2_arrow:
        #if (f2_mag==0):
        #    f2_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[])
        if (f2_mag<=-p_magi):
            f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yS= [1-(f2_mag/1)], yE=[0.8], lW = [2])
        elif (f2_mag > -p_magi) & (f2_mag <= 0.0):
            f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yS= [1-(f2_mag/1)], yE=[0.8], lW = [2])
        elif (f2_mag > 0) & ( f2_mag < p_magi ):
            f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yS= [-1-(f2_mag/1)], yE=[-0.8], lW = [2])
        else:
            f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yS= [-1-(f2_mag/1)], yE=[-0.8], lW =[2])

#initial function:
def initial():
    p_loc_slide.value = p_loci
    f2_loc_slide.value = f2_loci
    p_mag_slide.value = p_magi
    lth_slide.value = 2
    checkbox.active = []
    Fun_Update(None,None,None)
    support_source1.data = dict(sp1=[support1], x= [-0.325], y= [-0.1])

##########Plotting##########

###Main Plot:
plot = Figure(title="Double-Supported Beam and Single Load", x_range=(x0-.5,xf+.5), y_range=(-2.5,2.5), height = 400, logo=None)
my_line=plot.line(x='x', y='y', source=plot_source, color='#0065BD',line_width=20)
plot.add_glyph(support_source1,ImageURL(url="sp1", x=-0.325, y=-0.1, w=0.66, h=0.4))
plot.add_glyph(support_source2,ImageURL(url="sp2", x='x', y='y', w=0.66, h=0.4))
#plot.triangle(x='x', y='y', size = 'size', source= triangle_source,color="#E37222", line_width=2)
plot.quad(top='top', bottom='bottom', left='left',
    right='right', source = quad_source, color="#808080", fill_alpha = 0.5)
plot.segment(x0='x0', y0='y0', x1='x1',
          y1='y1', source = segment_source, color="#F4A582", line_width=2)
plot.axis.visible = False
plot.outline_line_width = 2
#plot.outline_line_alpha = 0.3
plot.outline_line_color = "Black"
plot.title.text_font_size="13pt"
labels = LabelSet(x='x', y='y', text='name', level='glyph',
              x_offset=5, y_offset=-30, source=labels_source, render_mode='canvas')


###Plot1 with moment:
y_range0 = -10
y_range1 = -y_range0
plot1 = Figure(title="Bending Moment", x_range=(x0-.5,xf+.5), y_range=(y_range0,y_range1), height = 200, logo=None)

#Insert TUM-COLOUR
plot1.line(x='x', y='y', source=mom_source, color='blue',line_width=5)

plot1.line(x= [x0-1,xf+1], y = [0, 0 ], color = 'black', line_width =2 ,line_alpha = 0.4, line_dash=[1])
plot1.line(x= [xf/2,xf/2], y = [y_range0,y_range1], color = 'black', line_width =2 ,line_alpha = 0.4, line_dash=[1])
plot1.axis.visible = False
plot1.outline_line_width = 2
#plot.outline_line_alpha = 0.3
plot1.outline_line_color = "Black"
plot1.title.text_font_size="13pt"
# dummy glyphs for the legend entries

#Insert TUM-COLOUR
plot1.square([0.0],[0.0],size=0,fill_color='blue',fill_alpha=0.5,legend="Bending Moment")

#Insert TUM-COLOUR
#plot1.square([0.0],[0.0],size=0,fill_color='red',fill_alpha=0.5,legend="Shear Force")

plot1.legend.location = 'top_right'


###Plot2 with shear:
y_range0 = -10
y_range1 = -y_range0
plot2 = Figure(title="Shear Force", x_range=(x0-.5,xf+.5), y_range=(y_range0,y_range1), height = 200, logo=None)

#Insert TUM-COLOUR
plot2.line(x='x', y='y', source=shear_source, color='red',line_width=5)

plot2.line(x= [x0-1,xf+1], y = [0, 0 ], color = 'black', line_width =2 ,line_alpha = 0.4, line_dash=[1])
plot2.line(x= [xf/2,xf/2], y = [y_range0,y_range1], color = 'black', line_width =2 ,line_alpha = 0.4, line_dash=[1])
plot2.axis.visible = False
plot2.outline_line_width = 2
#plot.outline_line_alpha = 0.3
plot2.outline_line_color = "Black"
plot2.title.text_font_size="13pt"
# dummy glyphs for the legend entries

#Insert TUM-COLOUR
#plot2.square([0.0],[0.0],size=0,fill_color='blue',fill_alpha=0.5,legend="Bending Moment")

#Insert TUM-COLOUR
plot2.square([0.0],[0.0],size=0,fill_color='red',fill_alpha=0.5,legend="Shear Force")

plot2.legend.location = 'top_right'


###arrow plotting:
#P arrow:
p_arrow_glyph = Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=p_arrow_source,line_color="#0065BD")
#Position 2 arrow:
f2_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 2,size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_width = "lW", source=f2_arrow_source,line_color="#E37222")
#Position 1 arrow:
f1_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 2,size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width = "lW", source=f1_arrow_source,line_color="#E37222" )
###add layouts:
plot.add_layout(labels)
plot.add_layout(p_arrow_glyph)
plot.add_layout(f2_arrow_glyph)
plot.add_layout(f1_arrow_glyph)

###Reset Button
button = Button(label="Reset", button_type="success")

###CheckboxGroup
#Biegelinie Checkbox
checkbox = CheckboxGroup(
        labels=["Bending Curve"], active=[])


###on_change:
p_loc_slide.on_change('value', Fun_Update)
p_mag_slide.on_change('value', Fun_Update)
f2_loc_slide.on_change('value',Fun_Update)
# lth_slide.on_change('value',Fun_Update)
# checkbox.on_change('active',Fun_Update)
button.on_click(initial)

#main:
initial()

curdoc().add_root( row( column(Spacer(height=200,width=50), p_loc_slide, p_mag_slide, f2_loc_slide, widgetbox(button)),  column(plot,plot2,plot1 ) ) )
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
