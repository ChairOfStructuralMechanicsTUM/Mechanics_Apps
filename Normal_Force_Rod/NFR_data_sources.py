from bokeh.models import ColumnDataSource
import numpy as np


## inner app imports
from NFR_constants import (
        xr_start, xr_end, y_offset, #r_reso, # rod coords
        xsl, xsr, ysl, ysr, # support coords
        slide_support_img, fixed_support_img, # support images
        sol_reso
        )



# rod
#rod_source = ColumnDataSource(data=dict(x = np.linspace(xr_start,xr_end,r_reso), y = np.ones(r_reso) * y_offset))
#rod_source = ColumnDataSource(data=dict(x = [xr_start, xr_end], y = [y_offset, y_offset])) # for patch only, no bending
rod_source = ColumnDataSource(data=dict(x=[], y=[]))

# Position of supports
support_source_left  = ColumnDataSource(data=dict(sp_img=[fixed_support_img], x=[xsl] , y=[ysl]))
support_source_right = ColumnDataSource(data=dict(sp_img=[slide_support_img], x=[xsr] , y=[ysr]))


# force/load graphics
force_point_source     = ColumnDataSource(data=dict(xS=[xr_start-1.0], xE=[xr_start], yS=[y_offset+0.1], yE=[y_offset+0.1], lW=[2], lC=["#0065BD"]))
constant_load_source   = ColumnDataSource(data=dict(x=[], y=[]))
triangular_load_source = ColumnDataSource(data=dict(x=[], y=[]))
temperature_source     = ColumnDataSource(data=dict(x=[], y=[]))
#constant_load_source   = ColumnDataSource(data=dict(x=[xr_start, xr_start, xr_end, xr_end], y=[y_offset+0.2, y_offset+1.2, y_offset+1.2, y_offset+0.2]))
#triangular_load_source = ColumnDataSource(data=dict(x=[xr_start, xr_start, xr_end], y=[y_offset+0.2, y_offset+1.2, y_offset+0.2]))
# starting point at lower left of the load

# labels
#labels_source = ColumnDataSource(data=dict(x=[] , y=[], name=[]))
labels_source = ColumnDataSource(dict(x=[],y=[],name=[]))
# main_labels_source
# nomral_lab
#...
labels_N      = ColumnDataSource(dict(x=[],y=[],name=[]))
labels_U      = ColumnDataSource(dict(x=[],y=[],name=[]))


# discretized solutions for the plots
x_samples = np.linspace(xr_start,xr_end,sol_reso)
#samplesF  = ColumnDataSource(dict(x=[], y=[]))
#samplesU  = ColumnDataSource(dict(x=[], y=[]))

# write x_samples also in y to avoid bokeh warning regarind different length
samplesF  = ColumnDataSource(dict(x=x_samples, y=x_samples))
samplesU  = ColumnDataSource(dict(x=x_samples, y=x_samples))



# line roots<->min<->max
aux_line = ColumnDataSource(data=dict(x=[2,2], y=[-100,100]))

# error message window
error_msg_frame = ColumnDataSource(data=dict(x=[],y=[]))
error_msg       = ColumnDataSource(data=dict(x=[],y=[],name=[]))


## global variables (dict, list, no CDS)
#global_variables = dict(rod_line_width=2)
#global_variables = dict(y_cross=0.0)
global_variables = dict(ampl=1.0)

#TODO: maybe move glabal variables also to "constants" and rename it to "variables" or so




