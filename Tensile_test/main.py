from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.models import ColumnDataSource, Slider, LabelSet, Arrow, OpenHead, Button
from bokeh.io import curdoc
from numpy import loadtxt
from os.path import dirname, join, split

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
Elastic = True
MaxPlotted=0
MinPlasticPlotted=44

## Load Plotting Points from file ##
TheoryData = loadtxt('Tensile_test/TheoryData.txt');
PlasticData = loadtxt('Tensile_test/PlasticData.txt');

## Create arrays containing the points which need to be plotted for each
#  incrementation of the force slider
TheoryDataDictionary = loadtxt('Tensile_test/TheoryDataDictionary.txt',int);
PlasticDataDictionary = loadtxt('Tensile_test/PlasticDataDictionary.txt',int);

########### Functions ###########

# initialising function
def init():
    # initialise the position of the top half of the sample #
    X=[1, 4, 4, 3, 3, 2.8, 2.2, 2, 2, 1]
    Y=[10, 10, 9, 8, 4.96, 3.1, 3.1, 4.96, 8, 9]
    top_of_sample_source.data = dict(x=X, y=Y)

def Pull(attrname,old,new):
    global MaxPlotted, TheoryData, TheoryDataDictionary, MinPlasticPlotted, L
    global PlasticData, PlasticDataDictionary, plot_source_theory, plot_source_practical
    # if the plot has changed
    if (new>MaxPlotted):
        if(new<102.5):
            # if this is a change where the point is on the graph, 
            # update the extent of the graph
            MaxPlotted=new
        else:
            # if the point has exited the graph ensure that everything that needs to be plotted has been plotted
            MaxPlotted=102
            Eps=list(PlasticData[PlasticDataDictionary[MinPlasticPlotted]:PlasticDataDictionary[MaxPlotted]+1,0])
            SigP=list(PlasticData[PlasticDataDictionary[MinPlasticPlotted]:PlasticDataDictionary[MaxPlotted]+1,1])
            plot_source_practical.data=dict(eps=Eps,sig=SigP)
        # check if any new lines have appeared and if so plot them
        # (this cannot be done with if/else statements in case the slider is moved too quickly)
        if (new>=75):
            global Sig_B, Sig_B_text, Sig_B_text_B
            Sig_B.visible=True
            Sig_B_text.visible=True
            Sig_B_text_B.visible=True
        if (new>=50):
            global Sig_S, Sig_S_text, Sig_S_text_S
            Sig_S.visible=True
            Sig_S_text.visible=True
            Sig_S_text_S.visible=True
        if (new>=45):
            global Sig_P, Sig_P_text, Sig_P_text_P
            Sig_P.visible=True
            Sig_P_text.visible=True
            Sig_P_text_P.visible=True
        
        # plot the new theoretical line
        Eps=list(TheoryData[0:TheoryDataDictionary[MaxPlotted]+1,0])
        Sig=list(TheoryData[0:TheoryDataDictionary[MaxPlotted]+1,1])
        plot_source_theory.data=dict(eps=Eps,sig=Sig)
        # plot the new practical line
        if (MaxPlotted<50):
            # if the elastic limit is not yet reached then it can be plotted similarly
            SigP=list(TheoryData[0:TheoryDataDictionary[MaxPlotted]+1,2])
            Eps=list(TheoryData[0:TheoryDataDictionary[MaxPlotted]+1,0])
            plot_source_practical.data=dict(eps=Eps,sig=SigP)
        else:
            # if the elastic limit has been reached then the plastic data is also included
            Eps=list(PlasticData[PlasticDataDictionary[MinPlasticPlotted]:PlasticDataDictionary[MaxPlotted]+1,0])
            SigP=list(PlasticData[PlasticDataDictionary[MinPlasticPlotted]:PlasticDataDictionary[MaxPlotted]+1,1])
            plot_source_practical.data=dict(eps=Eps,sig=SigP)
    
    # plot the new experimental line
    if (new>102.5):
        # if the material has broken then there is nothing to plot
        # dL is calculated to position the black dot and the image
        dL= PlasticData[-1,0]*L+(new-102)*0.05
    elif (MaxPlotted>49):
        # if the material has passed the elastic limit
        if (new<MinPlasticPlotted):
            # if the plot has changed then update it
            MinPlasticPlotted=new
            Eps=list(PlasticData[PlasticDataDictionary[MinPlasticPlotted]:PlasticDataDictionary[MaxPlotted]+1,0])
            SigP=list(PlasticData[PlasticDataDictionary[MinPlasticPlotted]:PlasticDataDictionary[MaxPlotted]+1,1])
            plot_source_practical.data=dict(eps=Eps,sig=SigP)
        # dL is calculated to position the black dot and the image
        dL = PlasticData[PlasticDataDictionary[new],0]*L
    else:
        # dL is calculated to position the black dot and the image
        dL = TheoryData[TheoryDataDictionary[new],0]*L
    
    # the black dot and the image are positioned
    draw(dL,new)

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
Force_input = Slider(title="Kraft (Force)", value=0.0, start=0.0, end=110.0, step=1)
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

def reset():
    global plot_source_theory, plot_source_practical, Elastic, MaxPlotted, MinPlasticPlotted
    init()
    Elastic = True
    MaxPlotted=0
    MinPlasticPlotted=44
    plot_source_theory.data=dict(eps=[], sig=[])
    plot_source_practical.data=dict(eps=[], sig=[])
    if (Force_input.value==0):
        Pull(None,0,0)
    else:
        Force_input.value=0
    global Sig_B, Sig_B_text, Sig_B_text_B, Sig_S, Sig_S_text, Sig_S_text_S, Sig_P, Sig_P_text, Sig_P_text_P
    Sig_B.visible=False
    Sig_B_text.visible=False
    Sig_B_text_B.visible=False
    Sig_S.visible=False
    Sig_S_text.visible=False
    Sig_S_text_S.visible=False
    Sig_P.visible=False
    Sig_P_text.visible=False
    Sig_P_text_P.visible=False

reset_button=Button(label="Reset", button_type="success")
reset_button.on_click(reset)

## Send to window
curdoc().add_root(column(row(p,plot),row(Force_input,Spacer(width=400),reset_button)))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
