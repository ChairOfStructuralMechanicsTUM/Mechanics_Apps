from bokeh.models import ColumnDataSource, Button, DataTable, TableColumn
from bokeh.plotting import Figure, curdoc
from bokeh.layouts import widgetbox, column, layout

from os.path import dirname, split

import numpy as np

import boundaryVal_math as bv_math
import boundaryVal_helper as bv_help
import boundaryVal_settings as bv_settings


def shoot_further():
    """
    called to shoot further. Via bisection the next shot is placed in the interval right of the current shot
    """
    alpha_right = app_data.data['alpha_right'][0]
    alpha_left = app_data.data['alpha'][0]
    app_data.data = dict(alpha=[(alpha_left + alpha_right) / 2],
                         alpha_left=[alpha_left],
                         alpha_right=[alpha_right])
    update_data()


def shoot_shorter():
    """
    called to shoot shorter. Via bisection the next shot is placed in the interval left of the current shot
    """
    alpha_right = app_data.data['alpha'][0]
    alpha_left = app_data.data['alpha_left'][0]
    app_data.data = dict(alpha=[(alpha_left + alpha_right) / 2],
                         alpha_left=[alpha_left],
                         alpha_right=[alpha_right])
    update_data()


def update_data():
    """
    Called each time that any watched property changes. This updates the shooting curve data with the most recent values
    """

    # solve shooting ODE with numerical scheme
    _, x = bv_math.shoot_with_alpha(app_data.data['alpha'][0])
    _, x_short = bv_math.shoot_with_alpha(app_data.data['alpha_left'][0])
    _, x_far = bv_math.shoot_with_alpha(app_data.data['alpha_right'][0])

    source_datatable.data = dict(shot_alpha=[app_data.data['alpha'][0]],
                                 shot_error=[x[0,-1]-target_position])

    rx = x[0, :].tolist()
    ry = x[1, :].tolist()
    rx_short = x_short[0, :].tolist()
    ry_short = x_short[1, :].tolist()
    rx_far = x_far[0, :].tolist()
    ry_far = x_far[1, :].tolist()

    source.data = dict(rx=rx, ry=ry)
    source_short.data = dict(rx_short=rx_short, ry_short=ry_short)
    source_far.data = dict(rx_far=rx_far, ry_far=ry_far)


# initialize data source
source = ColumnDataSource(data=dict(rx=[], ry=[]))
source_short = ColumnDataSource(data=dict(rx_short=[], ry_short=[]))
source_far = ColumnDataSource(data=dict(rx_far=[], ry_far=[]))
source_datatable = ColumnDataSource(data=dict(shot_alpha=[], shot_error=[]))
app_data = ColumnDataSource(data=dict(alpha=[bv_settings.alpha_init], alpha_left=[bv_settings.alpha_left],
                                      alpha_right=[bv_settings.alpha_right]))

buttonShort = Button(label="shoot shorter", width=300)
buttonShort.on_click(shoot_shorter)
buttonFar = Button(label="shoot further", width=300)
buttonFar.on_click(shoot_further)

# initialize plot
toolset = "crosshair,pan,reset,wheel_zoom,box_zoom"
# Generate a figure container
plot = Figure(plot_height=bv_settings.fig_height,
              plot_width=bv_settings.fig_width,
              tools=toolset,
              title=bv_settings.title,  # obj.text.value,
              x_range=[bv_settings.min_x, bv_settings.max_x],
              y_range=[bv_settings.min_y, bv_settings.max_y]
              )
# Plot the line by the x,y values in the source property
plot.line('rx', 'ry',
          source=source,
          line_width=3,
          line_alpha=0.6,
          color='blue',
          legend_label='current shot')
plot.line('rx_short', 'ry_short',
          source=source_short,
          line_width=1,
          line_alpha=.6,
          line_dash=[4, 4],
          color='green',
          legend_label='old next shorter shot')
plot.line('rx_far', 'ry_far',
          source=source_far,
          line_width=1,
          line_alpha=.6,
          line_dash=[4, 4],
          color='red',
          legend_label='old next farther sh')

# insert picture of cannon and target
target_position = np.random.rand() * 10
bv_help.draw_target_at(plot, target_position)
bv_help.draw_cannon(plot)

columns = [
    TableColumn(field="shot_alpha", title="Alpha"),
    TableColumn(field="shot_error", title="Error")
]

data_table = DataTable(source=source_datatable, columns=columns, width=350, height=50)

# calculate data
update_data()

# make layout
curdoc().add_root(layout(children=[[plot],
                                   [widgetbox(buttonShort, buttonFar, width=300, height=100)],
                                   [widgetbox(data_table, width=350, height=80)]],
                         sizing_mode='fixed'))

curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
