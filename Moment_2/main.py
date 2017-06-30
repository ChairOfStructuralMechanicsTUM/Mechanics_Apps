"""
Python Bokeh program which interactively change two vectos and display its sum

done by :Rishith Ellath Meethal
"""

from bokeh.plotting import figure 
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, LabelSet, Arrow, OpenHead, Line,Div
from bokeh.io import curdoc
from os.path import dirname, join
import numpy as np



#Plot source:
plot_source = ColumnDataSource(data=dict(x = np.linspace(0,40,100), y = np.linspace(0,0,100)))

#Force Vectors
P1_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
P2_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
F1_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
F2_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
#labels for Forces
P1_label_source = ColumnDataSource(data=dict(x=[],y=[],P1=[]))
P2_label_source = ColumnDataSource(data=dict(x=[],y=[],P2=[]))
F1_label_source = ColumnDataSource(data=dict(x=[],y=[],F1=[]))
F2_label_source = ColumnDataSource(data=dict(x=[],y=[],F2=[]))
#Triangle source:
triangle_source = ColumnDataSource(data=dict(x= [], y= [], size = []))
#plot corresponding  to  change in  Force
ForcegraphTop=ColumnDataSource(data=dict(x=[], y=[])) 
ForcegraphBottom=ColumnDataSource(data=dict(x=[], y=[])) 


def initialise():
    P1_arrow_source.data = dict(xS=[0], xE=[0], yS=[-10], yE=[0], lW = [5])
    P1_label_source.data = dict(x=[1],y=[-7],P1=['P1'])
    P2_arrow_source.data = dict(xS=[40], xE=[40], yS=[10], yE=[0], lW = [5])
    P2_label_source.data = dict(x=[77.5],y=[5],P2=['P2'])
    F1_arrow_source.data = dict(xS=[0], xE=[0], yS=[10], yE=[0], lW = [5])
    F1_label_source.data = dict(x=[1],y=[5],F1=['F1'])
    F2_arrow_source.data = dict(xS=[40], xE=[40], yS=[-10], yE=[0], lW = [5])
    F2_label_source.data = dict(x=[37.5],y=[-7],F2=['F2'])
    triangle_source.data = dict(x = [20], y = [-2], size = [20,20]) 
    ForcegraphTop.data      = dict(x =[0],y =[10] )
    ForcegraphBottom.data      = dict(x =[40],y =[-10] )


plot = figure(title="Moment_2", x_range=(0-2,40+2), y_range=(-50,50))
plot.axis.axis_label_text_font_style="normal"
plot.axis.axis_label_text_font_size="14pt"
plot.xaxis.axis_label="Distance [m]"
plot.yaxis.axis_label="Force[N]"

my_line=plot.line(x='x', y='y', source=plot_source, color='#0065BD',line_width=20)
plot.triangle(x='x', y='y', size = 'size', source= triangle_source,color="#E37222", line_width=2)

#plotting Vectors as arrows
P1_arrow_glyph = Arrow(end=OpenHead(line_color="#A2AD00",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=P1_arrow_source,line_color="#A2AD00")
P2_arrow_glyph = Arrow(end=OpenHead(line_color="#A2AD00",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=P2_arrow_source,line_color="#A2AD00")
F1_arrow_glyph = Arrow(end=OpenHead(line_color="#F4A582",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=F1_arrow_source,line_color="#F4A582")
F2_arrow_glyph = Arrow(end=OpenHead(line_color="#F4A582",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=F2_arrow_source,line_color="#F4A582")
P1_label_glyph=LabelSet(x='x', y='y',text='P1',text_font_size="15pt",level='glyph',source=P1_label_source)
P2_label_glyph=LabelSet(x='x', y='y',text='P2',text_font_size="15pt",level='glyph',source=P2_label_source)
F1_label_glyph=LabelSet(x='x', y='y',text='F1',text_font_size="15pt",level='glyph',source=F1_label_source)
F2_label_glyph=LabelSet(x='x', y='y',text='F2',text_font_size="15pt",level='glyph',source=F2_label_source)
plot.add_layout(P1_arrow_glyph)
plot.add_layout(P2_arrow_glyph)
plot.add_layout(F1_arrow_glyph)
plot.add_layout(F2_arrow_glyph)
plot.add_layout(P1_label_glyph)
plot.add_layout(P2_label_glyph)
plot.add_layout(F1_label_glyph)
plot.add_layout(F2_label_glyph)
plot.line(x='x',y='y', source=ForcegraphTop,line_width=3,line_color='red',legend=" Force change" )
plot.line(x='x',y='y', source=ForcegraphBottom,line_width=3,line_color='red',legend=" Force change" )


initialise()

def changeF1F2(attr,old,new):
    
     #changing Force graph back to initial condition
     ForcegraphTop.data      = dict(x =[0],y =[10] )
     ForcegraphBottom.data      = dict(x =[40],y =[-10] )
     YS = 400/(40-2*new)
     F1_arrow_source.data = dict(xS=[0+new], xE=[0+new], yS=[YS], yE=[0], lW = [5])
     F1_label_source.data = dict(x=[1+new],y=[5],F1=['F1'])
     F2_arrow_source.data = dict(xS=[40-new], xE=[40-new], yS=[-YS], yE=[0], lW = [5])
     F2_label_source.data = dict(x=[37.5-new],y=[-7],F2=['F2'])
     XcordinatesT=[None]*(2*new+3)
     XcordinatesB=[None]*(2*new+3)
     YcordinatesT=[None]*(2*new+3)
     YcordinatesB=[None]*(2*new+3)
    
    
     XcordinatesT[0]=0
     XcordinatesB[0]=40
     YcordinatesT[0]=10
     YcordinatesB[0]=-10
     i=1
     count = 1
     for i in range(new+1):
         XcordinatesT[count]=(i-0.5)
         XcordinatesT[count+1]=(i)
         XcordinatesB[count]=40-(i-0.5)
         XcordinatesB[count+1]=40-(i)
         y=float(400/(40-(2*(i-0.5))))
         y1=float(400/(40-(2*(i))))
         YcordinatesT[count]=y
         YcordinatesT[count+1]=y1
         YcordinatesB[count]=-y
         YcordinatesB[count+1]=-y1
         count=count+2
                     
                     
     new_dataT= {
    'x' : XcordinatesT,
    'y' : YcordinatesT,
            }
     
     ForcegraphTop.stream(new_dataT)
     
     new_dataB= {
    'x' : XcordinatesB,
    'y' : YcordinatesB,
            }
     ForcegraphBottom.stream(new_dataB)
     
#creating  slider to change location of Forces F1 and F2
F1F2Location_slider= Slider(title="Change Location of F1 & F2 together",value= 0,start = 0, end = 19, step = 1)
F1F2Location_slider.on_change('value',changeF1F2)

#adding description from HTML file
description_filename = join(dirname(__file__), "description.html")
description = Div(text=open(description_filename).read(), render_as_text=False, width=1200)

curdoc().add_root(column(description,row(plot,column(F1F2Location_slider))))
curdoc().title = "Moment_2"