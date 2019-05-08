

## inner app imports
from NFR_constants import (
        xr_start, xr_end, y_offset, r_reso, # rod coords
        xsl, xsr, ysl, ysr, # support coords
        slide_support_img, fixed_support_img # support images
        )

from NFR_data_sources import (
        rod_source,
        support_source_left, support_source_right,
        force_point_source, constant_load_source, triangular_load_source,
        labels_source,
        aux_line
        )





def change_load(attr, old, new):
    print("DEBUG: change_load, new=",new)
    if new==0:
        labels_source.data = dict(x=[xr_start-0.6],y=[y_offset+0.2],name=['F'])
        force_point_source.data = dict(xS=[xr_start-1.0], xE=[xr_start], yS=[y_offset+0.1], yE=[y_offset+0.1], lW=[2], lC=["#0065BD"])
        constant_load_source.data = dict(x=[], y=[])
        triangular_load_source.data = dict(x=[], y=[])
    elif new==1:
        labels_source.data = dict(x=[xr_start+1.5,xr_start+4.5,xr_start+7.5],y=[y_offset+0.9,y_offset+0.9,y_offset+0.9],name=['F','F','F'])
        force_point_source.data = dict(xS=[xr_start+1,xr_start+4,xr_start+7], xE=[xr_start+2,xr_start+5,xr_start+8], yS=[y_offset+0.7,y_offset+0.7,y_offset+0.7], yE=[y_offset+0.7,y_offset+0.7,y_offset+0.7], lW=[2,2,2], lC=["#0065BD","#0065BD","#0065BD"])
        constant_load_source.data = dict(x=[xr_start, xr_start, xr_end, xr_end], y=[y_offset+0.2, y_offset+1.2, y_offset+1.2, y_offset+0.2])
        triangular_load_source.data = dict(x=[], y=[])
    elif new==2:
        labels_source.data = dict(x=[],y=[],name=[])
        force_point_source.data = dict(xS=[xr_start+0.5,xr_start+2], xE=[xr_start+1.5,xr_start+3], yS=[y_offset+0.7,y_offset+0.7], yE=[y_offset+0.7,y_offset+0.7], lW=[2,2], lC=["#0065BD","#0065BD"])
        constant_load_source.data = dict(x=[], y=[])
        triangular_load_source.data = dict(x=[xr_start, xr_start, xr_end], y=[y_offset+0.2, y_offset+1.2, y_offset+0.2])
    elif new==3:
        print("Temperature")
        # do coding
    else:
        print("How did you get here?")
        # raise error or something (plot message on screen via bokeh?)