from __future__ import division # float division only, like in python 3
from bokeh.io import curdoc
from math import sin, cos, radians
import numpy as np

from RT_global_variables import (
        fig_data, fig_lines_data, fig_values,
        fig_in_use, fig_objects,
        figure_list,
        time_display, icon_display, icons_collection,
        glob_callback_id, glob_time,
        wall_sources, ramp_sources,
        glob_fun_handles,
        rampLength, rampAddLength,
        TX0, TY0, t_end, max_samples, buf
        )
from RT_buttons import (
        start_button, reset_button, mode_selection,
        object_select0, object_select1, object_select2,
        radius_slider0, radius_slider1, radius_slider2,
        ri_slider0, ri_slider1, ri_slider2
        )
from RT_helper_functions import (
        get_t_samples, get_coordinates, 
        disable_all_sliders, check_availability
        )
from RT_object_creation import (
        createSphere, createHollowSphere,
        createCylinder, createHollowCylinder
        )
from RT_object_movement import (
        moveSphere, moveHollowSphere,
        moveCylinder, moveHollowCylinder
        )

###############################################################################
###         main function for changing the appearance of the plots          ###
###############################################################################
# function to change the shape, radius or inner radius of the object in figure FIG
# only indirectly a callback function
def changeObject(FIG,new_object,r,ri):
    # save the new radius and inner radius
    fig_values[FIG]["r"]  = r
    fig_values[FIG]["ri"] = ri
    # relate the object to the correct figure
    fig_objects[FIG] = new_object
    # save the data concerned in data and line_data
    data      = fig_data[FIG]
    line_data = fig_lines_data[FIG]
    vals      = fig_values[FIG]
    
    # update the samples
    get_t_samples(FIG)
    
    # depending on the shape specified, create the object and
    # save the new evolution function in the variable func
    if (new_object == "Sphere"):
        createSphere(data,line_data,vals)
        func=lambda(x):moveSphere(FIG,x,data,line_data,vals)
    elif (new_object == "Hollow cylinder"):
        createHollowCylinder(data,line_data,vals)
        func=lambda(x):moveHollowCylinder(FIG,x,data,line_data,vals)
    elif (new_object == "Hollow sphere"):
        createHollowSphere(data,line_data,vals)
        func=lambda(x):moveHollowSphere(FIG,x,data,line_data,vals)
    else:
        createCylinder(data,line_data,vals)
        func=lambda(x):moveCylinder(FIG,x,data,line_data,vals)
    
    # check the availability of each plot (existing object, still running or finished)
    check_availability()
    
    # save the evolution function to the appropriate function handle
    glob_fun_handles[FIG] = func
    figure_list[FIG].title.text=new_object


## slider/widget functions
###############################################################################
###                      functions to change the shape                      ###
###############################################################################
def changeObject0(attr,old,new):
    changeObject(0,new,radius_slider0.value,ri_slider0.value)

def changeObject1(attr,old,new):
    changeObject(1,new,radius_slider1.value,ri_slider1.value)

def changeObject2(attr,old,new):
    changeObject(2,new,radius_slider2.value,ri_slider2.value)

###############################################################################
###                     functions to change the radius                      ###
###############################################################################
def changeRadius0(attr,old,new):
    changeObject(0,object_select0.value,new,ri_slider0.value)
    ri_slider0.end   = new
    ri_slider0.value = min(ri_slider0.value,new)

def changeRadius1(attr,old,new):
    changeObject(1,object_select1.value,new,ri_slider1.value)
    ri_slider1.end   = new
    ri_slider1.value = min(ri_slider1.value,new)

def changeRadius2(attr,old,new):
    changeObject(2,object_select2.value,new,ri_slider2.value)
    ri_slider2.end   = new
    ri_slider2.value = min(ri_slider2.value,new)

###############################################################################
###          functions to change the inner radius  / wall thickness         ###
###############################################################################
def changeWall0(attr,old,new):
    changeObject(0,object_select0.value,radius_slider0.value,new)
    
def changeWall1(attr,old,new):
    changeObject(1,object_select1.value,radius_slider1.value,new)
    
def changeWall2(attr,old,new):
    changeObject(2,object_select2.value,radius_slider2.value,new)

###############################################################################
###                      slider function for the angle                      ###
###############################################################################
def changeAlpha(FIG,new_alpha):
    alpha=radians(new_alpha)
    COS  =  cos(alpha)
    SIN  =  sin(alpha)
    TX1  =  -rampLength*COS
    TY1  =  rampLength*SIN
    fig_values[FIG].update(dict(alpha=alpha, SIN=SIN, COS=COS, TX1=TX1, TY1=TY1)) #      /output
    ramp_sources[FIG].data = dict(x=[TX1-rampAddLength*COS,TX0],y=[TY1+rampAddLength*SIN,TY0])
    wall_sources[FIG].data = dict(x=[TX1-rampAddLength*COS,TX1-rampAddLength*COS],y=[TY1+rampAddLength*SIN,TY0])
    reset()


def changeAlpha0(attr,old,new):
    changeAlpha(0,new)

def changeAlpha1(attr,old,new):
    changeAlpha(1,new)

def changeAlpha2(attr,old,new):
    changeAlpha(2,new)


###############################################################################
###                       start button functionality                        ###
###############################################################################
def start():
    [callback_id] = glob_callback_id.data["callback_id"] # input/output
    # switch the label
    if start_button.label == "Start":
        start_button.label = "Stop"
        reset_button.disabled = True
        # add the call to evolve
        callback_id = curdoc().add_periodic_callback(evolve,50)
        glob_callback_id.data = dict(callback_id = [callback_id])
    elif start_button.label == "Stop":
        start_button.label = "Start"
        reset_button.disabled = False
        # remove the call to evolve
        curdoc().remove_periodic_callback(callback_id)
    # disable sliders during simulation
    disable_all_sliders(True)
    
###############################################################################
###                       reset button functionality                        ###
###############################################################################
def reset():
    glob_time["t"] = 0 #      /output
    changeObject(0,object_select0.value,radius_slider0.value,ri_slider0.value)
    changeObject(1,object_select1.value,radius_slider1.value,ri_slider1.value)
    changeObject(2,object_select2.value,radius_slider2.value,ri_slider2.value)
    disable_all_sliders(False)
    time_display[0].data=dict(x=[],y=[],t=[])
    time_display[1].data=dict(x=[],y=[],t=[])
    time_display[2].data=dict(x=[],y=[],t=[])
    icon_display[0].data=dict(x=[],y=[],img=[])
    icon_display[1].data=dict(x=[],y=[],img=[])
    icon_display[2].data=dict(x=[],y=[],img=[])
    icons_collection[0] = icons_collection[3]
    check_availability()
          

###############################################################################
###                          evolve one iteration                           ###
###############################################################################
def evolve():
    t = glob_time["t"] # input/output
    t += 1
    glob_time["t"] = t
    
    # only in special case if boundary checks below fail
    # if this condition is met, build a bigger buffer like x_coords[i]>=...-buf, buf=1e-8
    # set buf in RT_global_variables.py
    if(t>=max_samples):
        print("WARNING: simulation exceeded maximum number of provided samples")
        print("-- [Possible Fix]: adjust buffer size 'buf' in RT_global_variables.py --")
        start() #equals to stop if it is running
        start_button.disabled = True
        return
    
    # call all necessary functions
    # get new coordinates of objects which are still running
    # set them far from the conditions if the corresponding plot has already stopped
    (x_coords,y_coords) = get_coordinates(glob_fun_handles, fig_in_use, t)
    
    
    ## if an object has reached the end of the ramp then stop the simulation
    
    # create index arrays to see which plots satisfies the stopping criterion
    # we need to compare to the actual center and not the end of the ramp/plot
    # otherwise the same object with greater radius is "further" than the other 
    ind_x_max = [i for i in range(0,len(x_coords)) if x_coords[i]>=TX0+fig_values[i]["r"]*fig_values[i]["SIN"] - buf]
    ind_y_max = [i for i in range(0,len(y_coords)) if y_coords[i]<=TY0+fig_values[i]["r"]*fig_values[i]["COS"] - buf]
    
    # find and sort unique indices to avoid stopping the same plot twice
    max_indices = np.unique(np.concatenate((ind_x_max, ind_y_max)))
    
    # convert to int, because numpy sets it to float64 as default
    max_indices = max_indices.astype(int)
    
    # get corresponding end times
    t_final = np.array(t_end)[max_indices]
    # get the winners positions (len(pos) == len(max_indices))
    [t_final,pos] = np.unique(t_final, return_inverse=True)
    assert(len(pos) == len(max_indices))
    
    # loop through the plots if multiple simulations fulfill the stopping criterions simultaneously
    for idx, plot_num in enumerate(max_indices):
        fig_in_use[plot_num] = False
        # change the corresponding CDS to display the time only in this plot
        time_display[plot_num].data=dict(x=[TX0-10],y=[TY0+20],t=["%5.3f" % t_end[plot_num] + " s"])
        # show the next icon in all plots that finish simultaneously
        icon_display[plot_num].data=dict(x=[TX0-20],y=[TY0+20],img=[icons_collection[pos[idx]]])
    # update the order of winner symbols 
    if len(max_indices)>0 :
        icons_collection[0] = icons_collection[3-int(sum(fig_in_use))]
        
    # in mode "one" (active==0) the simulation is stopped after one of the objects reached the end of the ramp
    # in mode "all" (active==1) the simulation is stopped after all objects reached the end of the ramp 
    if ((len(max_indices)>0 and mode_selection.active==0) or sum(fig_in_use)<1):
        start() #equals to stop if it is running
    
    # if all simulations have finished, disable the start button
    if (not any(fig_in_use)):
        start_button.disabled = True
    

###############################################################################
###                   visability of inner radius sliders                    ###
###############################################################################
# hide inner radius slider if full object is selected
# show inner radius slider if hollow object is selected
object_select_JS = """
choice = cb_obj.value;
caller = cb_obj.name;

// extract the number of the name and convert it to integer
slider_idx = parseInt(caller.match(/\d/g).join(""));

slider_in_question = document.getElementsByClassName("wall_slider")[slider_idx];

// if hollow object is selected, show the slider (get rid of hidden)
if(choice.includes("Hollow")){
        slider_in_question.className=slider_in_question.className.replace(" hidden","");
}
// if full object is selected, check if slider is hidden; if not, hide it
else if(!slider_in_question.className.includes("hidden")){
        slider_in_question.className+=" hidden";
}
"""