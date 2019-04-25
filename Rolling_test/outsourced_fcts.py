import numpy as np


def is_empty(obj):
    if obj:  # returns true in a boolean context if obj has elements inside 
        return False
    else:
        return True



def check_empty_data(fig_data):
    # checks if all fig_datas are empty
    # this is the case if only hollow objects are choosen with radius == inner radius
    # A simulation does not make sense in this case, so disable the start button.
    n = len(fig_data)
    data_is_empty = [False]*n
    for i in range(0,n):
        # unpack the values of the CDS dictionary and 
        # concatenate them via sum(.,[])
        data_is_empty[i] = is_empty(sum(fig_data[i].data.values(),[]))
        
        
    return data_is_empty
        
#    if (all(data_is_empty)):
#        # if all datas are empty (radius == inner radius) disable the start button
#        # simulation cannot be run without any existing object
#        start_button.disabled = True
#    else:
#        # if any of the data is not empty, at least one obejct exists
#        # therefore, enable start button
#        start_button.disabled = False



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



def logical_indexing(arr, arr_ind, val):
    # length arr == length arr_ind
    # arr[arr_ind] = val
    # write val in places in arr where arr_ind is True
    for i in range(len(arr)):
        arr[i] = val if arr_ind[i] else arr[i]
        

def check_availability(fig_data):
    # check if the data of each plot is empty    
    data_is_empty = check_empty_data(fig_data)
    
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
        # if any of the data is not empty, at least one obejct exists
        # therefore, enable start button
        start_button.disabled = False