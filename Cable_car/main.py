"""
TENSIONS ON THE CABLE CAR TRANSPORTATION SYSTEM - This interactive web app 
computes the cable tensions of the cable car system for a user defined axial
location of the carriage car
Created on Tue Jun  1 22:53:14 2021
@author: Ramsubramanian Pazhanisamy
"""
#################################
##           IMPORTS           ##
#################################

# general imports
import numpy as np
import sympy as sp

# bokeh imports
from bokeh.io             import curdoc
from bokeh.plotting       import figure
from bokeh.models         import ColumnDataSource, Arrow, OpenHead, Range1d, TeeHead
from bokeh.models.glyphs  import ImageURL
from bokeh.models.widgets import Button
from bokeh.layouts        import column, row

# latex integration
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexDiv, LatexLabelSet, LatexSlider
# ----------------------------------------------------------------- #

###################################################
##           APP THEORETICAL DESCRIPTION         ##
###################################################
#Theoretical description of the app in Latex
description_filename1 = join(dirname(__file__), "description1.html") #Part I of the description
description1 = LatexDiv(text=open(description_filename1).read(), render_as_text=False, width=1000)

description_filename2 = join(dirname(__file__), "description2.html")#Part II of the description
description2 = LatexDiv(text=open(description_filename2).read(), render_as_text=False, width=1000)

description_filename3 = join(dirname(__file__), "description3.html")#Part III of the description
description3 = LatexDiv(text=open(description_filename3).read(), render_as_text=False, width=1000)

#Figures_static
#Kinematics of the cable car 
kinematics_img="Cable_car/static/images/Kinematics.svg"
figure_kin = figure(height=235, width=235)
figure_kin.toolbar.logo = None # do not display the bokeh logo
figure_kin.toolbar_location = None # do not display the tools 
figure_kin.x_range=Range1d(start=0, end=1)
figure_kin.y_range=Range1d(start=0, end=1)
figure_kin.xaxis.visible = None
figure_kin.yaxis.visible = None
figure_kin.xgrid.grid_line_color = None
figure_kin.ygrid.grid_line_color = None
kinematics_src = ColumnDataSource(dict(url = [kinematics_img]))
figure_kin.image_url(url='url', x=0, y = 1, h=1, w=1, source=kinematics_src)
figure_kin.outline_line_alpha = 0 

# Free boy diagram of the cable car
fbd_img="Cable_car/static/images/FreeBodyDiagram.svg"
figure_fbd = figure(height=259, width=279)
figure_fbd.toolbar.logo = None # do not display the bokeh logo
figure_fbd.toolbar_location = None # do not display the tools 
figure_fbd.x_range=Range1d(start=0, end=1)
figure_fbd.y_range=Range1d(start=0, end=1)
figure_fbd.xaxis.visible = None
figure_fbd.yaxis.visible = None
figure_fbd.xgrid.grid_line_color = None
figure_fbd.ygrid.grid_line_color = None
fbd_src = ColumnDataSource(dict(url = [fbd_img]))
figure_fbd.image_url(url='url', x=0, y = 1, h=1, w=1, source=fbd_src)
figure_fbd.outline_line_alpha = 0 

#################################
##        INITIALIZATION       ##
#################################

# Initial parameters & its limits
#Cable car dimensions & user inputs
H_max =550.0 #Verical distance between the supports (m) -H
H_min= 450.0
H=500.0

B_max=550.0 #Horizontal distance between the supports (m) -B
B_min=450.0
B=500.0

c_max=1.009  #Cable length stretch factor -c
c_min=1.003
c=(c_min+c_max)/2

M_max=300.0 #Mass of the cable car - M (Kg)
M_min=200.0 
M=250.0

x=0.5*B #Axial location of the cable car
D=np.sqrt(H*H+B*B) #Diagonal distance between the supports (m)
L=c*D #Length of the cable (m) - cable length should be always higher than the distance between the supports
theta_s1= np.arcsin(H/D) #Angle of the support 1 - bottom support
theta_s2= np.arcsin(B/D) #Angle of the support 2 - top support
W=M*9.81 #Weight of the car (N)

a1=0.0 #alpha1 - angle between the cable and diagonal joining the supports at bottom support
a2=0.0 #alpha2 - angle between the cable and diagonal joining the supports at top support            

#Symbolic constants for sympy - a1 & a2
alpha1=sp.Symbol('alpha1',real=True)
alpha2=sp.Symbol('alpha2',real=True)        

#Kinematic equations 
eq1= sp.Eq(((L-x/sp.cos(theta_s1-alpha1))*sp.sin(theta_s2-alpha2))+x-B,0)
eq2= sp.Eq((x/sp.cos(theta_s1-alpha1)*sp.sin(alpha1))-((L-x/sp.cos(theta_s1-alpha1))*sp.sin(alpha2)),0)    

#Simultaneously solving the system of equations numerically
[a1,a2]=sp.nsolve((eq1,eq2),(alpha1,alpha2),(0.10,0.10))    

#Effective angles on the Cable
theta_total1=float(theta_s1-a1) #Actual angle at S1 for a specific car position on the rope
theta_total2=float(theta_s2+a2) #Actual angle at S2 for a specific car position on the rope
Lx=x/np.cos(theta_total1) #Length of the bottom cable segement     

#Tensions on the Cable
T1= W/(np.sin(theta_total2)-(np.cos(theta_total2)*np.sin(theta_total1)/np.cos(theta_total1)))*(np.cos(theta_total2)/np.cos(theta_total1)) # Cable tension in the bottom
T2= W/(np.sin(theta_total2)-(np.cos(theta_total2)*np.sin(theta_total1)/np.cos(theta_total1)))  # Cable tension in the top
# ----------------------------------------------------------------- #

#################################
##     CALLBACK FUNCTIONS      ##
#################################

# Div to show tension and distance values
value_plot_distance_cable_length= LatexDiv(text="", render_as_text=False, width=300)
value_plot_angles1 = LatexDiv(text="", render_as_text=False, width=300)
value_plot_angles2 = LatexDiv(text="", render_as_text=False, width=300)
value_plot_tensions = LatexDiv(text="", render_as_text=False, width=300)

#Display the results
def setValueText(D,L,t1,t2,a1,a2,T1,T2):
    value_plot_distance_cable_length.text = "$$\\begin{aligned} D&=" + "{:4.1f}".format(D) + "\\,\\mathrm{m}\\\\ L&=" + "{:4.1f}".format(L) + "\\,\\mathrm{m} \\end{aligned}$$"    #Display the D & L
    value_plot_angles1.text = "$$\\begin{aligned} \\theta_1&=" + "{:4.1f}".format(t1) + "\\,\\mathrm{°}\\\\ \\theta_2&=" + "{:4.1f}".format(t2) + "\\,\\mathrm{°} \\end{aligned}$$" #Display Theta1 & Theta2
    value_plot_angles2.text = "$$\\begin{aligned} \\alpha_1&=" + "{:4.1f}".format(a1) + "\\,\\mathrm{°}\\\\ \\alpha_2&=" + "{:4.1f}".format(a2) + "\\,\\mathrm{°} \\end{aligned}$$" #Display alpha1 & alpha2
    value_plot_tensions.text = "$$\\begin{aligned} T_1&=" + "{:4.1f}".format(T1) + "\\,\\mathrm{N}\\\\ T_2&=" + "{:4.1f}".format(T2) + "\\,\\mathrm{N} \\end{aligned}$$"           #Display T1 & T2

#Slider change call back function for H, c, M, X
def slider_cb_fun(attr,old,new):
    H=H_slider.value
    B=B_slider.value
    c=c_slider.value
    M=M_slider.value
    x=X_slider.value
    
    D=np.sqrt(H*H+B*B) #Height of the support (m)
    L=c*D #Length of the rope (m)
    
    theta_s1= np.arcsin(H/D) #Angle of the support 1
    theta_s2= np.arcsin(B/D) #Angle of the support 2
    W=M*9.81 #Weight of the car (N)
    
    a1=0.0 #alpha1 - angle between the cable and diagonal joining the supports at bottom support
    a2=0.0 #alpha2 - angle between the cable and diagonal joining the supports at top support            

    #Symbolic constants for sympy - a1 & a2
    alpha1=sp.Symbol('alpha1',real=True)
    alpha2=sp.Symbol('alpha2',real=True)        

    #Kinematic equations 
    eq1= sp.Eq(((L-x/sp.cos(theta_s1-alpha1))*sp.sin(theta_s2-alpha2))+x-B,0)
    eq2= sp.Eq((x/sp.cos(theta_s1-alpha1)*sp.sin(alpha1))-((L-x/sp.cos(theta_s1-alpha1))*sp.sin(alpha2)),0)    

    #Simultaneously solving the system of equations numerically
    [a1,a2]=sp.nsolve((eq1,eq2),(alpha1,alpha2),(0.10,0.10))    

    #Effective angles on the Cable
    theta_total1=float(theta_s1-a1) #Actual angle at S1 for a specific car position on the rope
    theta_total2=float(theta_s2+a2) #Actual angle at S2 for a specific car position on the rope
    Lx=x/np.cos(theta_total1) #Length of the bottom cable segement     

    #Tensions on the Cable
    T1= W/(np.sin(theta_total2)-(np.cos(theta_total2)*np.sin(theta_total1)/np.cos(theta_total1)))*(np.cos(theta_total2)/np.cos(theta_total1)) # Rope tension in the bottom
    T2= W/(np.sin(theta_total2)-(np.cos(theta_total2)*np.sin(theta_total1)/np.cos(theta_total1)))  # Rope tension in the top

    #Update the result display
    setValueText(D, L,theta_total1*180/np.pi, theta_total2*180/np.pi, a1*180/np.pi, a2*180/np.pi, T1, T2) 
    #Update the animated plot
    plot.x_range.end=B+150.0 
    plot.y_range.end=H+150.0
    support_source_top.patch( {'x':[(0,B)]} )
    support_source_top.patch( {'y':[(0,H+5.0)]} )
    line_source_bottom.data=dict(xs = [0, Lx * np.cos(theta_total1)], ys =[0, Lx * np.sin(theta_total1)] )
    line_source_top.data=dict(xs = [Lx * np.cos(theta_total1), B], ys =[Lx * np.sin(theta_total1), H] )
    line_source_carriage.data=dict(xs = [Lx * np.cos(theta_total1),Lx * np.cos(theta_total1)], ys= [Lx * np.sin(theta_total1)-70,Lx * np.sin(theta_total1)] )
    mass_source_carriage.data=dict(x = [Lx * np.cos(theta_total1)], y = [Lx * np.sin(theta_total1)-70], size=[int(M/M_max*35)] )
    connecting_pt_circle.data=dict(x = [Lx * np.cos(theta_total1)], y = [ Lx * np.sin(theta_total1)] )
    B_dist_source.patch( {'xE':[(0,B)], 'xL':[(0,0.5*B)]} )
    X_dist_source.patch( {'xE':[(0,x)], 'xL':[(0,0.5*x)]} )
    H_dist_source.patch( {'xS':[(0,B+30)],'xE':[(0,B+30)],'yE':[(0,H)], 'xL':[(0,B+40)], 'yL':[(0,0.5*H)]} )
    D_dist_source.patch( {'xE':[(0,B-60)], 'xL':[(0,0.5*B-70)], 'yE':[(0,H+60)], 'yL':[(0,0.5*H+70)]} )
    T1_source.patch( {'xE':[(0,-5-(np.cos(theta_total1)*150*(T1/(T1+T2))))],'yE':[(0,+5-(np.sin(theta_total1)*150*(T1/(T1+T2))))], 'xL':[(0,-25-0.5*(np.cos(theta_total1)*150*(T1/(T1+T2))))], 'yL':[(0,+15-0.5*(np.sin(theta_total1)*150*(T1/(T1+T2))))]} )
    T2_source.patch( {'xS':[(0,+5+B)],'xE':[(0,+5+B+(np.cos(theta_total2)*150*T2/(T1+T2)))],'yS':[(0,+5+H)],'yE':[(0,+5+H+(np.sin(theta_total2)*150*T2/(T1+T2)))], 'xL':[(0,+35+B+0.5*(np.cos(theta_total2)*150*T2/(T1+T2)))], 'yL':[(0,-10+H+0.5*(np.sin(theta_total2)*150*T2/(T1+T2)))]} )

#Slider change call back function for B    
def slider_cb_fun_b(attr,old,new):
    H=H_slider.value
    B=B_slider.value
    M=M_slider.value
    
    x_old_fraction = (X_slider.value - X_slider.start) / (X_slider.end - X_slider.start)
    X_slider.start=int(0.1*B)
    X_slider.end=int(0.9*B)
    X_slider.value=int(x_old_fraction * (X_slider.end - X_slider.start) + X_slider.start)
    x=int(x_old_fraction * (X_slider.end - X_slider.start) + X_slider.start)
        
    D=np.sqrt(H*H + B*B) #Height of the support (m)
    c=c_slider.value    
    L=c*D #Length of the rope (m)
    
    theta_s1= np.arcsin(H/D) #Angle of the support 1
    theta_s2= np.arcsin(B/D) #Angle of the support 2
    W=M*9.81 #Weight of the car (N)

    a1=0.0 #alpha1 - angle between the cable and diagonal joining the supports at bottom support
    a2=0.0 #alpha2 - angle between the cable and diagonal joining the supports at top support            

    #Symbolic constants for sympy - a1 & a2
    alpha1=sp.Symbol('alpha1',real=True)
    alpha2=sp.Symbol('alpha2',real=True)        

    #Kinematic equations 
    eq1= sp.Eq(((L-x/sp.cos(theta_s1-alpha1))*sp.sin(theta_s2-alpha2))+x-B,0)
    eq2= sp.Eq((x/sp.cos(theta_s1-alpha1)*sp.sin(alpha1))-((L-x/sp.cos(theta_s1-alpha1))*sp.sin(alpha2)),0)    

    #Simultaneously solving the system of equations numerically
    [a1,a2]=sp.nsolve((eq1,eq2),(alpha1,alpha2),(0.10,0.10))    

    #Effective angles on the Cable
    theta_total1=float(theta_s1-a1) #Actual angle at S1 for a specific car position on the rope
    theta_total2=float(theta_s2+a2) #Actual angle at S2 for a specific car position on the rope
    Lx=x/np.cos(theta_total1) #Length of the bottom cable segement     

    #Tensions on the Cable
    T1= W/(np.sin(theta_total2)-(np.cos(theta_total2)*np.sin(theta_total1)/np.cos(theta_total1)))*(np.cos(theta_total2)/np.cos(theta_total1)) # Cable tension in the bottom
    T2= W/(np.sin(theta_total2)-(np.cos(theta_total2)*np.sin(theta_total1)/np.cos(theta_total1)))  # Cable tension in the top

    #Update the result display
    setValueText(D, L,theta_total1*180/np.pi, theta_total2*180/np.pi, a1*180/np.pi, a2*180/np.pi, T1, T2) 
    #Update the animated plot
    plot.x_range.end=B+150.0 
    plot.y_range.end=H+150.0
    support_source_top.patch( {'x':[(0,B)]} )
    support_source_top.patch( {'y':[(0,H+5.0)]} )
    line_source_bottom.data=dict(xs = [0, Lx * np.cos(theta_total1)], ys =[0, Lx * np.sin(theta_total1)] )
    line_source_top.data=dict(xs = [Lx * np.cos(theta_total1), B], ys =[Lx * np.sin(theta_total1), H] )
    line_source_carriage.data=dict(xs = [Lx * np.cos(theta_total1),Lx * np.cos(theta_total1)], ys= [Lx * np.sin(theta_total1)-70,Lx * np.sin(theta_total1)] )
    mass_source_carriage.data=dict(x = [Lx * np.cos(theta_total1)], y = [Lx * np.sin(theta_total1)-70], size=[int(M/M_max*35)] )
    connecting_pt_circle.data=dict(x = [Lx * np.cos(theta_total1)], y = [ Lx * np.sin(theta_total1)] )
    B_dist_source.patch( {'xE':[(0,B)], 'xL':[(0,0.5*B)]} )
    X_dist_source.patch( {'xE':[(0,x)], 'xL':[(0,0.5*x)]} )
    H_dist_source.patch( {'xS':[(0,B+30)],'xE':[(0,B+30)],'yE':[(0,H)], 'xL':[(0,B+40)], 'yL':[(0,0.5*H)]} )
    D_dist_source.patch( {'xE':[(0,B-60)], 'xL':[(0,0.5*B-70)], 'yE':[(0,H+60)], 'yL':[(0,0.5*H+70)]} )
    T1_source.patch( {'xE':[(0,-5-(np.cos(theta_total1)*150*(T1/(T1+T2))))],'yE':[(0,+5-(np.sin(theta_total1)*150*(T1/(T1+T2))))], 'xL':[(0,-25-0.5*(np.cos(theta_total1)*150*(T1/(T1+T2))))], 'yL':[(0,+15-0.5*(np.sin(theta_total1)*150*(T1/(T1+T2))))]} )
    T2_source.patch( {'xS':[(0,+5+B)],'xE':[(0,+5+B+(np.cos(theta_total2)*150*T2/(T1+T2)))],'yS':[(0,+5+H)],'yE':[(0,+5+H+(np.sin(theta_total2)*150*T2/(T1+T2)))], 'xL':[(0,+35+B+0.5*(np.cos(theta_total2)*150*T2/(T1+T2)))], 'yL':[(0,-10+H+0.5*(np.sin(theta_total2)*150*T2/(T1+T2)))]} )


#Call back function for reset button
def callback_reset(event):
    H_slider.value=H
    c_slider.value=c
    B_slider.value=B
    M_slider.value=M
    X_slider.start=0.1*B
    X_slider.end=0.9*B
    X_slider.value=0.5*B    
    x=X_slider.value
    
    D=np.sqrt(H*H+B*B) #Height of the support (m)
    L=c*D #Length of the rope (m)
    
    theta_s1= np.arcsin(H/D) #Angle of the support 1
    theta_s2= np.arcsin(B/D) #Angle of the support 2
    W=M*9.81 #Weight of the car (N)
    a1=0.0 #alpha1 - angle between the cable and diagonal joining the supports at bottom support
    a2=0.0 #alpha2 - angle between the cable and diagonal joining the supports at top support            

    #Symbolic constants for sympy - a1 & a2
    alpha1=sp.Symbol('alpha1',real=True)
    alpha2=sp.Symbol('alpha2',real=True)        

    #Kinematic equations 
    eq1= sp.Eq(((L-x/sp.cos(theta_s1-alpha1))*sp.sin(theta_s2-alpha2))+x-B,0)
    eq2= sp.Eq((x/sp.cos(theta_s1-alpha1)*sp.sin(alpha1))-((L-x/sp.cos(theta_s1-alpha1))*sp.sin(alpha2)),0)    

    #Simultaneously solving the system of equations numerically
    [a1,a2]=sp.nsolve((eq1,eq2),(alpha1,alpha2),(0.10,0.10))    

    #Effective angles on the Cable
    theta_total1=float(theta_s1-a1) #Actual angle at S1 for a specific car position on the rope
    theta_total2=float(theta_s2+a2) #Actual angle at S2 for a specific car position on the rope
    Lx=x/np.cos(theta_total1) #Length of the bottom cable segement     

    #Tensions on the Cable
    T1= W/(np.sin(theta_total2)-(np.cos(theta_total2)*np.sin(theta_total1)/np.cos(theta_total1)))*(np.cos(theta_total2)/np.cos(theta_total1)) # Cable tension in the bottom
    T2= W/(np.sin(theta_total2)-(np.cos(theta_total2)*np.sin(theta_total1)/np.cos(theta_total1)))  # Cable tension in the top

    #Update the result display
    setValueText(D, L,theta_total1*180/np.pi, theta_total2*180/np.pi, a1*180/np.pi, a2*180/np.pi, T1, T2) 
    #Update the animated plot
    plot.x_range.end=B+150.0 
    plot.y_range.end=H+150.0
    support_source_top.patch( {'x':[(0,B)]} )
    support_source_top.patch( {'y':[(0,H+5.0)]} )
    line_source_bottom.data=dict(xs = [0, Lx * np.cos(theta_total1)], ys =[0, Lx * np.sin(theta_total1)] )
    line_source_top.data=dict(xs = [Lx * np.cos(theta_total1), B], ys =[Lx * np.sin(theta_total1), H] )
    line_source_carriage.data=dict(xs = [Lx * np.cos(theta_total1),Lx * np.cos(theta_total1)], ys= [Lx * np.sin(theta_total1)-70,Lx * np.sin(theta_total1)] )
    mass_source_carriage.data=dict(x = [Lx * np.cos(theta_total1)], y = [Lx * np.sin(theta_total1)-70], size=[int(M/M_max*35)] )
    connecting_pt_circle.data=dict(x = [Lx * np.cos(theta_total1)], y = [ Lx * np.sin(theta_total1)] )
    B_dist_source.patch( {'xE':[(0,B)], 'xL':[(0,0.5*B)]} )
    X_dist_source.patch( {'xE':[(0,x)], 'xL':[(0,0.5*x)]} )
    H_dist_source.patch( {'xS':[(0,B+30)],'xE':[(0,B+30)],'yE':[(0,H)], 'xL':[(0,B+40)], 'yL':[(0,0.5*H)]} )
    D_dist_source.patch( {'xE':[(0,B-60)], 'xL':[(0,0.5*B-70)], 'yE':[(0,H+60)], 'yL':[(0,0.5*H+70)]} )
    T1_source.patch( {'xE':[(0,-5-(np.cos(theta_total1)*150*(T1/(T1+T2))))],'yE':[(0,+5-(np.sin(theta_total1)*150*(T1/(T1+T2))))], 'xL':[(0,-25-0.5*(np.cos(theta_total1)*150*(T1/(T1+T2))))], 'yL':[(0,+15-0.5*(np.sin(theta_total1)*150*(T1/(T1+T2))))]} )
    T2_source.patch( {'xS':[(0,+5+B)],'xE':[(0,+5+B+(np.cos(theta_total2)*150*T2/(T1+T2)))],'yS':[(0,+5+H)],'yE':[(0,+5+H+(np.sin(theta_total2)*150*T2/(T1+T2)))], 'xL':[(0,+35+B+0.5*(np.cos(theta_total2)*150*T2/(T1+T2)))], 'yL':[(0,-10+H+0.5*(np.sin(theta_total2)*150*T2/(T1+T2)))]} )
# ----------------------------------------------------------------- #

####################################
##        SLIDERS & BUTTONS       ##
####################################
#Sliders
#Vertical Distance between the supports
H_slider = LatexSlider(title="\\text{Vertical distance between supports (H)}=", value_unit="\\text{m}", value=H, start=H_min, end=H_max, step=1.0, width=400, css_classes=["slider"])
H_slider.on_change('value',slider_cb_fun) # callback function is called when value changes

#Horizontal Distance between the supports
B_slider = LatexSlider(title="\\text{Horizontal distance between supports (B)}=", value_unit="\\text{m}", value=B, start=B_min, end=B_max, step=1.0, width=400, css_classes=["slider"])
B_slider.on_change('value',slider_cb_fun_b) # callback function is called when value changes

#Cable length stretch factor to compute the length of the cable from the distance between the supports 
c_slider = LatexSlider(title="\\text{Cable length stretch factor (c = L/D)}", value=c, start=c_min, end=c_max, step=0.00005, width=400, css_classes=["slider"], show_value=False)
c_slider.on_change('value',slider_cb_fun) # callback function is called when value changes

#Mass carried by the cable car container
M_slider = LatexSlider(title="\\text{Mass carried by the system (M)}=", value_unit="\\text{Kg}", value=M, start=M_min, end=M_max, step=1.0, width=400, css_classes=["slider"])
M_slider.on_change('value',slider_cb_fun) # callback function is called when value changes

#Axial location of the carriage
X_slider = LatexSlider(title="\\text{Horizontal location of the carriage (X)}=", value_unit="\\text{m}", value=int(0.5*B_slider.value), start=int(0.1*B_slider.value), end=int(0.9*B_slider.value), step=1.0, width=400, css_classes=["slider"])
X_slider.on_change('value',slider_cb_fun) # callback function is called when value changes

#Reset Button
button_width = 100
Reset_button=Button(label='Reset', button_type='success', width=button_width)
Reset_button.on_click(callback_reset)
# ----------------------------------------------------------------- #

####################################
##    ANIMATED PLOT               ##
####################################

# Plot
plot = figure(title="", tools="", x_range=(-100,B+150), y_range=(-200,H+150))
plot.toolbar.logo = None
plot.axis.axis_label_text_font_style="normal"
plot.axis.axis_label_text_font_size="14pt"
plot.xaxis.axis_label='X (m)'
plot.yaxis.axis_label='Y (m)'

#Column Data Sources definition
# Support source
support_source_bottom = ColumnDataSource(dict(x = [0], y = [0+5.0] , src = ["Cable_car/static/images/fixed_support.svg"]))
support_source_top    = ColumnDataSource(dict(x = [B], y = [H+5.0] , src = ["Cable_car/static/images/fixed_support.svg"]))

#Line source for the cable
line_source_bottom = ColumnDataSource(dict(xs = [0, Lx * np.cos(theta_total1)], ys =[0, Lx * np.sin(theta_total1)] ))
line_source_top    = ColumnDataSource(dict(xs = [Lx * np.cos(theta_total1), B], ys =[Lx * np.sin(theta_total1), H] ))

# Carriage
line_source_carriage = ColumnDataSource(dict(xs = [Lx * np.cos(theta_total1),Lx * np.cos(theta_total1)], ys= [Lx * np.sin(theta_total1)-70,Lx * np.sin(theta_total1)] ))
mass_source_carriage=ColumnDataSource(dict(x = [Lx * np.cos(theta_total1)], y = [Lx * np.sin(theta_total1)-70], size=[int(M/M_max*35)] ))
connecting_pt_circle=ColumnDataSource(dict(x = [Lx * np.cos(theta_total1)], y = [ Lx * np.sin(theta_total1)] ))

#Annotations 
B_dist_source = ColumnDataSource(dict(xS=[0], xE=[B], yS=[-180], yE=[-180], xL=[B*0.5], yL=[-170], text=["B"]))
X_dist_source = ColumnDataSource(dict(xS=[0], xE=[x], yS=[-125], yE=[-125], xL=[x*0.5], yL=[-115], text=["X"]))
H_dist_source = ColumnDataSource(dict(xS=[B+30], xE=[B+30], yS=[0], yE=[H], xL=[B+40], yL=[0.5*H], text=["H"]))
D_dist_source = ColumnDataSource(dict(xS=[0-60], xE=[B-60], yS=[0+60], yE=[H+60], xL=[B*0.5-70], yL=[H*0.5+70], text=["D"]))

#Cable Tensions & Load
T1_source = ColumnDataSource(dict(xS=[-5], xE=[-5-(np.cos(theta_total1)*150*T1/(T1+T2))], yS=[-5], yE=[-5-(np.sin(theta_total1)*150*T1/(T1+T2))], xL=[-25-0.5*(np.cos(theta_total1)*150*T1/(T1+T2))], yL=[+15-0.5*(np.sin(theta_total1)*150*T1/(T1+T2))], name=["T_1"]))
T2_source =ColumnDataSource(dict(xS=[5+B], xE=[5+B+(np.cos(theta_total2)*150*T2/(T1+T2))], yS=[5+H], yE=[5+H+(np.sin(theta_total2)*150*T2/(T1+T2))], xL=[+35+B+0.5*(np.cos(theta_total2)*150*T2/(T1+T2))], yL=[-10+H+0.5*(np.sin(theta_total2)*150*T2/(T1+T2))], name=["T_2"]))

#Labels and arrows for annotations & cable tensions
B_dist = Arrow(end=TeeHead(line_color="#808080", line_width=1, size=10),
               start=TeeHead(line_color="#808080",line_width=1, size=10),
               x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_width=1, line_color="#808080", source=B_dist_source)
B_dist_label = LatexLabelSet(x='xL', y='yL', text='text', source=B_dist_source)

X_dist = Arrow(end=TeeHead(line_color="#808080", line_width=1, size=10),
               start=TeeHead(line_color="#808080",line_width=1, size=10),
               x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_width=1, line_color="#808080", source=X_dist_source)
X_dist_label = LatexLabelSet(x='xL', y='yL', text='text', source=X_dist_source)

H_dist = Arrow(end=TeeHead(line_color="#808080", line_width=1, size=10),
               start=TeeHead(line_color="#808080",line_width=1, size=10),
               x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_width=1, line_color="#808080", source=H_dist_source)
H_dist_label = LatexLabelSet(x='xL', y='yL', text='text', source=H_dist_source)

D_dist = Arrow(end=TeeHead(line_color="#808080", line_width=1, size=10),
               start=TeeHead(line_color="#808080",line_width=1, size=10),
               x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_width=1, line_color="#808080", source=D_dist_source)
D_dist_label = LatexLabelSet(x='xL', y='yL', text='text', source=D_dist_source)

T1_arrow_glyph = Arrow(end=OpenHead(line_color="#333333", line_width=4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_width=4, source=T1_source,line_color="#333333")

T2_arrow_glyph = Arrow(end=OpenHead(line_color="#333333", line_width=4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_width=4, source=T2_source,line_color="#333333")

T1_label_glyph=LatexLabelSet(x='xL', y='yL', text='name', text_font_size="15pt", level='glyph', source=T1_source)
T2_label_glyph=LatexLabelSet(x='xL', y='yL', text='name', text_font_size="15pt", level='glyph', source=T2_source)

#Adding all glyps into the plot - lines, carriage, supports, tensions & annotations
plot.line(x='xs', y='ys', source=line_source_bottom , line_width=5, color='#3070B3')
plot.line(x='xs', y='ys', source=line_source_top , line_width=5, color='#3070B3')
plot.circle(x='x', y='y', source=connecting_pt_circle, size=10, color="#e37222")
plot.line(x='xs', y='ys', source=line_source_carriage,  line_width=5, color="#e37222")
plot.square(x='x', y='y', size='size', source=mass_source_carriage,  color="#e37222")

plot.add_glyph(support_source_top,ImageURL(url="src", x='x', y='y', w=40, h=40, anchor="top_center"))
plot.add_glyph(support_source_bottom,ImageURL(url="src", x='x', y='y', w=40, h=40, anchor="top_center"))
plot.add_layout(T1_arrow_glyph)
plot.add_layout(T2_arrow_glyph)
plot.add_layout(T1_label_glyph)
plot.add_layout(T2_label_glyph)
plot.add_layout(B_dist)
plot.add_layout(B_dist_label)
plot.add_layout(X_dist)
plot.add_layout(X_dist_label)
plot.add_layout(H_dist)
plot.add_layout(H_dist_label)
plot.add_layout(D_dist)
plot.add_layout(D_dist_label)
# ----------------------------------------------------------------- #

####################################
##        LAYOUT                  ##
#################################### 
curdoc().add_root(column(
    description1,
    figure_kin,
    description2,
    figure_fbd,
    description3,
    row(plot,column(H_slider,
    B_slider,
    c_slider,
    M_slider,
    X_slider,
    Reset_button,
    value_plot_distance_cable_length,
    #value_plot_angles1,
    #value_plot_angles2,
    value_plot_tensions))
    ))

curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
# ----------------------------------------------------------------- #




