from __future__ import division # float division only, like in python 3
import numpy as np

from RT_global_variables import (
        rampLength, g, max_samples,
        t_end, glob_time, 
        fig_values, fig_samples,
        fig_in_use, fig_objects
        )

# using a mixin class for RT_callback_functions
class helper_fcts:
    ###############################################################################
    ###                            helper functions                             ###
    ###############################################################################
    def is_empty(self,obj):
        if obj:  # returns true in a boolean context if obj has elements inside 
            return False
        else:
            return True
    
    def logical_indexing(self,arr, arr_ind, val):
        # requirement: length arr == length arr_ind
        # simulates:   arr[arr_ind] = val
        # write val in places in arr where arr_ind is True
        for i in range(len(arr)):
            arr[i] = val if arr_ind[i] else arr[i]
            
    ###############################################################################
    ###                 new coordinates from each move function                 ###
    ###############################################################################
    def get_coordinates(self,fun_handles, in_execution, t):
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
    def get_t_end(self,FIG):
        # calculate the end time when the object hits the end of the ramp
        load_vals = ["SIN", "r", "ri"]
        SIN, r, ri = [fig_values[FIG].get(val) for val in load_vals]
        
        # ATTENTION: setting ri/r = 0 in case of r==ri is unphysical! 
        # but it won't get shown in the app, the object vanishes
        # however, calculations are expected
        ratio = ri/r if (abs(r-ri)>1e-5) else 0
        if (fig_objects[FIG] == "Sphere"):
            t_end[FIG] = np.sqrt(14.0*rampLength/(5.0*g*SIN))
        elif (fig_objects[FIG] == "Hollow cylinder"):
            z = 3.0 + ratio*ratio
            t_end[FIG] = np.sqrt(z*rampLength/(g*SIN))
        elif (fig_objects[FIG] == "Hollow sphere"):
            k = 1.0 + 0.4*(1.0 - ratio**5)/(1.0 - ratio**3)
            t_end[FIG] = np.sqrt(2.0*k*rampLength/(g*SIN)) 
        else: # cylinder
            t_end[FIG] = np.sqrt(3.0*rampLength/(g*SIN))
    
    
    def get_t_samples(self,FIG):
        # upate the time samples based on the maximum end time
        self.get_t_end(FIG)
        glob_time["t_samples"] = np.linspace(0.0,max(t_end),max_samples, endpoint=True)
        # also update all displacement values
        self.get_fig_samples()
    
    
    def get_fig_samples(self):
        t_samples = glob_time["t_samples"] # input/
        load_vals = ["SIN", "r", "ri"]
        for FIG in range(0,3):
            SIN, r, ri = [fig_values[FIG].get(val) for val in load_vals]
            ratio = ri/r if (abs(r-ri)>1e-5) else 0
            if (fig_objects[FIG] == "Sphere"):
                fig_samples[FIG] = 5./14*g*SIN*t_samples*t_samples
            elif (fig_objects[FIG] == "Hollow cylinder"):
                z = 3.0 + ratio*ratio
                fig_samples[FIG] =  (g/z)*SIN*t_samples*t_samples
            elif (fig_objects[FIG] == "Hollow sphere"):
                k = 1.0 + 0.4*(1.0 - ratio**5)/(1.0 - ratio**3)            
                fig_samples[FIG] =  0.5*(g/k)*SIN*t_samples*t_samples
            else: # cylinder
                fig_samples[FIG] =  (g/3.0)*SIN*t_samples*t_samples
    
    
    ###############################################################################
    ###                    simulation status (running/done)                     ###
    ###############################################################################
    def check_availability(self,fig_data):
        # check if all fig_datas are empty (data of each plot)
        # this is the case if only hollow objects are chosen with radius == inner radius
        # A simulation does not make sense in this case, so disable the start button.
        n = len(fig_data)
        data_is_empty = [False]*n
        for i in range(0,n):
            # unpack the values of the CDS dictionary and 
            # concatenate them via sum(.,[])
            data_is_empty[i] = self.is_empty(sum(fig_data[i].data.values(),[]))
        
        # simulations can be stopped for figures where radius == inner radius
        # fig_in_use[data_is_empty] = False # in logical indexing format
        self.logical_indexing(fig_in_use,data_is_empty,False)
        # the same for the complementary data_is_empty list if we change back the slider
        self.logical_indexing(fig_in_use,[not i for i in data_is_empty],True)
        
        if (all(data_is_empty)):
            # if all datas are empty (radius == inner radius) disable the start button
            # simulation cannot be run without any existing object
            self.my_sources.start_button.disabled = True
        else:
            # if any of the data is not empty, at least one object exists
            # therefore, enable start button
            self.my_sources.start_button.disabled = False
    
    
    ###############################################################################
    ###                 control slider and widget availability                  ###
    ###############################################################################
    def disable_all_sliders(self,d=True):
        self.my_sources.object_select0.disabled = d
        self.my_sources.object_select1.disabled = d
        self.my_sources.object_select2.disabled = d
        self.my_sources.radius_slider0.disabled = d
        self.my_sources.radius_slider1.disabled = d
        self.my_sources.radius_slider2.disabled = d
        self.my_sources.ri_slider0.disabled     = d
        self.my_sources.ri_slider1.disabled     = d
        self.my_sources.ri_slider2.disabled     = d
        self.my_sources.alpha_slider0.disabled  = d
        self.my_sources.alpha_slider1.disabled  = d
        self.my_sources.alpha_slider2.disabled  = d
        self.my_sources.mode_selection.disabled = d
        
        