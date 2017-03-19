from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, LabelSet, Arrow, OpenHead
from bokeh.io import curdoc
from numpy import loadtxt
from time import sleep

## set up data sources for movable objects ##
#     data sources for drawing
top_of_sample_source = ColumnDataSource(data=dict(x=[], y=[]))
L_arrow_source = ColumnDataSource(data=dict(xS=[-1], xE=[-1], yS=[3],yE=[8]))
dL_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[]))
top_sample_line_source = ColumnDataSource(data=dict(x=[-3,8], y=[8,8]))
S_width_source = ColumnDataSource(data=dict(xS=[2], xE=[3],yS=[5.5],yE=[5.5]))
S_label_source = ColumnDataSource(data=dict(x=[2.3],y=[6],S=['S']))
F_label_source = ColumnDataSource(data=dict(x=[2.5],y=[10.6],F=['F']))
F_arrow_source = ColumnDataSource(data=dict(xS=[2.5], xE=[2.5],yS=[9],yE=[10.5]))
#     data sources for plot
plot_source_theory = ColumnDataSource(data=dict(eps=[], sig=[]))
plot_source_practical = ColumnDataSource(data=dict(eps=[], sig=[]))
current_coords = ColumnDataSource(data=dict(eps=[0], sig=[0]))

## Define constants ##
# L chosen to keep deformations in the drawing window
L=0.05;

## Load Plotting Points from file ##
DataPlotter = loadtxt('Zugversuch/GraphData.txt');

## Create array containing the points which need to be plotted for each
#  incrementation of the force slider (i.e. for Force = 5 (1 incrementation)
#  the points DataPlotter[0] and DataPlotter[1] need to be plotted as 
#  DataPlotterDictionary[1]=2, and
#  DataPlotter[0:2]=[DataPlotter[0], DataPlotter[1]] ##
DataPlotterDictionary = [1,2,3,4,5,6,7,8,9,11,16,18,21,24,27,30,33,35,37,39,41,42];


########### Functions ###########

# initialising function
def init():
    # initialise the position of the top half of the sample #
    X=[1, 4, 4, 3, 3, 2.8, 2.2, 2, 2, 1]
    Y=[10, 10, 9, 8, 4.96, 3.1, 3.1, 4.96, 8, 9]
    top_of_sample_source.data = dict(x=X, y=Y)

# function which pulls the sample with a force F (new)
def Pull(attrname, old, new):
    # use loaded data
    global DataPlotter, DataPlotterDictionary
    
    # get index value for DataPlotterDictionary from Force value
    i=min(new//5,20)
    
    # if the plot has not yet been drawn up to this value of sigma,
    # update the plot
    if (DataPlotterDictionary[i]>len( plot_source_theory.data['eps'])):
         plot_source_theory.data = dict(eps=DataPlotter[0:DataPlotterDictionary[i],0],sig=DataPlotter[0:DataPlotterDictionary[i],1])
         plot_source_practical.data = dict(eps=DataPlotter[0:DataPlotterDictionary[i],0],sig=DataPlotter[0:DataPlotterDictionary[i],2])
    
    # calculate length change and use it to update the figure
    if (i<20):
        dL= plot_source_practical.data['eps'][DataPlotterDictionary[i]-1]*L
    else:
        dL= plot_source_practical.data['eps'][DataPlotterDictionary[20]-1]*L+(new-100)*0.05
    draw(dL,new)
    
    
    if (new==75):
        global Sig_B, Sig_B_text, Sig_B_text_B
        Sig_B.visible=True
        Sig_B_text.visible=True
        Sig_B_text_B.visible=True
    elif (new==50):
        global Sig_S, Sig_S_text, Sig_S_text_S
        Sig_S.visible=True
        Sig_S_text.visible=True
        Sig_S_text_S.visible=True
    elif (new==45):
        global Sig_P, Sig_P_text, Sig_P_text_P
        Sig_P.visible=True
        Sig_P_text.visible=True
        Sig_P_text_P.visible=True
    """
    elif(new==??):
    """
    
    """
    ## attempt to make movement smoother, failed as I can't find a way
    ## to force bokeh to update now rather than waiting until the end
    ## of the function "Pull"
    
    i=new//5
    j=int(old//5)
    l=min(i,j)
    if (i<20):
        nSteps=abs(DataPlotterDictionary[i]-DataPlotterDictionary[j])
        for k in range(0,DataPlotterDictionary[i]-DataPlotterDictionary[j],DataPlotterDictionary[i]-DataPlotterDictionary[j]):
            # calculate the change in length of the sample
            dL= plot_source_practical.data['eps'][DataPlotterDictionary[j]+k+1]*L
            F = plot_source_practical.data['sig'][DataPlotterDictionary[j]+k+1]
        draw(dL,F);
        if (k!=nSteps-1):
            print "zzzzzz"
            #push_session()
            #session().store_obj(top_sample_line_source)
            sleep(1)
    else:
        for k in range(0,i-j,i-j):
            # calculate the change in length of the sample after breakage
            dL= plot_source_practical.data['eps'][DataPlotterDictionary[20]-1]*L+float((new-100)*0.05*(k+1))/float(i-j)
            F = old + (new-old)*float(k+1)/float(i-j)
            print dL, F
        draw(dL,F);
        if (k!=nSteps-1):
            #push_session()
            sleep(1)
    """

def draw(dL,F):
    # update circle showing current position on plot
    current_coords.data = dict(eps=[float(dL)/L],sig=[F])
    
    # Only display the dL arrow and label if dL=/=0
    if (dL==0):
        dL_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[])
        global dL_text
        dL_text.visible = False
    else:
        dL_arrow_source.data = dict(xS=[0], xE=[0], yS=[8], yE=[8+dL])
        dL_text.visible = True
    
    # update length of L arrow
    L_arrow_source.data = dict(xS=[-1], xE=[-1], yS=[3], yE=[8+dL])
    # update top line
    top_sample_line_source.data = dict(x=[-3,8], y=[8+dL,8+dL])
    # update force arrow
    F_arrow_source.data = dict(xS=[2.5],xE=[2.5],yS=[9+dL],yE=[10.5+dL])
    F_label_source.data = dict(x=[2.5],y=[10.6+dL],F=['F'])
    
    # calculate the new positions of the sample
    X=[1, 4, 4, 3, 3, 2.8, 2.2, 2, 2, 1]
    Y=[10, 10, 9, 8, 4.96, 3.1, 3.1, 4.96, 8, 9]
    top_of_sample_source.data = dict(x=X, y=(Y+dL))
    
    # manage surface labels
    if (dL>5):
        # remove S after break
        S_width_source.data = dict(xS=[],xE=[],yS=[],yE=[])
        S_label_glyph.text_alpha=0
    elif (dL>0.54):
        # ensure S is visible
        S_label_glyph.text_alpha=1
        # update label position (account for width change)
        XX=0.2*(dL/2.0-0.54)/1.86
        Y=5.5+dL/2
        S_label_source.data = dict(x=[2.3],y=[Y+0.5], S=['S'])
        S_width_source.data = dict(xS=[2+XX],xE=[3-XX],yS=[Y],yE=[Y])
    else:
        # ensure S is visible
        S_label_glyph.text_alpha=1
        # update label position
        Y=5.5+dL/2
        S_label_source.data = dict(x=[2.3],y=[Y+0.5], S=['S'])
        S_width_source.data = dict(xS=[2], xE=[3], yS=[Y],yE=[Y])

########### Main ###########

## Initialise
init()

## Draw sample
#  initialise drawing area
p = figure(title="Zugversuch (Tensile Testing)", tools="", x_range=(-5,9), y_range=(-0.5,17))
p.title.text_font_size="20pt"
#  remove graph lines
p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None
#  draw bottom section
p.patch([1, 4, 4, 3, 3, 2.8, 2.2, 2, 2, 1], [1, 1, 2, 3, 6.04, 7.9, 7.9, 6.04, 3, 2], 
    fill_color="#CCCCC6", line_color="#CCCCC6", line_width=2)
#  draw movable top section
p.patch(x='x', y='y', source=top_of_sample_source, fill_color="#CCCCC6", line_color="#CCCCC6", line_width=2)
p.line([-3,8],y=[8,8], line_color='#003359',line_dash=[4,4])
L0_arrow_glyph = Arrow(end=OpenHead(line_color="#003359",line_width=2,size=10),
    x_start=0, y_start=3, x_end=0, y_end=8,line_color="#003359",line_width=2)
p.add_layout(L0_arrow_glyph)
dL_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width=2,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=dL_arrow_source,line_color="#E37222",line_width=2)
p.add_layout(dL_arrow_glyph)
L_arrow_glyph = Arrow(end=OpenHead(line_color="black",line_width=2,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=L_arrow_source,line_color="black",line_width=2)
p.add_layout(L_arrow_glyph)
p.line(x='x', y='y', source=top_sample_line_source, line_color='#E37222',line_width=3)
p.line(x=[-3,8], y=[3,3], line_color='#E37222',line_width=3)
p.text(-0.5,5.5,text=[u"L\u2092"],text_color='#003359',text_font_size="15pt")
dL_text=p.text(0.3,8.5,text=["dL"],text_color='#E37222',text_font_size="15pt")
dL_text.visible = False
p.text(-1.5,5.5,text=["L"],text_color='black',text_font_size="15pt")
S0_arrow_glyph = Arrow(start=OpenHead(line_color="#003359",line_width=2, size=10),
    end=OpenHead(line_color="#003359",line_width=2, size=10),
    x_start=2, y_start=4, x_end=3, y_end=4,line_color="#003359",line_width=2)
p.add_layout(S0_arrow_glyph)
p.text(2.3,3.2,text=[u"S\u2092"],text_color='#003359',text_font_size="15pt")
S_arrow_glyph = Arrow(start=OpenHead(line_color="#003359",line_width=2, size=10),
    end=OpenHead(line_color="#003359",line_width=2, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=S_width_source,line_color="#003359",line_width=2)
p.add_layout(S_arrow_glyph)
S_label_glyph=LabelSet(x='x', y='y',text='S',text_color='#003359',text_font_size="15pt",level='glyph',source=S_label_source)
p.add_layout(S_label_glyph)
p.text(2.5,-0.5,text=["F"],text_color='#E37222',text_font_size="15pt",text_align="center")
F_down_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width=2,size=10),
    x_start=2.5, y_start=2, x_end=2.5, y_end=0.5,line_color="#E37222",line_width=2)
p.add_layout(F_down_arrow_glyph)
F_label_glyph=LabelSet(x='x', y='y',text='F',text_color='#E37222',text_font_size="15pt",
    level='glyph',source=F_label_source,text_align="center")
p.add_layout(F_label_glyph)
F_up_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222",line_width=2,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=F_arrow_source,line_color="#E37222",line_width=2)
p.add_layout(F_up_arrow_glyph)

## Create slider to choose force applied
Force_input = Slider(title="Kraft (Force)", value=0.0, start=0.0, end=110.0, step=5)
#Force_input.text_font_size="14pt"
Force_input.on_change('value',Pull)

## Create Plot
toolset = "pan,reset,resize,wheel_zoom"
plot = figure(title="Diagramm (Graph)", tools=toolset, x_range=[0,110], y_range=[0,120])
plot.title.text_font_size="20pt"
plot.xaxis.axis_label_text_font_size="14pt"
plot.yaxis.axis_label_text_font_size="14pt"
plot.xaxis.major_label_text_font_size="12pt"
plot.yaxis.major_label_text_font_size="12pt"
plot.xaxis.axis_label_text_font_style="normal"
plot.yaxis.axis_label_text_font_style="normal"
plot.xaxis.axis_label = u"\u03B5"
plot.yaxis.axis_label = u"\u03C3 [N/mm\u00B2]"
plot.line(x='eps', y='sig', source=plot_source_theory, legend=u"F/S\u2092", color='#0065BD')
plot.line(x='eps', y='sig', source=plot_source_practical, legend="F/S", color='#0065BD',line_dash=[4,4])
plot.legend.location="top_left"
plot.legend.label_text_font_size="14pt"
plot.circle(x='eps', y='sig', source=current_coords, color='black', radius=1)
#add sigma labels
Sig_B=plot.line([0, 100], [67.2, 67.2], color='#E37222')
Sig_S=plot.line([0, 100], [50, 50], color='#E37222')
Sig_P=plot.line([0, 100], [41.5, 41.5], color='#E37222')
Sig_B_text=plot.text(101,65,text=[u"\u03C3"],text_color="#E37222",text_font_size="12pt")
Sig_B_text_B=plot.text(103.5,64.5,text=["B"],text_color="#E37222",text_font_size="8pt")
Sig_S_text=plot.text(101,48,text=[u"\u03C3"],text_color="#E37222",text_font_size="12pt")
Sig_S_text_S=plot.text(103.5,47.5,text=["S"],text_color="#E37222",text_font_size="8pt")
Sig_P_text=plot.text(101,39.5,text=[u"\u03C3"],text_color="#E37222",text_font_size="12pt")
Sig_P_text_P=plot.text(103.5,39,text=["P"],text_color="#E37222",text_font_size="8pt")
#make sigma labels invisible until sufficiently plotted
Sig_B.visible=False
Sig_S.visible=False
Sig_P.visible=False
Sig_B_text.visible=False
Sig_S_text.visible=False
Sig_P_text.visible=False
Sig_B_text_B.visible=False
Sig_S_text_S.visible=False
Sig_P_text_P.visible=False

## Send to window
curdoc().add_root(column(row(p,plot),Force_input))
curdoc().title = "Zugversuch"
