"""
Python Bokeh program which interactively change two vectos and display its sum

initial work by: Rishith Ellath Meethal
"""

from bokeh.plotting import figure 
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, Arrow, OpenHead, Line, TeeHead
from bokeh.models.glyphs import ImageURL
from bokeh.io import curdoc

from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv, LatexSlider, LatexLabelSet

h_beam = 1.0

# Force vectors and labels
P1_arrow_source = ColumnDataSource(dict(xS=[0], xE=[0], yS=[-10], yE=[-h_beam], lW = [5]))
P1_label_source = ColumnDataSource(dict(x=[1],y=[-7],P1=["P"]))
P2_arrow_source = ColumnDataSource(dict(xS=[40], xE=[40], yS=[10], yE=[h_beam], lW = [5]))
P2_label_source = ColumnDataSource(dict(x=[37.5],y=[5],P2=["P"]))
F1_arrow_source = ColumnDataSource(dict(xS=[10], xE=[10], yS=[20], yE=[h_beam], lW = [5]))
F1_label_source = ColumnDataSource(dict(x=[11],y=[5],F1=["F"]))
F2_arrow_source = ColumnDataSource(dict(xS=[30], xE=[30], yS=[-20], yE=[-h_beam], lW = [5]))
F2_label_source = ColumnDataSource(dict(x=[27.5],y=[-7],F2=["F"]))
# Support source
support_source = ColumnDataSource(dict(x = [20], y = [-h_beam], src = ["Couple_moment/static/images/fixed_support.svg"]))

# Plot
plot = figure(title="", tools="", x_range=(0-2,40+2), y_range=(-50,50))
plot.toolbar.logo = None
plot.axis.axis_label_text_font_style="normal"
plot.axis.axis_label_text_font_size="14pt"
plot.xaxis.axis_label="Distance [m]"
plot.yaxis.axis_label="Force [N]"

# plot bar and support
plot.line([0, 40], [0, 0], line_width=10, color='#3070B3')
plot.add_glyph(support_source,ImageURL(url="src", x='x', y='y', w=3.3, h=5, anchor="top_center"))

# plot distance
dist_a = Arrow(end=TeeHead(line_color="#808080", line_width=1, size=10),
    start=TeeHead(line_color="#808080",line_width=1, size=10),
    x_start=0, y_start=-15, x_end=20, y_end=-15,line_width=1, line_color="#808080")
dist_a_label = LatexLabelSet(x='x', y='y', text='text', source=ColumnDataSource(dict(x=[9.7], y=[-13.5], text=["a"])))
dist_b_source = ColumnDataSource(dict(xS=[20], xE=[30], yS=[15], yE=[15], xL=[24.7], yL=[16.5], text=["b"]))
dist_b = Arrow(end=TeeHead(line_color="#808080", line_width=1, size=10),
    start=TeeHead(line_color="#808080",line_width=1, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_width=1, line_color="#808080", source=dist_b_source)
dist_b_label = LatexLabelSet(x='xL', y='yL', text='text', source=dist_b_source)


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
plot.add_layout(dist_a)
plot.add_layout(dist_a_label)
plot.add_layout(dist_b)
plot.add_layout(dist_b_label)

def changeF1F2(attr, old, new):
    new = 20.0-new
    YS = 400.0/(40.0-2.0*new)
    F1_arrow_source.patch( {"xS":[(0,new)], "xE":[(0,new)], "yS":[(0,YS)]} )
    F1_label_source.patch( {"x":[(0,1+new)]} )
    F2_arrow_source.patch( {"xS":[(0,40-new)], "xE":[(0,40-new)], "yS":[(0,-YS)]} )
    F2_label_source.patch( {"x":[(0,37.5-new)]} )
    dist_b_source.patch( {'xE':[( 0,40-new )], 'xL':[(0,(20-new)/2.0+20)]} )
     
# Slider to change location of Forces F1 and F2
F1F2Location_slider = LatexSlider(title="\\text{Length } b =",value=10, start=1, end=20, step=1, value_unit="\\text{m}")
F1F2Location_slider.on_change('value',changeF1F2)

#adding description from HTML file
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=880)

curdoc().add_root(column(description,row(plot,column(F1F2Location_slider))))
curdoc().title = "Couple moment"
