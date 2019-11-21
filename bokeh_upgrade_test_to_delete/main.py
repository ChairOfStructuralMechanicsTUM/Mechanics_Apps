from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Slider, Arrow, OpenHead
from bokeh.layouts import column
from bokeh.io import curdoc


cds_arrow = ColumnDataSource(dict(xS=[0], yS=[1], xE=[1], yE=[1]))
#cds_arrow = ColumnDataSource(dict(xS=[0,0,0], yS=[1,2,3], xE=[1,1,1], yE=[1,2,3]))
cds_line  = ColumnDataSource(dict(x=[0,1], y=[3,3]))


def slider_callback_data(attr,old,new):
    cds_arrow.data = dict(xS=[0], yS=[1], xE=[new], yE=[1])
    cds_line.data  = dict(x=[0,new], y=[3,3])
    #print(cds_arrow.data) # data is updated but not plotted

def slider_callback_stream(attr,old,new):
    cds_arrow.stream(dict(xS=[0], yS=[1], xE=[new], yE=[1]),rollover=1)
    cds_line.stream(dict(x=[0,new], y=[3,3]),rollover=2)


slider_data = Slider(title="cds.data", value=1.0, start=0.0, end=5.0, step=0.1, width=400)
slider_data.on_change('value',slider_callback_data)

slider_stream = Slider(title="cds.stream", value=1.0, start=0.0, end=5.0, step=0.1, width=400)
slider_stream.on_change('value',slider_callback_stream)

figure_test = figure(title="Example Figure", x_range=(-1,6), y_range=(-0.5,4.5), height=300, width=400, tools="")
figure_test.line(x='x', y='y', source=cds_line)
arrow_glyph = Arrow(end=OpenHead(), x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=cds_arrow)
figure_test.add_layout(arrow_glyph)


curdoc().add_root(column(figure_test, slider_data, slider_stream))
