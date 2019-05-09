############################ 
####     MAIN FILE      ####
############################
from bokeh.plotting import Figure#, output_file , show
#from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, Arrow
from bokeh.models import Arrow, OpenHead, LabelSet
from bokeh.models.glyphs import ImageURL, Patch#, Quadratic, Rect, Patch
from bokeh.models.layouts import Spacer
from bokeh.models.widgets import Paragraph
from bokeh.layouts import column, row, widgetbox, layout
from bokeh.io import curdoc
import numpy as np
#import math
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexDiv#, LatexLabel, LatexLabelSet, LatexSlider, LatexLegend



## inner app imports
from NFR_constants import (
        fig_height, fig_width, x_range
        )
from NFR_data_sources import (
        rod_source,
        support_source_left, support_source_right,
        force_point_source, constant_load_source, triangular_load_source,
        labels_source,
        aux_line
        )
from NFR_buttons import (
        load_position_slide, load_magnitude_slide,
        radio_button_group, radio_group_left, radio_group_right, radio_group_cross,
        reset_button, dummy_button
        )
from NFR_callback_functions import (
        change_load, change_cross_section,
        change_left_support, change_right_support,
        change_load_position,
        reset
        )



## file description (put -also- in Readme)
# NFR_constants             global constants, default values, images (ext. source)
# NFR_data_sources          ColumnDataSources needed for this program
# NFR_buttons               Buttons, Sliders, Radio Buttons (baically input widgets)
# NFR_callback_functions    inner parts, buttons, sliders (etc.) functionality





radio_button_group.on_change('active',change_load)


radio_group_left.on_change('active',change_left_support)
radio_group_right.on_change('active',change_right_support)
radio_group_cross.on_change('active',change_cross_section)

load_position_slide.on_change('value',change_load_position)

reset_button.on_click(reset)



########################################
#####           PLOTTING           #####
########################################


###### MAIN PLOT (SUPPORT AND LOAD):
# Define plot:
plot_main = Figure(title="Rod with Supports and Load", tools="", x_range=x_range, y_range=(-2.5,2.5), height=fig_height)
# Set properties
plot_main.axis.visible = False
plot_main.outline_line_width = 2
plot_main.outline_line_color = "Black"
plot_main.title.text_font_size = "13pt"
plot_main.toolbar.logo = None


plot_main.add_glyph(support_source_left,ImageURL(url="sp_img", x='x', y='y', w=0.66, h=0.4))
plot_main.add_glyph(support_source_right,ImageURL(url="sp_img", x='x', y='y', w=0.66, h=0.4))


#plot_main.line(x='x', y='y', source=rod_source, color='#0065BD',line_width=15)
rod_glyph = Patch(x='x', y='y', line_color='#0065BD',line_width=15, fill_color="#0065BD")
plot_main.add_glyph(rod_source, rod_glyph)
# patch instead of line to comply with cross-section

force_arrow_glyph = Arrow(end=OpenHead(line_color="#0065BD",line_width=2, size=5), 
                          x_start='xS', x_end='xE', y_start='yS', y_end='yE',
                          line_width='lW', line_color='lC', source=force_point_source)

plot_main.add_layout(force_arrow_glyph)

# outsource in callback functions
#labels_source.data = dict(x=[-0.6],y=[0.2],name=['F'])
main_labels = LabelSet(x='x', y='y', text='name', level='glyph', render_mode='canvas', source=labels_source)
plot_main.add_layout(main_labels)

constant_load_glyph = Patch(x='x', y='y', fill_color="#0065BD", fill_alpha=0.5)
triangular_load_glyph = Patch(x='x', y='y', fill_color="#0065BD", fill_alpha=0.5)
plot_main.add_glyph(constant_load_source, constant_load_glyph)
plot_main.add_glyph(triangular_load_source, triangular_load_glyph)





###### PLOT (NORMAL FORCE):
# Define plot
plot_normalF = Figure(title="Normal force N(x)", tools="", x_range=x_range, y_range=(-11,11), height=fig_height)
# Set properties
plot_normalF.axis.visible = False
plot_normalF.outline_line_width = 2
plot_normalF.outline_line_color = "Black"
plot_normalF.title.text_font_size = "13pt"
plot_normalF.toolbar.logo = None


## const p=2     -2x
#x = np.linspace(0,10,1000)
#y = np.ones(1000)*-2*x
#normalF_source = ColumnDataSource(data=dict(x=[] , y=[]))
#normalF_source.data = dict(x=x, y=y)
#
#plot_normalF.line(x='x', y='y', source=normalF_source, color="#A2AD00",line_width=2)

# evtl. gleichmit scipy und integration rules für beliebiges p


###### PLOT (DEFORMATION):
# Define plot
plot_deform = Figure(title="Deformation u(x)", tools="", x_range=x_range, y_range=(-12,12), height=fig_height)
# Set properties
plot_deform.axis.visible = False
plot_deform.outline_line_width = 2
plot_deform.outline_line_color = "Black"
plot_deform.title.text_font_size = "13pt"
plot_deform.toolbar.logo = None


##### ADD DESCRIPTION FROM HTML FILE
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1000)



rt_filename = join(dirname(__file__), "radio_button_title.html")
rt = LatexDiv(text=open(rt_filename).read())

p_rt1 = Paragraph(text="""Left support:  """)
p_rt2 = Paragraph(text="""Right support: """)
p_rt3 = Paragraph(text="""Cross-section: """)


#slider_group = widgetbox(p_loc_slide,p_mag_slide,sup2_loc_slide) # together to close....
simple_button_group = widgetbox([reset_button, dummy_button])

doc_layout = layout(children=[
        column(description,
               row(column(
                       Spacer(height=20,width=450),
                       widgetbox(radio_button_group),
                       row(widgetbox(p_rt1, width=120), widgetbox(radio_group_left)),
                       row(widgetbox(p_rt2, width=120), widgetbox(radio_group_right)), 
                       row(widgetbox(p_rt3, width=120), widgetbox(radio_group_cross)), 
                       load_position_slide,
                       load_magnitude_slide,
                       #slider_group,
                       simple_button_group),
                   column(plot_main,plot_normalF,plot_deform ) ) ) ] )



curdoc().add_root(doc_layout)
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '