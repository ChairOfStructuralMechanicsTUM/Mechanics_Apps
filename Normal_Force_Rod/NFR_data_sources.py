from bokeh.models import ColumnDataSource
import numpy as np


## inner app imports
from NFR_constants import (
        xr_start, xr_end, r_reso, # rod coords
        xsl, xsr, ysl, ysr, # support coords
        slide_support_img, fixed_support_img # support images
        )



# rod
rod_source = ColumnDataSource(data=dict(x = np.linspace(xr_start,xr_end,r_reso), y = np.ones(r_reso) * 0 ))

# Position of supports
support_source_left  = ColumnDataSource(data=dict(sp_img=[fixed_support_img], x=[xsl] , y=[ysl]))
support_source_right = ColumnDataSource(data=dict(sp_img=[slide_support_img], x=[xsr] , y=[ysr]))



# line roots<->min<->max
aux_line = ColumnDataSource(data=dict(x=[], y=[])) # test, see if it works


