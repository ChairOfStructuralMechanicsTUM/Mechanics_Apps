from __future__ import division # float division only, like in python 3

## inner app imports
from NFR_constants import (
        xr_start, xr_end, # rod coords
        y_offset,# y_cross,
        xsl, xsr, ysl, ysr, # support coords
        slide_support_img, fixed_support_img # support images
        )
from NFR_data_sources import (
        rod_source, #global_variables,
        support_source_left, support_source_right,
        force_point_source, constant_load_source, triangular_load_source,
        temperature_source,
        labels_source, labels_N, labels_U,
        aux_line, samplesF,
        error_msg, error_msg_frame,
        temp_pics
        )
from NFR_buttons import (
        radio_group_left, radio_group_right, #radio_group_cross,
        radio_group_ampl,
        radio_button_group,
        load_position_slide,
        line_button
        )
from NFR_equations import (
        calcNU
        )



def clear_point_load():
    force_point_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW=[], lC=[])
def clear_constant_load():
    constant_load_source.data = dict(x=[], y=[])
def clear_triangular_load():
    triangular_load_source.data = dict(x=[], y=[])
def clear_temperature():
    temperature_source.data = dict(x=[], y=[])
def clear_labels():
    labels_source.data = dict(x=[], y=[], name=[])
# TODO: check for general CDS clearing    


# TODO: maybe variable for arrow length for more general case?
    

def set_point_load(load_position):
    #y_cross = global_variables["y_cross"]
    labels_source.data = dict(x=[xr_start-0.1+load_position, xr_start-0.05+load_position],y=[y_offset+0.3,y_offset],name=['F','|'])
    force_point_source.data = dict(xS=[xr_start-0.5+load_position], xE=[xr_start+0.5+load_position], yS=[y_offset+0.2], yE=[y_offset+0.2], lW=[2], lC=["#0065BD"])
    clear_constant_load()
    clear_triangular_load()
    clear_temperature()


def set_constant_load(load_position):
    if load_position<1e-5: #close to zero
        clear_constant_load()
        clear_labels()
        clear_point_load()
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
        labels_source.data = dict(x=[load_position+0.1],y=[y_offset+0.2], name=['p'])
        
        force_point_source.data = dict(xS=xS, xE=xE, yS=[y_offset+0.45]*num_arrows, yE=[y_offset+0.45]*num_arrows, lW=[2]*num_arrows, lC=["#0065BD"]*num_arrows)
        
        constant_load_source.data = dict(x=[xr_start, xr_start, load_position, load_position], y=[y_offset+0.2, y_offset+0.7, y_offset+0.7, y_offset+0.2])
        #triangular_load_source.data = dict(x=[], y=[])
    clear_triangular_load()
    clear_temperature()


def set_triangular_load(load_position):
    if load_position<1e-5: #close to zero
        clear_triangular_load()
        clear_labels()
        clear_point_load()
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
        labels_source.data = dict(x=[load_position+0.1],y=[y_offset+0.2], name=['p'])
        force_point_source.data = dict(xS=xS, xE=xE, yS=[y_offset+0.45]*num_arrows, yE=[y_offset+0.45]*num_arrows, lW=[2]*num_arrows, lC=["#0065BD"]*num_arrows)
        triangular_load_source.data = dict(x=[xr_start, xr_start, load_position], y=[y_offset+0.2, y_offset+0.7, y_offset+0.2])
    clear_constant_load()
    clear_temperature()


def set_temperature(load_position):
    if load_position<1e-5: #close to zero
        clear_temperature()
        clear_labels()
    else:
        #y_cross = global_variables["y_cross"]
        
        labels_source.data = dict(x=[(load_position-xr_start)/2],y=[y_offset+0.35], name=['T'])
        temperature_source.data = dict(x=[xr_start, xr_start, load_position, load_position], y=[y_offset+0.2, y_offset+0.7, y_offset+0.7, y_offset+0.2])
        #TODO: nice design for Temperature (hot/cold)
    clear_point_load()
    clear_constant_load()
    clear_triangular_load()
    
    #"Normal_Force_Rod/static/images/snowflake01.svg"
    xC = [1.2, 4.8, 7.1]
    yC = [0.0, 0.0, 0.0]
    temp_pics.data = dict(x=xC, y=yC, img=["Normal_Force_Rod/static/images/snowflake03.svg"]*3)
    #TODO: find the reason why the pictures don't show...
    
    



def set_load(load_type, load_position):
    if load_type==0:
        set_point_load(load_position)
    elif load_type==1:
        set_constant_load(load_position)
    elif load_type==2:
        set_triangular_load(load_position)
    elif load_type==3:
        set_temperature(load_position)
    else:
        print("How did you get here? [helper_functions, set_load]")
    
    
    #TODO: consider re-structuring with function handles like in rolling test
    # advantage: calling the functions via list index instead of if-else




def move_aux_line():
    x_samples = samplesF.data['x']
    y_samples = samplesF.data['y']
    roots     = []
    
    for i in range(0,len(y_samples)-1):
        if y_samples[i]*y_samples[i+1] < 0: # sign changes
            r = 0.5*(x_samples[i+1]-x_samples[i]) + x_samples[i]
            roots.append([r,r])
    
    aux_line.data = dict(x=roots, y=[[15,-15]]*len(roots))



def show_error(show=True):
    
    if show:
        error_msg.data = dict(x=[2],y=[1.35],name=["Warning! - Kinematic, rod slides away!"])
        error_msg_frame.data = dict(x=[5], y=[1.5])
    else:
        error_msg.data = dict(x=[], y=[], name=[])
        error_msg_frame.data = dict(x=[], y=[])



def compute_new_scenario():
    ls_type   = radio_group_left.active
    rs_type   = radio_group_right.active
    load_type = radio_button_group.active
    L1        = load_position_slide.value
    calcNU(ls_type, rs_type, load_type, L1)
    show_special_values()
    # if the auxiliary line should be shown, the line button shows "Hide line"
    if line_button.label == "Hide line":
        move_aux_line()


def show_special_values(): #labels
    # show only for fixed-fixed scenario
    if (radio_group_left.active == 0 and radio_group_right.active == 0):
        load_type = radio_button_group.active
        
        # for constant and triangular load only for Load Poistion == L
        if (load_position_slide.value == xr_end):
            if load_type==1: # constant load
                labels_N.data = dict(x=[0.0,10.0], y=[2.0,-2.0], name=['N', 'N'])
                labels_U.data = dict(x=[5.0], y=[10.0], name=['U'])
            elif load_type==2: # triangular load
                labels_N.data = dict(x=[0.0,10.0], y=[2.0,-2.0], name=['N', 'N'])
                labels_U.data = dict(x=[6.0], y=[8.0], name=['U'])
        
        # for point load only for Load Position = L/2
        elif (load_position_slide.value == (xr_end-xr_start)//2):
            if load_type==0: # point load
                labels_N.data = dict(x=[0.0,10.0], y=[2.0,-2.0], name=['N', 'N'])
                labels_U.data = dict(x=[5.0], y=[-5.0], name=['U'])
        else:
            labels_N.data = dict(x=[], y=[], name=[])
            labels_U.data = dict(x=[], y=[], name=[])
            
    else:
        labels_N.data = dict(x=[], y=[], name=[])
        labels_U.data = dict(x=[], y=[], name=[])
        #TODO: clear by function 


#labels_N.data = dict(x=[0.0,10.0], y=[2.0,2.0], name=['N', 'N'])
#labels_U.data = dict(x=[5.0], y=[-5.0], name=['U'])






