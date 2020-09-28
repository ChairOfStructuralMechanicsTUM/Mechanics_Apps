## IMPORTS

# general imports
from math import cos, sin, cosh, sinh
import numpy as np

# bokeh imports
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.layouts import column, row, Spacer
from bokeh.models import Slider, Button, Select, CustomJS, Div, Arrow, NormalHead, LogAxis, ColumnDataSource
from bokeh.models.glyphs import ImageURL

# latex integration
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexDiv, LatexSlider

# internal imports
from Beam_Modes_surface3d import Beam_Modes_Surface3d
from Beam_Modes_constants import ( 
    c_orange, c_green, c_black, c_blue, c_gray, c_white,                    # colors
    pinned_support_img, fixed_support_left_img, fixed_support_right_img,    # support images
    img_h, img_w_fixed, img_w_pinned, y_fixed,                              # image properties
    F, L, EI, mue,                                                           # beam properties
    n, max_omega, max_amp_plot,                                             # plotting properties
    )

length_left = 2.0                                     # distance between the load and the left support
length_right = L-length_left                           # distance between the load and the right support                                               
omega = 5.0                                                       # excitation frequency
lam = (mue*(omega**2)/EI)**(1/4)              # lambda (the length of the beam is already integrated in the corresponding calculations)

# initial coordinates of the beam 
x_beam = np.linspace(0,L,n)
y_beam = np.zeros(n)

# initial coordinates of the amplitude display
x_amp =                 np.linspace(1,max_omega,max_omega)
y_amp =                 np.zeros(max_omega)

# initial coordinates of the pointer which indicates the location 
# of frequency analysis
x_lfa =                 [0.0,0.0]
y_lfa =                 [-L,L]

# initial coordinates of the pointer which indicates the current frequency
x_freq =                [omega,omega]
y_freq =                [0.00001,max_amp_plot]

length_left_glob = ColumnDataSource(data=dict(length_left=[length_left]))
length_right_glob = ColumnDataSource(data=dict(length_right=[length_right]))
lam_glob = ColumnDataSource(data=dict(lam=[lam]))

beam_coordinates_source = ColumnDataSource(data=dict(x=x_beam,y=y_beam))                 # beam deflection coordinates
amp_coordinates_source = ColumnDataSource(data=dict(x = x_amp, y = y_amp))    # amplitude coordinates
lfa_coordinates_source = ColumnDataSource(data=dict(x = x_lfa, y = y_lfa))    # coordinates of the amplitude pointer on the beam
freq_coordinates_source = ColumnDataSource(data=dict(x = x_freq, y = y_freq))  # coordinates for the amplitude pointer
load_arrow_source = ColumnDataSource(data = dict(xs = [length_left], xe =[length_left], ys = [4.5], ye=[3.5])) # pointer for the location of the load


support_left_source = ColumnDataSource(data=dict(x = [-0.0015], y = [0.05], src = [pinned_support_img], w = [img_w_pinned] , h = [img_h]))   # image support left
support_right_source = ColumnDataSource(data=dict(x = [L-0.0015], y = [0.05], src = [pinned_support_img], w = [img_w_pinned] , h = [img_h])) # image support right

####################################
##              PLOTS             ##
####################################

## beam
plot = figure(x_range=[-0.2*L,1.2*L], y_range=[-L,L],height = 295, width= 600,toolbar_location = None, tools = "")
plot.axis.visible = False
plot.grid.visible = False
plot.outline_line_color = c_gray

# beam initial position
plot.line(x=[0,L], y=[0,0], line_color = c_gray, line_dash ="4 4")

# beam supports
plot.add_glyph(support_left_source,ImageURL(url="src", x='x', y='y', w= 'w', h= 'h', anchor= "top_center"))
plot.add_glyph(support_right_source,ImageURL(url="src", x='x', y='y', w= 'w', h= 'h', anchor= "top_center"))

# beam deflection
plot.line(x = 'x', y = 'y', source = beam_coordinates_source, color = c_black)

# pointer which indicates location of frequency analysis
plot.line(x = 'x', y = 'y', source = lfa_coordinates_source, color = c_green, line_dash = "dashed")

# arrow for load indication
arrow_load = Arrow(start=NormalHead(line_color=c_orange, fill_color = c_orange, fill_alpha = 0.5),      
                   end=NormalHead(line_alpha = 0, fill_alpha = 0),
                   x_start='xs', y_start='ye', x_end='xe', y_end='ys', line_alpha = 0, source=load_arrow_source,line_color=c_white)
plot.add_layout(arrow_load)

## deflection for every frequency
disp_freq = figure(x_range = [1, max_omega],y_axis_type="log", y_range = [0.00001,max_amp_plot],
                   height = 335, width = 280,toolbar_location = None, tools = "")

disp_freq.yaxis.axis_label = "deflection [m]"
disp_freq.yaxis.visible = False
disp_freq.add_layout(LogAxis(axis_label='deflection [m]'), 'right')
disp_freq.xaxis.axis_label = "frequency [1/s]"
disp_freq.outline_line_color = c_gray

# deflection for every frequency
disp_freq.line(x = 'x', y = 'y', source = amp_coordinates_source)

# indicator for the current frequency
disp_freq.line(x = 'x', y = 'y', source = freq_coordinates_source, line_dash = "dashed")

## 3D plot
x_3D = np.linspace(0,L,100)
y_3D = np.linspace(1,max_omega,250)
xx, yy = np.meshgrid(x_3D, y_3D)
xx = xx.ravel()
yy = yy.ravel()

value = np.sin(xx/50 + 2/10) * np.cos(yy/50 + 2/10) * 50 + 50

source = ColumnDataSource(data=dict(x=xx, y=yy, z=value))

surface = Beam_Modes_Surface3d(x="x", y="y", z="z", data_source=source)


################################
#####      Functions       #####
################################
#def update_3d_plot():
#    ""

def change_selection(attr,old,new):                                                 
    [length_left] = length_left_glob.data["length_left"]
    [length_right] = length_right_glob.data["length_right"]
    [lam] = lam_glob.data["lam"]
    # update support images
    if new == "Pinned-Pinned beam":
        support_left_source.data = dict(x = [-0.0015], y = [0.05], src = [pinned_support_img], w = [img_w_pinned] , h = [img_h])        
        support_right_source.data = dict(x = [L-0.0015], y = [0.05], src = [pinned_support_img], w = [img_w_pinned] , h = [img_h])      
    elif new == "Fixed-Fixed beam":
        support_left_source.data = dict(x = [-0.05], y = [y_fixed], src = [fixed_support_left_img], w = [img_w_fixed] , h = [img_h])    
        support_right_source.data = dict(x = [L+0.05], y = [y_fixed], src = [fixed_support_right_img], w = [img_w_fixed] , h = [img_h]) 
    elif new == "Fixed-Pinned beam":
        support_left_source.data = dict(x = [-0.05], y = [y_fixed], src = [fixed_support_left_img], w = [img_w_fixed] , h = [img_h])    
        support_right_source.data = dict(x = [L-0.0015], y = [0.05], src = [pinned_support_img], w = [img_w_pinned] , h = [img_h])   
    elif new == "Fixed-Free beam":
        support_left_source.data = dict(x = [-0.05], y = [y_fixed], src = [fixed_support_left_img], w = [img_w_fixed] , h = [img_h])    
        support_right_source.data = dict(x = [], y = [], src = [], w = [] , h = []) 
    calculate_deflection(n,x_beam,system_select.value,EI,F)

def create_matrix_and_calculate_coefficients(system, EI, F): 

    [length_left] = length_left_glob.data["length_left"]
    [length_right] = length_right_glob.data["length_right"]
    [lam] = lam_glob.data["lam"]

    # M_line_1 doesn't change since the deflection at the left support is always zero                        
    if system == "Pinned-Pinned beam":                     # moment is equal to zero                                                           
        M_line_2 = [0, 1, 0, -1, 0, 0, 0, 0]   
    else:                                               # distortion is equal to zero
        M_line_2 = [1, 0, 1, 0, 0, 0, 0, 0]   
    if system == "Fixed-Free beam":                        # lateral force is equal to zero
        M_line_7 = [0, 0, 0, 0, cos(lam*length_right), -sin(lam*length_right),     
                    -cosh(lam*length_right), -sinh(lam*length_right)]
    else:                                               # deflection is equal to zero
        M_line_7 = [0, 0, 0, 0, sin(lam*length_right), cos(lam*length_right),     
                    sinh(lam*length_right), cosh(lam*length_right)]
    if system == "Fixed-Fixed beam":                       # distortion is equal to zero
        M_line_8 = [0, 0, 0, 0, cos(lam*length_right), -sin(lam*length_right),         
                    cosh(lam*length_right), sinh(lam*length_right)]
    else:                                               # moment is equal to zero
        M_line_8 = [0, 0, 0, 0, sin(lam*length_right), cos(lam*length_right),     
                    -sinh(lam*length_right), -cosh(lam*length_right)]

    M_ges = np.matrix([
        [0, 1, 0, 1, 0, 0, 0, 0],                                                                                   
        M_line_2,                                                                                                        
        [sin(lam*length_left), cos(lam*length_left), sinh(lam*length_left), cosh(lam*length_left), 0, -1, 0, -1],   
        [cos(lam*length_left), -sin(lam*length_left), cosh(lam*length_left), sinh(lam*length_left), -1, 0, -1, 0], 
        [sin(lam*length_left), cos(lam*length_left), -sinh(lam*length_left), -cosh(lam*length_left), 0, -1, 0, 1],  
        [cos(lam*length_left), -sin(lam*length_left), -cosh(lam*length_left), -sinh(lam*length_left), -1, 0, 1, 0], 
        M_line_7, 
        M_line_8])
                                                                                                      # line 8 (variable)
    V_ges = np.matrix([[0],[0],[0],[0],[0],[F/(EI*(lam**3))],[0],[0]])           # vector of the matrix equation 
    [A1,A2,A3,A4,B1,B2,B3,B4] = (np.linalg.inv(M_ges))*V_ges     
                    # resulting variables    
    return A1,A2,A3,A4,B1,B2,B3,B4

def calculate_deflection(n,x_beam,system,EI,F):     # calculates the deflection for every point of the beam

    [length_left] = length_left_glob.data["length_left"]
    [length_right] = length_right_glob.data["length_right"]
    [lam] = lam_glob.data["lam"]

    A1,A2,A3,A4,B1,B2,B3,B4 = create_matrix_and_calculate_coefficients(system, EI, F)

    y_beam = np.zeros(n)
    if (length_left != 0 and length_right != 0) or (length_left != 0 and system=="Fixed-Free beam"):                                     # precludes conditions, where no calculation is needed    
        i = 0
        while i < n:
            if x_beam[i] <= length_left:                                               # for the subsystem on the left
                y_beam[i] = -1*(A1*sin(lam*x_beam[i])+A2*cos(lam*x_beam[i])+A3*sinh(lam*x_beam[i])+A4*cosh(lam*x_beam[i]))  
            else:                                                                 # for the subsystem on the right
                y_beam[i] = -1*(B1*sin(lam*(x_beam[i]-length_left))+B2*cos(lam*(x_beam[i]-length_left))+B3*sinh(lam*(x_beam[i]-length_left))+B4*cosh(lam*(x_beam[i]-length_left)))
            i+=1
        max_value = np.amax(np.absolute(y_beam))
        y_beam = y_beam * (3/max_value)                                                     # scales the deflection to a maximum amplitude of 3 
    beam_coordinates_source.data = dict(x=x_beam,y=y_beam)

def calculate_amp(mue,EI,max_omega,F):                                                                    # calculates the deflection for every frequency
    [length_left] = length_left_glob.data["length_left"]
    [length_right] = length_right_glob.data["length_right"]
    [lam] = lam_glob.data["lam"]

    y_amp = np.zeros(max_omega)
    if (length_left != 0 and length_right != 0 and float(lfa_coordinates_source.data['x'][0]) != 0 and float(lfa_coordinates_source.data['x'][0]) != L) or (system_select.value=="Fixed-Free beam" and float(lfa_coordinates_source.data['x'][0]) != 0 and length_left != 0):
        j = 1
        while j < max_omega:
            lam_temp = (mue*(j**2)/EI)**(1/4)           # calculates lambda for every frequency  
            lam_glob.data = dict(lam=[lam_temp])   
            A1,A2,A3,A4,B1,B2,B3,B4 = create_matrix_and_calculate_coefficients(system_select.value, EI, F)
            if lfa_coordinates_source.data['x'][0] <= length_left:  # for the subsystem on the left
                y_amp[j] = -1*(A1*sin(lam_temp*lfa_coordinates_source.data['x'][0])+A2*cos(lam_temp*lfa_coordinates_source.data['x'][0])
                                 +A3*sinh(lam_temp*lfa_coordinates_source.data['x'][0])+A4*cosh(lam_temp*lfa_coordinates_source.data['x'][0]))
            else:                                       # for the subsystem on the right
                y_amp[j] = -1*(B1*sin(lam_temp*(lfa_coordinates_source.data['x'][0]-length_left))+B2*cos(lam_temp*(lfa_coordinates_source.data['x'][0]-length_left))
                                 +B3*sinh(lam_temp*(lfa_coordinates_source.data['x'][0]-length_left))+B4*cosh(lam_temp*(lfa_coordinates_source.data['x'][0]-length_left)))
            j+=1
    amp_coordinates_source.data['y'] = np.absolute(y_amp)      # calculates the absolute values
    lam_glob.data = dict(lam=[lam])

def change_location_load(attr,old,new):                                           # changes the location of the load and adjust the location of its pointer
    length_left = new*L                                         # defines the new place of the load
    length_right = L - length_left
    length_left_glob.data = dict(length_left=[length_left])
    length_right_glob.data = dict(length_right=[length_right])
    calculate_deflection(n,x_beam,system_select.value,EI,F)
    load_arrow_source.stream(dict(xs = [length_left], xe =[length_left], ys = [4.5], ye=[3.5]),rollover=1) # updates load pointer
    
def change_location_freq(attr,old,new):                                            # changes the location of the point used for the frequency plot
    lfa_coordinates_source.data = dict(x = [new*L,new*L], y = [-L,L])
    
def change_frequency (attr,old,new):                                              # changes the frequency of the oscillating load
    omega = new                                                 # adjusts omega to the new value
    lam = (mue*(omega**2)/EI)**(1/4)  
    lam_glob.data = dict(lam=[lam])                          # calculates the new lambda  
    calculate_deflection(n,x_beam,system_select.value,EI,F)
    freq_coordinates_source.data = dict(x = [new,new], y = [0.00001,max_amp_plot])

def disable_plot_sliders ():                                                      # disables / enables sliders coresponding to the frequency / load and frequency locations
    if switch_button.label == "⇦  Change load and shown location":# case 1: "Change load..." is displayed while pushing the button
        slider_location_load.disabled = False
        slider_location_freq.disabled = False 
        system_select.disabled = False
        slider_frequency.disabled = True
        switch_button.label =  "Frequency Analysis  ⇨"
        
    elif switch_button.label == "Frequency Analysis  ⇨":           # case 2: "Frequency Analysis" is displayed while pushing the button
        slider_location_load.disabled = True
        slider_location_freq.disabled = True
        system_select.disabled = True
        slider_frequency.disabled = False
        calculate_amp(mue,EI,max_omega,F)
        switch_button.label = "⇦  Change load and shown location"


########################################
#####          User input          #####
########################################

# system selection
system_select = Select(title="Type of beam:", value="Pinned-Pinned beam", width=300,
                                 options=["Pinned-Pinned beam", "Fixed-Fixed beam", "Fixed-Pinned beam", "Fixed-Free beam"])
system_select.on_change('value', change_selection)

# slider location load
slider_location_load = LatexSlider(title="\\text{Location of the load} \\left[ \\mathrm{m} \\right]: ", value_unit="\\mathrm{L}", value=length_left/L,
                                   start=0, end=1, step=.01, width=423, height=30, bar_color = c_orange, css_classes=["slider"])
slider_location_load.on_change('value',change_location_load)

# slider for location of the frequency analysis
slider_location_freq = LatexSlider(title="\\text{Location of the frequency analysis} \\left[ \\mathrm{m} \\right]: ", value_unit="\\mathrm{L}", 
                                   value=0, start=0, end=1, step=.01, width=423, height=30,
                                   bar_color = c_green, css_classes=["slider"]) 
slider_location_freq.on_change('value',change_location_freq)

# slider for the excitation frequency
slider_frequency = LatexSlider(title="\\text{Excitation frequency } \\Omega \\left[ \\mathrm{\\frac{1}{s}} \\right]: ", value=5, 
                               start=1, end=max_omega, step=1, width=215,height=40, bar_color = c_blue, 
                               css_classes=["slider"]) 
slider_frequency.on_change('value',change_frequency)

# button to switch between selection of the locations and the adjustment of the frequency 
switch_button = Button(label="Frequency Analysis  ⇨", button_type="success", width=220, height=40)
switch_button.on_click(disable_plot_sliders)
slider_frequency.disabled = True

calculate_deflection(n,x_beam,system_select.value,EI,F)

########################################
#####        ADD DESCRIPTION       #####
########################################

description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)

########################################
#####       ASSEMBLE THE APP       #####
########################################

curdoc().add_root(
    column(
        description, system_select, Spacer(height=20),row(
            column(
                row(
                    Spacer(width=85), slider_location_load
                ), 
                row(
                    Spacer(width=85), slider_location_freq
                ), Spacer(height=20),plot
            ), Spacer(width=15),
            column(
                Spacer(height=225), switch_button
            ), Spacer(width=15),
            column(
                Spacer(height=39), slider_frequency, Spacer(height=11), disp_freq
            )
        ), surface
    )
)

curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
