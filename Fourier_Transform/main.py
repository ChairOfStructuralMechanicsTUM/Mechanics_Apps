from __future__ import division
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import Slider, Button, Div, Arrow, OpenHead, Range1d, Label, Select, ColumnDataSource, NormalHead, LabelSet
from math import cos, sin, radians, sqrt, pi, atan2, exp
from os.path import dirname, join, split
import numpy as np
from scipy import signal


from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv, LatexSlider, LatexLabel, LatexLabelSet

initial_func = "rect(t)"
initial_mod = "Scaling"
x0 = -7.0
x = np.linspace(x0, 7.0, 1401)
y = []
y_mod = []
y_FT_Re = []
y_FT_Im = []
y_FT_Re_mod = []
y_FT_Im_mod = []
text_mod = ["f^{*}(t)=f(\\lambda t)"]
text_FT_mod = ["\\frac{1}{|\\lambda|}F\\left(\\frac{\\omega}{\\lambda}\\right)"]
with_text =["with"]
lambda_input = LatexSlider(title="\\lambda =", value=1, start=-3, end=3, step=0.1, width=250)
g_select = Select(title="g(t):", value=initial_mod,
    options=["Scaling","Shifting", "Multiplication with exponential function", "Multiplication with other function", "Convolution with other function",
    "Differentiation","Integration","Linear combination"], width = 430)

for i in range(0,1401):
    t = x[i]
    if t < -0.5 or t > 0.5:
        y.append(0.0)
        y_mod.append(0.0)
    elif t>=-0.5 and t<=0.5:
        y.append(1.0)
        y_mod.append(1.0)
    if t != 0:
        y_FT_Re.append(2.0*sin(t*0.5)/t)
        y_FT_Re_mod.append(2.0*sin(t*0.5)/t)
    elif t == 0:
        y_FT_Re.append(1.0)
        y_FT_Re_mod.append(1.0)
    y_FT_Im.append(0)
    y_FT_Im_mod.append(0)

def changeFunc(attr,old,new):
    global y, x, y_FT_Im, y_FT_Re, y_mod, y_FT_Im_mod, y_FT_Re_mod
    if new == "rect(t)":
        for i in range(0,1401):
            t = x[i]
            if t < -0.5 or t > 0.5:
                y[i]=0.0
                y_mod[i]=0.0
            elif t>=-0.5 and t<=0.5:
                y[i]=1.0
                y_mod[i]=1.0
            if t != 0:
                y_FT_Re[i]=2.0*sin(t*0.5)/t
                y_FT_Re_mod[i]=2.0*sin(t*0.5)/t
            elif t == 0:
                y_FT_Re[i]=1.0
                y_FT_Re_mod[i]=1.0
            y_FT_Im[i]=0
            y_FT_Im_mod[i]=0
        update_functions(y, y_mod, y_FT_Re, y_FT_Im, y_FT_Re_mod, y_FT_Im_mod)
        update_all_arrows()
        mod_select.value = "Scaling"
        lambda_input.value = 1
    elif new == "si(t)":
        for i in range(0,1401):
            t = x[i]
            if t != 0:
                y[i] = sin(t)/t
                y_mod[i]=sin(t)/t
            elif t == 0:
                y[i] = 1.0
                y_mod[i]=1.0
            if t < -1 or t > 1:
                y_FT_Re[i]=0.0
                y_FT_Re_mod[i]=0.0
            elif t>=-1 and t<=1:
                y_FT_Re[i]=pi
                y_FT_Re_mod[i]=pi
            y_FT_Im[i]=0.0
            y_FT_Im_mod[i]=0.0
        update_functions(y, y_mod, y_FT_Re, y_FT_Im, y_FT_Re_mod, y_FT_Im_mod)
        update_all_arrows()
        mod_select.value = "Scaling"
        lambda_input.value = 1
    elif new == "\u03B4(t)":
        y = 0.9*signal.unit_impulse(1401,700)
        y_mod = 0.9*signal.unit_impulse(1401,700)
        for i in range(0,1401):
            y_FT_Re[i]=1.0
            y_FT_Re_mod[i]=1.0
            y_FT_Im[i]=0.0
            y_FT_Im_mod[i]=0.0
        update_functions(y, y_mod, y_FT_Re, y_FT_Im, y_FT_Re_mod, y_FT_Im_mod)
        update_all_arrows()
        mod_select.value = "Scaling"
        lambda_input.value = 1
    elif new == "1":
        for i in range(0,1401):
            y[i] = 1.0
            y_mod[i] = 1.0
            y_FT_Im[i] = 0.0
            y_FT_Im_mod[i] = 0.0
        y_FT_Re = 0.95*2*pi*signal.unit_impulse(1401,700)
        y_FT_Re_mod = 0.95*2*pi*signal.unit_impulse(1401,700)
        update_functions(y, y_mod, y_FT_Re, y_FT_Im, y_FT_Re_mod, y_FT_Im_mod)
        update_all_arrows()
        mod_select.value = "Scaling"
        lambda_input.value = 1
    elif new == "sin(t)":
        for i in range(0,1401):
            t = x[i]
            y[i] = sin(t)  
            y_mod[i]=sin(t)
            y_FT_Re[i] = 0.0
            y_FT_Re_mod[i]=0.0
        y_FT_Im = 0.9*pi*signal.unit_impulse(1401,600)
        y_FT_Im_mod = 0.9*pi*signal.unit_impulse(1401,600)
        update_functions(y, y_mod, y_FT_Re, y_FT_Im, y_FT_Re_mod, y_FT_Im_mod)
        update_all_arrows()
        mod_select.value = "Scaling"
        lambda_input.value = 1
    elif new == "cos(t)":
        for i in range(0,1401):
            t = x[i]
            y[i] = cos(t)  
            y_mod[i]=cos(t)
            y_FT_Im[i] = 0.0
            y_FT_Im_mod[i]=0.0
            y_FT_Re = 0.85*pi*signal.unit_impulse(1401,600)+0.85*pi*signal.unit_impulse(1401,800)
            y_FT_Re_mod = 0.85*pi*signal.unit_impulse(1401,600)+0.85*pi*signal.unit_impulse(1401,800)
        update_functions(y, y_mod, y_FT_Re, y_FT_Im, y_FT_Re_mod, y_FT_Im_mod)
        update_all_arrows()
        mod_select.value = "Scaling"
        lambda_input.value = 1
        
func_select = Select(title="Input function f(t):", value=initial_func,
    options=["rect(t)","si(t)", "\u03B4(t)", "1", "sin(t)", "cos(t)"], width = 430)
func_select.on_change('value',changeFunc)


func_time_source = ColumnDataSource(data=dict(x=x,y=y)) # Default values
func_freq_Re_source = ColumnDataSource(data=dict(x=x,y=y_FT_Re)) # Default values
func_freq_Im_source = ColumnDataSource(data=dict(x=x, y=y_FT_Im))
mod_time_source = ColumnDataSource(data=dict(x=x,y=y_mod)) # Default values
arrow_source = ColumnDataSource(data = dict(x1=[],y1=[],x2=[],y2=[]))
arrow_source_Re = ColumnDataSource(data = dict(x1=[],y1=[],x2=[],y2=[]))
arrow_source_Im = ColumnDataSource(data = dict(x1=[],y1=[],x2=[],y2=[]))
arrow_source_Re2 = ColumnDataSource(data = dict(x1=[],y1=[],x2=[],y2=[]))
arrow_source_Im2 = ColumnDataSource(data = dict(x1=[],y1=[],x2=[],y2=[]))
arrow_line_source = ColumnDataSource(data=dict(x=[0],y=[0]))
mod_freq_Re_source = ColumnDataSource(data=dict(x=x,y=y_FT_Re_mod)) # Default values
mod_freq_Im_source = ColumnDataSource(data=dict(x=x,y=y_FT_Im_mod))
mod_arrow_source = ColumnDataSource(data = dict(x1=[],y1=[],x2=[],y2=[]))
mod_arrow_source_Re = ColumnDataSource(data = dict(x1=[],y1=[],x2=[],y2=[]))
mod_arrow_source_Im = ColumnDataSource(data = dict(x1=[],y1=[],x2=[],y2=[]))
mod_arrow_source_Re2 = ColumnDataSource(data = dict(x1=[],y1=[],x2=[],y2=[]))
mod_arrow_source_Im2 = ColumnDataSource(data = dict(x1=[],y1=[],x2=[],y2=[]))
mod_arrow_line_source1 = ColumnDataSource(data=dict(x=[0],y=[0]))
mod_arrow_line_source2 = ColumnDataSource(data=dict(x=[0],y=[0]))
modification_source = ColumnDataSource(data=dict(t=text_mod))
modification_result_source = ColumnDataSource(data=dict(t=text_FT_mod))
with_source = ColumnDataSource(data=dict(t=with_text))
# Initial space and time plot-boundaries
value_range = Range1d(-7,7)
time_range = Range1d(x0,7)

func_time_plot = figure(plot_width = 500,plot_height= 300,x_range  = time_range,y_range  = value_range, tools = "")
func_time_plot.axis.axis_label_text_font_size="12pt"
func_time_plot.xaxis.axis_label="t"
func_time_plot.yaxis.axis_label="f(t)"
func_time_plot.axis.axis_label_text_font_style="normal"
func_time_plot.toolbar.logo = None
func_time_plot.line(x='x',y='y', source = func_time_source, color='#3070b3',line_width=2)
func_time_plot.add_layout(Arrow(end=NormalHead(fill_color="#3070b3",line_color="#3070b3",size=10),line_color="#3070b3",line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=arrow_source))

# Initial space and time plot-boundaries

func_freq_plot = figure(plot_width = 500,plot_height= 300,x_range  = time_range,y_range  = value_range, tools="")
func_freq_plot.axis.axis_label_text_font_size="12pt"
func_freq_plot.xaxis.axis_label="ω"
func_freq_plot.yaxis.axis_label="F(ω)"
func_freq_plot.axis.axis_label_text_font_style="normal"
func_freq_plot.toolbar.logo = None
func_freq_plot.line(x='x',y='y', source = func_freq_Re_source, color='#e37222', legend_label='Re(F)',line_width=2)
func_freq_plot.line(x='x',y='y', source = func_freq_Im_source, color='#a2ad00', legend_label='Im(F)', line_dash='dashed',line_width=2)
func_freq_plot.add_layout(Arrow(end=NormalHead(fill_color="#e37222",line_color="#e37222",size=10),line_color="#e37222",line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=arrow_source_Re))
func_freq_plot.add_layout(Arrow(end=NormalHead(fill_color="#a2ad00",line_color="#a2ad00",size=10),line_color="#a2ad00",line_dash='dashed',line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=arrow_source_Im))
func_freq_plot.add_layout(Arrow(end=NormalHead(fill_color="#e37222",line_color="#e37222",size=10),line_color="#e37222",line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=arrow_source_Re2))
func_freq_plot.add_layout(Arrow(end=NormalHead(fill_color="#a2ad00",line_color="#a2ad00",size=10),line_color="#a2ad00",line_dash='dashed',line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=arrow_source_Im2))
func_freq_plot.line(x='x',y='y', source = arrow_line_source, color='#a2ad00', line_dash='dashed',line_width=2.5)


mod_time_plot = figure(plot_width = 500,plot_height= 300,x_range  = time_range,y_range  = value_range, tools="")
mod_time_plot.axis.axis_label_text_font_size="12pt"
mod_time_plot.xaxis.axis_label="t"
mod_time_plot.yaxis.axis_label="f(t)"
mod_time_plot.axis.axis_label_text_font_style="normal"
mod_time_plot.toolbar.logo = None
mod_time_plot.line(x='x',y='y', source = mod_time_source, color='#3070b3',line_width=2)
mod_time_plot.add_layout(Arrow(end=NormalHead(fill_color="#3070b3",line_color="#3070b3",size=10),line_color="#3070b3",line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=mod_arrow_source))

mod_freq_plot = figure(plot_width = 500,plot_height= 300,x_range  = time_range,y_range  = value_range, tools="")
mod_freq_plot.axis.axis_label_text_font_size="12pt"
mod_freq_plot.xaxis.axis_label="ω"
mod_freq_plot.yaxis.axis_label="F(ω)"
mod_freq_plot.axis.axis_label_text_font_style="normal"
mod_freq_plot.toolbar.logo = None
mod_freq_plot.line(x='x',y='y', source = mod_freq_Re_source, color='#e37222', legend_label='Re(F)',line_width=2)
mod_freq_plot.line(x='x',y='y', source = mod_freq_Im_source, color='#a2ad00', legend_label='Im(F)',line_dash='dashed',line_width=2)
mod_freq_plot.add_layout(Arrow(end=NormalHead(fill_color="#e37222",line_color="#e37222",size=10),line_color="#e37222",line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=mod_arrow_source_Re))
mod_freq_plot.add_layout(Arrow(end=NormalHead(fill_color="#a2ad00",line_color="#a2ad00",size=10),line_color="#a2ad00",line_dash='dashed',line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=mod_arrow_source_Im))
mod_freq_plot.add_layout(Arrow(end=NormalHead(fill_color="#e37222",line_color="#e37222",size=10),line_color="#e37222",line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=mod_arrow_source_Re2))
mod_freq_plot.add_layout(Arrow(end=NormalHead(fill_color="#a2ad00",line_color="#a2ad00",size=10),line_color="#a2ad00",line_dash='dashed',line_width=2,
    x_start='x1',y_start='y1',x_end='x2',y_end='y2',source=mod_arrow_source_Im2))
mod_freq_plot.line(x='x',y='y', source = mod_arrow_line_source1, color='#a2ad00', line_dash='dashed',line_width=2.5)
mod_freq_plot.line(x='x',y='y', source = mod_arrow_line_source2, color='#a2ad00', line_dash='dashed',line_width=2.5)
# add app description
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)

fig = figure(title="", tools = "", x_range=(-5,5), y_range=(-5,5),width=150,height=130)
fig.axis.visible = False
fig.grid.visible = False
fig.outline_line_color = None
fig.toolbar.logo = None
fig.line(x=[-2.5,2.5],y=[0,0],color="black",line_width=2)
fig.ellipse(x=-3,y=0,width=1,height=1,line_color="black",fill_color=None,line_width=2)
fig.ellipse(x=3,y=0,width=1,height=1,line_color="black",fill_color="black",line_width=2)
fig.add_layout(Label(x=0,y=1.5,text="FT",text_color='black',text_font_size="12pt",text_baseline="middle",text_align="center"))

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



def changeMod(attr, old, new):
    global text_mod, text_FT_mod, lambda_input, layout, modification, g_select, with_text
    if new == "Scaling":
        text_mod = ["f^{*}(t)=f(\\lambda t)"]
        text_FT_mod = ["\\frac{1}{|\\lambda|}F\\left(\\frac{\\omega}{\\lambda}\\right)"]
        modification_source.data = dict(t=text_mod)
        modification_result_source.data = dict(t=text_FT_mod)
        lambda_input = LatexSlider(title="\\lambda =", value=1, start=-3, end=3, step=0.1, width=250)
        reset_mod_functions(y,y_mod,y_FT_Im,y_FT_Re,y_FT_Im_mod,y_FT_Re_mod)
        update_all_arrows()
        lambda_input.on_change('value',change_lambda_scaling)
        with_text =["with"]
        with_source.data=dict(t=with_text)
        layout.children[5] = row(Spacer(width=35),modification, column(Spacer(height=19),lambda_input))
    elif new == "Shifting":
        text_mod = ["f^{*}(t)=f(t-\\lambda)"]
        text_FT_mod = ["e^{-i\\lambda\\omega}F(\\omega)"]
        modification_source.data = dict(t=text_mod)
        modification_result_source.data = dict(t=text_FT_mod)
        lambda_input = LatexSlider(title="\\lambda =", value=0, start=-3, end=3, step=0.1, width=250)
        reset_mod_functions(y,y_mod,y_FT_Im,y_FT_Re,y_FT_Im_mod,y_FT_Re_mod)
        update_all_arrows()
        lambda_input.on_change('value',change_lambda_shifting)
        with_text =["with"]
        with_source.data=dict(t=with_text)
        layout.children[5] = row(Spacer(width=35),modification, column(Spacer(height=19),lambda_input)) 
    elif new == "Multiplication with exponential function":
        text_mod = ["f^{*}(t)=f(t)e^{i\\lambda t}"]
        text_FT_mod = ["F(\\omega-\\lambda)"]
        modification_source.data = dict(t=text_mod)
        modification_result_source.data = dict(t=text_FT_mod)
        lambda_input = LatexSlider(title="\\lambda =", value=0, start=-3, end=3, step=0.1, width=250)
        reset_mod_functions(y,y_mod,y_FT_Im,y_FT_Re,y_FT_Im_mod,y_FT_Re_mod)
        update_all_arrows()
        lambda_input.on_change('value',change_lambda_exp)
        with_text =["with"]
        with_source.data=dict(t=with_text)
        layout.children[5] = row(Spacer(width=35),modification, column(Spacer(height=19),lambda_input)) 
    elif new == "Multiplication with other function":
        text_mod = ["f^{*}(t)=f(t)\\cdot g(t)"]
        text_FT_mod = ["\\frac{1}{2\\pi}(F(\\omega)*G(\\omega))"]
        modification_source.data = dict(t=text_mod)
        modification_result_source.data = dict(t=text_FT_mod)
        g_select = Select(title="g(t):", value="1", options=["rect(t)","si(t)", "\u03B4(t)", "1", "sin(t)", "cos(t)"], width = 100)
        reset_mod_functions(y,y_mod,y_FT_Im,y_FT_Re,y_FT_Im_mod,y_FT_Re_mod)
        update_all_arrows()
        g_select.on_change('value',change_g_mult)
        with_text =["with"]
        with_source.data=dict(t=with_text)
        layout.children[5] = row(Spacer(width=35),modification, column(Spacer(height=19),g_select)) 
    elif new == "Convolution with other function":
        text_mod = ["f^{*}(t)=f(t)*g(t)"]
        text_FT_mod = ["F(\\omega)\\cdot G(\\omega))"]
        modification_source.data = dict(t=text_mod)
        modification_result_source.data = dict(t=text_FT_mod)
        g_select = Select(title="g(t):", value="rect(t)", options=["rect(t)","si(t)", "\u03B4(t)", "1", "sin(t)", "cos(t)"], width = 100)
        reset_mod_functions(y,y_mod,y_FT_Im,y_FT_Re,y_FT_Im_mod,y_FT_Re_mod)
        update_all_arrows()
        g_select.on_change('value',change_g_conv)
        with_text =["with"]
        with_source.data=dict(t=with_text)
        layout.children[5] = row(Spacer(width=35),modification, column(Spacer(height=19),g_select))         
    elif new == "Differentiation":
        text_mod = ["f^{*}(t)=f^{(n)}(t)"]
        text_FT_mod = ["(i\\omega)^{n}F(\\omega)"]
        modification_source.data = dict(t=text_mod)
        modification_result_source.data = dict(t=text_FT_mod)
        with_text =[""]
        with_source.data=dict(t=with_text)
        reset_mod_functions(y,y_mod,y_FT_Im,y_FT_Re,y_FT_Im_mod,y_FT_Re_mod)
        update_all_arrows()
        layout.children[5] = row(Spacer(width=35),modification) 
    elif new == "Integration":
        text_mod = ["f^{*}(t)=\\int f(t)dt"]
        text_FT_mod = ["\\frac{1}{i\\omega}F(\\omega)"]
        modification_source.data = dict(t=text_mod)
        modification_result_source.data = dict(t=text_FT_mod)
        with_text =[""]
        with_source.data=dict(t=with_text)
        reset_mod_functions(y,y_mod,y_FT_Im,y_FT_Re,y_FT_Im_mod,y_FT_Re_mod)
        update_all_arrows()
        layout.children[5] = row(Spacer(width=35),modification)  
    elif new == "Linear combination":
        text_mod = ["f^{*}(t)=\\lambda_\\mathrm{1}f(t)+\\lambda_\\mathrm{2}g(t)"]
        text_FT_mod = ["\\lambda_\\mathrm{1}F(\\omega)+\\lambda_\\mathrm{2}G(\\omega)"]
        modification_source.data = dict(t=text_mod)
        modification_result_source.data = dict(t=text_FT_mod)
        g_select = Select(title="g(t):", value="1", options=["rect(t)","si(t)", "\u03B4(t)", "1", "sin(t)", "cos(t)"], width = 100)
        g_select.on_change('value',change_g_conv)
        lambda1_input = LatexSlider(title="\\lambda_\\mathrm{1} =", value=0, start=-3, end=3, step=0.1, width=250)
        lambda1_input.on_change('value',change_lambda1)
        lambda2_input = LatexSlider(title="\\lambda_\\mathrm{2} =", value=0, start=-3, end=3, step=0.1, width=250)
        lambda2_input.on_change('value',change_lambda2)
        reset_mod_functions(y,y_mod,y_FT_Im,y_FT_Re,y_FT_Im_mod,y_FT_Re_mod)
        update_all_arrows()
        with_text =["with"]
        with_source.data=dict(t=with_text)
        layout.children[5] = row(Spacer(width=35),modification, column(Spacer(height=19),g_select),Spacer(width=20),column(Spacer(height=19),
            lambda1_input),Spacer(width=20),column(Spacer(height=19),lambda2_input))          

mod_select = Select(title="Modification of input function f(t):", value=initial_mod,
    options=["Scaling","Shifting", "Multiplication with exponential function", "Multiplication with other function", "Convolution with other function",
    "Differentiation","Integration","Linear combination"], width = 430)
mod_select.on_change('value',changeMod)

layout = column(description, row(Spacer(width=35), func_select), row(func_time_plot, column(Spacer(height=64),fig), 
    func_freq_plot),Spacer(height=20), row(Spacer(width=35),mod_select),row(Spacer(width=35),modification, column(Spacer(height=19),
    lambda_input)), Spacer(height=10),row(mod_time_plot, column(Spacer(height=64),fig), mod_freq_plot))

def update_mod_functions(y_mod, y_FT_Re_mod, y_FT_Im_mod):
    mod_time_source.data = dict(x=x,y=y_mod)
    mod_freq_Re_source.data = dict(x=x,y=y_FT_Re_mod) 
    mod_freq_Im_source.data = dict(x=x, y=y_FT_Im_mod)

def reset_mod_functions(y,y_mod,y_FT_Im,y_FT_Re,y_FT_Im_mod,y_FT_Re_mod):
    y_mod = y
    y_FT_Im_mod = y_FT_Im
    y_FT_Re_mod = y_FT_Re
    update_mod_functions(y_mod, y_FT_Re_mod, y_FT_Im_mod)

def update_functions(y, y_mod, y_FT_Re, y_FT_Im, y_FT_Re_mod, y_FT_Im_mod):
    func_time_source.data = dict(x=x, y=y)
    mod_time_source.data = dict(x=x,y=y_mod)
    func_freq_Re_source.data = dict(x=x,y=y_FT_Re) 
    func_freq_Im_source.data = dict(x=x, y=y_FT_Im)
    mod_freq_Re_source.data = dict(x=x,y=y_FT_Re_mod) 
    mod_freq_Im_source.data = dict(x=x, y=y_FT_Im_mod)

def update_all_arrows():
    arrow_source.stream(dict(x1=[100],y1=[0],x2=[100],y2=[0]),rollover=1)
    arrow_source_Re.stream(dict(x1=[100],y1=[0],x2=[100],y2=[0]),rollover=1)
    arrow_source_Im.stream(dict(x1=[100],y1=[0],x2=[100],y2=[0]),rollover=1)
    arrow_source_Re2.stream(dict(x1=[100],y1=[0],x2=[100],y2=[0]),rollover=1)
    arrow_source_Im2.stream(dict(x1=[100],y1=[0],x2=[100],y2=[0]),rollover=1)
    arrow_line_source.data = dict(x=[0],y=[0])
    mod_arrow_source.stream(dict(x1=[100],y1=[0],x2=[100],y2=[0]),rollover=1)
    mod_arrow_source_Re.stream(dict(x1=[100],y1=[0],x2=[100],y2=[0]),rollover=1)
    mod_arrow_source_Im.stream(dict(x1=[100],y1=[0],x2=[100],y2=[0]),rollover=1)
    mod_arrow_source_Re2.stream(dict(x1=[100],y1=[0],x2=[100],y2=[0]),rollover=1)
    mod_arrow_source_Im2.stream(dict(x1=[100],y1=[0],x2=[100],y2=[0]),rollover=1)
    mod_arrow_line_source1.data = dict(x=[0],y=[0])
    mod_arrow_line_source2.data = dict(x=[0],y=[0])
    if func_select.value == "\u03B4(t)":
        arrow_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[1]),rollover=1)
        mod_arrow_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[1]),rollover=1)
    elif func_select.value == "1":
        arrow_source_Re.stream(dict(x1=[0],y1=[0],x2=[0],y2=[2*pi]),rollover=1)
        mod_arrow_source_Re.stream(dict(x1=[0],y1=[0],x2=[0],y2=[2*pi]),rollover=1)
    elif func_select.value == "sin(t)":
        arrow_source_Im.stream(dict(x1=[-1],y1=[0],x2=[-1],y2=[pi]),rollover=1)
        arrow_source_Im2.stream(dict(x1=[1],y1=[0],x2=[1],y2=[-pi]),rollover=1)
        mod_arrow_source_Im.stream(dict(x1=[-1],y1=[0],x2=[-1],y2=[pi]),rollover=1)
        mod_arrow_source_Im2.stream(dict(x1=[1],y1=[0],x2=[1],y2=[-pi]),rollover=1)
        arrow_line_source.data = dict(x=[1,1],y=[0,-pi])
        mod_arrow_line_source2.data = dict(x=[1,1],y=[0,-pi])
    elif func_select.value == "cos(t)":
        arrow_source_Re.stream(dict(x1=[-1],y1=[0],x2=[-1],y2=[pi]),rollover=1) 
        arrow_source_Re2.stream(dict(x1=[1],y1=[0],x2=[1],y2=[pi]),rollover=1)
        mod_arrow_source_Re.stream(dict(x1=[-1],y1=[0],x2=[-1],y2=[pi]),rollover=1)
        mod_arrow_source_Re2.stream(dict(x1=[1],y1=[0],x2=[1],y2=[pi]),rollover=1)


def change_lambda_scaling(attr,old,new):
    global y,x,y_mod, y_FT_Re_mod, y_FT_Im_mod
    if func_select.value == "rect(t)":
        if new == 0:
            for i in range(0,1401):
                t = x[i]
                y_mod[i]=1
                y_FT_Im_mod[i]=0.0
            y_FT_Re_mod=0.95*2*pi*signal.unit_impulse(1401,700)
            mod_arrow_source_Re.stream(dict(x1=[0],y1=[0],x2=[0],y2=[2*pi]),rollover=1)
        else:
            for i in range(0,1401):
                t = x[i]
                if t < -0.5/abs(new) or t > 0.5/abs(new):
                    y_mod[i]=0.0
                elif t>=-0.5/abs(new) and t<=0.5/abs(new):
                    y_mod[i]=1.0
                if t != 0:
                    y_FT_Re_mod[i]=2.0/abs(new)*sin(t*0.5/new)/(t/new)
                elif t == 0:
                    y_FT_Re_mod[i]=1/abs(new)
                y_FT_Im[i]=0
            mod_arrow_source_Re.stream(dict(x1=[100],y1=[0],x2=[100],y2=[0]),rollover=1)
        update_mod_functions(y_mod, y_FT_Re_mod, y_FT_Im_mod)
    elif func_select.value == "si(t)":
        if new == 0:
            for i in range(0,1401):
                t = x[i]
                y_mod[i]=1
                y_FT_Im_mod[i] = 0.0
            y_FT_Re_mod = 0.95*2*pi*signal.unit_impulse(1401,700)
            mod_arrow_source_Re.stream(dict(x1=[0],y1=[0],x2=[0],y2=[2*pi]),rollover=1)
        else:
            for i in range(0,1401):
                t = x[i]
                if t != 0:
                    y_mod[i]=sin(new*t)/(t*new)
                elif t == 0:
                    y_mod[i]=1.0
                if t < -abs(new) or t > abs(new):
                    y_FT_Re_mod[i]=0.0
                elif t>=-abs(new) and t<=abs(new):
                    y_FT_Re_mod[i]=pi/abs(new)
                y_FT_Im_mod[i] = 0.0
            mod_arrow_source_Re.stream(dict(x1=[100],y1=[0],x2=[100],y2=[0]),rollover=1)
        update_mod_functions(y_mod, y_FT_Re_mod, y_FT_Im_mod)
    elif func_select.value == "\u03B4(t)":
        y_mod = 0.9*signal.unit_impulse(1401,700)
        mod_arrow_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[1]),rollover=1)
        mod_time_source.data = dict(x=x,y=y_mod)
    elif func_select.value == "1":
        for i in range(0,1401):
            y_mod[i] = 1.0
        mod_time_source.data = dict(x=x,y=y_mod)
    elif func_select.value == "sin(t)":
        if new == 0:
            for i in range(0,1401):
                y_mod[i]=0.0
                y_FT_Im_mod[i]=0.0
                y_FT_Re_mod[i]=0.0
            mod_arrow_source_Im.stream(dict(x1=[100],y1=[0],x2=[100],y2=[0]),rollover=1)
            mod_arrow_source_Im2.stream(dict(x1=[100],y1=[0],x2=[100],y2=[0]),rollover=1)
            mod_arrow_line_source1.data = dict(x=[0],y=[0])
            mod_arrow_line_source2.data = dict(x=[0],y=[0])
        else:
            for i in range(0,1401):
                t = x[i]
                y_mod[i]=sin(t*new)
                y_FT_Re_mod[i]=0.0
                y_FT_Im_mod[i]=0.0
            mod_arrow_line_source1.data=dict(x=[-new,-new],y=[0,pi])
            mod_arrow_line_source2.data=dict(x=[new,new],y=[0,-pi])
            mod_arrow_source_Im.stream(dict(x1=[-new],y1=[0],x2=[-new],y2=[pi]),rollover=1)
            mod_arrow_source_Im2.stream(dict(x1=[new],y1=[0],x2=[new],y2=[-pi]),rollover=1)
        update_mod_functions(y_mod, y_FT_Re_mod, y_FT_Im_mod)
    elif func_select.value == "cos(t)":
        if new == 0:
            for i in range(0,1401):
                t = x[i]
                y_mod[i]=1
                y_FT_Im_mod[i]=0.0
            y_FT_Re_mod=0.95*2*pi*signal.unit_impulse(1401,700)
            mod_arrow_source_Re.stream(dict(x1=[0],y1=[0],x2=[0],y2=[2*pi]),rollover=1)
            mod_arrow_source_Re2.stream(dict(x1=[100],y1=[0],x2=[100],y2=[0]),rollover=1)
        else:
            for i in range(0,1401):
                t = x[i]
                y_mod[i]=cos(t*new)
                y_FT_Im_mod[i]=0.0
            y_FT_Re_mod=0.85*pi*signal.unit_impulse(1401,700-int(new*100))+0.85*pi*signal.unit_impulse(1401,700+int(new*100))
            mod_arrow_source_Re.stream(dict(x1=[-new],y1=[0],x2=[-new],y2=[pi]),rollover=1)
            mod_arrow_source_Re2.stream(dict(x1=[new],y1=[0],x2=[new],y2=[pi]),rollover=1)
        update_mod_functions(y_mod, y_FT_Re_mod, y_FT_Im_mod)
        

def change_lambda_shifting(attr,old,new):
    global y,x,y_mod, y_FT_Re_mod, y_FT_Im_mod
    if func_select.value == "rect(t)":
        for i in range(0,1401):
            t = x[i]
            if t < -0.5+new or t > 0.5+new:
                y_mod[i]=0.0
            elif t>=-0.5+new and t<=0.5+new:
                y_mod[i]=1.0    
            if t != 0:
                y_FT_Im_mod[i]=sin(-new*t)*2.0*sin(t*0.5)/t
                y_FT_Re_mod[i]=cos(-new*t)*2.0*sin(t*0.5)/t
            elif t == 0:
                y_FT_Re_mod[i]=1.0
                y_FT_Im_mod[i]=0.0
        update_mod_functions(y_mod, y_FT_Re_mod, y_FT_Im_mod)
    elif func_select.value == "si(t)":
        for i in range(0,1401):
            t = x[i]
            if t != new:
                y_mod[i]=sin(t-new)/(t-new)
            elif t == new:
                y_mod[i]=1.0
            if t < -1 or t > 1:
                y_FT_Re_mod[i]=0.0
                y_FT_Im_mod[i]=0.0
            elif t>=-1 and t<=1:
                y_FT_Re_mod[i]=pi*cos(-new*t)
                y_FT_Im_mod[i]=pi*sin(-new*t)
        update_mod_functions(y_mod, y_FT_Re_mod, y_FT_Im_mod)
    elif func_select.value == "\u03B4(t)":
        y_mod = 0.9*signal.unit_impulse(1401,int(700+new*100))
        mod_arrow_source.stream(dict(x1=[new],y1=[0],x2=[new],y2=[1]),rollover=1)
        for i in range(0,1401):
            t = x[i]
            y_FT_Im_mod[i]=sin(-new*t)
            y_FT_Re_mod[i]=cos(-new*t)
        update_mod_functions(y_mod, y_FT_Re_mod, y_FT_Im_mod)
    elif func_select.value == "1":
        ""
    elif func_select.value == "sin(t)":
        for i in range(0,1401):
            t = x[i]
            y_mod[i]=sin(t-new)
            y_FT_Im_mod[i]=0.0
        y_FT_Re_mod= -0.85*pi*signal.unit_impulse(1401,600)*sin(new)+0.85*pi*signal.unit_impulse(1401,800)*sin(-new)
        mod_arrow_line_source1.data=dict(x=[-1,-1],y=[0,pi*cos(new)])
        mod_arrow_line_source2.data=dict(x=[1,1],y=[0,-pi*cos(-new)])
        mod_arrow_source_Im.stream(dict(x1=[-1],y1=[0],x2=[-1],y2=[pi*cos(new)]),rollover=1)
        mod_arrow_source_Im2.stream(dict(x1=[1],y1=[0],x2=[1],y2=[-pi*cos(-new)]),rollover=1)
        if new != 0:
            mod_arrow_source_Re.stream(dict(x1=[-1],y1=[0],x2=[-1],y2=[-pi*sin(new)]),rollover=1)
            mod_arrow_source_Re2.stream(dict(x1=[1],y1=[0],x2=[1],y2=[pi*sin(-new)]),rollover=1)
        elif new == 0:
            mod_arrow_source_Re.stream(dict(x1=[100],y1=[0],x2=[100],y2=[0]),rollover=1)
            mod_arrow_source_Re2.stream(dict(x1=[100],y1=[0],x2=[100],y2=[0]),rollover=1)
        update_mod_functions(y_mod, y_FT_Re_mod, y_FT_Im_mod)
    elif func_select.value == "cos(t)":
        for i in range(0,1401):
            t = x[i]
            y_mod[i]=cos(t-new)
            y_FT_Im_mod[i]=0.0
        y_FT_Re_mod=0.85*pi*signal.unit_impulse(1401,600)*cos(new)+0.85*pi*signal.unit_impulse(1401,800)*cos(-new)
        mod_arrow_line_source1.data=dict(x=[-1,-1],y=[0,pi*sin(new)])
        mod_arrow_line_source2.data=dict(x=[1,1],y=[0,pi*sin(-new)])
        if new ==0:
            mod_arrow_source_Im.stream(dict(x1=[100],y1=[0],x2=[100],y2=[0]),rollover=1)
            mod_arrow_source_Im2.stream(dict(x1=[100],y1=[0],x2=[100],y2=[0]),rollover=1) 
        elif new != 0:
            mod_arrow_source_Im.stream(dict(x1=[-1],y1=[0],x2=[-1],y2=[pi*sin(new)]),rollover=1)
            mod_arrow_source_Im2.stream(dict(x1=[1],y1=[0],x2=[1],y2=[pi*sin(-new)]),rollover=1)
        mod_arrow_source_Re.stream(dict(x1=[-1],y1=[0],x2=[-1],y2=[pi*cos(new)]),rollover=1)
        mod_arrow_source_Re2.stream(dict(x1=[1],y1=[0],x2=[1],y2=[pi*cos(-new)]),rollover=1)
        update_mod_functions(y_mod, y_FT_Re_mod, y_FT_Im_mod)
def change_lambda_exp(attr,old,new):
    ""
def change_g_mult(attr,old,new):
    global y,x,y_mod, y_FT_Re_mod, y_FT_Im_mod
    if new == "rect(t)":
        if func_select.value == "\u03B4(t)":
            y_mod=0.9*signal.unit_impulse(1401,700)
            mod_arrow_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[1]),rollover=1)
        else:
            for i in range(0,1401):
                t = x[i]
                if t < -0.5 or t > 0.5:
                    y_mod[i]=0.0
                elif t>=-0.5 and t<=0.5:
                    y_mod[i]=y[i]
        update_mod_functions(y_mod, y_FT_Re_mod, y_FT_Im_mod)
    elif new == "si(t)":
        if func_select.value == "\u03B4(t)":
            y_mod=0.9*signal.unit_impulse(1401,700)
            mod_arrow_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[1]),rollover=1)
        else:
            for i in range(0,1401):
                t = x[i]
                if t != 0:
                    y_mod[i]=y[i]*sin(t)/t
                elif t == 0:
                    y_mod[i]=y[i]
        update_mod_functions(y_mod, y_FT_Re_mod, y_FT_Im_mod)
    elif new == "\u03B4(t)":
        if func_select.value == "sin(t)":
            for i in range(0,1401):
                t = x[i]
                y_mod[i]=0
        else:
            y_mod=0.9*signal.unit_impulse(1401,700)
            mod_arrow_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[1]),rollover=1)
        update_mod_functions(y_mod, y_FT_Re_mod, y_FT_Im_mod)
    elif new == "1":
        if func_select.value == "\u03B4(t)":
            y_mod=0.9*signal.unit_impulse(1401,700)
            mod_arrow_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[1]),rollover=1)
        else:
            for i in range(0,1401):
                t = x[i]
                y_mod[i]=y[i]
        update_mod_functions(y_mod, y_FT_Re_mod, y_FT_Im_mod)
    elif new == "sin(t)":
        for i in range(0,1401):
            t = x[i]
            if func_select.value == "\u03B4(t)":
                y_mod[i]=0.0
            else:
                y_mod[i]=y[i]*sin(t)
        update_mod_functions(y_mod, y_FT_Re_mod, y_FT_Im_mod)   
    elif new == "cos(t)":
        if func_select.value == "\u03B4(t)":
            y_mod=0.9*signal.unit_impulse(1401,700)
            mod_arrow_source.stream(dict(x1=[0],y1=[0],x2=[0],y2=[1]),rollover=1)
        else:
            for i in range(0,1401):
                t = x[i]
                y_mod[i]=y[i]*cos(t)
        update_mod_functions(y_mod, y_FT_Re_mod, y_FT_Im_mod)     

   
def change_g_conv(attr,old,new):
    ""
def change_lambda1(attr,old,new):
    ""
def change_lambda2(attr,old,new):
    ""

changeMod(0,0,"Scaling")

                    
## Send to window
curdoc().add_root(layout)        
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '