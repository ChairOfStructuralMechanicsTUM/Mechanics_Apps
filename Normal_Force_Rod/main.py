from bokeh.plotting import Figure#, output_file , show
#from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, Arrow
from bokeh.models import Arrow, OpenHead, LabelSet
from bokeh.models.glyphs import ImageURL, Patch, MultiLine, Rect #, Quadratic, Rect, Patch
from bokeh.models.layouts import Spacer
from bokeh.models.widgets import Paragraph
from bokeh.layouts import column, row, widgetbox, layout
from bokeh.io import curdoc
#import numpy as np
#import math
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexDiv#, LatexLabel, LatexLabelSet, LatexSlider, LatexLegend



from NFR_constants import (
        xr_start, xr_end,
        x_range, fig_height,
        lb, ub
        )

from NFR_Shapes import (
        NFR_Rod, NFR_RodShadow,
        NFR_ForceArrow, NFR_ConstantLoad, NFR_TriangularLoad, NFR_TemperatureLoad
        )
from NFR_DrawAPI import (
        NFR_BlueRod, NFR_BlackShadowRod, NFR_BlueArrow, NFR_BlueLoad
        )

from NFR_GUIControl import NFR_GUIControl


from NFR_helper_functions import (
        set_load, 
        refresh_objects
        )


########################################
#####      init all objects        #####
########################################
rod = NFR_Rod(NFR_BlueRod())
rod_shadow = NFR_RodShadow(NFR_BlackShadowRod())




# buttons, sliders, etc.
control = NFR_GUIControl()




force_arrow = NFR_ForceArrow(NFR_BlueArrow(), xr_start-1.0, xr_start, 0.1, 0.1)
const_load  = NFR_ConstantLoad(NFR_BlueLoad(), control.load_position_slider.value, lb, ub)
triang_load = NFR_TriangularLoad(NFR_BlueLoad(), control.load_position_slider.value, lb, ub)
temp_load = NFR_TemperatureLoad(NFR_BlueLoad(), control.load_position_slider.value, lb, ub)


########################################
#####      init all objects        #####
########################################
# seems impossible to outsurce using this structure
# keep them as short and simple as possible
# helper functions can be used in the way that they don't manipulate CDS directly

def change_load(attr, old, new):
    print("DEBUG: change_load, new=",new)
    current_position = control.load_position_slider.value
    
#    #print(const_load.shape.data)
#    [force_arrow.shape.data,
#     const_load.shape.data,
#     triang_load.shape.data,
#     temp_load.shape.data]    =  set_load(new,current_position)
    
    
    #print(const_load.shape.data)
    
    obj_list = [force_arrow, const_load, triang_load, temp_load]
    set_load(new, current_position, obj_list)
    
    #print(const_load.shape.data)
    
#    force_arrow.draw(plot_main)
#    const_load.draw(plot_main)
#    triang_load.draw(plot_main)
#    temp_load.draw(plot_main)
    
    refresh_objects(obj_list, plot_main)
    
    
    #const_load.drawAPI.drawPatch(plot_main, const_load.shape, alpha=0.1)
    #print(const_load.shape.data)
    #compute_new_scenario()

def reset():
    pass
    #rod.shape.data = dict(x=[8, 8, 9, 9], y=[0, 0.2, 0.2, 0])
    #rod.drawAPI.drawPatch(plot_main, rod.shape, color="#446511")
    #refresh_object(rod, plot_main)



control.reset_button.on_click(reset)

control.radio_button_group.on_change('active',change_load)



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


#rod.drawAPI.drawPatch(plot_main, rod.shape)
rod.draw(plot_main)
force_arrow.draw(plot_main)
#const_load.draw(plot_main)






###### PLOT (NORMAL FORCE):
# Define plot
plot_normalF = Figure(title="Normal force N(x)", tools="yzoom_in,yzoom_out,reset", x_range=x_range, y_range=(-11,11), height=fig_height)
# Set properties
plot_normalF.axis.visible = False
plot_normalF.outline_line_width = 2
plot_normalF.outline_line_color = "Black"
plot_normalF.title.text_font_size = "13pt"
plot_normalF.toolbar.logo = None

rod_shadow.draw(plot_normalF)




###### PLOT (DEFORMATION):
# Define plot
plot_deform = Figure(title="Deformation u(x)", tools="yzoom_in,yzoom_out,reset", x_range=x_range, y_range=(-12,12), height=fig_height)
# Set properties
plot_deform.axis.visible = False
plot_deform.outline_line_width = 2
plot_deform.outline_line_color = "Black"
plot_deform.title.text_font_size = "13pt"
plot_deform.toolbar.logo = None


rod_shadow.draw(plot_deform)






##### ADD DESCRIPTION FROM HTML FILE
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1000)


doc_layout = layout(children=[
        column(description,
               row(column(
                       Spacer(height=20,width=450),
                       widgetbox(control.radio_button_group),
                       #row(widgetbox(p_rt1, width=120), widgetbox(radio_group_left)),
                       #row(widgetbox(p_rt2, width=120), widgetbox(radio_group_right)), 
                       ##row(widgetbox(p_rt3, width=120), widgetbox(radio_group_cross)), 
                       #row(widgetbox(p_rt4, width=120), widgetbox(radio_group_ampl)), 
                       #load_position_slide,
                       ##load_magnitude_slide,
                       ##slider_group,
                       #simple_button_group
                       control.reset_button),
                   column(plot_main,plot_normalF,plot_deform ) ) ) ] )



curdoc().add_root(doc_layout)
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '