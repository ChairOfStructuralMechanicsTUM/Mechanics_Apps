#################################
##           IMPORTS           ##
#################################

# general imports
from math import cos, sin, cosh, sinh, pi, sqrt
import numpy as np
import cmath as cm

# bokeh imports
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.layouts import column, row, Spacer
from bokeh.models import Slider, Button, Select, CustomJS, Div, Arrow, NormalHead, LogAxis, LinearAxis, ColumnDataSource, Range1d
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
    n_beam, n_r, max_r                                                      # plotting properties
    )


#################################
##        INITIALIZATION       ##
#################################

# initial parameters
length_left = 2.0                                   # initial distance between the load and the left support
length_right = L-length_left                        # initial distance between the load and the right support     
lfa = 2.0                                           # inital location of frequency analysis                                          
r = 0.2                                             # initial excitation frequency ratio
damping = 0.1                                       # initial damping coefficient
EI = complex(EI_real, EI_real*damping)              # Youngs Modulus * area moment of inertia
lam = pi*sqrt(r)*cm.sqrt(cm.sqrt(EI/EI_real))       # lambda 

# initial coordinates of the 3D plot
kmin = 0                                            # the first 100 rows of the 3D plot coordinates are plotted
kmax = 100
x_3D_all = np.linspace(0,L,26)
y_3D_all = np.linspace(0.04,10.0,250)
xx_all, yy_all = np.meshgrid(x_3D_all, y_3D_all)
value_unraveled_all = np.zeros((250,26))
zmax = 0.05
zmin = -0.05

# initial coordinates of the beam 
x_beam = np.linspace(0,L,n_beam)
y_beam = np.zeros(n_beam, dtype=complex)

# initial coordinates of the amplitude display
x_amp =                 np.linspace(0.04,max_r,n_r)
y_amp =                 np.zeros(n_r, dtype=complex)

# initial coordinates of the phase display
x_phase =                 np.linspace(0.04,max_r,n_r)
y_phase =                 np.zeros(n_r)

# initial coordinates of the pointer which indicates the location of frequency analysis
x_lfa =                 [lfa,lfa]
y_lfa =                 [-L,L]

# initial coordinates of the pointer which indicates the current frequency ratio for the amplitude
x_freq =                [r,r]
y_freq =                [0.00001,100]

# initial coordinates of the pointer which indicates the current frequency ratio for the phase angle
x_freq2 =                [r,r]
y_freq2 =                [-pi-0.1,pi+0.1]


#################################
##      COLUMNDATASOURCES      ##
#################################

# define global variables
length_left_glob = ColumnDataSource(data=dict(length_left=[length_left]))
length_right_glob = ColumnDataSource(data=dict(length_right=[length_right]))
r_glob = ColumnDataSource(data=dict(r=[r]))
lam_glob = ColumnDataSource(data=dict(lam=[lam]))
EI_glob = ColumnDataSource(data=dict(EI=[EI]))
value_unraveled_all_glob = ColumnDataSource(data=dict(value_unraveled_all=value_unraveled_all))
zmax_glob = ColumnDataSource(data=dict(zmax=[zmax]))
zmin_glob = ColumnDataSource(data=dict(zmin=[zmin]))
kmin_glob = ColumnDataSource(data=dict(kmin=[kmin]))
kmax_glob = ColumnDataSource(data=dict(kmax=[kmax]))

# define plotting variables
beam_coordinates_source = ColumnDataSource(data=dict(x=x_beam,y=y_beam.real))                 # beam deflection 
amp_coordinates_source = ColumnDataSource(data=dict(x = x_amp, y = y_amp.real))               # amplitude for every excitation frequency ratio
phase_coordinates_source = ColumnDataSource(data=dict(x = x_phase, y = y_phase))              # phase for every excitation frequency ratio
lfa_coordinates_source = ColumnDataSource(data=dict(x = x_lfa, y = y_lfa))                    # coordinates for the location of frequency analysis
freq_coordinates_source = ColumnDataSource(data=dict(x = x_freq, y = y_freq))                 # coordinates for the current excitation frequency ratio
freq2_coordinates_source = ColumnDataSource(data=dict(x = x_freq2, y = y_freq2))              # coordinates for the current excitation frequency ratio
load_arrow_source = ColumnDataSource(data=dict(xs = [length_left], xe =[length_left], ys = [4.5], ye=[3.5])) # coordinates for the location of the load
plot_3D_source = ColumnDataSource(data=dict(x=[], y=[], z=[]))                                # 3D plot coordinates
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

# amplitude for every excitation frequency ratio
disp_freq = figure(x_range = [0.04, max_r], y_axis_type="log", y_range = [0.00001,100],
                   height = 335, width = 280,toolbar_location = None, tools = "")
disp_freq.yaxis.visible = False
disp_freq.add_layout(LogAxis(axis_label='Normalized Deflection W(x)⋅E⋅I/(F⋅L³)'), 'right')
disp_freq.xaxis.axis_label = "Excitation Frequency Ratio"
disp_freq.outline_line_color = c_gray
disp_freq.line(x = 'x', y = 'y', source = amp_coordinates_source)
disp_freq.line(x = 'x', y = 'y', source = freq_coordinates_source, line_dash = "dashed")

# phase angle for every excitation frequency ratio
disp_phase = figure(x_range = [0.04, max_r], y_range = [-pi-0.1, pi+0.1],
                   height = 335, width = 280,toolbar_location = None, tools = "")
disp_phase.yaxis.axis_label = "Phase Angle [rad]"
disp_phase.yaxis.visible = False
disp_phase.add_layout(LinearAxis(axis_label='Phase Angle [rad]'), 'right')
disp_phase.xaxis.axis_label = "Excitation Frequency Ratio"
disp_phase.outline_line_color = c_gray
disp_phase.line(x = 'x', y = 'y', source = phase_coordinates_source)
disp_phase.line(x = 'x', y = 'y', source = freq2_coordinates_source, line_dash = "dashed")

# 3D plot
surface = Beam_Modes_Surface3d(x="x", y="y", z="z", data_source=plot_3D_source)


#################################
##          FUNCTIONS          ##
#################################

# calculates the coordinates of the 3D plot for new input parameters
def calculate_3d_plot_coordinates(system):     

    # get global variables
    [length_left] = length_left_glob.data["length_left"]
    [length_right] = length_right_glob.data["length_right"]
    [lam] = lam_glob.data["lam"]
    [EI] = EI_glob.data["EI"]

    xx = xx_all[0]

    value_unraveled_all = np.zeros((250,26), dtype=complex)
    if (length_left != 0 and length_right != 0) or (length_left != 0 and system=="Fixed-Free Beam"): # otherwise the beam is not deformed
        j = 0.04
        k = 0
        while j <= 10.0:
            lam_temp = calculate_lambda(system,j,EI)     # calculates lambda for every frequency
            lam_glob.data = dict(lam=[lam_temp])   
            A1,A2,A3,A4,B1,B2,B3,B4 = create_matrix_and_calculate_coefficients(system)

            i = 0
            while i < 26:
                if xx[i] <= length_left:                 # for the subsystem on the left
                    value_unraveled_all[k][i] = -1*EI*j*j/(F*(L**3))*(A1*cm.sin(lam_temp/L*xx[i])+A2*cm.cos(lam_temp/L*xx[i])+A3*cm.sinh(lam_temp/L*xx[i])+A4*cm.cosh(lam_temp/L*xx[i]))  
                else:                                    # for the subsystem on the right
                    value_unraveled_all[k][i] = -1*EI*j*j/(F*(L**3))*(B1*cm.sin(lam_temp/L*(xx[i]-length_left))+B2*cm.cos(lam_temp/L*(xx[i]-length_left))+B3*cm.sinh(lam_temp/L*(xx[i]-length_left))+B4*cm.cosh(lam_temp/L*(xx[i]-length_left)))
                i+=1       
            k+=1
            j = round(j+0.04,2)

    zmax = complex(max(value_unraveled_all.ravel().real), 0)    # get maximum z value
    zmin = complex(min(value_unraveled_all.ravel().real), 0)    # get minimum z value
    if (zmax.real == 0.0 and zmin.real == 0.0):
        zmax = complex(0.05, 0)
        zmin = complex(-0.05, 0)

    lam_glob.data = dict(lam=[lam])
    zmax_glob.data = dict(zmax=[zmax])
    zmin_glob.data = dict(zmin=[zmin])

    value_unraveled_all_glob.data = dict(value_unraveled_all=value_unraveled_all)

# updates the 3D plot when the excitation frequency ratio is changed
def update_3d_plot():

    # get global variables
    value_unraveled_all = value_unraveled_all_glob.data["value_unraveled_all"]
    [zmax] = zmax_glob.data["zmax"]
    [zmin] = zmin_glob.data["zmin"]
    [kmax] = kmax_glob.data["kmax"]
    [kmin] = kmin_glob.data["kmin"]
    
    # define grid: rows between kmin and kmax are used to plot the 3D plot
    xx = xx_all[kmin:kmax]                                  
    xx = xx.ravel()
    yy = yy_all[kmin:kmax]
    yy = yy.ravel()
    value_unraveled = value_unraveled_all[kmin:kmax]
    value = value_unraveled.ravel()

    # append value with zmax and zmin since only xx, yy and value are given to the class Beam_Modes_Surface3d
    xx = np.append(xx, [0, 0])
    yy = np.append(yy, [0, 0])
    value = np.append(value, [zmin, zmax])     

    plot_3D_source.data = dict(x=xx, y=yy, z=value.real)

# update support images when type of beam is changed and update the deflection
def change_selection(attr,old,new):    

    if new == "Pinned-Pinned Beam":
        support_left_source.data = dict(x = [-0.0015], y = [0.05], src = [pinned_support_img], w = [img_w_pinned] , h = [img_h])        
        support_right_source.data = dict(x = [L-0.0015], y = [0.05], src = [pinned_support_img], w = [img_w_pinned] , h = [img_h])  
    elif new == "Fixed-Fixed Beam":
        support_left_source.data = dict(x = [-0.05], y = [y_fixed], src = [fixed_support_left_img], w = [img_w_fixed] , h = [img_h])    
        support_right_source.data = dict(x = [L+0.05], y = [y_fixed], src = [fixed_support_right_img], w = [img_w_fixed] , h = [img_h])
    elif new == "Fixed-Pinned Beam":
        support_left_source.data = dict(x = [-0.05], y = [y_fixed], src = [fixed_support_left_img], w = [img_w_fixed] , h = [img_h])    
        support_right_source.data = dict(x = [L-0.0015], y = [0.05], src = [pinned_support_img], w = [img_w_pinned] , h = [img_h]) 
    elif new == "Fixed-Free Beam":
        support_left_source.data = dict(x = [-0.05], y = [y_fixed], src = [fixed_support_left_img], w = [img_w_fixed] , h = [img_h])    
        support_right_source.data = dict(x = [], y = [], src = [], w = [] , h = []) 

    calculate_deflection(system_select.value)

def calculate_lambda(system,r,EI):

    if system == "Pinned-Pinned Beam":
        lam = pi*sqrt(r)*cm.sqrt(cm.sqrt(EI/EI_real))   
    elif system == "Fixed-Fixed Beam":
        lam = 1.505618812*pi*sqrt(r)*cm.sqrt(cm.sqrt(EI/EI_real))    
    elif system == "Fixed-Pinned Beam":
        lam = 1.249876236*pi*sqrt(r)*cm.sqrt(cm.sqrt(EI/EI_real))   
    elif system == "Fixed-Free Beam":
        lam = 0.5968641408*pi*sqrt(r)*cm.sqrt(cm.sqrt(EI/EI_real))   

    return lam

# calculate coefficients C_1, C_2, C_3, C_4 for both subsystems
def create_matrix_and_calculate_coefficients(system): 

    # get global variables
    [length_left] = length_left_glob.data["length_left"]
    [length_right] = length_right_glob.data["length_right"]
    [lam] = lam_glob.data["lam"]
    [EI] = EI_glob.data["EI"]
                      
    if system == "Pinned-Pinned Beam":                     # moment of left support is equal to zero                                                           
        M_line_2 = [0, 1, 0, -1, 0, 0, 0, 0]   
    else:                                                   
        M_line_2 = [1, 0, 1, 0, 0, 0, 0, 0]                # distortion of left support is equal to zero
    if system == "Fixed-Free Beam":                        # lateral force of right support is equal to zero
        M_line_7 = [0, 0, 0, 0, cm.cos(lam/L*length_right), -cm.sin(lam/L*length_right),     
                    -cm.cosh(lam/L*length_right), -cm.sinh(lam/L*length_right)]
    else:                                                  # deflection of right support is equal to zero 
        M_line_7 = [0, 0, 0, 0, cm.sin(lam/L*length_right), cm.cos(lam/L*length_right),     
                    cm.sinh(lam/L*length_right), cm.cosh(lam/L*length_right)]
    if system == "Fixed-Fixed Beam":                       # distortion of right support is equal to zero
        M_line_8 = [0, 0, 0, 0, cm.cos(lam/L*length_right), -cm.sin(lam/L*length_right),         
                    cm.cosh(lam/L*length_right), cm.sinh(lam/L*length_right)]
    else:                                                  # moment of right support is equal to zero
        M_line_8 = [0, 0, 0, 0, cm.sin(lam/L*length_right), cm.cos(lam/L*length_right),     
                    -cm.sinh(lam/L*length_right), -cm.cosh(lam/L*length_right)]

    M_ges = np.matrix([
        [0, 1, 0, 1, 0, 0, 0, 0],                          # deflection of left support is always equal to zero                                                         
        M_line_2,                                                                                                        
        [cm.sin(lam/L*length_left), cm.cos(lam/L*length_left), cm.sinh(lam/L*length_left), cm.cosh(lam/L*length_left), 0, -1, 0, -1],   
        [cm.cos(lam/L*length_left), -cm.sin(lam/L*length_left), cm.cosh(lam/L*length_left), cm.sinh(lam/L*length_left), -1, 0, -1, 0], 
        [cm.sin(lam/L*length_left), cm.cos(lam/L*length_left), -cm.sinh(lam/L*length_left), -cm.cosh(lam/L*length_left), 0, -1, 0, 1],  
        [cm.cos(lam/L*length_left), -cm.sin(lam/L*length_left), -cm.cosh(lam/L*length_left), -cm.sinh(lam/L*length_left), -1, 0, 1, 0], 
        M_line_7, 
        M_line_8])
                                                                                                     
    V_ges = np.matrix([[0],[0],[0],[0],[0],[F/(EI*((lam/L)**3))],[0],[0]])           
    [A1,A2,A3,A4,B1,B2,B3,B4] = (np.linalg.inv(M_ges))*V_ges    
                      
    return A1,A2,A3,A4,B1,B2,B3,B4

# calculates the deflection for every point of the beam
def calculate_deflection(system):     

    # get global variables
    [length_left] = length_left_glob.data["length_left"]
    [length_right] = length_right_glob.data["length_right"]
    [lam] = lam_glob.data["lam"]

    A1,A2,A3,A4,B1,B2,B3,B4 = create_matrix_and_calculate_coefficients(system)

    y_beam = np.zeros(n_beam, dtype=complex)
    if (length_left != 0 and length_right != 0) or (length_left != 0 and system=="Fixed-Free Beam"):  # otherwise the beam is not deformed                                 
        i = 0
        while i < n_beam:
            if x_beam[i] <= length_left:                                          # for the subsystem on the left
                y_beam[i] = -1*(A1*cm.sin(lam/L*x_beam[i])+A2*cm.cos(lam/L*x_beam[i])+A3*cm.sinh(lam/L*x_beam[i])+A4*cm.cosh(lam/L*x_beam[i]))
            else:                                                                 # for the subsystem on the right
                y_beam[i] = -1*(B1*cm.sin(lam/L*(x_beam[i]-length_left))+B2*cm.cos(lam/L*(x_beam[i]-length_left))+B3*cm.sinh(lam/L*(x_beam[i]-length_left))+B4*cm.cosh(lam/L*(x_beam[i]-length_left)))
            i+=1

        # scales the deflection to a maximum amplitude of 3 
        max_value = np.amax(np.absolute(y_beam))
        y_beam = y_beam * (3/max_value) 
                                                     
    beam_coordinates_source.data = dict(x=x_beam,y=y_beam.real)

# calculates the amplitude of the deflection and the phase angle for every frequency
def calculate_amp_and_phase():

    # get global variables
    [length_left] = length_left_glob.data["length_left"]
    [length_right] = length_right_glob.data["length_right"]
    [lam] = lam_glob.data["lam"]
    [EI] = EI_glob.data["EI"]

    y_amp = np.zeros(n_r, dtype=complex)
    if (length_left != 0 and length_right != 0 and float(lfa_coordinates_source.data['x'][0]) != 0 and float(lfa_coordinates_source.data['x'][0]) != L) or (system_select.value=="Fixed-Free Beam" and float(lfa_coordinates_source.data['x'][0]) != 0 and length_left != 0):  # otherwise the amplitude is zero for every excitation frequency
        j = 0.04
        i = 0
        while j < max_r:
            lam_temp = calculate_lambda(system_select.value, j, EI)     # calculates lambda for every frequency ratio
            lam_glob.data = dict(lam=[lam_temp])   
            A1,A2,A3,A4,B1,B2,B3,B4 = create_matrix_and_calculate_coefficients(system_select.value)
            if lfa_coordinates_source.data['x'][0] <= length_left:      # for the subsystem on the left
                y_amp[i] = -1*EI/(F*(L**3))*(A1*cm.sin(lam_temp/L*lfa_coordinates_source.data['x'][0])+A2*cm.cos(lam_temp/L*lfa_coordinates_source.data['x'][0])
                                 +A3*cm.sinh(lam_temp/L*lfa_coordinates_source.data['x'][0])+A4*cm.cosh(lam_temp/L*lfa_coordinates_source.data['x'][0]))     
            else:                                                       # for the subsystem on the right
                y_amp[i] = -1*EI/(F*(L**3))*(B1*cm.sin(lam_temp/L*(lfa_coordinates_source.data['x'][0]-length_left))+B2*cm.cos(lam_temp/L*(lfa_coordinates_source.data['x'][0]-length_left))
                                 +B3*cm.sinh(lam_temp/L*(lfa_coordinates_source.data['x'][0]-length_left))+B4*cm.cosh(lam_temp/L*(lfa_coordinates_source.data['x'][0]-length_left)))
            j+=0.02
            i+=1         

    for i in range(0,n_r): 
        if slider_damping.value == 0:
            y_phase[i] = cm.phase(y_amp[i])            # calculate the phase angle for every exitation frequency ratio
        else:
            y_phase[i] = -cm.phase(y_amp[i])
        y_amp[i] = abs(y_amp[i])                       # calculate the absolute value  

    # update plotting variables
    amp_coordinates_source.data['y'] = y_amp.real   
    phase_coordinates_source.data['y'] = y_phase
    lam_glob.data = dict(lam=[lam])

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
    lfa_coordinates_source.data['x']= [new*L,new*L]

# if the damping is changed, update value for E*I
def change_damping(attr,old,new):
    EI = complex(EI_real, EI_real*new)
    EI_glob.data = dict(EI = [EI])

# if the excitation frequency ratio is changed, update beam deflection, 3D plot and corresponding global variables and plotting variables
def change_frequency_ratio(attr,old,new): 

    new = round(new,2)    
    old = round(old,2)  

    # get global variable                            
    [EI] = EI_glob.data["EI"]
                                           
    lam = calculate_lambda(system_select.value,new, EI) 
    lam_glob.data = dict(lam=[lam])                      
    calculate_deflection(system_select.value)

    freq_coordinates_source.data['x'] = [new,new]
    freq2_coordinates_source.data['x'] = [new,new]

    # kmin and kmax define which rows of the 3D plot coordinates are plotted
    if new <= 2.04:
        kmin = 0
        kmax = 100
    elif new >= 8:
        kmin = 149
        kmax = 249
    else:
        kmin = int(((new-2)/0.04)-1)
        kmax = int(((new+2)/0.04)-1)
    
    kmin_glob.data = dict(kmin = [kmin])
    kmax_glob.data = dict(kmax = [kmax])

    if (new > 2.04 and new < 8) or (new <= 2.04 and old > 2.04) or (new >= 8 and old < 8):  # otherwise the 3D plot doesn't change
        update_3d_plot()
    
# disables / enables sliders 
def disable_plot_sliders(): 

    # case 1: "Change input parameters" is displayed while pushing the button
    if switch_button.label == "⇦  Change Input Parameters":
        slider_location_load.disabled = False
        slider_location_freq.disabled = False 
        system_select.disabled = False
        slider_damping.disabled = False
        slider_frequency.disabled = True
        switch_button.label =  "Frequency Analysis  ⇨"
    
    # case 2: "Frequency Analysis" is displayed while pushing the button
    elif switch_button.label == "Frequency Analysis  ⇨":           
        slider_location_load.disabled = True
        slider_location_freq.disabled = True
        system_select.disabled = True
        slider_damping.disabled = True
        slider_frequency.disabled = False
        calculate_amp_and_phase()
        calculate_3d_plot_coordinates(system_select.value)
        update_3d_plot()
        freq_coordinates_source.data = dict(x = [slider_frequency.value, slider_frequency.value], y = [disp_freq.y_range.start, disp_freq.y_range.end])
        switch_button.label = "⇦  Change Input Parameters"


#################################
##          USER INPUT         ##
#################################

# selection for beam type
system_select = Select(title="Type of Beam:", value="Pinned-Pinned Beam", width=300,
                                 options=["Pinned-Pinned Beam", "Fixed-Fixed Beam", "Fixed-Pinned Beam", "Fixed-Free Beam"])
system_select.on_change('value', change_selection)

# slider for location of the load
slider_location_load = LatexSlider(title="\\text{Location of the Load} \\left[ \\mathrm{m} \\right]: ", value_unit="\\mathrm{L}", value=length_left/L,
                                   start=0, end=1, step=.01, width=423, bar_color = c_orange)
slider_location_load.on_change('value',change_location_load)

# slider for location of the frequency analysis
slider_location_freq = LatexSlider(title="\\text{Location of the Frequency Analysis} \\left[ \\mathrm{m} \\right]: ", value_unit="\\mathrm{L}", 
                                   value=lfa/L, start=0, end=1, step=.01, width=423, bar_color = c_green)
slider_location_freq.on_change('value',change_location_freq)

# slider for damping coefficient
slider_damping = LatexSlider(title="\\text{Loss Modulus } \\eta: ", value=damping, start=0.01, end=0.4, step=.01, width=423) 
slider_damping.on_change('value',change_damping)

# slider for excitation frequency ratio
slider_frequency = LatexSlider(title="\\text{Excitation Frequency Ratio } r=\\frac{\\Omega}{\\omega_1}: ", value=r, 
                               start=0.04, end=10, step=0.04, width=215, bar_color = c_blue) 
slider_frequency.on_change('value',change_frequency_ratio)

# button to switch between the adjustment of the input parameters and the adjustment of the excitation frequency ratio
switch_button = Button(label="Frequency Analysis  ⇨", button_type="success", width=200, height=40)
switch_button.on_click(disable_plot_sliders)
slider_frequency.disabled = True


#################################
##        INITIAL STATE        ##
#################################

calculate_deflection(system_select.value)
calculate_amp_and_phase()
calculate_3d_plot_coordinates(system_select.value)
update_3d_plot()


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