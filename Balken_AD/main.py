# Main file:
from bokeh.plotting import Figure, output_file , show
from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, Arrow
from bokeh.models.glyphs import ImageURL, Quadratic, Rect, Patch
from bokeh.models.layouts import Spacer
from bokeh.layouts import column, row, widgetbox, layout
from bokeh.io import curdoc, output_file, show
from bokeh.models.widgets import Button, CheckboxGroup, RadioButtonGroup
import numpy as np
import math
# from os.path import dirname, join, split

from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexDiv, LatexLabel, LatexLabelSet, LatexSlider, LatexLegend

# Global Beam Properties:
resol = 100             # resolution of deflection visualization
resol_plo = 1000        # resolution of forces plot
x0 = 0.0                  # starting value of beam
xf = 10.0
E  = 2.0e1              # modulus of elasticity
I  = 30.0                 # moment of inertia
length  = xf-x0         # length of beam
p_mag = []             # initialize the p force
p_magi = 1.0
p_loci = xf/2           # initial location of load
f2_loci = xf            # initial location of second support             
plotwidth = 20.0
loadoptionsi = 0

global showvar          # Declaration of global auxiliary variable to determine if support forces should be diplayed
showvar = -1            # Initial value = -1 -> hide support forces

x_length = np.linspace(x0,xf,resol_plo)     # initialize Arrays for Forces Plot
y_mom = []                                  # Declaration of momentum plot vector
y_shear = []                                # Declaration of shear forces plot vector

# Sources:
# Plot source:
plot_source = ColumnDataSource(data=dict(x = np.linspace(x0,xf,resol), y = np.ones(resol) * 0 ))
# Plot label Source:
plot1_label_source   = ColumnDataSource(data=dict(x=[], y=[], names=[]))
plot2_label_source   = ColumnDataSource(data=dict(x=[], y=[], names=[]))
# Moment Source:
mom_source = ColumnDataSource(data=dict(x=[], y=[]))
# Shear Source:
shear_source = ColumnDataSource(data=dict(x=[] , y=[]))
# Support Forces Source:
support_label_source = ColumnDataSource(data=dict(x=[] , y=[], names=[]))
# Beam Measurement Label Source:
beam_measure_label_source = ColumnDataSource(data=dict(x=[] , y=[], names=[]))
# Arrow Sources:
beam_doublearrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
p_arrow_source1 = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
p_arrow_source2 = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
p_arrow_source3 = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
f2_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
f1_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
# Load Shapes Sources:
constant_load_source  = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
triangular_load_source  = ColumnDataSource(data=dict(x=[], y=[]))
# Label Source:
labels_source = ColumnDataSource(data=dict(x=[] , y=[], name = []))
# Support Source:
support1 = "Balken_AD/static/images/auflager02.svg"
support2 = "Balken_AD/static/images/auflager01.svg"
support_source1 = ColumnDataSource(data=dict(sp1=[], x=[] , y=[]))
support_source2 = ColumnDataSource(data=dict(sp2=[], x=[] , y=[]))
# Cantilever rectangle source:
quad_source = ColumnDataSource(data=dict(top= [], bottom= [],left = [], right =[]))
segment_source = ColumnDataSource(data=dict(x0= [], y0= [],x1 = [], y1 =[]))

# Sliders:
p_loc_slide= LatexSlider(title="\\mathrm{Load \ Position}", value_unit='\\frac{\\mathrm{L}}{\\mathrm{10}}', value= p_loci,start = x0, end = xf, step = 1.0)
p_mag_slide = LatexSlider(title="\\mathrm{Load \ Amplitude}", value = 1.0, start=-1.0, end=1.0, step=2.0)
f2_loc_slide = LatexSlider(title="\\mathrm{Support \ Position}", value_unit='\\frac{\\mathrm{L}}{\\mathrm{10}}', value=f2_loci,start = x0, end = xf, step = 1.0)

radio_button_group = RadioButtonGroup(
        labels=["Point Load", "Constant Load", "Triangular Load"], active=loadoptionsi, width = 600)


# FUNCTION: Calculation of deflection:
def Fun_Deflection(a,b,l,p_mag,x):
    ynew = []
    for i in range(0,int(resol) ):
        dy = 0
        ynew.append(dy)
    return ynew    

# FUNCTION: Cantilever Deflection function:
def Fun_C_Deflection(p,b,x):
    '''Calculates the deflection of the beam when it is cantilever'''

    ynew = []
    for i in range(0,int(resol) ):
        dy = 0
        ynew.append(dy)
    return ynew  
    
# FUNCTION: Cantilever function:
# If position of Support 2 is 0, this function is called:
def Fun_Cantilever():
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
        support_source2.data = dict(sp2=[], x = [] , y = [])
        support_source1.data = dict(sp1=[], x = [] , y = [])

#FUNCTION: Update:
def Fun_Update(attrname, old, new):
     
    plot1_label_source.data = dict(x=[], y=[], names=[])    
    plot2_label_source.data = dict(x=[], y=[], names=[])
    support_label_source.data = dict(x=[], y=[], names=[])

# IF POINT LOAD SELECTED ###########################################################################################################
    if radio_button_group.active == 0:   
        
        p_loc_slide.disabled = False
        my_line.glyph.line_width = 15

        a = p_loc_slide.value
        f2_coord = f2_loc_slide.value
        b = f2_coord - a
        p_coord = p_loc_slide.value
        p_mag = p_mag_slide.value
        l = f2_coord
        x1 = xf - l

#####################        
        if f2_coord == 0: # CANTILEVER MODE
#####################         
            xcan = x0
            Fun_Cantilever()
            if (p_mag>0):
                p_arrow_source1.data = dict(xS= [p_coord], xE= [p_coord], yE= [1-(p_mag/2.3)], yS=[1+(p_mag/2.3)], lW = [2] )
                p_arrow_source2.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                p_arrow_source3.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                labels_source.data = dict(x = [p_coord] , y = [1],name = ['F'])
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
                triangular_load_source.data  = dict(x=[], y=[])                
            else:
                p_arrow_source1.data = dict(xS= [p_coord], xE= [p_coord], yE= [-1.1-(p_mag/2.3)], yS=[-1.1+(p_mag/2.3)], lW = [2] )
                p_arrow_source2.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                p_arrow_source3.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                labels_source.data = dict(x = [p_coord] , y = [-1.1],name = ['F'])
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
                triangular_load_source.data  = dict(x=[], y=[])                

            # Moment and shear calculation:
            y_mom=[]
            y_shear=[]
            for i in range(0,resol_plo):
                if x_length[i]<=a :
                    y_shear.append(p_mag)
                    y_mom.append(p_mag *a*(1-x_length[i]/a))
                if x_length[i]>a :
                    y_shear.append(0)
                    y_mom.append(0)   
            mom_source.data = dict(x=x_length, y=y_mom)
            shear_source.data = dict(x=x_length, y=y_shear)

            ynew = Fun_C_Deflection(p_mag,a,plot_source.data['x'])
            plot_source.data = dict(x = np.linspace(x0,xf,resol), y = ynew)

#####################
        else: 
#####################
            quad_source.data = dict(top = [], bottom = [], left = [] , right = [])
            segment_source.data = dict(x0= [], y0= [],x1 = [], y1 =[])

            f1_mag = float(-1.0 * (p_mag *b) / l)
            f2_mag = float(-1.0 * (p_mag *a) / l)
            ynew = Fun_Deflection(a,b,l,p_mag,plot_source.data['x'])
            plot_source.data = dict(x = np.linspace(x0,xf,resol), y = ynew)
            move_tri = -0.4

            # Moment and shear calculation:
            y_mom = []
            y_shear = []
            if (l >= a):
                if (p_coord!=f2_coord):            
                    for i in range(0,resol_plo):
                        if x_length[i]<a:
                            y_shear.append(-1.0*f1_mag)
                            y_mom.append(f1_mag*x_length[i])
                        if x_length[i]>=a and x_length[i]<=l:
                            y_shear.append(-1.0*(f1_mag+p_mag))
                            y_mom.append(f1_mag*a+(f1_mag+p_mag)*(x_length[i]-a))
                        if x_length[i]>l:
                            y_shear.append(-1.0*(f1_mag+p_mag+f2_mag))
                            y_mom.append(f1_mag*a+(f1_mag+p_mag)*(l-a))
                else:
                    for i in range(0,resol_plo):
                        y_shear.append(0)
                        y_mom.append(0)
                mom_source.data = dict(x=x_length, y=y_mom)
                shear_source.data = dict(x=x_length, y=y_shear)
            else:            
                for i in range(0,resol_plo):
                    if x_length[i]<l:
                        y_shear.append(-1.0*f1_mag)
                        y_mom.append(f1_mag*x_length[i])                      
                    if x_length[i]>=l and x_length[i]<=a:
                        y_shear.append(-1.0*(f1_mag+f2_mag))
                        y_mom.append(f1_mag*l+(f1_mag+f2_mag)*(x_length[i]-l))
                    if x_length[i]>a:
                        y_shear.append(-1.0*(f1_mag+p_mag+f2_mag))
                        y_mom.append(f1_mag*l+(f1_mag+f2_mag)*(a-l))
                mom_source.data = dict(x=x_length, y=y_mom)
                shear_source.data = dict(x=x_length, y=y_shear)

            # Show max Values:    
            if (p_coord==5 and f2_coord==10 ):
                if p_mag>0:
                    plot1_label_source.data = dict(x=[5.25,5.25,5.25,4.4,4.5,4.5,4.87,4.87], y=[0.8,0.78,0.45,-0.2,-0.22,-0.55,-0.38,0.62], names=["F","_","2","-F","_","2","x","x"])
                    plot2_label_source.data = dict(x=[4.8,4.8,4.85,4.87], y=[0.8,0.78,-0.55,-2.0], names=["FL","__","4","x"])
                else:
                    plot1_label_source.data = dict(x=[4.4,4.5,4.5,5.25,5.25,5.25,4.87,4.87], y=[0.8,0.78,0.45,-0.2,-0.22,-0.55,-0.38,0.62], names=["-F","_","2","F","_","2","x","x"])
                    plot2_label_source.data = dict(x=[4.8,4.8,4.85,4.87], y=[0.8,0.78,-0.55,3.0], names=["FL","__","4","x"])

            # p_arrow and labels:
            if (p_mag>0):
                p_arrow_source1.data = dict(xS= [p_coord], xE= [p_coord], yS= [1+(p_mag/2.3)], yE=[1-(p_mag/2.3)], lW = [2] )
                p_arrow_source2.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                p_arrow_source3.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
                triangular_load_source.data  = dict(x=[], y=[])                
                labels_source.data = dict(x = [p_coord] , y = [1],name = ['F'])
                support_source2.data = dict(sp2=[support2], x = [f2_coord-0.33] , y = [-0.1])
                support_source1.data = dict(sp1=[support1], x= [-0.325], y= [-0.1])
            else:
                p_arrow_source1.data = dict(xS= [p_coord], xE= [p_coord], yS= [-1.1+(p_mag/2.3)], yE=[-1.1-(p_mag/2.3)], lW = [2] )
                p_arrow_source2.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                p_arrow_source3.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
                triangular_load_source.data  = dict(x=[], y=[])                
                labels_source.data = dict(x = [p_coord] , y = [-1.1],name = ['F'])
                support_source2.data = dict(sp2=[support2], x = [f2_coord-0.33] , y = [-0.1])
                support_source1.data = dict(sp1=[support1], x= [-0.325], y= [-0.1])

            # f1_arrow:
            if (p_mag<0):
                if (f1_mag>0):
                    f1_arrow_source.data = dict(xS= [0], xE= [0], yE= [0.8], yS=[1+(math.atan(f1_mag)/1.1)], lW = [1.0+2.0*math.atan(f1_mag*0.05)])
                elif (f1_mag<0):                
                    f1_arrow_source.data = dict(xS= [0], xE= [0], yE= [1-(math.atan(f1_mag)/1.1)], yS=[0.8], lW = [1.0-2.0*math.atan(f1_mag*0.05)])
                else:                    
                    f1_arrow_source.data = dict(xS= [], xE= [], yE= [], yS=[], lW = [])
            else:
                if (f1_mag>0):                    
                    f1_arrow_source.data = dict(xS= [0], xE= [0], yE= [-1-(math.atan(f1_mag)/1.1)], yS=[-0.8], lW = [1.0+2.0*math.atan(f1_mag*0.05)])
                elif (f1_mag<0):                
                    f1_arrow_source.data = dict(xS= [0], xE= [0], yE= [-0.8], yS=[-1+(math.atan(f1_mag)/1.1)], lW = [1.0-2.0*math.atan(f1_mag*0.05)])
                else:                    
                    f1_arrow_source.data = dict(xS= [], xE= [], yE= [], yS=[], lW = [])            
            # f2_arrow:
            if (p_mag<0):
                if (f2_mag>0 and p_coord!=0):
                    f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yE= [0.8], yS=[1+(math.atan(f2_mag)/1.1)], lW = [1.0+2.0*math.atan(f2_mag*0.05)])
                elif (f2_mag<0 and p_coord!=0):
                    f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yE= [1-(math.atan(f2_mag)/1.1)], yS=[0.8], lW = [1.0-2.0*math.atan(f2_mag*0.05)])
                else:                    
                    f2_arrow_source.data = dict(xS= [], xE= [], yE= [], yS=[], lW = [])
            else:
                if (f2_mag>0 and p_coord!=0):
                    f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yE= [-1-(math.atan(f2_mag)/1.1)], yS=[-0.8], lW = [1.0+2.0*math.atan(f2_mag*0.05)])
                elif (f2_mag<0 and p_coord!=0):
                    f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yE= [-0.8], yS=[-1+(math.atan(f2_mag)/1.1)], lW = [1.0-2.0*math.atan(f2_mag*0.05)])
                else:                    
                    f2_arrow_source.data = dict(xS= [], xE= [], yE= [], yS=[], lW = [])
            
            # Show Support Forces
            if (showvar==1):
                if (p_mag>0):
                    if (f2_coord==10):
                        support_label_source.data = dict(x=[0.1,0.6, f2_coord-0.9, f2_coord-0.4], y=[-1.3, -1.3, -1.3, -1.3], names=["%.2f" % round(abs(f1_mag),2), "F", "%.2f" % round(abs(f2_mag),2), "F"])
                    else:
                        support_label_source.data = dict(x=[0.1,0.6, f2_coord+0.1, f2_coord+0.6], y=[-1.3, -1.3, -1.3, -1.3], names=["%.2f" % round(abs(f1_mag),2), "F", "%.2f" % round(abs(f2_mag),2), "F"])
                else:
                    if (f2_coord==10):                    
                        support_label_source.data = dict(x=[0.1,0.6, f2_coord-0.9, f2_coord-0.4], y=[1.3, 1.3, 1.3, 1.3], names=["%.2f" % round(abs(f1_mag),2), "F", "%.2f" % round(abs(f2_mag),2), "F"])
                    else:
                        support_label_source.data = dict(x=[0.1,0.6, f2_coord+0.1, f2_coord+0.6], y=[1.3, 1.3, 1.3, 1.3], names=["%.2f" % round(abs(f1_mag),2), "F", "%.2f" % round(abs(f2_mag),2), "F"])
# IF CONSTANT LOAD SELECTED ###########################################################################################################
    if radio_button_group.active == 1: 

        p_loc_slide.disabled = False
        my_line.glyph.line_width = 15

        p_mag = float(p_mag_slide.value)
        a = float(p_loc_slide.value)
        l = float(f2_loc_slide.value)
        f2_coord = float(f2_loc_slide.value)
        p_coord = float(p_loc_slide.value)
        b = l - a
        x1 = xf - l
#####################
        if f2_coord == 0: # CANTILEVER MODE
#####################            
            xcan = x0
            Fun_Cantilever()

            if (p_mag>0) and (p_coord!=0):
                p_arrow_source1.data = dict(xS= [0.2*p_coord], xE= [0.2*p_coord], yE= [1-(p_mag/2.3)], yS=[1+(p_mag/2.3)], lW = [2] )
                p_arrow_source2.data = dict(xS= [p_coord/2.0], xE= [p_coord/2.0], yE= [1-(p_mag/2.3)], yS=[1+(p_mag/2.3)], lW = [2] )
                p_arrow_source3.data = dict(xS= [p_coord*(1-0.2)], xE= [p_coord*(1-0.2)], yE= [1-(p_mag/2.3)], yS=[1+(p_mag/2.3)], lW = [2] )
                constant_load_source.data  = dict(x=[p_coord/2.0], y=[1], w=[p_coord], h=[p_mag], angle=[0])
                triangular_load_source.data  = dict(x=[], y=[])                
                labels_source.data = dict(x = [p_coord] , y = [1],name = ['p'])            
            elif (p_mag<0) and (p_coord!=0):
                p_arrow_source1.data = dict(xS= [0.2*p_coord], xE= [0.2*p_coord], yE= [-1.1-(p_mag/2.3)], yS=[-1.1+(p_mag/2.3)], lW = [2] )
                p_arrow_source2.data = dict(xS= [p_coord/2.0], xE= [p_coord/2.0], yE= [-1.1-(p_mag/2.3)], yS=[-1.1+(p_mag/2.3)], lW = [2] )
                p_arrow_source3.data = dict(xS= [p_coord*(1-0.2)], xE= [p_coord*(1-0.2)], yE= [-1.1-(p_mag/2.3)], yS=[-1.1+(p_mag/2.3)], lW = [2] )
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

            # Moment and shear calculation:
            y_mom=[]
            y_shear=[]
            fac_m=0.25
            fac_s=0.15
            for i in range(0,resol_plo):
                if x_length[i]<a :
                    y_shear.append(fac_s*(p_mag*a - p_mag*x_length[i]))
                    y_mom.append(fac_m*(p_mag*a**2.0/2.0-p_mag*x_length[i]**2.0/2.0) )
                if x_length[i]>=a :
                    y_shear.append(0)
                    y_mom.append(0)
            mom_source.data = dict(x=x_length, y=y_mom)
            shear_source.data = dict(x=x_length, y=y_shear)


            ynew = Fun_C_Deflection(p_mag,a,plot_source.data['x'])
            plot_source.data = dict(x = np.linspace(x0,xf,resol), y = ynew)

#####################
        else: # Double Supported Beam Mode
#####################
            quad_source.data = dict(top = [], bottom = [], left = [] , right = [])
            segment_source.data = dict(x0= [], y0= [],x1 = [], y1 =[])

            ynew = Fun_Deflection(a,b,l,p_mag,plot_source.data['x'])
            plot_source.data = dict(x = np.linspace(x0,xf,resol), y = ynew)
            move_tri = -0.4

            # Moment and shear calculation:
            y_mom = []
            y_shear = []
            fac_m=0.25
            fac_s=0.15
            if (l >= a):
                f1_mag = -1.0* p_mag*a/l*(l - a + a/2.0)
                f2_mag = -1.0* ( p_mag* a**2.0 ) / 2.0 / l
                for i in range(0,resol_plo):
                    if x_length[i]<a:
                        y_shear.append(-fac_s*(f1_mag + p_mag*x_length[i]))
                        y_mom.append(fac_m*(f1_mag*x_length[i] + p_mag*x_length[i]**2/2.0))
                    if x_length[i]>=a and x_length[i]<=l:
                        y_shear.append(-fac_s*(f1_mag + p_mag* a))
                        y_mom.append(fac_m*(f1_mag*a + (p_mag*a**2.0)/2.0 + (f1_mag + p_mag*a)*(x_length[i]-a)))
                    if x_length[i]>l:
                        y_shear.append(-fac_s*(f1_mag + p_mag*a + f2_mag ))
                        y_mom.append(fac_m*(f1_mag*a + (p_mag*a**2.0)/2.0 + (f1_mag + p_mag*a)*(l-a) + ( f1_mag + p_mag*a + f2_mag) * (x_length[i]-l) ) )
                mom_source.data = dict(x=x_length, y=y_mom)
                shear_source.data = dict(x=x_length, y=y_shear)

            else: # if l<a
                f1_mag = -1.0*p_mag*a/l*(l-a/2.0)
                f2_mag = -1.0*p_mag* a**2.0/2.0/l
                for i in range(0,resol_plo):
                    if x_length[i]<l:
                        y_shear.append(-fac_s*(f1_mag + p_mag*x_length[i]))
                        y_mom.append(fac_m*(f1_mag*x_length[i] + p_mag*x_length[i]**2.0/2.0))
                    if x_length[i]>=l and x_length[i]<=a:
                        y_shear.append(-fac_s*(f1_mag + p_mag *l + f2_mag + p_mag*(x_length[i]-l)))
                        y_mom.append(fac_m*(f1_mag*l + p_mag*l**2.0/2.0 + (f1_mag + p_mag*l+f2_mag)*(x_length[i]-l) + p_mag*(x_length[i]-l)**2.0/2.0))
                    if x_length[i]>a:
                        y_shear.append(-fac_s*(f1_mag + p_mag *l + f2_mag + p_mag*(a-l)))
                        y_mom.append(fac_m*(f1_mag*l + p_mag*l**2.0/2.0 + (f1_mag + p_mag*l+f2_mag)*(a-l) + p_mag*(a-l)**2.0/2.0 + (f1_mag + p_mag *l + f2_mag + p_mag*(a-l))* (x_length[i]-a)))
                mom_source.data = dict(x=x_length, y=y_mom)
                shear_source.data = dict(x=x_length, y=y_shear)

            # Show max values:
            if (p_coord==10 and f2_coord==10 ):
                if p_mag >0:
                    plot1_label_source.data = dict(x=[0.0,0.0,0.05,9.4,9.5,9.55,-0.12,9.83], y=[0.25,0.18,-0.15,0.25,0.18,-0.15,0.87,-0.617], names=["pL","__","2","-pL","__","2","x","x"])
                    plot2_label_source.data = dict(x=[4.8,4.8,4.85,5.1,4.87], y=[0.90,0.78,-0.55,1.5,-2.6], names=["pL","__","8","2","x"])                    
                    
                else:
                    plot1_label_source.data = dict(x=[0.0,0.0,0.05,9.4,9.5,9.55,-0.12,9.83], y=[0.25,0.18,-0.15,0.25,0.18,-0.15,-0.617,0.87], names=["pL","__","2","-pL","__","2","x","x"])
                    plot2_label_source.data =dict(x=[4.8,4.8,4.85,5.1,4.87], y=[0.90,0.78,-0.55,1.5,3.6], names=["pL","__","8","2","x"])   

            # p_arrow and labels:
            if (p_mag>0) and (p_coord!=0):
                p_arrow_source1.data = dict(xS= [0.2*p_coord], xE= [0.2*p_coord], yE= [1-(p_mag/2.3)], yS=[1+(p_mag/2.3)], lW = [2] )
                p_arrow_source2.data = dict(xS= [p_coord/2.0], xE= [p_coord/2.0], yE= [1-(p_mag/2.3)], yS=[1+(p_mag/2.3)], lW = [2] )
                p_arrow_source3.data = dict(xS= [p_coord*(1-0.2)], xE= [p_coord*(1-0.2)], yE= [1-(p_mag/2.3)], yS=[1+(p_mag/2.3)], lW = [2] )
                constant_load_source.data  = dict(x=[p_coord/2.0], y=[1], w=[p_coord], h=[p_mag], angle=[0])
                triangular_load_source.data  = dict(x=[], y=[])                
                labels_source.data = dict(x = [p_coord] , y = [1],name = ['p'])
                support_source2.data = dict(sp2=[support2], x = [f2_coord-0.33] , y = [-0.1])
                support_source1.data = dict(sp1=[support1], x= [-0.325], y= [-0.1])      
            elif (p_mag<0) and (p_coord!=0):
                p_arrow_source1.data = dict(xS= [0.2*p_coord], xE= [0.2*p_coord], yE= [-1.1-(p_mag/2.3)], yS=[-1.1+(p_mag/2.3)], lW = [2] )
                p_arrow_source2.data = dict(xS= [p_coord/2.0], xE= [p_coord/2.0], yE= [-1.1-(p_mag/2.3)], yS=[-1.1+(p_mag/2.3)], lW = [2] )
                p_arrow_source3.data = dict(xS= [p_coord*(1-0.2)], xE= [p_coord*(1-0.2)], yE= [-1.1-(p_mag/2.3)], yS=[-1.1+(p_mag/2.3)], lW = [2] )
                constant_load_source.data  = dict(x=[p_coord/2.0], y=[-1.1], w=[p_coord], h=[p_mag], angle=[0])
                triangular_load_source.data  = dict(x=[], y=[])                
                labels_source.data = dict(x = [p_coord] , y = [-1.1],name = ['p'])
                support_source2.data = dict(sp2=[support2], x = [f2_coord-0.33] , y = [-0.1])
                support_source1.data = dict(sp1=[support1], x= [-0.325], y= [-0.1])
            else: 
                p_arrow_source1.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                p_arrow_source2.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                p_arrow_source3.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
                triangular_load_source.data  = dict(x=[], y=[])                
                labels_source.data = dict(x = [] , y = [],name = [])
                support_source2.data = dict(sp2=[support2], x = [f2_coord-0.33] , y = [-0.1])
                support_source1.data = dict(sp1=[support1], x= [-0.325], y= [-0.1]) 

            # f1_arrow:
            if (p_mag<0 and p_coord!=0):
                if (f1_mag>0):
                    f1_arrow_source.data = dict(xS= [0], xE= [0], yE= [0.8], yS=[1+(math.atan(f1_mag)/1.1)], lW = [1.0+2.0*math.atan(f1_mag*0.05)])
                else:
                    f1_arrow_source.data = dict(xS= [0], xE= [0], yE= [1-(math.atan(f1_mag)/1.1)], yS=[0.8], lW = [1.0-2.0*math.atan(f1_mag*0.05)])
            elif (p_mag>0 and p_coord!=0):
                if (f1_mag>0):
                    f1_arrow_source.data = dict(xS= [0], xE= [0], yE= [-1-(math.atan(f1_mag)/1.1)], yS=[-0.8], lW = [1.0+2.0*math.atan(f1_mag*0.05)])
                else:
                    f1_arrow_source.data = dict(xS= [0], xE= [0], yE= [-0.8], yS=[-1+(math.atan(f1_mag)/1.1)], lW = [1.0-2.0*math.atan(f1_mag*0.05)])
            else:
                 f1_arrow_source.data = dict(xS= [], xE= [], yE= [], yS=[], lW = [])

          # f2_arrow:
            if (p_mag<0 and p_coord!=0):
                if (f2_mag>0):
                    f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yE= [0.8], yS=[1+(math.atan(f2_mag)/1.1)], lW = [1.0+2.0*math.atan(f2_mag*0.05)])
                else:
                    f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yE= [1-(math.atan(f2_mag)/1.1)], yS=[0.8], lW = [1.0-2.0*math.atan(f2_mag*0.05)])
            elif (p_mag>0 and p_coord!=0):
                if (f2_mag>0):
                    f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yE= [-1-(math.atan(f2_mag)/1.1)], yS=[-0.8], lW = [1.0+2.0*math.atan(f2_mag*0.05)])
                else:
                    f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yE= [-0.8], yS=[-1+(math.atan(f2_mag)/1.1)], lW = [1.0-2.0*math.atan(f2_mag*0.05)])
            else:
                 f2_arrow_source.data = dict(xS= [], xE= [], yE= [], yS=[], lW = [])
                    
            # Show Support Forces
            if (showvar==1):
                if (p_mag>0):
                    if (f2_coord==10):
                        support_label_source.data = dict(x=[0.1,0.60, f2_coord-1.0, f2_coord-0.5], y=[-1.3, -1.3, -1.3, -1.3], names=["%.2f" % round(abs(f1_mag)/10,2), "pL", "%.2f" % round(abs(f2_mag)/10,2), "pL"])
                    else:
                        support_label_source.data = dict(x=[0.1,0.60, f2_coord+0.1, f2_coord+0.6], y=[-1.3, -1.3, -1.3, -1.3], names=["%.2f" % round(abs(f1_mag)/10,2), "pL", "%.2f" % round(abs(f2_mag)/10,2), "pL"])                               
                
                else:
                    if (f2_coord==10):
                        support_label_source.data = dict(x=[0.1,0.6, f2_coord-1.0, f2_coord-0.5], y=[1.3, 1.3, 1.3, 1.3], names=["%.2f" % round(abs(f1_mag)/10,2), "pL", "%.2f" % round(abs(f2_mag)/10,2), "pL"])
                    else:
                        support_label_source.data = dict(x=[0.1,0.6, f2_coord+0.1, f2_coord+0.6], y=[1.3, 1.3, 1.3, 1.3], names=["%.2f" % round(abs(f1_mag)/10,2), "pL", "%.2f" % round(abs(f2_mag)/10,2), "pL"])

# IF TRIANGULAR LOAD SELECTED ###########################################################################################################
    if radio_button_group.active == 2:
        
        p_loc_slide.disabled = False
        my_line.glyph.line_width = 15
        p_mag = float(p_mag_slide.value)
        a = float(p_loc_slide.value)
        l = float(f2_loc_slide.value)
        f2_coord = float(f2_loc_slide.value)
        p_coord = float(p_loc_slide.value)
        b = l - a
        x1 = xf - l

#####################
        if f2_coord == 0: #CANTILEVER MODE
#####################
            xcan = x0
            Fun_Cantilever()

            if (p_mag>0) and (p_coord!=0):
                p_arrow_source1.data = dict(xS= [0.2*p_coord], xE= [0.2*p_coord], yS= [1-p_mag/2.3+p_mag/10.0], yE=[1-p_mag/2.3], lW = [2] )
                p_arrow_source2.data = dict(xS= [p_coord/2.0], xE= [p_coord/2.0], yS= [1-p_mag/2.3+p_mag/2.6], yE=[1-(p_mag/2.3)], lW = [2] )
                p_arrow_source3.data = dict(xS= [p_coord*(1-0.2)], xE= [p_coord*(1-0.2)], yS= [1+(p_mag/2.3/1.9)], yE=[1-(p_mag/2.3)], lW = [2] )
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])     
              
                N = 30
                x1 = np.linspace(0, p_coord, N)
                x2 = x1[::-1]
                y1 = 0.95 + x1/p_coord*p_mag - p_mag/2.3
                y2 = np.ones(N)*(0.95 - p_mag/2.3)
                x = np.hstack((x1, x2))
                y = np.hstack((y1, y2))
                triangular_load_source.data  = dict(x=x, y=y)
                labels_source.data = dict(x = [p_coord] , y = [1],name = ['p'])

            elif (p_mag<=0) and (p_coord!=0):
                p_arrow_source1.data = dict(xS= [0.2*p_coord], xE= [0.2*p_coord], yS= [-1.1-p_mag/2.3+p_mag/10.0], yE=[-1.1-p_mag/2.3], lW = [2] )
                p_arrow_source2.data = dict(xS= [p_coord/2.0], xE= [p_coord/2.0], yS= [-1.1-p_mag/2.3+p_mag/2.6], yE=[-1.1-(p_mag/2.3)], lW = [2] )
                p_arrow_source3.data = dict(xS= [p_coord*(1-0.2)], xE= [p_coord*(1-0.2)], yS= [-1.1+(p_mag/2.3/1.9)], yE=[-1.1-(p_mag/2.3)], lW = [2] )
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])     

                # Shape triangular load:
                N = 30
                x1 = np.linspace(0, p_coord, N)
                x2 = x1[::-1]
                y1 = -1.05 + x1/p_coord*p_mag - p_mag/2.3
                y2 = np.ones(N)*(-1.05 - p_mag/2.3)
                x = np.hstack((x1, x2))
                y = np.hstack((y1, y2))
                triangular_load_source.data  = dict(x=x, y=y)                   
                labels_source.data = dict(x = [p_coord] , y = [-1.1],name = ['p'])
            else:
                p_arrow_source1.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                p_arrow_source2.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                p_arrow_source3.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
                triangular_load_source.data  = dict(x=[], y=[])     
                labels_source.data = dict(x = [] , y = [],name = [])

            # Moment and shear calculation:
            y_mom=[]
            y_shear=[]
            fac_m=0.25
            fac_s=0.15
            for i in range(0,resol_plo):
                if x_length[i]<a :
                    y_shear.append(fac_s*(p_mag*a/2.0-p_mag*x_length[i]/2.0))
                    y_mom.append( fac_m*(p_mag*a**2.0/3.0-p_mag*a/2.0*x_length[i] + p_mag/6.0/a*x_length[i]**3.0  ))
                if x_length[i]>=a :
                    y_shear.append(0)
                    y_mom.append(0)
            mom_source.data = dict(x=x_length, y=y_mom)
            shear_source.data = dict(x=x_length, y=y_shear)

            ynew = Fun_C_Deflection(p_mag,a,plot_source.data['x'])
            plot_source.data = dict(x = np.linspace(x0,xf,resol), y = ynew)


#####################
        else:
#####################
            quad_source.data = dict(top = [], bottom = [], left = [] , right = [])
            segment_source.data = dict(x0= [], y0= [],x1 = [], y1 =[])
            ynew = Fun_Deflection(a,b,l,p_mag,plot_source.data['x'])
            plot_source.data = dict(x = np.linspace(x0,xf,resol), y = ynew)
            move_tri = -0.4

            # Moment and shear calculation:
            y_mom = []
            y_shear = []
            fac_m=0.25
            fac_s=0.15
            if (l >= a):
                f1_mag = -1.0*p_mag*a/2.0/l*(l-a+a/3.0)
                f2_mag = -1.0*p_mag*a**2.0/l/3.0
                for i in range(0,resol_plo):
                    if x_length[i]<a:
                        y_shear.append(-fac_s*(f1_mag + p_mag*x_length[i]**2.0/2.0/a))
                        y_mom.append(fac_m*( f1_mag*x_length[i] + x_length[i]**3.0*p_mag/6.0/a))
                    if x_length[i]>=a and x_length[i]<=l:
                        y_shear.append( -fac_s*(f1_mag + p_mag*a/2.0 ))
                        y_mom.append(fac_m*(f1_mag*a + a**2.0*p_mag/6.0 + (f1_mag + p_mag*a/2.0)*(x_length[i]-a) ))
                    if x_length[i]>l:
                        y_shear.append( -fac_s*(f1_mag + p_mag*a/2.0 - p_mag*a**2.0/3.0/l))
                        y_mom.append( fac_m*(f1_mag*a + a**2.0*p_mag/6.0 + (f1_mag + p_mag*a/2.0)*(l-a) ) )
                mom_source.data = dict(x=x_length, y=y_mom)
                shear_source.data = dict(x=x_length, y=y_shear)

            else: # if l<a                
                f1_mag_1 = -1.0*p_mag*a/2.0/l*(l-a+a/3.0)
                f2_mag = -1.0* ( p_mag*a**2.0 /3.0/l )
                f1_mag = -1.0*(p_mag*a/2.0 + f2_mag)

                for i in range(0,resol_plo):
                    if x_length[i]<l:
                        y_shear.append(-fac_s*(f1_mag + p_mag*x_length[i]**2.0/2.0/a))
                        y_mom.append( fac_m*(f1_mag*x_length[i] + x_length[i]**3.0*p_mag/6.0/a))
                    if x_length[i]>=l and x_length[i]<=a:
                        y_shear.append(-fac_s*(f1_mag + p_mag*l**2.0 /2.0/a + f2_mag  + (l/a*p_mag*(x_length[i]-l) + (x_length[i]/a-l/a)*p_mag*(x_length[i]-l)/2.0) ))
                        y_mom.append(fac_m*((f1_mag*l + p_mag*l**3.0 /6.0/a) + f2_mag*(x_length[i]-l)  + (f1_mag + p_mag*l**2.0/2.0/a)*(x_length[i]-l) + (l/a*p_mag*(x_length[i]-l))*(1.0/2.0)*(x_length[i]-l) + ((x_length[i]/a-l/a)*p_mag*(x_length[i]-l)/2.0)*(1.0/3.0)*(x_length[i]-l) ))
                    if x_length[i]>a:
                        y_shear.append( 0 )
                        y_mom.append( 0 ) 
                    
                mom_source.data = dict(x=x_length, y=y_mom)
                shear_source.data = dict(x=x_length, y=y_shear)


            # Show max values:
            if (p_coord==10 and f2_coord==10 ):
                if p_mag >0:
                    plot1_label_source.data = dict(x=[0.0,0.0,0.05,9.4,9.5,9.55,-0.12,9.83], y=[0.15,0.08,-0.25,0.25,0.18,-0.15,0.375,-0.4], names=["pL","__","6","-pL","__","3","x","x"])  
                    plot2_label_source.data = dict(x=[4.8,4.5,4.5,5.1,4.87], y=[1.5,1.38,0.05,2.1,-1.1], names=["pL","______","9*sqrt(3)","2","x"])
                else:
                    plot1_label_source.data = dict(x=[0.0,0.0,0.05,9.4,9.5,9.55,-0.12,9.83], y=[0.45,0.38,0.05,0.25,0.18,-0.15,-0.13,0.62], names=["pL","__","6","-pL","__","3","x","x"])
                    plot2_label_source.data =dict(x=[4.8,4.5,4.5,5.1,4.87], y=[0.3,0.18,-1.15,0.9,2.0], names=["pL","______","9*sqrt(3)","2","x"])

            # p_arrow and labels:
            if (p_mag>0) and (p_coord!=0):
                p_arrow_source1.data = dict(xS= [0.2*p_coord], xE= [0.2*p_coord], yS= [1-p_mag/2.3+p_mag/10.0], yE=[1-p_mag/2.3], lW = [2] )
                p_arrow_source2.data = dict(xS= [p_coord/2.0], xE= [p_coord/2.0], yS= [1-p_mag/2.3+p_mag/2.6], yE=[1-(p_mag/2.3)], lW = [2] )
                p_arrow_source3.data = dict(xS= [p_coord*(1-0.2)], xE= [p_coord*(1-0.2)], yS= [1+(p_mag/2.3/1.9)], yE=[1-(p_mag/2.3)], lW = [2] )
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])     

                # Shape triangular load
                N = 30
                x1 = np.linspace(0, p_coord, N)
                x2 = x1[::-1]
                y1 = 0.95 + x1/p_coord*p_mag - p_mag/2.3
                y2 = np.ones(N)*(0.95 - p_mag/2.3)
                x = np.hstack((x1, x2))
                y = np.hstack((y1, y2))
                triangular_load_source.data  = dict(x=x, y=y)
                        
                labels_source.data = dict(x = [p_coord] , y = [1],name = ['p'])
                support_source2.data = dict(sp2=[support2], x = [f2_coord-0.33] , y = [-0.1])
                support_source1.data = dict(sp1=[support1], x= [-0.325], y= [-0.1])
            elif (p_mag<=0) and (p_coord!=0):
                p_arrow_source1.data = dict(xS= [0.2*p_coord], xE= [0.2*p_coord], yS= [-1.1-p_mag/2.3+p_mag/10.0], yE=[-1.1-p_mag/2.3], lW = [2] )
                p_arrow_source2.data = dict(xS= [p_coord/2.0], xE= [p_coord/2.0], yS= [-1.1-p_mag/2.3+p_mag/2.6], yE=[-1.1-(p_mag/2.3)], lW = [2] )
                p_arrow_source3.data = dict(xS= [p_coord*(1-0.2)], xE= [p_coord*(1-0.2)], yS= [-1.1+(p_mag/2.3/1.9)], yE=[-1.1-(p_mag/2.3)], lW = [2] )
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])     

                N = 30
                x1 = np.linspace(0, p_coord, N)
                x2 = x1[::-1]
                y1 = -1.05 + x1/p_coord*p_mag - p_mag/2.3
                y2 = np.ones(N)*(-1.05 - p_mag/2.3)
                x = np.hstack((x1, x2))
                y = np.hstack((y1, y2))
                triangular_load_source.data  = dict(x=x, y=y)                   
                labels_source.data = dict(x = [p_coord] , y = [-1.1],name = ['p'])
                support_source2.data = dict(sp2=[support2], x = [f2_coord-0.33] , y = [-0.1])
                support_source1.data = dict(sp1=[support1], x= [-0.325], y= [-0.1])
            else:
                p_arrow_source1.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                p_arrow_source2.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                p_arrow_source3.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [] )
                constant_load_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
                triangular_load_source.data  = dict(x=[], y=[])                    
                labels_source.data = dict(x = [] , y = [],name = [])
                support_source2.data = dict(sp2=[support2], x = [f2_coord-0.33] , y = [-0.1])
                support_source1.data = dict(sp1=[support1], x= [-0.325], y= [-0.1]) 

            # f1_arrow:
            if (p_mag<0):
                if (f1_mag>0):
                    f1_arrow_source.data = dict(xS= [0], xE= [0], yE= [0.8], yS=[1+(math.atan(f1_mag)/1.1)], lW = [1.0+2.0*math.atan(f1_mag*0.05)])
                else:
                    f1_arrow_source.data = dict(xS= [0], xE= [0], yE= [1-(math.atan(f1_mag)/1.1)], yS=[0.8], lW = [1.0-2.0*math.atan(f1_mag*0.05)])
            else:
                if (f1_mag>0):
                    f1_arrow_source.data = dict(xS= [0], xE= [0], yE= [-1-(math.atan(f1_mag)/1.1)], yS=[-0.8], lW = [1.0+2.0*math.atan(f1_mag*0.05)])
                else:
                    f1_arrow_source.data = dict(xS= [0], xE= [0], yE= [-0.8], yS=[-1+(math.atan(f1_mag)/1.1)], lW = [1.0-2.0*math.atan(f1_mag*0.05)])
            # f2_arrow:
            if (p_mag<0):
                if (f2_mag>0):
                    f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yE= [0.8], yS=[1+(math.atan(f2_mag)/1.1)], lW = [1.0+2.0*math.atan(f2_mag*0.05)])
                else:
                    f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yE= [1-(math.atan(f2_mag)/1.1)], yS=[0.8], lW = [1.0-2.0*math.atan(f2_mag*0.05)])
            else:
                if (f2_mag>0):
                    f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yE= [-1-(math.atan(f2_mag)/1.1)], yS=[-0.8], lW = [1.0+2.0*math.atan(f2_mag*0.05)])
                else:
                    f2_arrow_source.data = dict(xS= [f2_coord], xE= [f2_coord], yE= [-0.8], yS=[-1+(math.atan(f2_mag)/1.1)], lW = [1.0-2.0*math.atan(f2_mag*0.05)])
                   
            # Show Support Forces
            if (showvar==1):
                if (p_mag>0):
                    if (f2_coord==10):
                        support_label_source.data = dict(x=[0.1,0.60, f2_coord-1.0, f2_coord-0.5], y=[-1.3, -1.3, -1.3, -1.3], names=["%.2f" % round(abs(f1_mag)/10,2), "pL", "%.2f" % round(abs(f2_mag)/10,2), "pL"])
                    else:
                        support_label_source.data = dict(x=[0.1,0.60, f2_coord+0.1, f2_coord+0.6], y=[-1.3, -1.3, -1.3, -1.3], names=["%.2f" % round(abs(f1_mag)/10,2), "pL", "%.2f" % round(abs(f2_mag)/10,2), "pL"])                
                else:
                    if (f2_coord==10):                    
                        support_label_source.data = dict(x=[0.1,0.6, f2_coord-1.0, f2_coord-0.5], y=[1.3, 1.3, 1.3, 1.3],  names=["%.2f" % round(abs(f1_mag)/10,2), "pL",  "%.2f" % round(abs(f2_mag)/10,2), "pL"])
                    else:
                        support_label_source.data = dict(x=[0.1,0.6, f2_coord+0.1, f2_coord+0.6], y=[1.3, 1.3, 1.3, 1.3],  names=["%.2f" % round(abs(f1_mag)/10,2), "pL", "%.2f" % round(abs(f2_mag)/10,2), "pL"])

# Initial function:
def initial():
    p_loc_slide.value = p_loci
    f2_loc_slide.value = f2_loci
    p_mag_slide.value = p_magi
    Fun_Update(None,None,None)
    support_source1.data = dict(sp1=[support1], x= [-0.325], y= [-0.1])
    beam_doublearrow_source.data = dict(xS= [0.05], xE= [9.95], yS= [-0.6], yE=[-0.6], lW = [5])
    beam_measure_label_source.data = dict(x=[4.85], y=[-0.8], names=["L"])

# Show function
def show():
    global showvar
    showvar = showvar*-1
    Fun_Update(None,None,None)

##########Plotting##########

####### Main Plot:
plot = Figure(title="Beam with Supports and Load", tools="", x_range=(x0-.5,xf+.5), y_range=(-2.5,2.5), height = 400, logo=None)
my_line=plot.line(x='x', y='y', source=plot_source, color='#0065BD',line_width=20)
plot.add_glyph(support_source1,ImageURL(url="sp1", x=-0.325, y=-0.1, w=0.66, h=0.4))
plot.add_glyph(support_source2,ImageURL(url="sp2", x='x', y='y', w=0.66, h=0.4))

plot.quad(top='top', bottom='bottom', left='left',
    right='right', source = quad_source, color='black', fill_alpha = 0.5)
plot.segment(x0='x0', y0='y0', x1='x1',
          y1='y1', source = segment_source, color='black', line_width=2)
plot.axis.visible = False
plot.outline_line_width = 2
plot.outline_line_color = "Black"
plot.title.text_font_size="13pt"
labels = LabelSet(x='x', y='y', text='name', level='glyph',
              x_offset=5, y_offset=-30, source=labels_source, render_mode='canvas')
support_label = LabelSet(x='x', y='y', text='names', source=support_label_source, text_color = "#A2AD00", level='glyph', x_offset=3, y_offset=-15, text_font_size="10pt")
beam_measure_label= LabelSet(x='x', y='y', text='names', source=beam_measure_label_source, text_color = 'black', level='glyph', x_offset=3, y_offset=-15)

####### Plot1 with shear:
plot1 = Figure(title="Shear Force", tools="", x_range=(x0-.5,xf+.5), y_range=(-1.5,1.5), height = 200, logo=None)
plot1_labels1 = LabelSet(x='x', y='y', text='names', source=plot1_label_source, text_color = "#A2AD00", level='glyph', x_offset=3, y_offset=-15)
plot1.add_layout(plot1_labels1)
plot1.line(x='x', y='y', source=shear_source, color="#A2AD00",line_width=2)
plot1.line(x= [x0-1,xf+1], y = [0, 0 ], color = 'black', line_width =2 ,line_alpha = 0.4, line_dash=[1])
plot1.line(x= [xf/2,xf/2], y = [-1.5,1.5], color = 'black', line_width =2 ,line_alpha = 0.4, line_dash=[1])
plot1.axis.visible = False
plot1.outline_line_width = 2
plot1.outline_line_color = "Black"
plot1.title.text_font_size="13pt"
plot1.square([0.0],[0.0],size=0,fill_color="#A2AD00",fill_alpha=0.5,legend="Shear Force")
plot1.legend.location = 'top_right'

####### Plot2 with moment:
plot2 = Figure(title="Bending Moment", tools="", x_range=(x0-.5,xf+.5), y_range=(-6,6), height = 200, logo=None)
plot2_labels1 = LabelSet(x='x', y='y', text='names', source=plot2_label_source, text_color ="#E37222", level='glyph', x_offset=3, y_offset=-15)
plot2.add_layout(plot2_labels1)
plot2.line(x="x", y="y", source=mom_source, color="#E37222",line_width=2)
plot2.line(x= [x0-1,xf+1], y = [0, 0], color = 'black', line_width =2 ,line_alpha = 0.4, line_dash=[1])
plot2.line(x= [xf/2,xf/2], y = [-6,6], color = 'black', line_width =2 ,line_alpha = 0.4, line_dash=[1])
plot2.axis.visible = False
plot2.outline_line_width = 2
plot2.outline_line_color = "Black"
plot2.title.text_font_size="13pt"
plot2.square([0.0],[0.0],size=0,fill_color="#E37222",fill_alpha=0.5,legend="Bending Moment")
plot2.legend.location = 'top_right'

### Arrow plotting:
# Beam measurements arrow:
beam_doublearrow_glyph = Arrow(start=OpenHead(line_color='black',line_width= 2, size=8), end=OpenHead(line_color='black',line_width= 2, size=8),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=beam_doublearrow_source,line_color='black')
# P arrow:
p_arrow_glyph1 = Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=p_arrow_source1,line_color="#0065BD")
p_arrow_glyph2 = Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=p_arrow_source2,line_color="#0065BD")
p_arrow_glyph3 = Arrow(end=OpenHead(line_color="#0065BD",line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=p_arrow_source3,line_color="#0065BD")        
# Position 2 arrow:
f2_arrow_glyph = Arrow(end=OpenHead(line_color="#0065BD",line_width= 3,size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_width = "lW", source=f2_arrow_source,line_color="#0065BD")
# Position 1 arrow:
f1_arrow_glyph = Arrow(end=OpenHead(line_color="#0065BD",line_width= 3,size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width = "lW", source=f1_arrow_source,line_color="#0065BD" )
# Load-shapes glyph
constant_load_glyph = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color="#0065BD", fill_alpha=0.5)
triangular_load_glyph = Patch(x="x", y="y", fill_color="#0065BD",  fill_alpha=0.5)

### add layouts:
plot.add_layout(labels)
plot.add_layout(p_arrow_glyph1)
plot.add_layout(p_arrow_glyph2)
plot.add_layout(p_arrow_glyph3)
plot.add_layout(f2_arrow_glyph)
plot.add_layout(f1_arrow_glyph)
plot.add_layout(beam_doublearrow_glyph)
plot.add_layout(support_label)
plot.add_layout(beam_measure_label)
plot.add_glyph(constant_load_source,constant_load_glyph)
plot.add_glyph(triangular_load_source, triangular_load_glyph)
### Reset Button
button = Button(label="Reset", button_type="success")
### Show Button
Showbutton = Button(label="Show/Hide Support Forces", button_type="success")
### on_change:
p_loc_slide.on_change('value', Fun_Update)
p_mag_slide.on_change('value', Fun_Update)
f2_loc_slide.on_change('value',Fun_Update)
radio_button_group.on_change('active', Fun_Update)
button.on_click(initial)
Showbutton.on_click(show)

### Add description from HTML file
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1140)

### Initialising all column data for the initial plots
initial()
### Arrange layout
doc_layout = layout(children=[column(description,row(column(Spacer(height=20,width=350),widgetbox(radio_button_group), p_loc_slide, p_mag_slide, f2_loc_slide, widgetbox(Showbutton), widgetbox(button)),  column(plot,plot1,plot2 ) ) ) ] )
curdoc().add_root(doc_layout)
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '