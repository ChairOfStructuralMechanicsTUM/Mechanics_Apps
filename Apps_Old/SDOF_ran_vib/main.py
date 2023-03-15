<<<<<<< HEAD:Apps_Old/SDOF_ran_vib/main.py
#---------------------------------------------------------------------------------- imports-------------------------------------------------------------------------------------------------------
#math
from matplotlib.pyplot import ylim
import numpy as np
from scipy.fft import rfftfreq #, export_svg
from scipy.stats import norm
import statistics
# bokeh
from bokeh.layouts import column, row
from bokeh.plotting import *
from bokeh.models import *
from bokeh.driving import linear
from bokeh.events import PointEvent, Tap
from bokeh.io import curdoc

from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv, LatexSlider, LatexLabel, LatexLabelSet, LatexLegend

#from bokeh.io import export_png


# importing functions from files
from calculations import *
from rfourier_test import to_frequency_domain, to_time_domain
from gaussian_process import *

#------------------------------------------------------------------------------------initial variables----------------------------------------------------------------------------------------------
#symbols legend
"t_list" #time interval
"f_list" #frequency interval
"w_0" # natural undamped angular frequency 
"f_0" # natural undamped  frequency in Hz
"w_d" # natural damped angular frequency 
"f_d" # natural damped frequency in Hz
"cov" # covariance function
"S"   # spectral density
"h_x" # impulse response function
"H_x" # harmonic transfer function
"u"   # critical value


#observation window
T = 8 # observation time
dt = 1/sample_rate
sample_rate = 128
N = T * sample_rate
f_list = rfftfreq(N , 1/sample_rate) 
t_list = np.linspace(-T/2, T/2, T * sample_rate, endpoint=False)  


#SDOF system parameters
system_params = Properties()  
system_params.stiffness = 10*pow(20 * np.pi, 2)  # stiffness
system_params.mass = 10  # mass
system_params.zeta = 0.05  # damping ratio
# initial conditions
u0 = 0
v0 = 0

#excitation
mean = 0
sigma = 2
standard_deviation = 0
b = np.pi/4
cov = np.ones(len(t_list)) * mean
realizations = []   
S = []

#response
response = np.zeros(10)


#predifined vlaue to enable the tabel 
omega_ex = 0
omega_res = 0
upcrossing_ex = 0
upcrossing_res = 0
peak_ex = 0
peak_res = 0
IF_ex = 0 #sigma_velocity**2/(sigma*sigma_acceleration)
IF_res = 0

#----------------------------------------------------------------------------------------bokeh widgets------------------------------------------------------------------------------------------------
#CheckboxButtonGroup
statistical_property_checkbox =  CheckboxButtonGroup(labels=["Process Categroy", "Theory"], active=[1], width = 1250)
covariance_checkbox = CheckboxButtonGroup(labels=["Narrowband Process", " Squared Exponential Cov", "Martérn Class", "White Noise"], active=[], width = 1250)
#Button
calculate_button_Gauss = Button(label="Calculate", button_type="primary", height=40)
Add_Gaussian_Button =Button(label="Add Realization", button_type="primary", height=30)
Remove_Gaussian_Button = Button(label = "Remove Realization", button_type = "primary", height = 30)
#Slider
damping_slider = Slider(title="damping ratio \u03B6 [-]", value=system_params.zeta, start=0.01, end=1, step=0.01)
stiffness_slider = Slider(title="stiffness k [N/m]", value=system_params.stiffness, start=1000, end=100000, step=1000)
mass_slider = Slider(title="mass m [kg]", value=system_params.mass, start=1, end=25, step=1)

sigma_slider = Slider(title="standard deviation \u03C3 [-]", value=sigma, start=0.0, end=5.0, step=0.5, max_width = 300)
mean_slider = Slider(title='mean value \u03BC [-]',value = mean ,start = -5, end = 5.0, step = 1) 
correlation_slider = Slider(title='correlation lenght/  length scale [-]',value = 0.1 ,start = 0.001, end = 1, step = 0.001, max_width = 300) #start != 0 because no devision by 0
bandwidth_slider = Slider(title="bandwidth [-]", value=0, start=0, end=np.pi*2, step=np.pi/8, max_width = 300)
ferquency_slider = Slider(title="frequency f [Hz]", value=5, start=1, end=10, step=1, max_width = 300)

failure_slider = Slider(title="critical level |u|[-]", value=3, start=1, end= 6, step=0.5, min_width = 600, max_width = 600)
#-----------------------------------------------------------------------------------------bokeh divs--------------------------------------------------------------------------------------------------
div_width = 300
title_div = Div(text="<b>SDOF under Random Vibration</b>", style={'font-size': '30px'}, width=div_width, height=15, sizing_mode="stretch_width", align="center", height_policy = "fit")
Exitation_div = Div(text="<b>Excitation</b>", style={'font-size': '20px'}, width=div_width, height=15, sizing_mode="stretch_width", align="center", height_policy = "fit")
para_div = Div(text="<b>Parameter Control</b>", style={'font-size': '20px'}, width=div_width, height=15, sizing_mode="stretch_width", align="center")
Response_div = Div(text="<b>Response</b>", style={'font-size': '20px'}, width=div_width, height=15, sizing_mode="stretch_width", align="center", height_policy = "fit")
Gaussian_div = Div(text="<b>Marginal Gaussian Distribution</b>", style={'font-size': '20px'}, width=div_width, height=15, sizing_mode="stretch_width", align="center", height_policy = "fit")
Control_para_div = Div(text="<b>Control Parameters</b>", style={'font-size': '20px'}, width=div_width, height=15, sizing_mode="stretch_width", align="center", height_policy = "fit")
Failure_div = Div(text="<b>Failure Analysis</b>", style={'font-size': '20px'}, width=div_width, height=15, sizing_mode="stretch_width", align="center", height_policy = "fit")
system_para_div = Div(text="<b>SDOF System</b>", style={'font-size': '15px'}, width=div_width, height=15, sizing_mode="stretch_width", align="center", height_policy = "fit")
SDOF_system_div = Div(text="<b>SDOF System</b>", style={'font-size': '20px'}, width=div_width, height=15, sizing_mode="stretch_width", align="center", height_policy = "fit")
excitation_para = Div(text="<b>Excitation</b>", style={'font-size': '15px'}, width=div_width, height=15, sizing_mode="stretch_width", align="center", height_policy = "fit")
realization_div = Div(text="<b>Realization</b>", style={'font-size': '15px'}, width=div_width, height=15, sizing_mode="stretch_width", align="center", height_policy = "fit")

frequency_title = Div(text=f"Natural frequency: {round(system_params.w, 2)}rad/s or {round(system_params.w / (2 * np.pi), 2)}Hz", style={'font-size': '12px'})

theory_div = LatexDiv(text=" This application is supposed to visualize the response of a single degree of freedom (SDOF) system subjected to random vibration. The excitation thereby is a Gaussian random process $\\{X(t)\\}$ and thus solely dependent on the mean vector $\\bm{\\mu}_{X}$ and covariance matrix $\\mathbf{K}_{X X}$:"
"$$p_{\\mathbf{X}}(\\mathbf{u})=\\frac{1}{2\\pi^{n / 2}\\left|\\mathbf{K}_{X X}\\right|^{1 / 2}} \\exp \\left(-\\frac{1}{2}\\left(\\mathbf{u}-\\bm{\\mu}_{X}\\right)^{T}\\mathbf{K}_{X X}^{-1}\\left(\\mathbf{u}-\\bm{\\mu}_{X}\\right)\\right)\\:.$$"
"The response of the SDOF system is calculated with the harmonic transfer function $H_x(f)$ in the frequency domain with the following formular:"
"$$X(f) = H_x(f)F(f)\\:,$$"
"where $F(f)$ and $X(f)$ denote the excitation and reponse spectrum, respectively."
"</p>"
"Furthermore, all processes are second-order stationary. This indicates that the mean and the covarinace are independent of a time shift along the abscissa. Thus, the mean value is constant for all values of $t$:"
"$$\mu_{X}(t)=\mu_{X}\\:.$$"
"The reason for considering stationary vibrations is that we suppose the system has oscillated since $t = -\infty$. Thus, we can assume a steady-state response. Furthermore, the choice of a Gaussian random process enables a feasible response calculation. As it is known that the response of a system subjected to a Gaussian vibration will also be Gaussian distributed."
"</p>"
"On top of the application, the user can choose between different categories of random processes. The chategories are defined by their covaraince and thus by the degree of correlations between the different random variables that define the Gaussian process. Possible choices and their respective stationary covariance functions are:"
"</p>"
"narrowband processes: $$G_{\\mathrm{XX,NB}}(\\tau) = \\sigma^2 \\cos{(f_c\\tau)} \\frac{\\sin{(b\\tau)}}{b\\tau}\\:,$$"
"processes with a squared exponential covariance: $$G_{\\mathrm{XX,SE}}(\\tau)= \\sigma^2 \\exp \\left(-\\frac{\\tau^{2}}{2 \ell^{2}}\\right)\\:,$$"
"processes with a Matérn class covariance :$$G_{\\mathrm{XX,MC}}(\\tau)= \\sigma^{2}\\frac{2^{1-\\nu}}{\Gamma(\\nu)}\left(\\frac{\\sqrt{2 \\nu} \\tau}{\ell}\\right)^{\\nu} K_{\\nu}\left(\\frac{\sqrt{2 \\nu} \\tau}{\\ell}\\right) \\:,$$ and "
"white noise processes: $$  G_{\\mathrm{XX,WN}}(\\tau) = 2\\pi S_0\\delta(\\tau)\\:.$$"
"After choosing a covariance the system and the excitation can be altered by the control parameters on the top of the page. Further, to demonstrate that the shown vibration is only one possible realization, the user can add and delete other realizations."
"</p>"
"At the bottom of the application, the marginal cumulative distribution function (CDF) and marginal probability density function (PDF) of each random variable of the process are shown. Moreover, the probability of survival and first passage time gives an estimation of the probability of failure depending on a chosen critical level $|u|$ that indicating malfunction."
"It is important to note that |u| in this case, defines the multiples of the standard deviation $\\sigma$.  This means that $ u*\\sigma$ is passed to the functions. Further, the probability of survival is implemented by:"
"$$L_{|X|}(u, t) = L_{|X|}(u, 0) \\exp \\left[-v_{|X|}^{+}(u) t\\right]\ \:,$$"
"where $ L_{|X|}(u, 0) $ is calculated of the CDF for the value $u$, and $ v_{|X|}^{+}(u) t $ describes the occurrence of crossing of level |u|." 
"The probability of failure time is given by"
"$$p_{T_{X}}(t) = v_{X}^{+}(u) \\exp \\left[-v_{|X|}^{+}(u) t\\right]\\:.$$"
"For both functions, the Poisson approximation was used.", style={'font-size': '12px'} , render_as_text=False, width=1200)

spacer = Div(text="", style={'font-size': '12px'} , width = 300)

# ----------------------------------------------------------------------------------------bokeh plots------------------------------------------------------------------------------------------------------
plot_width = 300
plot_height = plot_width * 2// 3
line_width = 1
text_font_size = "10pt"

# excitation realization in time domain
excitation_time = figure(title="Realization - Time Domain", x_axis_label="t [s]",
                         y_axis_label="f(t)",
                         plot_width=plot_width, plot_height=plot_height, x_range=[0, 4], output_backend="svg")
excitation_time.title.align = "center" #titel in the center
excitation_time.toolbar.logo = None 
excitation_time.outline_line_width = line_width
excitation_time.outline_line_color = "Black"
excitation_time.title.text_font_size =text_font_size
line_excitation_t = excitation_time.line([], [], line_color="royalblue", line_width=line_width)
ds_excitation_t = line_excitation_t.data_source
line_excitation_t_mean = excitation_time.line([], [], line_color="red",  line_width= line_width)
ds_excitation_t_mean =line_excitation_t_mean.data_source
ex_new1 = excitation_time.line([], [], line_color="sienna", line_width=line_width)
ex_new2 = excitation_time.line([], [], line_color="purple", line_width=line_width)
ex_new3 = excitation_time.line([], [], line_color="green", line_width=line_width)
ds_ex_new1 = ex_new1.data_source
ds_ex_new2 = ex_new2.data_source
ds_ex_new3 = ex_new3.data_source
varea_excitation_time = excitation_time.varea(x = [], y1 = [] , y2 = [] , alpha = 0.25, fill_color = "olivedrab", legend_label = "\u03C3")
ds_excitation_time_varea = varea_excitation_time.data_source
varea_excitation_3_time = excitation_time.varea(x = [], y1 = [] , y2 = [] , alpha = 0.25, fill_color = "darkorange", legend_label = "3\u03C3")
ds_excitation_time_3_varea = varea_excitation_3_time.data_source
excitation_time.legend.label_text_font_size = "7pt"

# excitation realization in frequency domain
excitation_freq = figure(title="Realization - Frequency Domain", x_axis_label="f [Hz]", y_axis_label=" |F(f)| [Power/Hz]",
                         plot_width=plot_width, plot_height=plot_height, x_range=[0, 25], output_backend="svg")
excitation_freq.title.align = "center"
excitation_freq.toolbar.logo = None
excitation_freq.outline_line_width = line_width
excitation_freq.outline_line_color = "Black"
excitation_freq.title.text_font_size =  text_font_size
line_excitation_f_real = excitation_freq.line([], [], line_color="royalblue", line_width=line_width)
ds_excitation_f_real = line_excitation_f_real.data_source
line_excitation_f_imag = excitation_freq.line([], [], line_color="red", line_width=line_width)
ds_excitation_f_imag = line_excitation_f_imag.data_source

#covaraince of the excitation
covariance_exc = figure(title="Covariance", x_axis_label="\u03C4 [s]",
                         y_axis_label="G_FF(\u03C4)",
                         plot_width=plot_width, plot_height=plot_height, x_range=[-4, 4], output_backend="svg")
covariance_exc.title.align = "center" #titel in the center
covariance_exc.toolbar.logo = None 
covariance_exc.outline_line_width = line_width
covariance_exc.outline_line_color = "Black"
covariance_exc.title.text_font_size = text_font_size
line_covariance_exc = covariance_exc.line([], [], line_color="royalblue", line_width=line_width)
ds_covariance_exc = line_covariance_exc.data_source

spectral_density_exc = figure(title="Spectral Density", x_axis_label="f [Hz]",y_axis_label = "|S_FF(f)|[Power/Hz]",
                         plot_width=plot_width, plot_height=plot_height, x_range=[0, 25] , output_backend="svg")
spectral_density_exc.title.align = "center" 
spectral_density_exc.toolbar.logo = None 
spectral_density_exc.outline_line_width = line_width
spectral_density_exc.add_layout(LatexLabel(x=0,y=0,text="|S_XX(f)|",text_color='black',text_font_size="9pt",level='overlay',text_baseline="middle"))
spectral_density_exc.outline_line_color = "Black"
spectral_density_exc.title.text_font_size = text_font_size
line_spectral_density_exc = spectral_density_exc.line([], [], line_color="royalblue", line_width=line_width)
ds_spectral_density_exc = line_spectral_density_exc.data_source

# unit-impulse response plot
transfer_time = figure(title="Impulse Response Function", y_axis_label="h_x(t)",  x_axis_label="t [s]",
                        plot_width=plot_width, plot_height=plot_height, x_range=[0, 2], output_backend="svg")
transfer_time.yaxis[0].formatter = PrintfTickFormatter(format = "%4.0e")
transfer_time.title.align = "center"
transfer_time.toolbar.logo = None
transfer_time.outline_line_width = line_width
transfer_time.outline_line_color = "Black"
transfer_time.title.text_font_size =  text_font_size
line_transfer_t = transfer_time.line([], [], line_color="royalblue", line_width=line_width)
ds_transfer_t = line_transfer_t.data_source

# frequency domain harmonic tranfer function 
transfer_freq_mag = figure(title="Harmonic Transfer Function",  x_axis_label="f [Hz]",
                         y_axis_label="|H_X(f)| [Power/Hz]",
                        plot_width=plot_width, plot_height=plot_height, x_range=[0, 25], output_backend="svg")
transfer_freq_mag.yaxis[0].formatter = PrintfTickFormatter(format = "%4.0e")
transfer_freq_mag.title.align = "center"
transfer_freq_mag.toolbar.logo = None
transfer_freq_mag.outline_line_width = line_width
transfer_freq_mag.outline_line_color = "Black"
transfer_freq_mag.title.text_font_size = text_font_size
line_transfer_f_mag = transfer_freq_mag.line([], [], line_color="royalblue", line_width=line_width)
ds_transfer_f_mag = line_transfer_f_mag.data_source

# response realization in time domain
min_value = 0
response_time = figure(title = "Realization - Time Domain", x_axis_label="t [s]",  x_range=[0, 4] , # f"Displacement {(min_value)}"
                          y_axis_label="x(t)",
                          plot_width=plot_width, plot_height=plot_height, output_backend="svg")
response_time.yaxis[0].formatter = PrintfTickFormatter(format = "%4.0e")
response_time.title.align = "center"
response_time.toolbar.logo = None
response_time.outline_line_width = line_width
response_time.outline_line_color = "Black"
response_time.title.text_font_size = text_font_size
line_response_time = response_time.line([], [], line_color="royalblue", line_width=line_width)
ds_response_time =line_response_time.data_source
line_response_t_mean = response_time.line([], [], line_color="red",  line_width= line_width)
ds_response_t_mean =line_response_t_mean.data_source
res_new = response_time.line([], [], line_color="sienna", line_width=line_width)
res_new2 = response_time.line([], [], line_color="purple", line_width=line_width)
res_new3 = response_time.line([], [], line_color="green", line_width=line_width)
res_new_1 = res_new.data_source
res_new_2 = res_new2.data_source
res_new_3 = res_new3.data_source
varea1_response = response_time.varea(x = [] , y1 = [] , y2 = [] , alpha = 0.25, fill_color = "olivedrab", legend_label = "\u03C3")
ds_response_varea1 = varea1_response.data_source
varea2_response = response_time.varea(x = [] , y1 = [] , y2 = [] , alpha = 0.25, fill_color = "darkorange", legend_label = "3\u03C3")
ds_response_varea2 = varea2_response.data_source
response_time.legend.label_text_font_size = "7pt"

# response realization in frequency domain
response_freq = figure(title="Realization - Frequency Domain", x_axis_label="f [Hz]", y_axis_label="|X(f)| [Power/Hz]",
                          plot_width=plot_width, plot_height=plot_height, x_range=[0, 25], output_backend="svg")
response_freq.yaxis[0].formatter = PrintfTickFormatter(format = "%4.0e")
response_freq.title.align = "center"
response_freq.toolbar.logo = None
response_freq.outline_line_width = line_width
response_freq.outline_line_color = "Black"
response_freq.title.text_font_size = text_font_size
line_response_freq = response_freq.line([], [], line_color="royalblue",  line_width=line_width)
ds_responsef_freq = line_response_freq.data_source

#covaraince of the response
covariance_res = figure(title="Covariance", x_axis_label="\u03C4 [s]",
                         y_axis_label="G_XX(\u03C4)",
                         plot_width=plot_width, plot_height=plot_height, x_range=[-4, 4], output_backend="svg")
covariance_res.yaxis[0].formatter = PrintfTickFormatter(format = "%4.0e")
covariance_res.title.align = "center" #titel in the center
covariance_res.toolbar.logo = None 
covariance_res.outline_line_width = line_width
covariance_res.outline_line_color = "Black"
covariance_res.title.text_font_size = text_font_size
line_covariance_res = covariance_res.line([], [], line_color="royalblue", line_width = line_width)
ds_covariance_res = line_covariance_res.data_source
line_covariance_res_proof = covariance_res.line([], [], line_color="green", line_width=line_width)
ds_covariance_res_proof = line_covariance_res_proof.data_source

#spectral density of the response
spectral_density_res = figure(title="Spectral Density", x_axis_label="f [Hz]",
                         y_axis_label="|S_XX(f)| [Power/Hz]",
                         plot_width=plot_width, plot_height=plot_height, x_range=[0, 25], output_backend="svg")
spectral_density_res.yaxis[0].formatter = PrintfTickFormatter(format = "%4.0e")
spectral_density_res.title.align = "center" #titel in the center
spectral_density_res.toolbar.logo = None 
spectral_density_res.outline_line_width = line_width
spectral_density_res.outline_line_color = "Black"
spectral_density_res.title.text_font_size = text_font_size
line_spectral_density_res = spectral_density_res.line([], [], line_color="royalblue", line_width=line_width)
ds_spectral_density_res = line_spectral_density_res.data_source

#probability density function of response 
pdf_gaussian = figure(title="Probability Density", x_axis_label="u",
                         y_axis_label="p_X(u)",
                         plot_width=plot_width, plot_height=plot_height, output_backend="svg")
pdf_gaussian.xaxis[0].formatter = PrintfTickFormatter(format = "%4.0e")
pdf_gaussian.xaxis.major_label_orientation = "vertical"
pdf_gaussian.align  = "center"
pdf_gaussian.title.align = "center" #titel in the center
pdf_gaussian.toolbar.logo = None 
pdf_gaussian.outline_line_width = line_width
pdf_gaussian.outline_line_color = "Black"
pdf_gaussian.title.text_font_size = text_font_size
line_gaussian_distribution = pdf_gaussian.line([], [], line_color="royalblue", line_width=line_width)
ds_pdf_gaussian = line_gaussian_distribution.data_source
vbar1_pdf_gaussian = pdf_gaussian.vbar(x = [], top =[], bottom = [], width=standard_deviation/20, line_color="olivedrab", alpha = 0.5,legend_label = "\u03C3" )
ds_pdf_gaussian_vbar1 = vbar1_pdf_gaussian.data_source
vbar2_pdf_gaussian = pdf_gaussian.vbar(x = [], top =[], bottom = [], width=standard_deviation/20, line_color="darkorange", alpha = 0.5, legend_label = "3\u03C3")
ds_pdf_gaussian_vbar2 = vbar2_pdf_gaussian.data_source
pdf_gaussian.legend.label_text_font_size = "7pt"

#cumulative distribution function of response 
cdf_gaussian = figure(title="Cumulative Distribution", x_axis_label= "u",
                         y_axis_label="\u03C6((u-\u03BC)/\u03C3)",
                         plot_width=plot_width, plot_height=plot_height, output_backend="svg")
cdf_gaussian.xaxis[0].formatter = PrintfTickFormatter(format = "%4.0e")
cdf_gaussian.xaxis.major_label_orientation = "vertical"
cdf_gaussian.title.align = "center" #titel in the center
cdf_gaussian.align  = "center"
cdf_gaussian.toolbar.logo = None 
cdf_gaussian.outline_line_width = line_width
cdf_gaussian.outline_line_color = "Black"
cdf_gaussian.title.text_font_size = text_font_size
line_cdf_gaussian = cdf_gaussian.line([], [], line_color="royalblue", line_width=line_width)
ds_cdf_gaussian = line_cdf_gaussian.data_source

#bivariate distibution of response 
# bivariate_gaussian = figure(title="Bivariate Distribution", x_axis_label= "X 1",
#                          y_axis_label="X 2",
#                          plot_width=plot_width, plot_height=plot_height, output_backend="svg")
# bivariate_gaussian.title.align = "center" #titel in the center
# bivariate_gaussian.align  = "center"
# bivariate_gaussian.toolbar.logo = None 
# bivariate_gaussian.outline_line_width = line_width
# bivariate_gaussian.title.text_font_size = text_font_size
# line_bivariate_gaussian = bivariate_gaussian.multi_line(xs = [], ys = [], line_color = [])
# ds_bivariate_gaussian = line_bivariate_gaussian.data_source

#probability of survival of response realization
prob_of_survival = figure(title="Probability of Survival", x_axis_label="t [s]",
                         y_axis_label=f"L_X(u = (u\u03C3),t)",
                         plot_width=plot_width, plot_height=plot_height, x_range=[0, 4], output_backend="svg")
prob_of_survival.title.align = "center" #titel in the center
prob_of_survival.align  = "center"
prob_of_survival.toolbar.logo = None 
prob_of_survival.outline_line_width = line_width
prob_of_survival.outline_line_color = "Black"
prob_of_survival.title.text_font_size = text_font_size
line_prob_of_survival = prob_of_survival.line([], [], line_color="royalblue", line_width=line_width)
ds_prob_of_survival = line_prob_of_survival.data_source

#first passage time of response realization
prob_of_time = figure(title="First Passage Time", x_axis_label="t [s]",
                         y_axis_label="p(T_X(t))",
                         plot_width=plot_width, plot_height=plot_height, x_range=[0, 4], output_backend="svg")
prob_of_time.title.align = "center" #titel in the center
prob_of_time.align  = "center"
prob_of_time.toolbar.logo = None 
prob_of_time.outline_line_width = line_width
prob_of_time.outline_line_color = "Black"
prob_of_time.title.text_font_size = text_font_size
line_prob_of_time = prob_of_time.line([], [], line_color="royalblue", line_width=line_width)
ds_prob_of_time = line_prob_of_time.data_source
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------call back functions---------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def update_statistic_checkbox(attrname, old, new): 
#Makes sure that only on item (covariance, spectral density or theory is selected and shows bokeh widgets accordingly)
    global active_statistical #varaible that remembers last checkbox item
    if statistical_property_checkbox.active == [1]: #theory
        covariance_checkbox.visible = False
        theory_div.visible = True
        covariance_checkbox.active = []
        update_checkbox(None, None, None)
    
    if (statistical_property_checkbox.active == [0,1]):
        #If used selects more than one checkbox item at ones, the fisr selected item is active
        statistical_property_checkbox.active = active_statistical
    
    if statistical_property_checkbox.active == [0]:
        covariance_checkbox.visible = True
        theory_div.visible = False
       
    active_statistical = statistical_property_checkbox.active

def update_covariance_checkbox(attrname, old, new):
    global active_cov
    if (covariance_checkbox.active == [0,1]) | (covariance_checkbox.active == [1,2]) | (covariance_checkbox.active == [2,3]) | (covariance_checkbox.active == [0,3]) | (covariance_checkbox.active == [1,3]) | (covariance_checkbox.active == [0,2]):
        covariance_checkbox.active = active_cov

    update_checkbox(None, None, None)
    active_cov = covariance_checkbox.active

def update_checkbox(attrname, old, new):
    global excitation, realizations

    ds_response_time.data["x"] = t_list
    ds_response_time.data["y"] = []
    ds_responsef_freq.data["x"] = t_list
    ds_responsef_freq.data["y"] = []
    
    ds_spectral_density_res.data["x"] = t_list
    ds_spectral_density_res.data["y"] = []

    ds_covariance_res.data["x"] = t_list
    ds_covariance_res.data["y"] = []


    ds_ex_new1.data["x"] = t_list
    ds_ex_new1.data["y"] = []
    ds_ex_new2.data["x"] = t_list
    ds_ex_new2.data["y"] = []
    ds_ex_new3.data["x"] = t_list
    ds_ex_new3.data["y"] = []

    res_new_1.data["x"] = t_list
    res_new_1.data["y"] = []
    res_new_2.data["x"] = t_list
    res_new_2.data["y"] = []
    res_new_3.data["x"] = t_list
    res_new_3.data["y"] = []

    realizations = []

    # changing GUI depending on checkbox values (Gaussian Process, Equalizer)
    if  statistical_property_checkbox.active == [1]: 
        statistical_property_checkbox.visible = True
        theory_div.visible = True
        sigma_slider.visible = False
        mean_slider.visible = False
        ferquency_slider.visible = False
        bandwidth_slider.visible = False
        correlation_slider.visible = False
        mass_slider. visible = False
        damping_slider.visible = False
        stiffness_slider.visible = False
        transfer_time.visible = False
        transfer_freq_mag.visible = False
        excitation_time.visible = False
        excitation_freq.visible = False
        response_time.visible = False
        response_freq.visible = False
        covariance_exc.visible = False
        spectral_density_exc.visible = False
        covariance_res.visible = False
        spectral_density_res.visible = False
        calculate_button_Gauss.visible = False
        frequency_title.visible = False
        Add_Gaussian_Button.visible = False
        Remove_Gaussian_Button.visible = False
        Exitation_div.visible = False
        Response_div.visible = False
        Gaussian_div.visible = False
        Failure_div.visible = False
        pdf_gaussian.visible = False
        cdf_gaussian.visible = False
        #bivariate_gaussian.visible = False
        Control_para_div.visible = False
        prob_of_survival.visible = False
        prob_of_time.visible = False
        failure_slider.visible = False
        SDOF_system_div.visible = False
        system_para_div.visible = False
        excitation_para.visible = False
        realization_div.visible = False
    else:
        mass_slider. visible = True
        damping_slider.visible = True
        stiffness_slider.visible = True
        transfer_time.visible = True
        transfer_freq_mag.visible = True
        excitation_time.visible = True
        excitation_freq.visible = True
        response_time.visible = True
        response_freq.visible = True
        covariance_exc.visible = True
        spectral_density_exc.visible = True
        covariance_res.visible = True
        spectral_density_res.visible = True
        calculate_button_Gauss.visible = True
        frequency_title.visible = True
        Add_Gaussian_Button.visible = True
        Remove_Gaussian_Button.visible = True
        Exitation_div.visible = True
        Response_div.visible = True
        Gaussian_div.visible = True
        Failure_div.visible = True
        theory_div.visible = False
        Failure_div.visible = True
        pdf_gaussian.visible = True
        cdf_gaussian.visible = True
        #bivariate_gaussian.visible = True
        Control_para_div.visible = True
        prob_of_survival.visible = True
        prob_of_time.visible = True
        failure_slider.visible = True
        SDOF_system_div.visible = True
        system_para_div.visible = True
        excitation_para.visible = True
        realization_div.visible = True
        
    update_cov_slider()

def update_cov_slider():
    if covariance_checkbox.active == [0]: 
        sigma_slider.visible = True
        mean_slider.visible = True
        correlation_slider.visible = False
        ferquency_slider.visible = True
        bandwidth_slider.visible = True
    elif (covariance_checkbox.active == [1]) | (covariance_checkbox.active == [2]):
        sigma_slider.visible = True
        mean_slider.visible = True
        correlation_slider.visible = True
        ferquency_slider.visible = False
        bandwidth_slider.visible = False
    elif covariance_checkbox.active == [3]:
        sigma_slider.visible = True #nur wenn sigam auch einen einfluss hat ??????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
        mean_slider.visible = True
        correlation_slider.visible = False
        ferquency_slider.visible = False
        bandwidth_slider.visible = False
    update_excitation_cov(None, None, None)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------SDOF system calculatoin--------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# update unit impulse-response plot values in the time domain and in the frequency domain

def update_impulse(attrname, old, new):

    # passing slider values
    system_params.stiffness = stiffness_slider.value
    system_params.mass = mass_slider.value
    system_params.zeta = damping_slider.value
    frequency_title.text = f"Natural frequency: {round(system_params.w, 2)}rad/s or {round(system_params.w / (2 * np.pi), 2)}Hz"

    h_x = unit_impulse_function(t_list, system_params)  # unit impulse response values

    H_x = to_frequency_domain(t_list, h_x)  # harmonic transfer


    # passing arrays to plot
    ds_transfer_t.data["x"] = t_list
    ds_transfer_t.data["y"] = h_x
    ds_transfer_f_mag.data["x"] = f_list
    ds_transfer_f_mag.data["y"] = np.abs(H_x)  # abs(H_x.real)
    # ds_transfer_f_phase.data["x"] = tH_x
    # ds_transfer_f_phase.data["y"] = np.arctan(H_x.imag/H_x.real)  # abs(H_x.imag)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------excitation calculation---------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# function for calculation of the Force at given moment over which the Duhamel's Integral integrates
def excitation_real(t_list):
    global S

    degree_of_covariance = correlation_slider.value
    sigma = sigma_slider.value
    mean = mean_slider.value
    b = bandwidth_slider.value
    freq = ferquency_slider.value

    if covariance_checkbox.active == [0]:
        cov = cos_cov(t_list, freq, b, sigma) 
        solution = gaussian_function(mean*np.ones(len(t_list)),cov)

    elif covariance_checkbox.active == [1]:
        cov = squared_exponential_cov(t_list, sigma, degree_of_covariance) 
        solution  = gaussian_function(mean*np.ones(len(t_list)),cov) 
        
    elif covariance_checkbox.active == [2]:
        cov = matérn_class(t_list,0.5, sigma)
        solution  = gaussian_function(mean*np.ones(len(t_list)),cov)

    elif covariance_checkbox.active == [3]:
        cov = dirac_delta_cov(2, t_list) 
        solution  = gaussian_function(mean*np.ones(len(t_list)),cov)

    else: 
        solution = np.zeros(len(t_list))
    
    return solution

# # # update excitation plots in the time and frequency domain
def update_excitation_cov(attrname, old, new):
    global excitation

    excitation = excitation_real(t_list)  # excitation (y_values) on the time interval 

    p_fft = to_frequency_domain(t_list, excitation)  # FFT
   
    mean = mean_slider.value
    sigma = sigma_slider.value
 
    # passing arrays to plots
    ds_excitation_t.data["x"] = t_list
    ds_excitation_t.data["y"] = excitation
    ds_excitation_f_real.data["x"] =f_list
    ds_excitation_f_real.data["y"] = np.abs(p_fft)

    x = t_list
    y1 = (mean - sigma) * np.ones(len(t_list))
    y2 = (mean + sigma) * np.ones(len(t_list))

    ds_excitation_time_varea.data["x"] = x
    ds_excitation_time_varea.data["y1"] = y1
    ds_excitation_time_varea.data["y2"] = y2

    y1 = (mean - 3*sigma) * np.ones(len(t_list))
    y2 = (mean + 3*sigma) * np.ones(len(t_list))

    ds_excitation_time_3_varea.data["x"] = x
    ds_excitation_time_3_varea.data["y1"] = y1
    ds_excitation_time_3_varea.data["y2"] = y2

    ds_excitation_t_mean.data["x"] = t_list
    ds_excitation_t_mean.data["y"] = mean * np.ones(len(t_list))


    if len(realizations) == 1:
        ds_ex_new1.data["x"] = t_list
        ds_ex_new1.data["y"] = excitation_real(t_list)

    if len(realizations) == 2:
        ds_ex_new1.data["x"] = t_list
        ds_ex_new1.data["y"] = excitation_real(t_list)
        ds_ex_new2.data["x"] = t_list
        ds_ex_new2.data["y"] = excitation_real(t_list)

    if len(realizations) == 3: 
        ds_ex_new1.data["x"] = t_list
        ds_ex_new1.data["y"] = excitation_real(t_list)
        ds_ex_new2.data["x"] = t_list
        ds_ex_new2.data["y"] = excitation_real(t_list)
        ds_ex_new3.data["x"] = t_list
        ds_ex_new3.data["y"] = excitation_real(t_list)
    
    covariance_distribution()  

def covariance_distribution():
    global cov, S
    correlation = correlation_slider.value
    sigma = sigma_slider.value
    b = bandwidth_slider.value
    freq = ferquency_slider.value
    
    if covariance_checkbox.active == [0]:
        cov = cos_cov(t_list, freq, b, sigma)[512]  

    elif covariance_checkbox.active == [1]:
        cov = squared_exponential_cov(t_list, sigma, correlation)[512]  

    elif covariance_checkbox.active == [2]:
        cov = matérn_class(t_list, correlation, sigma)[512]  
        
    elif covariance_checkbox.active == [3]:
        cov = dirac_delta_cov(2, t_list)[512]  
        
    ds_covariance_exc.data["x"] = t_list
    ds_covariance_exc.data["y"] = cov
    spec_dens(cov)

def spec_dens(cov):
    global S
    S = to_frequency_domain(t_list, cov)
                
    ds_spectral_density_exc.data["x"] = f_list
    ds_spectral_density_exc.data["y"] = np.abs(S)


def add_Gaussian():
    global realizations
    realizations.append(excitation_real(t_list))

    if len(realizations) == 1:
        ds_ex_new1.data["x"] = t_list
        ds_ex_new1.data["y"] = realizations[0]

    if len(realizations) == 2:
        ds_ex_new2.data["x"] = t_list
        ds_ex_new2.data["y"] = realizations[1]

    if len(realizations) == 3:

        ds_ex_new3.data["x"] = t_list
        ds_ex_new3.data["y"] = realizations[2]
    else:
    #only three additional realizations can be added
        realizations = realizations[:3]

def delete_Gaussian():

    if len(realizations) == 1:
        ds_ex_new1.data["x"] = t_list
        ds_ex_new1.data["y"] = []
        realizations.pop()

    if len(realizations) == 2:
        ds_ex_new2.data["x"] = t_list
        ds_ex_new2.data["y"] = []
        realizations.pop()

    if len(realizations) == 3:
        ds_ex_new3.data["x"] = t_list
        ds_ex_new3.data["y"] = []
        realizations.pop()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------response calculation----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def calculate():

    res_new_1.data["x"] = t_list
    res_new_1.data["y"] = []
    res_new_2.data["x"] = t_list
    res_new_2.data["y"] = []
    res_new_3.data["x"] = t_list
    res_new_3.data["y"] = []

    response_cov()

def response_cov():
    global response_f, excitation
    system_params.stiffness = stiffness_slider.value
    system_params.mass = mass_slider.value
    system_params.zeta = damping_slider.value

    H_x = harmonic_transfer_function(f_list, system_params)

    p_fft = to_frequency_domain(t_list, excitation) #excitation in frequency domain
    u_fft =H_x * p_fft
        
    response_f = to_time_domain(f_list, u_fft) #displacement through frequency domain

    ds_response_time.data["x"] = t_list
    ds_response_time.data["y"] = response_f.real
    ds_responsef_freq.data["x"] = f_list
    ds_responsef_freq.data["y"] = np.abs(u_fft)


    if len(realizations) == 1:
            p_fft = to_frequency_domain(t_list, realizations[0]) #realizations in frequency domain
            u_fft =H_x * p_fft
            response_f = to_time_domain(f_list, u_fft)
            res_new_1.data["x"] = t_list
            res_new_1.data["y"] = response_f.real
            ds_response_time.data["x"] = t_list
            ds_response_time.data["y"] = response_f.real

    if len(realizations) == 2:
            p_fft = to_frequency_domain(t_list, realizations[0]) #realizations in frequency domain
            H_x * p_fft
            response_f = to_time_domain(f_list, u_fft)
            p_fft_2 = to_frequency_domain(t_list, realizations[1]) #realizations in frequency domain
            u_fft_2 =H_x* p_fft_2
            response_f_2 = to_time_domain(f_list, u_fft_2)
            res_new_1.data["x"] = t_list
            res_new_1.data["y"] = response_f.real
            res_new_2.data["x"] = t_list
            res_new_2.data["y"] = response_f_2.real
            ds_response_time.data["x"] = t_list
            ds_response_time.data["y"] = response_f.real      

    if len(realizations) == 3: 
            p_fft = to_frequency_domain(t_list, realizations[0]) #realizations in frequency domain
            H_x * p_fft
            response_f = to_time_domain(f_list, u_fft)
            p_fft_2 = to_frequency_domain(t_list, realizations[1]) #realizations in frequency domain
            u_fft_2 = H_x* p_fft_2
            response_f_2 = to_time_domain(f_list, u_fft_2)
            p_fft_3 = to_frequency_domain(t_list, realizations[2]) #realizations in frequency domain
            u_fft_3 = H_x* p_fft_3
            response_f_3 = to_time_domain(f_list, u_fft_3)
            res_new_1.data["x"] = t_list
            res_new_1.data["y"] = response_f.real
            res_new_2.data["x"] = t_list
            res_new_2.data["y"] = response_f_2.real
            res_new_3.data["x"] = t_list
            res_new_3.data["y"] = response_f_3.real
            ds_response_time.data["x"] = t_list
            ds_response_time.data["y"] = response_f.real

    calculate_stochastic()


def calculate_stochastic():
    global standard_deviation    
    mean = statistics.mean(response_f)

    ds_response_t_mean.data["x"] = t_list
    ds_response_t_mean.data["y"] = np.ones(len(t_list)) *mean
        
    H_x = harmonic_transfer_function(f_list, system_params)

    S_deform = np.multiply(np.abs(H_x)**2, S) 
    
    ds_spectral_density_res.data["x"] = f_list
    ds_spectral_density_res.data["y"] = np.abs(S_deform)
    
    cov_de =to_time_domain(f_list, S_deform)
    ds_covariance_res.data["x"] = t_list
    ds_covariance_res.data["y"] = cov_de.real

    variance = cov_de.real[512]
    standard_deviation = np.sqrt(variance)
    # standard_deviation = np.std(response)
        
    three_sigma = standard_deviation *3

    
    #plotting the shaded one- and three-sigma area
    x = t_list
    y1 = (mean- standard_deviation) * np.ones(len(t_list))
    y2 = (mean +standard_deviation) * np.ones(len(t_list))

    ds_response_varea1.data["x"] = x
    ds_response_varea1.data["y1"] = y1
    ds_response_varea1.data["y2"] = y2
    
    x = t_list
    y1 = (mean - three_sigma) * np.ones(len(t_list))
    y2 = (mean + three_sigma) * np.ones(len(t_list))

    ds_response_varea2.data["x"] = x
    ds_response_varea2.data["y1"] = y1
    ds_response_varea2.data["y2"] = y2


    Gaussian_distribution()
    failure(None, None, None)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------Gaussian distribution------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def Gaussian_distribution():
    mean = statistics.mean(response_f)

    u = np.linspace(-standard_deviation*5 + mean, standard_deviation * 5 + mean, 100)
    gauss_pdf = Gaussian_distribution_pdf(u, mean, standard_deviation)
    gauss_cdf = Gaussian_distribution_cdf(u, mean, standard_deviation)

    x = np.linspace(-standard_deviation + mean, standard_deviation + mean, 20)
    y = gauss_pdf[40:60]
    y_bottom = np.zeros(len(y))

    x_1 = np.linspace(-3*standard_deviation + mean,3*standard_deviation + mean, 60)
    y_1 = gauss_pdf[20:80]
    y1_bottom = np.zeros(len(y_1))

    ds_pdf_gaussian_vbar1.data["x"]= x
    ds_pdf_gaussian_vbar1.data["top"]= y
    ds_pdf_gaussian_vbar1.data["bottom"]= y_bottom

    ds_pdf_gaussian_vbar2.data["x"]= x_1
    ds_pdf_gaussian_vbar2.data["top"]= y_1
    ds_pdf_gaussian_vbar2.data["bottom"]= y1_bottom

    ds_pdf_gaussian.data["x"] = u
    ds_pdf_gaussian.data["y"] = gauss_pdf

    ds_cdf_gaussian.data["x"] = u
    ds_cdf_gaussian.data["y"] = gauss_cdf


    # mean_bivariate = np.array([mean, mean])
    # sigma_bivariate = np.array([[sigma, 0.95], [ 0.95, sigma]])
    # xs, ys, col, xt, yt, text = plot_Gaussian_contours(mean_bivariate,sigma_bivariate)
    
    # ds_bivariate_gaussian.data["xs"] = xs
    # ds_bivariate_gaussian.data["ys"] = ys
    # ds_bivariate_gaussian.data["col"] = col
    # ds_bivariate_gaussian.data["xt"] = xt
    # ds_bivariate_gaussian.data["yt"] = yt
    # ds_bivariate_gaussian.data["text"] = text

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------failure calculation-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def failure(attr, old, new):
    mean = statistics.mean(response_f)
    velocity = np.gradient(response_f, dt)
    sigma_velocity= np.std(velocity)
    u = failure_slider.value * standard_deviation
    v = 2 * rate_of_upcrossing(u, standard_deviation, sigma_velocity, 0)
    d = norm(loc=mean, scale=standard_deviation)
    L = d.cdf(np.abs(u)) #+ d.cdf(np.abs(-u)) 
    prob_surv = prob_of_surv(v, L, t_list)

    ds_prob_of_survival.data["x"] = t_list[512 :]
    ds_prob_of_survival.data["y"] = prob_surv[512:]

    prob_time = prob_of_failure_time(v, t_list)
    #prob_of_survival.y_axis_label=f"Probability L_X(({failure_slider.value}\u03C3),t)"
    ds_prob_of_time.data["x"] = t_list[512 :]
    ds_prob_of_time.data["y"] = prob_time[512 :]

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------widgets callback-------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

statistical_property_checkbox.on_change("active", update_statistic_checkbox)
covariance_checkbox.on_change("active", update_covariance_checkbox)

damping_slider.on_change("value_throttled", update_impulse)
stiffness_slider.on_change("value_throttled", update_impulse) 
mass_slider.on_change("value_throttled", update_impulse)

sigma_slider.on_change("value_throttled", update_excitation_cov)
mean_slider.on_change("value_throttled", update_excitation_cov) #it will calculate a new Gaussian process, is this desirebale
correlation_slider.on_change("value_throttled", update_excitation_cov)
ferquency_slider.on_change("value_throttled", update_excitation_cov)
bandwidth_slider.on_change("value_throttled", update_excitation_cov)

Add_Gaussian_Button.on_click(add_Gaussian)
Remove_Gaussian_Button.on_click(delete_Gaussian)

calculate_button_Gauss.on_click(calculate)

failure_slider.on_change("value_throttled", failure)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------pre run-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#WEBSITE_START

#calling callbacks at start of website so no values are undefined
#update_excitation_cov(None, None, None)
update_impulse(None, None, None)
update_statistic_checkbox(None, None, None)
covariance_distribution()
spec_dens(cov)


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------bokeh layout-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# putting widgets into GUI
#inputs = column(para_div, damping_slider, stiffness_slider, mass_slider, frequency_title, explain_text, covariance_checkbox, transfer_time, transfer_freq, sigma_slider, mean_slider, calculation_title)
input_1 = row(damping_slider, stiffness_slider, mass_slider, frequency_title)
input_2 = row(spacer,transfer_time, transfer_freq_mag, spacer)
input_3 = row(sigma_slider, mean_slider, correlation_slider, ferquency_slider, bandwidth_slider)
input_4 = row(spacer, Add_Gaussian_Button, Remove_Gaussian_Button, spacer)


# putting plots into GUI

explain = theory_div
plot = column(Exitation_div, row(covariance_exc, spectral_density_exc, excitation_time, excitation_freq),
                    calculate_button_Gauss, Response_div,
               row(covariance_res, spectral_density_res, response_time, response_freq), Gaussian_div,
               row(spacer, pdf_gaussian, cdf_gaussian, spacer), Failure_div, row(spacer,failure_slider), row(spacer,prob_of_survival, prob_of_time, spacer)) #, data_table)

final = column(title_div, statistical_property_checkbox, covariance_checkbox,explain, Control_para_div, system_para_div, input_1, excitation_para, input_3, realization_div, input_4, SDOF_system_div ,input_2,  plot)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# add curdoc => start serverpa
curdoc().add_root(row(final, width=plot_width * 10))
curdoc().title = "SDOF under Random Vibration"
# export_svg(row(inputs, plots, width=plot_width * 3), filename="app")
# to terminal: bokeh serve --show main_.py
=======
#---------------------------------------------------------------------------------- imports-------------------------------------------------------------------------------------------------------
#math
from matplotlib.pyplot import ylim
import numpy as np
from scipy.fft import rfftfreq #, export_svg
from scipy.stats import norm
import statistics
# bokeh
from bokeh.layouts import column, row
from bokeh.plotting import *
from bokeh.models import *
from bokeh.driving import linear
from bokeh.events import PointEvent, Tap
from bokeh.io import curdoc

from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv, LatexSlider, LatexLabel, LatexLabelSet, LatexLegend

#from bokeh.io import export_png


# importing functions from files
from calculations import *
from rfourier_test import to_frequency_domain, to_time_domain
from gaussian_process import *

#------------------------------------------------------------------------------------initial variables----------------------------------------------------------------------------------------------
#symbols legend
"t_list" #time interval
"f_list" #frequency interval
"w_0" # natural undamped angular frequency 
"f_0" # natural undamped  frequency in Hz
"w_d" # natural damped angular frequency 
"f_d" # natural damped frequency in Hz
"cov" # covariance function
"S"   # spectral density
"h_x" # impulse response function
"H_x" # harmonic transfer function
"u"   # critical value


#observation window
T = 8 # observation time
sample_rate = 128
dt = 1/sample_rate
N = T * sample_rate
f_list = rfftfreq(N , 1/sample_rate) 
t_list = np.linspace(-T/2, T/2, T * sample_rate, endpoint=False)  

#SDOF system parameters
system_params = Properties()  
system_params.stiffness = 10*pow(20 * np.pi, 2)  # stiffness
system_params.mass = 10  # mass
system_params.zeta = 0.05  # damping ratio
# initial conditions
u0 = 0
v0 = 0

#excitation
mean = 0
sigma = 1
standard_deviation = 0
b = np.pi/4
cov = np.ones(len(t_list)) * mean
realizations = []   
S = []

#response
response = np.zeros(10)


#predifined vlaue to enable the tabel 
omega_ex = 0
omega_res = 0
upcrossing_ex = 0
upcrossing_res = 0
peak_ex = 0
peak_res = 0
IF_ex = 0 #sigma_velocity**2/(sigma*sigma_acceleration)
IF_res = 0

#----------------------------------------------------------------------------------------bokeh widgets------------------------------------------------------------------------------------------------
#CheckboxButtonGroup
# statistical_property_checkbox =  CheckboxButtonGroup(labels=["Application", "Theory"], active=[0], width = 1250)
covariance_checkbox = CheckboxButtonGroup(labels=["Narrowband Process", " Squared Exponential Cov", "Martérn Class", "White Noise"], active=[], width = 1250)
#Button
calculate_button_Gauss = Button(label="Calculate", button_type="primary", height=40)
Add_Gaussian_Button =Button(label="Add Realization", button_type="primary", height=30)
Remove_Gaussian_Button = Button(label = "Remove Realization", button_type = "primary", height = 30)
#Slider
damping_slider = Slider(title="damping ratio \u03B6 [-]", value=system_params.zeta, start=0.01, end=1, step=0.01)
stiffness_slider = Slider(title="stiffness k [N/m]", value=system_params.stiffness, start=1000, end=100000, step=1000)
mass_slider = Slider(title="mass m [kg]", value=system_params.mass, start=1, end=25, step=1)

sigma_slider = Slider(title="standard deviation \u03C3 [-]", value=sigma, start=0.0, end=5.0, step=0.5, max_width = 300)
mean_slider = Slider(title='mean value \u03BC [-]',value = mean ,start = -5, end = 5.0, step = 1) 
correlation_slider = Slider(title='correlation lenght/  length scale [-]',value = 0.1 ,start = 0.001, end = 1, step = 0.001, max_width = 300) #start != 0 because no devision by 0
bandwidth_slider = Slider(title="bandwidth [-]", value=0, start=0, end=np.pi*2, step=np.pi/8, max_width = 300)
ferquency_slider = Slider(title="frequency f [Hz]", value=5, start=1, end=10, step=1, max_width = 300)

#failure_slider = Slider(title="critical level |u|[-]", value=3, start=1, end= 6, step=0.5, min_width = 600, max_width = 600)

#-----------------------------------------------------------------------------------------bokeh divs--------------------------------------------------------------------------------------------------
div_width = 300
title_div = Div(text="<b>SDOF under Random Vibration</b>", style={'font-size': '30px'}, width=div_width, height=15, sizing_mode="stretch_width", align="center", height_policy = "fit")
Exitation_div = Div(text="<b>Excitation</b>", style={'font-size': '20px'}, width=div_width, height=15, sizing_mode="stretch_width", align="center", height_policy = "fit")
para_div = Div(text="<b>Parameter Control</b>", style={'font-size': '20px'}, width=div_width, height=15, sizing_mode="stretch_width", align="center")
Response_div = Div(text="<b>Response</b>", style={'font-size': '20px'}, width=div_width, height=15, sizing_mode="stretch_width", align="center", height_policy = "fit")
#Gaussian_div = Div(text="<b>Marginal Gaussian Distribution</b>", style={'font-size': '20px'}, width=div_width, height=15, sizing_mode="stretch_width", align="center", height_policy = "fit")
Control_para_div = Div(text="<b>Control Parameters</b>", style={'font-size': '20px'}, width=div_width, height=15, sizing_mode="stretch_width", align="center", height_policy = "fit")
#Failure_div = Div(text="<b>Failure Analysis</b>", style={'font-size': '20px'}, width=div_width, height=15, sizing_mode="stretch_width", align="center", height_policy = "fit")
system_para_div = Div(text="<b>SDOF System</b>", style={'font-size': '15px'}, width=div_width, height=15, sizing_mode="stretch_width", align="center", height_policy = "fit")
SDOF_system_div = Div(text="<b>System response functions</b>", style={'font-size': '20px'}, width=div_width, height=15, sizing_mode="stretch_width", align="center", height_policy = "fit")
excitation_para = Div(text="<b>Excitation</b>", style={'font-size': '15px'}, width=div_width, height=15, sizing_mode="stretch_width", align="center", height_policy = "fit")
realization_div = Div(text="<b>Add and remove realizations</b>", style={'font-size': '20px'}, width=div_width, height=15, sizing_mode="stretch_width", align="center", height_policy = "fit")

frequency_title = Div(text=f"Natural frequency: {round(system_params.w, 2)}rad/s or {round(system_params.w / (2 * np.pi), 2)}Hz", style={'font-size': '12px'})

theory_div = LatexDiv(text=" This application visualizesthe response $\\{X(t)\\}$ of a single degree of freedom (SDOF) system subjected to random vibration. "
"The excitation is modelled through a stationary Gaussian random process $\\{F(t)\\}$ with constant mean $\\mu_{F}$ and autocovrariance function $G_{FF} (\\tau)$."
"The response of the SDOF system can be calculated in the frequency domain using the harmonic transfer function $H (f)$ with the following formula:"
"$$X(f) = H_x(f)F(f)\\:,$$"
"where $F(f)$ and $X(f)$ denote the excitation and reponse spectrum, respectively."
"Under the assumption of Gaussian excitation the response of the SDOF system will also be Gaussian. "
"</p>"
"The user can choose between different autocorrelation functions of the random excitation. Depending on the chosen autocorrelation function, the user can choose a number of hyperparameters in the correlation model. "
"</p>"
"The available models are:"
"<ul>"
"<li>narrowband processes: $$G_{\\mathrm{FF,NB}}(\\tau) = \\sigma^2 \\cos{(f_c\\tau)} \\frac{\\sin{(b\\tau)}}{b\\tau}\\:,$$</li>"
"<li> squared exponential covariance: $$G_{\\mathrm{FF,SE}}(\\tau)= \\sigma^2 \\exp \\left(-\\frac{\\tau^{2}}{2 \ell^{2}}\\right)\\:,$$</li>"
"<li> Matérn class covariance :$$G_{\\mathrm{FF,MC}}(\\tau)= \\sigma^{2}\\frac{2^{1-\\nu}}{\Gamma(\\nu)}\left(\\frac{\\sqrt{2 \\nu} \\tau}{\ell}\\right)^{\\nu} K_{\\nu}\left(\\frac{\sqrt{2 \\nu} \\tau}{\\ell}\\right) \\:,$$ </li>"
"<li> white noise processes: $$  G_{\\mathrm{FF,WN}}(\\tau) = 2\\pi S_0\\delta(\\tau)\\:.$$</li>"
"</ul>"
"In addition to the first and second order moments, we plot a number of realizations of the excitation and response processes.",
# "</p>"
# "At the bottom of the application, the marginal cumulative distribution function (CDF) and marginal probability density function (PDF) of each random variable of the process are shown. Moreover, the probability of survival and first passage time gives an estimation of the probability of failure depending on a chosen critical level $|u|$ that indicating malfunction."
# "It is important to note that |u| in this case, defines the multiples of the standard deviation $\\sigma$.  This means that $ u*\\sigma$ is passed to the functions. Further, the probability of survival is implemented by:"
# "$$L_{|X|}(u, t) = L_{|X|}(u, 0) \\exp \\left[-v_{|X|}^{+}(u) t\\right]\ \:,$$"
# "where $ L_{|X|}(u, 0) $ is calculated of the CDF for the value $u$, and $ v_{|X|}^{+}(u) t $ describes the occurrence of crossing of level |u|." 
# "The probability of failure time is given by"
# "$$p_{T_{X}}(t) = v_{X}^{+}(u) \\exp \\left[-v_{|X|}^{+}(u) t\\right]\\:.$$"
# "For both functions, the Poisson approximation was used.", 
style={'font-size': '12px'} , render_as_text=False, width=1200)

spacer = Div(text="", style={'font-size': '12px'} , width = 300)

# ----------------------------------------------------------------------------------------bokeh plots------------------------------------------------------------------------------------------------------
plot_width = 300
plot_height = plot_width * 2// 3
line_width = 1
text_font_size = "10pt"

# excitation realization in time domain
excitation_time = figure(title="Realization - Time Domain", x_axis_label="t [s]",
                         y_axis_label="f(t)",
                         plot_width=plot_width, plot_height=plot_height, x_range=[0, 4], output_backend="svg")
excitation_time.title.align = "center" #titel in the center
excitation_time.toolbar.logo = None 
excitation_time.outline_line_width = line_width
excitation_time.outline_line_color = "Black"
excitation_time.title.text_font_size =text_font_size
varea_excitation_time = excitation_time.varea(x = [], y1 = [] , y2 = [] , alpha = 0.25, fill_color = "olivedrab", legend_label = "\u03C3")
ds_excitation_time_varea = varea_excitation_time.data_source
varea_excitation_3_time = excitation_time.varea(x = [], y1 = [] , y2 = [] , alpha = 0.25, fill_color = "darkorange", legend_label = "3\u03C3")
ds_excitation_time_3_varea = varea_excitation_3_time.data_source
line_excitation_t = excitation_time.line([], [], line_color="royalblue", line_width=line_width)
ds_excitation_t = line_excitation_t.data_source
line_excitation_t_mean = excitation_time.line([], [], line_color="red",  line_width= line_width)
ds_excitation_t_mean =line_excitation_t_mean.data_source
ex_new1 = excitation_time.line([], [], line_color="sienna", line_width=line_width)
ex_new2 = excitation_time.line([], [], line_color="purple", line_width=line_width)
ex_new3 = excitation_time.line([], [], line_color="green", line_width=line_width)
ds_ex_new1 = ex_new1.data_source
ds_ex_new2 = ex_new2.data_source
ds_ex_new3 = ex_new3.data_source
excitation_time.legend.label_text_font_size = "7pt"

# excitation realization in frequency domain
excitation_freq = figure(title="Realization - Frequency Domain", x_axis_label="f [Hz]", y_axis_label=" |F(f)| [Power/Hz]",
                         plot_width=plot_width, plot_height=plot_height, x_range=[0, 25], output_backend="svg")
excitation_freq.title.align = "center"
excitation_freq.toolbar.logo = None
excitation_freq.outline_line_width = line_width
excitation_freq.outline_line_color = "Black"
excitation_freq.title.text_font_size =  text_font_size
line_excitation_f_real = excitation_freq.line([], [], line_color="royalblue", line_width=line_width)
ds_excitation_f_real = line_excitation_f_real.data_source
line_excitation_f_imag = excitation_freq.line([], [], line_color="red", line_width=line_width)
ds_excitation_f_imag = line_excitation_f_imag.data_source

#covaraince of the excitation
covariance_exc = figure(title="Covariance", x_axis_label="\u03C4 [s]",
                         y_axis_label="G_FF(\u03C4)",
                         plot_width=plot_width, plot_height=plot_height, x_range=[-4, 4], output_backend="svg")
covariance_exc.title.align = "center" #titel in the center
covariance_exc.toolbar.logo = None 
covariance_exc.outline_line_width = line_width
covariance_exc.outline_line_color = "Black"
covariance_exc.title.text_font_size = text_font_size
line_covariance_exc = covariance_exc.line([], [], line_color="royalblue", line_width=line_width)
ds_covariance_exc = line_covariance_exc.data_source

spectral_density_exc = figure(title="Spectral Density", x_axis_label="f [Hz]",y_axis_label = "|S_FF(f)|[Power/Hz]",
                         plot_width=plot_width, plot_height=plot_height, x_range=[0, 25] , output_backend="svg")
spectral_density_exc.title.align = "center" 
spectral_density_exc.toolbar.logo = None 
spectral_density_exc.outline_line_width = line_width
spectral_density_exc.add_layout(LatexLabel(x=0,y=0,text="|S_XX(f)|",text_color='black',text_font_size="9pt",level='overlay',text_baseline="middle"))
spectral_density_exc.outline_line_color = "Black"
spectral_density_exc.title.text_font_size = text_font_size
line_spectral_density_exc = spectral_density_exc.line([], [], line_color="royalblue", line_width=line_width)
ds_spectral_density_exc = line_spectral_density_exc.data_source

# unit-impulse response plot
transfer_time = figure(title="Impulse Response Function", y_axis_label="h_x(t)",  x_axis_label="t [s]",
                        plot_width=plot_width, plot_height=plot_height, x_range=[0, 2], output_backend="svg")
transfer_time.yaxis[0].formatter = PrintfTickFormatter(format = "%4.0e")
transfer_time.title.align = "center"
transfer_time.toolbar.logo = None
transfer_time.outline_line_width = line_width
transfer_time.outline_line_color = "Black"
transfer_time.title.text_font_size =  text_font_size
line_transfer_t = transfer_time.line([], [], line_color="royalblue", line_width=line_width)
ds_transfer_t = line_transfer_t.data_source

# frequency domain harmonic tranfer function 
transfer_freq_mag = figure(title="Harmonic Transfer Function",  x_axis_label="f [Hz]",
                         y_axis_label="|H_X(f)| [Power/Hz]",
                        plot_width=plot_width, plot_height=plot_height, x_range=[0, 25], output_backend="svg")
transfer_freq_mag.yaxis[0].formatter = PrintfTickFormatter(format = "%4.0e")
transfer_freq_mag.title.align = "center"
transfer_freq_mag.toolbar.logo = None
transfer_freq_mag.outline_line_width = line_width
transfer_freq_mag.outline_line_color = "Black"
transfer_freq_mag.title.text_font_size = text_font_size
line_transfer_f_mag = transfer_freq_mag.line([], [], line_color="royalblue", line_width=line_width)
ds_transfer_f_mag = line_transfer_f_mag.data_source

# response realization in time domain
min_value = 0
response_time = figure(title = "Realization - Time Domain", x_axis_label="t [s]",  x_range=[0, 4] , # f"Displacement {(min_value)}"
                          y_axis_label="x(t)",
                          plot_width=plot_width, plot_height=plot_height, output_backend="svg")
response_time.yaxis[0].formatter = PrintfTickFormatter(format = "%4.0e")
response_time.title.align = "center"
response_time.toolbar.logo = None
response_time.outline_line_width = line_width
response_time.outline_line_color = "Black"
response_time.title.text_font_size = text_font_size
varea1_response = response_time.varea(x = [] , y1 = [] , y2 = [] , alpha = 0.25, fill_color = "olivedrab", legend_label = "\u03C3")
ds_response_varea1 = varea1_response.data_source
varea2_response = response_time.varea(x = [] , y1 = [] , y2 = [] , alpha = 0.25, fill_color = "darkorange", legend_label = "3\u03C3")
ds_response_varea2 = varea2_response.data_source
line_response_time = response_time.line([], [], line_color="royalblue", line_width=line_width)
ds_response_time =line_response_time.data_source
line_response_t_mean = response_time.line([], [], line_color="red",  line_width= line_width)
ds_response_t_mean =line_response_t_mean.data_source
res_new = response_time.line([], [], line_color="sienna", line_width=line_width)
res_new2 = response_time.line([], [], line_color="purple", line_width=line_width)
res_new3 = response_time.line([], [], line_color="green", line_width=line_width)
res_new_1 = res_new.data_source
res_new_2 = res_new2.data_source
res_new_3 = res_new3.data_source
response_time.legend.label_text_font_size = "7pt"

# response realization in frequency domain
response_freq = figure(title="Realization - Frequency Domain", x_axis_label="f [Hz]", y_axis_label="|X(f)| [Power/Hz]",
                          plot_width=plot_width, plot_height=plot_height, x_range=[0, 25], output_backend="svg")
response_freq.yaxis[0].formatter = PrintfTickFormatter(format = "%4.0e")
response_freq.title.align = "center"
response_freq.toolbar.logo = None
response_freq.outline_line_width = line_width
response_freq.outline_line_color = "Black"
response_freq.title.text_font_size = text_font_size
line_response_freq = response_freq.line([], [], line_color="royalblue",  line_width=line_width)
ds_responsef_freq = line_response_freq.data_source

#covaraince of the response
covariance_res = figure(title="Covariance", x_axis_label="\u03C4 [s]",
                         y_axis_label="G_XX(\u03C4)",
                         plot_width=plot_width, plot_height=plot_height, x_range=[-4, 4], output_backend="svg")
covariance_res.yaxis[0].formatter = PrintfTickFormatter(format = "%4.0e")
covariance_res.title.align = "center" #titel in the center
covariance_res.toolbar.logo = None 
covariance_res.outline_line_width = line_width
covariance_res.outline_line_color = "Black"
covariance_res.title.text_font_size = text_font_size
line_covariance_res = covariance_res.line([], [], line_color="royalblue", line_width = line_width)
ds_covariance_res = line_covariance_res.data_source
line_covariance_res_proof = covariance_res.line([], [], line_color="green", line_width=line_width)
ds_covariance_res_proof = line_covariance_res_proof.data_source

#spectral density of the response
spectral_density_res = figure(title="Spectral Density", x_axis_label="f [Hz]",
                         y_axis_label="|S_XX(f)| [Power/Hz]",
                         plot_width=plot_width, plot_height=plot_height, x_range=[0, 25], output_backend="svg")
spectral_density_res.yaxis[0].formatter = PrintfTickFormatter(format = "%4.0e")
spectral_density_res.title.align = "center" #titel in the center
spectral_density_res.toolbar.logo = None 
spectral_density_res.outline_line_width = line_width
spectral_density_res.outline_line_color = "Black"
spectral_density_res.title.text_font_size = text_font_size
line_spectral_density_res = spectral_density_res.line([], [], line_color="royalblue", line_width=line_width)
ds_spectral_density_res = line_spectral_density_res.data_source

#probability density function of response 
# pdf_gaussian = figure(title="Probability Density", x_axis_label="u",
#                          y_axis_label="p_X(u)",
#                          plot_width=plot_width, plot_height=plot_height, output_backend="svg")
# pdf_gaussian.xaxis[0].formatter = PrintfTickFormatter(format = "%4.0e")
# pdf_gaussian.xaxis.major_label_orientation = "vertical"
# pdf_gaussian.align  = "center"
# pdf_gaussian.title.align = "center" #titel in the center
# pdf_gaussian.toolbar.logo = None 
# pdf_gaussian.outline_line_width = line_width
# pdf_gaussian.outline_line_color = "Black"
# pdf_gaussian.title.text_font_size = text_font_size
# line_gaussian_distribution = pdf_gaussian.line([], [], line_color="royalblue", line_width=line_width)
# ds_pdf_gaussian = line_gaussian_distribution.data_source
# vbar1_pdf_gaussian = pdf_gaussian.vbar(x = [], top =[], bottom = [], width=standard_deviation/20, line_color="olivedrab", alpha = 0.5,legend_label = "\u03C3" )
# ds_pdf_gaussian_vbar1 = vbar1_pdf_gaussian.data_source
# vbar2_pdf_gaussian = pdf_gaussian.vbar(x = [], top =[], bottom = [], width=standard_deviation/20, line_color="darkorange", alpha = 0.5, legend_label = "3\u03C3")
# ds_pdf_gaussian_vbar2 = vbar2_pdf_gaussian.data_source
# pdf_gaussian.legend.label_text_font_size = "7pt"

#cumulative distribution function of response 
# cdf_gaussian = figure(title="Cumulative Distribution", x_axis_label= "u",
#                          y_axis_label="\u03C6((u-\u03BC)/\u03C3)",
#                          plot_width=plot_width, plot_height=plot_height, output_backend="svg")
# cdf_gaussian.xaxis[0].formatter = PrintfTickFormatter(format = "%4.0e")
# cdf_gaussian.xaxis.major_label_orientation = "vertical"
# cdf_gaussian.title.align = "center" #titel in the center
# cdf_gaussian.align  = "center"
# cdf_gaussian.toolbar.logo = None 
# cdf_gaussian.outline_line_width = line_width
# cdf_gaussian.outline_line_color = "Black"
# cdf_gaussian.title.text_font_size = text_font_size
# line_cdf_gaussian = cdf_gaussian.line([], [], line_color="royalblue", line_width=line_width)
# ds_cdf_gaussian = line_cdf_gaussian.data_source

#bivariate distibution of response 
# bivariate_gaussian = figure(title="Bivariate Distribution", x_axis_label= "X 1",
#                          y_axis_label="X 2",
#                          plot_width=plot_width, plot_height=plot_height, output_backend="svg")
# bivariate_gaussian.title.align = "center" #titel in the center
# bivariate_gaussian.align  = "center"
# bivariate_gaussian.toolbar.logo = None 
# bivariate_gaussian.outline_line_width = line_width
# bivariate_gaussian.title.text_font_size = text_font_size
# line_bivariate_gaussian = bivariate_gaussian.multi_line(xs = [], ys = [], line_color = [])
# ds_bivariate_gaussian = line_bivariate_gaussian.data_source

#probability of survival of response realization
# prob_of_survival = figure(title="Probability of Survival", x_axis_label="t [s]",
#                          y_axis_label=f"L_X(u = (u\u03C3),t)",
#                          plot_width=plot_width, plot_height=plot_height, x_range=[0, 4], output_backend="svg")
# prob_of_survival.title.align = "center" #titel in the center
# prob_of_survival.align  = "center"
# prob_of_survival.toolbar.logo = None 
# prob_of_survival.outline_line_width = line_width
# prob_of_survival.outline_line_color = "Black"
# prob_of_survival.title.text_font_size = text_font_size
# line_prob_of_survival = prob_of_survival.line([], [], line_color="royalblue", line_width=line_width)
# ds_prob_of_survival = line_prob_of_survival.data_source

#first passage time of response realization
# prob_of_time = figure(title="First Passage Time", x_axis_label="t [s]",
#                          y_axis_label="p(T_X(t))",
#                          plot_width=plot_width, plot_height=plot_height, x_range=[0, 4], output_backend="svg")
# prob_of_time.title.align = "center" #titel in the center
# prob_of_time.align  = "center"
# prob_of_time.toolbar.logo = None 
# prob_of_time.outline_line_width = line_width
# prob_of_time.outline_line_color = "Black"
# prob_of_time.title.text_font_size = text_font_size
# line_prob_of_time = prob_of_time.line([], [], line_color="royalblue", line_width=line_width)
# ds_prob_of_time = line_prob_of_time.data_source

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------call back functions---------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def update_statistic_checkbox(attrname, old, new): 
# #Makes sure that only on item (covariance, spectral density or theory is selected and shows bokeh widgets accordingly)
#     global active_statistical #varaible that remembers last checkbox item
#     if statistical_property_checkbox.active == [1]: #theory
#         covariance_checkbox.visible = False
#         theory_div.visible = True
#         covariance_checkbox.active = []
#         update_checkbox(None, None, None)
    
#     if (statistical_property_checkbox.active == [0,1]):
#         #If used selects more than one checkbox item at ones, the fisr selected item is active
#         statistical_property_checkbox.active = active_statistical
    
#     if statistical_property_checkbox.active == [0]:
#         covariance_checkbox.visible = True
#         theory_div.visible = False
       
#     active_statistical = statistical_property_checkbox.active

def update_covariance_checkbox(attrname, old, new):
    global active_cov
    if (covariance_checkbox.active == [0,1]) | (covariance_checkbox.active == [1,2]) | (covariance_checkbox.active == [2,3]) | (covariance_checkbox.active == [0,3]) | (covariance_checkbox.active == [1,3]) | (covariance_checkbox.active == [0,2]):
        covariance_checkbox.active = active_cov

    update_checkbox(None, None, None)
    active_cov = covariance_checkbox.active

def update_checkbox(attrname, old, new):
    global excitation, realizations

    ds_response_time.data["x"] = t_list
    ds_response_time.data["y"] = []
    ds_responsef_freq.data["x"] = t_list
    ds_responsef_freq.data["y"] = []
    
    ds_spectral_density_res.data["x"] = t_list
    ds_spectral_density_res.data["y"] = []

    ds_covariance_res.data["x"] = t_list
    ds_covariance_res.data["y"] = []


    ds_ex_new1.data["x"] = t_list
    ds_ex_new1.data["y"] = []
    ds_ex_new2.data["x"] = t_list
    ds_ex_new2.data["y"] = []
    ds_ex_new3.data["x"] = t_list
    ds_ex_new3.data["y"] = []

    res_new_1.data["x"] = t_list
    res_new_1.data["y"] = []
    res_new_2.data["x"] = t_list
    res_new_2.data["y"] = []
    res_new_3.data["x"] = t_list
    res_new_3.data["y"] = []

    realizations = []

    # # changing GUI depending on checkbox values (Gaussian Process, Equalizer)
    # if  statistical_property_checkbox.active == [1]: 
    #     statistical_property_checkbox.visible = True
    #     theory_div.visible = True
    #     sigma_slider.visible = False
    #     mean_slider.visible = False
    #     ferquency_slider.visible = False
    #     bandwidth_slider.visible = False
    #     correlation_slider.visible = False
    #     mass_slider. visible = False
    #     damping_slider.visible = False
    #     stiffness_slider.visible = False
    #     transfer_time.visible = False
    #     transfer_freq_mag.visible = False
    #     excitation_time.visible = False
    #     excitation_freq.visible = False
    #     response_time.visible = False
    #     response_freq.visible = False
    #     covariance_exc.visible = False
    #     spectral_density_exc.visible = False
    #     covariance_res.visible = False
    #     spectral_density_res.visible = False
    #     calculate_button_Gauss.visible = False
    #     frequency_title.visible = False
    #     Add_Gaussian_Button.visible = False
    #     Remove_Gaussian_Button.visible = False
    #     Exitation_div.visible = False
    #     Response_div.visible = False
    #     # Gaussian_div.visible = False
    #     # Failure_div.visible = False
    #     # pdf_gaussian.visible = False
    #     # cdf_gaussian.visible = False
    #     #bivariate_gaussian.visible = False
    #     Control_para_div.visible = False
    #     # prob_of_survival.visible = False
    #     # prob_of_time.visible = False
    #     # failure_slider.visible = False
    #     SDOF_system_div.visible = False
    #     system_para_div.visible = False
    #     excitation_para.visible = False
    #     realization_div.visible = False
    # else:
    #     mass_slider. visible = True
    #     damping_slider.visible = True
    #     stiffness_slider.visible = True
    #     transfer_time.visible = True
    #     transfer_freq_mag.visible = True
    #     excitation_time.visible = True
    #     excitation_freq.visible = True
    #     response_time.visible = True
    #     response_freq.visible = True
    #     covariance_exc.visible = True
    #     spectral_density_exc.visible = True
    #     covariance_res.visible = True
    #     spectral_density_res.visible = True
    #     calculate_button_Gauss.visible = True
    #     frequency_title.visible = True
    #     Add_Gaussian_Button.visible = True
    #     Remove_Gaussian_Button.visible = True
    #     Exitation_div.visible = True
    #     Response_div.visible = True
    #     # Gaussian_div.visible = True
    #     # Failure_div.visible = True
    #     theory_div.visible = False
    #     # Failure_div.visible = True
    #     # pdf_gaussian.visible = True
    #     # cdf_gaussian.visible = True
    #     #bivariate_gaussian.visible = True
    #     Control_para_div.visible = True
    #     # prob_of_survival.visible = True
    #     # prob_of_time.visible = True
    #     # failure_slider.visible = True
    #     SDOF_system_div.visible = True
    #     system_para_div.visible = True
    #     excitation_para.visible = True
    #     realization_div.visible = True
        
    update_cov_slider()

def update_cov_slider():
    if covariance_checkbox.active == [0]: 
        sigma_slider.visible = True
        mean_slider.visible = True
        correlation_slider.visible = False
        ferquency_slider.visible = True
        bandwidth_slider.visible = True
    elif (covariance_checkbox.active == [1]) | (covariance_checkbox.active == [2]):
        sigma_slider.visible = True
        mean_slider.visible = True
        correlation_slider.visible = True
        ferquency_slider.visible = False
        bandwidth_slider.visible = False
    elif covariance_checkbox.active == [3]:
        sigma_slider.visible = True #nur wenn sigam auch einen einfluss hat ??????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
        mean_slider.visible = True
        correlation_slider.visible = False
        ferquency_slider.visible = False
        bandwidth_slider.visible = False
    update_excitation_cov(None, None, None)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------SDOF system calculatoin--------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# update unit impulse-response plot values in the time domain and in the frequency domain

def update_impulse(attrname, old, new):

    # passing slider values
    system_params.stiffness = stiffness_slider.value
    system_params.mass = mass_slider.value
    system_params.zeta = damping_slider.value
    frequency_title.text = f"Natural frequency: {round(system_params.w, 2)}rad/s or {round(system_params.w / (2 * np.pi), 2)}Hz"

    h_x = unit_impulse_function(t_list, system_params)  # unit impulse response values

    H_x = to_frequency_domain(t_list, h_x)  # harmonic transfer


    # passing arrays to plot
    ds_transfer_t.data["x"] = t_list
    ds_transfer_t.data["y"] = h_x
    ds_transfer_f_mag.data["x"] = f_list
    ds_transfer_f_mag.data["y"] = np.abs(H_x)  # abs(H_x.real)
    # ds_transfer_f_phase.data["x"] = tH_x
    # ds_transfer_f_phase.data["y"] = np.arctan(H_x.imag/H_x.real)  # abs(H_x.imag)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------excitation calculation---------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# function for calculation of the Force at given moment over which the Duhamel's Integral integrates
def excitation_real(t_list):
    global S

    degree_of_covariance = correlation_slider.value
    sigma = sigma_slider.value
    mean = mean_slider.value
    b = bandwidth_slider.value
    freq = ferquency_slider.value

    if covariance_checkbox.active == [0]:
        cov = cos_cov(t_list, freq, b, sigma) 
        solution = gaussian_function(mean*np.ones(len(t_list)),cov)

    elif covariance_checkbox.active == [1]:
        cov = squared_exponential_cov(t_list, sigma, degree_of_covariance) 
        solution  = gaussian_function(mean*np.ones(len(t_list)),cov) 
        
    elif covariance_checkbox.active == [2]:
        cov = matérn_class(t_list,0.5, sigma)
        solution  = gaussian_function(mean*np.ones(len(t_list)),cov)

    elif covariance_checkbox.active == [3]:
        cov = dirac_delta_cov(2, t_list) 
        solution  = gaussian_function(mean*np.ones(len(t_list)),cov)

    else: 
        solution = np.zeros(len(t_list))
    
    return solution

# # # update excitation plots in the time and frequency domain
def update_excitation_cov(attrname, old, new):
    global excitation

    excitation = excitation_real(t_list)  # excitation (y_values) on the time interval 

    p_fft = to_frequency_domain(t_list, excitation)  # FFT
   
    mean = mean_slider.value
    sigma = sigma_slider.value
 
    # passing arrays to plots
    ds_excitation_t.data["x"] = t_list
    ds_excitation_t.data["y"] = excitation
    ds_excitation_f_real.data["x"] =f_list
    ds_excitation_f_real.data["y"] = np.abs(p_fft)

    x = t_list
    y1 = (mean - sigma) * np.ones(len(t_list))
    y2 = (mean + sigma) * np.ones(len(t_list))

    ds_excitation_time_varea.data["x"] = x
    ds_excitation_time_varea.data["y1"] = y1
    ds_excitation_time_varea.data["y2"] = y2

    y1 = (mean - 3*sigma) * np.ones(len(t_list))
    y2 = (mean + 3*sigma) * np.ones(len(t_list))

    ds_excitation_time_3_varea.data["x"] = x
    ds_excitation_time_3_varea.data["y1"] = y1
    ds_excitation_time_3_varea.data["y2"] = y2

    ds_excitation_t_mean.data["x"] = t_list
    ds_excitation_t_mean.data["y"] = mean * np.ones(len(t_list))


    if len(realizations) == 1:
        ds_ex_new1.data["x"] = t_list
        ds_ex_new1.data["y"] = excitation_real(t_list)

    if len(realizations) == 2:
        ds_ex_new1.data["x"] = t_list
        ds_ex_new1.data["y"] = excitation_real(t_list)
        ds_ex_new2.data["x"] = t_list
        ds_ex_new2.data["y"] = excitation_real(t_list)

    if len(realizations) == 3: 
        ds_ex_new1.data["x"] = t_list
        ds_ex_new1.data["y"] = excitation_real(t_list)
        ds_ex_new2.data["x"] = t_list
        ds_ex_new2.data["y"] = excitation_real(t_list)
        ds_ex_new3.data["x"] = t_list
        ds_ex_new3.data["y"] = excitation_real(t_list)
    
    covariance_distribution()  

def covariance_distribution():
    global cov, S
    correlation = correlation_slider.value
    sigma = sigma_slider.value
    b = bandwidth_slider.value
    freq = ferquency_slider.value
    
    if covariance_checkbox.active == [0]:
        cov = cos_cov(t_list, freq, b, sigma)[512]  

    elif covariance_checkbox.active == [1]:
        cov = squared_exponential_cov(t_list, sigma, correlation)[512]  

    elif covariance_checkbox.active == [2]:
        cov = matérn_class(t_list, correlation, sigma)[512]  
        
    elif covariance_checkbox.active == [3]:
        cov = dirac_delta_cov(2, t_list)[512]  
        
    ds_covariance_exc.data["x"] = t_list
    ds_covariance_exc.data["y"] = cov
    spec_dens(cov)

def spec_dens(cov):
    global S
    S = to_frequency_domain(t_list, cov)
                
    ds_spectral_density_exc.data["x"] = f_list
    ds_spectral_density_exc.data["y"] = np.abs(S)


def add_Gaussian():
    global realizations
    realizations.append(excitation_real(t_list))

    if len(realizations) == 1:
        ds_ex_new1.data["x"] = t_list
        ds_ex_new1.data["y"] = realizations[0]

    if len(realizations) == 2:
        ds_ex_new2.data["x"] = t_list
        ds_ex_new2.data["y"] = realizations[1]

    if len(realizations) == 3:

        ds_ex_new3.data["x"] = t_list
        ds_ex_new3.data["y"] = realizations[2]
    else:
    #only three additional realizations can be added
        realizations = realizations[:3]

def delete_Gaussian():

    if len(realizations) == 1:
        ds_ex_new1.data["x"] = t_list
        ds_ex_new1.data["y"] = []
        realizations.pop()

    if len(realizations) == 2:
        ds_ex_new2.data["x"] = t_list
        ds_ex_new2.data["y"] = []
        realizations.pop()

    if len(realizations) == 3:
        ds_ex_new3.data["x"] = t_list
        ds_ex_new3.data["y"] = []
        realizations.pop()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------response calculation----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def calculate():

    res_new_1.data["x"] = t_list
    res_new_1.data["y"] = []
    res_new_2.data["x"] = t_list
    res_new_2.data["y"] = []
    res_new_3.data["x"] = t_list
    res_new_3.data["y"] = []

    response_cov()

def response_cov():
    global response_f, excitation
    system_params.stiffness = stiffness_slider.value
    system_params.mass = mass_slider.value
    system_params.zeta = damping_slider.value

    H_x = harmonic_transfer_function(f_list, system_params)

    p_fft = to_frequency_domain(t_list, excitation) #excitation in frequency domain
    u_fft =H_x * p_fft
        
    response_f = to_time_domain(f_list, u_fft) #displacement through frequency domain

    ds_response_time.data["x"] = t_list
    ds_response_time.data["y"] = response_f.real
    ds_responsef_freq.data["x"] = f_list
    ds_responsef_freq.data["y"] = np.abs(u_fft)


    if len(realizations) == 1:
            p_fft = to_frequency_domain(t_list, realizations[0]) #realizations in frequency domain
            u_fft =H_x * p_fft
            response_f = to_time_domain(f_list, u_fft)
            res_new_1.data["x"] = t_list
            res_new_1.data["y"] = response_f.real
            ds_response_time.data["x"] = t_list
            ds_response_time.data["y"] = response_f.real

    if len(realizations) == 2:
            p_fft = to_frequency_domain(t_list, realizations[0]) #realizations in frequency domain
            H_x * p_fft
            response_f = to_time_domain(f_list, u_fft)
            p_fft_2 = to_frequency_domain(t_list, realizations[1]) #realizations in frequency domain
            u_fft_2 =H_x* p_fft_2
            response_f_2 = to_time_domain(f_list, u_fft_2)
            res_new_1.data["x"] = t_list
            res_new_1.data["y"] = response_f.real
            res_new_2.data["x"] = t_list
            res_new_2.data["y"] = response_f_2.real
            ds_response_time.data["x"] = t_list
            ds_response_time.data["y"] = response_f.real      

    if len(realizations) == 3: 
            p_fft = to_frequency_domain(t_list, realizations[0]) #realizations in frequency domain
            H_x * p_fft
            response_f = to_time_domain(f_list, u_fft)
            p_fft_2 = to_frequency_domain(t_list, realizations[1]) #realizations in frequency domain
            u_fft_2 = H_x* p_fft_2
            response_f_2 = to_time_domain(f_list, u_fft_2)
            p_fft_3 = to_frequency_domain(t_list, realizations[2]) #realizations in frequency domain
            u_fft_3 = H_x* p_fft_3
            response_f_3 = to_time_domain(f_list, u_fft_3)
            res_new_1.data["x"] = t_list
            res_new_1.data["y"] = response_f.real
            res_new_2.data["x"] = t_list
            res_new_2.data["y"] = response_f_2.real
            res_new_3.data["x"] = t_list
            res_new_3.data["y"] = response_f_3.real
            ds_response_time.data["x"] = t_list
            ds_response_time.data["y"] = response_f.real

    calculate_stochastic()


def calculate_stochastic():
    global standard_deviation    
    mean = statistics.mean(response_f)

    ds_response_t_mean.data["x"] = t_list
    ds_response_t_mean.data["y"] = np.ones(len(t_list)) *mean
        
    H_x = harmonic_transfer_function(f_list, system_params)

    S_deform = np.multiply(np.abs(H_x)**2, S) 
    
    ds_spectral_density_res.data["x"] = f_list
    ds_spectral_density_res.data["y"] = np.abs(S_deform)
    
    cov_de =to_time_domain(f_list, S_deform)
    ds_covariance_res.data["x"] = t_list
    ds_covariance_res.data["y"] = cov_de.real

    variance = cov_de.real[512]
    standard_deviation = np.sqrt(variance)
    # standard_deviation = np.std(response)
        
    three_sigma = standard_deviation *3

    
    #plotting the shaded one- and three-sigma area
    x = t_list
    y1 = (mean- standard_deviation) * np.ones(len(t_list))
    y2 = (mean +standard_deviation) * np.ones(len(t_list))

    ds_response_varea1.data["x"] = x
    ds_response_varea1.data["y1"] = y1
    ds_response_varea1.data["y2"] = y2
    
    x = t_list
    y1 = (mean - three_sigma) * np.ones(len(t_list))
    y2 = (mean + three_sigma) * np.ones(len(t_list))

    ds_response_varea2.data["x"] = x
    ds_response_varea2.data["y1"] = y1
    ds_response_varea2.data["y2"] = y2


    # Gaussian_distribution()
    # failure(None, None, None)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------Gaussian distribution------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def Gaussian_distribution():
#     mean = statistics.mean(response_f)

#     u = np.linspace(-standard_deviation*5 + mean, standard_deviation * 5 + mean, 100)
#     gauss_pdf = Gaussian_distribution_pdf(u, mean, standard_deviation)
#     gauss_cdf = Gaussian_distribution_cdf(u, mean, standard_deviation)

#     x = np.linspace(-standard_deviation + mean, standard_deviation + mean, 20)
#     y = gauss_pdf[40:60]
#     y_bottom = np.zeros(len(y))

#     x_1 = np.linspace(-3*standard_deviation + mean,3*standard_deviation + mean, 60)
#     y_1 = gauss_pdf[20:80]
#     y1_bottom = np.zeros(len(y_1))

#     ds_pdf_gaussian_vbar1.data["x"]= x
#     ds_pdf_gaussian_vbar1.data["top"]= y
#     ds_pdf_gaussian_vbar1.data["bottom"]= y_bottom

#     ds_pdf_gaussian_vbar2.data["x"]= x_1
#     ds_pdf_gaussian_vbar2.data["top"]= y_1
#     ds_pdf_gaussian_vbar2.data["bottom"]= y1_bottom

#     ds_pdf_gaussian.data["x"] = u
#     ds_pdf_gaussian.data["y"] = gauss_pdf

#     ds_cdf_gaussian.data["x"] = u
#     ds_cdf_gaussian.data["y"] = gauss_cdf


#     # mean_bivariate = np.array([mean, mean])
#     # sigma_bivariate = np.array([[sigma, 0.95], [ 0.95, sigma]])
#     # xs, ys, col, xt, yt, text = plot_Gaussian_contours(mean_bivariate,sigma_bivariate)
    
#     # ds_bivariate_gaussian.data["xs"] = xs
#     # ds_bivariate_gaussian.data["ys"] = ys
#     # ds_bivariate_gaussian.data["col"] = col
#     # ds_bivariate_gaussian.data["xt"] = xt
#     # ds_bivariate_gaussian.data["yt"] = yt
#     # ds_bivariate_gaussian.data["text"] = text

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------failure calculation-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def failure(attr, old, new):
#     mean = statistics.mean(response_f)
#     velocity = np.gradient(response_f, dt)
#     sigma_velocity= np.std(velocity)
#     u = failure_slider.value * standard_deviation
#     v = 2 * rate_of_upcrossing(u, standard_deviation, sigma_velocity, 0)
#     d = norm(loc=mean, scale=standard_deviation)
#     L = d.cdf(np.abs(u)) #+ d.cdf(np.abs(-u)) 
#     prob_surv = prob_of_surv(v, L, t_list)

#     ds_prob_of_survival.data["x"] = t_list[512 :]
#     ds_prob_of_survival.data["y"] = prob_surv[512:]

#     prob_time = prob_of_failure_time(v, t_list)
#     #prob_of_survival.y_axis_label=f"Probability L_X(({failure_slider.value}\u03C3),t)"
#     ds_prob_of_time.data["x"] = t_list[512 :]
#     ds_prob_of_time.data["y"] = prob_time[512 :]

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------widgets callback-------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# statistical_property_checkbox.on_change("active", update_statistic_checkbox)
covariance_checkbox.on_change("active", update_covariance_checkbox)

damping_slider.on_change("value_throttled", update_impulse)
stiffness_slider.on_change("value_throttled", update_impulse) 
mass_slider.on_change("value_throttled", update_impulse)

sigma_slider.on_change("value_throttled", update_excitation_cov)
mean_slider.on_change("value_throttled", update_excitation_cov) #it will calculate a new Gaussian process, is this desirebale
correlation_slider.on_change("value_throttled", update_excitation_cov)
ferquency_slider.on_change("value_throttled", update_excitation_cov)
bandwidth_slider.on_change("value_throttled", update_excitation_cov)

Add_Gaussian_Button.on_click(add_Gaussian)
Remove_Gaussian_Button.on_click(delete_Gaussian)

calculate_button_Gauss.on_click(calculate)

# failure_slider.on_change("value_throttled", failure)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------pre run-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#WEBSITE_START

#calling callbacks at start of website so no values are undefined
#update_excitation_cov(None, None, None)
update_impulse(None, None, None)
# update_statistic_checkbox(None, None, None)
covariance_distribution()
spec_dens(cov)


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------bokeh layout-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# putting widgets into GUI
#inputs = column(para_div, damping_slider, stiffness_slider, mass_slider, frequency_title, explain_text, covariance_checkbox, transfer_time, transfer_freq, sigma_slider, mean_slider, calculation_title)
input_1 = row(damping_slider, stiffness_slider, mass_slider, frequency_title)
input_2 = row(spacer,transfer_time, transfer_freq_mag, spacer)
input_3 = row(sigma_slider, mean_slider, correlation_slider, ferquency_slider, bandwidth_slider)
input_4 = row(spacer, Add_Gaussian_Button, Remove_Gaussian_Button, spacer)


# putting plots into GUI

# explain = theory_div
plot = column(Exitation_div, row(covariance_exc, spectral_density_exc, excitation_time, excitation_freq),
                    calculate_button_Gauss, Response_div,
               row(covariance_res, spectral_density_res, response_time, response_freq)) #, data_table)
#, Gaussian_div,
            #    row(spacer, pdf_gaussian, cdf_gaussian, spacer), Failure_div, row(spacer,failure_slider), row(spacer,prob_of_survival, prob_of_time, spacer)

# final = column(title_div, statistical_property_checkbox, covariance_checkbox,explain, Control_para_div, system_para_div, input_1, excitation_para, input_3, SDOF_system_div ,input_2, realization_div, input_4,  plot)
final = column(title_div, theory_div, covariance_checkbox, Control_para_div, system_para_div, input_1, excitation_para, input_3, SDOF_system_div ,input_2, realization_div, input_4,  plot)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# add curdoc => start serverpa
curdoc().add_root(row(final, width=plot_width * 10))
curdoc().title = "SDOF under Random Vibration"
# export_svg(row(inputs, plots, width=plot_width * 3), filename="app")
# to terminal: bokeh serve --show main_.py
>>>>>>> 62f4189fd4a2825521a13dabe3092e6abed4705c:SDOF_ran_vib/main.py
