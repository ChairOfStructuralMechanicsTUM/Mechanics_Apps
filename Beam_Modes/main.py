## IMPORTS

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
    F, L, EI, mue,                                                           # beam properties
    n, max_omega,                                             # plotting properties
    )

length_left = 2.0                                     # distance between the load and the left support
length_right = L-length_left                           # distance between the load and the right support                                               
omega = 5.0                                                       # excitation frequency
lam = (mue*(omega**2)/EI)**(1/4)              # lambda (the length of the beam is already integrated in the corresponding calculations)

# initial coordinates of the 3D plot
x_3D = np.linspace(0,L,26)
y_3D = np.linspace(1,201,101)
xx, yy = np.meshgrid(x_3D, y_3D)
xx = xx.ravel()
yy = yy.ravel()
value_unraveled = np.zeros((101,26))
value = value_unraveled.ravel()
value_unraveled2 = np.zeros((101,26))
value2 = value_unraveled2.ravel()

# initial coordinates of the beam 
x_beam = np.linspace(0,L,n)
y_beam = np.zeros(n, dtype=complex)

# initial coordinates of the amplitude display
x_amp =                 np.linspace(1,max_omega,501)
y_amp =                 np.zeros(501, dtype=complex)

# initial coordinates of the phase display
x_phase =                 np.linspace(1,max_omega,501)
y_phase =                 np.zeros(501)

# initial coordinates of the pointer which indicates the location 
# of frequency analysis
x_lfa =                 [0.0,0.0]
y_lfa =                 [-L,L]

# initial coordinates of the pointer which indicates the current frequency
x_freq =                [omega,omega]
y_freq =                [-0.05,0.05]

# initial coordinates of the pointer which indicates the current frequency
x_freq2 =                [omega,omega]
y_freq2 =                [-pi,pi]

length_left_glob = ColumnDataSource(data=dict(length_left=[length_left]))
length_right_glob = ColumnDataSource(data=dict(length_right=[length_right]))
lam_glob = ColumnDataSource(data=dict(lam=[lam]))
y_3D_glob = ColumnDataSource(data=dict(y_3D=y_3D))
value_unraveled_glob = ColumnDataSource(data=dict(value_unraveled=value_unraveled))
value_unraveled_glob2 = ColumnDataSource(data=dict(value_unraveled2=value_unraveled2))

beam_coordinates_source = ColumnDataSource(data=dict(x=x_beam,y=y_beam.real))                 # beam deflection coordinates
amp_coordinates_source = ColumnDataSource(data=dict(x = x_amp, y = y_amp.real))    # amplitude coordinates
phase_coordinates_source = ColumnDataSource(data=dict(x = x_phase, y = y_phase))
lfa_coordinates_source = ColumnDataSource(data=dict(x = x_lfa, y = y_lfa))    # coordinates of the amplitude pointer on the beam
freq_coordinates_source = ColumnDataSource(data=dict(x = x_freq, y = y_freq))  # coordinates for the amplitude pointer
freq2_coordinates_source = ColumnDataSource(data=dict(x = x_freq2, y = y_freq2))
load_arrow_source = ColumnDataSource(data=dict(xs = [length_left], xe =[length_left], ys = [4.5], ye=[3.5])) # pointer for the location of the load
plot_3D_source = ColumnDataSource(data=dict(x=xx, y=yy, z=value.real))
plot_3D_source2 = ColumnDataSource(data=dict(x=xx, y=yy, z=value2.real))

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
disp_freq = figure(x_range = [1, max_omega], y_range = [-0.05,0.05],
                   height = 335, width = 280,toolbar_location = None, tools = "")
disp_freq.yaxis.visible = False
disp_freq.add_layout(LinearAxis(axis_label='Normalized Deflection W(x)⋅E⋅I/(F⋅L³)⋅Ω² [1/s²]'), 'right')
disp_freq.xaxis.axis_label = "Excitation Frequency [1/s]"
disp_freq.outline_line_color = c_gray

# deflection for every frequency
disp_freq.line(x = 'x', y = 'y', source = amp_coordinates_source)

# indicator for the current frequency
disp_freq.line(x = 'x', y = 'y', source = freq_coordinates_source, line_dash = "dashed")



## deflection for every frequency
disp_phase = figure(x_range = [1, max_omega], y_range = [-pi, pi],
                   height = 335, width = 280,toolbar_location = None, tools = "")
disp_phase.yaxis.axis_label = "Phase Angle [rad]"
disp_phase.yaxis.visible = False
disp_phase.add_layout(LinearAxis(axis_label='Phase Angle [rad]'), 'right')
disp_phase.xaxis.axis_label = "Excitation Frequency [1/s]"
disp_phase.outline_line_color = c_gray

# deflection for every frequency
disp_phase.line(x = 'x', y = 'y', source = phase_coordinates_source)

# indicator for the current frequency
disp_phase.line(x = 'x', y = 'y', source = freq2_coordinates_source, line_dash = "dashed")



## 3D plot
surface = Beam_Modes_Surface3d(x="x", y="y", z="z", data_source=plot_3D_source)

surface2 = Beam_Modes_Surface3d(x="x", y="y", z="z", data_source=plot_3D_source2)

################################
#####      Functions       #####
################################
def update_3d_plot(x_3D,system,EI,F):     # calculates the deflection for every point of the beam

    [length_left] = length_left_glob.data["length_left"]
    [length_right] = length_right_glob.data["length_right"]
    [lam] = lam_glob.data["lam"]
    y_3D = y_3D_glob.data["y_3D"]
    xx, yy = np.meshgrid(x_3D, y_3D)
    xx = xx.ravel()
    yy = yy.ravel()

    value_unraveled = np.zeros((101,26), dtype=complex)
    value_unraveled2 = np.zeros((101,26), dtype=complex)

    if (length_left != 0 and length_right != 0) or (length_left != 0 and system=="Fixed-Free beam"): 
        j = min(y_3D)
        k = 0
        while j <= max(y_3D):
            lam_temp = (mue*(j**2)/EI)**(1/4)  
            lam_glob.data = dict(lam=[lam_temp])   
            A1,A2,A3,A4,B1,B2,B3,B4 = create_matrix_and_calculate_coefficients(system, EI, F)
  
            i = 0
            while i < 26:
                if xx[i] <= length_left:                                               # for the subsystem on the left
                    value_unraveled[k][i] = -1*j*j*(A1*cm.sin(lam_temp*xx[i])+A2*cm.cos(lam_temp*xx[i])+A3*cm.sinh(lam_temp*xx[i])+A4*cm.cosh(lam_temp*xx[i])) 
                else:                                                                 # for the subsystem on the right
                    value_unraveled[k][i] = -1*j*j*(B1*cm.sin(lam_temp*(xx[i]-length_left))+B2*cm.cos(lam_temp*(xx[i]-length_left))+B3*cm.sinh(lam_temp*(xx[i]-length_left))+B4*cm.cosh(lam_temp*(xx[i]-length_left)))
                value_unraveled2[k][i] = value_unraveled[k][i]
                i+=1    
            max_value_unraveled_k = np.amax(np.absolute(value_unraveled[k]))
            value_unraveled[k] = value_unraveled[k] * (3/max_value_unraveled_k)    
            k+=1
            j+=2

    lam_glob.data = dict(lam=[lam])
    value = value_unraveled.ravel()
    value2 = value_unraveled2.ravel()
    plot_3D_source.data = dict(x=xx, y=yy, z=value.real)
    value_unraveled_glob.data = dict(value_unraveled=value_unraveled)
    plot_3D_source2.data = dict(x=xx, y=yy, z=value2.real)
    value_unraveled_glob2.data = dict(value_unraveled2=value_unraveled2)

def shift_3d_plot(old,new,F,system):
    [length_left] = length_left_glob.data["length_left"]
    [lam] = lam_glob.data["lam"]
    y_3D = y_3D_glob.data["y_3D"]
    value_unraveled = value_unraveled_glob.data["value_unraveled"]
    value_unraveled2 = value_unraveled_glob2.data["value_unraveled2"]

    xx, yy = np.meshgrid(x_3D, y_3D)
    xx = xx.ravel()
    yy = yy.ravel()

    if new-old == 2 or old-new == 2:
        if new > old:
            value_unraveled = value_unraveled[1:]
            value_unraveled2 = value_unraveled2[1:]
            j = max(y_3D)
        elif new < old:
            value_unraveled = value_unraveled[:100]
            value_unraveled2 = value_unraveled2[:100]
            j = min(y_3D)
        lam_temp = (mue*(j**2)/EI)**(1/4)  
        lam_glob.data = dict(lam=[lam_temp])   
        A1,A2,A3,A4,B1,B2,B3,B4 = create_matrix_and_calculate_coefficients(system, EI, F)
  
        i = 0
        a = np.zeros(26, dtype=complex)
        a2 = np.zeros(26, dtype=complex)
        while i < 26:
            if xx[i] <= length_left:                                               # for the subsystem on the left
                a[i] = -1*j*j*(A1*cm.sin(lam_temp*xx[i])+A2*cm.cos(lam_temp*xx[i])+A3*cm.sinh(lam_temp*xx[i])+A4*cm.cosh(lam_temp*xx[i]))  
            else:                                                                 # for the subsystem on the right
                a[i] = -1*j*j*(B1*cm.sin(lam_temp*(xx[i]-length_left))+B2*cm.cos(lam_temp*(xx[i]-length_left))+B3*cm.sinh(lam_temp*(xx[i]-length_left))+B4*cm.cosh(lam_temp*(xx[i]-length_left)))
            a2[i] = a[i]
            i+=1    
        max_a = np.amax(np.absolute(a))
        if max_a != 0:
            a = a * (3/max_a)

    else: 
        if new > old:
            
            num = int((new-old)/2)
            if (new > 101 and old < 101):
                num = int((new-101)/2)
            if new > 401:
                num = int((401-old)/2) 
            if num > 101:
                num = 101

            value_unraveled = value_unraveled[num:]
            value_unraveled2 = value_unraveled2[num:]
            
            a = np.zeros((num,26), dtype=complex)
            a2 = np.zeros((num,26), dtype=complex)
            j = y_3D[-num]
            k = 0
            while j <= max(y_3D):
                lam_temp = (mue*(j**2)/EI)**(1/4)  
                lam_glob.data = dict(lam=[lam_temp])   
                A1,A2,A3,A4,B1,B2,B3,B4 = create_matrix_and_calculate_coefficients(system, EI, F)
  
                i = 0
                while i < 26:
                    if xx[i] <= length_left:                                               # for the subsystem on the left
                        a[k][i] = -1*j*j*(A1*cm.sin(lam_temp*xx[i])+A2*cm.cos(lam_temp*xx[i])+A3*cm.sinh(lam_temp*xx[i])+A4*cm.cosh(lam_temp*xx[i]))  
                    else:                                                                 # for the subsystem on the right
                        a[k][i] = -1*j*j*(B1*cm.sin(lam_temp*(xx[i]-length_left))+B2*cm.cos(lam_temp*(xx[i]-length_left))+B3*cm.sinh(lam_temp*(xx[i]-length_left))+B4*cm.cosh(lam_temp*(xx[i]-length_left)))
                    a2[k][i] = a[k][i]
                    i+=1    
                max_a_k = np.amax(np.absolute(a[k]))
                if max_a_k != 0:
                    a[k] = a[k] * (3/max_a_k)    
                k+=1
                j+=2

        elif new < old:
            num = int((old-new)/2)
            if (new < 401 and old > 401):
                num = int((401-new)/2)
            if new < 101:
                num = int((old-101)/2) 
            if num > 101:
                num = 101
            value_unraveled = value_unraveled[:101-num]
            value_unraveled2 = value_unraveled2[:101-num]
        
            a = np.zeros((num,26), dtype=complex)
            a2 = np.zeros((num,26), dtype=complex)
            j = min(y_3D)
            k = 0
            while j <= y_3D[num-1]:
                lam_temp = (mue*(j**2)/EI)**(1/4)  
                lam_glob.data = dict(lam=[lam_temp])   
                A1,A2,A3,A4,B1,B2,B3,B4 = create_matrix_and_calculate_coefficients(system, EI, F)
  
                i = 0
                while i < 26:
                    if xx[i] <= length_left:                                               # for the subsystem on the left
                        a[k][i] = -1*j*j*(A1*cm.sin(lam_temp*xx[i])+A2*cm.cos(lam_temp*xx[i])+A3*cm.sinh(lam_temp*xx[i])+A4*cm.cosh(lam_temp*xx[i]))  
                    else:                                                                 # for the subsystem on the right
                        a[k][i] = -1*j*j*(B1*cm.sin(lam_temp*(xx[i]-length_left))+B2*cm.cos(lam_temp*(xx[i]-length_left))+B3*cm.sinh(lam_temp*(xx[i]-length_left))+B4*cm.cosh(lam_temp*(xx[i]-length_left)))
                    a2[k][i] = a[k][i]
                    i+=1   
                max_a_k = np.amax(np.absolute(a[k])) 
                if max_a_k != 0:
                    a[k] = a[k] * (3/max_a_k)    
                k+=1
                j+=2

    if new > old:
        value_unraveled = np.vstack((value_unraveled,a))
        value_unraveled2 = np.vstack((value_unraveled2,a2))

    elif new < old:
        value_unraveled = np.vstack((a,value_unraveled))
        value_unraveled2 = np.vstack((a2,value_unraveled2))
    
    value_unraveled_glob.data = dict(value_unraveled=value_unraveled)
    value = value_unraveled.ravel()
    plot_3D_source.data = dict(x=xx, y=yy, z=value.real)
    value_unraveled_glob2.data = dict(value_unraveled2=value_unraveled2)
    value2 = value_unraveled2.ravel()
    plot_3D_source2.data = dict(x=xx, y=yy, z=value2.real)
    lam_glob.data = dict(lam=[lam])


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
        M_line_7 = [0, 0, 0, 0, cm.cos(lam*length_right), -cm.sin(lam*length_right),     
                    -cm.cosh(lam*length_right), -cm.sinh(lam*length_right)]
    else:                                               # deflection is equal to zero
        M_line_7 = [0, 0, 0, 0, cm.sin(lam*length_right), cm.cos(lam*length_right),     
                    cm.sinh(lam*length_right), cm.cosh(lam*length_right)]
    if system == "Fixed-Fixed beam":                       # distortion is equal to zero
        M_line_8 = [0, 0, 0, 0, cm.cos(lam*length_right), -cm.sin(lam*length_right),         
                    cm.cosh(lam*length_right), cm.sinh(lam*length_right)]
    else:                                               # moment is equal to zero
        M_line_8 = [0, 0, 0, 0, cm.sin(lam*length_right), cm.cos(lam*length_right),     
                    -cm.sinh(lam*length_right), -cm.cosh(lam*length_right)]

    M_ges = np.matrix([
        [0, 1, 0, 1, 0, 0, 0, 0],                                                                                   
        M_line_2,                                                                                                        
        [cm.sin(lam*length_left), cm.cos(lam*length_left), cm.sinh(lam*length_left), cm.cosh(lam*length_left), 0, -1, 0, -1],   
        [cm.cos(lam*length_left), -cm.sin(lam*length_left), cm.cosh(lam*length_left), cm.sinh(lam*length_left), -1, 0, -1, 0], 
        [cm.sin(lam*length_left), cm.cos(lam*length_left), -cm.sinh(lam*length_left), -cm.cosh(lam*length_left), 0, -1, 0, 1],  
        [cm.cos(lam*length_left), -cm.sin(lam*length_left), -cm.cosh(lam*length_left), -cm.sinh(lam*length_left), -1, 0, 1, 0], 
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

    y_beam = np.zeros(n, dtype=complex)
    if (length_left != 0 and length_right != 0) or (length_left != 0 and system=="Fixed-Free beam"):                                     # precludes conditions, where no calculation is needed    
        i = 0
        while i < n:
            if x_beam[i] <= length_left:    
                y_beam[i] = -1*(A1*cm.sin(lam*x_beam[i])+A2*cm.cos(lam*x_beam[i])+A3*cm.sinh(lam*x_beam[i])+A4*cm.cosh(lam*x_beam[i]))
            else:                                                                 # for the subsystem on the right
                y_beam[i] = -1*(B1*cm.sin(lam*(x_beam[i]-length_left))+B2*cm.cos(lam*(x_beam[i]-length_left))+B3*cm.sinh(lam*(x_beam[i]-length_left))+B4*cm.cosh(lam*(x_beam[i]-length_left)))
            i+=1
        max_value = np.amax(np.absolute(y_beam))
        y_beam = y_beam * (3/max_value)                                                     # scales the deflection to a maximum amplitude of 3 
    beam_coordinates_source.data = dict(x=x_beam,y=y_beam.real)

def calculate_amp_and_phase(mue,EI,max_omega,F):                                                                    # calculates the deflection for every frequency
    [length_left] = length_left_glob.data["length_left"]
    [length_right] = length_right_glob.data["length_right"]
    [lam] = lam_glob.data["lam"]

    y_amp = np.zeros(501, dtype=complex)
    if (length_left != 0 and length_right != 0 and float(lfa_coordinates_source.data['x'][0]) != 0 and float(lfa_coordinates_source.data['x'][0]) != L) or (system_select.value=="Fixed-Free beam" and float(lfa_coordinates_source.data['x'][0]) != 0 and length_left != 0):
        j = 1
        while j < max_omega:
            lam_temp = (mue*(j**2)/EI)**(1/4)           # calculates lambda for every frequency  
            lam_glob.data = dict(lam=[lam_temp])   
            A1,A2,A3,A4,B1,B2,B3,B4 = create_matrix_and_calculate_coefficients(system_select.value, EI, F)
            if lfa_coordinates_source.data['x'][0] <= length_left:  # for the subsystem on the left
                y_amp[j-1] = -1*10000/(80*(5**3))*j*j*(A1*cm.sin(lam_temp*lfa_coordinates_source.data['x'][0])+A2*cm.cos(lam_temp*lfa_coordinates_source.data['x'][0])
                                 +A3*cm.sinh(lam_temp*lfa_coordinates_source.data['x'][0])+A4*cm.cosh(lam_temp*lfa_coordinates_source.data['x'][0]))
            else:                                       # for the subsystem on the right
                y_amp[j-1] = -1*10000/(80*(5**3))*j*j*(B1*cm.sin(lam_temp*(lfa_coordinates_source.data['x'][0]-length_left))+B2*cm.cos(lam_temp*(lfa_coordinates_source.data['x'][0]-length_left))
                                 +B3*cm.sinh(lam_temp*(lfa_coordinates_source.data['x'][0]-length_left))+B4*cm.cosh(lam_temp*(lfa_coordinates_source.data['x'][0]-length_left)))
            j+=1
    for i in range(0,501): 
        y_phase[i] = cm.phase(y_amp[i])
    amp_coordinates_source.data['y'] = y_amp.real      # calculates the absolute values
    phase_coordinates_source.data['y'] = y_phase
    lam_glob.data = dict(lam=[lam])
    if min(y_amp.real) == 0:
        disp_freq.y_range.start = -0.01
    else:
        disp_freq.y_range.start = 1.2*min(y_amp.real) 
    if max(y_amp.real) == 0:
        disp_freq.y_range.end = 0.01
    else:
        disp_freq.y_range.end = 1.2*max(y_amp.real)

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
        shift_3d_plot(old,new,F,system_select.value)
    

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
        calculate_amp_and_phase(mue,EI,max_omega,F)
        update_3d_plot(x_3D,system_select.value,EI,F)
        freq_coordinates_source.data = dict(x = [slider_frequency.value, slider_frequency.value], y = [disp_freq.y_range.start, disp_freq.y_range.end])
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
                               start=1, end=max_omega, step=2, width=215,height=40, bar_color = c_blue, 
                               css_classes=["slider"]) 
slider_frequency.on_change('value',change_frequency)

# button to switch between selection of the locations and the adjustment of the frequency 
switch_button = Button(label="Frequency Analysis  ⇨", button_type="success", width=220, height=40)
switch_button.on_click(disable_plot_sliders)
slider_frequency.disabled = True

calculate_deflection(n,x_beam,system_select.value,EI,F)
update_3d_plot(x_3D,system_select.value,EI,F)

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
                ), Spacer(height=20),plot, surface2
            ), Spacer(width=15),
            column(
                Spacer(height=225), switch_button
            ), Spacer(width=15),
            column(
                Spacer(height=39), slider_frequency, Spacer(height=11), disp_freq, disp_phase
            )
        )
    )
)

curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
