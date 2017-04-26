#main file:

from bokeh.plotting import Figure, output_file , show
from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, Arrow
from bokeh.layouts import column, row, widgetbox
from bokeh.io import curdoc
from bokeh.models.widgets import Button, CheckboxGroup
import numpy as np

#Global Beam Properties:
resol = 100
x0 = 0                  #starting value of beam
xf = 10                 #ending value of beam
E  = 500.0e1            #modulus of elasticity
I  = 30                 #moment of inertia
length  = xf-x0              #length of beam
p_mag = 100.0           #initialize the p force
p_magi = 100.0
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
#Triangle source:
triangle_source = ColumnDataSource(data=dict(x= [], y= [], size = []))
#Cantilever rectangle source:
quad_source = ColumnDataSource(data=dict(top= [], bottom= [],left = [], right =[]))
segment_source = ColumnDataSource(data=dict(x0= [], y0= [],x1 = [], y1 =[]))
#Sliders:
p_loc_slide= Slider(title="Lastposition",value= p_loci,start = x0, end = xf, step = 1/resol)
p_mag_slide = Slider(title="Lastamplitude", value=p_mag, start=-2*p_mag, end=2*p_mag, step=1)
f2_loc_slide = Slider(title="Lagerposition",value=f2_loci,start = x0, end = xf, step = 1/resol)
lth_slide = Slider(title="Laenge zu Hoehe",value=lthi ,start = 2, end = 20, step = 1)

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
    triangle_source.data = dict(x = [], y = [], size = [])
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
#FUNCTION: Update:
def Fun_Update(attrname, old, new):
    #values used by both cases:
    my_line.glyph.line_width = 40/lth_slide.value
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
            p_arrow_source.data = dict(xS= [p_coord], xE= [p_coord], yS= [1-(p_mag/200.0)], yE=[1], lW = [abs(p_mag/40.0)] )
            labels_source.data = dict(x = [p_coord] , y = [1],name = ['F'])
        else:
            p_arrow_source.data = dict(xS= [p_coord], xE= [p_coord], yS= [-1-(p_mag/200.0)], yE=[-1], lW = [abs(p_mag/40.0)] )
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
        elif checkbox.active == [1]:
            checkbox.active = []
        elif checkbox.active == [0,1]:
            ynew = Fun_C_Deflection(p_mag,a,plot_source.data['x'])
            plot_source.data = dict(x = np.linspace(x0,xf,resol), y = ynew)
            print 'this would be mit schub'
        else:
            print 'fatal error'

#####################
    else: ##this else is what determines whether or not the figure is in cantilever mode
#####################
        quad_source.data = dict(top = [], bottom = [], left = [] , right = [])
        segment_source.data = dict(x0= [], y0= [],x1 = [], y1 =[])

        f1_mag = Fun_F(p_mag_slide.value,b,l)
        f2_mag = Fun_F(p_mag_slide.value,a,l)

        if checkbox.active == [0]:
            ynew = Fun_Deflection(a,b,l,p_mag,plot_source.data['x'])
            plot_source.data = dict(x = np.linspace(x0,xf,resol), y = ynew)
        elif checkbox.active == []:
            plot_source.data= dict( x = np.linspace(x0,xf,resol) , y = np.ones(resol) * 0)
        elif checkbox.active == [1]:
            checkbox.active = []
        elif checkbox.active == [0,1]:
            ynew = Fun_Deflection(a,b,l,p_mag,plot_source.data['x'])
            plot_source.data = dict(x = np.linspace(x0,xf,resol), y = ynew)
            print 'this would be mit schub'
        else:
            print 'fatal error'

        #print plot_source.data['y']

        move_tri = -0.25
        triangle_source.data = dict(x = [0.0,f2_loc_slide.value], y = [0+move_tri, 0+move_tri], size = [20,20])

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
            p_arrow_source.data = dict(xS= [p_coord], xE= [p_coord], yS= [1-(p_mag/200.0)], yE=[1], lW = [abs(p_mag/40.0)] )
            labels_source.data = dict(x = [p_coord,0,f2_coord] , y = [1,move_tri,move_tri],name = ['F','A','B'])

        else:
            p_arrow_source.data = dict(xS= [p_coord], xE= [p_coord], yS= [-1-(p_mag/200.0)], yE=[-1], lW = [abs(p_mag/40.0)] )
            labels_source.data = dict(x = [p_coord,0,f2_coord] , y = [-1,move_tri,move_tri],name = ['F','A','B'])

        #f1_arrow:
        #if (f1_mag==0):
            #f1_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        if (f1_mag<=-p_magi):
            f1_arrow_source.data = dict(xS= [0], xE= [0], yS= [1-(f1_mag/200.0)], yE=[0.8], lW = [6])
        elif ( f1_mag>-p_magi ) & ( f1_mag<=0 ):
            f1_arrow_source.data = dict(xS= [0], xE= [0], yS= [1-(f1_mag/200.0)], yE=[0.8], lW = [abs(f1_mag/40.0)])
        elif (f1_mag > 0) & ( f1_mag < p_magi ):
            f1_arrow_source.data = dict(xS= [0], xE= [0], yS= [-1-(f1_mag/200.0)], yE=[-0.8], lW = [abs(f1_mag/40.0)] )
        else:
            f1_arrow_source.data = dict(xS= [0], xE= [0], yS= [-1-(f1_mag/200.0)], yE=[-0.8], lW = [6] )

        #f2_arrow:
        #if (f2_mag==0):
        #    f2_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[])
        if (f2_mag<=-p_magi):
            f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yS= [1-(f2_mag/200.0)], yE=[0.8], lW = [6])
        elif (f2_mag > -p_magi) & (f2_mag <= 0.0):
            f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yS= [1-(f2_mag/200.0)], yE=[0.8], lW = [abs(f2_mag/40.0)])
        elif (f2_mag > 0) & ( f2_mag < p_magi ):
            f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yS= [-1-(f2_mag/200.0)], yE=[-0.8], lW = [abs(f2_mag/40.0)])
        else:
            f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yS= [-1-(f2_mag/200.0)], yE=[-0.8], lW = [6])

#initial function:
def initial():
    p_loc_slide.value = p_loci
    f2_loc_slide.value = f2_loci
    p_mag_slide.value = p_magi
    lth_slide.value = 2
    checkbox.active = []
    Fun_Update(None,None,None)

##########Plotting##########

###Main Plot:
plot = Figure(title="Doppeltgelagerter Balken und Einzellast", x_range=(x0-.5,xf+.5), y_range=(-2.5,2.5))
my_line=plot.line(x='x', y='y', source=plot_source, color='#0065BD',line_width=20)
plot.triangle(x='x', y='y', size = 'size', source= triangle_source,color="#E37222", line_width=2)
plot.quad(top='top', bottom='bottom', left='left',
    right='right', source = quad_source, color="#808080", fill_alpha = 0.5)
plot.segment(x0='x0', y0='y0', x1='x1',
          y1='y1', source = segment_source, color="#F4A582", line_width=2)
plot.axis.visible = False
plot.outline_line_width = 7
plot.outline_line_alpha = 0.3
plot.outline_line_color = "Black"
labels = LabelSet(x='x', y='y', text='name', level='glyph',
              x_offset=5, y_offset=-30, source=labels_source, render_mode='canvas')
###Plot with moment and shear:
y_range0 = -600
y_range1 = -y_range0
plot1 = Figure(title="Biegemoment, Querkraft", x_range=(x0,xf), y_range=(y_range0,y_range1), width = 400, height = 200)
plot1.line(x='x', y='y', source=mom_source, color='blue',line_width=5)
plot1.line(x='x', y='y', source=shear_source, color='red',line_width=5)
plot1.line(x= [x0-1,xf+1], y = [0, 0 ], color = 'black', line_width =2 ,line_alpha = 0.4, line_dash=[1])
plot1.line(x= [xf/2,xf/2], y = [y_range0,y_range1], color = 'black', line_width =2 ,line_alpha = 0.4, line_dash=[1])
plot1.axis.visible = False
###arrow plotting:
#P arrow:
p_arrow_glyph = Arrow(end=OpenHead(line_color="#A2AD00",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=p_arrow_source,line_color="#A2AD00")
#Position 2 arrow:
f2_arrow_glyph = Arrow(end=OpenHead(line_color="#003359",line_width= 4,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_width = "lW", source=f2_arrow_source,line_color="#003359")
#Position 1 arrow:
f1_arrow_glyph = Arrow(end=OpenHead(line_color="#003359",line_width= 4,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width = "lW", source=f1_arrow_source,line_color="#003359" )
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
        labels=["Biegelinie", "Mit Schub (Biegelinie muss auch markiert sein!)"], active=[])


###on_change:
p_loc_slide.on_change('value', Fun_Update)
p_mag_slide.on_change('value', Fun_Update)
f2_loc_slide.on_change('value',Fun_Update)
lth_slide.on_change('value',Fun_Update)
checkbox.on_change('active',Fun_Update)
button.on_click(initial)

#main:
initial()

curdoc().add_root( row( column(p_loc_slide,p_mag_slide,f2_loc_slide,lth_slide,plot1,widgetbox(button)),  column(plot,widgetbox(checkbox) ) ) )
