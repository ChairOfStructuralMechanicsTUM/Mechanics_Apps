# general imports

# bokeh imports
from bokeh.plotting import figure
from bokeh.models   import ColumnDataSource, Arrow, OpenHead, LabelSet

# internal imports
from SD_Shape import SD_Shape

# latex integration

#---------------------------------------------------------------------#

# class that handles the drawing of the car and house

class SD_Visualisation:
    def __init__ (self):
        # save original shape of car in a shape (to make displacement easy)
        self.carshape = SD_Shape([-3,0,0,-0.05,-0.5,-1,-2,-2,-3],[0.25,0.25,0.7,0.75,0.75,1.25,1.25,0.75,0.75])
        # create column data sources for the car and its acceleration
        self.car = ColumnDataSource(data=dict(x=self.carshape.x,y=self.carshape.y))
        self.wheels = ColumnDataSource(data=dict(x=[-2.25,-0.75],y=[0.25,0.25],w=[0.5,0.5],h=[0.5,0.5]))
        self.arrow = ColumnDataSource(data=dict(xS=[],yS=[],xE=[],yE=[]))
        self.v_label = ColumnDataSource(data=dict(x=[],y=[],S=[]))
        # create the figure
        self.fig = figure(tools="",x_range=(-4,31),y_range=(0,4),height=100)
        #  remove graph lines
        self.fig.yaxis.visible = False
        self.fig.grid.visible = False
        self.fig.toolbar.logo = None
        self.fig.outline_line_color = None
        # draw the house
        self.fig.line([30.0,30.0,29.5,30.5],[0,3.0,3.0,4.0],line_color="black",line_width=4)
        # add the car chassis to the image
        self.fig.patch(x='x',y='y',color="#0065BD",source=self.car)
        # add the car wheels to the image
        self.fig.ellipse(x='x',y='y',width='w',height='h',source=self.wheels, color="#0065BD")
        # create and add the arrow representing the velocity to the diagram
        arrow_glyph = Arrow(end=OpenHead(line_color="#003359",line_width=2,size=10),
            x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=self.arrow,line_color="#003359",line_width=2)
        self.fig.add_layout(arrow_glyph)
        # create the label for the velocity and add it to the diagram
        v_glyph=LabelSet(x='x', y='y',text='S',text_color='#003359',level='glyph',source=self.v_label)
        self.fig.add_layout(v_glyph)
    
    def setV(self,v_0):
        # modify the arrow so its length is proportional to the velocity
        self.arrow.stream(dict(xS=[0],yS=[0.5], xE=[v_0], yE=[0.5]),rollover=1)
        # move the velocity label to the middle of the arrow
        self.v_label.data = dict(x=[v_0/2.0],y=[0.5],S=[u"v\u2092"])
    
    def move(self,x,v):
        # move the car chassis to its new position
        temp=self.carshape+(x,0)
        self.car.data=dict(x=temp.x,y=temp.y)
        # move the wheels to their new position
        temp=dict(self.wheels.data)
        temp['x']=[x-2.25,x-0.75]
        self.wheels.data=temp
        # modify the arrow so its length is proportional to the velocity
        self.arrow.stream(dict(xS=[x],yS=[0.5], xE=[v+x], yE=[0.5]),rollover=1)
        if (x==0):
            # move the velocity label to the middle of the arrow
            self.v_label.data = dict(x=[x+v/2.0],y=[0.5],S=[u"v\u2092"])
        else:
            # move the velocity label to the middle of the arrow
            self.v_label.data = dict(x=[x+v/2.0],y=[0.5],S=["v"])
