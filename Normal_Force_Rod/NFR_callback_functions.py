

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
    if new==0: # point laod
        labels_source.data = dict(x=[xr_start-0.6],y=[y_offset+0.2],name=['F'])
        force_point_source.data = dict(xS=[xr_start-1.0], xE=[xr_start], yS=[y_offset+0.1], yE=[y_offset+0.1], lW=[2], lC=["#0065BD"])
        constant_load_source.data = dict(x=[], y=[])
        triangular_load_source.data = dict(x=[], y=[])
    elif new==1: # constant load
        labels_source.data = dict(x=[xr_start+1.5,xr_start+4.5,xr_start+7.5],y=[y_offset+0.9,y_offset+0.9,y_offset+0.9],name=['F','F','F'])
        force_point_source.data = dict(xS=[xr_start+1,xr_start+4,xr_start+7], xE=[xr_start+2,xr_start+5,xr_start+8], yS=[y_offset+0.7,y_offset+0.7,y_offset+0.7], yE=[y_offset+0.7,y_offset+0.7,y_offset+0.7], lW=[2,2,2], lC=["#0065BD","#0065BD","#0065BD"])
        constant_load_source.data = dict(x=[xr_start, xr_start, xr_end, xr_end], y=[y_offset+0.2, y_offset+1.2, y_offset+1.2, y_offset+0.2])
        triangular_load_source.data = dict(x=[], y=[])
    elif new==2: # triangular load
        labels_source.data = dict(x=[],y=[],name=[])
        force_point_source.data = dict(xS=[xr_start+0.5,xr_start+2], xE=[xr_start+1.5,xr_start+3], yS=[y_offset+0.7,y_offset+0.7], yE=[y_offset+0.7,y_offset+0.7], lW=[2,2], lC=["#0065BD","#0065BD"])
        constant_load_source.data = dict(x=[], y=[])
        triangular_load_source.data = dict(x=[xr_start, xr_start, xr_end], y=[y_offset+0.2, y_offset+1.2, y_offset+0.2])
    elif new==3: # temperature
        print("Temperature")
        # do coding
    else:
        print("How did you get here?")
        # raise error or something (plot message on screen via bokeh?)




def change_cross_section(attr, old, new):
    if new==0: # constant cross-section
        #rod_source.data = dict(x = np.linspace(xr_start,xr_end,r_reso), y = np.ones(r_reso) * y_offset )
        rod_source.data = dict(x = [xr_start, xr_end], y = [y_offset, y_offset])
    elif new==1: # tapered
        rod_source.data = dict(x=[xr_start, xr_start, xr_end, xr_end], y=[y_offset, y_offset+1, y_offset+0.2, y_offset])

    # TODO: maybe use fill_color, line_width, etc. as variables to change between line and patch



def change_left_support(attr, old, new):
    # new==0 means fixed support image
    # new==1 means slide support image
    new_support_img = fixed_support_img if new==0 else slide_support_img
    support_source_left.data = dict(sp_img=[new_support_img], x=[xsl] , y=[ysl])
    # TODO: check again if it is possible to only change sp_img


def change_right_support(attr, old, new):
    # new==0 means fixed support image
    # new==1 means slide support image
    new_support_img = fixed_support_img if new==0 else slide_support_img
    support_source_right.data = dict(sp_img=[new_support_img], x=[xsr] , y=[ysr])
    # TODO: check again if it is possible to only change sp_img





