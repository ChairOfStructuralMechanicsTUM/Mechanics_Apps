from math import radians
from bokeh.plotting import Figure
from bokeh.layouts import row,widgetbox
from bokeh.models import Arrow, OpenHead
from bokeh.models.widgets import TextInput
from bokeh.io import curdoc
from bokeh.models.widgets import Slider

xMin=0
xMax=10
yMin=0
yMax=10

p=Figure(plot_width=400,
         plot_height=300,
         x_range=(xMin,xMax),
         y_range=(yMin,yMax),
         title='Instant Centre of Rotation',
        )
p.yaxis.visible=False
p.title.text_font_size = "25px"
p.title.align = "center"
p.circle(x=2.5,y=2.5,radius=1)

p.add_layout(Arrow(end=OpenHead(line_color='black',line_width=4),
                   x_start=2.5,y_start=2.5,x_end=5,y_end=5))

test=Slider(title="Check",value=0.0,start=-1.0,end=1.0)
text_input = TextInput(value="Angle of arrow 1",title="label:")

inputs=widgetbox(test,text_input)
curdoc().add_root(row(p,inputs,width=800))