from __future__ import division # float division only, like in python 3


import numpy as np

from NFR_constants import (
        xr_start, y_offset,
        lb, ub,
        xr_end, sol_reso
        )

from NFR_equations import calcNU


def clear_point_load():
    return dict(xS=[], xE=[], yS=[], yE=[])
def clear_constant_load():
    return dict(x=[], y=[])
def clear_triangular_load():
    return dict(x=[], y=[])
def clear_temperature():
    return dict(x=[], y=[])
def clear_labels():
    return dict(x=[], y=[], name=[])


# TODO: maybe variable for arrow length for more general case?
    

def set_point_load(load_position, load_output):
    #y_cross = global_variables["y_cross"]
    # labels
    load_output[4] = dict(x=[xr_start-0.1+load_position, xr_start-0.05+load_position],y=[y_offset+0.3,y_offset],name=['F','|'])
    
    load_output[0] = dict(xS=[xr_start-0.5+load_position], xE=[xr_start+0.5+load_position], yS=[y_offset+0.2], yE=[y_offset+0.2])
    
    load_output[1] = clear_constant_load()
    load_output[2] = clear_triangular_load()
    load_output[3] = clear_temperature()

#def set_constant_load(load_position, load_output):
#    #y_cross = global_variables["y_cross"]
#    #labels_source.data = dict(x=[xr_start-0.1+load_position, xr_start-0.05+load_position],y=[y_offset+0.3,y_offset],name=['F','|'])
#    
#    #load_output[0] = dict(xS=[xr_start-0.5+load_position], xE=[xr_start+0.5+load_position], yS=[y_offset+0.2], yE=[y_offset+0.2], lW=[2], lC=["#0065BD"])
#    load_output[0] = clear_point_load()
#    load_output[1] = clear_constant_load()
#    load_output[2] = clear_triangular_load()
#    load_output[3] = clear_temperature()
    
    
def set_constant_load(load_position, load_output):
    if load_position<1e-5: #close to zero
        load_output[1] = clear_constant_load()
        load_output[4] = clear_labels()
        load_output[0] = clear_point_load()
    else:
        #labels_source.data = dict(x=[xr_start+1.5,xr_start+4.5,xr_start+7.5],y=[y_offset+0.9,y_offset+0.9,y_offset+0.9],name=['F','F','F'])
        #y_cross = global_variables["y_cross"]
        
        xS = []
        xE = []
        #xM = []
        # calculate the coordinats for the arrows and labels
        num_arrows = 3 # amount of arrows
        part = (load_position-xr_start)/(num_arrows*2+1)
        local_index = list(range(1,num_arrows*2+1))
        # arrow start positions (odd)
        for i in local_index[::2]:
            xS.append(part*i)
            #xM.append(part*(i+0.5))
        for i in local_index[1:][::2]:
            xE.append(part*i)
        
        #labels_source.data = dict(x=xM,y=[y_offset+0.9,y_offset+0.9,y_offset+0.9],name=['F']*num_arrows)
        load_output[4] = dict(x=[load_position+0.1],y=[y_offset+0.2], name=['p'])
        
        load_output[0] = dict(xS=xS, xE=xE, yS=[y_offset+0.45]*num_arrows, yE=[y_offset+0.45]*num_arrows)#, lW=[2]*num_arrows, lC=["#0065BD"]*num_arrows)
        
        load_output[1] = dict(x=[xr_start, xr_start, load_position, load_position], y=[y_offset+lb, y_offset+ub, y_offset+ub, y_offset+lb])
        #triangular_load_source.data = dict(x=[], y=[])
    load_output[2] = clear_triangular_load()
    load_output[3] = clear_temperature()



def set_triangular_load(load_position, load_output):
    if load_position<1e-5: #close to zero
        load_output[2] = clear_triangular_load()
        load_output[4] = clear_labels()
        load_output[0] = clear_point_load()
    else:
        #y_cross = global_variables["y_cross"]
        
        xS = []
        xE = []
        # calculate the coordinats for the arrows and labels
        num_arrows = 2 # amount of arrows
        part = 0.5*(load_position-xr_start)/(num_arrows*2+1)
        local_index = list(range(1,num_arrows*2+1))
        # arrow start positions (odd)
        for i in local_index[::2]:
            xS.append(part*i)
            #xM.append(part*(i+0.5))
        for i in local_index[1:][::2]:
            xE.append(part*i)
        load_output[4] = dict(x=[load_position+0.1],y=[y_offset+0.2], name=['p'])
        load_output[0] = dict(xS=xS, xE=xE, yS=[y_offset+0.45]*num_arrows, yE=[y_offset+0.45]*num_arrows)
        load_output[2] =  dict(x=[xr_start, xr_start, load_position], y=[y_offset+lb, y_offset+ub, y_offset+lb])
    load_output[1] = clear_constant_load()
    load_output[3] = clear_temperature()
    


def set_temperature(load_position, load_output):
    if load_position<1e-5: #close to zero
        load_output[3] = clear_temperature()
        load_output[4] = clear_labels()
    else:
        #y_cross = global_variables["y_cross"]
        
        load_output[4] = dict(x=[(load_position-xr_start)/2],y=[y_offset+0.35], name=['T'])
        load_output[3] = dict(x=[xr_start, xr_start, load_position, load_position], y=[y_offset+lb, y_offset+ub, y_offset+ub, y_offset+lb])
        #TODO: nice design for Temperature (hot/cold)
    load_output[0] = clear_point_load()
    load_output[1] = clear_constant_load()
    load_output[2] = clear_triangular_load()
    
    #"Normal_Force_Rod/static/images/snowflake01.svg"
    #xC = [1.2, 4.8, 7.1]
    #yC = [0.0, 0.0, 0.0]
    #temp_pics.data = dict(x=xC, y=yC, img=["Normal_Force_Rod/static/images/snowflake03.svg"]*3)
    #TODO: find the reason why the pictures don't show...



    
    
def set_load(load_type, load_position, obj_list):
    load_output = [dict()]*(4+1)  # num of load types + labels
    # empty dict is not enough, the variables in the CDS have to be set empty
    # => load_ouput has to be filled by the specific functions
    if load_type==0:
        #load_output[0] = set_point_load(load_position)
        set_point_load(load_position, load_output)
    elif load_type==1:
        set_constant_load(load_position, load_output)
    elif load_type==2:
        set_triangular_load(load_position, load_output)
    elif load_type==3:
        set_temperature(load_position, load_output)
    else:
        print("How did you get here? [helper_functions, set_load]")
    #return load_output
    
    for i, obj in enumerate(obj_list):
        obj.shape.data = load_output[i]
    




def refresh_objects(obj_list,fig):
    # give list of objects and loop over it to draw them
    for obj in obj_list:
        obj.draw(fig)





def compute_new_scenario(GUI, graph_obj_N, graph_obj_U):
    ls_type   = GUI.radio_group_left.active
    rs_type   = GUI.radio_group_right.active
    load_type = GUI.radio_button_group.active
    L1        = GUI.load_position_slider.value
    #print("DBUG: pos_slider:", L1)
    ampl      = -1 + 2*GUI.radio_group_ampl.active  # ampl=-1 if active=0, ampl=1 if active=1
    #print("DBUG: ampl:", ampl)
    #samples   = calcNU(ls_type, rs_type, load_type, L1, graph_obj_N.shape.data['x'], ampl)
    #x_samples = np.linspace(xr_start,xr_end,sol_reso)
    #samples   = calcNU(ls_type, rs_type, load_type, L1, x_samples, ampl)
    samples   = calcNU(ls_type, rs_type, load_type, L1, ampl)
#    graph_obj_N.shape.data['x'] = samples['x']
#    graph_obj_N.shape.data['y'] = samples['yN']
#    graph_obj_U.shape.data['x'] = samples['x']
#    graph_obj_U.shape.data['y'] = samples['yU']
    graph_obj_N.shape.data = dict(x=samples['x'], y=samples['yN'])
    graph_obj_U.shape.data = dict(x=samples['x'], y=samples['yU'])
    
    print("in comp...")
    print("DBUG: yN=",samples['yN'])
    print("DBUG: yU=",samples['yU'])
    print("DBUG: CDSyN=",graph_obj_N.shape.data['y'])
    print("DBUG: CDSyU=",graph_obj_U.shape.data['y'])
    print("comp fertig...")
#    show_special_values()
#    # if the auxiliary line should be shown, the line button shows "Hide line"
#    if line_button.label == "Hide line":
#        move_aux_line()








    
    