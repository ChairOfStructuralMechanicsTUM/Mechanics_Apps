#main file:

from bokeh.plotting import Figure, output_file , show
from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, Arrow
from bokeh.models.glyphs import ImageURL, Quadratic, Rect, Patch
from bokeh.models.layouts import Spacer
from bokeh.layouts import column, row, widgetbox
from bokeh.io import curdoc, output_file, show
from bokeh.models.widgets import Button, CheckboxGroup, RadioButtonGroup
import numpy as np
from os.path import dirname, join, split


#Global Beam Properties:
resol = 100             # resolution of deflection visualization
resol_plo = 1000        # resolution of forces plot
x0 = 0.0                  #starting value of beam
xf = 10.0                 #ending value of beam
E  = 5.0e1              #modulus of elasticity
I  = 30.0                 #moment of inertia
length  = xf-x0         #length of beam
p_mag = 0.5             #initialize the p force
p_magi = 0.5
p_loci = xf/2
f2_loci = xf
lthi = 2.0
plotwidth = 20.0
loadoptionsi = 0

#EDIT:
x_length = np.linspace(x0,xf,resol_plo)     #Initialize Arrays for Forces Plot
y_mom = []
y_shear = []                           

#Sources:
#Plot source:
plot_source = ColumnDataSource(data=dict(x = np.linspace(x0,xf,resol), y = np.ones(resol) * 0 ))
#Moment Source:
#mom_source = ColumnDataSource(data=dict(x0=[], y0=[], x1=[], y1=[], x2=[], y2=[], xe=[], ye=[]))
mom_source = ColumnDataSource(data=dict(x=[], y=[]))

#Shear Source:
shear_source = ColumnDataSource(data=dict(x=[] , y=[]))
#Arrow Sources:
p_arrow_source1 = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
p_arrow_source2 = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
p_arrow_source3 = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
f2_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
f1_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
#Load Shapes Sources:
constant_load_source  = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
triangular_load_source  = ColumnDataSource(data=dict(x=[], y=[]))

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
p_loc_slide= Slider(title="Load Position",value= p_loci,start = x0, end = xf, step = 1.0)
p_mag_slide = Slider(title="Load Amplitude", value = p_magi, start=-2*p_magi, end=2*p_magi, step=.1)
f2_loc_slide = Slider(title="Support Position",value=f2_loci,start = x0, end = xf, step = 1.0)
lth_slide = Slider(title="Beam-Height",value=lthi ,start = 2.0, end = 20.0, step = 1.0)

radio_button_group = RadioButtonGroup(
        labels=["Point Load", "Constant Load", "Triangular Load"], active=loadoptionsi, width = 600)

#FUNCTION: Calculate Force at Support 1
def Fun_F(p_mag,b,l):
    if radio_button_group.active == 0:
        f1_mag = -1.0 * (p_mag *b) / l
        return f1_mag
    # if radio_button_group.active == 1:
    #     f_res=b
    #     f1_mag = p_mag*10/l*f_res
    #     return f1_mag



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
    if radio_button_group.active == 0:
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

    if radio_button_group.active == 1:   
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
 
    if radio_button_group.active == 2:   
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
    if radio_button_group.active == 0:
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
        ### EDIT:
        support_source2.data = dict(sp2=[], x = [] , y = [])
        support_source1.data = dict(sp1=[], x = [] , y = [])
    
    if radio_button_group.active == 1:
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
        ### EDIT:
        support_source2.data = dict(sp2=[], x = [] , y = [])
        support_source1.data = dict(sp1=[], x = [] , y = [])

    if radio_button_group.active == 2:    
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
        ### EDIT:
        support_source2.data = dict(sp2=[], x = [] , y = [])
        support_source1.data = dict(sp1=[], x = [] , y = [])

#FUNCTION: Update:
def Fun_Update(attrname, old, new):
    #values used by both cases:9

    if radio_button_group.active == 0:   # If Point Load is selected
        
        p_loc_slide.disabled = False
        my_line.glyph.line_width = 15
        a = p_loc_slide.value
        f2_coord = f2_loc_slide.value
        b = f2_coord - a
        p_coord = p_loc_slide.value
        p_mag = p_mag_slide.value
        l = f2_coord
        x1 = xf - l
        
        if f2_coord == 0:   #Supports all left -> Cantilever 
            xcan = x0
            Fun_Cantilever()
            if (p_mag<0):
                p_arrow_source1.data = dict(xS= [p_coord], xE= [p_coord], yS= [1-(p_mag/2.3)], yE=[1+(p_mag/2.3)], lW = [2] )
                p_arrow_source2.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                p_arrow_source3.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                labels_source.data = dict(x = [p_coord] , y = [1],name = ['F'])
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
                triangular_load_source.data  = dict(x=[], y=[])                
            else:
                p_arrow_source1.data = dict(xS= [p_coord], xE= [p_coord], yS= [-1.1-(p_mag/2.3)], yE=[-1.1+(p_mag/2.3)], lW = [2] )
                p_arrow_source2.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                p_arrow_source3.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                labels_source.data = dict(x = [p_coord] , y = [-1.1],name = ['F'])
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
                triangular_load_source.data  = dict(x=[], y=[])                

            #EDIT:
            y_mom=[]
            y_shear=[]
            for i in range(0,resol_plo):
                if x_length[i]<a :
                    y_shear.append(p_mag)
                    y_mom.append(p_mag *a*(1-x_length[i]/a))
                if x_length[i]>=a :
                    y_shear.append(0)
                    y_mom.append(0)
            mom_source.data = dict(x=x_length, y=y_mom)
            shear_source.data = dict(x=x_length, y=y_shear)

            ynew = Fun_C_Deflection(p_mag,a,plot_source.data['x'])
            plot_source.data = dict(x = np.linspace(x0,xf,resol), y = ynew)

#####################
        else: ##this else is what determines whether or not the figure is in cantilever mode
#####################
            quad_source.data = dict(top = [], bottom = [], left = [] , right = [])
            segment_source.data = dict(x0= [], y0= [],x1 = [], y1 =[])

            f1_mag = Fun_F(p_mag_slide.value,b,l)
            f2_mag = Fun_F(p_mag_slide.value,a,l)
            ynew = Fun_Deflection(a,b,l,p_mag,plot_source.data['x'])
            plot_source.data = dict(x = np.linspace(x0,xf,resol), y = ynew)
            move_tri = -0.4

            #EDIT:
            m_max = Fun_Moment(p_mag_slide.value,a,b,l)
            y_mom = []
            y_shear = []
            if (l >= a):
                for i in range(0,resol_plo):
                    if x_length[i]<a:
                        y_shear.append(f1_mag)
                        y_mom.append(f1_mag*x_length[i])
                    if x_length[i]>=a and x_length[i]<l:
                        y_shear.append(f1_mag+p_mag)
                        y_mom.append(f1_mag*a+(f1_mag+p_mag)*(x_length[i]-a))
                    if x_length[i]>=l:
                        y_shear.append(f1_mag+p_mag+f2_mag)
                        y_mom.append(f1_mag*a+(f1_mag+p_mag)*(l-a))

                mom_source.data = dict(x=x_length, y=y_mom)
                shear_source.data = dict(x=x_length, y=y_shear)
            
            else:
                for i in range(0,resol_plo):
                    if x_length[i]<l:
                        y_shear.append(f1_mag)
                        y_mom.append(f1_mag*x_length[i])
                    if x_length[i]>=l and x_length[i]<a:
                        y_shear.append(f1_mag+f2_mag)
                        y_mom.append(f1_mag*l+(f1_mag+f2_mag)*(x_length[i]-l))
                    if x_length[i]>=a:
                        y_shear.append(f1_mag+p_mag+f2_mag)
                        y_mom.append(f1_mag*l+(f1_mag+f2_mag)*(a-l))

                mom_source.data = dict(x=x_length, y=y_mom)
                shear_source.data = dict(x=x_length, y=y_shear)

            #p_arrow and labels:
            if (p_mag<0):
                p_arrow_source1.data = dict(xS= [p_coord], xE= [p_coord], yS= [1-(p_mag/2.3)], yE=[1+(p_mag/2.3)], lW = [2] )
                p_arrow_source2.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                p_arrow_source3.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
                triangular_load_source.data  = dict(x=[], y=[])                
                # labels_source.data = dict(x = [p_coord,0,f2_coord-0.2] , y = [1,move_tri,move_tri],name = ['F','A','B'])
                labels_source.data = dict(x = [p_coord] , y = [1],name = ['F'])
                support_source2.data = dict(sp2=[support2], x = [f2_coord-0.33] , y = [-0.1])
                support_source1.data = dict(sp1=[support1], x= [-0.325], y= [-0.1])
            else:
                p_arrow_source1.data = dict(xS= [p_coord], xE= [p_coord], yS= [-1.1-(p_mag/2.3)], yE=[-1.1+(p_mag/2.3)], lW = [2] )
                p_arrow_source2.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                p_arrow_source3.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
                triangular_load_source.data  = dict(x=[], y=[])                
                # labels_source.data = dict(x = [p_coord,-0.2,f2_coord-0.2] , y = [-1,move_tri,move_tri],name = ['F','A','B'])
                labels_source.data = dict(x = [p_coord] , y = [-1.1],name = ['F'])
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

    if radio_button_group.active == 1:  #If constant load is selected

        p_loc_slide.disabled = False
        my_line.glyph.line_width = 15
        
        p_mag = p_mag_slide.value
        a = p_loc_slide.value
        l = f2_loc_slide.value
        f2_coord = f2_loc_slide.value
        p_coord = p_loc_slide.value
        b = l - a
        x1 = xf - l

        if f2_coord == 0:
            xcan = x0
            Fun_Cantilever()

            if (p_mag<0) and (p_coord!=0):
                p_arrow_source1.data = dict(xS= [0.2*p_coord], xE= [0.2*p_coord], yS= [1-(p_mag/2.3)], yE=[1+(p_mag/2.3)], lW = [2] )
                p_arrow_source2.data = dict(xS= [p_coord/2.0], xE= [p_coord/2.0], yS= [1-(p_mag/2.3)], yE=[1+(p_mag/2.3)], lW = [2] )
                p_arrow_source3.data = dict(xS= [p_coord*(1-0.2)], xE= [p_coord*(1-0.2)], yS= [1-(p_mag/2.3)], yE=[1+(p_mag/2.3)], lW = [2] )
                constant_load_source.data  = dict(x=[p_coord/2.0], y=[1], w=[p_coord], h=[p_mag], angle=[0])
                triangular_load_source.data  = dict(x=[], y=[])                
                labels_source.data = dict(x = [p_coord] , y = [1],name = ['p'])            
            elif (p_mag>0) and (p_coord!=0):
                p_arrow_source1.data = dict(xS= [0.2*p_coord], xE= [0.2*p_coord], yS= [-1.1-(p_mag/2.3)], yE=[-1.1+(p_mag/2.3)], lW = [2] )
                p_arrow_source2.data = dict(xS= [p_coord/2.0], xE= [p_coord/2.0], yS= [-1.1-(p_mag/2.3)], yE=[-1.1+(p_mag/2.3)], lW = [2] )
                p_arrow_source3.data = dict(xS= [p_coord*(1-0.2)], xE= [p_coord*(1-0.2)], yS= [-1.1-(p_mag/2.3)], yE=[-1.1+(p_mag/2.3)], lW = [2] )
                constant_load_source.data  = dict(x=[p_coord/2.0], y=[-1.1], w=[p_coord], h=[p_mag], angle=[0])
                triangular_load_source.data  = dict(x=[], y=[])                
                labels_source.data = dict(x = [p_coord] , y = [-1.1],name = ['p']) 
            else: 
                p_arrow_source1.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                p_arrow_source2.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                p_arrow_source3.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
                triangular_load_source.data  = dict(x=[], y=[])                
                labels_source.data = dict(x = [] , y = [],name = [])                        

            #cantilever forces calculation:
            y_mom=[]
            y_shear=[]
            for i in range(0,resol_plo):
                if x_length[i]<a :
                    y_shear.append(p_mag*a - p_mag*x_length[i])
                    y_mom.append(p_mag*a**2.0/2.0-p_mag*x_length[i]**2.0/2.0 )
                if x_length[i]>=a :
                    y_shear.append(0)
                    y_mom.append(0)
            mom_source.data = dict(x=x_length, y=y_mom)
            shear_source.data = dict(x=x_length, y=y_shear)

            ynew = Fun_C_Deflection(p_mag,a,plot_source.data['x'])
            plot_source.data = dict(x = np.linspace(x0,xf,resol), y = ynew)

#####################
        else: ##this else is what determines whether or not the figure is in cantilever mode
#####################
            quad_source.data = dict(top = [], bottom = [], left = [] , right = [])
            segment_source.data = dict(x0= [], y0= [],x1 = [], y1 =[])

            # f1_mag = Fun_F(p_mag_slide.value,b,l)
            # f2_mag = Fun_F(p_mag_slide.value,a,l)

            ynew = Fun_Deflection(a,b,l,p_mag,plot_source.data['x'])
            plot_source.data = dict(x = np.linspace(x0,xf,resol), y = ynew)

            move_tri = -0.4
            #triangle_source.data = dict(x = [0.0,f2_loc_slide.value], y = [0+move_tri, 0+move_tri], size = [20,20])

            #moment and shear:
            y_mom = []
            y_shear = []

            if (l >= a):
                f1_mag = -1.0* p_mag*a/l*(l - a + a/2.0)
                f2_mag = -1.0* ( p_mag* a**2.0 ) / 2.0 / l
                for i in range(0,resol_plo):
                    if x_length[i]<a:
                        y_shear.append(f1_mag + p_mag*x_length[i])
                        y_mom.append(f1_mag*x_length[i] + p_mag*x_length[i]**2/2.0)
                    if x_length[i]>=a and x_length[i]<l:
                        y_shear.append(f1_mag + p_mag* a)
                        y_mom.append(f1_mag*a + (p_mag*a**2.0)/2.0 + (f1_mag + p_mag*a)*(x_length[i]-a))
                    if x_length[i]>=l:
                        y_shear.append( f1_mag + p_mag*a + f2_mag )
                        y_mom.append( f1_mag*a + (p_mag*a**2.0)/2.0 + (f1_mag + p_mag*a)*(l-a) + ( f1_mag + p_mag*a + f2_mag) * (x_length[i]-l) ) 
                mom_source.data = dict(x=x_length, y=y_mom)
                shear_source.data = dict(x=x_length, y=y_shear)
                # mom_source.data = dict(x=[], y=[])
                # shear_source.data = dict(x=[], y=[])

            else: #if l<a
                f1_mag = -1.0*p_mag*a/l*(l-a/2.0)
                f2_mag = -1.0*p_mag* a**2.0/2.0/l
                for i in range(0,resol_plo):
                    if x_length[i]<l:
                        y_shear.append(f1_mag + p_mag*x_length[i])
                        y_mom.append(f1_mag*x_length[i] + p_mag*x_length[i]**2.0/2.0)
                    if x_length[i]>=l and x_length[i]<a:
                        y_shear.append(f1_mag + p_mag *l + f2_mag + p_mag*(x_length[i]-l))
                        y_mom.append(f1_mag*l + p_mag*l**2.0/2.0 + (f1_mag + p_mag*l+f2_mag)*(x_length[i]-l) + p_mag*(x_length[i]-l)**2.0/2.0)
                    if x_length[i]>=a:
                        y_shear.append(f1_mag + p_mag *l + f2_mag + p_mag*(a-l))
                        y_mom.append(f1_mag*l + p_mag*l**2.0/2.0 + (f1_mag + p_mag*l+f2_mag)*(a-l) + p_mag*(a-l)**2.0/2.0 + (f1_mag + p_mag *l + f2_mag + p_mag*(a-l))* (x_length[i]-a))
                mom_source.data = dict(x=x_length, y=y_mom)
                shear_source.data = dict(x=x_length, y=y_shear)
                # mom_source.data = dict(x=[] , y=[])
                # shear_source.data = dict(x=[], y=[])

            #p_arrow and labels:
            if (p_mag<0) and (p_coord!=0):
                p_arrow_source1.data = dict(xS= [0.2*p_coord], xE= [0.2*p_coord], yS= [1-(p_mag/2.3)], yE=[1+(p_mag/2.3)], lW = [2] )
                p_arrow_source2.data = dict(xS= [p_coord/2.0], xE= [p_coord/2.0], yS= [1-(p_mag/2.3)], yE=[1+(p_mag/2.3)], lW = [2] )
                p_arrow_source3.data = dict(xS= [p_coord*(1-0.2)], xE= [p_coord*(1-0.2)], yS= [1-(p_mag/2.3)], yE=[1+(p_mag/2.3)], lW = [2] )
                constant_load_source.data  = dict(x=[p_coord/2.0], y=[1], w=[p_coord], h=[p_mag], angle=[0])
                triangular_load_source.data  = dict(x=[], y=[])                
                # labels_source.data = dict(x = [p_coord,-0.2,f2_coord-0.2] , y = [1,move_tri,move_tri],name = ['p','A','B'])
                labels_source.data = dict(x = [p_coord] , y = [1],name = ['p'])
                support_source2.data = dict(sp2=[support2], x = [f2_coord-0.33] , y = [-0.1])
                support_source1.data = dict(sp1=[support1], x= [-0.325], y= [-0.1])      
            elif (p_mag>0) and (p_coord!=0):
                p_arrow_source1.data = dict(xS= [0.2*p_coord], xE= [0.2*p_coord], yS= [-1.1-(p_mag/2.3)], yE=[-1.1+(p_mag/2.3)], lW = [2] )
                p_arrow_source2.data = dict(xS= [p_coord/2.0], xE= [p_coord/2.0], yS= [-1.1-(p_mag/2.3)], yE=[-1.1+(p_mag/2.3)], lW = [2] )
                p_arrow_source3.data = dict(xS= [p_coord*(1-0.2)], xE= [p_coord*(1-0.2)], yS= [-1.1-(p_mag/2.3)], yE=[-1.1+(p_mag/2.3)], lW = [2] )
                constant_load_source.data  = dict(x=[p_coord/2.0], y=[-1.1], w=[p_coord], h=[p_mag], angle=[0])
                triangular_load_source.data  = dict(x=[], y=[])                
                # labels_source.data = dict(x = [p_coord,-0.2,f2_coord-0.2] , y = [-1,move_tri,move_tri],name = ['p','A','B'])
                labels_source.data = dict(x = [p_coord] , y = [-1.1],name = ['p'])
                support_source2.data = dict(sp2=[support2], x = [f2_coord-0.33] , y = [-0.1])
                support_source1.data = dict(sp1=[support1], x= [-0.325], y= [-0.1])
            else: 
                p_arrow_source1.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                p_arrow_source2.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                p_arrow_source3.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
                triangular_load_source.data  = dict(x=[], y=[])                
                # labels_source.data = dict(x = [-0.2,f2_coord-0.2] , y = [move_tri,move_tri],name = ['A','B'])
                labels_source.data = dict(x = [] , y = [],name = [])
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

    
    if radio_button_group.active == 2:

        # p_loc_slide.value = 10 
        # p_loc_slide.disabled = True
        p_loc_slide.disabled = False
        my_line.glyph.line_width = 15
        
        #EDIT
        p_mag = p_mag_slide.value
        a = p_loc_slide.value
        l = f2_loc_slide.value
        f2_coord = f2_loc_slide.value
        p_coord = p_loc_slide.value
        b = l - a
        x1 = xf - l
        # f_res=l-5


        if f2_coord == 0:
            xcan = x0
            Fun_Cantilever()

            if (p_mag<0) and (p_coord!=0):
                #EDIT: Spannungsrechteck einsetzen!
                p_arrow_source1.data = dict(xS= [0.2*p_coord], xE= [0.2*p_coord], yS= [1+p_mag/2.3-p_mag/10.0], yE=[1+p_mag/2.3], lW = [2] )
                p_arrow_source2.data = dict(xS= [p_coord/2.0], xE= [p_coord/2.0], yS= [1+p_mag/2.3-p_mag/2.6], yE=[1+(p_mag/2.3)], lW = [2] )
                p_arrow_source3.data = dict(xS= [p_coord*(1-0.2)], xE= [p_coord*(1-0.2)], yS= [1-(p_mag/2.3/1.9)], yE=[1+(p_mag/2.3)], lW = [2] )
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])     

                N = 30
                x1 = np.linspace(0, p_coord, N)
                x2 = x1[::-1]
                y1 = 0.95 - x1/p_coord*p_mag + p_mag/2.3
                y2 = np.ones(N)*(0.95 + p_mag/2.3)
                x = np.hstack((x1, x2))
                y = np.hstack((y1, y2))
                triangular_load_source.data  = dict(x=x, y=y)
                
                # labels_source.data = dict(x = [0,0,f2_coord-0.2] , y = [1,move_tri,move_tri],name = ['p','A','B'])
                labels_source.data = dict(x = [p_coord] , y = [1],name = ['p'])
            elif (p_mag>=0) and (p_coord!=0):
                p_arrow_source1.data = dict(xS= [0.2*p_coord], xE= [0.2*p_coord], yS= [-1.1+p_mag/2.3-p_mag/10.0], yE=[-1.1+p_mag/2.3], lW = [2] )
                p_arrow_source2.data = dict(xS= [p_coord/2.0], xE= [p_coord/2.0], yS= [-1.1+p_mag/2.3-p_mag/2.6], yE=[-1.1+(p_mag/2.3)], lW = [2] )
                p_arrow_source3.data = dict(xS= [p_coord*(1-0.2)], xE= [p_coord*(1-0.2)], yS= [-1.1-(p_mag/2.3/1.9)], yE=[-1.1+(p_mag/2.3)], lW = [2] )
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])     

                N = 30
                x1 = np.linspace(0, p_coord, N)
                x2 = x1[::-1]
                y1 = -1.05 - x1/p_coord*p_mag + p_mag/2.3
                y2 = np.ones(N)*(-1.05 + p_mag/2.3)
                x = np.hstack((x1, x2))
                y = np.hstack((y1, y2))
                triangular_load_source.data  = dict(x=x, y=y)                   

                # labels_source.data = dict(x = [0,-0.2,f2_coord-0.2] , y = [-1,move_tri,move_tri],name = ['p','A','B'])
                labels_source.data = dict(x = [p_coord] , y = [-1.1],name = ['p'])
            else:
                p_arrow_source1.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                p_arrow_source2.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                p_arrow_source3.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
                triangular_load_source.data  = dict(x=[], y=[])     

                # labels_source.data = dict(x = [-0.2,f2_coord-0.2] , y = [move_tri,move_tri],name = ['A','B'])
                labels_source.data = dict(x = [] , y = [],name = [])


            #EDIT:
            y_mom=[]
            y_shear=[]
            for i in range(0,resol_plo):
                if x_length[i]<a :
                    y_shear.append(p_mag*a/2.0-p_mag*x_length[i]/2.0)
                    y_mom.append( p_mag*a**2.0/3.0-p_mag*a/2.0*x_length[i] + p_mag/6.0/a*x_length[i]**3.0  )
                if x_length[i]>=a :
                    y_shear.append(0)
                    y_mom.append(0)
            mom_source.data = dict(x=x_length, y=y_mom)
            shear_source.data = dict(x=x_length, y=y_shear)

            ynew = Fun_C_Deflection(p_mag,a,plot_source.data['x'])
            plot_source.data = dict(x = np.linspace(x0,xf,resol), y = ynew)


#####################
        else: ##this else is what determines whether or not the figure is in cantilever mode
#####################
            quad_source.data = dict(top = [], bottom = [], left = [] , right = [])
            segment_source.data = dict(x0= [], y0= [],x1 = [], y1 =[])

            # f1_mag = Fun_F(p_mag_slide.value,b,l)
            # f2_mag = Fun_F(p_mag_slide.value,a,l)

            ynew = Fun_Deflection(a,b,l,p_mag,plot_source.data['x'])
            plot_source.data = dict(x = np.linspace(x0,xf,resol), y = ynew)

            move_tri = -0.4
            #triangle_source.data = dict(x = [0.0,f2_loc_slide.value], y = [0+move_tri, 0+move_tri], size = [20,20])

            #moment and shear:
            y_mom = []
            y_shear = []

            if (l >= a):
                f1_mag = -1.0*p_mag*a/2.0/l*(l-a+a/3.0)
                f2_mag = -1.0*p_mag*a**2.0/l/3.0
                for i in range(0,resol_plo):
                    if x_length[i]<a:
                        y_shear.append(f1_mag + p_mag*x_length[i]**2.0/2.0/a)
                        y_mom.append( f1_mag*x_length[i] + x_length[i]**3.0*p_mag/6.0/a)
                    if x_length[i]>=a and x_length[i]<l:
                        y_shear.append( f1_mag + p_mag*a/2.0 )
                        y_mom.append(f1_mag*a + a**2.0*p_mag/6.0 + (f1_mag + p_mag*a/2.0)*(x_length[i]-a) )
                    if x_length[i]>=l:
                        y_shear.append( f1_mag + p_mag*a/2.0 - p_mag*a**2.0/3.0/l)
                        y_mom.append( f1_mag*a + a**2.0*p_mag/6.0 + (f1_mag + p_mag*a/2.0)*(l-a) ) 
                mom_source.data = dict(x=x_length, y=y_mom)
                shear_source.data = dict(x=x_length, y=y_shear)
                # mom_source.data = dict(x=[], y=[])
                # shear_source.data = dict(x=[], y=[])

            else: #if l<a
                f1_mag = -1.0* (p_mag*a/2.0 - p_mag*a**2.0/3.0/l)
                # f1_mag = -1.0* ( p_mag*l**2.0 /a/6.0 - (p_mag /6.0/a + a*p_mag /3.0/l) * (a-l)**2.0 )
                f2_mag = -1.0* ( p_mag*a**2.0 /3.0/l )
                for i in range(0,resol_plo):
                    if x_length[i]<l:
                        y_shear.append(f1_mag + p_mag*x_length[i]**2.0/2.0/a)
                        y_mom.append( f1_mag*x_length[i] + x_length[i]**3.0*p_mag/6.0/a)
                    if x_length[i]>=l and x_length[i]<a:
                        # y_shear.append(f1_mag + p_mag*l**2.0 /2.0/a + f2_mag  + (p_mag*(x_length[i]-l) * (l/a + (l+(x_length[i]-l)) /a) /2.0 ) )
                        y_shear.append(f1_mag + p_mag*l**2.0 /2.0/a + f2_mag  + ( l*p_mag*(x_length[i]-l) /a + (((x_length[i]-l)-l)*p_mag*(x_length[i]-l) /a/2.0) ))
                        y_mom.append(f1_mag*l + l**3.0*p_mag/6.0/a + (f1_mag + p_mag*l**2.0/2.0/a + f2_mag)*(x_length[i]-l) + p_mag*l*(x_length[i]-l)**2.0/a/6.0 + p_mag*(x_length[i])/2.0/a * (x_length[i]-l)**2.0*2.0/3.0 )
                    if x_length[i]>=a:
                        y_shear.append( f1_mag + p_mag*l**2.0/2.0/a + f2_mag  + (p_mag*(a-l) * (l/a+(l+a-l)/a)/2.0 ))
                        y_mom.append( 0 ) 
                mom_source.data = dict(x=x_length, y=y_mom)
                shear_source.data = dict(x=x_length, y=y_shear)
                # mom_source.data = dict(x=[] , y=[])
                # shear_source.data = dict(x=[], y=[])

            #p_arrow and labels:
            if (p_mag<0) and (p_coord!=0):
                #EDIT: Spannungsrechteck einsetzen!
                p_arrow_source1.data = dict(xS= [0.2*p_coord], xE= [0.2*p_coord], yS= [1+p_mag/2.3-p_mag/10.0], yE=[1+p_mag/2.3], lW = [2] )
                p_arrow_source2.data = dict(xS= [p_coord/2.0], xE= [p_coord/2.0], yS= [1+p_mag/2.3-p_mag/2.6], yE=[1+(p_mag/2.3)], lW = [2] )
                p_arrow_source3.data = dict(xS= [p_coord*(1-0.2)], xE= [p_coord*(1-0.2)], yS= [1-(p_mag/2.3/1.9)], yE=[1+(p_mag/2.3)], lW = [2] )
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])     

                N = 30
                x1 = np.linspace(0, p_coord, N)
                x2 = x1[::-1]
                y1 = 0.95 - x1/p_coord*p_mag + p_mag/2.3
                y2 = np.ones(N)*(0.95 + p_mag/2.3)
                x = np.hstack((x1, x2))
                y = np.hstack((y1, y2))
                triangular_load_source.data  = dict(x=x, y=y)
                        
                # labels_source.data = dict(x = [0,0,f2_coord-0.2] , y = [1,move_tri,move_tri],name = ['p','A','B'])
                labels_source.data = dict(x = [p_coord] , y = [1],name = ['p'])
                support_source2.data = dict(sp2=[support2], x = [f2_coord-0.33] , y = [-0.1])
                support_source1.data = dict(sp1=[support1], x= [-0.325], y= [-0.1])
            elif (p_mag>=0) and (p_coord!=0):
                p_arrow_source1.data = dict(xS= [0.2*p_coord], xE= [0.2*p_coord], yS= [-1.1+p_mag/2.3-p_mag/10.0], yE=[-1.1+p_mag/2.3], lW = [2] )
                p_arrow_source2.data = dict(xS= [p_coord/2.0], xE= [p_coord/2.0], yS= [-1.1+p_mag/2.3-p_mag/2.6], yE=[-1.1+(p_mag/2.3)], lW = [2] )
                p_arrow_source3.data = dict(xS= [p_coord*(1-0.2)], xE= [p_coord*(1-0.2)], yS= [-1.1-(p_mag/2.3/1.9)], yE=[-1.1+(p_mag/2.3)], lW = [2] )
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])     

                N = 30
                x1 = np.linspace(0, p_coord, N)
                x2 = x1[::-1]
                y1 = -1.05 - x1/p_coord*p_mag + p_mag/2.3
                y2 = np.ones(N)*(-1.05 + p_mag/2.3)
                x = np.hstack((x1, x2))
                y = np.hstack((y1, y2))
                triangular_load_source.data  = dict(x=x, y=y)                   
                # labels_source.data = dict(x = [0,-0.2,f2_coord-0.2] , y = [-1,move_tri,move_tri],name = ['p','A','B'])

                labels_source.data = dict(x = [p_coord] , y = [-1.1],name = ['p'])
                support_source2.data = dict(sp2=[support2], x = [f2_coord-0.33] , y = [-0.1])
                support_source1.data = dict(sp1=[support1], x= [-0.325], y= [-0.1])
            else:
                p_arrow_source1.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                p_arrow_source2.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                p_arrow_source3.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
                triangular_load_source.data  = dict(x=[], y=[])                    
                # labels_source.data = dict(x = [-0.2,f2_coord-0.2] , y = [move_tri,move_tri],name = ['A','B'])
                labels_source.data = dict(x = [] , y = [],name = [])
                support_source2.data = dict(sp2=[support2], x = [f2_coord-0.33] , y = [-0.1])
                support_source1.data = dict(sp1=[support1], x= [-0.325], y= [-0.1]) 


            # if (p_mag<0):   
            #     p_arrow_source1.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
            #     p_arrow_source2.data = dict(xS= [p_coord/2.0], xE= [p_coord/2.0], yS= [1-p_mag/2.0], yE=[1], lW = [2] )
            #     p_arrow_source3.data = dict(xS= [p_coord], xE= [p_coord], yS= [1-(p_mag)], yE=[1], lW = [2] )
            #     constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])                
            #     labels_source.data = dict(x = [0,0,f2_coord-0.2] , y = [1,move_tri,move_tri],name = ['p','A','B'])
            #     support_source2.data = dict(sp2=[support2], x = [f2_coord-0.33] , y = [-0.1])
            #     support_source1.data = dict(sp1=[support1], x= [-0.325], y= [-0.1])
            # else:
            #     p_arrow_source1.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
            #     p_arrow_source2.data = dict(xS= [p_coord/2.0], xE= [p_coord/2.0], yS= [-1-(p_mag)/2.0], yE=[-1], lW = [2] )
            #     p_arrow_source3.data = dict(xS= [p_coord], xE= [p_coord], yS= [-1-p_mag], yE=[-1], lW = [2] )      
            #     constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])                          
            #     labels_source.data = dict(x = [0,-0.2,f2_coord-0.2] , y = [-1,move_tri,move_tri],name = ['p','A','B'])
            #     support_source2.data = dict(sp2=[support2], x = [f2_coord-0.33] , y = [-0.1])
            #     support_source1.data = dict(sp1=[support1], x= [-0.325], y= [-0.1])
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
plot = Figure(title="Beam with Supports and Load", x_range=(x0-.5,xf+.5), y_range=(-2.5,2.5), height = 400, logo=None)
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
plot1.line(x="x", y="y", source=mom_source, color='blue',line_width=2)

#EDIT:
# mom_glyph = Quadratic(x0= "x0", y0= "y0", cx= "x1", cy= "y1", x1= "x3", y1= "y3", line_color='blue', line_width=5)
# plot1.add_glyph(mom_source, mom_glyph)

plot1.line(x= [x0-1,xf+1], y = [0, 0], color = 'black', line_width =2 ,line_alpha = 0.4, line_dash=[1])
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
plot2.line(x='x', y='y', source=shear_source, color='red',line_width=2)

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
p_arrow_glyph1 = Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=p_arrow_source1,line_color="#0065BD")
p_arrow_glyph2 = Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=p_arrow_source2,line_color="#0065BD")
p_arrow_glyph3 = Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=p_arrow_source3,line_color="#0065BD")        
#Position 2 arrow:
f2_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 2,size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_width = "lW", source=f2_arrow_source,line_color="#E37222")
#Position 1 arrow:
f1_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 2,size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width = "lW", source=f1_arrow_source,line_color="#E37222" )

#EDIT: load-shapes glyph
constant_load_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#0065BD", fill_alpha=0.5)
triangular_load_glyph = Patch(x="x", y="y", fill_color="#0065BD",  fill_alpha=0.5)

###add layouts:
plot.add_layout(labels)
plot.add_layout(p_arrow_glyph1)
plot.add_layout(p_arrow_glyph2)
plot.add_layout(p_arrow_glyph3)
plot.add_layout(f2_arrow_glyph)
plot.add_layout(f1_arrow_glyph)
#EDIT: Add load-shapes glyphs
plot.add_glyph(constant_load_source,constant_load_glyph)
plot.add_glyph(triangular_load_source, triangular_load_glyph)

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
radio_button_group.on_change('active', Fun_Update)
button.on_click(initial)

#main:
initial()

curdoc().add_root( row( column(Spacer(height=115,width=350), widgetbox(radio_button_group), p_loc_slide, p_mag_slide, f2_loc_slide, widgetbox(button)),  column(plot,plot2,plot1 ) ) )
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
