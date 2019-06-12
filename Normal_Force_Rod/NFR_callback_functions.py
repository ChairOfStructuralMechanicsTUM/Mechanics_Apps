from __future__ import division # float division only, like in python 3

## inner app imports
from NFR_constants import (
        xr_start, xr_end, y_offset, # rod coords
        xsl, xsr, ysl, ysr, # support coords
        slide_support_img, fixed_support_img # support images
        )
from NFR_data_sources import (
        rod_source, global_variables,
        support_source_left, support_source_right,
        force_point_source, constant_load_source, triangular_load_source,
        labels_source,
        aux_line
        )
from NFR_buttons import (
        radio_group_left, radio_group_right, #radio_group_cross,
        radio_group_ampl,
        radio_button_group,
        load_position_slide, 
        line_button
        )
from NFR_helper_functions import (
        set_load, set_point_load, set_constant_load, show_error,
        compute_new_scenario, move_aux_line
        )





def change_load(attr, old, new):
    print("DEBUG: change_load, new=",new)
    
    current_position = load_position_slide.value
    
    set_load(new,current_position)
    compute_new_scenario()
    


def change_load_position(attr, old, new):
    
    # have to handle distinct cases, otherwise there are ValueErrors for empty lists
    new_position = new*10/(xr_end-xr_start)
    
    current_load = radio_button_group.active
    
    set_load(current_load,new_position)
    
    compute_new_scenario()
    
    



#def change_cross_section(attr, old, new):
#    if new==0: # constant cross-section
#        #rod_source.data = dict(x = np.linspace(xr_start,xr_end,r_reso), y = np.ones(r_reso) * y_offset )
#        #rod_source.data = dict(x = [xr_start, xr_end], y = [y_offset, y_offset])
#        rod_source.data = dict(x=[xr_start, xr_start, xr_end, xr_end], y=[y_offset-0.1, y_offset+0.1, y_offset+0.1, y_offset-0.1])
#        global_variables["y_cross"] = 0.0
#        set_load(radio_button_group.active,load_position_slide.value)
#    elif new==1: # tapered
#        rod_source.data = dict(x=[xr_start, xr_start, xr_end, xr_end], y=[y_offset-0.1, y_offset+0.4, y_offset+0.1, y_offset-0.1])
##        global_variables["rod_line_width"] = 20
#        global_variables["y_cross"] = 0.5
#        set_load(radio_button_group.active,load_position_slide.value)

    # TODO: maybe use fill_color, line_width, etc. as variables to change between line and patch



def change_left_support(attr, old, new):
    # new==0 means fixed support image
    # new==1 means slide support image
    new_support_img = fixed_support_img if new==0 else slide_support_img
    support_source_left.data = dict(sp_img=[new_support_img], x=[xsl] , y=[ysl])
    # TODO: check again if it is possible to only change sp_img
    
    if radio_group_right.active==1 and new==1: # both slide
        show_error(True)
    else:
        show_error(False)
        
    compute_new_scenario()


def change_right_support(attr, old, new):
    # new==0 means fixed support image
    # new==1 means slide support image
    new_support_img = fixed_support_img if new==0 else slide_support_img
    support_source_right.data = dict(sp_img=[new_support_img], x=[xsr] , y=[ysr])
    # TODO: check again if it is possible to only change sp_img
    
    if radio_group_left.active==1 and new==1: # both slide
        show_error(True)
    else:
        show_error(False)
        
    compute_new_scenario()




def change_amplitude(attr, old, new):
    xS_old = force_point_source.data["xS"]
    xE_old = force_point_source.data["xE"]
    
    # change direction of arrows in x-direction (parallel to rod)
    force_point_source.data["xS"] = xE_old
    force_point_source.data["xE"] = xS_old
    
    # change sign for the calculations
    global_variables["ampl"] = -global_variables["ampl"]
    
    compute_new_scenario()
    


def reset():
    radio_button_group.active = 0
    radio_group_left.active   = 0
    radio_group_right.active  = 1
    #radio_group_cross.active  = 0
    radio_group_ampl.active   = 1
    load_position_slide.value = (xr_end-xr_start)/2
    set_load(radio_button_group.active,load_position_slide.value)
    compute_new_scenario()


def change_line_visibility():
    if line_button.label == "Show line":
        move_aux_line()
        line_button.label = "Hide line"
    elif line_button.label == "Hide line":
        aux_line.data = dict(x=[], y=[])
        line_button.label = "Show line"






