from bokeh.plotting import figure
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource, Range1d
from math import sqrt

class Graphs:
    def __init__(self):
        self.st=figure(tools="",x_range=(0,10),y_range=(0,30))
        #self.st.x_range=Range1d(0,10)
        #self.st.y_range=Range1d(0,30)
        self.st.xaxis.axis_label_text_font_size="14pt"
        self.st.yaxis.axis_label_text_font_size="14pt"
        self.st.xaxis.major_label_text_font_size="12pt"
        self.st.yaxis.major_label_text_font_size="12pt"
        self.st.xaxis.axis_label_text_font_style="normal"
        self.st.yaxis.axis_label_text_font_style="normal"
        self.st.xaxis.axis_label = "Zeit (s)"
        self.st.yaxis.axis_label = "Weg (m)"
        self.vt=figure(tools="",x_range=(0,10),y_range=(0,10))
        self.vt.xaxis.axis_label_text_font_size="14pt"
        self.vt.yaxis.axis_label_text_font_size="14pt"
        self.vt.xaxis.major_label_text_font_size="12pt"
        self.vt.yaxis.major_label_text_font_size="12pt"
        self.vt.xaxis.axis_label_text_font_style="normal"
        self.vt.yaxis.axis_label_text_font_style="normal"
        self.vt.xaxis.axis_label = "Zeit (s)"
        self.vt.yaxis.axis_label = "Geschwindigkeit (m/s)"
        self.ts=figure(tools="",x_range=(0,30),y_range=(0,10))
        self.ts.xaxis.axis_label_text_font_size="14pt"
        self.ts.yaxis.axis_label_text_font_size="14pt"
        self.ts.xaxis.major_label_text_font_size="12pt"
        self.ts.yaxis.major_label_text_font_size="12pt"
        self.ts.xaxis.axis_label_text_font_style="normal"
        self.ts.yaxis.axis_label_text_font_style="normal"
        self.ts.xaxis.axis_label = "Weg (m)"
        self.ts.yaxis.axis_label = "Zeit (s)"
        self.vs=figure(tools="",x_range=(0,30),y_range=(0,10))
        self.vs.xaxis.axis_label_text_font_size="14pt"
        self.vs.yaxis.axis_label_text_font_size="14pt"
        self.vs.xaxis.major_label_text_font_size="12pt"
        self.vs.yaxis.major_label_text_font_size="12pt"
        self.vs.xaxis.axis_label_text_font_style="normal"
        self.vs.yaxis.axis_label_text_font_style="normal"
        self.vs.xaxis.axis_label = "Weg (m)"
        self.vs.yaxis.axis_label = "Geschwindigkeit (m/s)"
        self.stSource = ColumnDataSource(data=dict(t=[],s=[]))
        self.vtSource = ColumnDataSource(data=dict(t=[],v=[]))
        self.vsSource = ColumnDataSource(data=dict(s=[],v=[]))
        self.st.line(x='t',y='s',source=self.stSource)
        self.vt.line(x='t',y='v',source=self.vtSource)
        self.ts.line(x='s',y='t',source=self.stSource)
        self.vs.line(x='s',y='v',source=self.vsSource)
    
    def setup(self,v,a):
        self.v0=v
        self.a0=a
        tmax=-v/a
        if (v**2+60*a<0):
            self.st.x_range.end=tmax+1
            self.vt.x_range.end=tmax+1
            self.ts.y_range.end=tmax+1
        else:
            self.st.x_range.end=min(tmax+1,1+(sqrt(v**2+60*a)-v)/a)
            self.vt.x_range.end=min(tmax+1,1+(sqrt(v**2+60*a)-v)/a)
            self.ts.y_range.end=min(tmax+1,1+(sqrt(v**2+60*a)-v)/a)
        self.vt.y_range.end=v*1.5
        self.vs.y_range.end=v*1.5
        self.addPoint(0)
    
    def addPoint(self,t):
        self.stSource.stream(dict(t=[t],s=[0.5* self.a0*t**2+self.v0*t]))
        self.vtSource.stream(dict(v=[self.a0*t+self.v0],t=[t]))
        self.vsSource.stream(dict(v=[self.a0*t+self.v0],s=[0.5* self.a0*t**2+self.v0*t]))
    
    def Reset(self):
        self.stSource.data = dict(s=[],t=[])
        self.vtSource.data = dict(v=[],t=[])
        self.vsSource.data = dict(v=[],s=[])
    
    def disp(self):
        return gridplot([[self.st,self.vt],[self.ts,self.vs]],plot_width=300,plot_height=250)
