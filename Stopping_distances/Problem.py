from string import replace

from Visualisation import Visualisation
from Graphs import Graphs
from TestSolutions import isEquation
from random import seed, randrange
from bokeh.layouts import column, row
from bokeh.models.widgets import TextInput, Button, Paragraph, CheckboxGroup, Slider, Select, Div
from bokeh.io import curdoc

class Problem:
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
        self.Vs = TextInput(value=str(self.v), title="Initial Velocity",width=300)
        self.Vs.on_change('value',self.getNewV)
        # choice of v0 or v(s) method
        self.VMethod = Select(title="", value="Initial Velocity",
            options=["Initial Velocity", "Distance-dependent Velocity"])
        self.VMethod.on_change('value',self.changeModel)
        # get user value for acceleration
        self.UserAcceleration = TextInput(value="", title="Acceleration :")
        # button which runs the simulation
        self.startSim = Button(label="Start",button_type="success",width=100)
        self.startSim.on_click(self.test)
        # reset button
        self.reset_button = Button(label="Reset",button_type="success")
        self.reset_button.on_click(self.Reset)
        #self.idealAcc = -self.v**2/40.0
        # checkbox for whether equations as a function of time are visible
        self.eqVis = checkbox_group = CheckboxGroup(labels=["Show equations as a function of the time"], active=[])
        self.eqVis.on_change('active',self.toggleEquation)
        # save space to write equations as a function of time
        self.eqst = Paragraph(text="")
        self.eqvt = Paragraph(text="")
        # user input for t(s) to be tested against simulation
        self.UserTs = TextInput(value="", title="t(s) = ",width=200)
        # button to allow sqrt to be used in t(s)
        self.TsSqrt = Button(label="Insert: " u"\u221A",button_type="success",width=100)
        self.TsSqrt.on_click(self.addSqrtTs)
        # user input for v(s) (or a(s)) to be tested against simulation
        self.UserVs = TextInput(value="", title="v(s) = ",width=200)
        # button to allow sqrt to be used in v(s)/a(s)
        self.VsSqrt = Button(label="Insert: " u"\u221A",button_type="success",width=100)
        self.VsSqrt.on_click(self.addSqrtVs)
        # button to plot t(s) and v(s)/a(s) over simulation data
        self.TestEqs = Button(label="Check equations",button_type="success",width=100)
        self.TestEqs.on_click(self.plot_attempt)
        
        # initialise initial time and displacement
        self.t = 0
        self.s = 0
        # remember which model is being used
        self.va='v'
        # save layout
        self.Layout = column(row(self.Vs,self.VMethod),row(self.UserAcceleration,self.startSim),self.reset_button,self.eqVis,
            self.eqst,self.eqvt,row(self.UserTs,self.TsSqrt),row(self.UserVs,self.VsSqrt),self.TestEqs)
    
    def getNewV(self,attr,old,new):
        if (self.va=='v'):
            # if first method is in use (i.e. v0 is specified)
            try:
                # replace , with . i.e. change 0,5 to 0.5
                new=replace(new,',','.')
                # convert input to float, if this is not possible then a ValueError is thrown
                temp=float(new)
                # update velocity
                self.v=temp
                # reset the setup
                self.Reset()
            except ValueError:
                # if conversion was unsuccesful then reset box to old v0
                self.Vs.value=str(self.v)
        else:
            # if second method is in use (i.e. v(s) is specified)
            if (len(new)!=0):
                # if box is not empty
                # check if input is a valid equation
                s1=isEquation(new,'s')
                if (s1!=False):
                    # if this is the case then save the new velocity
                    self.v=s1
                    # reset the setup
                    self.Reset()
                else:
                    # if it isn't then revert to old value
                    self.Vs.value=old
    
    def test(self):
        # start the simulation
        print(self.v)
        if (self.t!=0):
            # if it is not already at the beginning then reset the setup
            self.Reset()
        if (self.va=='v'):
            # if the first problem is being used
            try:
                # replace , with . i.e. change 0,5 to 0.5
                s=replace(self.UserAcceleration.value,',','.')
                # convert input to float, if this is not possible then a ValueError is thrown
                self.a=float(s)
                # setup the graphs with an initial velocity and acceleration
                # so the ranges can be set
                self.Plotter.setup(self.v,self.a)
                # add the first point
                self.Plotter.addPointInTime(0)
                # start the simulation
                curdoc().add_periodic_callback(self.vSimulation, 100)
            except ValueError:
                pass
        elif(self.v!=0):
            # start the simulation
            curdoc().add_periodic_callback(self.aSimulation, 100)
    
    def vSimulation(self):
        # update time
        self.t+=0.1
        # add point to graphs
        self.Plotter.addPointInTime(self.t)
        # calculate new displacement and velocity
        s=0.5*self.a*self.t**2+self.v*self.t
        v=self.a*self.t+self.v
        # if the car has stopped of started to reverse then stop the simulation
        if (v<=0):
            # place the car with 0 velocity
            self.Vis.move(s,0)
            curdoc().remove_periodic_callback(self.vSimulation)
        # if the car has hit the wall then stop the simulation
        elif (s>=30):
            # place the car at the wall
            self.Vis.move(30,v)
            curdoc().remove_periodic_callback(self.vSimulation)
        else:
            # place the car
            self.Vis.move(s,v)

    def aSimulation(self):
        # v is a function of s but for the simulation to appear realistic
        # the plot must be done at similar time steps
        # therefore temporary variables are used 
        totT=0
        sTemp=self.s
        t=self.t
        # the initial displacement step is val
        val=0.05
        # the function is looped until the total time step = 0.05s
        while (totT<0.05):
            # create s for the eval
            s=sTemp
            # find the old velocity
            oldv=eval(self.v)
            # update s with displacement step
            s+=val
            # find new velocity
            v=eval(self.v)
            if (v<=1e-10 and val<=0.0005):
                # if the velocity is 0 (including rounding errors)
                # or negative and val has reached it's minimum value
                # then the car is placed with 0 velocity
                self.Vis.move(s,0)
                # the simulation is stopped
                curdoc().remove_periodic_callback(self.aSimulation)
                # and totT is made large enough to break the while loop
                totT=0.15
            elif (v<0):
                # else if the velocity is negative
                # then reduce the displacement step
                val/=2.0
            else:
                # else if the velocity is normal then find the time step
                dt=val/v
                if (totT+dt<=0.06):
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
                    if (v<=1e-10):
                        # if velocity is 0 or negative then place the car with 0 velocity
                        v=0
                        # and stop simulation
                        totT=0.15
                        curdoc().remove_periodic_callback(self.aSimulation)
                    elif (abs(v-oldv)<0.001):
                        # if acceleration is too slow to see changes stop the simulation
                        totT=0.15
                        curdoc().remove_periodic_callback(self.aSimulation)
                    elif (s>=29.99):
                        # if the car has hit the wall then place the car
                        s=30
                        # and stop the simulation
                        totT=0.15
                        curdoc().remove_periodic_callback(self.aSimulation)
                else:
                    # if dt was too large then decrease deplacement step
                    val=val/2.0
        self.Vis.move(s,v)
        # save new displacement and time values
        self.s=s
        self.t=t
    
    def Reset(self):
        # reset start values of t and s
        self.t = 0
        self.s = 0
        if (self.va=='v'):
            # if using first model then move car to start and show velocity arrow
            self.Vis.move(0,self.v)
        elif (self.v==0):
            # if using second model and no equation is given,
            # move car to start but show no velocity
            self.Vis.move(0,0)
        else:
            # if using second model equation is given,
            # move car to start and show v0 (calculated by eval(self.v) as
            # self.v contains an equation as a functin of s which has been defined as 0)
            s=0
            self.Vis.move(0,eval(self.v))
        # reset graphs
        self.Plotter.Reset()
        try:
            # remove call which makes car move
            # (if it is not moving then a ValueError is thrown and ignored)
            if (self.va=='v'):
                curdoc().remove_periodic_callback(self.vSimulation)
            else:
                curdoc().remove_periodic_callback(self.aSimulation)
        except ValueError:
            pass
    
    def toggleEquation (self,attr,old,new):
        # show/hide equations as a function of time
        if (len(new)==1):
            self.eqst.text = u"s(t)=0.5 a\u2092t \u00B2+v\u2092t"
            self.eqvt.text = u"v(t)=a\u2092t+v\u2092"
        else:
            self.eqst.text = ""
            self.eqvt.text = ""
    
    def addSqrtTs (self):
        # add sqrt (unicode symbol) to user input for t(s)
        self.UserTs.value=self.UserTs.value+u"\u221A("

    def addSqrtVs (self):
        # add sqrt (unicode symbol) to user input for v(s) (or a(s))
        self.UserVs.value=self.UserVs.value+u"\u221A("

    def plot_attempt(self):
        s1=isEquation(self.UserTs.value,'s')
        #print(s1)
        # if s1 is a string
        if (s1!=False):
            self.Plotter.test_equation(s1,'s')
        s1=isEquation(self.UserVs.value,'s')
        # if s1 is a string
        if (s1!=False):
            self.Plotter.test_equation(s1,self.va)
    
    def changeModel(self,attr,old,new):
        # change problem type
        if (new=="Initial Velocity"):
            # if new problem type is where user provides v0
            # update input title to indicate this
            self.Vs.title="Initial Velocity = "
            # allow user to test v(s) rather that a(s)
            self.UserVs.title="v(s) = "
            # remember which model is in use
            self.va='v'
            # initialise with a random velocity between 0.5 and 10 (increments of 0.5)
            self.v=randrange(5,100,5)/10.0
            self.Vs.value=str(self.v)
            # alert graphs that problem type has changed
            self.Plotter.swapSetup()
            # reset drawing
            self.Reset()
            # enable viewer to see s(t) and v(t)
            self.eqVis.disabled=False
            # rename acceleration input
            self.UserAcceleration.disabled = False
            self.UserAcceleration.title="Acceleration :"
        elif (new=="Distance-dependent Velocity"):
            # if new problem type is where user provides v(s)
            # update input title to indicate this
            self.Vs.title="Distance-dependent Velocity, v(s)="
            # allow user to test a(s) rather that v(s)
            self.UserVs.title="a(s) = "
            # remember which model is in use
            self.va='a'
            # remove old data
            self.Vs.value=""
            self.v=0
            # alert graphs that problem type has changed
            self.Plotter.swapSetup()
            # reset drawing
            self.Reset()
            # stop viewer from seeing s(t) and v(t) (as not relevant to this problem)
            self.eqVis.disabled=True
            # clear and remove name from acceleration input
            # (disabled does not work, nor does visible)
            self.UserAcceleration.value=""
            self.UserAcceleration.title=""
            self.UserAcceleration.disabled = True