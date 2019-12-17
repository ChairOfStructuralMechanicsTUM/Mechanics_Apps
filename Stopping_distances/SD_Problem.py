#from string import replace

#from SD_Visualisation import SD_Visualisation
#from SD_Graphs import SD_Graphs
from SD_TestSolutions import eval_fct #isEquation
from random import seed, randrange
from bokeh.layouts import column, row
from bokeh.models.widgets import TextInput, Button, Paragraph, CheckboxGroup, Select#, Slider, Div
from bokeh.io import curdoc

from SD_Constants import (
    min_v, max_v, steps_v
)

class SD_Problem:
    def __init__(self,Vis,Plotter):
        # setup random by selecting a seed (so that numbers are truly random)
        seed()
        # save car viewer
        self.Vis=Vis
        # save graph plotter
        self.Plotter=Plotter
        # choose a random velocity between 0.5 and 10 (steps of 0.5)
        self.v=randrange(5,100,5)/10.0
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
        self.startSim.on_click(self.dummy_callback)
        # reset button
        self.reset_button = Button(label="Reset",button_type="success", width=100)
        self.reset_button.on_click(self.dummy_callback)
        #self.idealAcc = -self.v**2/40.0
        # checkbox for whether equations as a function of time are visible
        #self.eqVis = checkbox_group = CheckboxGroup(labels=["Show equations as a function of the time"], active=[])
        self.eqVis = CheckboxGroup(labels=["Show equations as a function of the time"], active=[])
        self.eqVis.on_change('active',self.dummy_callback_attr)
        # save space to write equations as a function of time
        self.eqst = Paragraph(text="")
        self.eqvt = Paragraph(text="")
        # user input for t(s) to be tested against simulation
        self.UserTs = TextInput(value="", title="t(s) = ",width=200)
        # button to allow sqrt to be used in t(s)
        self.TsSqrt = Button(label="Insert: " u"\u221A",button_type="success",width=100)
        self.TsSqrt.on_click(self.dummy_callback)
        # user input for v(s) (or a(s)) to be tested against simulation
        self.UserVs = TextInput(value="", title="v(s) = ",width=200)
        # button to allow sqrt to be used in v(s)/a(s)
        self.VsSqrt = Button(label="Insert: " u"\u221A",button_type="success",width=100)
        self.VsSqrt.on_click(self.dummy_callback)
        # button to plot t(s) and v(s)/a(s) over simulation data
        self.TestEqs = Button(label="Check equations",button_type="success",width=100)
        self.TestEqs.on_click(self.dummy_callback)
        
        # initialise initial time and displacement
        self.t = 0
        self.s = 0
        # remember which model is being used
        self.model_type = "init_v"  # "init_v" and "distance_v"
        # save layout
        #self.Layout = column(row(self.Vs,self.VMethod),row(self.UserAcceleration,self.startSim),self.reset_button,self.eqVis,
        #    self.eqst,self.eqvt,row(self.UserTs,self.TsSqrt),row(self.UserVs,self.VsSqrt),self.TestEqs)
        self.Layout = column(self.VMethod, self.Vs, self.UserAcceleration, self.startSim, self.reset_button,
                             self.eqVis, self.eqst, self.eqvt, row(self.UserTs, self.TsSqrt), row(self.UserVs,self.VsSqrt),self.TestEqs)



    def set_v(self, attr, old, new):
        #print("in set v callback")
        if self.model_type == "init_v":
            #print("in init_v")
            # if method using initial velocity v0 is used
            try:
                # replace , with . i.e. change 0,5 to 0.5
                new = new.replace(',','.')
                self.Vs.value = new
                # convert input to float, if this is not possible then a ValueError is thrown
                temp = float(new)
                # update velocity
                self.v = temp
                # reset the setup
                #self.Reset()
            except ValueError:
                # if conversion was unsuccesful then reset box to old v0
                self.Vs.value = str(self.v)
        
        elif self.model_type == "distance_v":
            # if method using distance dependent velocity v(s) is used
            if (len(new)!=0):
                # if box is not empty
                # check if input is a valid equation and evaluate it
                #s1=isEquation(new,'s')
                s1 = eval_fct(new,'s',self.s)
                if (s1!=False):
                    # if this is the case then save the new velocity
                    self.v = s1
                    # reset the setup
                    #self.Reset()
                else:
                    # if it isn't valid then revert to old value
                    self.Vs.value = old
            else:
                print("WARNING: Please enter a function v(s)!")


    def check_acceleration(self, attr, old, new):
        # could be extended to e.g. disallow very huge magnitudes

        # get rid of empty spaces
        new = new.replace(" ","")
        # replace , with . i.e. change 0,5 to 0.5
        new = new.replace(',','.')
        self.UserAcceleration.value = new
        #print("inf loop?") # only twice
        if len(new)!=0:
            self.startSim.disabled = False
        else:
            self.startSim.disabled = True





    def switch_model(self, attr, old, new):
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
            # enable viewer to see s(t) and v(t)
            self.eqVis.visible=True
            # rename acceleration input
            self.UserAcceleration.title="Acceleration :"
            #self.UserAcceleration.disabled = False
            self.UserAcceleration.visible = True

        elif new == "Distance-dependent Velocity":
            # set the new model internally
            self.model_type = "distance_v"
            # change input title and remove current value from the input box
            self.Vs.title = "Distance-dependent Velocity, v(s)="
            self.Vs.value = ""
            # change title to expect a a(s) user function instead of v(s)
            self.UserVs.title = "a(s) = "
            
            # set the current velocity to zero
            #self.v = 0
            # show an example of a distance dependent velocity function
            self.Vs.value = "2s+1"
            # calculate the velocity for s=0
            self.v = eval_fct(self.Vs.value,'s',0)

            # alert graphs that problem type has changed
            self.Plotter.swapSetup()
            # reset drawing
            self.Reset()
            # stop viewer from seeing s(t) and v(t) (as not relevant to this problem)
            self.eqVis.visible=False
            # clear and remove name from acceleration input
            # (disabled does not work, nor does visible)
            self.UserAcceleration.value= ""
            #self.UserAcceleration.title= ""
            #self.UserAcceleration.disabled = True
            self.UserAcceleration.visible = False

        else:
            print("WARNING: model '", new, "' does not exist - using '", self.model_type, "'", sep="")



    def Reset(self):
        # reset time and distance
        self.t = 0
        self.s = 0
        
        # print the current value in the textbox
        #self.Vs.value = str(self.v)

        # move the car to the start with current velocity
        self.Vis.move(self.s, self.v)

        # # if using the initial velocity model, move the car to the start with current velocity
        # if self.model_type == "init_v":
        #     self.Vis.move(self.s, self.v)
        # elif self.model_type == "distance_v":
        #     pass
        #     #self.Vis.move(self.s, eval_fct(self.v,'s',self.s))
        # else:
        #     pass

        # reset graphs
        self.Plotter.Reset()
        



    def _init_random_velocity(self):
        return randrange(min_v*10,max_v*10,steps_v*10)/10.0

    def dummy_callback(self):
        pass

    def dummy_callback_attr(self, attr, old, new):
        pass
        

