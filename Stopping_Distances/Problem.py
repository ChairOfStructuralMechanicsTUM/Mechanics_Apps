from Visualisation import *
from Graphs import *
from random import seed, randrange
from bokeh.layouts import column, row, widgetbox
from bokeh.models.widgets import TextInput, Button, Paragraph, CheckboxGroup
from bokeh.io import curdoc

class Problem:
    def __init__(self,Vis,Plotter):
        seed()
        self.Vis=Vis
        self.Plotter=Plotter
        self.v=randrange(5,100,5)/10.0
        self.Vis.setV(self.v)
        self.UserAcceleration = TextInput(value="", title="Beschleunigung :")
        self.getAcc = Button(label="Test",button_type="success",width=100)
        self.getAcc.on_click(self.test)
        self.newV = Button(label="Neue Anfangsgeschwindigkeit",button_type="success",width=200)
        self.newV.on_click(self.getNewV)
        self.userInfo = Paragraph(text="Die Anfangsgeschwindigkeit ist "+str(self.v)+" m/s")
        self.reset_button = Button(label="Reset",button_type="success")
        self.reset_button.on_click(self.Reset)
        self.idealAcc = -self.v**2/40.0
        self.eqst = Paragraph(text="")
        self.eqvt = Paragraph(text="")
        self.eqVis = checkbox_group = CheckboxGroup(labels=["Gleichung anzeigen"], active=[])
        self.eqVis.on_change('active',self.toggleEquation)
        self.t = 0
    
    def disp(self):
        return column(row(self.userInfo,self.newV),row(self.UserAcceleration,self.getAcc),self.reset_button,self.eqVis,
            self.eqst,self.eqvt)#,self.eqts,self.eqvs)
    
    def getNewV(self):
        self.v=randrange(5,100,5)/10.0
        self.userInfo.text="Die Anfangsgeschwindigkeit ist "+str(self.v)+" m/s"
        self.Vis.setV(self.v)
        self.Reset()
    
    def test(self):
        if (self.t!=0):
            self.Reset()
        try:
            self.a=float(self.UserAcceleration.value)
            self.Plotter.setup(self.v,self.a)
            curdoc().add_periodic_callback(self.simulation, 100)
        except ValueError:
            pass

    def simulation(self):
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
    
    def Reset(self):
        self.t = 0
        self.Vis.move(0,self.v)
        self.Plotter.Reset()
    
    def toggleEquation (self,attr,old,new):
        if (len(new)==1):
            self.eqst.text = u"s(t)=0.5 a\u2092t \u00B2+v\u2092t"
            self.eqvt.text = u"v(t)=a\u2092t+v\u2092"
        else:
            self.eqst.text = ""
            self.eqvt.text = ""
