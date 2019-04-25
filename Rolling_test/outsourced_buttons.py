from bokeh.models import ColumnDataSource, Select, Button

start_button = Button(label="Start", button_type="success")
start_button.on_click(start)