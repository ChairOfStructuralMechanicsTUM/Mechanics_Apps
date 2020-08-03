################################
#####       MAIN FILE      #####
################################

# general imports
from math import cos, sin, cosh, sinh
import numpy as np

# bokeh imports
from bokeh.plotting         import figure, output_file, ColumnDataSource as cds, reset_output 
from bokeh.io               import curdoc, show
from bokeh.layouts          import column, row, Spacer
from bokeh.models           import Slider, Button, Select, CustomJS, Div, Arrow, NormalHead, LogAxis
from bokeh.models.glyphs    import ImageURL

# latex integration
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexDiv, LatexLabel, LatexLabelSet, LatexSlider, LatexLegend

# internal imports
from TA_constants           import ( 
    c_orange, c_green, c_black, c_blue, c_gray, c_white,                    # colors
    pinned_support_img, fixed_support_left_img, fixed_support_right_img,    # support images
    img_h, img_w_fixed, img_w_pinned, y_fixed,                              # image properties
    F,L, EI,                                                                # fixed beam properties
    n, max_omega, max_amp_plot,                                             # fixed plotting properties
    X,Y, X_Amp, Y_Amp, X_NAF, Y_NAF, X_freq, Y_freq, mue                    # start values
    )

length_left =           2.0                                     # distance between the load and the left  support
length_right =          L-length_left                           # distance between the load and the right support
                                                      
omega=5.0                                                       # excitation frequency
lam =                   (mue*(omega**2)/EI)**(1/4)              # lambda (the length of the beam is already integrated in the coresponding calculations)

plot_values =           cds(data=dict(x=X,y=Y))                 # beam deflection coordinates

Amp_values =            cds(data=dict(x = X_Amp, y = Y_Amp))    # amplitude coordinates

NAF_values =            cds(data=dict(x = X_NAF, y = Y_NAF))    # coordinates of the amplitude pointer on the beam

freq_location =         cds(data=dict(x = X_freq, y = Y_freq))  # coordinates for the amplitude pointer

pointer_load =          cds(data = dict(xs = [length_left], xe =[length_left], ys = [4.5], ye=[3.5])) # pointer for the location of the load

selection =             0                                       # determines which beam is selected

support_source_left =   cds(data=dict(x = [-0.0015], y = [0.05], src = [pinned_support_img], w = [img_w_pinned] , h = [img_h])) # image support left
support_source_right =  cds(data=dict(x = [L-0.0015], y = [0.05], src = [pinned_support_img], w = [img_w_pinned] , h = [img_h]))# image support right


################################
#####      Functions       #####
################################

def change_matrix(length_left,length_right,EI,lam):                               # adjusts calculations to the different types of support
    global selection,support_source_left,support_source_right
    if selection == 0:                                                            # pinned-pinned beam
        M_line_2 = [0, 1, 0, -1, 0, 0, 0, 0]                                      # boundry condition momentum on the left support  = 0
        M_line_8 = [0, 0, 0, 0, sin(lam*length_right), cos(lam*length_right),     # boundry condition momentum on the right support = 0
                   -sinh(lam*length_right), -cosh(lam*length_right)]
        # updates support image
        support_source_left.data = dict(x = [-0.0015], y = [0.05], src = [pinned_support_img], w = [img_w_pinned] , h = [img_h])        
        support_source_right.data = dict(x = [L-0.0015], y = [0.05], src = [pinned_support_img], w = [img_w_pinned] , h = [img_h])      

    elif selection == 1:                                                          # fixed-pinned beam
        M_line_2 = [1, 0, 1, 0, 0, 0, 0, 0]                                       # boundry condition distortion of the left support = 0
        M_line_8 = [0, 0, 0, 0, sin(lam*length_right), cos(lam*length_right),     # boundry condition momentum on the right support  = 0
                   -sinh(lam*length_right), -cosh(lam*length_right)]
        # updates support image
        support_source_left.data = dict(x = [-0.05], y = [y_fixed], src = [fixed_support_left_img], w = [img_w_fixed] , h = [img_h])    
        support_source_right.data = dict(x = [L-0.0015], y = [0.05], src = [pinned_support_img], w = [img_w_pinned] , h = [img_h])      

    else:                                                                         # fixed-fixed beam
        M_line_2 = [1,0,1,0,0,0,0,0]                                              # boundry condition distortion of the left support  = 0
        M_line_8 = [0,0,0,0,cos(lam*length_right),-sin(lam*length_right),         # boundry condition distortion of the right support = 0
                   cosh(lam*length_right),sinh(lam*length_right)]
        # updates support image
        support_source_left.data = dict(x = [-0.05], y = [y_fixed], src = [fixed_support_left_img], w = [img_w_fixed] , h = [img_h])    
        support_source_right.data = dict(x = [L+0.05], y = [y_fixed], src = [fixed_support_right_img], w = [img_w_fixed] , h = [img_h]) 

    return M_line_2,M_line_8

def get_variables(length_left,length_right,EI,lam,F):   	                      # calculates the variables of the vibration boundary line
    [M_2,M_8] = change_matrix(length_left,length_right,EI,lam)
    M_ges = np.matrix([
        [0, 1, 0, 1, 0, 0, 0, 0],                                                                                   # line 1
        M_2,                                                                                                        # line 2 (variable)
        [sin(lam*length_left), cos(lam*length_left), sinh(lam*length_left), cosh(lam*length_left), 0, -1, 0, -1],   # line 3
        [cos(lam*length_left), -sin(lam*length_left), cosh(lam*length_left), sinh(lam*length_left), -1, 0, -1, 0],  # line 4
        [sin(lam*length_left), cos(lam*length_left), -sinh(lam*length_left), -cosh(lam*length_left), 0, -1, 0, 1],  # line 5
        [cos(lam*length_left), -sin(lam*length_left), -cosh(lam*length_left), -sinh(lam*length_left), -1, 0, 1, 0], # line 6
        [0, 0, 0, 0, sin(lam*length_right), cos(lam*length_right), sinh(lam*length_right), cosh(lam*length_right)], # line 7
        M_8])                                                                                                       # line 8 (variable)
    V_ges = np.matrix([[0],[0],[0],[0],[0],[F/(EI*(lam**3))],[0],[0]])           # vector of the matrix equation 

    [A1,A2,A3,A4,B1,B2,B3,B4] = (np.linalg.inv(M_ges))*V_ges                     # resulting variables    
    return A1,A2,A3,A4,B1,B2,B3,B4

def get_amp():                                                                    # calculates the deflection for every frequency
    global n,F,L,length_left,length_right,EI,X,Y,max_omega,F, mue

    if length_left == 0 or length_right == 0 or float(NAF_values.data['x'][0]) == 0 or float(NAF_values.data['x'][0]) == L:
       Amp_values.data['y'] = np.zeros(max_omega)     # precludes conditions, where no calculation is needed
    else:
        j = 1
        Y_temp = np.zeros(max_omega)
        while j < max_omega:
            lam_temp = (mue*(j**2)/EI)**(1/4)           # calculates lambda for every frequency      
            A1,A2,A3,A4,B1,B2,B3,B4 = get_variables(length_left,length_right,EI,lam_temp,F)
            if NAF_values.data['x'][0] <= length_left:  # for the subsystem on the left
                Y_temp[j] = -1*(A1*sin(lam_temp*NAF_values.data['x'][0])+A2*cos(lam_temp*NAF_values.data['x'][0])
                                 +A3*sinh(lam_temp*NAF_values.data['x'][0])+A4*cosh(lam_temp*NAF_values.data['x'][0]))
            else:                                       # for the subsystem on the right
                Y_temp[j] = -1*(B1*sin(lam_temp*(NAF_values.data['x'][0]-length_left))+B2*cos(lam_temp*(NAF_values.data['x'][0]-length_left))
                                 +B3*sinh(lam_temp*(NAF_values.data['x'][0]-length_left))+B4*cosh(lam_temp*(NAF_values.data['x'][0]-length_left)))
            j+=1
        Amp_values.data['y'] = np.absolute(Y_temp)      # calculates the absolute values

def get_values(n,F,L,length_left,length_right,omega,EI,lam,plot_values, X,Y):     # calculates the deflection for every point of the beam
    global selection
    if length_left == 0 or length_right == 0:                                     # precludes conditions, where no calculation is needed    
        Y = np.zeros(n)
        change_matrix(length_left,length_right,EI,lam)
    else:
        [M_2,M_8] = change_matrix(length_left,length_right,EI,lam)                # gets the variable matrix lines
        A1,A2,A3,A4,B1,B2,B3,B4 = get_variables(length_left,length_right,EI,lam,F) 

        X = np.linspace(0,L,n)
        Y = np.zeros(n)
        i = 0
        while i < n:
            if X[i] <= length_left:                                               # for the subsystem on the left
                Y[i] = -1*(A1*sin(lam*X[i])+A2*cos(lam*X[i])+A3*sinh(lam*X[i])+A4*cosh(lam*X[i]))
                
            else:                                                                 # for the subsystem on the right
                Y[i] = -1*(B1*sin(lam*(X[i]-length_left))+B2*cos(lam*(X[i]-length_left))+B3*sinh(lam*(X[i]-length_left))+B4*cosh(lam*(X[i]-length_left)))
            i+=1
        max_value = np.amax(np.absolute(Y))
        Y = Y * (3/max_value)                                                     # scales the deflection to a maximum amplitude of 3 

    plot_values.data = dict(y = Y, x = X)          # updates plot values

def get_selection(attr,old,new):                                                  # selects the type of beam
    global selection
    if new == "Pinned-Pinned beam":
        selection = 0
    elif new == "Fixed-Pinned beam":
        selection = 1
    elif new == "Fixed-Fixed beam":
        selection = 2
    get_values(n,F,L,length_left,length_right,omega,EI,lam,plot_values, X,Y)

def change_location_load(attr,old,new):                                           # changes the location of the load and adjust the location of its pointer
    global n,F,L,length_left,length_right,omega,EI,lam,plot_values, X,Y
    length_left = new                                           # defines the new place of the load
    length_right = L - length_left
    get_values(n,F,L,length_left,length_right,omega,EI,lam,plot_values, X,Y)
    pointer_load.stream(dict(xs = [length_left], xe =[length_left], ys = [4.5], ye=[3.5]),rollover=1) # updates load pointer
    
def change_location_NAF(attr,old,new):                                            # changes the location of the point used for the frequency plot
    global Y_NAF, X_NAF
    NAF_values.data = dict(x = [new,new], y = [-L,L])
    
def change_frequency (attr,old,new):                                              # changes the frequency of the oscillating load
    global n,F,L,length_left,length_right,omega,EI,lam,plot_values, X,Y
    omega = new                                                 # adjusts omega to the new value
    lam = (mue*(omega**2)/EI)**(1/4)                            # calculates the new lambda  
    get_values(n,F,L,length_left,length_right,omega,EI,lam,plot_values, X,Y)
    freq_location.data = dict(x = [new,new], y = [0.00001,max_amp_plot])

def disable_plot_sliders ():                                                      # disables / enables sliders coresponding to the frequency / load and frequency locations
    if switch_button.label == "Change load and\nshown location":# case 1: "Change load..." is displayed while pushing the button
        slider_location_load.disabled = False
        slider_location_freq.disabled = False 
        system_selection_select.disabled = False
        slider_frequency.disabled = True
        switch_button.label =  "Frequency Analysis"
        
    elif switch_button.label == "Frequency Analysis":           # case 2: "Frequency Analysis" is displayed while pushing the button
        slider_location_load.disabled = True
        slider_location_freq.disabled = True
        system_selection_select.disabled = True
        slider_frequency.disabled = False

        get_amp()
        switch_button.label = "Change load and\nshown location"


get_values(n,F,L,length_left,length_right,omega,EI,lam,plot_values, X,Y) # creates beam coordinates

arrow_load = Arrow(start=NormalHead(line_color=c_orange, fill_color = c_orange, fill_alpha = 0.5),       # creates the pointer for the load
                  end=NormalHead(line_alpha = 0, fill_alpha = 0),
             x_start='xs', y_start='ye', x_end='xe', y_end='ys', line_alpha = 0, source=pointer_load,line_color=c_white)

########################################
#####          MAIN PLOT           #####
########################################

plot = figure(x_range=[-0.2*L,1.2*L], y_range=[-L,L],height = 295, width= 600,toolbar_location = None, tools = "")

# cosmetics
plot.axis.visible = False
plot.grid.visible = False
plot.outline_line_color = c_gray

# beam starting position
plot.line(x=[0,L], y=[0,0], line_color = c_gray, line_dash ="4 4")

# beam supports
plot.add_glyph(support_source_left,ImageURL(url="src", x='x', y='y', w= 'w', h= 'h', anchor= "top_center"))
plot.add_glyph(support_source_right,ImageURL(url="src", x='x', y='y', w= 'w', h= 'h', anchor= "top_center"))

# display of the deflection
plot.line(x = 'x', y = 'y',source = plot_values, color = c_black)

# location of displayed frequency range
plot.line(x ='x', y = 'y', source = NAF_values, color = c_green, line_dash = "dashed")

# arrow for load indication
plot.add_layout(arrow_load)


########################################
#####        SECONDARY PLOT        #####
########################################

disp_freq = figure(x_range = [0,max_omega],y_axis_type="log", y_range = [0.00001,max_amp_plot],
                   height = 345, width = 250,toolbar_location = None, tools = "")

# cosmetics
disp_freq.yaxis.axis_label = "deflection [m]"
disp_freq.yaxis.visible = False
disp_freq.add_layout(LogAxis(axis_label='deflection [m]'), 'right')
disp_freq.xaxis.axis_label = "frequency [1/s]"
disp_freq.outline_line_color = c_gray

# deflection for every frequency
disp_freq.line(x = 'x', y = 'y', source = Amp_values)

# indicator for the current deflection
disp_freq.line(x = 'x', y = 'y', source = freq_location, line_dash = "dashed")



########################################
#####          User input          #####
########################################

# beam selection
system_selection_select = Select(title="Type of beam :", value="Pinned-Pinned beam", width=600, height = 40,
                                 options=["Pinned-Pinned beam", "Fixed-Pinned beam", "Fixed-Fixed beam"])
system_selection_select.on_change('value',get_selection)

# slider location load
slider_location_load = LatexSlider(title="\\text{Location of the load}=", value_unit="m", value=length_left,
                                   start=0.00, end=L, step=.01, width=423, height=30, bar_color = c_orange, 
                                   css_classes=["slider"])
slider_location_load.on_change('value',change_location_load)

# slider for location of the frequency
slider_location_freq = LatexSlider(title="\\text{Location of the frequency analysis}=", value_unit="m", 
                                   value=0, start=0, end=L, step=.01, width=423, height=30,
                                   bar_color = c_green, css_classes=["slider"]) 
slider_location_freq.on_change('value',change_location_NAF)

# slider for the excitation frequency
slider_frequency = LatexSlider(title="\\text{Frequency of the load}=", value_unit="\\frac{1}{s}", value=5, 
                               start=1, end=max_omega, step=1, width=185,height=40, bar_color = c_blue, 
                               css_classes=["slider"]) 
slider_frequency.on_change('value',change_frequency)

# button to switch between selection of the locations and the adjustment of the frequency display
switch_button = Button(label="Frequency Analysis", button_type="success", width=250, height=40)
switch_button.on_click(disable_plot_sliders)
slider_frequency.disabled = True

########################################
#####          TEXT FILES          #####
########################################

caption_1_filename = join(dirname(__file__), "caption_1.html")
caption_1 = Div(text=open(caption_1_filename).read(), render_as_text=False, height = 80, width=250)

caption_2_filename = join(dirname(__file__), "caption_2.html")
caption_2 = Div(text=open(caption_2_filename).read(), render_as_text=False, height = 55, width=600)

description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1000)

########################################
#####       ASSEMBLE THE APP       #####
########################################

curdoc().add_root(
    column(description,row(
        Spacer(width = 50),
                column(
                    Spacer(height = 15),
                    switch_button,
                    caption_1,
                    row(Spacer(width = 1, height = 40),slider_frequency),
                    disp_freq),                 
                                Spacer(width = 90),
                                        column(
                                            system_selection_select,
                                            Spacer(height = 15),                                            
                                            caption_2,
                                            row(Spacer(height = 30, width = 83),slider_location_load),
                                            row(Spacer(height = 30, width = 83),slider_location_freq),
                                            Spacer(height = 5),
                                            plot))))

curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
