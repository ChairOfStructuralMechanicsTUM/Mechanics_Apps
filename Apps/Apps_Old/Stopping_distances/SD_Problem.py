# general imports
from random import seed, randrange

# bokeh imports
from bokeh.io             import curdoc
from bokeh.layouts        import column, row
from bokeh.models.widgets import TextInput, Button, Paragraph, CheckboxGroup, Select, Div

# internal imports
from SD_TestSolutions import eval_fct
from SD_InputChecker  import isempty, validate_function, validate_value
from SD_Constants     import (
    min_random_v, max_random_v, steps_v,
    min_v, min_val, max_totT, t_update,
    msg_invalid_value, msg_invalid_function, msg_empty_field,
    bl_quad, bl_sqrt, math_button_width
)

# latex integration
#from os.path import dirname, join, split, abspath
#import sys, inspect
#currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
#parentdir = join(dirname(currentdir), "shared/")
#sys.path.insert(0,parentdir) 
#from latex_support import LatexDiv

# Using pathlib
import pathlib
import sys, inspect
shareddir = str(pathlib.Path(__file__).parent.parent.resolve() / "shared" ) + "/"
sys.path.insert(0,shareddir)
from latex_support import LatexDiv

app_base_path = pathlib.Path(__file__).resolve().parents[0]

#---------------------------------------------------------------------#


class SD_Problem:
    def __init__(self,Vis,Plotter):
        # setup random by selecting a seed (so that numbers are truly random)
        seed()
        # save car viewer
        self.Vis = Vis
        # save graph plotter
        self.Plotter = Plotter
        # choose a random velocity, e.g. between 0.5 and 10 (steps of 0.5)
        self.v = self._init_random_velocity()
        # tell the car viewer about this choice
        self.Vis.setV(self.v)   
        
        ## set up interactions
        # input for v0 or v(s)
        self.Vs = TextInput(value=str(self.v), title="Initial Velocity", width=300)
        self.Vs.on_change('value',self.set_v)
        # choice of v0 or v(s) method
        self.VMethod = Select(title="", value="Initial Velocity",
            options=["Initial Velocity", "Distance-dependent Velocity"], width=300)
        self.VMethod.on_change('value',self.switch_model)
        # get user value for acceleration
        self.UserAcceleration = TextInput(value="", title="Acceleration :", width=300)
        self.UserAcceleration.on_change('value', self.check_acceleration)
        # button which runs the simulation
        self.startSim = Button(label="Start",button_type="success", width=100, disabled=True)
        self.startSim.on_click(self.Start)
        # reset button
        self.reset_button = Button(label="Reset",button_type="success", width=100)
        self.reset_button.on_click(self.Reset)
        # selection for exact time and distance dependent formulas
        self.eq_selection = Select(title="", value="Select an equation", width=300,
            options=["Select an equation",
                     "s(t) - time dependent distance",
                     "v(t) - time dependent velocity",
                     "t(s) - distance dependent time",
                     "v(s) - distance dependent velocity"])
        self.eq_selection.on_change('value', self.show_equation)
        # write equations into a invisible div
        self.eq_st = LatexDiv(text="$$ s(t) = \\frac{1}{2} a_0 t^2 + v_0 t $$", visible=False)
        self.eq_vt = LatexDiv(text="$$ v(t) = \\frac{1}{2} a_0 t + v_0 $$"    , visible=False)
        self.eq_ts = LatexDiv(text="$$ t(s) = \\frac{2s}{v(s)+v_0} = \\frac{2s}{\\sqrt{2as + v_0^2}+v_0} $$", visible=False)
        self.eq_vs = LatexDiv(text="$$ v(s) = \\sqrt{2as + v_0^2} $$"         , visible=False)
        self.equations = {"st":self.eq_st, "vt":self.eq_vt, "ts":self.eq_ts, "vs":self.eq_vs}
        # user input for t(s) to be tested against simulation
        self.UserTs = TextInput(value="", title="t(s) = ",width=200)
        self.UserTs.on_change('value', self.check_function_inputs)
        # user input for v(s) (or a(s)) to be tested against simulation
        self.UserVs = TextInput(value="", title="v(s) = ",width=200)
        self.UserVs.on_change('value', self.check_function_inputs)
        # button to plot t(s) and v(s)/a(s) over simulation data
        self.TestEqs = Button(label="Check equations",button_type="success",width=150)
        self.TestEqs.on_click(self.plot_attempt)
        # warning widget
        self.warning_widget     = Div(text="", render_as_text = False, style={'color':'red', 'font_size':'200%'}, width=300)
        self.warning_widget_equ = Div(text="", render_as_text = False, style={'color':'red', 'font_size':'200%'}, width=300)

        # mathematical operation buttons for user input
        self.math_group_map = {0:self.Vs, 1:self.UserTs, 2:self.UserVs}
        num_math_usr_button_groups = len(self.math_group_map)
        self.math_usr_buttons = dict(sqrts=[], quads=[])
        for i in range(0,num_math_usr_button_groups):
            tmp_tag = "math_group_"+str(i)
            self.math_usr_buttons["sqrts"].append(Button(label=bl_sqrt, button_type="success", width=math_button_width, tags=[tmp_tag]))
            self.math_usr_buttons["quads"].append(Button(label=bl_quad, button_type="success", width=math_button_width, tags=[tmp_tag]))
            self.math_usr_buttons["sqrts"][i].on_click(self.add_math_op)
            self.math_usr_buttons["quads"][i].on_click(self.add_math_op)

        # define a callback map for easy removal and reset of callbacks to widgets
        self.callback_map = {self.Vs: self.set_v, self.UserTs: self.check_function_inputs, self.UserVs: self.check_function_inputs}
    
        
        # initialise initial time, displacement and acceleration
        self.t = 0
        self.s = 0
        self.a = 0
        # remember which model is being used
        self.model_type = "init_v"  # "init_v" and "distance_v"

        # save the callback id to run the simulations
        self.callback_id = None

        # save layout
        self.Layout = column(self.VMethod,
                             row(self.math_usr_buttons["sqrts"][0], self.math_usr_buttons["quads"][0]), 
                             self.Vs, 
                             self.UserAcceleration,
                             row(self.startSim, self.warning_widget),
                             self.reset_button,
                             self.eq_selection, self.eq_st, self.eq_vt, self.eq_ts, self.eq_vs,
                             row(self.math_usr_buttons["sqrts"][1], self.math_usr_buttons["quads"][1]), 
                             self.UserTs,
                             row(self.math_usr_buttons["sqrts"][2], self.math_usr_buttons["quads"][2]),
                             self.UserVs,
                             row(self.TestEqs, self.warning_widget_equ)
                             )



    def set_v(self, attr, old, new):
        # if the box is empty, do nothing
        if new=="": return

        # remove the callback while working in this function
        self.Vs.remove_on_change('value',self.set_v)

        if self.model_type == "init_v":
            # if method using initial velocity v0 is used
            [valid, new_v] = validate_value(new, self.v)
            # store new value if it is valid, otherwise throw a warning message
            if valid:
                self.v = new_v
                self.warning_widget.text = ""
            else:
                self.warning_widget.text = msg_invalid_value
            # display new value in input box
            self.Vs.value = str(new_v)
        
        elif self.model_type == "distance_v":
            # if a sqrt has been inserted, disable the start button since the function is not valid
            if new[-2:] == u"\u221A(":
                self.startSim.disabled = True
                self.Vs.on_change('value',self.set_v)
                return
            # if method using distance dependent velocity v(s) is used
            if (len(new)!=0):
                # if box is not empty
                # check if input is a valid equation and evaluate it
                [valid, fct] = validate_function(new,'s')
                if not valid:
                    print("WARNING: Not a valid function, using old entry.")
                    self.warning_widget.text = msg_invalid_function
                    self.Vs.value = old
                else:
                    self.v = eval_fct(new,'s',self.s)
                    self.warning_widget.text = ""
                    self.startSim.disabled = False
            else:
                print("WARNING: Please enter a function v(s)!")

        # plot the new velocity arrow
        self.Vis.move(self.s, self.v)

        # set the callback again
        self.Vs.on_change('value',self.set_v)


    def check_acceleration(self, attr, old, new):
        # remove the callback while working in this function
        self.UserAcceleration.remove_on_change('value',self.check_acceleration)

        [valid, new_a] = validate_value(new, self.a)
        # store new value if it is valid, otherwise throw a warning message
        if valid:
            self.a = new_a
            self.warning_widget.text = ""
        else:
            self.warning_widget.text = msg_invalid_value
        # display new value in input box
        self.UserAcceleration.value = str(new_a)   # calls function again (max. twice)


        if isempty(self.UserAcceleration.value) or self.a==0:
            # keep the start button disabled
            self.startSim.disabled = True
        else:
            # enable the start button
            self.startSim.disabled = False

        # set the callback again
        self.UserAcceleration.on_change('value',self.check_acceleration)



    def check_function_inputs(self, attr, old, new):
        # if a sqrt has been inserted, do nothing
        if new[-2:] == u"\u221A(": return
        # check if given function is valid
        [valid, fct] = validate_function(new, 's')
        if not valid:
            self.warning_widget_equ.text = msg_invalid_function
        else:
            self.warning_widget_equ.text = ""


        

    def switch_model(self, attr, old, new):
        # remove the callback while working in this function
        self.Vs.remove_on_change('value',self.set_v)

        if new == "Initial Velocity":
            # set the new model internally
            self.model_type = "init_v"
            # change input title
            self.Vs.title = "Initial Velocity = "
            # change title to expect a v(s) user function instead of a(s)
            self.UserVs.title = "v(s) = "
            # initialize a new random initial velocity
            self.v = self._init_random_velocity()
            # show this initial velocity in the text box
            self.Vs.value = str(self.v)

            # alert graphs that problem type has changed
            self.Plotter.swapSetup()
            # reset drawing
            self.Reset()
            # rename acceleration input
            self.UserAcceleration.title="Acceleration :"
            #self.UserAcceleration.disabled = False
            self.UserAcceleration.visible = True

            # disable start button until acceleration is given
            if isempty(self.UserAcceleration.value):
                self.startSim.disabled = True

        elif new == "Distance-dependent Velocity":
            # set the new model internally
            self.model_type = "distance_v"
            # change input title and remove current value from the input box
            self.Vs.title = "Distance-dependent Velocity, v(s)="
            #self.Vs.value = ""
            # change title to expect a a(s) user function instead of v(s)
            self.UserVs.title = "a(s) = "
            
            # show an example of a distance dependent velocity function
            self.Vs.value = u"\u221A(2*(-0.15s)+9)"
            # calculate the velocity for s=0
            self.v = eval_fct(self.Vs.value,'s',0)

            # alert graphs that problem type has changed
            self.Plotter.swapSetup()
            # reset drawing
            self.Reset()
            # clear acceleration input for distance dependent velocity, not needed in this case
            #self.UserAcceleration.value= ""
            self.UserAcceleration.visible = False

        else:
            print("WARNING: model '", new, "' does not exist - using '", self.model_type, "'", sep="")
        
        # set the callback again
        self.Vs.on_change('value',self.set_v)



    def Start(self):
        # remove warnings
        self.warning_widget.text = ""

        # all input functions and values should be valid at this point
        # however there is still a check in the eval_fct for double safety

        if self.model_type == "init_v":
            # setup the graphs with an initial velocity and acceleration
            # so the ranges can be set
            self.Plotter.setup(self.v,self.a)
            # add the first point
            self.Plotter.addPointInTime(0)
            # start the simulation
            self.callback_id = curdoc().add_periodic_callback(self.init_v_Simulation, 100)
        
        elif self.model_type == "distance_v":
            # setup and addPointInTime can only be used for init_v ... TODO: code them more general

            # start the simulation
            self.callback_id = curdoc().add_periodic_callback(self.distance_v_Simulation, 100)

        # start button should not be pressed during simulation
        self.startSim.disabled = True
        


    def init_v_Simulation(self):
        # update time
        self.t+=t_update
        # add point to graphs
        self.Plotter.addPointInTime(self.t)
        # calculate new displacement and velocity
        s = 0.5*self.a*self.t**2+self.v*self.t
        v = self.a*self.t+self.v
        # if the car has stopped or started to reverse then stop the simulation
        if (v<=0):
            # place the car with 0 velocity
            self.Vis.move(s,0)
            curdoc().remove_periodic_callback(self.callback_id)
        # if the car has hit the wall then stop the simulation
        elif (s>=30):
            # place the car at the wall
            self.Vis.move(30,v)
            curdoc().remove_periodic_callback(self.callback_id)
        else:
            # place the car
            self.Vis.move(s,v)



    def distance_v_Simulation(self):
        # v is a function of s but for the simulation to appear realistic
        # the plot must be done at similar time steps
        # therefore temporary variables are used 
        totT  = 0
        sTemp = self.s
        t     = self.t
        # the initial displacement step is val
        val = 0.05
        # the function is looped until the total time step = 0.05s
        while (totT<max_totT):
            # create s for the eval
            s = sTemp
            # find the old velocity
            oldv = eval_fct(self.Vs.value,'s',s)
            # update s with displacement step
            s += val
            # find new velocity
            v = eval_fct(self.Vs.value,'s',s)

            if (v<=min_v or val<=min_val):
                # if the velocity is 0 (including rounding errors)
                # or negative or val has reached it's minimum value
                # then the car is placed with 0 velocity
                self.Vis.move(s,0)
                # the simulation is stopped
                curdoc().remove_periodic_callback(self.callback_id)
                break
            else:
                # else if the velocity is still big enough, fint the next time step
                dt = val/v

                if (totT+dt<= max_totT+0.01):
                    # if dt is small enough then keep it
                    # update total time simulated
                    totT+=dt
                    # update position to which simulated
                    sTemp=s
                    # update time to which simulated
                    t+=dt
                    # calculate acceleration (a(s)=dv^2(s)/ds)
                    a=0.5*(v**2-oldv**2)/val
                    # add new point to graphs
                    self.Plotter.addPoint(t,s,v,a)
                    if (s>=29.99):
                        # if the car has hit the wall then place the car
                        s=30
                        # and stop the simulation
                        curdoc().remove_periodic_callback(self.callback_id)
                        break
                else:
                    # if dt was too large then decrease deplacement step
                    val = 0.5*val
        self.Vis.move(s,v)
        # save new displacement and time values
        self.s=s
        self.t=t



    def Reset(self):
        # reset time and distance
        self.t = 0
        self.s = 0
        
        # move the car to the start with current velocity
        self.Vis.move(self.s, self.v)

        # reset graphs
        self.Plotter.Reset()

        # enable start button again if all callbacks are removed
        if not curdoc().session_callbacks:
            self.startSim.disabled = False
        else: # otherwise stop the running simulation
            curdoc().remove_periodic_callback(self.callback_id)
            self.startSim.disabled = False



    def show_equation(self, attr, old, new):
        if new == "Select an equation":
            for k in self.equations.keys():
                self.equations[k].visible = False
        else:
            # get the key for the equations dict by extracting the first letters
            k = new[:4].replace('(','').replace(')','')
            # hide all other equations
            # remark: need to go through all keys, since value of "old" might be "Select..." which has no key
            for other_key in self.equations.keys():
                if k != other_key: # attention!  != compares strings,  "is not" compares ids
                    self.equations[other_key].visible = False
            # show the corresponding equation
            self.equations[k].visible = True
 

    def add_math_op(self, event_obj):
        # get the Button which called this function
        b = curdoc().get_model_by_id(event_obj._model_id)
        # check if there is a fitting tag - if not, do nothing
        if not any("math_group" in s for s in b.tags):
            print("WARNING: No valid tag for function 'add_math_op'!")
            return
        # extract digit from tag
        mg = int(b.tags[0].split('_')[-1]) # math group
        # set corresponding text input box
        # math_group_map maps the digit in the tag to the currect input box widget
        tmp_input_box = self.math_group_map[mg]

        # avoid triggering the callback while setting a new value
        tmp_input_box.remove_on_change('value',self.callback_map[tmp_input_box])

        # add the correct operator to the end of the string
        if b.label == bl_sqrt:
            tmp_input_box.value = tmp_input_box.value + bl_sqrt + '('
        elif b.label == bl_quad:
            tmp_input_box.value = tmp_input_box.value + '^2'
        else:
            print("WARNING: Operator not supported!")

        # set the callback again
        tmp_input_box.on_change('value',self.callback_map[tmp_input_box])



    def plot_attempt(self):
        # if any of the input fields is empty, provide a message
        if isempty(self.UserTs.value) or isempty(self.UserVs.value):
            self.warning_widget_equ.text = msg_empty_field
        # if there is already a warning message, this button has no functionality
        elif self.warning_widget_equ.text == msg_invalid_function:
            pass
        # double check if the given function is valid
        elif validate_function(self.UserTs.value,'s')[0]==False or validate_function(self.UserVs.value,'s')[0]==False:
            self.warning_widget_equ.text = msg_invalid_function
        # if everything is fine, call the plotter to plot the graphs of user defined functions
        else:
            self.Plotter.test_equation(self.UserTs.value,'t')
            if self.model_type == "init_v":
                self.Plotter.test_equation(self.UserVs.value,'v')
            else:
                self.Plotter.test_equation(self.UserVs.value,'a')


    def _init_random_velocity(self):
        return randrange(min_random_v*10, max_random_v*10, steps_v*10)/10.0

    