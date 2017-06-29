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
