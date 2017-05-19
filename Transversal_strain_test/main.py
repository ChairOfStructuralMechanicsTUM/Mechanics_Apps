from __future__ import division
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Slider, LabelSet, Arrow, OpenHead
from bokeh.layouts import column, row
from bokeh.io import curdoc
from os.path import dirname, join, split

E_inv = 1e-2
nu = 0.5

Updatables=[]
Circular_Updatables=[]
Force_Updatables=[]
Force_label_Updatables=[]

class DeformableObj(object):
    def __init__(self,XL_0,YL_0):
        # store original width and height
        self.XL_0 = XL_0
        self.YL_0 = YL_0
        # store current width and height
        self.X = XL_0
        self.Y=YL_0
        # store centre co-ordinates
        self.CX = 0
        self.CY = 0
        # create arrays for storing original positions of objects
        self.orig_babies=[]
        self.orig_Cbabies=[]
        self.orig_forces=[]
        self.force_label_arrows=[]
        # store array size
        self.nb_babies=0
        self.nb_Cbabies=0
        self.nb_force_objs=0
        self.nb_force_labels=0
    
    # calculate deformed co-ordinate in an arbitrary direction
    def deform_coord(self,old,centre,eps):
        return old+(old-centre)*eps
    
    # calculate all deformed co-ordinates for a given (non-circular) shape
    def new_coord(self,old,eps):
        new_vals = [ [], [] ]
        for i in range(0,len(old['x'])):
            new_vals[0].append(self.deform_coord(old['x'][i],self.CX,eps[0]))
            new_vals[1].append(self.deform_coord(old['y'][i],self.CY,eps[1]))
        return new_vals
    
    # function called by slider functions which deforms the object
    def deform(self,Force):
        global E_inv, nu, Updatables, Circular_Updatables
        # update physical constants
        sig = [Force[0]/self.Y, Force[1]/self.X]
        eps = [E_inv*sig[0]-nu*E_inv*sig[1], E_inv*sig[1]-nu*E_inv*sig[0]]
        # deform all non-circular objects
        for j in range(0,self.nb_babies):
            new_vals = self.new_coord(self.orig_babies[j],eps)
            Updatables[j].data = dict(x=new_vals[0], y=new_vals[1])
        # deform all circular objects
        for j in range(0,self.nb_Cbabies):
            old=self.orig_Cbabies[j];
            new_x0=self.deform_coord(old[0],self.CX,eps[0])
            new_y0=self.deform_coord(old[2],self.CY,eps[1])
            new_width=abs(self.deform_coord(old[0]+old[1]*0.5,self.CX,eps[0])-self.deform_coord(old[0]-old[1]*0.5,self.CX,eps[0]))
            new_height=abs(self.deform_coord(old[2]+old[3]*0.5,self.CY,eps[1])-self.deform_coord(old[2]-old[3]*0.5,self.CY,eps[1]))
            Circular_Updatables[j].data=dict(x=[new_x0],y=[new_y0],w=[new_width], h=[new_height])
        # deform main object (not plotted but important for S when calculating sigma)
        self.X=self.XL_0*(1+eps[0])
        self.Y=self.YL_0*(1+eps[1])
        # deform force arrows
        for j in range(0,self.nb_force_objs):
            if (self.orig_forces[j][1]=='yE'):
                # get original length
                length=self.orig_forces[j][0]['yE'][0]-self.orig_forces[j][0]['yS'][0]
                # keep start position relative to main object
                newY0=self.orig_forces[j][0]['yS'][0]*(1+eps[1])
                # alter arrow length by a factor of (1+F/200) 
                Force_Updatables[j].data=dict(xS=Force_Updatables[j].data['xS'],xE=Force_Updatables[j].data['xE'],
                    yS=[newY0], yE=[newY0+(1+Force[1]*0.005)*length])
            else:
                # get original length
                length=self.orig_forces[j][0]['xE'][0]-self.orig_forces[j][0]['xS'][0]
                # keep start position relative to main object
                newX0=self.orig_forces[j][0]['xS'][0]*(1+eps[0])
                # alter arrow length by a factor of (1+F/200) 
                Force_Updatables[j].data=dict(xS=[newX0],xE=[newX0+(1+Force[0]*0.005)*length],
                    yS=Force_Updatables[j].data['yS'], yE=Force_Updatables[j].data['yE'])
        
        # deform force labels
        for j in range(0,self.nb_force_labels,2):
            # to be placed at the end of the linked arrow
            linked_arrow=Force_Updatables[self.force_label_arrows[int(j/2)]['i']].data;
            n=len(linked_arrow['xE'])
            if (self.force_label_arrows[int(j/2)]['xy']=='y'):
                # if x fixed, keep x
                X=Force_label_Updatables[j].data['x']
                # move by 1 from end in correct direction
                if (linked_arrow['yE'][n-2]>0):
                    Y=[linked_arrow['yE'][n-2]+1]
                else:
                    Y=[linked_arrow['yE'][n-2]-1]
            else:
                # if y fixed, keep y
                Y=Force_label_Updatables[j].data['y']
                # move by 1 from end in correct direction
                if (linked_arrow['xE'][n-2]>0):
                    X=[linked_arrow['xE'][n-2]+1]
                else:
                    X=[linked_arrow['xE'][n-2]-1]
            Force_label_Updatables[j].data=dict(x=X, y=Y,f=['F'])
            # update subscript
            Force_label_Updatables[j+1].data=dict(x=[X[0]+0.2], y=[Y[0]-0.2],f=Force_label_Updatables[j+1].data['f'])
    
    # add non-circular object to Deformable object
    def add_baby(self,shape_x,shape_y,diagram,colour):
        global Updatables
        # store original position
        self.orig_babies.append(dict(x=shape_x,y=shape_y))
        # create ColumnDataSource
        Updatables.append(ColumnDataSource(data=dict(x=shape_x, y=shape_y)))
        # add to diagram
        diagram.patch(x='x',y='y',source=Updatables[self.nb_babies], fill_color=colour,line_color=colour)
        # update number of objects
        self.nb_babies+=1
    
    # add circular object to Deformable object
    def add_circular_baby(self,x_0, y_0, width, height,diagram,colour):
        global Circular_Updatables
        # store original position
        self.orig_Cbabies.append([x_0,width,y_0,height])
        # create ColumnDataSource
        Circular_Updatables.append(ColumnDataSource(data=dict(x=[x_0],y=[y_0],w=[width], h=[height])))
        # add to diagram
        diagram.ellipse(x='x',y='y',width='w',height='h',source=Circular_Updatables[self.nb_Cbabies], 
            fill_color=colour,line_color=colour)
        # update number of objects
        self.nb_Cbabies+=1
    
    # draws all 4 arrows on one side at once
    def add_force_arrows(self,xStart,yStart,length,xy,diagram):
        global Force_Updatables
        # create ColumnDataSources
        if (xy=='yE'):
            n=len(xStart)
        else:
            n=len(yStart)
        if (xy=='xE'):
            # if x variable then xStart[i]=xStart[i+1]
            # and yEnd always equals yStart
            xEnd=xStart+length
        else:
            # if y variable then yStart[i]=yStart[i+1]
            # and xEnd always equals xStart
            yEnd=yStart+length
        c=self.nb_force_objs
        for i in range(0,n):
            # create ColumnDataSource
            if (xy=='xE'):
                # if x variable then xStart[i]=xStart[i+1]
                Force_Updatables.append(ColumnDataSource(data=dict(xS=[xStart],xE=[xEnd],yS=[yStart[i]],yE=[yStart[i]])))
            else:
                # if y variable then yStart[i]=yStart[i+1]
                Force_Updatables.append(ColumnDataSource(data=dict(xS=[xStart[i]],xE=[xStart[i]],yS=[yStart],yE=[yEnd])))
            # add to diagram
            arrow_glyph = Arrow(end=OpenHead(line_color="black",line_width=3,size=10),
                x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=Force_Updatables[c+i],
                line_color="black",line_width=3)
            diagram.add_layout(arrow_glyph)
            # store original position and fixed direction
            self.orig_forces.append([dict(Force_Updatables[c+i].data), xy])
        # update number of objects
        self.nb_force_objs+=n
    
    def add_force_label(self,x,y,xy,diagram):
        global Force_Updatables
        # create ColumnDataSource
        Force_label_Updatables.append(ColumnDataSource(data=dict(x=[x], y=[y],f=['F'])))
        Force_label_Updatables.append(ColumnDataSource(data=dict(x=[x+0.2], y=[y-0.2],f=[xy])))
        # store associated arrow and fixed direction
        # associated arrow is at position self.nb_force_labels*2 as
        # there are 4 arrows and 2 force_labels
        self.force_label_arrows.append(dict(i=self.nb_force_labels*2,xy=xy))
        # add to diagram
        F_glyph=LabelSet(x='x', y='y',text='f',text_color='black',text_font_size="15pt",
            level='glyph',text_baseline="middle",text_align="center",source=Force_label_Updatables[self.nb_force_labels])
        diagram.add_layout(F_glyph)
        # add subscript to diagram
        F_glyph=LabelSet(x='x', y='y',text='f',text_color='black',text_font_size="10pt",
            level='glyph',text_baseline="middle",text_align="center",source=Force_label_Updatables[self.nb_force_labels+1])
        diagram.add_layout(F_glyph)
        # update number of labels
        self.nb_force_labels+=2
        
## Slider call functions
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
ForceX_input = Slider(title="Kraft-x (Force-x) [N]", value=0.0, start=0.0, end=125.0, step=5,width=350)
ForceX_input.on_change('value',change_FX)

## Create slider to choose force applied to y axis
ForceY_input = Slider(title="Kraft-y (Force-y) [N]", value=0.0, start=0.0, end=125.0, step=5,width=350)
ForceY_input.on_change('value',change_FY)

## Create slider to choose nu applied
Nu_input = Slider(title="Nu", value=0.5, start=0.0, end=1.0, step=0.1,width=350)
Nu_input.on_change('value',change_nu)

## Create slider to choose Young's modulus
E_input = Slider(title=u"Elastizit\u00E4tsmodul (Young's Modulus) [N/m\u00B2]",
    value=100.0, start=100.0, end=1000.0, step=100,width=350)
E_input.on_change('value',change_E)

## Create Deformable Object
Block = DeformableObj(10,5)
## Create drawing
diagram = figure(title="Querdehnung (Transverse Strain)", tools="", x_range=(-11,11), y_range=(-11,11))
diagram.title.text_font_size="20pt"
diagram.xaxis.major_label_text_font_size="12pt"
diagram.yaxis.major_label_text_font_size="12pt"
diagram.xaxis.axis_label_text_font_style="normal"
diagram.yaxis.axis_label_text_font_style="normal"
diagram.xaxis.axis_label_text_font_size="14pt"
diagram.yaxis.axis_label_text_font_size="14pt"
diagram.xaxis.axis_label="x"
diagram.yaxis.axis_label="y"
diagram.xaxis.major_tick_line_color=None
diagram.xaxis.major_label_text_color=None
diagram.xaxis.minor_tick_line_color=None
diagram.yaxis.major_tick_line_color=None
diagram.yaxis.major_label_text_color=None
diagram.yaxis.minor_tick_line_color=None
## add objects to figure and Deformable object
diagram.patch([-5,5,5,-5],[-2.5,-2.5,2.5,2.5], fill_color="#003359",line_color=None)
Block.add_baby([-5,5,5,-5],[-2.5,-2.5,2.5,2.5],diagram,"#0065BD")
Block.add_baby([-4,-1,-1,-4],[-1,-1,1,1],diagram,"#333333")
Block.add_baby([3.25,4.25,3.25,2.25],[-1,0,1,0],diagram,"#333333")
Block.add_circular_baby(1,0,1.5,1.5,diagram,"#333333")
## add horizontal force arrows
Block.add_force_arrows(4.75,[1.4,0.5,-0.5,-1.4],2,'xE',diagram)
Block.add_force_arrows(-4.75,[1.4,0.5,-0.5,-1.4],-2,'xE',diagram)
## add vertical force arrows
Block.add_force_arrows([3,1,-1,-3],2.25,2,'yE',diagram)
Block.add_force_arrows([3,1,-1,-3],-2.25,-2,'yE',diagram)
## add force labels (must be done in same order as arrows and after arrows)
Block.add_force_label(8,0,'x',diagram)
Block.add_force_label(-8,0,'x',diagram)
Block.add_force_label(0,5.5,'y',diagram)
Block.add_force_label(0,-5.5,'y',diagram)

## Send to window
curdoc().add_root(row(column(ForceX_input,ForceY_input,E_input,Nu_input),diagram))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
