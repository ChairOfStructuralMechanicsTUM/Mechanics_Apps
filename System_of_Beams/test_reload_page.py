

from bokeh.models           import ColumnDataSource, Button, Div
from bokeh.layouts          import column
from bokeh.models.callbacks import CustomJS
from bokeh.plotting         import figure, curdoc
from functools              import partial
import time                 as time
from threading              import Thread

doc = curdoc()
Data = ColumnDataSource(data=dict(x=[], y=[]))
div_input = Div(width=200, height=100)
JS = CustomJS(args=dict(div=None), code="""
    //JavaScript code:
    alert( 'on_change works!' );
    """)

# plot
p = figure(x_range=(0, 5), y_range=(0, 5),  tools='box_select')
p.circle('x','y',source=Data)
def cb_on_change(div_input):
    # Java Script
    JS.args['div'] = div_input
    return JS

def callback():
    print('here')
    Data.data=dict(x=[3],y=[3])

def do_smth():
    Data.selected.js_on_change('indices', cb_on_change(div_input))

def blocking_task():
    while True:
        time.sleep(0.1)
        doc.add_next_tick_callback(partial(do_smth))


# button
button = Button(label='button')
button.on_click(callback)





# place in window
doc.add_root(column(button,p,div_input))


thread = Thread(target=blocking_task)
thread.start()