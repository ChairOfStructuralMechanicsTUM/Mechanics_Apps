#trash


'''
class SupportB(Force):
    def __init__(self,name):
        Force.__init__(self,name,0.0,1.0)

    def fun_clear(self):
        self.triangle_source = ColumnDataSource(data=dict(x= [], y= [], size = []))
        self.arrow_source.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [])
'''


class Force(Beam):
    def __init__(self,name,which=0):
        Beam.__init__(self)
        self.mag = 100.0
        self.magi = 100.0
        self.loci = self.xf/2
        self.loc = 0
        self.xS = 0
        self.xE = 0
        self.yS = 0
        self.yE = 0
        self.lW = 0
        self.name = name
        self.which = which
        self.dy = []                        #deflection caused by force
        self.arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))

        if (which == 2 ):
            print "hi"
            self.loc_slider = Slider(title=self.name + " lalaPosition",value = self.xf,start = self.x0, end = self.xf, step = 1/self.resol)
            self.loc = self.xf
        else:
            self.loc_slider = Slider(title=self.name + " Position",value = self.loci,start = self.x0, end = self.xf, step = 1/self.resol)

        self.mag_slider = Slider(title=self.name + " amplitude", value=self.magi, start=-2*self.magi, end=2*self.magi, step=1)
        self.arrow_glyph = Arrow(end=OpenHead(line_color="#003359",line_width= 4,size=10),
            x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width = "lW", source=self.arrow_source,line_color="#003359" )

    def change_loc(self):
        pass
    def change_mag(self):
        pass

    def update_arrow(self, l):
        if self.which==0:
            self.loc = self.loc_slider.value
            self.mag = self.mag_slider.value
        elif self.which==1: #A position support
            self.loc = 0
            #self.mag = fun_mag(self.b)
        elif self.which==2: #B position support
            self.loc = self.loc_slider.value
            #self.mag = fun_mag(self.a)

        self.xS = [self.loc]
        self.xE = [self.loc]
        self.lW = [abs(self.mag/40.0)]
        if self.mag<0:
            self.yS = [1-(self.mag/200.0)]
            self.yE = [1]
        elif self.mag>0:
            self.yS = [-1-(self.mag/200.0)]
            self.yE = [-1]
        else:
            self.yS = [-5]
            self.yE = [-5]
            self.xS = [-5]
            self.xE = [-5]
        self.dy = Fun_Deflection(self.loc,l - self.loc, l, self.mag, np.linspace(self.x0,self.xf,self.resol), self.xf, self.resol, self.E, self.I)
        self.arrow_source.data = dict(xS= self.xS, xE= self.xE, yS= self.yS, yE=self.yE, lW = self.lW )





        '''
        def Fun_Update(attr,old,new):
            #1names = []
            #1rmag = 0
            #1rloc = 0
            #1rdy  = np.ones(beam.resol) * 0
            for i in range(0,number):
                flist[i].update_arrow(fb.loc_slider.value)         #update the concentrated loads
                rmag += flist[i].mag
                rloc += flist[i].loc
                rdy  = np.add(rdy,flist[i].dy)
                #names.append(flist[i].name)
            rloc = rloc / number
            a = rloc - beam.x0
            b = fb.loc - rloc
            beam.source.data['y'] = rdy

            if fb.loc_slider.value == 0: #cantilever
                Fun_Cantilever()
            else:
            #Update the support forces
                #1fa.mag = Fun_F(rmag,b,fb.loc_slider.value)
                #1fb.mag = Fun_F(rmag,a,fb.loc_slider.value)
                #1fa.update_arrow(fb.loc_slider.value)
                #1fb.update_arrow(fb.loc_slider.value)
                #1triangle_source.data = dict(x = [0.0,fb.loc], y = [0-move_tri, 0-move_tri], size = [20,20])
                #names = names + fa.name + fb.name
        '''


### SASCHA KUBISCH 14-01-2019:
   
# FUNCTION: Calculation of deflection:
def Fun_Deflection(a,b,l,p_mag,x):
    ynew = []
    for i in range(0,int(resol) ):
        dy = 0
        ynew.append(dy)
    return ynew    


   
    # if radio_button_group.active == 0:    
    #     ynew = []
    #     ynew1 = []
    #     ynew2 = []
    #     for i in range(0,int(l*(resol/10) ) ):
    #         if a > l:
    #             dy = ( ( p_mag * b * x[i]) / (6 * E * I * l) ) * ( (l**2) - (x[i]**2) )
    #         else:
    #             if x[i] < a:
    #                 dy = ( ( p_mag * b * x[i]) / (6 * E * I * l) ) * ( (l**2) - (b**2) - (x[i]**2) )
    #             elif x[i] == a:
    #                 dy = ( p_mag * (a**2) * (b**2) ) / (3 * E * I * l)
    #             elif x[i] > a and x[i] <= l:
    #                 dy = ( (p_mag * a * (l-x[i]) ) / (6 * E * I * l) ) * ( (2*l*x[i]) - (x[i]**2) - (a**2) )
    #         # dy = 0
    #         ynew1.append(dy)
    #     new_range = int(resol - l*10)
    #     for i in range(0,new_range):
    #         # dy1 = 0
    #         dy1 = -1 *( ( (p_mag * a * b * x[i]) / (6 * E * I * l) ) * (l + a) )
    #         ynew2.append(dy1)
    #     ynew = ynew1 + ynew2
    #     return ynew


    # if radio_button_group.active == 1:
    #     ynew = []
    #     for i in range(0,int(resol) ):
    #         if a > l:
    #             f1_mag = 1.0*p_mag*a/l*(l-a/2.0)
    #             f2_mag = p_mag*a-f1_mag
    #             #calculate phi(x1=0) and phi(x2=0):
    #             phi_x1_0 = 1.0/E/I*(f1_mag*l**2.0/6.0 - p_mag*l**3.0/24.0) 
    #             phi_x2_0 = 1.0/E/I*(p_mag*l**3.0/6.0-f1_mag*l**2.0/2.0+ E*I*phi_x1_0)
    #             phi_x3_0 = 1.0/E/I*(p_mag*a**3.0/6.0 - (f1_mag + f2_mag - p_mag *l)*a**2.0/2.0 - (f1_mag*l - p_mag*l**2.0/2.0)*a + E*I*phi_x2_0)
    #             if x[i]<l:
    #                 dy = 1.0/E/I * (p_mag*x[i]**4.0/24.0 - f1_mag*x[i]**3.0/6.0 + E*I*phi_x1_0*x[i])
    #             if x[i]>=l and x[i]<a:
    #                 dy= 1.0/E/I * (p_mag*(x[i]-l)**4.0/24.0 - (f1_mag + f2_mag - p_mag*l)*(x[i]-l)**3.0/6.0 - (f1_mag*l - p_mag*l**2.0/2.0)*(x[i]-l)**2.0/2.0 + E*I*(x[i]-l)*phi_x2_0 ) 
        #         if x[i]>=a:
        #             #approximate free end with simple linear funtion:
        #             if x[i-1]<a:
        #                 index=i
        #             dy = ((ynew[index-2]-ynew[index-1])/(x[index-2]-x[index-1]))*(x[i]-a) + ynew[index-1]     
        #   ### FIND SOLUTION BEGIN
        #     else:  #l>=a
        #         f1_mag = 1.0* p_mag*a/l*(l - a + a/2.0)
        #         f2_mag = p_mag*a-f1_mag
        #         #calculate phi(x1=0) and phi(x2=0):
        #         phi_x1_0 = -1.0/E/I/(l+a)* (p_mag*l**4.0/24.0 - (f1_mag - p_mag*a)*l**3.0/6.0 - (f1_mag*a - p_mag*a**2.0/2.0)*l**2.0/2.0 + l*(p_mag*a**3.0/6.0 - f1_mag*a**2.0/2.0) + p_mag*a**4.0/24.0 - f1_mag*a**3.0/6.0 ) 
        #         phi_x2_0 = 1.0/E/I * (p_mag*a**3.0/6.0 - f1_mag*a**2.0/2.0 + E*I*phi_x1_0)
        #         if x[i]<a:
        #             dy = 1.0/E/I * (p_mag*x[i]**4.0/24.0 - f1_mag*x[i]**3.0/6.0 + E*I*phi_x1_0*x[i])
        #         if x[i]>=a and x[i]<l:
        #             dy_x1_a= 1.0/E/I * (p_mag*a**4.0/24.0 - f1_mag*a**3.0/6.0 + E*I*phi_x1_0*a)
        #             dy= 1.0/E/I*(p_mag*(x[i]-a)**4.0/24.0 - (f1_mag + p_mag* a)*(x[i]-a)**3.0/6.0 - (f1_mag*a + (p_mag*a**2.0)/2.0)*(x[i]-a)**2.0/2.0 + E*I*phi_x2_0 + E*I*dy_x1_a )
        #         if x[i]>=l:
        #             ##approximate free end with simple linear funtion:
        #             if x[i-1]<l:
        #                 index=i
        #             dy = ((ynew[index-2]-ynew[index-1])/(x[index-2]-x[index-1]))*(x[i]-l) + ynew[index-1] 
        #    ### FIND SOLUTION END
        #     ynew.append(dy)
        # return ynew

    # if radio_button_group.active == 2:
        # ynew = []
        # print a
        # for i in range(0,int(resol) ):
            # dy = 0
        #     ynew.append(dy)
        # return ynew

        
# FUNCTION: Cantilever Deflection function:
def Fun_C_Deflection(p,b,x):
    '''Calculates the deflection of the beam when it is cantilever'''

    ynew = []
    for i in range(0,int(resol) ):
        dy = 0
        ynew.append(dy)
    return ynew  
    
    # #b is the distance from the wall to the concentrated load
    # if radio_button_group.active == 0:
    #     ynew = []
    #     a = xf - b;     #The a for cantilever is the distance between
    #                     #the free end and the concentrated load.
    #     for i in range(0,resol):
    #         if x[i] < a:
    #             #dy = (  ( p * ( ( xf - x[i])**2 ) ) / (6 * E * I) ) * ( (3*b) - xf + x[i] )
    #             dy = (  ( p * (b**2) ) / (6 * E * I)  ) * ( (3*xf) - (3*x[i]) - b )
    #         elif x[i] == a:
    #             dy = ( p * (b**3) ) / (3 * E * I)
    #         elif x[i] > a:
    #             #dy = (  ( p * (a**2) ) / (6 * E * I)  ) * ( (3*xf) - (3*x[i]) - a )
    #             dy = (  ( p * ( ( xf - x[i])**2 ) ) / (6 * E * I) ) * ( (3*b) - xf + x[i] )
    #         dy = 0 
    #         ynew.append(dy)

    #     return list(reversed(ynew))     #need to reverse because x is calculated in the opposite direction

    # if radio_button_group.active == 1:   
    #     ynew = []
    #     a = xf - b;     #The a for cantilever is the distance between
    #                 #the free end and the concentrated load.
    #     for i in range(0,resol):
            
    #         #UNCOMMENT FOR DEFLECTION
    #         # if x[i] < a:
    #         #     #dy = (  ( p * ( ( xf - x[i])**2 ) ) / (6 * E * I) ) * ( (3*b) - xf + x[i] )
    #         #     dy = (  ( p * (b**2) ) / (6 * E * I)  ) * ( (3*xf) - (3*x[i]) - b )
    #         # elif x[i] == a:
    #         #     dy = ( p * (b**3) ) / (3 * E * I)
    #         # elif x[i] > a:
    #         #     #dy = (  ( p * (a**2) ) / (6 * E * I)  ) * ( (3*xf) - (3*x[i]) - a )
    #         #     dy = (  ( p * ( ( xf - x[i])**2 ) ) / (6 * E * I) ) * ( (3*b) - xf + x[i] )

    #         dy = 0
    #         ynew.append(dy)

    #     return list(reversed(ynew))     #need to reverse because x is calculated in the opposite direction
 
    # if radio_button_group.active == 2:   
    #     ynew = []
    #     a = xf - b;     #The a for cantilever is the distance between
    #                 #the free end and the concentrated load.
    #     for i in range(0,resol):
    #         # if x[i] < a:
    #         #     #dy = (  ( p * ( ( xf - x[i])**2 ) ) / (6 * E * I) ) * ( (3*b) - xf + x[i] )
    #         #     dy = (  ( p * (b**2) ) / (6 * E * I)  ) * ( (3*xf) - (3*x[i]) - b )
    #         # elif x[i] == a:
    #         #     dy = ( p * (b**3) ) / (3 * E * I)
    #         # elif x[i] > a:
    #         #     #dy = (  ( p * (a**2) ) / (6 * E * I)  ) * ( (3*xf) - (3*x[i]) - a )
    #         #     dy = (  ( p * ( ( xf - x[i])**2 ) ) / (6 * E * I) ) * ( (3*b) - xf + x[i] )

    #         dy = 0
    #         ynew.append(dy)

    #     return list(reversed(ynew))     #need to reverse because x is calculated in the opposite direction


#######################
#CANTILEVER FUNCTIONS
#######################

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

def Fun_C_Deflection(p,b,x,resol,xf,E,I):
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





#########################
###     MAIN 1
#########################


#main file:
from bokeh.plotting import Figure, output_file , show
from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, Arrow
from bokeh.layouts import column, row, widgetbox
from bokeh.io import curdoc
from bokeh.models.widgets import Button, CheckboxGroup
import numpy as np
from classes import *

#initialization of objects
canti       = Cantilever()
norm        = Norm()
fa          = Support("A",0.0,0.0)                                                    #creation of support a.
fb          = Support("B",0.0,norm.xf)                                                    #creation of support b
f1          = Load("F1")                                                            #1st load
f2          = Load("F2")                                                            #2nd load
f3          = Load("F3")                                                            #3rd load
f4          = Load("F4")                                                            #4th load
f5          = Load("F5")                                                            #5th load on frame
resultant   = Force("Resultant",0.0,0.0)                                                           #creation of (theoretical) resultant load


def fun_f(p_mag,k,l):
    f_mag = -1.0 * (p_mag *k) / l
    return f_mag

def calc_resultant(f1,f2,f3,f4,f5):
    resultant.mag           = (f1.mag + f2.mag + f3.mag + f4.mag + f5.mag) / 5.0
    resultant.loc           = (f1.loc + f2.loc + f3.loc + f4.loc + f5.loc) / 5.0
    #print f1.deflection
    print "f1 %r, f2 %r , f3 %r , f4 %r , f5 %r" %(len(f1.deflection),len(f2.deflection),len(f3.deflection),len(f4.deflection),len(f5.deflection))
    resultant.deflection    = ( np.asarray(f1.deflection) + np.asarray(f2.deflection)
            + np.asarray(f3.deflection) + np.asarray(f4.deflection)
            + np.asarray(f5.deflection) )

def update_supports():
    a = resultant.loc
    b = fb.loc - a
    fa.mag = fun_f(resultant.mag,b,fb.loc)
    fb.mag = fun_f(resultant.mag,a,fb.loc)
    fa.update_arrow()
    fb.update_arrow()

def fun_update(attr,old,new):
    f1.update_arrow()
    f2.update_arrow()
    f3.update_arrow()
    f4.update_arrow()
    f5.update_arrow()
    print "length of fb arrow_source %r" %(len(fb.arrow_source.data))
    print "canti length %r , %r " %( len(canti.source.data['x']),len(canti.source.data['y']) )
    print "norm length %r , %r " %( len(norm.source.data['x']),len(norm.source.data['y']) )


    if fb.loc == 0:
        fun_cantilever()
    elif fb.loc != 0:
        fun_normal()

    update_supports()

def fun_normal():
    canti.clear_beam()
    canti.clear_box()
    f1.deflection = norm.fun_deflection(f1.loc, fb.loc, f1.mag)
    f2.deflection = norm.fun_deflection(f2.loc, fb.loc, f2.mag)
    f3.deflection = norm.fun_deflection(f3.loc, fb.loc, f3.mag)
    f4.deflection = norm.fun_deflection(f4.loc, fb.loc, f4.mag)
    f5.deflection = norm.fun_deflection(f5.loc, fb.loc, f5.mag)
    calc_resultant(f1,f2,f3,f4,f5)
    norm.source.data['y'] = resultant.deflection
    #print resultant.deflection
    #print fb.loc

def fun_cantilever():
    norm.clear_beam()
    fa.fun_clear()
    fb.fun_clear()
    canti.create_box()
    f1.deflection = canti.fun_deflection(f1.loc, f1.mag)
    f2.deflection = canti.fun_deflection(f2.loc, f2.mag)
    f3.deflection = canti.fun_deflection(f3.loc, f3.mag)
    f4.deflection = canti.fun_deflection(f4.loc, f4.mag)
    f5.deflection = canti.fun_deflection(f5.loc, f5.mag)
    calc_resultant(f1,f2,f3,f4,f5)
    canti.source.data['y'] = resultant.deflection

print "hi"
#print canti.source.data


###Main Plot:
plot = Figure(title="Doppeltgelagerter Balken und Einzellast", x_range=(0-.1,1+.1), y_range=(-1,1))
plot.line(x='x', y='y', source=norm.source, color='#0065BD',line_width=20)
plot.line(x='x', y='y', source=canti.source, color='#0065BD',line_width=20)
#plot.line(x = [1 ,2, 3] , y = [1 ,2, 3])
#plot.line(x='x', y='y', source=norm.source, color='#0065BD',line_width=20)
plot.triangle(x='x', y='y', size = 'size', source= fb.triangle_source,color="#E37222", line_width=2)
plot.triangle(x='x', y='y', size = 'size', source= fa.triangle_source,color="#E37222", line_width=2)
plot.quad(top='top', bottom='bottom', left='left',
    right='right', source = canti.quad_source, color="#808080", fill_alpha = 0.5)
plot.segment(x0='x0', y0='y0', x1='x1',
          y1='y1', source = canti.segment_source, color="#F4A582", line_width=2)

plot.axis.visible = False
plot.outline_line_width = 7
plot.outline_line_alpha = 0.3
plot.outline_line_color = "Black"
#labels = LabelSet(x='x', y='y', text='name', level='glyph',
#              x_offset=5, y_offset=-30, source=labels_source, render_mode='canvas')
###Plot with moment and shear:
'''
y_range0 = -600
y_range1 = -y_range0
plot1 = Figure(title="Biegemoment, Querkraft", x_range=(x0,xf), y_range=(y_range0,y_range1), width = 400, height = 200)
plot1.line(x='x', y='y', source=mom_source, color='blue',line_width=5)
plot1.line(x='x', y='y', source=shear_source, color='red',line_width=5)
plot1.line(x= [x0-1,xf+1], y = [0, 0 ], color = 'black', line_width =2 ,line_alpha = 0.4, line_dash=[1])
plot1.line(x= [xf/2,xf/2], y = [y_range0,y_range1], color = 'black', line_width =2 ,line_alpha = 0.4, line_dash=[1])
plot1.axis.visible = False
'''
###arrow plotting:
#P arrow:'''
f1_arrow_glyph = Arrow(end=OpenHead(line_color="#A2AD00",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', source=f1.arrow_source,line_color="#A2AD00")

f2_arrow_glyph = Arrow(end=OpenHead(line_color="#A2AD00",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', source=f2.arrow_source,line_color="#A2AD00")
f3_arrow_glyph = Arrow(end=OpenHead(line_color="#A2AD00",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', source=f3.arrow_source,line_color="#A2AD00")

f4_arrow_glyph = Arrow(end=OpenHead(line_color="#A2AD00",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', source=f4.arrow_source,line_color="#A2AD00")

f5_arrow_glyph = Arrow(end=OpenHead(line_color="#A2AD00",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', source=f5.arrow_source,line_color="#A2AD00")
fb_arrow_glyph = Arrow(end=OpenHead(line_color="#003359",line_width= 4,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', source=fa.arrow_source,line_color="#003359")
#Position 1 arrow:
fa_arrow_glyph = Arrow(end=OpenHead(line_color="#003359",line_width= 4,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', source=fb.arrow_source,line_color="#003359" )

###add layouts:
#plot.add_layout(labels)
plot.add_layout(f1_arrow_glyph)
plot.add_layout(f2_arrow_glyph)
plot.add_layout(f3_arrow_glyph)
plot.add_layout(f4_arrow_glyph)
plot.add_layout(f5_arrow_glyph)

plot.add_layout(fa_arrow_glyph)
plot.add_layout(fb_arrow_glyph)

###Reset Button
#button = Button(label="Reset", button_type="success")

###CheckboxGroup
#Biegelinie Checkbox
#checkbox = CheckboxGroup(
#        labels=["Biegelinie", "Mit Schub (Biegelinie muss auch markiert sein!)"], active=[])


###on_change:
f1.loc_slider.on_change('value', fun_update)
f2.loc_slider.on_change('value', fun_update)
f3.loc_slider.on_change('value', fun_update)
f4.loc_slider.on_change('value', fun_update)
f5.loc_slider.on_change('value', fun_update)

f1.mag_slider.on_change('value', fun_update)
f2.mag_slider.on_change('value', fun_update)
f3.mag_slider.on_change('value', fun_update)
f4.mag_slider.on_change('value', fun_update)
f5.mag_slider.on_change('value', fun_update)

fb.loc_slider.on_change('value', fun_update)

#lth_slide.on_change('value',Fun_Update)
#checkbox.on_change('active',Fun_Update)
#button.on_click(initial)

#main:
#initial()
'''
#triangle_source.data = dict(x = [0.0,fb.loc], y = [0-move_tri, 0-move_tri], size = [20,20])

plot = Figure(title="", x_range=(beam.x0-.5,beam.xf+.5), y_range=(-2.5,2.5))
my_line=plot.line(x='x', y='y', source=beam.source, color='#0065BD',line_width=20)
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

for i in range(0,number):
    plot.add_layout(flist[i].arrow_glyph)
plot.add_layout(fa.arrow_glyph)
plot.add_layout(fb.arrow_glyph)

force.loc_slider.on_change('value', Fun_Update)
force.mag_slider.on_change('value', Fun_Update)
fb.loc_slider.on_change('value', Fun_Update)
#f2_loc_slide.on_change('value',Fun_Update)
#lth_slide.on_change('value',Fun_Update)





vals1 = []
vals2 = []
vals3 = []
for i in range(0,number):
    vals1 = flist[i].loc_slider
    vals2 = flist[i].mag_slider
    vals3.append(vals1)

column1 = [flist[0].loc_slider,flist[0].mag_slider,flist[1].loc_slider,flist[1].mag_slider,
    fb.loc_slider]

curdoc().add_root( row( column(column1),  column(plot) ) )
'''
#curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '



#f1.mag_slider,f2.mag_slider,fb.mag_slider,f1.loc_slider,f2.loc_slider,fb.loc_slider),

curdoc().add_root( column(plot,fb.loc_slider,f1.loc_slider,f2.loc_slider,f3.loc_slider,f4.loc_slider,f5.loc_slider,f1.mag_slider,f2.mag_slider,f3.mag_slider,f4.mag_slider,f5.mag_slider))



############################
##  DEFLECTION FUNCTIONS 
############################
#deflection function:

def Fun_Deflection(a,b,l,p,x,xf,resol,E,I):
    ynew = []
    ynew1 = []
    ynew2 = []

    if (l == 0):
        ynew = []
        a = xf - a;     #The a for cantilever is the distance between
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
            ynew = list(reversed(ynew))

    else:

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



####################################
####   CLASSES #####################
####################################


from bokeh.plotting import Figure, output_file , show
from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, Arrow
from bokeh.layouts import column, row, widgetbox
from bokeh.io import curdoc
from bokeh.models.widgets import Button, CheckboxGroup
import numpy as np
from deflection_funs import Fun_Deflection



#Concentrated Force class
class Beam(object):
    def __init__(self):
        self.resol              = 100
        self.x0                 = 0                                             #starting value of Beam
        self.xf                 = 1                  #ending value of Beam
        self.E                  = 1            #modulus of elasticity
        self.I                  = 1                 #moment of inertia
        self.length             = self.xf-self.x0         #length of Beam
        self.lthi               = 2
        self.lth                = self.lthi
        #self.plotwidth          = 20
        self.source             = ColumnDataSource(data=dict(x = np.linspace(self.x0,self.xf,self.resol), y = np.ones(self.resol) * 0 ))

    def clear_beam(self):
        self.source.data        = dict(x = [], y = [])


class Cantilever(Beam):
    def __init__(self):
        Beam.__init__(self)
        self.quad_source        = ColumnDataSource(data=dict(top= [], bottom= [],left = [], right =[]))
        self.segment_source     = ColumnDataSource(data=dict(x0= [], y0= [],x1 = [], y1 =[]))
        self.labels_source      = ColumnDataSource(data=dict(x=[] , y=[],name = []))

    def create_box(self):
        self.quad_source.data   = dict(top = [0.2], bottom = [-0.2], left = [-0.1] , right = [0])
        self.segment_source.data= dict(x0= np.ones(40) * -0.1,
            y0= np.linspace(-0.2,0.2-0.02,40),x1 = np.ones(40) * 0,
            y1 =np.linspace(-0.2+0.02,0.2,40))

    def clear_box(self):
        self.quad_source.data   = dict(top = [], bottom = [], left = [] , right = [])
        self.segment_source.data= dict(x0= [], y0= [],x1 = [], y1 =[])

    def fun_deflection(self,b,p):
        '''Calculates the deflection of the beam when it is cantilever'''
        #b is the distance from the wall to the concentrated load
        x = self.source.data['x']
        ynew = []
        xf = self.xf
        a = xf - b;     #The a for cantilever is the distance between
                        #the free end and the concentrated load.
        for i in range(0,self.resol):
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

class Norm(Beam):
    def __init__(self):
        Beam.__init__(self)

    def fun_deflection(self,a,l,p):
        print "l %r" %l
        b       = l - a
        xf      = self.xf
        resol   = self.resol
        E       = self.E
        I       = self.I
        x       = np.linspace(self.x0,self.xf,self.resol)
        ynew1   = []
        ynew2   = []
        ynew    = []
        for i in range(0,int(l*resol) ):
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

        new_range = int(resol - l*100)
        for i in range(0,new_range):
            dy1 = -1 *( ( (p * a * b * x[i]) / (6 * E * I * l) ) * (l + a) )
            ynew2.append(dy1)
        ynew = ynew1 + ynew2
        return ynew



'''
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
'''

class Force(object):
    def __init__(self,name,magi,loci):
        self.name = name
        self.mag = magi
        self.loc = loci
        self.magi = magi
        self.loci = loci
        self.arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[]))
        self.mag_slider = Slider(title=self.name + " amplitude", value=self.magi, start=-1, end=1, step=0.01)

class Load(Force):
    def __init__(self,name):
        Force.__init__(self,name,0.0,0.5)
        self.deflection = np.array([])
        self.loc_slider = Slider(title=self.name + " Position",value = 1.0,
                    start = 0.0, end = 1.0, step = 0.01)

    def update_arrow(self):
        self.loc = self.loc_slider.value
        self.mag = self.mag_slider.value
        if self.mag == 0:
            self.arrow_source.data = dict (xS= [], xE= [], yS= [], yE= [])
        elif self.mag != 0:
            self.arrow_source.data = dict (xS= [self.loc], xE= [self.loc],
                yS= [(self.mag/abs(self.mag)) * (1 - self.mag)],
                yE= [(self.mag/abs(self.mag)) * 1] )
        #self.dy = Fun_Deflection(self.loc, l, self.mag, self.resol, self.E, self.I)


    def Fun_Deflection(self,a,b,l,p,x,xf,resol,E,I):
        ynew = []
        ynew1 = []
        ynew2 = []

        if (l == 0):
            ynew = []
            a = xf - a;     #The a for cantilever is the distance between
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
                ynew = list(reversed(ynew))

        else:

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

class Support(Force):
    def __init__(self,name,magi,loci):
        Force.__init__(self,name,magi,loci)
        self.triangle_source = ColumnDataSource(data=dict(x= [], y= [], size = []))
        self.move_tri        = 0.25
        self.loc_slider = Slider(title=self.name + " Position",value = 1.0,
            start = 0.0, end = 1.0, step = 0.01)
    def fun_clear(self):
        self.triangle_source.data = dict(x = [], y = [], size = [])
        self.arrow_source.data = dict(xS= [], xE= [], yS= [], yE=[])

    def update_arrow(self):
        if self.name == "A":
            self.loc = 0
        elif self.name == "B":
            self.loc = self.loc_slider.value

        if self.mag == 0:
            self.arrow_source.data = dict (xS= [], xE= [], yS= [], yE= [])
        elif self.mag != 0:
            self.arrow_source.data = dict (xS= [self.loc], xE= [self.loc],
                yS= [(self.mag/abs(self.mag)) * (1 - self.mag)],
                yE= [(self.mag/abs(self.mag)) * 1])
        #self.dy = Fun_Deflection(self.loc,l - self.loc, l, self.mag, np.linspace(self.x0,self.xf,self.resol), self.xf, self.resol, self.E, self.I)
        #self.arrow_source.data = dict(xS= self.xS, xE= self.xE, yS= self.yS, yE=self.yE, lW = self.lW )
        self.triangle_source.data = dict(x = [self.loc], y = [0-self.move_tri], size = [20])


