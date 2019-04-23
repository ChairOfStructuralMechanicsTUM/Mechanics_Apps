"""
Python Bokeh program which interactively change two vectos and display its sum

initial work by: Rishith Ellath Meethal
"""

from bokeh.plotting import figure 
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, Arrow, OpenHead, Line
from bokeh.models.glyphs import ImageURL
from bokeh.io import curdoc

from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv, LatexLabelSet

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
support_source = ColumnDataSource(data=dict(x= [], y= [], src = []))
#plot corresponding  to  change in  Force
ForcegraphTop=ColumnDataSource(data=dict(x=[], y=[])) 
ForcegraphBottom=ColumnDataSource(data=dict(x=[], y=[])) 

h_beam = 1.0

def initialize():
    P1_arrow_source.data = dict(xS=[0], xE=[0], yS=[-10], yE=[-h_beam], lW = [5])
    P1_label_source.data = dict(x=[1],y=[-7],P1=["P"])
    P2_arrow_source.data = dict(xS=[40], xE=[40], yS=[10], yE=[h_beam], lW = [5])
    P2_label_source.data = dict(x=[37.5],y=[5],P2=["P"])
    F1_arrow_source.data = dict(xS=[0], xE=[0], yS=[10], yE=[h_beam], lW = [5])
    F1_label_source.data = dict(x=[1],y=[5],F1=["F"])
    F2_arrow_source.data = dict(xS=[40], xE=[40], yS=[-10], yE=[-h_beam], lW = [5])
    F2_label_source.data = dict(x=[37.5],y=[-7],F2=["F"])
    support_source.data = dict(x = [20], y = [-h_beam], src = ["Couple_moment/static/images/fixed_support.svg"]) 
    ForcegraphTop.data = dict(x =[0],y =[10] )
    ForcegraphBottom.data = dict(x =[40],y =[-10] )


plot = figure(title="", tools="", x_range=(0-2,40+2), y_range=(-50,50))
plot.axis.axis_label_text_font_style="normal"
plot.axis.axis_label_text_font_size="14pt"
plot.xaxis.axis_label="Distance [m]"
plot.yaxis.axis_label="Force [N]"

# plot bar and support
plot.line([0, 40], [0, 0], line_width=10, color='#3070B3')
plot.add_glyph(support_source,ImageURL(url="src", x='x', y='y', w=5, h=5, anchor="top_center"))

#plotting Vectors as arrows
P1_arrow_glyph = Arrow(end=OpenHead(line_color="#A2AD00",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=P1_arrow_source,line_color="#A2AD00")
P2_arrow_glyph = Arrow(end=OpenHead(line_color="#A2AD00",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=P2_arrow_source,line_color="#A2AD00")
F1_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=F1_arrow_source,line_color="#E37222")
F2_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=F2_arrow_source,line_color="#E37222")

P1_label_glyph=LatexLabelSet(x='x', y='y',text='P1',text_font_size="15pt",level='glyph',source=P1_label_source)
P2_label_glyph=LatexLabelSet(x='x', y='y',text='P2',text_font_size="15pt",level='glyph',source=P2_label_source)
F1_label_glyph=LatexLabelSet(x='x', y='y',text='F1',text_font_size="15pt",level='glyph',source=F1_label_source)
F2_label_glyph=LatexLabelSet(x='x', y='y',text='F2',text_font_size="15pt",level='glyph',source=F2_label_source)
plot.add_layout(P1_arrow_glyph)
plot.add_layout(P2_arrow_glyph)
plot.add_layout(F1_arrow_glyph)
plot.add_layout(F2_arrow_glyph)
plot.add_layout(P1_label_glyph)
plot.add_layout(P2_label_glyph)
plot.add_layout(F1_label_glyph)
plot.add_layout(F2_label_glyph)
plot.line(x='x',y='y', source=ForcegraphTop,line_width=3,line_color="#E37222",legend=" Force amplitude", line_dash='dotted')
plot.line(x='x',y='y', source=ForcegraphBottom,line_width=3,line_color="#E37222",legend=" Force amplitude",line_dash='dotted' )



def changeF1F2(attr, old, new):
    #changing Force graph back to initial condition
    YS = 400.0/(40.0-2.0*new)
    F1_arrow_source.patch( {"xS":[(0,new)], "xE":[(0,new)], "yS":[(0,YS)]} )
    F1_label_source.patch({"x":[(0,1+new)]})
    F2_arrow_source.patch( {"xS":[(0,40-new)], "xE":[(0,40-new)], "yS":[(0,-YS)]} )
    F2_label_source.patch({"x":[(0,37.5-new)]})
     
#creating  slider to change location of Forces F1 and F2
#F1F2Location_slider= Slider(title="Change Location of F"u"\u2081 and F"u"\u2082 (m)",value= 0,start = 0, end = 19, step = 1)
F1F2Location_slider= Slider(title="Change Location of F"u"\u2081 and F"u"\u2082 together",value= 0,start = 0, end = 19, step = 1)
F1F2Location_slider.on_change('value',changeF1F2)

#adding description from HTML file
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)

initialize()

curdoc().add_root(column(description,row(plot,column(F1F2Location_slider))))
curdoc().title = "Couple moment"
