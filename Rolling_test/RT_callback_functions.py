from __future__ import division # float division only, like in python 3
from bokeh.io import curdoc
from math import sin, cos, radians
import numpy as np

from RT_global_variables import (
        fig_data, fig_lines_data,
        fig_in_use,
        figure_list,
        time_display,
        glob_values, glob_callback_id,
        wall_source, ramp_source, AngleMarkerSource,
        glob_fun_handles,
        rampLength, rampAddLength
        )
from RT_buttons import (
        start_button, reset_button, mode_selection,
        object_select0, object_select1, object_select2,
        radius_slider0, radius_slider1, radius_slider2,
        ri_slider0, ri_slider1, ri_slider2
        )
from RT_helper_functions import check_availability, get_coordinates, disable_all_sliders
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
# function to change the shape, radius, or mass of the object in figure FIG
# only indirectly a callback function
def changeObject(FIG,new_object,r,ri,m):
    # save the data concerned in data and line_data
    data      = fig_data[FIG]
    line_data = fig_lines_data[FIG]
    # depending on the shape specified, create the object and
    # save the new evolution function in the variable func
    if (new_object == "Sphere"):
        createSphere(r,data,line_data)
        func=lambda(x):moveSphere(x,r,m,data,line_data)
    elif (new_object =="Hollow cylinder"):
        createHollowCylinder(r,ri,data,line_data)
        func=lambda(x):moveHollowCylinder(x,r,m,ri,data,line_data)
    elif (new_object == "Hollow sphere"):
        createHollowSphere(r,ri,data,line_data)
        func=lambda(x):moveHollowSphere(x,r,m,ri,data,line_data)
    else:
        createCylinder(r,data,line_data)
        func=lambda(x):moveCylinder(x,r,m,data,line_data)
    
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
    changeObject(0,new,radius_slider0.value,ri_slider0.value,1.0)

def changeObject1(attr,old,new):
    changeObject(1,new,radius_slider1.value,ri_slider1.value,1.0)

def changeObject2(attr,old,new):
    changeObject(2,new,radius_slider2.value,ri_slider2.value,1.0)

###############################################################################
###                     functions to change the radius                      ###
###############################################################################
def changeRadius0(attr,old,new):
    changeObject(0,object_select0.value,new,ri_slider0.value,1.0)
    ri_slider0.end = new
    ri_slider0.value = min(ri_slider0.value,new)

def changeRadius1(attr,old,new):
    changeObject(1,object_select1.value,new,ri_slider1.value,1.0)
    ri_slider1.end = new
    ri_slider1.value = min(ri_slider0.value,new)

def changeRadius2(attr,old,new):
    changeObject(2,object_select2.value,new,ri_slider2.value,1.0)
    ri_slider2.end = new
    ri_slider2.value = min(ri_slider2.value,new)

###############################################################################
###          functions to change the inner radius  / wall thickness         ###
###############################################################################
def changeWall0(attr,old,new):
    changeObject(0,object_select0.value,radius_slider0.value,new,1.0)
    
def changeWall1(attr,old,new):
    changeObject(1,object_select1.value,radius_slider1.value,new,1.0)
    
def changeWall2(attr,old,new):
    changeObject(2,object_select2.value,radius_slider2.value,new,1.0)


###############################################################################
###                      slider function for the angle                      ###
###############################################################################
def changeAlpha(attr,old,new):
    alpha=radians(new)
    X=[]
    Y=[]
    for i in range(0,11):
        X.append(-3*cos(i*alpha/10.0))
        Y.append(3*sin(i*alpha/10.0))
    AngleMarkerSource.data=dict(x=X,y=Y)
    COS    = cos(alpha)
    SIN    = sin(alpha)
    offset = -rampLength*COS
    H      = rampLength*SIN
    glob_values.update(dict(alpha=alpha, SIN=SIN, COS=COS, offset=offset, H=H)) #      /output
    ramp_source.data = dict(x=[offset-rampAddLength*COS,0],y=[H+rampAddLength*SIN,0])
    wall_source.data = dict(x=[offset-rampAddLength*COS,offset-rampAddLength*COS],y=[H+rampAddLength*SIN,0])
    reset()
    

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
    glob_values["t"] = 0.0 #      /output
    changeObject(0,object_select0.value,radius_slider0.value,ri_slider0.value,1.0)
    changeObject(1,object_select1.value,radius_slider1.value,ri_slider1.value,1.0)
    changeObject(2,object_select2.value,radius_slider2.value,ri_slider2.value,1.0)
    disable_all_sliders(False)
    time_display[0].data=dict(x=[],y=[],t=[])
    time_display[1].data=dict(x=[],y=[],t=[])
    time_display[2].data=dict(x=[],y=[],t=[])
    check_availability()
          

###############################################################################
###                          evolve one iteration                           ###
###############################################################################
def evolve():
    t = glob_values["t"] # input/output
    t+=0.01
    glob_values["t"] = t
    
    # call all necessary functions
    # get new coordinates of objects which are still running
    (x_coords,y_coords) = get_coordinates(glob_fun_handles, fig_in_use, t)
    
    # if an object has reached the end of the ramp then stop the simulation
    ind_x_max = np.argmax(x_coords)
    ind_y_max = np.argmax(y_coords)
    if (x_coords[ind_x_max]>0 or y_coords[ind_y_max]<0):
        # in mode "one" (active==0) the simulation is stopped after one of the objects reached the end of the ramp
        # in mode "all" (active==1) the simulation is stopped after all objects reached the end of the ramp 
        #               -> (only one fig in use anymore at ending time, one "True" <==> sum==1))
        # mode "one" is selected -> run until one simulation is finished
        # mode "all" is selected -> run all simulations till the end
        if (mode_selection.active==0 or sum(fig_in_use)<=1):
            start() #equals to stop if it is running
        
        # get the index (number of the plot) to know which plot finished the simulation
        plot_num = ind_x_max if x_coords[ind_x_max]>0 else ind_y_max
        fig_in_use[plot_num] = False
        # change the corresponding CDS to display the time only in this plot
        time_display[plot_num].data=dict(x=[-10],y=[20],t=[str(glob_values["t"])+" s"])
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
slider_idx = parseInt(caller.match(/\d/g).join("")); //-1; //-1 for starting at 0

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