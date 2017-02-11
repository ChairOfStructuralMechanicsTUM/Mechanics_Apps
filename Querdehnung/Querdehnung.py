from __future__ import division
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Slider, LabelSet
from bokeh.layouts import column, row
from bokeh.io import curdoc

E_inv = 1e-2
nu = 0.5

Updatables=[]
Circular_Updatables=[]

class DeformableObj(object):
    def __init__(self,XL_0,YL_0):
        # store original width and height
        self.XL_0 = XL_0
        self.YL_0 = YL_0
        self.X = XL_0
        self.Y = YL_0
        self.CX = 0
        self.CY = 0
        self.orig_babies=[]
        self.orig_Cbabies=[]
        self.nb_babies=0
        self.nb_Cbabies=0
    
    def deform_coord(self,old,centre,eps):
        return old+(old-centre)*eps
    
    def new_coord(self,old,eps):
        new_vals = [ [], [] ]
        for i in range(0,len(old['x'])):
            new_vals[0].append(self.deform_coord(old['x'][i],self.CX,eps[0]))
            new_vals[1].append(self.deform_coord(old['y'][i],self.CY,eps[1]))
        return new_vals
    
    def deform(self,Force):
        global E_inv, nu, Updatables, Circular_Updatables
        sig = [Force[0]/self.Y, Force[1]/self.X]
        eps = [E_inv*sig[0]-nu*E_inv*sig[1], E_inv*sig[1]-nu*E_inv*sig[0]]
        for j in range(0,self.nb_babies):
            new_vals = self.new_coord(self.orig_babies[j],eps)
            Updatables[j].data = dict(x=new_vals[0], y=new_vals[1])
        for j in range(0,self.nb_Cbabies):
            old=self.orig_Cbabies[j];
            new_x0=self.deform_coord(old[0],self.CX,eps[0])
            new_y0=self.deform_coord(old[2],self.CY,eps[1])
            new_width=abs(self.deform_coord(old[0]+old[1]/2.0,self.CX,eps[0])-self.deform_coord(old[0]-old[1]/2.0,self.CX,eps[0]))
            new_height=abs(self.deform_coord(old[2]+old[3]/2.0,self.CY,eps[1])-self.deform_coord(old[2]-old[3]/2.0,self.CY,eps[1]))
            Circular_Updatables[j].data=dict(x=[new_x0],y=[new_y0],w=[new_width], h=[new_height])
        self.X=self.XL_0*(1+eps[0])
        self.Y=self.YL_0*(1+eps[1])
    
    def add_baby(self,shape_x,shape_y):
        global Updatables
        self.orig_babies.append(dict(x=shape_x,y=shape_y))
        Updatables.append(ColumnDataSource(data=dict(x=shape_x, y=shape_y)))
        self.nb_babies+=1
        return self.nb_babies-1
    
    def add_circular_baby(self,x_0, y_0, width, height):
        global Circular_Updatables
        self.orig_Cbabies.append([x_0,width,y_0,height])
        Circular_Updatables.append(ColumnDataSource(data=dict(x=[x_0],y=[y_0],w=[width], h=[height])))
        self.nb_Cbabies+=1
        return self.nb_Cbabies-1
        

def change_FX(attrname, old, new):
    global Block
    global Block, ForceY_input
    Block.deform([new, ForceY_input.value])
    
def change_FY(attrname, old, new):
    global Block
    global Block, ForceX_input
    Block.deform([ForceX_input.value, new])

def change_nu(attrname, old, new):
    global nu, Block, ForceX_input, ForceY_input
    nu=new
    Block.deform([ForceX_input.value, ForceY_input.value])

def change_E(attrname, old, new):
    global E_inv, Block, ForceX_input, ForceY_input
    E_inv=1.0/float(new)
    Block.deform([ForceX_input.value, ForceY_input.value])

## Create slider to choose force applied to x axis
ForceX_input = Slider(title="Kraft-x (Force-x)", value=0.0, start=0.0, end=200.0, step=5)
ForceX_input.on_change('value',change_FX)

## Create slider to choose force applied to y axis
ForceY_input = Slider(title="Kraft-y (Force-y)", value=0.0, start=0.0, end=200.0, step=5)
ForceY_input.on_change('value',change_FY)

## Create slider to choose nu applied
Nu_input = Slider(title="Nu", value=0.5, start=0.0, end=1.0, step=0.1)
Nu_input.on_change('value',change_nu)

## Create slider to choose Young's modulus
E_input = Slider(title=u"Elastizit\u00E4tsmodul (Young's Modulus)", value=100.0, start=100.0, end=1000.0, step=100)
E_input.on_change('value',change_E)

Block = DeformableObj(10,5)
diagram = figure(title="Querdehnung (Transverse Strain)", tools="", x_range=(-10,10), y_range=(-10,10))
diagram.patch([-5,5,5,-5],[-2.5,-2.5,2.5,2.5], fill_color="blue")
Block.add_baby([-5,5,5,-5],[-2.5,-2.5,2.5,2.5])
diagram.patch(x='x',y='y',source=Updatables[0], fill_color="red")
Block.add_baby([-4,-1,-1,-4],[-1,-1,1,1])
diagram.patch(x='x',y='y',source=Updatables[1], fill_color="black")
Block.add_baby([3.5,4,3.5,3],[-0.5,0,0.5,0])
diagram.patch(x='x',y='y',source=Updatables[2], fill_color="black")
Block.add_circular_baby(1,0,1.5,1.5)
diagram.ellipse(x='x',y='y',width='w',height='h',source=Circular_Updatables[0], fill_color="black")

## Send to window
curdoc().add_root(row(column(ForceX_input,ForceY_input,E_input,Nu_input),diagram))
