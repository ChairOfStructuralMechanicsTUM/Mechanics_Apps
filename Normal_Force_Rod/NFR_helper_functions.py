from __future__ import division # float division only, like in python 3


from NFR_constants import (
        xr_start, y_offset
        )


def clear_point_load():
    return dict(xS=[], xE=[], yS=[], yE=[])
def clear_constant_load():
    return dict(x=[], y=[])
def clear_triangular_load():
    return dict(x=[], y=[])
def clear_temperature():
    return dict(x=[], y=[])
#def clear_labels():
#    labels_source.data = dict(x=[], y=[], name=[])


# TODO: maybe variable for arrow length for more general case?
    

def set_point_load(load_position, load_output):
    #y_cross = global_variables["y_cross"]
    #labels_source.data = dict(x=[xr_start-0.1+load_position, xr_start-0.05+load_position],y=[y_offset+0.3,y_offset],name=['F','|'])
    
    load_output[0] = dict(xS=[xr_start-0.5+load_position], xE=[xr_start+0.5+load_position], yS=[y_offset+0.2], yE=[y_offset+0.2])
    
    load_output[1] = clear_constant_load()
    load_output[2] = clear_triangular_load()
    load_output[3] = clear_temperature()

def set_constant_load(load_position, load_output):
    #y_cross = global_variables["y_cross"]
    #labels_source.data = dict(x=[xr_start-0.1+load_position, xr_start-0.05+load_position],y=[y_offset+0.3,y_offset],name=['F','|'])
    
    #load_output[0] = dict(xS=[xr_start-0.5+load_position], xE=[xr_start+0.5+load_position], yS=[y_offset+0.2], yE=[y_offset+0.2], lW=[2], lC=["#0065BD"])
    load_output[0] = clear_point_load()
    load_output[1] = clear_constant_load()
    load_output[2] = clear_triangular_load()
    load_output[3] = clear_temperature()
    
    
    
def set_load(load_type, load_position):
    load_output = [dict()]*4  # num of load types
    if load_type==0:
        #load_output[0] = set_point_load(load_position)
        set_point_load(load_position, load_output)
    elif load_type==1:
        set_constant_load(load_position, load_output)
#    elif load_type==2:
#        set_triangular_load(load_position)
#    elif load_type==3:
#        set_temperature(load_position)
    else:
        print("How did you get here? [helper_functions, set_load]")
    return load_output




def refresh_object(obj,fig):
    # give list of objects and loop over it
    obj.draw(fig)
    
    
    