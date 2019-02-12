from os.path import dirname, split, join
import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt 
from math import exp
from bokeh.plotting import Figure, show
from bokeh.models import ColumnDataSource, LinearColorMapper, LogTicker, ColorBar
from bokeh.layouts import widgetbox, layout
from bokeh.models.widgets import Button, Select, Slider,TextInput,Dropdown
from sympy import sympify, lambdify
from bokeh.io import curdoc

################
# Data Sources #
################
function_source = ColumnDataSource(data=dict(t=[],y=[]))
WaveLet_source = ColumnDataSource(data={'a': [],'b':[],'W':[]})

###########
# FIGURES #
###########
plot_function = Figure(x_range=(0, 5), y_range=(0, 3), 
                        x_axis_label='t', y_axis_label='f(t)',
                        active_scroll="wheel_zoom",
                        title="Function in the Original Domain")


plot_Wavelet = Figure(x_range=(0, 5), y_range=(0, 5),
                            x_axis_label='b', y_axis_label='a',
                            active_scroll="wheel_zoom",
                            title="Wavelet transform of the function")
color_mapper = LinearColorMapper(palette="Spectral11")
color_bar = ColorBar(color_mapper=color_mapper, ticker=LogTicker(),
                     label_standoff=12, border_line_color=None, location=(0,0))

# sample functions with corresponding id
sample_f_names = [
    ("Heaviside Function","Heaviside Function"),
    ("Rectangular Function","Rectangular Function"),
    ("Dirac delta Function","Dirac delta Function"),
   ("Trigonometric Function","Trigonometric Function")
]


#######################
# INTERACTIVE WIDGETS #
#######################
T0_input = TextInput(value= '1', title="Input T0:")
T1_input = TextInput(value= '3', title="Input T1:")
Amp_input = TextInput(value= '1', title="Input Amplitude:")
sample_fun_input_f = Dropdown(label="Choose a sample function f(t)",
                              menu=sample_f_names,
                              width=200)
Calc_button = Button(label="Calculate Wavelet Transform", button_type="success",width=100)



def extract_parameters():
    """
    etxracts the necessary parameters from the input widgets
    :return: float T_0, float T_1, Amplitude amp
    """
    T_0 = float((T0_input.value.replace(',','.')))  # Interval
    T0_input.value = str(T_0)
    T_1 = float((T1_input.value.replace(',','.')))  # Interval
    T1_input.value = str(T_1)
    amp = float((Amp_input.value.replace(',','.')))  # Interval
    Amp_input.value = str(amp)

    global sample_function_id
    if (sample_function_id == "Heaviside Function"):
        return T_0 , amp
    
    elif (sample_function_id == "Rectangular Function"):
        return T_0, T_1 , amp
    
    elif (sample_function_id == "Dirac delta Function"):
        return T_0, amp

def Find_Heaviside_WT(T0,amp):
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
            W[i][j]=quad(integrand1, T0, np.inf)[0]
    WaveLet_source.data = {'a': [a],'b':[b],'W':[W]}
    plot_Wavelet.image(image="W", source=WaveLet_source, color_mapper=color_mapper, x=0, y=0, dw=5, dh=5)
    plot_Wavelet.add_layout(color_bar, 'right')

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

def update():
    """
    Compute data depending on input function.
    """
    # Clear function and Wavelet plots
    # reset()

    # Extract parameters
    global sample_function_id
    if (sample_function_id == "Heaviside Function"):
        T_0 , amp = extract_parameters()
        function_source.data= dict(x=[0, T_0, T_0, 5] ,y=[0, 0, amp, amp])
        plot_function.line(x='x',y='y',source=function_source ,color="blue",line_width=3)
        Find_Heaviside_WT(T_0, amp)
    
    elif (sample_function_id == "Rectangular Function"):
        T_0, T_1 , amp = extract_parameters()
        function_source.data= dict(x=[0, T_0, T_0, T_1, T_1, 5] ,y=[0, 0, amp, amp, 0, 0])
        plot_function.line(x='x',y='y',source=function_source ,color="blue",line_width=3)
        Find_Rectangular_WT(T_0, T_1 , amp)
    
    elif (sample_function_id == "Dirac delta Function"):
        T_0, amp = extract_parameters()
        function_source.data= dict(x=[0, T_0, T_0, T_0, 5] ,y=[0, 0, amp, 0, 0])
        plot_function.line(x='x',y='y',source=function_source ,color="blue",line_width=3)
        Find_Dirac_WT(T_0, amp)


def Calc():
    update()

def sample_fun_input_modified(self):
    """
    Called if the sample function is changed.
    :param self:
    :return:
    """

    # we set the bool true, because we use a sample function for which we know the analytical solution
    global sample_function_id
  
    # get the id
    sample_function_id = sample_fun_input_f.value
    if (sample_function_id == "Heaviside Function"):
        controls = [sample_fun_input_f, T0_input, Amp_input]
        controls_box = widgetbox(controls, sizing_mode='scale_width')
        My_Layout.children[0].children[0]= controls_box  # all controls
        
    elif (sample_function_id == "Rectangular Function"):
        controls = [sample_fun_input_f, T0_input, T1_input, Amp_input]
        controls_box = widgetbox(controls, sizing_mode='scale_width')  # all controls
        My_Layout.children[0].children[0]= controls_box  # all controls
    
    elif (sample_function_id == "Dirac delta Function"):
        controls = [sample_fun_input_f, T0_input, Amp_input]
        controls_box = widgetbox(controls, sizing_mode='scale_width')  # all controls
        My_Layout.children[0].children[0]= controls_box  # all controls

    
def reset():
    function_source.data = dict(t=[],y=[])
    WaveLet_source.data = {'a': [],'b':[],'W':[]}


# add callback behaviour
sample_fun_input_f.on_click(sample_fun_input_modified)
Calc_button.on_click(Calc)

# create layout
controls = [sample_fun_input_f]
controls_box = widgetbox(controls, sizing_mode='scale_width')  # all controls
My_Layout = layout([[controls_box, plot_function],[Calc_button,plot_Wavelet]],sizing_mode='stretch_both')
curdoc().add_root(My_Layout) # add plots and controls to root
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '