from bokeh.plotting import figure
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource
from math import sqrt, isnan
from numpy import linspace

from SD_TestSolutions import eval_fct


class SD_Graphs:
    def __init__(self):
        ## create the 4 figures and set their visual properties
        # create velocity vs. time graph
        tmp_tools = "pan, wheel_zoom, reset"
        self.vt=figure(tools=tmp_tools,x_range=(0,10),y_range=(0,10))
        self.vt.axis.axis_label_text_font_size="14pt"
        self.vt.axis.major_label_text_font_size="12pt"
        #self.vt.axis.axis_label_text_font_style="normal"
        self.vt.xaxis.axis_label = "Time (s)"
        self.vt.yaxis.axis_label = "Velocity (m/s)"
        # create acceleration vs. time (or displacement) graph
        self.at=figure(tools=tmp_tools,x_range=(0,10),y_range=(-10,0))
        self.at.axis.axis_label_text_font_size="14pt"
        self.at.axis.major_label_text_font_size="12pt"
        #self.at.axis.axis_label_text_font_style="normal"
        self.at.xaxis.axis_label = "Time (s)"
        self.at.yaxis.axis_label = u"Acceleration (m/s\u00B2)"
        # create time vs. displacement graph
        self.st=figure(tools=tmp_tools,x_range=(0,30),y_range=(0,10))
        self.st.axis.axis_label_text_font_size="14pt"
        self.st.axis.major_label_text_font_size="12pt"
        #self.st.axis.axis_label_text_font_style="normal"
        self.st.xaxis.axis_label = "Travelled Distance (m)"
        self.st.yaxis.axis_label = "Time (s)"
        # create velocity vs. displacement graph
        self.vs=figure(tools=tmp_tools,x_range=(0,30),y_range=(0,10))
        self.vs.axis.axis_label_text_font_size="14pt"
        self.vs.axis.major_label_text_font_size="12pt"
        #self.vs.axis.axis_label_text_font_style="normal"
        self.vs.xaxis.axis_label = "Travelled Distance (m)"
        self.vs.yaxis.axis_label = "Velocity (m/s)"
        # create necessary column data sources
        self.atSource = ColumnDataSource(data=dict(ts=[],a=[]))
        self.UserAtSource = ColumnDataSource(data=dict(ts=[],a=[]))
        self.stSource = ColumnDataSource(data=dict(t=[],s=[]))
        self.UserStSource = ColumnDataSource(data=dict(t=[],s=[]))
        self.vtSource = ColumnDataSource(data=dict(t=[],v=[]))
        self.vsSource = ColumnDataSource(data=dict(s=[],v=[]))
        self.UserVsSource = ColumnDataSource(data=dict(s=[],v=[]))
        # create lines showing car movement
        self.vt.line(x='t',y='v',source=self.vtSource)
        self.at.line(x='ts',y='a',source=self.atSource)
        self.st.line(x='s',y='t',source=self.stSource)
        self.vs.line(x='s',y='v',source=self.vsSource)
        # create lines showing user calculated path
        self.at.line(x='ts',y='a',source=self.UserAtSource,color="red")
        self.st.line(x='s',y='t',source=self.UserStSource,color="red")
        self.vs.line(x='s',y='v',source=self.UserVsSource,color="red")
        # place the graphs in a grid layout
        self.Layout = gridplot([[self.vt,self.at],[self.st,self.vs]],plot_width=300,plot_height=250,toolbar_options=dict(logo=None))
        # depending upon whether the user specifies the initial velocity or v(s)
        # either a(t) or a(s) is shown in figure=self.at
        # it is important to know what is being drawn
        self.s_or_t = 't'
    
    def setup(self,v,a):
        # initial values are saved
        self.v0=v
        self.a0=a
        # if the initial velocity and constant acceleration was specified
        # then the car will stop at tmax (if it has not yet collided with the wall)
        tmax=abs(v/a)
        # set x and y ranges
        # the time range is [0,tmax] or [0,(sqrt(v^2+60*a)-v)/a]   # 60 = 2*30 = 2*s_max
        # if else is required to avoid sqrt of a negative number
        if (v**2+60*a<0):
            # figure at may have s or t on the x axis,
            # range is chosen to follow this
            if (self.s_or_t=='t'):
                self.at.x_range.end=tmax+1
            else:
                self.at.x_range.end=30
            # set range of axes showing time
            self.vt.x_range.end=tmax+1
            self.st.y_range.end=tmax+1
        else:
            # figure at may have s or t on the x axis,
            # range is chosen to follow this
            if (self.s_or_t=='t'):
                self.at.x_range.end=min(tmax+1,1+(sqrt(v**2+60*a)-v)/a)
            else:
                self.at.x_range.end=30
            # set range of axes showing time
            self.vt.x_range.end=min(tmax+1,1+(sqrt(v**2+60*a)-v)/a)
            self.st.y_range.end=min(tmax+1,1+(sqrt(v**2+60*a)-v)/a)
        # if the initial acceleration is negative, show negative axes
        if (a<0):
            self.at.y_range.start=a-1.0
            self.at.y_range.end=0
        # else show positive axes
        else:
            self.at.y_range.start=0
            self.at.y_range.end=a+1.0
        # set velocity ranges by giving some space for variation
        self.vt.y_range.end=v*1.5
        self.vs.y_range.end=v*1.5
    
    def addPointInTime(self,t):
        # add points to graphs using a=const, v=a*t+v0, s=a*t^2+v0*t
        # only to be used for first setup
        self.vtSource.stream(dict(v=[self.a0*t+self.v0],t=[t]))
        self.atSource.stream(dict(ts=[t],a=[self.a0]))
        self.stSource.stream(dict(t=[t],s=[0.5* self.a0*t**2+self.v0*t]))
        self.vsSource.stream(dict(v=[self.a0*t+self.v0],s=[0.5* self.a0*t**2+self.v0*t]))
    
    def addPoint(self,t,s,v,a):
        # add points in second setup, each point is explicitly given
        # if the point is not in the graph then update the boundaries
        # (in this setup it is much harder to know the correct ranges
        # in advance
        self.stSource.stream(dict(t=[t],s=[s]))
        if (t>self.st.y_range.end):
            self.st.y_range.end=t+1.0
        if (t<self.st.y_range.start):
            self.st.y_range.start=t-1.0
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
        # remove all lines from graphs
        self.vtSource.data = dict(v=[],t=[])
        self.atSource.data = dict(ts=[],a=[])
        self.UserAtSource.data = dict(ts=[],a=[])
        self.stSource.data = dict(s=[],t=[])
        self.UserStSource.data = dict(s=[],t=[])
        self.vsSource.data = dict(v=[],s=[])
        self.UserVsSource.data = dict(v=[],s=[])



    # user defined functions - for comparison to the actual graphs
    def test_equation(self,fct,plt):
        #plt: t, v, a

        if (plt=='t'):
            xmax = self.st.x_range.end
        if (plt=='v'):
            xmax = self.vs.x_range.end
        if (plt=='a'):
            xmax = self.at.x_range.end

        scale = linspace(0,xmax,100)

        #create lists to store coordinates
        X=[]
        Y=[]

        for s in scale:
            X.append(s)
            Y.append(eval_fct(fct,'s',s))  ## fix if sqrt becomes negative


        # add new data to appropriate figure
        if (plt=='t'):
            self.UserStSource.data = dict(s=X,t=Y)
        elif (plt=='v'):
            print(Y)
            self.UserVsSource.data = dict(s=X,v=Y)
        elif (plt=='a'):
            self.UserAtSource.data = dict(ts=X,a=Y)

        
    def swapSetup(self):
        # change between methods by figure
        if (self.s_or_t=='t'):
            self.at.xaxis.axis_label = "Travelled Distance (m)"
            self.at.x_range.end=30
            self.s_or_t='s'
        else:
            self.at.xaxis.axis_label = "Time (s)"
            self.at.x_range.end=10
            self.s_or_t='t'
