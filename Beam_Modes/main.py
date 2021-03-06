#################################
##           IMPORTS           ##
#################################

# general imports
from math import cos, sin, cosh, sinh, pi
import numpy as np
import cmath as cm

# bokeh imports
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.layouts import column, row, Spacer
from bokeh.models import Slider, Button, Select, CustomJS, Div, Arrow, NormalHead, LinearAxis, ColumnDataSource, Range1d
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
    F, L, mue, EI_real,                                                     # beam properties
    n, max_omega                                                           # plotting properties
    )


#################################
##        INITIALIZATION       ##
#################################

# initial parameters
length_left = 2.0                             # initial distance between the load and the left support
length_right = L-length_left                  # initial distance between the load and the right support                                               
omega = 5.0                                   # initial excitation frequency
damping = 0.1                                 # initial damping coefficient
EI = complex(EI_real, EI_real*damping)        # Youngs Modulus * area moment of inertia
lam = (mue*(omega**2)/EI)**(1/4)              # lambda (the length of the beam is already integrated in the corresponding calculations)

# initial coordinates of the 3D plot
x_3D = np.linspace(0,L,26)
y_3D = np.linspace(1,201,101)
xx, yy = np.meshgrid(x_3D, y_3D)
xx = xx.ravel()
yy = yy.ravel()
value_unraveled = np.zeros((101,26))
value = value_unraveled.ravel()

# initial coordinates of the beam 
x_beam = np.linspace(0,L,n)
y_beam = np.zeros(n, dtype=complex)

# initial coordinates of the amplitude display
x_amp =                 np.linspace(1,max_omega,501)
y_amp =                 np.zeros(501, dtype=complex)

# initial coordinates of the phase display
x_phase =                 np.linspace(1,max_omega,501)
y_phase =                 np.zeros(501)

# initial coordinates of the pointer which indicates the location of frequency analysis
x_lfa =                 [0.0,0.0]
y_lfa =                 [-L,L]

# initial coordinates of the pointer which indicates the current frequency for the amplitude
x_freq =                [omega,omega]
y_freq =                [-0.05,0.05]

# initial coordinates of the pointer which indicates the current frequency for the phase angle
x_freq2 =                [omega,omega]
y_freq2 =                [-pi,pi]


#################################
##      COLUMNDATASOURCES      ##
#################################

# define global variables
length_left_glob = ColumnDataSource(data=dict(length_left=[length_left]))
length_right_glob = ColumnDataSource(data=dict(length_right=[length_right]))
lam_glob = ColumnDataSource(data=dict(lam=[lam]))
y_3D_glob = ColumnDataSource(data=dict(y_3D=y_3D))
EI_glob = ColumnDataSource(data=dict(EI=[EI]))
value_unraveled_glob = ColumnDataSource(data=dict(value_unraveled=value_unraveled))

# define plotting variables
beam_coordinates_source = ColumnDataSource(data=dict(x=x_beam,y=y_beam.real))                 # beam deflection 
amp_coordinates_source = ColumnDataSource(data=dict(x = x_amp, y = y_amp.real))               # amplitude for every excitation frequency
phase_coordinates_source = ColumnDataSource(data=dict(x = x_phase, y = y_phase))              # phase for every excitation frequency
lfa_coordinates_source = ColumnDataSource(data=dict(x = x_lfa, y = y_lfa))                    # coordinates for the location of frequency analysis
freq_coordinates_source = ColumnDataSource(data=dict(x = x_freq, y = y_freq))                 # coordinates for the current excitation frequency 
freq2_coordinates_source = ColumnDataSource(data=dict(x = x_freq2, y = y_freq2))              # coordinates for the current excitation frequency
load_arrow_source = ColumnDataSource(data=dict(xs = [length_left], xe =[length_left], ys = [4.5], ye=[3.5])) # coordinates for the location of the load
plot_3D_source = ColumnDataSource(data=dict(x=xx, y=yy, z=value.real))                        # 3D plot
support_left_source = ColumnDataSource(data=dict(x = [-0.0015], y = [0.05], src = [pinned_support_img], w = [img_w_pinned] , h = [img_h]))   # image support left
support_right_source = ColumnDataSource(data=dict(x = [L-0.0015], y = [0.05], src = [pinned_support_img], w = [img_w_pinned] , h = [img_h])) # image support right


#################################
##            PLOTS            ##
#################################

# beam deflection
plot = figure(x_range=[-0.2*L,1.2*L], y_range=[-L,L],height = 295, width= 600,toolbar_location = None, tools = "")
plot.axis.visible = False
plot.grid.visible = False
plot.outline_line_color = c_gray
plot.line(x=[0,L], y=[0,0], line_color = c_gray, line_dash ="4 4")                                             # beam initial position
plot.add_glyph(support_left_source,ImageURL(url="src", x='x', y='y', w= 'w', h= 'h', anchor= "top_center"))    # beam supports
plot.add_glyph(support_right_source,ImageURL(url="src", x='x', y='y', w= 'w', h= 'h', anchor= "top_center"))   # beam supports
plot.line(x = 'x', y = 'y', source = beam_coordinates_source, color = c_black)                              
plot.line(x = 'x', y = 'y', source = lfa_coordinates_source, color = c_green, line_dash = "dashed")         
arrow_load = Arrow(start=NormalHead(line_color=c_orange, fill_color = c_orange, fill_alpha = 0.5),           
                   end=NormalHead(line_alpha = 0, fill_alpha = 0),
                   x_start='xs', y_start='ye', x_end='xe', y_end='ys', line_alpha = 0, source=load_arrow_source,line_color=c_white)
plot.add_layout(arrow_load)

# amplitude for every excitation frequency
disp_freq = figure(x_range = [1, max_omega], y_range = [-0.05,0.05],
                   height = 335, width = 280,toolbar_location = None, tools = "")
disp_freq.yaxis.visible = False
disp_freq.add_layout(LinearAxis(axis_label='Normalized Deflection W(x)⋅E⋅I⋅λ³/(F⋅L³) [-]'), 'right')
disp_freq.xaxis.axis_label = "Excitation Frequency [1/s]"
disp_freq.outline_line_color = c_gray
disp_freq.line(x = 'x', y = 'y', source = amp_coordinates_source)
disp_freq.line(x = 'x', y = 'y', source = freq_coordinates_source, line_dash = "dashed")

# phase angle for every excitation frequency
disp_phase = figure(x_range = [1, max_omega], y_range = [-pi, pi],
                   height = 335, width = 280,toolbar_location = None, tools = "")
disp_phase.yaxis.axis_label = "Phase Angle [rad]"
disp_phase.yaxis.visible = False
disp_phase.add_layout(LinearAxis(axis_label='Phase Angle [rad]'), 'right')
disp_phase.xaxis.axis_label = "Excitation Frequency [1/s]"
disp_phase.outline_line_color = c_gray
disp_phase.line(x = 'x', y = 'y', source = phase_coordinates_source)
disp_phase.line(x = 'x', y = 'y', source = freq2_coordinates_source, line_dash = "dashed")

# 3D plot
surface = Beam_Modes_Surface3d(x="x", y="y", z="z", data_source=plot_3D_source)


#################################
##          FUNCTIONS          ##
#################################

# calculates the deflection for the 3D plot for excitation frequencies between j_min and j_max
def calculate_3D_plot_coordinates(y_3D,j_min,j_max,xx,system,array):

    # get global variables
    [length_left] = length_left_glob.data["length_left"]
    [lam] = lam_glob.data["lam"]
    [EI] = EI_glob.data["EI"]

    j = j_min
    k = 0
    while j <= j_max:
        lam_temp = (mue*(j**2)/EI)**(1/4)            # calculates lambda for every frequency
        lam_glob.data = dict(lam=[lam_temp])   
        A1,A2,A3,A4,B1,B2,B3,B4 = create_matrix_and_calculate_coefficients(system)

        i = 0
        while i < 26:
            if xx[i] <= length_left:                 # for the subsystem on the left
                array[k][i] = -1*EI*(lam_temp**3)/(F*(L**3))*(A1*cm.sin(lam_temp*xx[i])+A2*cm.cos(lam_temp*xx[i])+A3*cm.sinh(lam_temp*xx[i])+A4*cm.cosh(lam_temp*xx[i]))  
            else:                                    # for the subsystem on the right
                array[k][i] = -1*EI*(lam_temp**3)/(F*(L**3))*(B1*cm.sin(lam_temp*(xx[i]-length_left))+B2*cm.cos(lam_temp*(xx[i]-length_left))+B3*cm.sinh(lam_temp*(xx[i]-length_left))+B4*cm.cosh(lam_temp*(xx[i]-length_left)))
            i+=1       
        k+=1
        j+=2

    lam_glob.data = dict(lam=[lam])

# calculates the coordinates of the 3D plot for new input parameters
def update_3d_plot(system):     

    # get global variables
    [length_left] = length_left_glob.data["length_left"]
    [length_right] = length_right_glob.data["length_right"]
    y_3D = y_3D_glob.data["y_3D"]

    # define grid
    xx, yy = np.meshgrid(x_3D, y_3D)
    xx = xx.ravel()
    yy = yy.ravel()

    value_unraveled = np.zeros((101,26), dtype=complex)
    if (length_left != 0 and length_right != 0) or (length_left != 0 and system=="Fixed-Free beam"): # otherwise the beam is not deformed
        j_min = min(y_3D)                 
        j_max = max(y_3D)
        calculate_3D_plot_coordinates(y_3D,j_min,j_max,xx,system,value_unraveled)

    # update plotting variables
    value = value_unraveled.ravel()
    plot_3D_source.data = dict(x=xx, y=yy, z=value.real)
    value_unraveled_glob.data = dict(value_unraveled=value_unraveled)

# shifts the 3D plot when the excitation frequency is changed
def shift_3d_plot(old,new,system):

    # get global variables
    y_3D = y_3D_glob.data["y_3D"]
    value_unraveled = value_unraveled_glob.data["value_unraveled"]

    # define grid
    xx, yy = np.meshgrid(x_3D, y_3D)
    xx = xx.ravel()
    yy = yy.ravel()

    if new > old:
        # number of excitation frequencies which have to be updated
        num = int((new-old)/2)                       
        if (new > 101 and old < 101):    
            num = int((new-101)/2)
        if new > 401:                    
            num = int((401-old)/2) 
        if num > 101:
            num = 101

        value_unraveled = value_unraveled[num:]           # delete corresponding values from the array
        
        # calculate new values
        a = np.zeros((num,26), dtype=complex)            
        j_min = y_3D[-num]
        j_max = max(y_3D)
        calculate_3D_plot_coordinates(y_3D,j_min,j_max,xx,system,a)

        value_unraveled = np.vstack((value_unraveled,a))  # add new values to the array

    elif new < old:
        # number of excitation frequencies which have to be updated
        num = int((old-new)/2)
        if (new < 401 and old > 401):
            num = int((401-new)/2)
        if new < 101:
            num = int((old-101)/2) 
        if num > 101:
            num = 101

        value_unraveled = value_unraveled[:101-num]       # delete corresponding values from the array

        # calculate new values
        a = np.zeros((num,26), dtype=complex)
        j_min = min(y_3D)
        j_max = y_3D[num-1]
        calculate_3D_plot_coordinates(y_3D,j_min,j_max,xx,system,a)

        value_unraveled = np.vstack((a,value_unraveled))  # add new values to the array

    # update plotting variables
    value_unraveled_glob.data = dict(value_unraveled=value_unraveled)
    value = value_unraveled.ravel()
    plot_3D_source.data = dict(x=xx, y=yy, z=value.real)

# update support images when type of beam is changed and update the deflection
def change_selection(attr,old,new):                                                 

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

    calculate_deflection(system_select.value)

# calculate coefficients C_1, C_2, C_3, C_4 for both subsystems
def create_matrix_and_calculate_coefficients(system): 

    # get global variables
    [length_left] = length_left_glob.data["length_left"]
    [length_right] = length_right_glob.data["length_right"]
    [lam] = lam_glob.data["lam"]
    [EI] = EI_glob.data["EI"]
                      
    if system == "Pinned-Pinned beam":                     # moment of left support is equal to zero                                                           
        M_line_2 = [0, 1, 0, -1, 0, 0, 0, 0]   
    else:                                                   
        M_line_2 = [1, 0, 1, 0, 0, 0, 0, 0]                # distortion of left support is equal to zero
    if system == "Fixed-Free beam":                        # lateral force of right support is equal to zero
        M_line_7 = [0, 0, 0, 0, cm.cos(lam*length_right), -cm.sin(lam*length_right),     
                    -cm.cosh(lam*length_right), -cm.sinh(lam*length_right)]
    else:                                                  # deflection of right support is equal to zero 
        M_line_7 = [0, 0, 0, 0, cm.sin(lam*length_right), cm.cos(lam*length_right),     
                    cm.sinh(lam*length_right), cm.cosh(lam*length_right)]
    if system == "Fixed-Fixed beam":                       # distortion of right support is equal to zero
        M_line_8 = [0, 0, 0, 0, cm.cos(lam*length_right), -cm.sin(lam*length_right),         
                    cm.cosh(lam*length_right), cm.sinh(lam*length_right)]
    else:                                                  # moment of right support is equal to zero
        M_line_8 = [0, 0, 0, 0, cm.sin(lam*length_right), cm.cos(lam*length_right),     
                    -cm.sinh(lam*length_right), -cm.cosh(lam*length_right)]

    M_ges = np.matrix([
        [0, 1, 0, 1, 0, 0, 0, 0],                          # deflection of left support is always equal to zero                                                         
        M_line_2,                                                                                                        
        [cm.sin(lam*length_left), cm.cos(lam*length_left), cm.sinh(lam*length_left), cm.cosh(lam*length_left), 0, -1, 0, -1],   
        [cm.cos(lam*length_left), -cm.sin(lam*length_left), cm.cosh(lam*length_left), cm.sinh(lam*length_left), -1, 0, -1, 0], 
        [cm.sin(lam*length_left), cm.cos(lam*length_left), -cm.sinh(lam*length_left), -cm.cosh(lam*length_left), 0, -1, 0, 1],  
        [cm.cos(lam*length_left), -cm.sin(lam*length_left), -cm.cosh(lam*length_left), -cm.sinh(lam*length_left), -1, 0, 1, 0], 
        M_line_7, 
        M_line_8])
                                                                                                     
    V_ges = np.matrix([[0],[0],[0],[0],[0],[F/(EI*(lam**3))],[0],[0]])           
    [A1,A2,A3,A4,B1,B2,B3,B4] = (np.linalg.inv(M_ges))*V_ges     
                      
    return A1,A2,A3,A4,B1,B2,B3,B4

# calculates the deflection for every point of the beam
def calculate_deflection(system):     

    # get global variables
    [length_left] = length_left_glob.data["length_left"]
    [length_right] = length_right_glob.data["length_right"]
    [lam] = lam_glob.data["lam"]

    A1,A2,A3,A4,B1,B2,B3,B4 = create_matrix_and_calculate_coefficients(system)

    y_beam = np.zeros(n, dtype=complex)
    if (length_left != 0 and length_right != 0) or (length_left != 0 and system=="Fixed-Free beam"):  # otherwise the beam is not deformed                                 
        i = 0
        while i < n:
            if x_beam[i] <= length_left:                                          # for the subsystem on the left
                y_beam[i] = -1*(A1*cm.sin(lam*x_beam[i])+A2*cm.cos(lam*x_beam[i])+A3*cm.sinh(lam*x_beam[i])+A4*cm.cosh(lam*x_beam[i]))
            else:                                                                 # for the subsystem on the right
                y_beam[i] = -1*(B1*cm.sin(lam*(x_beam[i]-length_left))+B2*cm.cos(lam*(x_beam[i]-length_left))+B3*cm.sinh(lam*(x_beam[i]-length_left))+B4*cm.cosh(lam*(x_beam[i]-length_left)))
            i+=1

        # scales the deflection to a maximum amplitude of 3 
        max_value = np.amax(np.absolute(y_beam))
        y_beam = y_beam * (3/max_value) 

    # update plotting variables                                                        
    beam_coordinates_source.data = dict(x=x_beam,y=y_beam.real)

# calculates the amplitude of the deflection and the phase angle for every frequency
def calculate_amp_and_phase():

    # get global variables
    [length_left] = length_left_glob.data["length_left"]
    [length_right] = length_right_glob.data["length_right"]
    [lam] = lam_glob.data["lam"]
    [EI] = EI_glob.data["EI"]

    y_amp = np.zeros(501, dtype=complex)
    if (length_left != 0 and length_right != 0 and float(lfa_coordinates_source.data['x'][0]) != 0 and float(lfa_coordinates_source.data['x'][0]) != L) or (system_select.value=="Fixed-Free beam" and float(lfa_coordinates_source.data['x'][0]) != 0 and length_left != 0):  # otherwise the amplitude is zero for every excitation frequency
        j = 1
        while j < max_omega:
            lam_temp = (mue*(j**2)/EI)**(1/4)           # calculates lambda for every frequency  
            lam_glob.data = dict(lam=[lam_temp])   
            A1,A2,A3,A4,B1,B2,B3,B4 = create_matrix_and_calculate_coefficients(system_select.value)
            if lfa_coordinates_source.data['x'][0] <= length_left:      # for the subsystem on the left
                y_amp[j-1] = -1*EI*(lam_temp**3)/(F*(L**3))*(A1*cm.sin(lam_temp*lfa_coordinates_source.data['x'][0])+A2*cm.cos(lam_temp*lfa_coordinates_source.data['x'][0])
                                 +A3*cm.sinh(lam_temp*lfa_coordinates_source.data['x'][0])+A4*cm.cosh(lam_temp*lfa_coordinates_source.data['x'][0]))
            else:                                                       # for the subsystem on the right
                y_amp[j-1] = -1*EI*(lam_temp**3)/(F*(L**3))*(B1*cm.sin(lam_temp*(lfa_coordinates_source.data['x'][0]-length_left))+B2*cm.cos(lam_temp*(lfa_coordinates_source.data['x'][0]-length_left))
                                 +B3*cm.sinh(lam_temp*(lfa_coordinates_source.data['x'][0]-length_left))+B4*cm.cosh(lam_temp*(lfa_coordinates_source.data['x'][0]-length_left)))
            j+=1

    for i in range(0,501): 
        y_phase[i] = cm.phase(y_amp[i])                # calculate the phase angle for every exitation frequency

    # update plotting variables
    amp_coordinates_source.data['y'] = y_amp.real      
    phase_coordinates_source.data['y'] = y_phase
    lam_glob.data = dict(lam=[lam])

    # adapt amplitude range to the maximum and minimum value
    if min(y_amp.real) == 0:
        disp_freq.y_range.start = -0.01
    else:
        disp_freq.y_range.start = 1.2*min(y_amp.real) 
    if max(y_amp.real) == 0:
        disp_freq.y_range.end = 0.01
    else:
        disp_freq.y_range.end = 1.2*max(y_amp.real)

# if the location of the load is changed, update beam deflection and corresponding global variables and plotting variables
def change_location_load(attr,old,new):            
    length_left = new*L                                         
    length_right = L - length_left
    length_left_glob.data = dict(length_left=[length_left])
    length_right_glob.data = dict(length_right=[length_right])
    calculate_deflection(system_select.value)
    load_arrow_source.stream(dict(xs = [length_left], xe =[length_left], ys = [4.5], ye=[3.5]),rollover=1) 

# if the location of frequency analysis is changed, update corresponding plotting variables
def change_location_freq(attr,old,new):             
    lfa_coordinates_source.data = dict(x = [new*L,new*L], y = [-L,L])

# if the damping is changed, update value for E*I
def change_damping(attr,old,new):
    EI = complex(EI_real, EI_real*new)
    EI_glob.data = dict(EI = [EI])

# if the excitation frequency is changed, update beam deflection, 3D plot and corresponding global variables and plotting variables
def change_frequency (attr,old,new):                  

    # get global variable                            
    [EI] = EI_glob.data["EI"]

    omega = new                                                 
    lam = (mue*(omega**2)/EI)**(1/4)  
    lam_glob.data = dict(lam=[lam])                      
    calculate_deflection(system_select.value)

    freq_coordinates_source.data = dict(x = [new,new], y = [disp_freq.y_range.start, disp_freq.y_range.end])
    freq2_coordinates_source.data = dict(x = [new,new], y = y_freq2)

    if new <= 101:
        y_3D = np.linspace(1,201,101)
    elif new >= 401:
        y_3D = np.linspace(301,501,101)
    else:
        y_3D = np.linspace(new-100,new+100,101)
    y_3D_glob.data=dict(y_3D=y_3D)

    if (new > 101 and new < 401) or (new <= 101 and old > 101) or (new >= 401 and old < 401):
        shift_3d_plot(old,new,system_select.value)
    
# disables / enables sliders 
def disable_plot_sliders(): 

    # case 1: "Change input parameters" is displayed while pushing the button
    if switch_button.label == "⇦  Change input parameters":
        slider_location_load.disabled = False
        slider_location_freq.disabled = False 
        system_select.disabled = False
        slider_frequency.disabled = True
        switch_button.label =  "Frequency Analysis  ⇨"
    
    # case 2: "Frequency Analysis" is displayed while pushing the button
    elif switch_button.label == "Frequency Analysis  ⇨":           
        slider_location_load.disabled = True
        slider_location_freq.disabled = True
        system_select.disabled = True
        slider_frequency.disabled = False
        calculate_amp_and_phase()
        update_3d_plot(system_select.value)
        freq_coordinates_source.data = dict(x = [slider_frequency.value, slider_frequency.value], y = [disp_freq.y_range.start, disp_freq.y_range.end])
        switch_button.label = "⇦  Change input parameters"


#################################
##          USER INPUT         ##
#################################

# selection for beam type
system_select = Select(title="Type of beam:", value="Pinned-Pinned beam", width=300,
                                 options=["Pinned-Pinned beam", "Fixed-Fixed beam", "Fixed-Pinned beam", "Fixed-Free beam"])
system_select.on_change('value', change_selection)

# slider for location of the load
slider_location_load = LatexSlider(title="\\text{Location of the load} \\left[ \\mathrm{m} \\right]: ", value_unit="\\mathrm{L}", value=length_left/L,
                                   start=0, end=1, step=.01, width=423, height=30, bar_color = c_orange, css_classes=["slider"])
slider_location_load.on_change('value',change_location_load)

# slider for location of the frequency analysis
slider_location_freq = LatexSlider(title="\\text{Location of the frequency analysis} \\left[ \\mathrm{m} \\right]: ", value_unit="\\mathrm{L}", 
                                   value=0, start=0, end=1, step=.01, width=423, height=30,
                                   bar_color = c_green, css_classes=["slider"]) 
slider_location_freq.on_change('value',change_location_freq)

# slider for damping coefficient
slider_damping = LatexSlider(title="\\text{Loss modulus } E'' \\left[ \\mathrm{\\frac{N}{m²}} \\right]: ", value_unit="\\mathrm{E'}", 
                                   value=damping, start=0, end=0.5, step=.01, width=423, height=30,
                                   css_classes=["slider"]) 
slider_damping.on_change('value',change_damping)

# slider for excitation frequency
slider_frequency = LatexSlider(title="\\text{Excitation frequency } \\Omega \\left[ \\mathrm{\\frac{1}{s}} \\right]: ", value=5, 
                               start=1, end=max_omega, step=2, width=215,height=30, bar_color = c_blue, 
                               css_classes=["slider"]) 
slider_frequency.on_change('value',change_frequency)

# button to switch between the adjustment of the input parameters and the adjustment of the excitation frequency 
switch_button = Button(label="Frequency Analysis  ⇨", button_type="success", width=200, height=40)
switch_button.on_click(disable_plot_sliders)
slider_frequency.disabled = True


#################################
##        INITIAL STATE        ##
#################################

calculate_deflection(system_select.value)
update_3d_plot(system_select.value)


#################################
##       APP DESCRIPTION       ##
#################################

description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)


#################################
##          APP LAYOUT         ##
#################################

curdoc().add_root(
    column(
        description, system_select, Spacer(height=15),row(
            column(
                row(
                    Spacer(width=85), slider_damping
                ), 
                row(
                    Spacer(width=85), slider_location_load
                ), 
                row(
                    Spacer(width=85), slider_location_freq
                ),Spacer(height=15),plot, surface
            ), Spacer(width=15),
            column(
                Spacer(height=258), switch_button
            ), Spacer(width=15),
            column(
                Spacer(height=80), slider_frequency, Spacer(height=15), disp_freq, Spacer(height=15), disp_phase
            )
        )
    )
)

curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '




