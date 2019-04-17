from os.path import dirname, split, join, abspath
import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt 
from math import sin, cos, pi, exp
from bokeh.plotting import Figure
from bokeh.models import ColumnDataSource, Div, LinearColorMapper, LogTicker, ColorBar
from bokeh.layouts import widgetbox, layout, column, row, Spacer
from bokeh.models.widgets import Button, Select, Slider, TextInput, Dropdown, Div
from sympy import sympify, lambdify
from bokeh.io import curdoc
import traceback
from scriptWT import*
from MorletWT import*

from filled_contours import filled_contours
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexDiv, LatexLegend

################    
# Data Sources #
################
function_source = ColumnDataSource(data=dict(t=[],y=[]))
WaveLet_source = ColumnDataSource(data={'a': [],'b':[],'W':[]})
Wavelet_Function_source = ColumnDataSource(data=dict(t=[],y=[]))

###########
# FIGURES #
###########
toolset=["pan, wheel_zoom, reset"]
plot_function = Figure(x_range=(0, 5), y_range=(-3, 3), 
                        x_axis_label='t', y_axis_label='f(t)',
                        tools =toolset,
                        title="Function in the Original Domain",  width=650, height=300)
plot_function.toolbar.logo = None

plot_Wavelet = Figure(x_range=(0, 5), y_range=(0, 5),
                            x_axis_label='b', y_axis_label='a',
                            tools =toolset,
                            title="Wavelet transform of the function",  width=650, height=300)
plot_Wavelet.toolbar.logo = None
color_mapper = LinearColorMapper(palette="Spectral11")
color_bar = ColorBar(color_mapper=color_mapper, ticker=LogTicker(),
                     label_standoff=12, border_line_color=None, location=(0,0))

plot_Wavelet_Function = Figure(x_range=(-10, 10), y_range=(-2, 2),
                            x_axis_label='t', y_axis_label='psi(t)',
                            tools=toolset,
                            title="Wavelet function",  width=650, height=300)
plot_Wavelet_Function.toolbar.logo = None

# sample functions with corresponding id
sample_f_names = [
    ("Heaviside function","Heaviside function"),
    ("Rectangular function","Rectangular function"),
    ("Dirac delta function","Dirac delta function"),
   ("User defined function","User defined function")
]

sample_Wavelet_names = [
    ("Morlet function","Morlet function"),
    ("script's WT","script's WT")
    #("Meyer Function","Meyer Function"),
    #("Mexican hat Function","Mexican hat Function")
]

# function and corresponding FT
sample_Wavelet_functions = {
    "Morlet Function":"exp(-(((t-b[j]])/a[i]])**2)/2) * cos(5*((t-b[j]])/a[i]]))",
    "Meyer Function":"",
    "Mexican hat Function":""
}

#######################
# INTERACTIVE WIDGETS #
#######################
T0_input = TextInput(value= '1.0', title="Input T0:", width=200)
T1_input = TextInput(value= '2.0', title="Input T1:", width=200)
Amp_input = TextInput(value= '1.0', title="Input Amplitude:", width=200)
User_Func = TextInput(value= None, title="Input Function f(t)", width=200)
Resolution = TextInput(value= '60', title="Input resolution:", width=200)
sample_fun_input_f = Dropdown(label="Choose a sample function f(t)",
                              menu=sample_f_names,
                              width=200)
Wavelet_fun_input = Dropdown(label="Choose a wavelet function psi(t)",
                              menu=sample_Wavelet_names,
                              width=200)
Calc_button = Button(label="Calculate Wavelet Transform", button_type="success",width=100)

def Plot_WT(a,b,W):
    WaveLet_source.data = {'a': [a],'b':[b],'W':[W]}
    plot_Wavelet.image(image="W", source=WaveLet_source, color_mapper=color_mapper, x=0, y=0, dw=5, dh=5)

def update(attr, old, new):
    """
    Compute depending on input function.
    """
    sample_function_id = sample_fun_input_f.value
    Wavelet_function_id = Wavelet_fun_input.value
    Resolut=int(sympify(Resolution.value.replace(',','.')))  # Interval
    Resolution.value=str(Resolut)
    My_Layout.children[0].children[2].children[1].children[0] = loading

    if (sample_function_id == "Heaviside function"):
        # Extract parameters
        T_0 = float(sympify(T0_input.value.replace(',','.')))  # Interval
        T0_input.value = str(T_0)
        amp = float(sympify(Amp_input.value.replace(',','.')))  # Interval
        Amp_input.value = str(amp)

        function_source.data= dict(x=[0, T_0, T_0, 5] ,y=[0, 0, amp, amp])
        plot_function.line(x='x',y='y',source=function_source ,color="blue",line_width=3)
        if (Wavelet_function_id == "Morlet function"):
            a,b,W = Find_Heaviside_Morlet_WT(T_0, amp, Resolut)
        elif (Wavelet_function_id == "script's WT"):
            a,b,W = Find_Heaviside_SWT(T_0, amp, Resolut)
        try:
            Plot_WT(a,b,W)
        except UnboundLocalError:
            My_Layout.children[0].children[2].children[1].children[0] = choose_WaveLet
            return None

            
    
    elif (sample_function_id == "Rectangular function"):
        # Extract parameters
        T_0 = float(sympify(T0_input.value.replace(',','.')))  # Interval
        T_1 = float(sympify(T1_input.value.replace(',','.')))  # Interval
        amp = float(sympify(Amp_input.value.replace(',','.')))  # Interval
        Amp_input.value = str(amp)
        # if T0>T1, swap numbers
        if(T_0>T_1):
            temp=T_1
            T_1=T_0
            T_0=temp
        T0_input.value = str(T_0)
        T1_input.value = str(T_1)

        function_source.data= dict(x=[0, T_0, T_0, T_1, T_1, 5] ,y=[0, 0, amp, amp, 0, 0])
        plot_function.line(x='x',y='y',source=function_source ,color="blue",line_width=3)
        if (Wavelet_function_id == "Morlet function"):
            a,b,W = Find_Rectangular_Morlet_WT(T_0, T_1 , amp, Resolut)
        elif (Wavelet_function_id == "script's WT"):
            a,b,W = Find_Rectangular_SWT(T_0, T_1 , amp, Resolut)
        try:
            Plot_WT(a,b,W)
        except UnboundLocalError:
            My_Layout.children[0].children[2].children[1].children[0] = choose_WaveLet
            return None

    elif (sample_function_id == "Dirac delta function"):
        # Extract parameters
        T_0 = float((T0_input.value.replace(',','.')))  # Interval
        T0_input.value = str(T_0)
        amp = float((Amp_input.value.replace(',','.')))  # Interval
        Amp_input.value = str(amp)

        function_source.data= dict(x=[0, T_0, T_0, T_0, 5] ,y=[0, 0, amp, 0, 0])
        plot_function.line(x='x',y='y',source=function_source ,color="blue",line_width=3)
        if (Wavelet_function_id == "Morlet function"):
            a,b,W = Find_Dirac_Morlet_WT(T_0, amp, Resolut)
        elif (Wavelet_function_id == "script's WT"):
            a,b,W = Find_Dirac_SWT(T_0, amp, Resolut)
        try:
            Plot_WT(a,b,W)
        except UnboundLocalError:
            My_Layout.children[0].children[2].children[1].children[0] = choose_WaveLet
            return None

    elif (sample_function_id == "User defined function"):
        n=500
        t=np.linspace(-5,5,n)
        #make a list of safe functions
        safe_dict = {
        'sin' : np.sin,
        'cos' : np.cos,
        'pi' : np.pi,
        'exp' : np.exp,
        't'  : t
        }
        print("check2")
        try:
            user_f= eval(User_Func.value, safe_dict)
        except (SyntaxError, TypeError, NameError):
            My_Layout.children[0].children[2].children[1].children[0] = user_function
            return None
        print("check3")
        try:
            function_source.data= dict(x=t ,y=user_f)
        except ValueError:
            My_Layout.children[0].children[2].children[1].children[0] = user_function
            return None
        print("check4")
        plot_function.line(x='x',y='y',source=function_source ,color="blue",line_width=3)
        if (Wavelet_function_id == "Morlet function"):
            a,b,W = Find_Custom_Morlet_WT(User_Func.value, Resolut)
        elif (Wavelet_function_id == "script's WT"):
            a,b,W = Find_Custom_SWT(User_Func.value,Resolut)
        try:
            Plot_WT(a,b,W)
        except UnboundLocalError:
            My_Layout.children[0].children[2].children[1].children[0] = choose_WaveLet
            return None
    
    My_Layout.children[0].children[2].children[1].children[0] = plot_Wavelet

def sample_fun_input_modified(self):
    """
    Called if the sample function is changed.
    :param self:
    :return:
    """
    reset()
    
    # global sample_function_id
  
    # get the id
    sample_function_id = sample_fun_input_f.value
    sample_fun_input_f.label=sample_function_id

    if (sample_function_id == "Heaviside function"):
        controls = [sample_fun_input_f, T0_input, Amp_input]
        controls_box = widgetbox(controls, sizing_mode='scale_width')
        My_Layout.children[0].children[1].children[0].children[0]= controls_box
        
    elif (sample_function_id == "Rectangular function"):
        controls = [sample_fun_input_f, T0_input, T1_input, Amp_input]
        controls_box = widgetbox(controls, sizing_mode='scale_width')  # all controls
        My_Layout.children[0].children[1].children[0].children[0]= controls_box
    
    elif (sample_function_id == "Dirac delta function"):
        controls = [sample_fun_input_f, T0_input, Amp_input]
        controls_box = widgetbox(controls, sizing_mode='scale_width')  # all controls
        My_Layout.children[0].children[1].children[0].children[0]= controls_box

    elif (sample_function_id == "User defined function"):
        controls = [sample_fun_input_f, User_Func]
        controls_box = widgetbox(controls, sizing_mode='scale_width')  # all controls
        My_Layout.children[0].children[1].children[0].children[0]= controls_box
    
    if (Wavelet_fun_input.value == ""):
        My_Layout.children[0].children[2].children[1].children[0] = choose_WaveLet


def Wavelet_fun_modified(self):

    Wavelet_function_id = Wavelet_fun_input.value
    Wavelet_fun_input.label=Wavelet_function_id
    n=200
    t=np.linspace(-10,10,n)
    
    if (Wavelet_function_id == "Morlet function"):
        y= np.exp(-(t**2)/2) * np.cos(5*t)
        Wavelet_Function_source.data = dict(t=t, y=y)
        WT = plot_Wavelet_Function.line('t', 'y', color='red', source=Wavelet_Function_source, line_width=2)
        plot_Wavelet_Function.add_layout(LatexLegend(items=[("e^{\\frac{t^2}{2}} \cos{(5t)}",[WT])], label_text_font_size='12pt', label_height= 20, label_width=40))
        
    elif (Wavelet_function_id == "script's WT"):
        y= t * np.exp(-t**2)
        Wavelet_Function_source.data = dict(t=t, y=y)
        WT = plot_Wavelet_Function.line('t', 'y', color='red', source=Wavelet_Function_source, line_width=2)
        plot_Wavelet_Function.add_layout(LatexLegend(items=[("                      {t} e^{-t^2}",[WT])], label_text_font_size='12pt', label_height= 20, label_width=40))
    
 
def reset():
    #  T0_input.value=''
    #  T1_input.value=''
    #  Amp_input.value='' 
     function_source.data = dict(x=[],y=[])
     WaveLet_source.data = {'a': [],'b':[],'W':[]}

def param_change(attr,old,new):
    Wavelet_function_id = Wavelet_fun_input.value
    Wavelet_fun_input.label=Wavelet_function_id
    n=400
    t=np.linspace(-10,10,n)
    if (Wavelet_function_id == "Morlet Function"):
        y= np.exp(-(((t-b_param.value)/a_param.value)**2)/2) * np.cos(5*((t-b_param.value)/a_param.value))
        Wavelet_Function_source.data = dict(t=t, y=y)
        plot_Wavelet_Function.line('t', 'y', color='red', source=Wavelet_Function_source, line_width=2)
        #plot_function.line('t', 'y', color='red', source=Wavelet_Function_source, line_width=2)
    
    elif (Wavelet_function_id == "script's WT"):
        y= (t-b_param.value)/a_param.value * np.exp(-((t-b_param.value)/a_param.value)**2)
        Wavelet_Function_source.data = dict(t=t, y=y)
        plot_Wavelet_Function.line('t', 'y', color='red', source=Wavelet_Function_source, line_width=2)
        #plot_function.line('t', 'y', color='red', source=Wavelet_Function_source, line_width=2)

 

# Create sliders to choose parameters
a_param = Slider(title="Scaling parameter 'a'", value=1.0, start=0.5, end=5.0, step=0.1,width=200)
a_param.on_change('value', param_change)

b_param = Slider(title="Shifting parameter 'b'", value=0.0, start=0.0, end=5.0, step=0.1,width=200)
b_param.on_change('value', param_change)

# add callback behaviour
sample_fun_input_f.on_click(sample_fun_input_modified)
Wavelet_fun_input.on_click(Wavelet_fun_modified)
Wavelet_fun_input.on_change('label',update)
Calc_button.on_click(update)
T0_input.on_change('value',update)
T1_input.on_change('value',update)
Amp_input.on_change('value',update)
User_Func.on_change('value',update)
Resolution.on_change('value',update)

#Description
description_filename = join(dirname(__file__), "description.html")
loading_spinner_filename = join(dirname(__file__), "loading_spinner.html")
choose_WaveLet_error_filename = join(dirname(__file__), "choose_WaveLet_error.html")
user_function_error_filename = join(dirname(__file__), "user_function_error.html")

description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1250)
loading = Div(text=open(loading_spinner_filename).read(), render_as_text=False, width=650, height=100)
choose_WaveLet = Div(text=open(choose_WaveLet_error_filename).read(), render_as_text=False, width=650, height=100)
user_function = Div(text=open(user_function_error_filename).read(), render_as_text=False, width=650, height=100)

# create layout
controls = [sample_fun_input_f]
controls_box = widgetbox(controls, sizing_mode='scale_width')  # all controls
#My_Layout = layout([[description],[controls_box, plot_function],[plot_Wavelet_Function,plot_Wavelet],
#            [column(row(Wavelet_fun_input),row(a_param, b_param))]],sizing_mode='stretch_both')
My_Layout = layout([column(description, row( column(controls_box), Spacer(width=10), column(Wavelet_fun_input,a_param, b_param, Resolution) , Spacer(width=135), column(plot_function) ), row( column(plot_Wavelet_Function), column(plot_Wavelet) ) )])
# curdoc().add_root(column([description,row([controls_box, plot_function]),row([plot_Wavelet_Function,plot_Wavelet]),
#             row([Wavelet_fun_input]),row([a_param, b_param])])) # add plots and controls to root
# My_Layout= [column(description, row( column(controls_box), Spacer(width=350), column(plot_function) ), row( column(plot_Wavelet_Function), column(plot_Wavelet) ), 
#             row( column(Wavelet_fun_input,a_param, b_param) ) )]
curdoc().add_root(My_Layout) # add plots and controls to root
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '