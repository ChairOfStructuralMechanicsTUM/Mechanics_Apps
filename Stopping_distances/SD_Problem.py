#from string import replace

#from SD_Visualisation import SD_Visualisation
#from SD_Graphs import SD_Graphs
from SD_TestSolutions import isEquation
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
        self.Vs.on_change('value',self.dummy_callback_attr)
        # choice of v0 or v(s) method
        self.VMethod = Select(title="", value="Initial Velocity",
            options=["Initial Velocity", "Distance-dependent Velocity"], width=300)
        self.VMethod.on_change('value',self.switch_model)
        # get user value for acceleration
        self.UserAcceleration = TextInput(value="", title="Acceleration :", width=300)
        # button which runs the simulation
        self.startSim = Button(label="Start",button_type="success", width=100)
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
            self.v = 0

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
        self.Vs.value = str(self.v)

        # if using the initial velocity model, move the car to the start with current velocity
        if self.model_type == "init_v":
            self.Vis.move(0, self.v)
        else:
            pass

        # reset graphs
        self.Plotter.Reset()
        



    def _init_random_velocity(self):
        return randrange(min_v*10,max_v*10,steps_v*10)/10.0

    def dummy_callback(self):
        pass

    def dummy_callback_attr(self, attr, old, new):
        pass
        

