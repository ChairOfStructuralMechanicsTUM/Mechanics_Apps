from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import Slider, Span, CustomJS, Label
from bokeh.plotting import figure
 
slider = Slider(start=0, end=10, value=3, step=0.1, title='Slider')
 
plot = figure(width=700, height=250, x_range=(0,10), y_range=(-1, 1))
span = Span(location=slider.value, dimension='height')
plot.add_layout(span)
label = Label(x=slider.value, y=0, x_units='data', y_units='data',
                 text="Minimum")
plot.add_layout(label)
 
slider.callback = CustomJS(args=dict(span=span, label=label, slider=slider), code="""
    span.location = slider.value
    label.x = slider.value
""")
curdoc().add_root(row(plot, widgetbox(slider)))
