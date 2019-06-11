from __future__ import division # float division only, like in python 3
import numpy as np

from RT_global_variables import (
        rampLength, g, max_samples,
        t_end, glob_time,
        fig_data, fig_lines_data, fig_values, fig_samples,
        fig_in_use, fig_objects,
        glob_fun_handles
        )
from RT_buttons import (
        start_button, mode_selection,
        object_select0, object_select1, object_select2,
        radius_slider0, radius_slider1, radius_slider2,
        ri_slider0, ri_slider1, ri_slider2,
        alpha_slider0, alpha_slider1, alpha_slider2
        )
from RT_object_movement import (
        moveSphere,
        moveCylinder, moveHollowCylinder
        )


###############################################################################
###                            helper functions                             ###
###############################################################################
def is_empty(obj):
    if obj:  # returns true in a boolean context if obj has elements inside 
        return False
    else:
        return True

def logical_indexing(arr, arr_ind, val):
    # requirement: length arr == length arr_ind
    # simulates:   arr[arr_ind] = val
    # write val in places in arr where arr_ind is True
    for i in range(len(arr)):
        arr[i] = val if arr_ind[i] else arr[i]
        
###############################################################################
###                 new coordinates from each move function                 ###
###############################################################################
def get_coordinates(fun_handles, in_execution, t):
    # Input:  - list of function handles, size n
    #         - list of bool values if function is still in execution, size n
    #         - time t to evaluate the function on
    # Output: - list of x- and y-coordinates, size 2xn
    x_coords = np.zeros(len(fun_handles))
    y_coords = x_coords.copy()
    for j, handle in enumerate(fun_handles):
        if in_execution[j]:
            (x_coords[j], y_coords[j]) = handle(t)
        else:
            (x_coords[j], y_coords[j]) = (-50,50)
    return (x_coords, y_coords)


###############################################################################
###                           build time samples                            ###
###############################################################################
def get_t_end(FIG,new_object):
    # calculate the end time when the object hits the end of the ramp
    load_vals = ["SIN", "r", "ri"]
    SIN, r, ri = [fig_values[FIG].get(val) for val in load_vals]
    #SIN   = fig_values[FIG]["SIN"]
    #r     = fig_values[FIG]["r"]
    #ri    = fig_values[FIG]["ri"]
    # ATTENTION: setting ri/r = 0 in case of r==ri is unphysical! 
    # but it won't get shown in the app, the object vanishes
    # however, calculations are expected
    ratio = ri/r if (abs(r-ri)>1e-5) else 0
    if (new_object == "Sphere"):
        t_end[FIG] = np.sqrt(14.0*rampLength/(5.0*g*SIN))
    elif (new_object == "Hollow cylinder"):
        z = 3.0 + ratio*ratio
        t_end[FIG] = np.sqrt(z*rampLength/(g*SIN))
    elif (new_object == "Hollow sphere"):
        k = 1.0 + 0.4*(1.0 - ratio**5)/(1.0 - ratio**3)
        t_end[FIG] = np.sqrt(2.0*k*rampLength/(g*SIN)) 
    else: # cylinder
        t_end[FIG] = np.sqrt(3.0*rampLength/(g*SIN))


def get_t_samples(FIG,new_object):
    # upate the time samples based on the maximum end time
    get_t_end(FIG,new_object)
    glob_time["t_samples"] = np.linspace(0.0,max(t_end),max_samples, endpoint=True)
    get_fig_samples() # only if max(t_end) changes -> var t_max_old to avoid call?


def get_fig_samples():
    t_samples = glob_time["t_samples"] # input/
    load_vals = ["SIN", "r", "ri"]
    for FIG in range(0,3):
        SIN, r, ri = [fig_values[FIG].get(val) for val in load_vals]
        ratio = ri/r if (abs(r-ri)>1e-5) else 0
        if (fig_objects[FIG] == "Sphere"):
            fig_samples[FIG] = 5./14*g*SIN*t_samples*t_samples
        elif (fig_objects[FIG] == "Hollow cylinder"):
            #ratio = ri/r
            z = 3.0 + ratio*ratio
            fig_samples[FIG] =  (g/z)*SIN*t_samples*t_samples
        elif (fig_objects[FIG] == "Hollow sphere"):
            #ratio = ri/r
            k = 1.0 + 0.4*(1.0 - ratio**5)/(1.0 - ratio**3)
            
            fig_samples[FIG] =  0.5*(g/k)*SIN*t_samples*t_samples
        else: # cylinder
            fig_samples[FIG] =  (g/3.0)*SIN*t_samples*t_samples


###############################################################################
###                    simulation status (running/done)                     ###
###############################################################################
def check_availability():
    # check if all fig_datas are empty (data of each plot)
    # this is the case if only hollow objects are chosen with radius == inner radius
    # A simulation does not make sense in this case, so disable the start button.
    n = len(fig_data)
    data_is_empty = [False]*n
    for i in range(0,n):
        # unpack the values of the CDS dictionary and 
        # concatenate them via sum(.,[])
        data_is_empty[i] = is_empty(sum(fig_data[i].data.values(),[]))
    
    # simulations can be ended for figures where radius == inner radius
    # fig_in_use[data_is_empty] = False
    logical_indexing(fig_in_use,data_is_empty,False)
    # the same for the complementary data_is_empty list if we change back the slider
    logical_indexing(fig_in_use,[not i for i in data_is_empty],True)
    
    if (all(data_is_empty)):
        # if all datas are empty (radius == inner radius) disable the start button
        # simulation cannot be run without any existing object
        start_button.disabled = True
    else:
        # if any of the data is not empty, at least one object exists
        # therefore, enable start button
        start_button.disabled = False


###############################################################################
###                 control slider and widget availability                  ###
###############################################################################
def disable_all_sliders(d=True):
    object_select0.disabled = d
    object_select1.disabled = d
    object_select2.disabled = d
    radius_slider0.disabled = d
    radius_slider1.disabled = d
    radius_slider2.disabled = d
    ri_slider0.disabled     = d
    ri_slider1.disabled     = d
    ri_slider2.disabled     = d
    alpha_slider0.disabled  = d
    alpha_slider1.disabled  = d
    alpha_slider2.disabled  = d
    mode_selection.disabled = d
        
        
###############################################################################
###                        initial function handles                         ###
############################################################################### 
# name the functions to be used by each figure depending upon their content
glob_fun_handles[0]=lambda(x):moveSphere(0,x,fig_data[0],fig_lines_data[0],fig_values[0])
glob_fun_handles[1]=lambda(x):moveCylinder(1,x,fig_data[1],fig_lines_data[1],fig_values[1])
glob_fun_handles[2]=lambda(x):moveHollowCylinder(2,x,fig_data[2],fig_lines_data[2],fig_values[2])