from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Arrow, OpenHead, LabelSet
from Shape import *

class Visualisation:
    def __init__ (self):
        self.carshape = Shape([-3,0,0,-0.05,-0.5,-1,-2,-2,-3],[0.25,0.25,0.7,0.75,0.75,1.25,1.25,0.75,0.75])
        self.car = ColumnDataSource(data=dict(x=self.carshape.x,y=self.carshape.y))
        self.wheels = ColumnDataSource(data=dict(x=[-2.25,-0.75],y=[0.25,0.25],w=[0.5,0.5],h=[0.5,0.5]))
        self.arrow = ColumnDataSource(data=dict(xS=[],yS=[],xE=[],yE=[]))
        self.v_label = ColumnDataSource(data=dict(x=[],y=[],S=[]))
        self.fig = figure(tools="",x_range=(-4,31),y_range=(0,4),height=100)
        #  remove graph lines
        self.fig.yaxis.visible = False
        self.fig.grid.visible = False
        self.fig.outline_line_color = None
        self.fig.line([30.0,30.0,29.5,30.5],[0,3.0,3.0,4.0],line_color="black",line_width=4)
        self.fig.patch(x='x',y='y',color="#0065BD",source=self.car)
        self.fig.ellipse(x='x',y='y',width='w',height='h',source=self.wheels, color="#0065BD")
        arrow_glyph = Arrow(end=OpenHead(line_color="#003359",line_width=2,size=10),
            x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=self.arrow,line_color="#003359",line_width=2)
        self.fig.add_layout(arrow_glyph)
        v_glyph=LabelSet(x='x', y='y',text='S',text_color='#003359',text_font_size="15pt",level='glyph',source=self.v_label)
        self.fig.add_layout(v_glyph)
    
    def setV(self,v_0):
        self.arrow.data = dict(xS=[0],yS=[0.5], xE=[v_0], yE=[0.5])
        self.v_label.data = dict(x=[v_0/2.0],y=[0.5],S=[u"v\u2092"])
    
    def disp (self):
        return self.fig
    
    def move(self,x,v):
        temp=self.carshape+(x,0)
        self.car.data=dict(x=temp.x,y=temp.y)
        temp=dict(self.wheels.data)
        temp['x']=[x-2.25,x-0.75]
        self.wheels.data=temp
        self.arrow.data = dict(xS=[x],yS=[0.5], xE=[v+x], yE=[0.5])
        self.v_label.data = dict(x=[x+v/2.0],y=[0.5],S=[u"v\u2092"])
