from __future__ import division
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import Slider, Button, Div, Arrow, OpenHead, Range1d, Label, Select, ColumnDataSource, NormalHead, LabelSet
from math import cos, sin, radians, sqrt, pi, atan2, exp
from os.path import dirname, join, split
import numpy as np
from scipy import signal
from scipy.special import sici

from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv, LatexSlider, LatexLabel, LatexLabelSet

## when the app is started, f(t) = rect(t)
initial_func = "rect(t)"

## when a new function f(t) is selected, the modification is always set to "Shifting"
initial_mod = "Shifting"

## frequency of sine and cosine function: sin(w0*t) and cos(w0*t)
w0 = 12

## inittial time and frequency range
time_range = Range1d(-4,4)
frequency_range = Range1d(-20,20)

## create arrays with time/frequency values for plotting
x_start = -4
x_end = 4
x_start_FT = -20
x_end_FT = 20
x = np.linspace(x_start, x_end, int(round((x_end-x_start)/0.01)))
x_Im = [] # needed for "Multiplication with exponential function"
x_FT = np.linspace(x_start_FT, x_end_FT, int(round((x_end_FT-x_start_FT)/0.01)))

## initialize arrays for plotting f(t) and F(w)
y = []
y_FT_Re = []
y_FT_Im = []
y_mod_Re = []
y_mod_Im = []
y_FT_Re_mod = []
y_FT_Im_mod = []
y_func_time = [0,0]
y_func_freq = [0,0]
y_mod_time = [0,0]
y_mod_freq = [0,0]

## initial modification 
text_mod = ["f^{*}(t)=f(t-\\lambda)"]
text_FT_mod = ["e^{-i\\lambda\\omega}F(\\omega)"]
with_text =["with"]
lambda_input = LatexSlider(title="\\lambda =", value=0, start=-3, end=3, step=0.1, width=250)

## when the app is started, f(t) = rect(t)
for i in range(0,len(x)):
    t = x[i]
    if t < -0.5 or t > 0.5:
        y.append(0.0)
        y_mod_Re.append(0.0)
    elif t >= -0.5 and t <= 0.5:
        y.append(1.0)
        y_mod_Re.append(1.0)
for i in range(0,len(x_FT)):
    w = x_FT[i]
    if w != 0:
        y_FT_Re.append(2.0*sin(w*0.5)/w)
        y_FT_Re_mod.append(2.0*sin(w*0.5)/w)
    elif w == 0:
        y_FT_Re.append(1.0)
        y_FT_Re_mod.append(1.0)
    y_FT_Im.append(0)
    y_FT_Im_mod.append(0)
    
## initial y-range for f(t) and F(w)
value_range = Range1d(min(y)-0.5,max(y)+0.5)
value_range_FT = Range1d(min(y_FT_Re)-0.5,max(y_FT_Re)+0.5)

## if the user selects a new function f(t), f(t) and its fourier transform F(ω) are plotted
def changeFunc(attr,old,new):
    line_mod_freq_Re.visible = True # if a new function is selected, y_FT_Re_mod is set to visible (y_FT_Re_mod is set to invisible 
                                    # when the dirac delta function is selected and the function is scaled with λ=0)
    if new == "\u03B4(t)":
        mod_select.options = ["Shifting","Scaling", "Multiplication with exponential function", "Multiplication with other function", 
        "Convolution with other function", "Linear combination"] # Differentiation is not defined for the dirac delta function
    else:
        mod_select.options = ["Shifting","Scaling", "Multiplication with exponential function", "Multiplication with other function", 
        "Convolution with other function", "Differentiation","Linear combination"]
    ## set new x-axis limits for each function
    if new == "rect(t)":
        func_time_plot.x_range.end = 4
        func_freq_plot.x_range.end = 20
        func_time_plot.x_range.start = -4
        func_freq_plot.x_range.start = -20
    elif new == "sinc(t)":
        func_time_plot.x_range.end = 10
        func_freq_plot.x_range.end = w0+1.5
        func_time_plot.x_range.start = -10
        func_freq_plot.x_range.start = -w0-1.5
    elif new == "\u03B4(t)":
        func_time_plot.x_range.end = 3.5
        func_freq_plot.x_range.end = w0+0.5
        func_time_plot.x_range.start = -3.5
        func_freq_plot.x_range.start = -w0-0.5
    elif new == "1":
        func_time_plot.x_range.end = 5
        func_freq_plot.x_range.end = w0+0.5
        func_time_plot.x_range.start = -5
        func_freq_plot.x_range.start = -w0-0.5
    elif new == "sin(12t)":
        func_time_plot.x_range.end = 2
        func_freq_plot.x_range.end = 2*w0+1
        func_time_plot.x_range.start = -2
        func_freq_plot.x_range.start = -2*w0-1
    elif new == "cos(12t)":
        func_time_plot.x_range.end = 2
        func_freq_plot.x_range.end = 2*w0+1
        func_time_plot.x_range.start = -2
        func_freq_plot.x_range.start = -2*w0-1
    function(new, x, x_Im, x_FT)
    update_all_arrows_and_y_values()
    update_value_range(y, y_mod_Re, y_mod_Im, y_FT_Re, y_FT_Im, y_FT_Re_mod, y_FT_Im_mod, y_func_time, y_func_freq, 
                       y_mod_time, y_mod_freq)
    ## modification is set to "Shifting" with λ = 0, so that f*(t) = f(t)
    changeMod(0,0,"Shifting") 
    mod_select.value = "Shifting"
    

## calculates the new functions f(t), f*(t), F(w) and F*(w) and plots them 
def function(new, x, x_Im, x_FT):
    global y, y_FT_Im, y_FT_Re, y_mod_Re, y_FT_Im_mod, y_FT_Re_mod
    if new == "rect(t)":
        for i in range(0,len(x)):
            t = x[i]
            if t < -0.5 or t > 0.5:
                y[i]=0.0
                y_mod_Re[i]=0.0
            elif t >= -0.5 and t <= 0.5:
                y[i]=1.0
                y_mod_Re[i]=1.0
        for i in range(0,len(x_FT)):
            w = x_FT[i]
            if w != 0:
                y_FT_Re[i]=2.0*sin(w*0.5)/w
                y_FT_Re_mod[i]=2.0*sin(w*0.5)/w
            elif w == 0:
                y_FT_Re[i]=1.0
                y_FT_Re_mod[i]=1.0
            y_FT_Im[i]=0
            y_FT_Im_mod[i]=0
    elif new == "sinc(t)":
        for i in range(0,len(x)):
            t = x[i]
            if t != 0:
                y[i] = sin(t)/t
                y_mod_Re[i]=sin(t)/t
            elif t == 0:
                y[i] = 1.0
                y_mod_Re[i]=1.0
        for i in range(0,len(x_FT)):
            w = x_FT[i]
            y_FT_Im[i]=0.0
            y_FT_Im_mod[i]=0.0
            if w < -1 or w > 1:
                y_FT_Re[i]=0.0
                y_FT_Re_mod[i]=0.0
            elif w >= -1 and w <= 1:
                y_FT_Re[i]=pi
                y_FT_Re_mod[i]=pi
    elif new == "\u03B4(t)":
        for i in range(0,len(x)):
            y[i] = 0
            y_mod_Re[i] = 0
        for i in range(0,len(x_FT)):
            y_FT_Re[i]=1.0
            y_FT_Re_mod[i]=1.0
            y_FT_Im[i]=0.0
            y_FT_Im_mod[i]=0.0    
    elif new == "1":
        for i in range(0,len(x)):
            y[i] = 1.0
            y_mod_Re[i] = 1.0
        for i in range(0,len(x_FT)):
            y_FT_Im[i] = 0.0
            y_FT_Im_mod[i] = 0.0
            y_FT_Re[i] = 0
            y_FT_Re_mod[i] = 0
    elif new == "sin(12t)":
        for i in range(0,len(x)):
            t = x[i]
            y[i] = sin(w0*t)  
            y_mod_Re[i]=sin(w0*t)
        for i in range(0,len(x_FT)):
            y_FT_Re[i] = 0.0
            y_FT_Re_mod[i]=0.0
            y_FT_Im[i]=0
            y_FT_Im_mod[i] = 0
    elif new == "cos(12t)":
        for i in range(0,len(x)):
            t = x[i]
            y[i] = cos(w0*t)  
            y_mod_Re[i]=cos(w0*t)
        for i in range(0,len(x_FT)):   
            y_FT_Im[i] = 0.0
            y_FT_Im_mod[i]=0.0
            y_FT_Re[i] = 0
            y_FT_Re_mod[i] = 0
    update_functions(x, x_Im, x_FT, y, y_mod_Re, y_mod_Im, y_FT_Re, y_FT_Im, y_FT_Re_mod, y_FT_Im_mod)

## create a drop-down for all possible functions f(t)
func_select = Select(title="Input function f(t):", value=initial_func,
    options=["rect(t)","sinc(t)", "\u03B4(t)", "1", "sin(12t)", "cos(12t)"], width = 430)
func_select.on_change('value',changeFunc)

## define ColumnDataSources for the lines
func_time_source = ColumnDataSource(data=dict(x=x,y=y)) 
func_freq_Re_source = ColumnDataSource(data=dict(x=x_FT,y=y_FT_Re)) 
func_freq_Im_source = ColumnDataSource(data=dict(x=x_FT,y=y_FT_Im))
mod_time_Re_source = ColumnDataSource(data=dict(x=x,y=y_mod_Re)) 
mod_time_Im_source = ColumnDataSource(data=dict(x=x_Im,y=y_mod_Im))
mod_freq_Re_source = ColumnDataSource(data=dict(x=x_FT,y=y_FT_Re_mod))
mod_freq_Im_source = ColumnDataSource(data=dict(x=x_FT,y=y_FT_Im_mod))
## define ColumnDataSources for the arrows
arrow_func_time_source = ColumnDataSource(data = dict(x1=[],y1=[],x2=[],y2=[]))
arrow_func_freq_Re_source = ColumnDataSource(data = dict(x1=[],y1=[],x2=[],y2=[]))
arrow_func_freq_Im_source = ColumnDataSource(data = dict(x1=[],y1=[],x2=[],y2=[]))
arrow_func_freq_Re_source2 = ColumnDataSource(data = dict(x1=[],y1=[],x2=[],y2=[]))
arrow_func_freq_Im_source2 = ColumnDataSource(data = dict(x1=[],y1=[],x2=[],y2=[]))
arrow_mod_time_source = ColumnDataSource(data = dict(x1=[],y1=[],x2=[],y2=[]))
arrow_mod_time_source2 = ColumnDataSource(data = dict(x1=[],y1=[],x2=[],y2=[]))
arrow_mod_freq_Re_source = ColumnDataSource(data = dict(x1=[],y1=[],x2=[],y2=[]))
arrow_mod_freq_Re_source2 = ColumnDataSource(data = dict(x1=[],y1=[],x2=[],y2=[]))
arrow_mod_freq_Re_source3 = ColumnDataSource(data = dict(x1=[],y1=[],x2=[],y2=[]))
arrow_mod_freq_Im_source = ColumnDataSource(data = dict(x1=[],y1=[],x2=[],y2=[]))
arrow_mod_freq_Im_source2 = ColumnDataSource(data = dict(x1=[],y1=[],x2=[],y2=[]))
## define ColumnDataSources for the modification rules
modification_source = ColumnDataSource(data=dict(t=text_mod))
modification_result_source = ColumnDataSource(data=dict(t=text_FT_mod))
with_source = ColumnDataSource(data=dict(t=with_text))


## if the x-axis changes, the current shown functions are updated with the new x-range
def update_functions_with_new_x_range(current_mod, current_func):
    function(current_func, x, x_Im, x_FT)
    if current_mod == "Shifting" or current_mod == "Scaling" or current_mod == "Multiplication with exponential function":
        current_lamda = lambda_input.value
        if current_mod == "Shifting":
            change_lambda_shifting(0, 0, current_lamda)
        elif current_mod == "Scaling":
            change_lambda_scaling(0, 0, current_lamda)
        elif current_mod == "Multiplication with exponential function":
            change_lambda_exp(0, 0, current_lamda)
        lambda_input.value = current_lamda 
    elif current_mod == "Linear combination" or current_mod == "Multiplication with other function" or current_mod == "Convolution with other function":
        current_g = g_select.value
        if current_mod == "Linear combination":
            change_g_comb(0, 0, current_g)
        elif current_mod == "Multiplication with other function":
            change_g_mult(0, 0, current_g)
        elif current_mod == "Convolution with other function":
            change_g_conv(0, 0, current_g)
        g_select.value = current_g
    elif current_mod == "Differentiation":
        changeMod(0,0,current_mod)
    
## update x-range whenever the x-axis is changed for the functions in the time domain
def change_x_range(attr, old, new):
    global x_start, x_end, x, x_Im
    x_start = func_time_plot.x_range.start
    x_end = -x_start
    x = np.linspace(x_start, x_end, int(round((x_end-x_start)/0.01)))
    x_Im = np.linspace(x_start, x_end, int(round((x_end-x_start)/0.01)))
    current_mod = mod_select.value
    current_func = func_select.value
    set_y_length()
    update_functions_with_new_x_range(current_mod, current_func)

## update x-range whenever the x-axis is changed for the functions in the frequency domain
def change_x_range_FT(attr, old, new):
    global x_start_FT, x_end_FT, x_FT
    x_start_FT = func_freq_plot.x_range.start
    x_end_FT = -x_start_FT
    x_FT = np.linspace(x_start_FT, x_end_FT, int(round((x_end_FT-x_start_FT)/0.01)))
    current_mod = mod_select.value
    current_func = func_select.value
    set_y_length()
    update_functions_with_new_x_range(current_mod, current_func)

## plot of f(t)
func_time_plot = figure(plot_width = 500,plot_height= 300,x_range = time_range,y_range = value_range, tools = "xzoom_in,xzoom_out")
func_time_plot.x_range.on_change('start',change_x_range)
func_time_plot.axis.axis_label_text_font_size="12pt"
func_time_plot.xaxis.axis_label="t"
func_time_plot.yaxis.axis_label="f(t)"
func_time_plot.axis.axis_label_text_font_style="normal"
func_time_plot.toolbar.logo = None
func_time_plot.line(x='x',y='y', source = func_time_source, color='#3070b3',line_width=2)
arrow_func_time = Arrow(end=NormalHead(fill_color="#3070b3",line_color="#3070b3",size=10),line_color="#3070b3",line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=arrow_func_time_source)
func_time_plot.add_layout(arrow_func_time)

## plot of F(ω)
func_freq_plot = figure(plot_width = 500,plot_height= 300,x_range = frequency_range,y_range = value_range_FT, tools="xzoom_in,xzoom_out")
func_freq_plot.x_range.on_change('start',change_x_range_FT)
func_freq_plot.axis.axis_label_text_font_size="12pt"
func_freq_plot.xaxis.axis_label="ω"
func_freq_plot.yaxis.axis_label="F(ω)"
func_freq_plot.axis.axis_label_text_font_style="normal"
func_freq_plot.toolbar.logo = None
func_freq_plot.line(x='x',y='y', source = func_freq_Re_source, color='#e37222', legend_label='Re(F)',line_width=2)
func_freq_plot.line(x='x',y='y', source = func_freq_Im_source, color='#a2ad00', legend_label='Im(F)', line_dash='dashed',line_width=2)
arrow_func_freq_Re = Arrow(end=NormalHead(fill_color="#e37222",line_color="#e37222",size=10),line_color="#e37222",line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=arrow_func_freq_Re_source)
func_freq_plot.add_layout(arrow_func_freq_Re)
arrow_func_freq_Im = Arrow(end=NormalHead(fill_color="#a2ad00",line_color="#a2ad00",size=10),line_color="#a2ad00",line_dash='dashed',line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=arrow_func_freq_Im_source)
func_freq_plot.add_layout(arrow_func_freq_Im)
arrow_func_freq_Re2 = Arrow(end=NormalHead(fill_color="#e37222",line_color="#e37222",size=10),line_color="#e37222",line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=arrow_func_freq_Re_source2)
func_freq_plot.add_layout(arrow_func_freq_Re2)
arrow_func_freq_Im2 = Arrow(end=NormalHead(fill_color="#a2ad00",line_color="#a2ad00",size=10),line_color="#a2ad00",line_dash='dashed',line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=arrow_func_freq_Im_source2)
func_freq_plot.add_layout(arrow_func_freq_Im2)

## plot of modificated f*(t)
mod_time_plot = figure(plot_width = 500,plot_height= 300,x_range = time_range,y_range = value_range, tools="xzoom_in,xzoom_out")
mod_time_plot.axis.axis_label_text_font_size="12pt"
mod_time_plot.xaxis.axis_label="t"
mod_time_plot.yaxis.axis_label="f(t)"
mod_time_plot.axis.axis_label_text_font_style="normal"
mod_time_plot.toolbar.logo = None
mod_time_plot.line(x='x',y='y', source = mod_time_Re_source, color='#3070b3',legend_label='Re(f)',line_width=2)
mod_time_plot.line(x='x',y='y', source = mod_time_Im_source, color='black',legend_label='Im(f)',line_dash='dashed',line_width=2)
arrow_mod_time = Arrow(end=NormalHead(fill_color="#3070b3",line_color="#3070b3",size=10),line_color="#3070b3",line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=arrow_mod_time_source)
mod_time_plot.add_layout(arrow_mod_time)
arrow_mod_time2 = Arrow(end=NormalHead(fill_color="#3070b3",line_color="#3070b3",size=10),line_color="#3070b3",line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=arrow_mod_time_source2)
mod_time_plot.add_layout(arrow_mod_time2)

## plot of modificated F*(ω)
mod_freq_plot = figure(plot_width = 500,plot_height= 300,x_range = frequency_range,y_range = value_range_FT, tools="xzoom_in,xzoom_out")
mod_freq_plot.axis.axis_label_text_font_size="12pt"
mod_freq_plot.xaxis.axis_label="ω"
mod_freq_plot.yaxis.axis_label="F(ω)"
mod_freq_plot.axis.axis_label_text_font_style="normal"
mod_freq_plot.toolbar.logo = None
line_mod_freq_Re = mod_freq_plot.line(x='x',y='y', source = mod_freq_Re_source, color='#e37222', legend_label='Re(F)',line_width=2)
mod_freq_plot.line(x='x',y='y', source = mod_freq_Im_source, color='#a2ad00', legend_label='Im(F)',line_dash='dashed',line_width=2)
arrow_mod_freq_Re = Arrow(end=NormalHead(fill_color="#e37222",line_color="#e37222",size=10),line_color="#e37222",line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=arrow_mod_freq_Re_source)
mod_freq_plot.add_layout(arrow_mod_freq_Re)
arrow_mod_freq_Im = Arrow(end=NormalHead(fill_color="#a2ad00",line_color="#a2ad00",size=10),line_color="#a2ad00",line_dash='dashed',line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=arrow_mod_freq_Im_source)
mod_freq_plot.add_layout(arrow_mod_freq_Im)
arrow_mod_freq_Re2 = Arrow(end=NormalHead(fill_color="#e37222",line_color="#e37222",size=10),line_color="#e37222",line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=arrow_mod_freq_Re_source2)
mod_freq_plot.add_layout(arrow_mod_freq_Re2)
arrow_mod_freq_Im2 = Arrow(end=NormalHead(fill_color="#a2ad00",line_color="#a2ad00",size=10),line_color="#a2ad00",line_dash='dashed',line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=arrow_mod_freq_Im_source2)
mod_freq_plot.add_layout(arrow_mod_freq_Im2)
arrow_mod_freq_Re3 = Arrow(end=NormalHead(fill_color="#e37222",line_color="#e37222",size=10),line_color="#e37222",line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=arrow_mod_freq_Re_source3)
mod_freq_plot.add_layout(arrow_mod_freq_Re3)

## add app description
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)

## figure which draws the Fourier Transform symbol o--o
fig = figure(title="", tools = "", x_range=(-5,5), y_range=(-5,5),width=150,height=130)
fig.axis.visible = False
fig.grid.visible = False
fig.outline_line_color = None
fig.toolbar.logo = None
fig.line(x=[-2.5,2.5],y=[0,0],color="black",line_width=2)
fig.ellipse(x=-3,y=0,width=1,height=1,line_color="black",fill_color=None,line_width=2)
fig.ellipse(x=3,y=0,width=1,height=1,line_color="black",fill_color="black",line_width=2)
fig.add_layout(Label(x=0,y=1.5,text="FT",text_color='black',text_font_size="12pt",text_baseline="middle",text_align="center"))

## figure which shows the rule that is applied to the modificated function f*(t)
modification = figure(title="", tools = "", x_range=(0,75), y_range=(-5,5),width=375,height=60)
modification.axis.visible = False
modification.grid.visible = False
modification.outline_line_color = None
modification.toolbar.logo = None
modification.add_layout(LatexLabelSet(x=0,y=0,text="t",text_color='black',text_font_size="9pt",level='overlay',text_baseline="middle", source=modification_source))
modification.line(x=[35,38],y=[-0.5,-0.5],color="black",line_width=1)
modification.ellipse(x=34.5,y=-0.5,width=1.0,height=1.0,line_color="black",fill_color=None,line_width=0.5)
modification.ellipse(x=38.5,y=-0.5,width=1.0,height=1.0,line_color="black",fill_color="black",line_width=0.5)
modification.add_layout(LatexLabelSet(x=41,y=0,text="t",text_color='black',text_font_size="9pt",level='overlay',text_baseline="middle", source=modification_result_source))
modification.add_layout(LabelSet(x=68,y=-0.5,text="t",text_color='black',text_font_size="9pt",level='overlay',text_baseline="middle", source=with_source))

## if the modification is changed, the rule and the slider/drop-down changes
def changeMod(attr, old, new):
    global text_mod, text_FT_mod, lambda_input, with_text, y_mod_Im, y_mod_Re, y_FT_Im_mod, y_FT_Re_mod, g_select, y_mod_time, y_mod_freq, x_Im, y_mod_Im
    line_mod_freq_Re.visible = True # if a new modification is selected, y_FT_Re_mod is set to visible (y_FT_Re_mod is set to invisible 
                                    # when the dirac delta function is selected and the function is scaled with λ=0)

    y_mod_time = y_func_time # when a new modification is selected, f*(t) = f(t) and F*(w) = F(w)
    y_mod_freq = y_func_freq 

    if new == "Multiplication with exponential function":
        x_Im = np.linspace(x_start, x_end, int(round((x_end-x_start)/0.01)))
        y_mod_Im = np.zeros(len(x_Im))
    else: # no imaginary part, if f(t) isn't multiplicated with an exponential function
        x_Im = []
        y_mod_Im = []
    if new == "Scaling":
        text_mod = ["f^{*}(t)=f(\\lambda t)"]
        text_FT_mod = ["\\frac{1}{|\\lambda|}F\\left(\\frac{\\omega}{\\lambda}\\right)"]
        lambda_input = LatexSlider(title="\\lambda =", value=1, start=-3, end=3, step=0.2, width=250)
        lambda_input.on_change('value',change_lambda_scaling)
        with_text =["with"]
        layout.children[5] = row(Spacer(width=35),modification, column(Spacer(height=19),lambda_input))
    elif new == "Shifting":
        text_mod = ["f^{*}(t)=f(t-\\lambda)"]
        text_FT_mod = ["e^{-i\\lambda\\omega}F(\\omega)"]
        lambda_input = LatexSlider(title="\\lambda =", value=0, start=-3, end=3, step=0.2, width=250)
        lambda_input.on_change('value',change_lambda_shifting)
        with_text =["with"]
        layout.children[5] = row(Spacer(width=35),modification, column(Spacer(height=19),lambda_input)) 
    elif new == "Multiplication with exponential function":
        text_mod = ["f^{*}(t)=f(t)e^{i\\lambda t}"]
        text_FT_mod = ["F(\\omega-\\lambda)"]
        lambda_input = LatexSlider(title="\\lambda =", value=0, start=-3, end=3, step=0.2, width=250)
        lambda_input.on_change('value',change_lambda_exp)
        with_text =["with"]
        layout.children[5] = row(Spacer(width=35),modification, column(Spacer(height=19),lambda_input)) 
    elif new == "Multiplication with other function":
        text_mod = ["f^{*}(t)=f(t)\\cdot g(t)"]
        text_FT_mod = ["\\frac{1}{2\\pi}(F(\\omega)*G(\\omega))"]
        g_select = Select(title="g(t):", value="1", options=["rect(t)","sinc(t)", "\u03B4(t)", "1", "sin(12t)", "cos(12t)"], width = 100)
        g_select.on_change('value',change_g_mult)
        if func_select.value == "rect(t)":
            g_select.options = ["sinc(t)", "\u03B4(t)", "1", "sin(12t)", "cos(12t)"]
        elif func_select.value == "\u03B4(t)":
            g_select.options = ["rect(t)", "sinc(t)", "1", "sin(12t)", "cos(12t)"]
        else:
            g_select.options = ["rect(t)", "sinc(t)", "\u03B4(t)", "1", "sin(12t)", "cos(12t)"]
        with_text =["with"]
        layout.children[5] = row(Spacer(width=35),modification, column(Spacer(height=19),g_select)) 
    elif new == "Convolution with other function":
        text_mod = ["f^{*}(t)=f(t)*g(t)"]
        text_FT_mod = ["F(\\omega)\\cdot G(\\omega))"]
        g_select = Select(title="g(t):", value="\u03B4(t)", options=["rect(t)","sinc(t)", "\u03B4(t)", "1", "sin(12t)", "cos(12t)"], width = 100)
        g_select.on_change('value',change_g_conv)
        if func_select.value == "sinc(t)":
            g_select.options = ["rect(t)", "\u03B4(t)", "1"]
        elif func_select.value == "1":
            g_select.options = ["rect(t)", "sinc(t)",  "\u03B4(t)"]
        elif func_select.value == "sin(12t)":
            g_select.options = ["rect(t)", "\u03B4(t)"]
        elif func_select.value == "cos(12t)":
            g_select.options = ["rect(t)", "\u03B4(t)"]
        else:
            g_select.options = ["rect(t)", "sinc(t)", "\u03B4(t)", "1", "sin(12t)", "cos(12t)"]
        with_text =["with"]
        layout.children[5] = row(Spacer(width=35),modification, column(Spacer(height=19),g_select))         
    elif new == "Differentiation":
        text_mod = ["f^{*}(t)=f^{(n)}(t)"]
        text_FT_mod = ["(i\\omega)^{n}F(\\omega)"]
        with_text =[""]
        layout.children[5] = row(Spacer(width=35),modification) 
        delete_mod_arrows()
        if func_select.value == "rect(t)":
            for i in range(0,len(x)):    
                y_mod_Re[i]=0
            for i in range(0,len(x_FT)):
                w = x_FT[i] 
                y_FT_Re_mod[i]=0
                y_FT_Im_mod[i]=2*sin(0.5*w)
            arrow_mod_time_source.stream(dict(x1=[-0.5],y1=[0],x2=[-0.5],y2=[1]),rollover=1)
            arrow_mod_time_source2.stream(dict(x1=[0.5],y1=[0],x2=[0.5],y2=[-1]),rollover=1)
            arrow_mod_time.visible = True
            arrow_mod_time2.visible = True
            y_mod_time = [-1, 1]
        elif func_select.value == "sinc(t)":
            for i in range(0,len(x)):
                t = x[i]
                if t != 0:
                    y_mod_Re[i]=-sin(t)/(t*t)+cos(t)/t
                elif t == 0:
                    y_mod_Re[i]=0
            for i in range(0,len(x_FT)):
                w = x_FT[i]
                y_FT_Re_mod[i]=0
                if w < -1 or w > 1:
                    y_FT_Im_mod[i]=0
                elif w>=-1 and w<=1:
                    y_FT_Im_mod[i]=w*pi
        elif func_select.value == "\u03B4(t)":
            ""
        elif func_select.value == "1":
            for i in range(0,len(x)):
                y_mod_Re[i]=0
            for i in range(0,len(x_FT)):
                y_FT_Re_mod[i]=0
                y_FT_Im_mod[i]=0
        elif func_select.value == "sin(12t)":
            for i in range(0,len(x)):
                t = x[i] 
                y_mod_Re[i]=cos(w0*t)*w0
            for i in range(0,len(x_FT)):
                y_FT_Im_mod[i]=0.0
                y_FT_Re_mod[i]=0
            arrow_mod_freq_Re_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[12*pi]),rollover=1)
            arrow_mod_freq_Re_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[12*pi]),rollover=1)
            arrow_mod_freq_Re.visible = True
            arrow_mod_freq_Re2.visible = True
            y_mod_freq = [0, 12*pi]
        elif func_select.value == "cos(12t)":
            for i in range(0,len(x)):
                t = x[i]
                y_mod_Re[i]=-sin(w0*t)*w0  
            for i in range(0,len(x_FT)):
                y_FT_Re_mod[i]=0.0
                y_FT_Im_mod[i]=0
            arrow_mod_freq_Im_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[-12*pi]),rollover=1)
            arrow_mod_freq_Im_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[12*pi]),rollover=1)
            arrow_mod_freq_Im.visible = True
            arrow_mod_freq_Im2.visible = True
            y_mod_freq = [-12*pi, 12*pi]
        update_mod_functions(x, x_Im, x_FT, y_mod_Re, y_mod_Im, y_FT_Re_mod, y_FT_Im_mod)
    elif new == "Linear combination":
        text_mod = ["f^{*}(t)=f(t)+g(t)"]
        text_FT_mod = ["F(\\omega)+G(\\omega)"]
        g_select = Select(title="g(t):", value="0", options=["0","rect(t)","sinc(t)", "\u03B4(t)", "1", "sin(12t)", "cos(12t)"], width = 100)
        g_select.on_change('value',change_g_comb)
        with_text =["with"]
        layout.children[5] = row(Spacer(width=35),modification, column(Spacer(height=19),g_select))
    modification_source.data = dict(t=text_mod)
    modification_result_source.data = dict(t=text_FT_mod)
    if new == "Differentiation":
        ""
    else:
        reset_mod_functions(x,x_Im,x_FT,y,y_mod_Re,y_mod_Im,y_FT_Im,y_FT_Re,y_FT_Im_mod,y_FT_Re_mod)
        update_all_arrows_and_y_values()
    with_source.data=dict(t=with_text)
    update_value_range(y, y_mod_Re, y_mod_Im, y_FT_Re, y_FT_Im, y_FT_Re_mod, y_FT_Im_mod, y_func_time, y_func_freq, 
                     y_mod_time, y_mod_freq)
    
## define all possible modifications       
mod_select = Select(title="Modification of input function f(t):", value=initial_mod,
    options=["Shifting","Scaling", "Multiplication with exponential function", "Multiplication with other function", "Convolution with other function",
    "Differentiation","Linear combination"], width = 430)
mod_select.on_change('value',changeMod)

## app layout
layout = column(description, row(Spacer(width=35), func_select), row(func_time_plot, column(Spacer(height=64),fig), 
    column(func_freq_plot)),Spacer(height=20), row(Spacer(width=35),mod_select),row(Spacer(width=35),modification, column(Spacer(height=19),
    lambda_input)), Spacer(height=10),row(mod_time_plot, column(Spacer(height=64),fig), column(mod_freq_plot)))

## when the x-range is changed, the corresponding y-array changes its length 
def set_y_length():
    global x_Im, y, y_mod_Re, y_mod_Im, y_FT_Im, y_FT_Re, y_FT_Im_mod, y_FT_Re_mod
    y = np.zeros(len(x))
    if mod_select.value == "Multiplication with exponential function":
        y_mod_Im = np.zeros(len(x_Im))
    else:
        y_mod_Im = []
        x_Im = []
    y_mod_Re = np.zeros(len(x))
    y_FT_Re = np.zeros(len(x_FT))
    y_FT_Im = np.zeros(len(x_FT))
    y_FT_Re_mod = np.zeros(len(x_FT))
    y_FT_Im_mod = np.zeros(len(x_FT)) 

## update modified functions f*(t) and F*(ω)
def update_mod_functions(x, x_Im, x_FT, y_mod_Re, y_mod_Im, y_FT_Re_mod, y_FT_Im_mod):
    mod_time_Re_source.data = dict(x=x,y=y_mod_Re)
    mod_freq_Re_source.data = dict(x=x_FT,y=y_FT_Re_mod) 
    mod_freq_Im_source.data = dict(x=x_FT, y=y_FT_Im_mod)
    mod_time_Im_source.data = dict(x=x_Im, y=y_mod_Im)


## reset modified function: f*(t) = f(t) and F*(ω) = F(ω)
def reset_mod_functions(x, x_Im, x_FT, y, y_mod_Re, y_mod_Im, y_FT_Im, y_FT_Re, y_FT_Im_mod, y_FT_Re_mod):
    for i in range(0,len(x)):
        y_mod_Re[i]=y[i]
    for i in range(0,len(x_FT)):
        y_FT_Im_mod[i]=y_FT_Im[i]
        y_FT_Re_mod[i]=y_FT_Re[i]
    update_mod_functions(x, x_Im, x_FT, y_mod_Re, y_mod_Im, y_FT_Re_mod, y_FT_Im_mod)

## update all functions
def update_functions(x, x_Im, x_FT, y, y_mod_Re, y_mod_Im, y_FT_Re, y_FT_Im, y_FT_Re_mod, y_FT_Im_mod):
    func_time_source.data = dict(x=x, y=y)
    mod_time_Re_source.data = dict(x=x,y=y_mod_Re)
    mod_time_Im_source.data = dict(x=x_Im,y=y_mod_Im)
    func_freq_Re_source.data = dict(x=x_FT,y=y_FT_Re) 
    func_freq_Im_source.data = dict(x=x_FT, y=y_FT_Im)
    mod_freq_Re_source.data = dict(x=x_FT,y=y_FT_Re_mod) 
    mod_freq_Im_source.data = dict(x=x_FT, y=y_FT_Im_mod)

## delete all arrows for the two modificated plots
def delete_mod_arrows():
    arrow_mod_time.visible = False
    arrow_mod_time2.visible = False
    arrow_mod_freq_Re.visible = False
    arrow_mod_freq_Im.visible = False
    arrow_mod_freq_Re2.visible = False
    arrow_mod_freq_Im2.visible = False
    arrow_mod_freq_Re3.visible = False

## sets the y-axis of all four plots according to the maximum and minimum value shown
def update_value_range(y, y_mod_Re, y_mod_Im, y_FT_Re, y_FT_Im, y_FT_Re_mod, y_FT_Im_mod, y_func_time, y_func_freq, 
                     y_mod_time, y_mod_freq):
    if y_mod_Im != []:
        func_time_plot.y_range.start = min(min(y),min(y_mod_Re),min(y_mod_Im),min(y_func_time),min(y_mod_time))-0.5
        func_time_plot.y_range.end = max(max(y),max(y_mod_Re),max(y_mod_Im),max(y_func_time),max(y_mod_time))+0.5
        
        func_freq_plot.y_range.start = min(min(y_FT_Re),min(y_FT_Im),min(y_FT_Re_mod),min(y_FT_Im_mod),
                                       min(y_func_freq),min(y_mod_freq))-0.5
        func_freq_plot.y_range.end = max(max(y_FT_Re),max(y_FT_Im),max(y_FT_Re_mod),max(y_FT_Im_mod),
                                     max(y_func_freq),max(y_mod_freq))+0.5
    else:
        func_time_plot.y_range.start = min(min(y),min(y_mod_Re),min(y_func_time),min(y_mod_time))-0.5
        func_time_plot.y_range.end = max(max(y),max(y_mod_Re),max(y_func_time),max(y_mod_time))+0.5
        
        func_freq_plot.y_range.start = min(min(y_FT_Re),min(y_FT_Im),min(y_FT_Re_mod),min(y_FT_Im_mod), 
                                       min(y_func_freq),min(y_mod_freq))-0.5
        func_freq_plot.y_range.end = max(max(y_FT_Re),max(y_FT_Im),max(y_FT_Re_mod),max(y_FT_Im_mod),
                                     max(y_func_freq),max(y_mod_freq))+0.5

## update all arrows for all four plots when f*(t) = f(t) and set the auxiliary variables y_func_time, y_func_freq, y_mod_time and 
## y_mod_freq according to the arrows so that the y-axis is scaled correctly
def update_all_arrows_and_y_values():
    global y_func_time, y_func_freq, y_mod_time, y_mod_freq
    # set all arrows to invisible and all auxiliary variables to zero
    arrow_func_time.visible = False
    arrow_func_freq_Re.visible = False
    arrow_func_freq_Im.visible = False
    arrow_func_freq_Re2.visible = False
    arrow_func_freq_Im2.visible = False
    delete_mod_arrows()
    y_func_time = [0,0]
    y_func_freq = [0,0]
    y_mod_time = [0,0]
    y_mod_freq = [0,0]
    if func_select.value == "\u03B4(t)":
        arrow_func_time_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[1]),rollover=1)
        arrow_mod_time_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[1]),rollover=1)
        arrow_func_time.visible = True
        arrow_mod_time.visible = True
        y_func_time = [0, 1]
        y_mod_time = [0, 1]
    elif func_select.value == "1":
        arrow_func_freq_Re_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[2*pi]),rollover=1)
        arrow_mod_freq_Re_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[2*pi]),rollover=1)
        arrow_func_freq_Re.visible = True
        arrow_mod_freq_Re.visible = True
        y_func_freq = [0, 2*pi]
        y_mod_freq = [0, 2*pi]
        y_func_time = [1, 1] # for f(t)=1, the min. value is 1
        y_mod_time = [1, 1] # for f*(t)=1, the min. value is 1
    elif func_select.value == "sin(12t)":
        arrow_func_freq_Im_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi]),rollover=1)
        arrow_func_freq_Im_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[-pi]),rollover=1)
        arrow_mod_freq_Im_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi]),rollover=1)
        arrow_mod_freq_Im_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[-pi]),rollover=1)
        arrow_func_freq_Im.visible = True
        arrow_func_freq_Im2.visible = True
        arrow_mod_freq_Im.visible = True
        arrow_mod_freq_Im2.visible = True
        y_func_freq = [-pi, pi]
        y_mod_freq = [-pi, pi]
    elif func_select.value == "cos(12t)":
        arrow_func_freq_Re_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi]),rollover=1) 
        arrow_func_freq_Re_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[pi]),rollover=1)
        arrow_mod_freq_Re_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi]),rollover=1)
        arrow_mod_freq_Re_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[pi]),rollover=1)
        arrow_func_freq_Re.visible = True
        arrow_func_freq_Re2.visible = True
        arrow_mod_freq_Re.visible = True
        arrow_mod_freq_Re2.visible = True
        y_func_freq = [0, pi]
        y_mod_freq = [0, pi]
    

 

## update modificated plots when f(t) is scaled by λ: f*(t) = f(λt)
def change_lambda_scaling(attr,old,new):
    global y_mod_Re, y_FT_Re_mod, y_FT_Im_mod, y_mod_freq, y_mod_time
    y_mod_freq = y_func_freq
    y_mod_time = y_func_time
    delete_mod_arrows()
    if func_select.value == "rect(t)":
        if new == 0:
            for i in range(0,len(x)):
                y_mod_Re[i]=1
            for i in range(0,len(x_FT)):
                y_FT_Im_mod[i]=0.0
                y_FT_Re_mod[i]=0
            arrow_mod_freq_Re_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[2*pi]),rollover=1)
            arrow_mod_freq_Re.visible = True
            y_mod_freq = [0, 2*pi]
        else:
            for i in range(0,len(x)):
                t = x[i]
                if t < -0.5/abs(new) or t > 0.5/abs(new):
                    y_mod_Re[i]=0.0
                elif t>=-0.5/abs(new) and t<=0.5/abs(new):
                    y_mod_Re[i]=1.0
            for i in range(0,len(x_FT)):
                w = x_FT[i]
                if w != 0:
                    y_FT_Re_mod[i]=2.0/abs(new)*sin(w*0.5/new)/(w/new)
                elif w == 0:
                    y_FT_Re_mod[i]=1/abs(new)
                y_FT_Im[i]=0
    elif func_select.value == "sinc(t)":
        if new == 0:
            for i in range(0,len(x)):
                y_mod_Re[i]=1
            for i in range(0,len(x_FT)):
                y_FT_Im_mod[i] = 0.0
                y_FT_Re_mod[i] = 0
            arrow_mod_freq_Re_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[2*pi]),rollover=1)
            arrow_mod_freq_Re.visible = True
            y_mod_freq = [0, 2*pi]
        else:
            for i in range(0,len(x)):
                t = x[i]
                if t != 0:
                    y_mod_Re[i]=sin(new*t)/(t*new)
                elif t == 0:
                    y_mod_Re[i]=1.0
            for i in range(0,len(x_FT)):
                w = x_FT[i]
                if w < -abs(new) or w > abs(new):
                    y_FT_Re_mod[i]=0.0
                elif w>=-abs(new) and w<=abs(new):
                    y_FT_Re_mod[i]=pi/abs(new)
                y_FT_Im_mod[i] = 0.0
    elif func_select.value == "sin(12t)":
        if new == 0:
            for i in range(0,len(x)):
                y_mod_Re[i]=0.0
            for i in range(0,len(x_FT)):
                y_FT_Im_mod[i]=0.0
                y_FT_Re_mod[i]=0.0
        else:
            for i in range(0,len(x)):
                t = x[i]
                y_mod_Re[i]=sin(w0*t*new)
            for i in range(0,len(x_FT)):
                y_FT_Re_mod[i]=0.0
                y_FT_Im_mod[i]=0.0
            arrow_mod_freq_Im_source.stream(dict(x1=[-new*w0],y1=[0],x2=[-new*w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Im_source2.stream(dict(x1=[new*w0],y1=[0],x2=[new*w0],y2=[-pi]),rollover=1)
            arrow_mod_freq_Im.visible = True
            arrow_mod_freq_Im2.visible = True
    elif func_select.value == "cos(12t)":
        if new == 0:
            for i in range(0,len(x)):
                y_mod_Re[i]=1
            for i in range(0,len(x_FT)):
                y_FT_Im_mod[i]=0.0
                y_FT_Re_mod[i]=0
            arrow_mod_freq_Re_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[2*pi]),rollover=1)
            arrow_mod_freq_Re.visible = True
            y_mod_freq = [0, 2*pi]
        else:
            for i in range(0,len(x)):
                t = x[i]
                y_mod_Re[i]=cos(w0*t*new)
            for i in range(0,len(x_FT)):
                y_FT_Im_mod[i]=0.0
                y_FT_Re_mod[i]=0
            arrow_mod_freq_Re_source.stream(dict(x1=[-new*w0],y1=[0],x2=[-new*w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Re_source2.stream(dict(x1=[new*w0],y1=[0],x2=[new*w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Re.visible = True
            arrow_mod_freq_Re2.visible = True
    elif func_select.value == "\u03B4(t)":
        if new == 0:
            line_mod_freq_Re.visible = False
            arrow_mod_time_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[1/0.1]),rollover=1)
            arrow_mod_time.visible = True
            y_mod_time = [0, 1/abs(0.2)]
        else:
            line_mod_freq_Re.visible = True
            for i in range(0,len(x)):
                y_mod_Re[i]=0
            for i in range(0,len(x_FT)):
                y_FT_Re_mod[i]=1/abs(new)    
            arrow_mod_time_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[1/abs(new)]),rollover=1)
            arrow_mod_time.visible = True
            y_mod_time = [0, 1/abs(new)]
    elif func_select.value == "1":
        arrow_mod_freq_Re_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[pi*2]),rollover=1)
        arrow_mod_freq_Re.visible = True
        y_mod_freq = [0, 2*pi]
    update_mod_functions(x, x_Im, x_FT, y_mod_Re, y_mod_Im, y_FT_Re_mod, y_FT_Im_mod)
    update_value_range(y, y_mod_Re, y_mod_Im, y_FT_Re, y_FT_Im, y_FT_Re_mod, y_FT_Im_mod, y_func_time, y_func_freq, 
                     y_mod_time, y_mod_freq)

## update modificated plots when f(t) is shifted by λ: f*(t) = f(t-λ)
def change_lambda_shifting(attr,old,new):
    global y, y_mod_Re, y_FT_Re_mod, y_FT_Im_mod, y_mod_freq
    y_mod_freq = y_func_freq
    delete_mod_arrows()
    if func_select.value == "rect(t)":
        for i in range(0,len(x)):
            t = x[i]
            if t < -0.5+new or t > 0.5+new:
                y_mod_Re[i]=0.0
            elif t>=-0.5+new and t<=0.5+new:
                y_mod_Re[i]=1.0
        for i in range(0,len(x_FT)): 
            w = x_FT[i]
            if w != 0:
                y_FT_Im_mod[i]=sin(-new*w)*2.0*sin(w*0.5)/w
                y_FT_Re_mod[i]=cos(-new*w)*2.0*sin(w*0.5)/w
            elif w == 0:
                y_FT_Re_mod[i]=1.0
                y_FT_Im_mod[i]=0.0
    elif func_select.value == "sinc(t)":
        for i in range(0,len(x)):
            t = x[i]
            if t != new:
                y_mod_Re[i]=sin(t-new)/(t-new)
            elif t == new:
                y_mod_Re[i]=1.0
        for i in range(0,len(x_FT)):
            w = x_FT[i]
            if w < -1 or w > 1:
                y_FT_Re_mod[i]=0.0
                y_FT_Im_mod[i]=0.0
            elif w>=-1 and w<=1:
                y_FT_Re_mod[i]=pi*cos(-new*w)
                y_FT_Im_mod[i]=pi*sin(-new*w)
    elif func_select.value == "\u03B4(t)":
        for i in range(0,len(x)):
            y_mod_Re[i] = 0
        for i in range(0,len(x_FT)):
            w = x_FT[i]
            y_FT_Im_mod[i]=sin(-new*w)
            y_FT_Re_mod[i]=cos(-new*w)
        arrow_mod_time_source.stream(dict(x1=[new],y1=[0],x2=[new],y2=[1]),rollover=1)
        arrow_mod_time.visible = True
    elif func_select.value == "1":
        arrow_mod_freq_Re_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[pi*2]),rollover=1)
        arrow_mod_freq_Re.visible = True
    elif func_select.value == "sin(12t)":
        for i in range(0,len(x)):
            t = x[i]
            y_mod_Re[i]=sin(w0*(t-new))
        for i in range(0,len(x_FT)):
            y_FT_Im_mod[i]=0.0
            y_FT_Re_mod[i] = 0
        arrow_mod_freq_Im_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi*cos(new)]),rollover=1)
        arrow_mod_freq_Im_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[-pi*cos(-new)]),rollover=1)
        arrow_mod_freq_Im.visible = True
        arrow_mod_freq_Im2.visible = True
        if new != 0:
            arrow_mod_freq_Re_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[-pi*sin(new)]),rollover=1)
            arrow_mod_freq_Re_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[pi*sin(-new)]),rollover=1)
            arrow_mod_freq_Re.visible = True
            arrow_mod_freq_Re2.visible = True
    elif func_select.value == "cos(12t)":
        for i in range(0,len(x)):
            t = x[i]
            y_mod_Re[i]=cos(w0*(t-new))
        for i in range(0,len(x_FT)):
            y_FT_Im_mod[i]=0.0
            y_FT_Re_mod[i] = 0
        if new != 0:
            arrow_mod_freq_Im_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi*sin(new)]),rollover=1)
            arrow_mod_freq_Im_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[pi*sin(-new)]),rollover=1)
            arrow_mod_freq_Im.visible = True
            arrow_mod_freq_Im2.visible = True
        arrow_mod_freq_Re_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi*cos(new)]),rollover=1)
        arrow_mod_freq_Re_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[pi*cos(-new)]),rollover=1)
        arrow_mod_freq_Re.visible = True
        arrow_mod_freq_Re2.visible = True
        y_mod_freq = [min([pi*sin(new), pi*sin(-new), pi*cos(new), pi*cos(-new)]), max([pi*sin(new), pi*sin(-new), pi*cos(new), pi*cos(-new)])]
    update_mod_functions(x, x_Im, x_FT, y_mod_Re, y_mod_Im, y_FT_Re_mod, y_FT_Im_mod)
    update_value_range(y, y_mod_Re, y_mod_Im, y_FT_Re, y_FT_Im, y_FT_Re_mod, y_FT_Im_mod, y_func_time, y_func_freq, 
                     y_mod_time, y_mod_freq)

## update modificated plots when f(t) is multiplicated with an exponential function exp(iωλ) 
def change_lambda_exp(attr,old,new):
    global y, y_mod_Re, y_mod_Im, y_FT_Re_mod, y_FT_Im_mod
    if func_select.value == "rect(t)":
        for i in range(0,len(x)):
            t = x[i]
            if t < -0.5 or t > 0.5:
                y_mod_Re[i]=0.0
                y_mod_Im[i] = 0.0
            elif t>=-0.5 and t<=0.5:
                y_mod_Re[i]=cos(new*t)
                y_mod_Im[i]=sin(new*t)  
        for i in range(0,len(x_FT)):
            w = x_FT[i]
            if w-new != 0:
                y_FT_Re_mod[i]=2.0*sin((w-new)*0.5)/(w-new)
            elif w-new == 0:
                y_FT_Re_mod[i]=1.0
            y_FT_Im_mod[i]=0
    elif func_select.value == "sinc(t)":
        for i in range(0,len(x)):
            t = x[i]
            if t != 0:
                y_mod_Re[i]=sin(t)*cos(new*t)/t
                y_mod_Im[i]=sin(t)*sin(new*t)/t
            elif t == 0:
                y_mod_Re[i]=1.0
                y_mod_Im[i]=0.0
        for i in range(0,len(x_FT)):
            w = x_FT[i]
            if w < -1+new or w > 1+new:
                y_FT_Re_mod[i]=0.0
            elif w>=-1+new and w<=1+new:
                y_FT_Re_mod[i]=pi
            y_FT_Im_mod[i]=0
    elif func_select.value == "\u03B4(t)":
        ""
    elif func_select.value == "1":
        for i in range(0,len(x)):
            t = x[i]
            y_mod_Re[i]=cos(new*t)
            y_mod_Im[i]=sin(new*t)
        arrow_mod_freq_Re_source.stream(dict(x1=[new],y1=[0],x2=[new],y2=[2*pi]),rollover=1)
    elif func_select.value == "sin(12t)":
        for i in range(0,len(x)):
            t = x[i]
            y_mod_Re[i]=sin(w0*t)*cos(new*t)
            y_mod_Im[i]=sin(new*t)*sin(w0*t)
        for i in range(0,len(x_FT)):
            y_FT_Im_mod[i]=0.0
            y_FT_Re_mod[i]=0.0
        arrow_mod_freq_Im_source.stream(dict(x1=[-w0+new],y1=[0],x2=[-w0+new],y2=[pi]),rollover=1)
        arrow_mod_freq_Im_source2.stream(dict(x1=[w0+new],y1=[0],x2=[w0+new],y2=[-pi]),rollover=1)
    elif func_select.value == "cos(12t)":
        for i in range(0,len(x)):
            t = x[i]
            y_mod_Re[i]=cos(w0*t)*cos(new*t)
            y_mod_Im[i]=cos(w0*t)*sin(new*t)
        for i in range(0,len(x_FT)):
            y_FT_Im_mod[i]=0.0
            y_FT_Re_mod[i]=0
        arrow_mod_freq_Re_source.stream(dict(x1=[-w0+new],y1=[0],x2=[-w0+new],y2=[pi]),rollover=1)
        arrow_mod_freq_Re_source2.stream(dict(x1=[w0+new],y1=[0],x2=[w0+new],y2=[pi]),rollover=1)
    update_mod_functions(x, x_Im, x_FT, y_mod_Re, y_mod_Im, y_FT_Re_mod, y_FT_Im_mod)
    update_value_range(y, y_mod_Re, y_mod_Im, y_FT_Re, y_FT_Im, y_FT_Re_mod, y_FT_Im_mod, y_func_time, y_func_freq, 
                     y_mod_time, y_mod_freq)

## update modificated plots when f(t) is multiplicated with another function g(t) 
def change_g_mult(attr,old,new):
    global y, y_mod_Re, y_FT_Re_mod, y_FT_Im_mod, y_mod_freq
    delete_mod_arrows()
    y_mod_freq = y_func_freq
    if new == "rect(t)":
        for i in range(0,len(x)):
            t = x[i]
            if t < -0.5 or t > 0.5:
                y_mod_Re[i]=0.0
            elif t>=-0.5 and t<=0.5:
                y_mod_Re[i]=y[i]
        if func_select.value == "1":
            for i in range(0,len(x_FT)):
                w = x_FT[i]
                if w != 0:
                    y_FT_Re_mod[i]=2.0*sin(w*0.5)/w
                elif w == 0:
                    y_FT_Re_mod[i]=1.0
                y_FT_Im_mod[i]=0
        elif func_select.value == "sinc(t)":
            for i in range(0,len(x_FT)):
                w = x_FT[i]
                (si1,_) = sici(0.5-0.5*w)
                (si2,_) = sici(0.5+0.5*w)
                y_FT_Re_mod[i]=si1+si2
                y_FT_Im_mod[i]=0.0
        elif func_select.value == "\u03B4(t)":
            for i in range(0,len(x_FT)):
                y_FT_Re_mod[i]=1.0
                y_FT_Im_mod[i]=0.0
            arrow_mod_time_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[1]),rollover=1)
            arrow_mod_time.visible = True
        elif func_select.value == "sin(12t)":
            for i in range(0,len(x_FT)):
                w = x_FT[i]
                if w != w0 and w != -w0:
                    y_FT_Im_mod[i]=sin(w*0.5+w0*0.5)/(w+w0)-sin(0.5*w0-0.5*w)/(w0-w)
                elif w == w0:
                    y_FT_Im_mod[i]=-0.5
                elif w == -w0:
                    y_FT_Im_mod[i]=0.5
                y_FT_Re_mod[i]=0
        elif func_select.value == "cos(12t)":
            for i in range(0,len(x_FT)):
                w = x_FT[i]
                if w != w0 and w != -w0:
                    y_FT_Re_mod[i]=sin(w*0.5+w0*0.5)/(w+w0)+sin(0.5*w0-0.5*w)/(w0-w)
                elif w == w0 or w == -w0:
                    y_FT_Re_mod[i]=0.5
                y_FT_Im_mod[i]=0
    elif new == "sinc(t)":
        for i in range(0,len(x)):
            t = x[i]
            if t != 0:
                y_mod_Re[i]=y[i]*sin(t)/t
            elif t == 0:
                y_mod_Re[i]=y[i]
        if func_select.value == "\u03B4(t)":
            for i in range(0,len(x_FT)):
                y_FT_Re_mod[i] = 1
                y_FT_Im_mod[i] = 0
            arrow_mod_time_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[1]),rollover=1)
            arrow_mod_time.visible = True
        elif func_select.value =="1":
            for i in range(0,len(x_FT)):
                w = x_FT[i]
                y_FT_Im_mod[i]=0.0
                if w < -1 or w > 1:
                    y_FT_Re_mod[i]=0.0
                elif w>=-1 and w<=1:
                    y_FT_Re_mod[i]=pi
        elif func_select.value == "rect(t)":
            for i in range(0,len(x_FT)):
                w = x_FT[i]
                (si1,_) = sici(0.5-0.5*w)
                (si2,_) = sici(0.5+0.5*w)
                y_FT_Re_mod[i]=si1+si2
                y_FT_Im_mod[i]=0.0
        elif func_select.value == "sinc(t)":
            for i in range(0,len(x_FT)):
                w = x_FT[i]
                if w <= -2 or w >= 2:
                    y_FT_Re_mod[i]=0
                elif w > -2 and w < 0:
                    y_FT_Re_mod[i]=pi+0.5*pi*w
                elif w >= 0 and w < 2:
                    y_FT_Re_mod[i]=pi-0.5*pi*w
                y_FT_Im_mod[i]=0.0
        elif func_select.value == "sin(12t)":
            for i in range(0,len(x_FT)):
                w = x_FT[i]
                if w < -1-w0 or w > 1+w0:
                    y_FT_Im_mod[i]=0
                elif w > 1-w0 and w < -1+w0:
                    y_FT_Im_mod[i]=0
                elif w >= -1-w0 and w <= 1-w0:
                    y_FT_Im_mod[i]=0.5*pi
                elif w >= -1+w0 and w < 1+w0:
                    y_FT_Im_mod[i]=-0.5*pi
                y_FT_Re_mod[i]=0.0
        elif func_select.value == "cos(12t)":
            for i in range(0,len(x_FT)):
                w = x_FT[i]
                if w < -1-w0 or w > 1+w0:
                    y_FT_Re_mod[i]=0
                elif w > 1-w0 and w < -1+w0:
                    y_FT_Re_mod[i]=0
                elif w >= -1-w0 and w <= 1-w0:
                    y_FT_Re_mod[i]=0.5*pi
                elif w >= -1+w0 and w < 1+w0:
                    y_FT_Re_mod[i]=0.5*pi
                y_FT_Im_mod[i]=0.0
    elif new == "\u03B4(t)":
        if func_select.value == "sin(12t)":
            for i in range(0,len(x)):
                y_mod_Re[i]=0
            for i in range(0,len(x_FT)):
                y_FT_Re_mod[i]=0
                y_FT_Im_mod[i]=0
        else:
            for i in range(0,len(x)):
                y_mod_Re[i]=0
            arrow_mod_time_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[1]),rollover=1)
            arrow_mod_time.visible = True
            for i in range(0,len(x_FT)):
                y_FT_Re_mod[i]=1.0
                y_FT_Im_mod[i]=0
    elif new == "1":
        reset_mod_functions(x, x_Im, x_FT, y, y_mod_Re, y_mod_Im, y_FT_Im, y_FT_Re, y_FT_Im_mod, y_FT_Re_mod)
        update_all_arrows_and_y_values()
    elif new == "sin(12t)":
        for i in range(0,len(x)):
            t = x[i]
            y_mod_Re[i]=y[i]*sin(w0*t)  
        if func_select.value == "rect(t)":
            for i in range(0,len(x_FT)):
                w = x_FT[i]
                if w != w0 and w != -w0:
                    y_FT_Im_mod[i]=sin(w*0.5+w0*0.5)/(w+w0)-sin(0.5*w0-0.5*w)/(w0-w)
                elif w == w0:
                    y_FT_Im_mod[i]=-0.5
                elif w == -w0:
                    y_FT_Im_mod[i]=0.5
                y_FT_Re_mod[i]=0
        elif func_select.value == "sinc(t)":
            for i in range(0,len(x_FT)):
                w = x_FT[i]
                if w < -1-w0 or w > 1+w0:
                    y_FT_Im_mod[i]=0
                elif w > 1-w0 and w < -1+w0:
                    y_FT_Im_mod[i]=0
                elif w >= -1-w0 and w <= 1-w0:
                    y_FT_Im_mod[i]=0.5*pi
                elif w >= -1+w0 and w < 1+w0:
                    y_FT_Im_mod[i]=-0.5*pi
                y_FT_Re_mod[i]=0.0
        elif func_select.value == "\u03B4(t)":
            for i in range(0,len(x_FT)):
                y_FT_Re_mod[i]=0
                y_FT_Im_mod[i]=0
        elif func_select.value == "1":
            for i in range(0,len(x_FT)):
                y_FT_Re_mod[i]=0.0
                y_FT_Im_mod[i] =  0
            arrow_mod_freq_Im_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Im_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[-pi]),rollover=1)
            arrow_mod_freq_Im.visible = True
            arrow_mod_freq_Im2.visible = True
            y_mod_freq = [-pi, pi]
        elif func_select.value == "sin(12t)":
            for i in range(0,len(x_FT)):
                y_FT_Im_mod[i]=0.0
                y_FT_Re_mod[i] = 0
            arrow_mod_freq_Re_source.stream(dict(x1=[-2*w0],y1=[0],x2=[-2*w0],y2=[-pi/2]),rollover=1)
            arrow_mod_freq_Re_source2.stream(dict(x1=[0],y1=[0],x2=[0],y2=[pi]),rollover=1)
            arrow_mod_freq_Re_source3.stream(dict(x1=[2*w0],y1=[0],x2=[2*w0],y2=[-pi/2]),rollover=1)
            arrow_mod_freq_Re.visible = True
            arrow_mod_freq_Re2.visible = True
            arrow_mod_freq_Re3.visible = True
        elif func_select.value == "cos(12t)":
            for i in range(0,len(x_FT)):
                y_FT_Re_mod[i]=0.0
                y_FT_Im_mod[i] = 0
            arrow_mod_freq_Im_source.stream(dict(x1=[-2*w0],y1=[0],x2=[-2*w0],y2=[pi/2]),rollover=1)
            arrow_mod_freq_Im_source2.stream(dict(x1=[2*w0],y1=[0],x2=[2*w0],y2=[-pi/2]),rollover=1)
            arrow_mod_freq_Im.visible = True
            arrow_mod_freq_Im2.visible = True
            y_mod_freq = [-pi/2, pi/2]
    elif new == "cos(12t)":
        for i in range(0,len(x)):
            t = x[i]
            y_mod_Re[i]=y[i]*cos(w0*t)
        if func_select.value == "\u03B4(t)":
            arrow_mod_time_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[1]),rollover=1)
            arrow_mod_time.visible = True
            for i in range(0,len(x_FT)):
                y_FT_Re_mod[i]=1.0
                y_FT_Im_mod[i]=0
        elif func_select.value == "rect(t)":
            for i in range(0,len(x_FT)):
                w = x_FT[i]
                if w != w0 and w != -w0:
                    y_FT_Re_mod[i]=sin(w*0.5+w0*0.5)/(w+w0)+sin(0.5*w0-0.5*w)/(w0-w)
                elif w == w0 or w == -w0:
                    y_FT_Re_mod[i]=0.5
                y_FT_Im_mod[i]=0
        elif func_select.value == "sinc(t)":
            for i in range(0,len(x_FT)):
                w = x_FT[i]
                if w < -1-w0 or w > 1+w0:
                    y_FT_Re_mod[i]=0
                elif w > 1-w0 and w < -1+w0:
                    y_FT_Re_mod[i]=0
                elif w >= -1-w0 and w <= 1-w0:
                    y_FT_Re_mod[i]=0.5*pi
                elif w >= -1+w0 and w < 1+w0:
                    y_FT_Re_mod[i]=0.5*pi
                y_FT_Im_mod[i]=0.0
        elif func_select.value == "1":
            for i in range(0,len(x_FT)):
                y_FT_Im_mod[i]=0.0
                y_FT_Re_mod[i] = 0
            arrow_mod_freq_Re_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Re_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Re.visible = True
            arrow_mod_freq_Re2.visible = True
            y_mod_freq = [0, pi]
        elif func_select.value == "sin(12t)":
            for i in range(0,len(x_FT)):
                y_FT_Re_mod[i]=0.0
                y_FT_Im_mod[i] = 0
            arrow_mod_freq_Im_source.stream(dict(x1=[-2*w0],y1=[0],x2=[-2*w0],y2=[pi/2]),rollover=1)
            arrow_mod_freq_Im_source2.stream(dict(x1=[2*w0],y1=[0],x2=[2*w0],y2=[-pi/2]),rollover=1)
            arrow_mod_freq_Im.visible = True
            arrow_mod_freq_Im2.visible = True
        elif func_select.value == "cos(12t)":
            for i in range(0,len(x_FT)):
                y_FT_Im_mod[i]=0.0
                y_FT_Re_mod[i] = 0
            arrow_mod_freq_Re_source.stream(dict(x1=[-2*w0],y1=[0],x2=[-2*w0],y2=[pi/2]),rollover=1)
            arrow_mod_freq_Re_source2.stream(dict(x1=[0],y1=[0],x2=[0],y2=[pi]),rollover=1)
            arrow_mod_freq_Re_source3.stream(dict(x1=[2*w0],y1=[0],x2=[2*w0],y2=[pi/2]),rollover=1)
            arrow_mod_freq_Re.visible = True
            arrow_mod_freq_Re2.visible = True
            arrow_mod_freq_Re3.visible = True
    update_mod_functions(x, x_Im, x_FT, y_mod_Re, y_mod_Im, y_FT_Re_mod, y_FT_Im_mod)
    update_value_range(y, y_mod_Re, y_mod_Im, y_FT_Re, y_FT_Im, y_FT_Re_mod, y_FT_Im_mod, y_func_time, y_func_freq, 
                     y_mod_time, y_mod_freq)

## update modificated plots when f(t) is convolved with another function g(t) 
def change_g_conv(attr,old,new):
    global y, y_mod_Re, y_FT_Re_mod, y_FT_Im_mod, y_mod_freq
    y_mod_freq = y_func_freq
    delete_mod_arrows()
    if new == "rect(t)":
        for i in range(0,len(x_FT)):
            w = x_FT[i]
            if w != 0:
                y_FT_Re_mod[i]=y_FT_Re[i]*2.0*sin(w*0.5)/w
            elif w == 0:
                y_FT_Re_mod[i]=y_FT_Re[i]
            y_FT_Im_mod[i]=0
        if func_select.value == "1":
            for i in range(0,len(x)):
                y_mod_Re[i]=1
            arrow_mod_freq_Re_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[2*pi]),rollover=1)
            arrow_mod_freq_Re.visible = True
        elif func_select.value == "sin(12t)":
            for i in range(0,len(x)):
                t = x[i]  
                y_mod_Re[i]=2*sin(0.5*w0)*sin(w0*t)/w0
            arrow_mod_freq_Im_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[2*pi*sin(0.5*w0)/w0]),rollover=1)
            arrow_mod_freq_Im_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[-2*pi*sin(0.5*w0)/w0]),rollover=1)
            arrow_mod_freq_Im.visible = True
            arrow_mod_freq_Im2.visible = True
        elif func_select.value == "cos(12t)":
            for i in range(0,len(x)):
                t = x[i]  
                y_mod_Re[i]=2*sin(0.5*w0)*cos(w0*t)/w0
            arrow_mod_freq_Re_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[2*pi*sin(0.5*w0)/w0]),rollover=1)
            arrow_mod_freq_Re_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[2*pi*sin(0.5*w0)/w0]),rollover=1)
            arrow_mod_freq_Re.visible = True
            arrow_mod_freq_Re2.visible = True
            y_mod_freq = [2*pi*sin(0.5*w0)/w0, 0]
        elif func_select.value == "rect(t)":
            for i in range(0,len(x)):
                t = x[i]
                if t < -1 or t > 1:
                    y_mod_Re[i]=0
                elif t >= -1 and t < 0:
                    y_mod_Re[i]=t+1
                elif t >= 0 and t <= 1:
                    y_mod_Re[i]=1-t
        elif func_select.value == "sinc(t)":
            for i in range(0,len(x)):
                t = x[i]
                (si1,_) = sici(0.5-t)
                (si2,_) = sici(0.5+t)
                y_mod_Re[i]=si1+si2
        elif func_select.value == "\u03B4(t)":
            for i in range(0,len(x)):
                t = x[i]
                if t < -0.5 or t > 0.5:  
                    y_mod_Re[i]=0.0
                elif t>=-0.5 and t<=0.5:
                    y_mod_Re[i]=1.0      
    elif new == "sinc(t)":
        for i in range(0,len(x_FT)):
            w = x_FT[i]
            if w < -1 or w > 1:
                y_FT_Re_mod[i]=0
            elif w >= -1 and w <= 1:
                y_FT_Re_mod[i]=y_FT_Re[i]*pi
            y_FT_Im_mod[i]=0
        if func_select.value == "rect(t)":
            for i in range(0,len(x)):
                t = x[i]
                (si1,_) = sici(0.5-t)
                (si2,_) = sici(0.5+t)
                y_mod_Re[i]=si1+si2
        elif func_select.value == "\u03B4(t)":
            for i in range(0,len(x)):
                t = x[i]
                if t != 0:  
                    y_mod_Re[i]=sin(t)/t
                elif t == 0:
                    y_mod_Re[i]=1.0
        elif func_select.value == "1":
            for i in range(0,len(x)):
                y_mod_Re[i]=pi
            arrow_mod_freq_Re_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[2*pi*pi]),rollover=1)
            arrow_mod_freq_Re.visible = True
            y_mod_freq = [0, 2*pi*pi]
    elif new == "\u03B4(t)":
        reset_mod_functions(x, x_Im, x_FT, y, y_mod_Re, y_mod_Im, y_FT_Im, y_FT_Re, y_FT_Im_mod, y_FT_Re_mod)
        update_all_arrows_and_y_values()
    elif new == "1":
        for i in range(0,len(x_FT)):
            y_FT_Re_mod[i]=0
            y_FT_Im_mod[i]=0
        if func_select.value == "rect(t)" or func_select.value == "\u03B4(t)":
            for i in range(0,len(x)):
                y_mod_Re[i]=1
            arrow_mod_freq_Re_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[2*pi]),rollover=1)
            arrow_mod_freq_Re.visible = True
            y_mod_freq = [0, 2*pi]
        elif func_select.value == "sinc(t)":
            for i in range(0,len(x)):
                y_mod_Re[i]=pi
            arrow_mod_freq_Re_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[2*pi*pi]),rollover=1)
            arrow_mod_freq_Re.visible = True
            y_mod_freq = [0, 2*pi*pi]
    elif new == "sin(12t)":
        for i in range(0,len(x_FT)):
            y_FT_Im_mod[i]=0
            y_FT_Re_mod[i]=0
        if func_select.value == "rect(t)":
            for i in range(0,len(x)):
                t = x[i]  
                y_mod_Re[i]=2*sin(0.5*w0)*sin(w0*t)/w0
            arrow_mod_freq_Im_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[2*pi*sin(0.5*w0)/w0]),rollover=1)
            arrow_mod_freq_Im_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[-2*pi*sin(0.5*w0)/w0]),rollover=1)
            arrow_mod_freq_Im.visible = True
            arrow_mod_freq_Im2.visible = True
        elif func_select.value == "\u03B4(t)":
            for i in range(0,len(x)):
                t = x[i]
                y_mod_Re[i]=sin(w0*t)
            arrow_mod_freq_Im_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Im_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[-pi]),rollover=1)
            arrow_mod_freq_Im.visible = True
            arrow_mod_freq_Im2.visible = True
            y_mod_freq = [-pi, pi]
    elif new == "cos(12t)":
        for i in range(0,len(x_FT)):
            y_FT_Re_mod[i]=0
            y_FT_Im_mod[i]=0
        if func_select.value == "rect(t)":
            for i in range(0,len(x)):
                t = x[i]  
                y_mod_Re[i]=2*sin(0.5*w0)*cos(w0*t)/w0
            arrow_mod_freq_Re_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[2*pi*sin(0.5*w0)/w0]),rollover=1)
            arrow_mod_freq_Re_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[2*pi*sin(0.5*w0)/w0]),rollover=1)
            arrow_mod_freq_Re.visible = True
            arrow_mod_freq_Re2.visible = True
        elif func_select.value == "\u03B4(t)":
            for i in range(0,len(x)):
                t = x[i]
                y_mod_Re[i]=cos(w0*t)
            arrow_mod_freq_Re_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Re_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Re.visible = True
            arrow_mod_freq_Re2.visible = True
            y_mod_freq = [0, pi]
    update_mod_functions(x, x_Im, x_FT, y_mod_Re, y_mod_Im, y_FT_Re_mod, y_FT_Im_mod)
    update_value_range(y, y_mod_Re, y_mod_Im, y_FT_Re, y_FT_Im, y_FT_Re_mod, y_FT_Im_mod, y_func_time, y_func_freq, 
                     y_mod_time, y_mod_freq)

## update modificated plots when f(t) is added to another function g(t) --> Linear combination
def change_g_comb(attr,old,new):
    global y, y_mod_Re, y_FT_Re_mod, y_FT_Im_mod, y_mod_time, y_mod_freq
    y_mod_time = y_func_time
    y_mod_freq = y_func_freq
    delete_mod_arrows()
    if new == "0":
        reset_mod_functions(x, x_Im, x_FT, y, y_mod_Re, y_mod_Im, y_FT_Im, y_FT_Re, y_FT_Im_mod, y_FT_Re_mod)
        update_all_arrows_and_y_values()
    elif new == "rect(t)":
        for i in range(0,len(x)):
            t = x[i]
            if t < -0.5 or t > 0.5:
                y_mod_Re[i]=y[i]
            elif t>=-0.5 and t<=0.5:
                y_mod_Re[i]=y[i]+1
        for i in range(0,len(x_FT)):
            w = x_FT[i]
            if w != 0:
                y_FT_Re_mod[i]=y_FT_Re[i]+2.0*sin(w*0.5)/w
            elif w == 0:
                y_FT_Re_mod[i]=y_FT_Re[i]+1
            y_FT_Im_mod[i]=y_FT_Im[i]
        if func_select.value == "\u03B4(t)":
            arrow_mod_time_source.stream(dict(x1=[0],y1=[1],x2=[0],y2=[2]),rollover=1)
            arrow_mod_time.visible = True
            y_mod_time = [1, 2]
        elif func_select.value == "1":
            arrow_mod_freq_Re_source.stream(dict(x1=[0],y1=[1],x2=[0],y2=[1+2*pi]),rollover=1)
            arrow_mod_freq_Re.visible = True
            y_mod_freq = [1, 1+2*pi]
        elif func_select.value == "sin(12t)":
            arrow_mod_freq_Im_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Im_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[-pi]),rollover=1)
            arrow_mod_freq_Im.visible = True
            arrow_mod_freq_Im2.visible = True
        elif func_select.value == "cos(12t)":
            arrow_mod_freq_Re_source.stream(dict(x1=[-w0],y1=[2.0*sin(-w0*0.5)/(-w0)],x2=[-w0],y2=[2.0*sin(-w0*0.5)/(-w0)+pi]),rollover=1)
            arrow_mod_freq_Re_source2.stream(dict(x1=[w0],y1=[2.0*sin(w0*0.5)/(w0)],x2=[w0],y2=[2.0*sin(w0*0.5)/(w0)+pi]),rollover=1) 
            arrow_mod_freq_Re.visible = True
            arrow_mod_freq_Re2.visible = True  
            y_mod_freq =[2.0*sin(-w0*0.5)/(-w0), 2.0*sin(-w0*0.5)/(-w0)+pi]     
    elif new == "sinc(t)":
        for i in range(0,len(x)):
            t = x[i]
            if t != 0:
                y_mod_Re[i]=y[i]+sin(t)/t
            elif t == 0:
                y_mod_Re[i]=y[i]+1
        for i in range(0,len(x_FT)):
            w = x_FT[i]
            if w < -1 or w > 1:
                y_FT_Re_mod[i]=y_FT_Re[i]
            elif w >= -1 and w <= 1:
                y_FT_Re_mod[i]=y_FT_Re[i]+pi
            y_FT_Im_mod[i]=y_FT_Im[i]
        if func_select.value == "\u03B4(t)":
            arrow_mod_time_source.stream(dict(x1=[0],y1=[1],x2=[0],y2=[2]),rollover=1)
            arrow_mod_time.visible = True
            y_mod_time = [1, 2]
        elif func_select.value == "1":
            arrow_mod_freq_Re_source.stream(dict(x1=[0],y1=[pi],x2=[0],y2=[3*pi]),rollover=1)
            arrow_mod_freq_Re.visible = True
            y_mod_freq = [pi, 3*pi]
        elif func_select.value == "sin(12t)":
            arrow_mod_freq_Im_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Im_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[-pi]),rollover=1)
            arrow_mod_freq_Im.visible = True
            arrow_mod_freq_Im2.visible = True
        elif func_select.value == "cos(12t)":
            arrow_mod_freq_Re_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Re_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Re.visible = True
            arrow_mod_freq_Re2.visible = True
    elif new == "\u03B4(t)":
        for i in range(0,len(x)):
            y_mod_Re[i]=y[i]
        for i in range(0,len(x_FT)):
            y_FT_Re_mod[i]=y_FT_Re[i]+1
            y_FT_Im_mod[i]=y_FT_Im[i]
        if func_select.value == "sin(12t)":
            arrow_mod_time_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[1]),rollover=1)
        elif func_select.value == "\u03B4(t)":
            arrow_mod_time_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[2]),rollover=1)
            y_mod_time = [0, 2]
        else:
            arrow_mod_time_source.stream(dict(x1=[0],y1=[1],x2=[0],y2=[2]),rollover=1)
            y_mod_time = [1, 2]
        arrow_mod_time.visible = True
        if func_select.value == "1":
            arrow_mod_freq_Re_source.stream(dict(x1=[0],y1=[1],x2=[0],y2=[2*pi+1]),rollover=1)
            arrow_mod_freq_Re.visible = True
            y_mod_freq = [1, 1+2*pi]
        elif func_select.value == "sin(12t)":
            arrow_mod_freq_Im_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Im_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[-pi]),rollover=1)
            arrow_mod_freq_Im.visible = True
            arrow_mod_freq_Im2.visible = True
        elif func_select.value == "cos(12t)":
            arrow_mod_freq_Re_source.stream(dict(x1=[-w0],y1=[1],x2=[-w0],y2=[1+pi]),rollover=1)
            arrow_mod_freq_Re_source2.stream(dict(x1=[w0],y1=[1],x2=[w0],y2=[1+pi]),rollover=1) 
            arrow_mod_freq_Re.visible = True
            arrow_mod_freq_Re2.visible = True
            y_mod_freq = [1, 1+pi]
    elif new == "1":
        for i in range(0,len(x)):
            y_mod_Re[i]=y[i]+1
        for i in range(0,len(x_FT)):
            y_FT_Re_mod[i]=y_FT_Re[i]
            y_FT_Im_mod[i]=y_FT_Im[i]
        if func_select.value == "rect(t)":
            arrow_mod_freq_Re_source.stream(dict(x1=[0],y1=[1],x2=[0],y2=[1+2*pi]),rollover=1)
            y_mod_freq = [1, 1+2*pi]
        elif func_select.value == "sinc(t)":
            arrow_mod_freq_Re_source.stream(dict(x1=[0],y1=[pi],x2=[0],y2=[pi+2*pi]),rollover=1)
            y_mod_freq = [pi, pi+2*pi]
        elif func_select.value == "1":
            arrow_mod_freq_Re_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[2*pi+2*pi]),rollover=1)
            y_mod_freq = [0, 2*pi+2*pi]
        elif func_select.value == "sin(12t)":
            arrow_mod_freq_Re_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[2*pi]),rollover=1)
            y_mod_freq = [0, 2*pi]
            arrow_mod_freq_Im_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Im_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[-pi]),rollover=1)
            arrow_mod_freq_Im.visible = True
            arrow_mod_freq_Im2.visible = True
        elif func_select.value == "cos(12t)":
            arrow_mod_freq_Re_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[2*pi]),rollover=1)
            y_mod_freq = [0, 2*pi]
            arrow_mod_freq_Re_source2.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Re_source3.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Re2.visible = True
            arrow_mod_freq_Re3.visible = True
        elif func_select.value == "\u03B4(t)":
            arrow_mod_freq_Re_source.stream(dict(x1=[0],y1=[1],x2=[0],y2=[1+2*pi]),rollover=1)
            y_mod_freq = [1, 1+2*pi]
            arrow_mod_time_source.stream(dict(x1=[0],y1=[1],x2=[0],y2=[2]),rollover=1)
            arrow_mod_time.visible = True
            y_mod_time = [1, 2]
        arrow_mod_freq_Re.visible = True
    elif new == "sin(12t)":
        for i in range(0,len(x)):
            t = x[i]
            y_mod_Re[i]=y[i]+sin(w0*t)
        for i in range(0,len(x_FT)):
            y_FT_Re_mod[i]=y_FT_Re[i]
            y_FT_Im_mod[i] = 0
        arrow_mod_freq_Im_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi]),rollover=1)
        arrow_mod_freq_Im_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[-pi]),rollover=1)
        arrow_mod_freq_Im.visible = True
        arrow_mod_freq_Im2.visible = True
        y_mod_freq = [-pi, pi]
        if func_select.value == "\u03B4(t)":
            arrow_mod_time_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[1]),rollover=1)
            arrow_mod_time.visible = True
        elif func_select.value == "1":
            arrow_mod_freq_Re_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[2*pi]),rollover=1)
            arrow_mod_freq_Re.visible = True
        elif func_select.value == "sin(12t)":
            arrow_mod_freq_Im_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[2*pi]),rollover=1)
            arrow_mod_freq_Im_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[-2*pi]),rollover=1)
            arrow_mod_freq_Im.visible = True
            arrow_mod_freq_Im2.visible = True
            y_mod_freq = [-2*pi, 2*pi]
        elif func_select.value == "cos(12t)":
            arrow_mod_freq_Re_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Re_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Re.visible = True
            arrow_mod_freq_Re2.visible = True
    elif new == "cos(12t)":
        for i in range(0,len(x)):
            t = x[i]
            y_mod_Re[i]=y[i]+cos(w0*t)
        for i in range(0,len(x_FT)):
            y_FT_Re_mod[i]=y_FT_Re[i]
            y_FT_Im_mod[i]=y_FT_Im[i]
        if func_select.value == "\u03B4(t)":
            arrow_mod_time_source.stream(dict(x1=[0],y1=[1],x2=[0],y2=[2]),rollover=1) 
            arrow_mod_time.visible = True
            y_mod_time = [1, 2]
            arrow_mod_freq_Re_source.stream(dict(x1=[-w0],y1=[1],x2=[-w0],y2=[1+pi]),rollover=1)
            arrow_mod_freq_Re_source2.stream(dict(x1=[w0],y1=[1],x2=[w0],y2=[1+pi]),rollover=1)
            y_mod_freq = [1, 1+pi]
        elif func_select.value == "1":
            arrow_mod_freq_Re_source3.stream(dict(x1=[0],y1=[0],x2=[0],y2=[2*pi]),rollover=1)
            arrow_mod_freq_Re3.visible = True
            arrow_mod_freq_Re_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Re_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[pi]),rollover=1)
        elif func_select.value == "sin(12t)":
            arrow_mod_freq_Im_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Im_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[-pi]),rollover=1)
            arrow_mod_freq_Im.visible = True
            arrow_mod_freq_Im2.visible = True
            arrow_mod_freq_Re_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Re_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[pi]),rollover=1)
        elif func_select.value == "sinc(t)":
            arrow_mod_freq_Re_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[pi]),rollover=1)
            arrow_mod_freq_Re_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[pi]),rollover=1)
        elif func_select.value == "cos(12t)":
            arrow_mod_freq_Re_source.stream(dict(x1=[-w0],y1=[0],x2=[-w0],y2=[2*pi]),rollover=1)
            arrow_mod_freq_Re_source2.stream(dict(x1=[w0],y1=[0],x2=[w0],y2=[2*pi]),rollover=1)
            y_mod_freq = [0, 2*pi]
        elif func_select.value == "rect(t)":
            arrow_mod_freq_Re_source.stream(dict(x1=[-w0],y1=[2.0*sin(-w0*0.5)/(-w0)],x2=[-w0],y2=[2.0*sin(-w0*0.5)/(-w0)+pi]),rollover=1)
            arrow_mod_freq_Re_source2.stream(dict(x1=[w0],y1=[2.0*sin(w0*0.5)/(w0)],x2=[w0],y2=[2.0*sin(w0*0.5)/(w0)+pi]),rollover=1)
            y_mod_freq =[2.0*sin(-w0*0.5)/(-w0), 2.0*sin(-w0*0.5)/(-w0)+pi]
        arrow_mod_freq_Re.visible = True
        arrow_mod_freq_Re2.visible = True
    update_mod_functions(x, x_Im, x_FT, y_mod_Re, y_mod_Im, y_FT_Re_mod, y_FT_Im_mod)
    update_value_range(y, y_mod_Re, y_mod_Im, y_FT_Re, y_FT_Im, y_FT_Re_mod, y_FT_Im_mod, y_func_time, y_func_freq, 
                     y_mod_time, y_mod_freq)

## set initial modification to "Shifting"
changeMod(0,0,"Shifting")
               
## Send to window
curdoc().add_root(layout)  

## get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  
