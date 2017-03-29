from bokeh.plotting import figure
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource, Range1d
from math import sqrt
from numpy import linspace

class Graphs:
    def __init__(self):
        self.at=figure(tools="",x_range=(0,10),y_range=(-10,0))
        #self.st.x_range=Range1d(0,10)
        #self.st.y_range=Range1d(0,30)
        self.at.xaxis.axis_label_text_font_size="14pt"
        self.at.yaxis.axis_label_text_font_size="14pt"
        self.at.xaxis.major_label_text_font_size="12pt"
        self.at.yaxis.major_label_text_font_size="12pt"
        self.at.xaxis.axis_label_text_font_style="normal"
        self.at.yaxis.axis_label_text_font_style="normal"
        self.at.xaxis.axis_label = "Zeit (s)"
        self.at.yaxis.axis_label = u"Beschleunigung (m/s\u00B2)"
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
        self.atSource = ColumnDataSource(data=dict(ts=[],a=[]))
        self.UserAtSource = ColumnDataSource(data=dict(ts=[],a=[]))
        self.tsSource = ColumnDataSource(data=dict(t=[],s=[]))
        self.UserStSource = ColumnDataSource(data=dict(t=[],s=[]))
        self.vtSource = ColumnDataSource(data=dict(t=[],v=[]))
        self.vsSource = ColumnDataSource(data=dict(s=[],v=[]))
        self.UserVsSource = ColumnDataSource(data=dict(s=[],v=[]))
        self.at.line(x='ts',y='a',source=self.atSource)
        self.at.line(x='ts',y='a',source=self.UserAtSource,color="red")
        self.vt.line(x='t',y='v',source=self.vtSource)
        self.ts.line(x='s',y='t',source=self.tsSource)
        self.ts.line(x='s',y='t',source=self.UserStSource,color="red")
        self.vs.line(x='s',y='v',source=self.vsSource)
        self.vs.line(x='s',y='v',source=self.UserVsSource,color="red")
        self.Layout = gridplot([[self.vt,self.at],[self.ts,self.vs]],plot_width=300,plot_height=250)
        self.s_or_t = 't'
    
    def setup(self,v,a):
        self.v0=v
        self.a0=a
        tmax=-v/a
        if (v**2+60*a<0):
            if (self.s_or_t=='t'):
                self.at.x_range.end=tmax+1
            else:
                self.at.x_range.end=30
            self.vt.x_range.end=tmax+1
            self.ts.y_range.end=tmax+1
        else:
            if (self.s_or_t=='t'):
                self.at.x_range.end=min(tmax+1,1+(sqrt(v**2+60*a)-v)/a)
            else:
                self.at.x_range.end=30
            self.vt.x_range.end=min(tmax+1,1+(sqrt(v**2+60*a)-v)/a)
            self.ts.y_range.end=min(tmax+1,1+(sqrt(v**2+60*a)-v)/a)
        if (a<0):
            self.at.y_range.start=a-1.0
            self.at.y_range.end=0
        else:
            self.at.y_range.start=0
            self.at.y_range.end=a+1.0
        self.vt.y_range.end=v*1.5
        self.vs.y_range.end=v*1.5
        self.addPoint(0)
    
    def addPoint(self,t):
        self.tsSource.stream(dict(t=[t],s=[0.5* self.a0*t**2+self.v0*t]))
        self.atSource.stream(dict(ts=[t],a=[self.a0]))
        self.vtSource.stream(dict(v=[self.a0*t+self.v0],t=[t]))
        self.vsSource.stream(dict(v=[self.a0*t+self.v0],s=[0.5* self.a0*t**2+self.v0*t]))
    
    def addPoint(self,t,s,v,a):
        self.tsSource.stream(dict(t=[t],s=[s]))
        if (t>self.ts.y_range.end):
            self.ts.y_range.end=t+1.0
        if (t<self.ts.y_range.start):
            self.ts.y_range.start=t-1.0
        self.atSource.stream(dict(ts=[s],a=[a]))
        if (s>self.at.x_range.end):
            self.at.x_range.end=s+1.0
        if (s<self.at.x_range.start):
            self.at.x_range.start=s-1.0
        if (a>self.at.y_range.end):
            self.at.y_range.end=a+1.0
        if (a<self.at.y_range.start):
            self.at.y_range.start=a-1.0
        self.vtSource.stream(dict(v=[v],t=[t]))
        if (v>self.vt.y_range.end):
            self.vt.y_range.end=v+1.0
        if (v<self.vt.y_range.start):
            self.vt.y_range.start=v-1.0
        if (t>self.vt.x_range.end):
            self.vt.x_range.end=t+1.0
        if (t<self.vt.x_range.start):
            self.vt.x_range.start=t-1.0
        self.vsSource.stream(dict(v=[v],s=[s]))
        if (v>self.vs.y_range.end):
            self.vs.y_range.end=v+1.0
        if (v<self.vs.y_range.start):
            self.vs.y_range.start=v-1.0
    
    def Reset(self):
        self.atSource.data = dict(ts=[],a=[])
        self.UserAtSource.data = dict(ts=[],a=[])
        self.tsSource.data = dict(s=[],t=[])
        self.UserStSource.data = dict(s=[],t=[])
        self.vtSource.data = dict(v=[],t=[])
        self.vsSource.data = dict(v=[],s=[])
        self.UserVsSource.data = dict(v=[],s=[])
    
    def test_equation(self,Str,sv):
        if (sv=='s'):
            xmax=self.ts.x_range.end
        elif (sv=='v'):
            xmax=self.vs.x_range.end
        elif (sv=='a'):
            xmax=self.at.x_range.end
        
        X=[]
        Y=[]
        for s in linspace(0,xmax,100.0):
            X.append(s)
            Y.append(eval(Str))
        
        X.append(xmax)
        s=xmax
        Y.append(eval(Str))
        
        if (sv=='s'):
            self.UserStSource.data = dict(s=X,t=Y)
        elif (sv=='v'):
            self.UserVsSource.data = dict(s=X,v=Y)
        elif (sv=='a'):
            self.UserAtSource.data = dict(ts=X,a=Y)
        
    def swapSetup(self):
        if (self.s_or_t=='t'):
            self.at.xaxis.axis_label = "Weg (m)"
            self.at.x_range.end=30
            self.s_or_t='s'
        else:
            self.at.xaxis.axis_label = "Zeit (s)"
            self.at.x_range.end=10
            self.s_or_t='t'
