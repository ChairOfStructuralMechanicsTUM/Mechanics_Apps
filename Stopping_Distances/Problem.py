from Visualisation import *
from Graphs import *
from TestSolutions import *
from random import seed, randrange
from bokeh.layouts import column, row
from bokeh.models.widgets import TextInput, Button, Paragraph, CheckboxGroup, Slider, Select, Div
from bokeh.io import curdoc

class Problem:
    def __init__(self,Vis,Plotter):
        seed()
        self.Vis=Vis
        self.Plotter=Plotter
        self.v=randrange(5,100,5)/10.0
        self.Vis.setV(self.v)
        self.UserAcceleration = TextInput(value="", title="Beschleunigung :")
        self.getAcc = Button(label=u"Uberpr\u00FCfen",button_type="success",width=100)
        self.getAcc.on_click(self.test)
        #self.newV = Button(label="Neue Geschwindigkeit",button_type="success",width=200)
        #self.newV.on_click(self.getNewV)
        #self.userInfo = Paragraph(text="Die Anfangsgeschwindigkeit ist "+str(self.v)+" m/s")
        #self.V0 = Slider(title="Anfangsgeschwindigkeit (m/s) ",value=self.v,start=0,end=10,step=0.1,width=300)
        #self.V0.on_change('value',self.getNewV)
        self.Vs = TextInput(value=str(self.v), title="Anfangsgeschwindigkeit",width=300)
        self.Vs.on_change('value',self.getNewV)
        self.VMethod = Select(title="", value="Anfangsgeschwindigkeit",
            options=["Anfangsgeschwindigkeit", u"Webabh\u00E4ngige Geschwindigkeit"])
        self.VMethod.on_change('value',self.changeModel)
        self.reset_button = Button(label="Reset",button_type="success")
        self.reset_button.on_click(self.Reset)
        self.idealAcc = -self.v**2/40.0
        self.eqst = Paragraph(text="")
        self.eqvt = Paragraph(text="")
        self.eqVis = checkbox_group = CheckboxGroup(labels=["Gleichung anzeigen"], active=[])
        self.eqVis.on_change('active',self.toggleEquation)
        self.t = 0
        self.s = 0
        self.UserTs = TextInput(value="", title="t(s) = ",width=200)
        self.TsSqrt = Button(label=u"\u221A",button_type="success",width=100)
        self.TsSqrt.on_click(self.addSqrtTs)
        self.UserVs = TextInput(value="", title="v(s) = ",width=200)
        self.VsSqrt = Button(label=u"\u221A",button_type="success",width=100)
        self.VsSqrt.on_click(self.addSqrtVs)
        self.va='v'
        self.TestEqs = Button(label=u"Gleichungen \u00FCberpr\u00FCfen",button_type="success",width=100)
        self.TestEqs.on_click(self.plot_attempt)
        self.Hack = Div(text="""<div style="position:fixed; width:20px; height:20px; color:red;top=0;"></div>""",width=10,height=10)
        self.Layout = column(row(self.Vs,self.VMethod),row(self.UserAcceleration,self.getAcc),self.reset_button,self.eqVis,
            self.eqst,self.eqvt,row(self.UserTs,self.TsSqrt),row(self.UserVs,self.VsSqrt),self.TestEqs,self.Hack)
    
    def getNewV(self,attr,old,new):
        if (self.va=='v'):
            try:
                new=replace(new,',','.')
                temp=float(new)
                self.v=temp
                self.Reset()
            except ValueError:
                self.Vs.value=str(self.v)
        else:
            if (len(new)!=0):
                s1=isEquation(new,'s')
                if (s1!=False):
                    self.v=s1
                    self.Reset()
                else:
                    self.Vs.value=old
    
    def test(self):
        if (self.t!=0):
            self.Reset()
        if (self.va=='v'):
            try:
                s=replace(self.UserAcceleration.value,',','.')
                self.a=float(s)
                self.Plotter.setup(self.v,self.a)
                curdoc().add_periodic_callback(self.simulation, 400)
            except ValueError:
                pass
        elif(self.v!=0):
            curdoc().add_periodic_callback(self.simulation, 400)

    def simulation(self):
        if (self.va=='v'):
            self.t+=0.1
            self.Plotter.addPoint(self.t)
            s=0.5*self.a*self.t**2+self.v*self.t
            v=self.a*self.t+self.v
            if (v<=0):
                self.Vis.move(s,0)
                curdoc().remove_periodic_callback(self.simulation)
            elif (s>=30):
                self.Vis.move(30,v)
                curdoc().remove_periodic_callback(self.simulation)
            else:
                self.Vis.move(s,v)
        else:
            totT=0
            sTemp=self.s
            t=self.t
            val=0.05
            while (totT<0.05):
                s=sTemp
                oldv=eval(self.v)
                s+=val
                v=eval(self.v)
                if ((v<=1e-10 or abs(v-oldv)<0.001) and val<=0.0005):
                    self.Vis.move(s,0)
                    curdoc().remove_periodic_callback(self.simulation)
                    totT=0.15
                elif (v<0):
                    val/=2.0
                else:
                    dt=val/v
                    if (dt<=0.01):
                        val*=2
                    elif (dt<=0.06):
                        totT+=dt
                        sTemp=s
                        t+=dt
                        a=0.5*(v**2-oldv**2)/val
                        self.Plotter.addPoint(t,s,v,a)
                        if (v<=1e-10 or abs(v-oldv)<0.001):
                            self.Vis.move(s,0)
                            curdoc().remove_periodic_callback(self.simulation)
                        elif (s>=29.99):
                            self.Vis.move(30,v)
                            curdoc().remove_periodic_callback(self.simulation)
                        else:
                            self.Vis.move(s,v)
                    else:
                        val=val/2.0
            self.s=s
            self.t=t
    
    def Reset(self):
        self.t = 0
        self.s = 0
        if (self.va=='v'):
            self.Vis.move(0,self.v)
        elif (self.v==0):
            self.Vis.move(0,0)
        else:
            s=0
            self.Vis.move(0,eval(self.v))
        self.Plotter.Reset()
        try:
            curdoc().remove_periodic_callback(self.simulation)
        except ValueError:
            pass
    
    def toggleEquation (self,attr,old,new):
        if (len(new)==1):
            self.eqst.text = u"s(t)=0.5 a\u2092t \u00B2+v\u2092t"
            self.eqvt.text = u"v(t)=a\u2092t+v\u2092"
        else:
            self.eqst.text = ""
            self.eqvt.text = ""
    
    def addSqrtTs (self):
        self.UserTs.value=self.UserTs.value+u"\u221A("

    def addSqrtVs (self):
        self.UserVs.value=self.UserVs.value+u"\u221A("

    def plot_attempt(self):
        s1=isEquation(self.UserTs.value,'s')
        # if s1 is a string
        if (s1!=False):
            self.Plotter.test_equation(s1,'s')
        s1=isEquation(self.UserVs.value,'s')
        # if s1 is a string
        if (s1!=False):
            self.Plotter.test_equation(s1,self.va)
    
    def changeModel(self,attr,old,new):
        if (new=="Anfangsgeschwindigkeit"):
            self.Vs.title="Anfangsgeschwindigkeit = "
            self.UserVs.title="v(s) = "
            self.v=randrange(5,100,5)/10.0
            self.va='v'
            self.Vs.value=str(self.v)
            self.Plotter.swapSetup()
            self.Reset()
        elif (new==u"Webabh\u00E4ngige Geschwindigkeit"):
            self.Vs.title=u"Webabh\u00E4ngige Geschwindigkeit, v(s)="
            self.UserVs.title="a(s) = "
            self.va='a'
            self.Vs.value=""
            self.v=0
            self.Plotter.swapSetup()
            self.Reset()
