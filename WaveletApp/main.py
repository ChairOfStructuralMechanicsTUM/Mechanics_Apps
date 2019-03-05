from os.path import dirname, split, join
import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt 
from math import sin, cos, pi, exp
from bokeh.plotting import Figure, show
from bokeh.models import ColumnDataSource, LinearColorMapper, LogTicker, ColorBar
from bokeh.layouts import widgetbox, layout
from bokeh.models.widgets import Button, Select, Slider, TextInput, Dropdown
from sympy import sympify, lambdify
from bokeh.io import curdoc
import traceback

from filled_contours import filled_contours

################
# Data Sources #
################
function_source = ColumnDataSource(data=dict(t=[],y=[]))
WaveLet_source = ColumnDataSource(data={'a': [],'b':[],'W':[]})
Wavelet_Function_source = ColumnDataSource(data=dict(t=[],y=[]))

###########
# FIGURES #
###########
plot_function = Figure(x_range=(0, 5), y_range=(-3, 3), 
                        x_axis_label='t', y_axis_label='f(t)',
                        active_scroll="wheel_zoom",
                        title="Function in the Original Domain")


plot_Wavelet = Figure(x_range=(0, 5), y_range=(0, 5),
                            x_axis_label='b', y_axis_label='a',
                            title="Wavelet transform of the function")
color_mapper = LinearColorMapper(palette="Spectral11")
color_bar = ColorBar(color_mapper=color_mapper, ticker=LogTicker(),
                     label_standoff=12, border_line_color=None, location=(0,0))

plot_Wavelet_Function = Figure(x_range=(-5, 5), y_range=(-5, 5),
                            x_axis_label='b', y_axis_label='u+03C8',
                            active_scroll="wheel_zoom",
                            title="Wavelet function")

# sample functions with corresponding id
sample_f_names = [
    ("Heaviside Function","Heaviside Function"),
    ("Rectangular Function","Rectangular Function"),
    ("Dirac delta Function","Dirac delta Function"),
   ("User defined function","User defined function")
]

sample_Wavelet_names = [
    ("Morlet Function","Morlet Function"),
    ("Meyer Function","Meyer Function"),
    ("Mexican hat Function","Mexican hat Function")
]


#######################
# INTERACTIVE WIDGETS #
#######################
T0_input = TextInput(value= '1', title="Input T0:")
T1_input = TextInput(value= '', title="Input T1:")
Amp_input = TextInput(value= '', title="Input Amplitude:")
User_Func = TextInput(value= '', title="Input Function f(t)")
sample_fun_input_f = Dropdown(label="Choose a sample function f(t)",
                              menu=sample_f_names,
                              width=200)
Wavelet_fun_input = Dropdown(label="Choose a wavelet function psi(t)",
                              menu=sample_Wavelet_names,
                              width=200)
Calc_button = Button(label="Calculate Wavelet Transform", button_type="success",width=100)


def Find_Heaviside_WT(T0,amp):
    # computation of WT
    n = 50
    a = np.linspace(0.1, 5, n)
    b = np.linspace(0.1, 5, n)
    W = np.zeros((len(a), len(b)))
    
    for i in range (0,len(a)):
        for j in range (0,len(b)):
            def integrand1(t):
                output = a[i]**-0.5 * amp * (t-b[j])/a[i] * exp(-( (t-b[j])/a[i] )**2.0)
                return output
            W[i][j]=quad(integrand1, T0, 12)[0]
    WaveLet_source.data = {'a': [a],'b':[b],'W':[W]}
    plot_Wavelet.image(image="W", source=WaveLet_source, color_mapper=color_mapper, x=0, y=0, dw=5, dh=5)
    # fig, ax = plt.subplots()
    # A, B = np.meshgrid(a, b)
    # contour = ax.contourf(A, B, W, extend='both', cmap='Spectral')
    # try:
    #     filled_contours(plot_Wavelet,  contour)
    # except:
    #     traceback.print_exc()
    #     raise
    # plot_Wavelet.patches(xs='a', ys='b', source=WaveLet_source, color='c', alpha='a')
    # plot_Wavelet.add_layout(color_bar, 'right')

def Find_Rectangular_WT(T0,T1,amp):
    # computation of WT
    n=200
    a=np.linspace(0.1,5,n)
    b=np.linspace(0.1,5,n)
    W=np.zeros((len(a), len(b)))

    for i in range (0,len(a)):
        for j in range (0,len(b)):
            def integrand1(t):
                output = a[i]**-0.5 * amp * (t-b[j])/a[i] * exp(-( (t-b[j])/a[i] )**2.0)
                return output
            W[i][j]=quad(integrand1, T0, T1)[0]
    WaveLet_source.data = {'a': [a],'b':[b],'W':[W]}
    plot_Wavelet.image(image="W", source=WaveLet_source, color_mapper=color_mapper, x=0, y=0, dw=5, dh=5)
    plot_Wavelet.add_layout(color_bar, 'right')

def Find_Dirac_WT(T0, amp):
    # computation of WT
    n=200
    a=np.linspace(0.1,5,n)
    b=np.linspace(0.1,5,n)
    W=np.zeros((len(a), len(b)))

    for i in range (0,len(a)):
        for j in range (0,len(b)):
            W[i][j]= a[i]**-0.5 * amp * (T0-b[j])/a[i] * exp(-( (T0-b[j])/a[i] )**2.0)
    WaveLet_source.data = {'a': [a],'b':[b],'W':[W]}
    plot_Wavelet.image(image="W", source=WaveLet_source, color_mapper=color_mapper, x=0, y=0, dw=5, dh=5)
    plot_Wavelet.add_layout(color_bar, 'right')

def Custom_Func_WT(user_func):
    n=60
    a=np.linspace(0.1,5,n)
    b=np.linspace(0.1,5,n)
    W=np.zeros((len(a), len(b)))
   
    #make a list of safe functions
    safe_dict = {
        'sin' : sin,
        'cos' : cos,
        'pi' : pi,
        'exp' : exp,
    }

    for i, a_i in enumerate(a):
        for j, b_j in enumerate(b):
            def integrand(t):
                safe_dict['t'] = t
                try:
                    return eval(user_func, safe_dict) *  a[i]**-0.5 * (t-b[j])/a[i] * exp(-( (t-b[j])/a[i] )**2.0)
                except NameError:
                    pass
            W[i][j]=quad(integrand, -12, 12)[0]
    WaveLet_source.data = {'a': [a],'b':[b],'W':[W]}
    plot_Wavelet.image(image="W", source=WaveLet_source, color_mapper=color_mapper, x=0, y=0, dw=5, dh=5)
    plot_Wavelet.add_layout(color_bar, 'right')

def update(attr, old, new):
    """
    Compute data depending on input function.
    """
    # Clear function and Wavelet plots
    #reset()

    global sample_function_id
    if (sample_function_id == "Heaviside Function"):
        # Extract parameters
        T_0 = float(sympify(T0_input.value.replace(',','.')))  # Interval
        T0_input.value = str(T_0)
        amp = float(sympify(Amp_input.value.replace(',','.')))  # Interval
        Amp_input.value = str(amp)

        function_source.data= dict(x=[0, T_0, T_0, 5] ,y=[0, 0, amp, amp])
        plot_function.line(x='x',y='y',source=function_source ,color="blue",line_width=3)
        Find_Heaviside_WT(T_0, amp)
    
    elif (sample_function_id == "Rectangular Function"):
        # Extract parameters
        T_0 = float(sympify(T0_input.value.replace(',','.')))  # Interval
        T0_input.value = str(T_0)
        T_1 = float(sympify(T1_input.value.replace(',','.')))  # Interval
        T1_input.value = str(T_1)
        amp = float(sympify(Amp_input.value.replace(',','.')))  # Interval
        Amp_input.value = str(amp)

        function_source.data= dict(x=[0, T_0, T_0, T_1, T_1, 5] ,y=[0, 0, amp, amp, 0, 0])
        plot_function.line(x='x',y='y',source=function_source ,color="blue",line_width=3)
        Find_Rectangular_WT(T_0, T_1 , amp)
    
    elif (sample_function_id == "Dirac delta Function"):
        # Extract parameters
        T_0 = float((T0_input.value.replace(',','.')))  # Interval
        T0_input.value = str(T_0)
        amp = float((Amp_input.value.replace(',','.')))  # Interval
        Amp_input.value = str(amp)

        function_source.data= dict(x=[0, T_0, T_0, T_0, 5] ,y=[0, 0, amp, 0, 0])
        plot_function.line(x='x',y='y',source=function_source ,color="blue",line_width=3)
        Find_Dirac_WT(T_0, amp)
    
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

        user_f= eval(User_Func.value, safe_dict)
        function_source.data= dict(x=t ,y=user_f)
        plot_function.line(x='x',y='y',source=function_source ,color="blue",line_width=3)
        Custom_Func_WT(User_Func.value)

def sample_fun_input_modified(self):
    """
    Called if the sample function is changed.
    :param self:
    :return:
    """
    reset()
    
    global sample_function_id
  
    # get the id
    sample_function_id = sample_fun_input_f.value
    sample_fun_input_f.label=sample_function_id

    if (sample_function_id == "Heaviside Function"):
        controls = [sample_fun_input_f, T0_input, Amp_input, Wavelet_fun_input]
        controls_box = widgetbox(controls, sizing_mode='scale_width')
        My_Layout.children[0].children[0]= controls_box  # all controls
        
    elif (sample_function_id == "Rectangular Function"):
        controls = [sample_fun_input_f, T0_input, T1_input, Amp_input, Wavelet_fun_input]
        controls_box = widgetbox(controls, sizing_mode='scale_width')  # all controls
        My_Layout.children[0].children[0]= controls_box  # all controls
    
    elif (sample_function_id == "Dirac delta Function"):
        controls = [sample_fun_input_f, T0_input, Amp_input, Wavelet_fun_input]
        controls_box = widgetbox(controls, sizing_mode='scale_width')  # all controls
        My_Layout.children[0].children[0]= controls_box  # all controls

    elif (sample_function_id == "User defined function"):
        controls = [sample_fun_input_f, User_Func, Wavelet_fun_input]
        controls_box = widgetbox(controls, sizing_mode='scale_width')  # all controls
        My_Layout.children[0].children[0]= controls_box  # all controls

def Wavelet_fun_modified(self):

    Wavelet_function_id = Wavelet_fun_input.value
    if (Wavelet_function_id == "Morlet Function"):
        Wavelet_fun_input.label=Wavelet_function_id
        n=200
        t=np.linspace(-5,5,n)
        y= t*np.exp(-t**2)
        Wavelet_Function_source.data = dict(t=t, y=y)
        plot_Wavelet_Function.line('t', 'y', color='red', source=Wavelet_Function_source, line_width=3)

def reset():
    # T0_input.value=' '
    # T1_input.value=' '
    # Amp_input.value=' '
    function_source.data = dict(x=[],y=[])
    WaveLet_source.data = {'a': [],'b':[],'W':[]}


T1_input.value
# add callback behaviour
sample_fun_input_f.on_click(sample_fun_input_modified)
Wavelet_fun_input.on_click(Wavelet_fun_modified)
Calc_button.on_click(update)
T0_input.on_change('value',update)
T1_input.on_change('value',update)
Amp_input.on_change('value',update)
User_Func.on_change('value',update)

# create layout
controls = [sample_fun_input_f, Wavelet_fun_input]
controls_box = widgetbox(controls, sizing_mode='scale_width')  # all controls
My_Layout = layout([[controls_box, plot_function],[plot_Wavelet_Function,plot_Wavelet]],sizing_mode='stretch_both')
curdoc().add_root(My_Layout) # add plots and controls to root
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '