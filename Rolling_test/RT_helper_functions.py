from __future__ import division # float devision only, like in python 3
import numpy as np

from RT_global_variables import (
        fig_data, fig_lines_data,
        fig_in_use,
        glob_fun_handles
        )
from RT_buttons import (
        start_button, mode_selection,
        object_select0, object_select1, object_select2,
        radius_slider0, radius_slider1, radius_slider2,
        ri_slider0, ri_slider1, ri_slider2,
        alpha_slider
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
    # length arr == length arr_ind
    # arr[arr_ind] = val
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
    alpha_slider.disabled   = d
    mode_selection.disabled = d
        
        
###############################################################################
###                        initial function handles                         ###
############################################################################### 
# name the functions to be used by each figure depending upon their content
glob_fun_handles[0]=lambda(x):moveSphere(x,2.0,1.0,fig_data[0],fig_lines_data[0])
glob_fun_handles[1]=lambda(x):moveCylinder(x,2.0,1.0,fig_data[1],fig_lines_data[1])
glob_fun_handles[2]=lambda(x):moveHollowCylinder(x,2.0,1.0,1.5,fig_data[2],fig_lines_data[2])