from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Range1d, FuncTickFormatter, FixedTicker
from math import pi, floor

#ColourOptions = ["red","blue","green","black","yellow","purple"]

class Collision_BarChart(object):
    def __init__(self, xVals, yVals, colours = None, width=None):
        Max = 0
        Min=0
        N=len(xVals)
        # create list of colours
        if (colours==None):
            colours=list(xVals)
            for i in range(0,N):
                colours[i]="red"
        else:
            if (not isinstance(colours,list)):
                colours=[colours]
                for i in range(1,N):
                    colours.append(colours[0])
        # create list of widths
        if (width==None):
            width=[]
            for i in range(0,N):
                width.append(1)
        # initialise values for loop
        self.fig=figure(tools="")
        self.barSources=[]
        x=0
        places=[]
        label_places=[]
        index={}
        for i in range(0,N):
            # add ColumnDataSource describing each bar
            self.barSources.append(ColumnDataSource(data=dict(x=[x, x, x+width[i],x+width[i]],
                y=[0,yVals[i], yVals[i], 0])))
            # update Max and Min for y_range
            if (yVals[i]+1>Max):
                Max=yVals[i]+1
            elif (yVals[i]<0 and yVals[i]-1<Min):
                Min=yVals[i]-1
            # create bar
            self.fig.patch(x='x', y='y', fill_color=colours[i], source=self.barSources[i], line_color=None)
            br=xVals[i].find('\n')
            places.append(x+width[i]/2.0)
            if (br==-1):
                # remember bar position
                label_places.append(x+width[i]/2.0)
                # remember label that should be written at that postion
                index[str(int(100*(x+width[i]/2.0)))] = [xVals[i]]
            else:
                label=[]
                while (br!=-1):
                    label.append(xVals[i][0:br])
                    xVals[i]=xVals[i][br+1:]
                    br=xVals[i].find('\n')
                label.append(xVals[i])
                N=len(label)
                for j in range(0,N):
                    index[str(int(100*(x+width[i]*(j+1)/(N+1.0))))] = [label[j]]
                    label_places.append((floor(100*(x+width[i]*(j+1)/(N+1.0)))/100.0))
            # increase x
            x+=width[i]+1
        
        # set figure properties
        self.fig.x_range=Range1d(-1,x)
        self.fig.y_range=Range1d(Min,Max)
        self.fig.grid.visible=False
        self.fig.xaxis.major_label_text_font_size="14pt"
        self.fig.xaxis.major_tick_line_color=None
        self.fig.xaxis.major_label_orientation=pi/2
        self.fig.yaxis.major_label_orientation=pi/2
        self.fig.yaxis.axis_label="Kinetic Energy ( Joule )"
        self.fig.toolbar.logo = None
        # only give x ticks at bars
        self.fig.xaxis[0].ticker=FixedTicker(ticks=label_places)
        # save vals in ColumnDataSource so ticker_func can use it as default val
        index_obj = ColumnDataSource(data=index)
        # define function which assigns values to tick labels
        def ticker_func(labels=index_obj):
            return labels.data[str(tick*100)]
        # call ticker_func
        self.fig.xaxis[0].formatter = FuncTickFormatter.from_py_func(ticker_func)
    
    def setTitle(self,title):
        self.fig.title=title
    
    def getFig(self):
        return self.fig
    
    # define operator[]
    def __getItem__ (self,key):
        return self.barSources[key].data
    def __setItem__ (self,key):
        return self.barSources[key].data
    
    def setHeight(self,key,height):
        self.barSources[key].data=dict(x=list(self.barSources[key].data['x']),y=[0,height,height,0])
    
    def Height(self,height):
        self.fig.height=height
    def Width(self,width):
        self.fig.width=width

