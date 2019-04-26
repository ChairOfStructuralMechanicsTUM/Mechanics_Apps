from os.path import dirname, split, join, abspath
import numpy as np
from math import sin, cos, pi, exp, ceil
import colorcet as cc
from bokeh.plotting import Figure, show
from bokeh.models import ColumnDataSource, Div, LinearColorMapper, ColorBar,BasicTicker
from bokeh.layouts import widgetbox, layout, column, row, Spacer
from bokeh.models.widgets import Button, RadioButtonGroup, Select, Slider, TextInput, Dropdown, Div
from sympy import sympify
from bokeh.io import curdoc
from Wavelet_Two import*
from Wavelet_One import*
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
toolset=["save, wheel_zoom, reset"]
plot_function = Figure(x_range=(0, 5), y_range=(-3, 3), 
                        x_axis_label='t', y_axis_label='f(t)',
                        tools =toolset,
                        title="Function in the Original Domain",  width=650, height=300)
plot_function.toolbar.logo = None

plot_Wavelet = Figure(x_range=(0, 5), y_range=(0, 5),
                            x_axis_label='b', y_axis_label='a',
                            tools =toolset,
                            title="Wavelet Transform of the Function",  width=650, height=300)
plot_Wavelet.toolbar.logo = None
color_mapper = LinearColorMapper(palette=cc.palette.CET_R2)
color_bar = ColorBar(color_mapper=color_mapper,
                     label_standoff=12, border_line_color=None, location=(0,0))
plot_Wavelet.add_layout(color_bar, 'right')

plot_Wavelet_Function = Figure(x_range=(-10, 10), y_range=(-2, 2),
                            x_axis_label='t', y_axis_label = ""u"\u03A8 (t)",
                            tools=toolset,
                            title="Wavelet function",  width=650, height=300)
# plot_Wavelet_Function.yaxis.axis_label = ""u"\u03A8 (t)" 
plot_Wavelet_Function.toolbar.logo = None

# sample functions with corresponding id
sample_f_names = [
    ("Heaviside function","Heaviside function"),
    ("Rectangular function","Rectangular function"),
    ("Dirac delta function","Dirac delta function"),
    ("Trigonometric function","Trigonometric function"),
   ("User defined function","User defined function")
]

# sample wavelet functions with corresponding id
sample_Wavelet_names = [
    ("Wavelet 1","Wavelet 1"),
    ("Wavelet 2","Wavelet 2")
]


#######################
# INTERACTIVE WIDGETS #
#######################
T0_input = TextInput(value= '1.0', width=200)
T1_input = TextInput(value= '3.0', title="Input t"u"\u2080 "u"\u2264 t "u"\u2081 "u"\u2264 5:", width=200)
Amp_input = TextInput(value= '1.0', title="Input -3 "u"\u2264 Amplitude "u"\u2264 3:", width=200)
User_Func = TextInput(value= None, title="Input function f(t):", width=200)
Resolution = TextInput(value= '60', title="Input resolution:", width=200)
sample_fun_input_f = Dropdown(label="Choose a sample function f(t)",
                              menu=sample_f_names,
                              width=200)
Wavelet_fun_input = Dropdown(label="Choose a wavelet function "u"\u03A8 (t)",
                              menu=sample_Wavelet_names,
                              width=200)
a_param = Slider(title="Scaling parameter 'a'", value=1.0, start=0.5, end=5.0, step=0.1,width=200)
b_param = Slider(title="Shifting parameter 'b'", value=0.0, start=-10.0, end=10.0, step=0.2,width=200)
Trigonometric_radio = RadioButtonGroup (labels=["sin", "cos"], active=0)
Frequency_Slider = Slider(title="Frequency (Hz)", value=1.0, start=0.5, end=5.0, step=0.1,width=200)
Calc_button = Button(label="Calculate Wavelet Transform", button_type="success",width=100)


#############
# Functions #
#############

def Plot_WT(a,b,W):
    """
    This function plots theWavelet transform
    input: 
        a: array_like of size (1xResolut), discretization of the y-axis
        b: array_like of size (1xResolut), discretization of the x-axis
        W: array_like of size (ResolutxResolut), matrix containing the wavelet transform value at each (a,b)
        
    """
    WaveLet_source.data = {'a': [a],'b':[b],'W':[W]}
    plot_Wavelet.image(image="W", source=WaveLet_source, palette=cc.palette.CET_R2, x=0, y=0, dw=5, dh=5)
    color_bar.ticker = BasicTicker()
    color_mapper.low = W.min()
    color_mapper.high = W.max()
  
def update(attr, old, new):
    """ 
    This function updates the app if one of the following interactive widgets value is changed:
        T0_input, T1_input, Amp_input, User_Func, Resolution, Calc_button
    return: None
    """
    # Check if the user selected both a sample function & and wavelet function
    if (sample_fun_input_f.label == "Choose a sample function f(t)"):
        My_Layout.children[0].children[2].children[1].children[0] = choose_SampleFunc  # Choose a sample function warning
        return None
    if (Wavelet_fun_input.label == "Choose a wavelet function "u"\u03A8 (t)"):
        My_Layout.children[0].children[2].children[1].children[0] = choose_WaveLet  # Choose a sample function warning
        return None

    sample_function_id = sample_fun_input_f.value 
    Wavelet_function_id = Wavelet_fun_input.value
    Resolut=int(sympify(Resolution.value.replace(',','.')))
    Resolution.value=str(Resolut)
    My_Layout.children[0].children[2].children[1].children[0] = loading # Computation loading spinner

    # Extract parameters and account for German dot
    T_0 = float(sympify(T0_input.value.replace(',','.')))
    T_1 = float(sympify(T1_input.value.replace(',','.')))
    amp = float(sympify(Amp_input.value.replace(',','.')))
    Amp_input.value = str(amp)

    if (sample_function_id == "Heaviside function"):  

        T0_input.value = str(T_0)
        # Plot heaviside function
        function_source.data = dict(x=[0, T_0, T_0, 5] ,y=[0, 0, amp, amp])
        plot_function.line(x='x',y= 'y',source= function_source ,color= "blue",line_width=3)

        # Determine which wavelet function to use for computation
        if (Wavelet_function_id == "Wavelet 1"):
            a,b,W = Find_Heaviside_Wavelet_One(T_0, amp, Resolut)
        elif (Wavelet_function_id == "Wavelet 2"):
            a,b,W = Find_Heaviside_Wavelet_Two(T_0, amp, Resolut)

    elif (sample_function_id == "Rectangular function"):

        # if T0>T1, swap values
        if(T_0>T_1):
            temp = T_0
            T_0 = T_1
            T_1 = temp
            #T_0 , T_1 = T_1 , T_0

        T0_input.value = str(T_0)
        T1_input.value = str(T_1)

        # Plot rectangular function
        function_source.data= dict(x=[0, T_0, T_0, T_1, T_1, 5] ,y=[0, 0, amp, amp, 0, 0])
        plot_function.line(x='x',y='y',source=function_source ,color="blue",line_width=3)

        # Determine which wavelet function to use for computation
        if (Wavelet_function_id == "Wavelet 1"):
            a,b,W = Find_Rectangular_Wavelet_One(T_0, T_1 , amp, Resolut)
        elif (Wavelet_function_id == "Wavelet 2"):
            a,b,W = Find_Rectangular_Wavelet_Two(T_0, T_1 , amp, Resolut)

    elif (sample_function_id == "Dirac delta function"):

        function_source.data= dict(x=[0, T_0, T_0, T_0, 5] ,y=[0, 0, amp, 0, 0])
        plot_function.line(x='x',y='y',source=function_source ,color="blue",line_width=3)

        # Determine which wavelet function to use for computation
        if (Wavelet_function_id == "Wavelet 1"):
            a,b,W = Find_Dirac_Wavelet_One(T_0, amp, Resolut)
        elif (Wavelet_function_id == "Wavelet 2"):
            a,b,W = Find_Dirac_Wavelet_Two(T_0, amp, Resolut)
    
    elif (sample_function_id == "Trigonometric function"):

        # Determine which wavelet function to use for computation
        if (Wavelet_function_id == "Wavelet 1"):
            a,b,W = Find_Trig_Wavelet_One (Trigonometric_radio.active, Frequency_Slider.value, Resolut)
        elif (Wavelet_function_id == "Wavelet 2"):
            a,b,W = Find_Trig_Wavelet_Two (Trigonometric_radio.active, Frequency_Slider.value, Resolut)

    elif (sample_function_id == "User defined function"):
        
        n=200
        t=np.linspace(-5,5,n)
        
        # Make a list of safe functions
        safe_dict = {
        'sin' : np.sin,
        'cos' : np.cos,
        'pi' : np.pi,
        'exp' : np.exp,
        't'  : t
        }

        try:
            user_f= eval(User_Func.value, safe_dict)
            function_source.data= dict(x=t ,y=user_f)
        except (SyntaxError, TypeError, NameError, ValueError):
            My_Layout.children[0].children[2].children[1].children[0] = user_function   # Choose a valid function warning
            return None
        
        # Plot user defined function
        plot_function.line(x='x',y='y',source=function_source ,color="blue",line_width=3)

        # Determine which wavelet function to use for computation
        if (Wavelet_function_id == "Wavelet 1"):
            a,b,W = Find_Custom_Wavelet_One(User_Func.value, Resolut)
        elif (Wavelet_function_id == "Wavelet 2"):
            a,b,W = Find_Custom_Wavelet_Two(User_Func.value,Resolut)
    
    Plot_WT(a,b,W)
    My_Layout.children[0].children[2].children[1].children[0] = plot_Wavelet    # Put the "plot_Wavelet" figure back to show the result 

def sample_fun_input_modified(self):
    """
    This function is called to change the layout of the interactive widgets according the new selected sample function
    """
    # Clear existing function and its wavelet transform plots
    reset()
  
    # Get the new sample function id
    sample_function_id = sample_fun_input_f.value
    sample_fun_input_f.label=sample_function_id

    # Change the Layout of interactive widgets according to sample functin id
    if (sample_function_id == "Heaviside function"):
        T0_input.title = "Input 0 "u"\u2264  t"u"\u2080 "u"\u2264 5:"
        controls = [sample_fun_input_f, T0_input, Amp_input]
        controls_box = widgetbox(controls, sizing_mode='scale_width')
        My_Layout.children[0].children[1].children[0].children[0]= controls_box
        
    elif (sample_function_id == "Rectangular function"):
        T0_input.title = "Input 0 "u"\u2264  t"u"\u2080 "u"\u2264 t"u"\u2081:"
        controls = [sample_fun_input_f, T0_input, T1_input, Amp_input]
        controls_box = widgetbox(controls, sizing_mode='scale_width')  # all controls
        My_Layout.children[0].children[1].children[0].children[0]= controls_box
    
    elif (sample_function_id == "Dirac delta function"):
        T0_input.title = "Input 0 "u"\u2264  t"u"\u2080 "u"\u2264 5:"
        controls = [sample_fun_input_f, T0_input, Amp_input]
        controls_box = widgetbox(controls, sizing_mode='scale_width')  # all controls
        My_Layout.children[0].children[1].children[0].children[0]= controls_box
    
    elif (sample_function_id == "Trigonometric function"):
        controls = [sample_fun_input_f, Trigonometric_radio, Frequency_Slider, Calc_button]
        controls_box = widgetbox(controls, sizing_mode='scale_width')  # all controls
        My_Layout.children[0].children[1].children[0].children[0]= controls_box

    elif (sample_function_id == "User defined function"):
        controls = [sample_fun_input_f, User_Func]
        controls_box = widgetbox(controls, sizing_mode='scale_width')  # all controls
        My_Layout.children[0].children[1].children[0].children[0]= controls_box

def Wavelet_fun_modified(self):
    """
    This function is called to plot the new selected wavelet function
    """
    # Get the new wavelet function id
    Wavelet_function_id = Wavelet_fun_input.value
    Wavelet_fun_input.label = Wavelet_function_id
    n = 200
    t=np.linspace(-10,10,n)
    
    if (Wavelet_function_id == "Wavelet 1"):
        y= np.exp(-(t**2)/2) * np.cos(5*t)
        # Plot wavelet
        Wavelet_Function_source.data = dict(t=t, y=y)
        WT = plot_Wavelet_Function.line('t', 'y', color='red', source=Wavelet_Function_source, line_width=2)
        plot_Wavelet_Function.add_layout(LatexLegend(items=[("e^{\\frac{t^2}{2}} \cos{(5t)}",[WT])], label_text_font_size='12pt', label_height= 20, label_width=40))
        
    elif (Wavelet_function_id == "Wavelet 2"):
        y= t * np.exp(-t**2)
        # Plot wavelet
        Wavelet_Function_source.data = dict(t=t, y=y)
        WT = plot_Wavelet_Function.line('t', 'y', color='red', source=Wavelet_Function_source, line_width=2)
        plot_Wavelet_Function.add_layout(LatexLegend(items=[("                       {t} e^{-t^2}",[WT])], label_text_font_size='12pt', label_height= 20, label_width=40))
    
def Trig_fun_modified(attr, old, new):
    """
    Called to plot the new selected trigonometric function
    """
    # Clear existing function and its wavelet transform plots 
    reset()

    n=200
    t=np.linspace(0,5,n)

    # The value "0" corresponds to sin & "1" to cos
    if (Trigonometric_radio.active == 0):
        y= np.sin( 2 * np.pi * Frequency_Slider.value *t )
        function_source.data= dict(x=t ,y=y )
        plot_function.line(x='x',y='y',source=function_source ,color="blue",line_width=3)
    
    elif (Trigonometric_radio.active == 1):
        y= np.cos( 2 * np.pi * Frequency_Slider.value *t )
        function_source.data = dict(x=t ,y=y )
        plot_function.line(x='x',y='y',source=function_source ,color="blue",line_width=3)

def reset():
    """
    This funcion clears the function and its wavelet transform plots 
    """
    function_source.data = dict(x=[],y=[])
    WaveLet_source.data = {'a': [],'b':[],'W':[]}

def param_change(attr,old,new):
    """
    This function is called to plot a new wavelet function if "a" or "b" parameters are changed
    """
    # Get the new wavelet function id
    Wavelet_function_id = Wavelet_fun_input.value
    Wavelet_fun_input.label = Wavelet_function_id
    n=200
    t=np.linspace(-10,10,n)

    if (Wavelet_function_id == "Wavelet 1"):
        y= np.exp(-(((t-b_param.value)/a_param.value)**2)/2) * np.cos(5*((t-b_param.value)/a_param.value))
        Wavelet_Function_source.data = dict(t=t, y=y)
        plot_Wavelet_Function.line('t', 'y', color='red', source=Wavelet_Function_source, line_width=2)
        #plot_function.line('t', 'y', color='red', source=Wavelet_Function_source, line_width=2)
    
    elif (Wavelet_function_id == "Wavelet 2"):
        y= (t-b_param.value)/a_param.value * np.exp(-((t-b_param.value)/a_param.value)**2)
        Wavelet_Function_source.data = dict(t=t, y=y)
        plot_Wavelet_Function.line('t', 'y', color='red', source=Wavelet_Function_source, line_width=2)
        #plot_function.line('t', 'y', color='red', source=Wavelet_Function_source, line_width=2)


######################
# Callback behaviour #
######################
sample_fun_input_f.on_click(sample_fun_input_modified)
Wavelet_fun_input.on_click(Wavelet_fun_modified)
Wavelet_fun_input.on_change('label', update)
T0_input.on_change('value', update)
T1_input.on_change('value', update)
Amp_input.on_change('value', update)
User_Func.on_change('value', update)
Resolution.on_change('value', update)
a_param.on_change('value', param_change)
b_param.on_change('value', param_change)
Trigonometric_radio.on_change('active',Trig_fun_modified)
Frequency_Slider.on_change('value',Trig_fun_modified)
Calc_button.on_change('clicks',update)


############################
# Description and warnings #
############################
description_filename = join(dirname(__file__), "description.html")
loading_spinner_filename = join(dirname(__file__), "loading_spinner.html")
choose_WaveLet_error_filename = join(dirname(__file__), "choose_WaveLet_error.html")
choose_SampleFunc_error_filename = join(dirname(__file__), "choose_SampleFunc_error.html")
user_function_error_filename = join(dirname(__file__), "user_function_error.html")
    
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1250)
loading = Div(text=open(loading_spinner_filename).read(), render_as_text=False, width=650, height=100)
choose_WaveLet = Div(text=open(choose_WaveLet_error_filename).read(), render_as_text=False, width=650, height=100)
choose_SampleFunc = Div(text=open(choose_SampleFunc_error_filename).read(), render_as_text=False, width=650, height=100)
user_function = Div(text=open(user_function_error_filename).read(), render_as_text=False, width=650, height=100)


#################
# Create layout #
#################
controls = [sample_fun_input_f]
controls_box = widgetbox(controls, sizing_mode='scale_width')  # all controls
My_Layout = layout([column(description, row( column(controls_box), Spacer(width=10), column(Wavelet_fun_input,a_param, b_param, Resolution) , Spacer(width=135), column(plot_function) ), row( column(plot_Wavelet_Function), column(plot_Wavelet) ) )])
curdoc().add_root(My_Layout) # add plots and controls to root
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '