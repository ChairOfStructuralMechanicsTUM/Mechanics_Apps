from __future__ import division # float division only, like in python 3
from bokeh.io import curdoc
from math import sin, cos, radians
import numpy as np

from RT_global_variables import (
        RT_global_variables,
        fig_values,
        fig_in_use, fig_objects,
        figure_list,
        icons_collection,
        glob_callback_id, glob_time,
        glob_fun_handles,
        rampLength, rampAddLength,
        TX0, TY0, t_end, max_samples, buf
        )
from RT_helper_functions import helper_fcts
from RT_object_creation import (
        createSphere, createHollowSphere,
        createCylinder, createHollowCylinder
        )
from RT_object_movement import (
        moveSphere, moveHollowSphere,
        moveCylinder, moveHollowCylinder
        )

                       #mixin class (see RT_helper_functions)
class all_callback_fcts(helper_fcts):
    def __init__(self):
        self.my_sources = RT_global_variables()
        
        ###############################################################################
        ###                   visability of inner radius sliders                    ###
        ###############################################################################
        # hide inner radius slider if full object is selected
        # show inner radius slider if hollow object is selected
        self.object_select_JS = """
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

        ###############################################################################
        ###                        initial function handles                         ###
        ############################################################################### 
        # name the functions to be used by each figure depending upon their content
        glob_fun_handles[0]=lambda x:moveSphere(0,x,self.my_sources.fig_data[0],self.my_sources.fig_lines_data[0],fig_values[0])
        glob_fun_handles[1]=lambda x:moveCylinder(1,x,self.my_sources.fig_data[1],self.my_sources.fig_lines_data[1],fig_values[1])
        glob_fun_handles[2]=lambda x:moveHollowCylinder(2,x,self.my_sources.fig_data[2],self.my_sources.fig_lines_data[2],fig_values[2])
    
    ###############################################################################
    ###         main function for changing the appearance of the plots          ###
    ###############################################################################
    # function to change the shape, radius or inner radius of the object in figure FIG
    # only indirectly a callback function
    def changeObject(self,FIG,new_object,r,ri):
        # save the new radius and inner radius
        fig_values[FIG]["r"]  = r
        fig_values[FIG]["ri"] = ri
        # relate the object to the correct figure
        fig_objects[FIG] = new_object
        # save the data concerned in data and line_data
        data      = self.my_sources.fig_data[FIG]
        line_data = self.my_sources.fig_lines_data[FIG]
        vals      = fig_values[FIG]
        
        # update the samples
        self.get_t_samples(FIG)
        
        # depending on the shape specified, create the object and
        # save the new evolution function in the variable func
        if (new_object == "Sphere"):
            createSphere(data,line_data,vals)
            func=lambda x:moveSphere(FIG,x,data,line_data,vals)
        elif (new_object == "Hollow cylinder"):
            createHollowCylinder(data,line_data,vals)
            func=lambda x:moveHollowCylinder(FIG,x,data,line_data,vals)
        elif (new_object == "Hollow sphere"):
            createHollowSphere(data,line_data,vals)
            func=lambda x:moveHollowSphere(FIG,x,data,line_data,vals)
        else:
            createCylinder(data,line_data,vals)
            func=lambda x:moveCylinder(FIG,x,data,line_data,vals)
        
        # check the availability of each plot (existing object, still running or finished)
        self.check_availability(self.my_sources.fig_data)
        
        # save the evolution function to the appropriate function handle
        glob_fun_handles[FIG] = func
        figure_list[FIG].title.text=new_object
    
    
    ## slider/widget functions
    ###############################################################################
    ###                      functions to change the shape                      ###
    ###############################################################################
    ## change from JavaScript to Pythohn for hide/show
    ## TODO: needs to be restructered!
    def changeObject0(self,attr,old,new):
        self.changeObject(0,new,self.my_sources.radius_slider0.value,self.my_sources.ri_slider0.value)
        if "Hollow" in new:
        #if (new == "Hollow sphere") or (new == "Hollow cylinder"):
        # .visible=True if "Hollow" in new else .visible=False
            self.my_sources.ri_slider0.visible = True
        else:
            self.my_sources.ri_slider0.visible = False
    
    def changeObject1(self,attr,old,new):
        self.changeObject(1,new,self.my_sources.radius_slider1.value,self.my_sources.ri_slider1.value)
        if "Hollow" in new:
            self.my_sources.ri_slider1.visible = True
        else:
            self.my_sources.ri_slider1.visible = False
    
    def changeObject2(self,attr,old,new):
        self.changeObject(2,new,self.my_sources.radius_slider2.value,self.my_sources.ri_slider2.value)
        if "Hollow" in new:
            self.my_sources.ri_slider2.visible = True
        else:
            self.my_sources.ri_slider2.visible = False
    
    ###############################################################################
    ###                     functions to change the radius                      ###
    ###############################################################################
    def changeRadius0(self,attr,old,new):
        self.changeObject(0,self.my_sources.object_select0.value,new,self.my_sources.ri_slider0.value)
        self.my_sources.ri_slider0.end   = new
        self.my_sources.ri_slider0.value = min(self.my_sources.ri_slider0.value,new)
    
    def changeRadius1(self,attr,old,new):
        self.changeObject(1,self.my_sources.object_select1.value,new,self.my_sources.ri_slider1.value)
        self.my_sources.ri_slider1.end   = new
        self.my_sources.ri_slider1.value = min(self.my_sources.ri_slider1.value,new)
    
    def changeRadius2(self,attr,old,new):
        self.changeObject(2,self.my_sources.object_select2.value,new,self.my_sources.ri_slider2.value)
        self.my_sources.ri_slider2.end   = new
        self.my_sources.ri_slider2.value = min(self.my_sources.ri_slider2.value,new)
    
    ###############################################################################
    ###          functions to change the inner radius  / wall thickness         ###
    ###############################################################################
    def changeWall0(self,attr,old,new):
        self.changeObject(0,self.my_sources.object_select0.value,self.my_sources.radius_slider0.value,new)
        
    def changeWall1(self,attr,old,new):
        self.changeObject(1,self.my_sources.object_select1.value,self.my_sources.radius_slider1.value,new)
        
    def changeWall2(self,attr,old,new):
        self.changeObject(2,self.my_sources.object_select2.value,self.my_sources.radius_slider2.value,new)
    
    ###############################################################################
    ###                      slider function for the angle                      ###
    ###############################################################################
    def changeAlpha(self,FIG,new_alpha):
        alpha=radians(new_alpha)
        COS  =  cos(alpha)
        SIN  =  sin(alpha)
        TX1  =  -rampLength*COS
        TY1  =  rampLength*SIN
        fig_values[FIG].update(dict(alpha=alpha, SIN=SIN, COS=COS, TX1=TX1, TY1=TY1)) #      /output
        self.my_sources.ramp_sources[FIG].data = dict(x=[TX1-rampAddLength*COS,TX0],y=[TY1+rampAddLength*SIN,TY0])
        self.my_sources.wall_sources[FIG].data = dict(x=[TX1-rampAddLength*COS,TX1-rampAddLength*COS],y=[TY1+rampAddLength*SIN,TY0])
        self.reset()
    
    
    def changeAlpha0(self,attr,old,new):
        self.changeAlpha(0,new)
    
    def changeAlpha1(self,attr,old,new):
        self.changeAlpha(1,new)
    
    def changeAlpha2(self,attr,old,new):
        self.changeAlpha(2,new)
    
    
    ###############################################################################
    ###                       start button functionality                        ###
    ###############################################################################
    def start(self):
        [callback_id] = glob_callback_id.data["callback_id"] # input/output
        # switch the label
        if self.my_sources.start_button.label == "Start":
            self.my_sources.start_button.label = "Stop"
            self.my_sources.reset_button.disabled = True
            # add the call to evolve
            callback_id = curdoc().add_periodic_callback(self.evolve,50)
            glob_callback_id.data = dict(callback_id = [callback_id])
        elif self.my_sources.start_button.label == "Stop":
            self.my_sources.start_button.label = "Start"
            self.my_sources.reset_button.disabled = False
            # remove the call to evolve
            curdoc().remove_periodic_callback(callback_id)
        # disable sliders during simulation
        self.disable_all_sliders(True)
        
    ###############################################################################
    ###                       reset button functionality                        ###
    ###############################################################################
    def reset(self):
        glob_time["t"] = 0 #      /output
        self.changeObject(0,self.my_sources.object_select0.value,self.my_sources.radius_slider0.value,self.my_sources.ri_slider0.value)
        self.changeObject(1,self.my_sources.object_select1.value,self.my_sources.radius_slider1.value,self.my_sources.ri_slider1.value)
        self.changeObject(2,self.my_sources.object_select2.value,self.my_sources.radius_slider2.value,self.my_sources.ri_slider2.value)
        self.disable_all_sliders(False)
        self.my_sources.time_display[0].data=dict(x=[],y=[],t=[])
        self.my_sources.time_display[1].data=dict(x=[],y=[],t=[])
        self.my_sources.time_display[2].data=dict(x=[],y=[],t=[])
        self.my_sources.icon_display[0].data=dict(x=[],y=[],img=[])
        self.my_sources.icon_display[1].data=dict(x=[],y=[],img=[])
        self.my_sources.icon_display[2].data=dict(x=[],y=[],img=[])
        icons_collection[:] = np.roll(icons_collection,glob_time["num_rolls"])
        glob_time["num_rolls"] = 0
        self.check_availability(self.my_sources.fig_data)
              
    
    ###############################################################################
    ###                          evolve one iteration                           ###
    ###############################################################################
    def evolve(self):
        t = glob_time["t"] # input/output
        t += 1
        glob_time["t"] = t
        
        # only in special case if boundary checks below fail
        # if this condition is met, build a bigger buffer like x_coords[i]>=...-buf, buf=1e-8
        # set buf in RT_global_variables.py
        if(t>=max_samples):
            print("WARNING: simulation exceeded maximum number of provided samples")
            print("-- [Possible Fix]: adjust buffer size 'buf' in RT_global_variables.py --")
            self.start() #equals to stop if it is running
            self.my_sources.start_button.disabled = True
            return
        
        # call all necessary functions
        # get new coordinates of objects which are still running
        # set them far from the conditions if the corresponding plot has already stopped
        (x_coords,y_coords) = self.get_coordinates(glob_fun_handles, fig_in_use, t)
        
        
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
            self.my_sources.time_display[plot_num].data=dict(x=[TX0-10],y=[TY0+20],t=["%5.3f" % t_end[plot_num] + " s"])
            # show the next icon in all plots that finish simultaneously
            self.my_sources.icon_display[plot_num].data=dict(x=[TX0-20],y=[TY0+20],img=[icons_collection[pos[idx]]])
        # update the order of winner symbols 
        if len(max_indices)>0 :
            glob_time["num_rolls"] += len(t_final)
            icons_collection[:] = np.roll(icons_collection,-len(t_final))
            
        # in mode "one" (active==0) the simulation is stopped after one of the objects reached the end of the ramp
        # in mode "all" (active==1) the simulation is stopped after all objects reached the end of the ramp 
        if ((len(max_indices)>0 and self.my_sources.mode_selection.active==0) or sum(fig_in_use)<1):
            self.start() #equals to stop if it is running
        
        # if all simulations have finished, disable the start button
        if (not any(fig_in_use)):
            self.my_sources.start_button.disabled = True
        