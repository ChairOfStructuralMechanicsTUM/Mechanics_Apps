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
import os
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

description_filename2 = join(dirname(__file__), "description2.html") #Part II of the description
description2 = LatexDiv(text=open(description_filename2).read(), render_as_text=False, width=1000)

description_filename3 = join(dirname(__file__), "description3.html") #Part III of the description
description3 = LatexDiv(text=open(description_filename3).read(), render_as_text=False, width=1000)

#Figures_static
# Plot
#Kinematics of the cable car 
kinematics_img=os.path.join(os.path.basename(os.path.dirname(__file__)), "static", "Kinematics.svg")
figure_kin = figure(height=235, width=298)
figure_kin.toolbar.logo = None # do not display the bokeh logo
figure_kin.toolbar_location = None # do not display the tools 
figure_kin.x_range=Range1d(start=0, end=1)
figure_kin.y_range=Range1d(start=0, end=1)
figure_kin.xaxis.visible = None
figure_kin.yaxis.visible = None
figure_kin.xgrid.grid_line_color = None
figure_kin.ygrid.grid_line_color = None
figure_kin.toolbar.active_drag = None
figure_kin.toolbar.active_scroll = None
figure_kin.toolbar.active_tap = None
kinematics_src = ColumnDataSource(dict(url = [kinematics_img]))
figure_kin.image_url(url='url', x=0, y = 1, h=1, w=1, source=kinematics_src)
figure_kin.outline_line_alpha = 0 

# Free boy diagram of the cable car
fbd_img=os.path.join(os.path.basename(os.path.dirname(__file__)), "static", "Free_Body_Diagram.svg")
figure_fbd = figure(height=385, width=450)
figure_fbd.toolbar.logo = None # do not display the bokeh logo
figure_fbd.toolbar_location = None # do not display the tools 
figure_fbd.x_range=Range1d(start=0, end=1)
figure_fbd.y_range=Range1d(start=0, end=1)
figure_fbd.xaxis.visible = None
figure_fbd.yaxis.visible = None
figure_fbd.xgrid.grid_line_color = None
figure_fbd.ygrid.grid_line_color = None
figure_fbd.toolbar.active_drag = None
figure_fbd.toolbar.active_scroll = None
figure_fbd.toolbar.active_tap = None
fbd_src = ColumnDataSource(dict(url = [fbd_img]))
figure_fbd.image_url(url='url', x=0, y = 1, h=1, w=1, source=fbd_src)
figure_fbd.outline_line_alpha = 0 



#################################
##        INITIALIZATION       ##
#################################

# Initial parameters & its limits
# Cable car dimensions & user inputs
H_max =525.0 #Verical distance between the supports (m) -H
H_min= 475.0
H=500.0

B_max=525.0 #Horizontal distance between the supports (m) -B
B_min=475.0
B=500.0

c_max=1.9  #Cable length stretch factor -c
c_min=1.00001
c=(c_min+c_max)/2

M_max=300.0 #Mass of the cable car - M (Kg)
M_min=200.0 
M=250.0

x=0.55*B #Axial location of the cable car
D=np.sqrt(H*H+B*B) #Diagonal distance between the supports (m)
L=c*D #Length of the cable (m) - cable length should be always higher than the distance between the supports
W=M*9.81 #Weight of the car (N)

#Symbolic constants
theta1=sp.Symbol('theta1',real=True)
theta2=sp.Symbol('theta2',real=True)         

#Kinematic equations
eq1= sp.Eq(((L-x/sp.cos(theta1))*sp.cos(theta2))+x-B,0)
eq2= sp.Eq(((x/sp.cos(theta1))*sp.sin(theta1))+((L-x/sp.cos(theta1))*sp.sin(theta2))-H,0)
    
#Solving the system of equations numerically
[t1,t2]=sp.nsolve((eq1,eq2),(theta1,theta2),(0.25,0.75))  

#Effective angles on the Cable
theta_total1=float(t1) #Actual angle at S1 for a specific car position on the rope
theta_total2=float(t2) #Actual angle at S2 for a specific car position on the rope
Lx=x/np.cos(theta_total1) #Length of the bottom cable segement     

#Tensions on the Cable
T1= W/(np.sin(theta_total2)-(np.cos(theta_total2)*np.sin(theta_total1)/np.cos(theta_total1)))*(np.cos(theta_total2)/np.cos(theta_total1)) # Cable tension in the bottom
T2= W/(np.sin(theta_total2)-(np.cos(theta_total2)*np.sin(theta_total1)/np.cos(theta_total1)))  # Cable tension in the top
# ----------------------------------------------------------------- #

#################################
##     CALLBACK FUNCTIONS      ##
#################################

# Div to show tension and distance values
value_plot_distance_cable_length= LatexDiv(text="", render_as_text=False, width=400)
value_plot_angles = LatexDiv(text="", render_as_text=False, width=400)
value_plot_tensions = LatexDiv(text="", render_as_text=False, width=400)

#Display the results
def setValueText(D,L,t1,t2,T1,T2):
    value_plot_distance_cable_length.text = "$$\\begin{aligned} D&=" + "{:4.1f}".format(D) + "\\,\\mathrm{m}\\\\ L&=" + "{:4.1f}".format(L) + "\\,\\mathrm{m} \\end{aligned}$$"    #Display the D & L
    value_plot_angles.text = "$$\\begin{aligned} \\theta_1&=" + "{:4.1f}".format((t1)) + "\\,\\mathrm{°}\\\\ \\theta_2&=" + "{:4.1f}".format(t2) + "\\,\\mathrm{°} \\end{aligned}$$" #Display Theta1 & Theta2
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
    W=M*9.81 #Weight of the car (N)
    
    #Symbolic constants
    theta1=sp.Symbol('theta1',real=True)
    theta2=sp.Symbol('theta2',real=True)         

    #Kinematic equations
    eq1= sp.Eq(((L-x/sp.cos(theta1))*sp.cos(theta2))+x-B,0)
    eq2= sp.Eq(((x/sp.cos(theta1))*sp.sin(theta1))+((L-x/sp.cos(theta1))*sp.sin(theta2))-H,0)
    
    #Solving the system of equations numerically
    [t1,t2]=sp.nsolve((eq1,eq2),(theta1,theta2),(0.25,0.75))    

    #Effective angles on the Cable
    theta_total1=float(t1) #Actual angle at S1 for a specific car position on the rope
    theta_total2=float(t2) #Actual angle at S2 for a specific car position on the rope
    Lx=x/np.cos(theta_total1) #Length of the bottom cable segement     

    #Tensions on the Cable
    T1= W/(np.sin(theta_total2)-(np.cos(theta_total2)*np.sin(theta_total1)/np.cos(theta_total1)))*(np.cos(theta_total2)/np.cos(theta_total1)) # Rope tension in the bottom
    T2= W/(np.sin(theta_total2)-(np.cos(theta_total2)*np.sin(theta_total1)/np.cos(theta_total1)))  # Rope tension in the top

    #Update the result display
    setValueText(D, L,theta_total1*180/np.pi, theta_total2*180/np.pi, T1, T2) 
    #Update the animated plot
    plot.x_range.end=B+200.0
    plot.y_range.start=min (-200,Lx * np.sin(theta_total1)-320)
    plot.y_range.end=H+150.0
    support_source_top.patch( {'x':[(0,B)]} )
    support_source_top.patch( {'y':[(0,H+5.0)]} )
    line_source_bottom.data=dict(xs = [0, Lx * np.cos(theta_total1)], ys =[0, Lx * np.sin(theta_total1)] )
    line_source_top.data=dict(xs = [Lx * np.cos(theta_total1), B], ys =[Lx * np.sin(theta_total1), H] )
    line_source_carriage.data=dict(xs = [Lx * np.cos(theta_total1),Lx * np.cos(theta_total1)], ys= [Lx * np.sin(theta_total1)-120,Lx * np.sin(theta_total1)] )
    mass_source_carriage.data=dict(x = [Lx * np.cos(theta_total1)], y = [Lx * np.sin(theta_total1)-120], size=[int(M/M_max*80)] )
    connecting_pt_circle.data=dict(x = [Lx * np.cos(theta_total1)], y = [ Lx * np.sin(theta_total1)] )
    x_pt_circle.data=dict(x = [Lx * np.cos(theta_total1)], y = [min(-200+25,Lx * np.sin(theta_total1)-320+25)] )
    y_pt_circle.data=dict(x = [-150+15], y = [ Lx * np.sin(theta_total1)] )
    B_dist_source.patch( {'xE':[(0,B)], 'yS':[(0,min(-150,Lx * np.sin(theta_total1)-270))], 'yE':[(0,min(-150,Lx * np.sin(theta_total1)-270))], 'xL':[(0,0.5*B)],'yL':[(0,min(-140,Lx * np.sin(theta_total1)-260))]} )
    H_dist_source.patch( {'xS':[(0,B+100)],'xE':[(0,B+100)],'yE':[(0,H)], 'xL':[(0,B+70)], 'yL':[(0,0.5*H)]} )
    D_dist_source.patch( {'xE':[(0,B-20)], 'xL':[(0,0.5*B-30)], 'yE':[(0,H+10)], 'yL':[(0,0.5*H+30)]} )
    T1_source.patch( {'xE':[(0,-(np.cos(theta_total1)*150*(T1/(T1+T2))))],'yE':[(0,-(np.sin(theta_total1)*150*(T1/(T1+T2))))], 'xL':[(0,-50-0.5*(np.cos(theta_total1)*150*(T1/(T1+T2))))], 'yL':[(0,-50-0.5*(np.sin(theta_total1)*150*(T1/(T1+T2))))]} )
    T2_source.patch( {'xS':[(0,B)],'xE':[(0,B+(np.cos(theta_total2)*150*T2/(T1+T2)))],'yS':[(0,H)],'yE':[(0,H+(np.sin(theta_total2)*150*T2/(T1+T2)))], 'xL':[(0,+25+B+0.5*(np.cos(theta_total2)*150*T2/(T1+T2)))], 'yL':[(0,-25+H+0.5*(np.sin(theta_total2)*150*T2/(T1+T2)))]} )

#Slider change call back function for B    
def slider_cb_fun_b(attr,old,new):
    H=H_slider.value
    B=B_slider.value
    M=M_slider.value
    
    x_old_fraction = (X_slider.value - X_slider.start) / (X_slider.end - X_slider.start)
    X_slider.start=int(0.2*B)
    X_slider.end=int(0.9*B)
    X_slider.value=int(x_old_fraction * (X_slider.end - X_slider.start) + X_slider.start)
    x=int(x_old_fraction * (X_slider.end - X_slider.start) + X_slider.start)
        
    D=np.sqrt(H*H + B*B) #Height of the support (m)
    c=c_slider.value    
    L=c*D #Length of the rope (m)
    W=M*9.81 #Weight of the car (N)
    
    #Symbolic constants
    theta1=sp.Symbol('theta1',real=True)
    theta2=sp.Symbol('theta2',real=True)         

    #Kinematic equations
    eq1= sp.Eq(((L-x/sp.cos(theta1))*sp.cos(theta2))+x-B,0)
    eq2= sp.Eq(((x/sp.cos(theta1))*sp.sin(theta1))+((L-x/sp.cos(theta1))*sp.sin(theta2))-H,0)
    
    #Solving the system of equations numerically
    [t1,t2]=sp.nsolve((eq1,eq2),(theta1,theta2),(0.25,0.75))    

    #Effective angles on the Cable
    theta_total1=float(t1) #Actual angle at S1 for a specific car position on the rope
    theta_total2=float(t2) #Actual angle at S2 for a specific car position on the rope
    Lx=x/np.cos(theta_total1) #Length of the bottom cable segement     

    #Tensions on the Cable
    T1= W/(np.sin(theta_total2)-(np.cos(theta_total2)*np.sin(theta_total1)/np.cos(theta_total1)))*(np.cos(theta_total2)/np.cos(theta_total1)) # Rope tension in the bottom
    T2= W/(np.sin(theta_total2)-(np.cos(theta_total2)*np.sin(theta_total1)/np.cos(theta_total1)))  # Rope tension in the top

    #Update the result display
    setValueText(D, L,theta_total1*180/np.pi, theta_total2*180/np.pi, T1, T2) 
    
    #Update the animated plot
    plot.x_range.end=B+200.0 
    plot.y_range.start=min (-200,Lx * np.sin(theta_total1)-320)
    plot.y_range.end=H+150.0
    support_source_top.patch( {'x':[(0,B)]} )
    support_source_top.patch( {'y':[(0,H+5.0)]} )
    line_source_bottom.data=dict(xs = [0, Lx * np.cos(theta_total1)], ys =[0, Lx * np.sin(theta_total1)] )
    line_source_top.data=dict(xs = [Lx * np.cos(theta_total1), B], ys =[Lx * np.sin(theta_total1), H] )
    line_source_carriage.data=dict(xs = [Lx * np.cos(theta_total1),Lx * np.cos(theta_total1)], ys= [Lx * np.sin(theta_total1)-120,Lx * np.sin(theta_total1)] )
    mass_source_carriage.data=dict(x = [Lx * np.cos(theta_total1)], y = [Lx * np.sin(theta_total1)-120], size=[int(M/M_max*80)] )
    connecting_pt_circle.data=dict(x = [Lx * np.cos(theta_total1)], y = [ Lx * np.sin(theta_total1)] )
    x_pt_circle.data=dict(x = [Lx * np.cos(theta_total1)], y = [min(-200+25,Lx * np.sin(theta_total1)-320+25)] )
    y_pt_circle.data=dict(x = [-150+15], y = [ Lx * np.sin(theta_total1)] )
    B_dist_source.patch( {'xE':[(0,B)], 'yS':[(0,min(-150,Lx * np.sin(theta_total1)-270))], 'yE':[(0,min(-150,Lx * np.sin(theta_total1)-270))], 'xL':[(0,0.5*B)],'yL':[(0,min(-140,Lx * np.sin(theta_total1)-260))]} )
    H_dist_source.patch( {'xS':[(0,B+100)],'xE':[(0,B+100)],'yE':[(0,H)], 'xL':[(0,B+70)], 'yL':[(0,0.5*H)]} )
    D_dist_source.patch( {'xE':[(0,B-20)], 'xL':[(0,0.5*B-30)], 'yE':[(0,H+10)], 'yL':[(0,0.5*H+30)]} )
    T1_source.patch( {'xE':[(0,-(np.cos(theta_total1)*150*(T1/(T1+T2))))],'yE':[(0,-(np.sin(theta_total1)*150*(T1/(T1+T2))))], 'xL':[(0,-50-0.5*(np.cos(theta_total1)*150*(T1/(T1+T2))))], 'yL':[(0,-50-0.5*(np.sin(theta_total1)*150*(T1/(T1+T2))))]} )
    T2_source.patch( {'xS':[(0,B)],'xE':[(0,B+(np.cos(theta_total2)*150*T2/(T1+T2)))],'yS':[(0,H)],'yE':[(0,H+(np.sin(theta_total2)*150*T2/(T1+T2)))], 'xL':[(0,+25+B+0.5*(np.cos(theta_total2)*150*T2/(T1+T2)))], 'yL':[(0,-25+H+0.5*(np.sin(theta_total2)*150*T2/(T1+T2)))]} )


#Call back function for reset button
def callback_reset(event):
    H_slider.value=H
    c_slider.value=c
    B_slider.value=B
    M_slider.value=M
    X_slider.start=0.2*B
    X_slider.end=0.9*B
    X_slider.value=0.55*B    
    x=X_slider.value
    
    D=np.sqrt(H*H+B*B) #Height of the support (m)
    L=c*D #Length of the rope (m)
    W=M*9.81 #Weight of the car (N)
    
    #Symbolic constants
    theta1=sp.Symbol('theta1',real=True)
    theta2=sp.Symbol('theta2',real=True)         

    #Kinematic equations
    eq1= sp.Eq(((L-x/sp.cos(theta1))*sp.cos(theta2))+x-B,0)
    eq2= sp.Eq(((x/sp.cos(theta1))*sp.sin(theta1))+((L-x/sp.cos(theta1))*sp.sin(theta2))-H,0)
    
    #Solving the system of equations numerically
    [t1,t2]=sp.nsolve((eq1,eq2),(theta1,theta2),(0.25,0.75))    

    #Effective angles on the Cable
    theta_total1=float(t1) #Actual angle at S1 for a specific car position on the rope
    theta_total2=float(t2) #Actual angle at S2 for a specific car position on the rope
    Lx=x/np.cos(theta_total1) #Length of the bottom cable segement     

    #Tensions on the Cable
    T1= W/(np.sin(theta_total2)-(np.cos(theta_total2)*np.sin(theta_total1)/np.cos(theta_total1)))*(np.cos(theta_total2)/np.cos(theta_total1)) # Rope tension in the bottom
    T2= W/(np.sin(theta_total2)-(np.cos(theta_total2)*np.sin(theta_total1)/np.cos(theta_total1)))  # Rope tension in the top

    #Update the result display
    setValueText(D, L,theta_total1*180/np.pi, theta_total2*180/np.pi, T1, T2) 
    
    #Update the animated plot
    plot.x_range.end=B+200.0 
    plot.y_range.start=min (-200,Lx * np.sin(theta_total1)-320)
    plot.y_range.end=H+150.0
    support_source_top.patch( {'x':[(0,B)]} )
    support_source_top.patch( {'y':[(0,H+5.0)]} )
    line_source_bottom.data=dict(xs = [0, Lx * np.cos(theta_total1)], ys =[0, Lx * np.sin(theta_total1)] )
    line_source_top.data=dict(xs = [Lx * np.cos(theta_total1), B], ys =[Lx * np.sin(theta_total1), H] )
    line_source_carriage.data=dict(xs = [Lx * np.cos(theta_total1),Lx * np.cos(theta_total1)], ys= [Lx * np.sin(theta_total1)-120,Lx * np.sin(theta_total1)] )
    mass_source_carriage.data=dict(x = [Lx * np.cos(theta_total1)], y = [Lx * np.sin(theta_total1)-120], size=[int(M/M_max*80)] )
    connecting_pt_circle.data=dict(x = [Lx * np.cos(theta_total1)], y = [ Lx * np.sin(theta_total1)] )
    x_pt_circle.data=dict(x = [Lx * np.cos(theta_total1)], y = [min(-200+25,Lx * np.sin(theta_total1)-320+25)] )
    y_pt_circle.data=dict(x = [-150+15], y = [ Lx * np.sin(theta_total1)] )
    B_dist_source.patch( {'xE':[(0,B)], 'yS':[(0,min(-150,Lx * np.sin(theta_total1)-270))], 'yE':[(0,min(-150,Lx * np.sin(theta_total1)-270))], 'xL':[(0,0.5*B)],'yL':[(0,min(-140,Lx * np.sin(theta_total1)-260))]} )
    H_dist_source.patch( {'xS':[(0,B+100)],'xE':[(0,B+100)],'yE':[(0,H)], 'xL':[(0,B+70)], 'yL':[(0,0.5*H)]} )
    D_dist_source.patch( {'xE':[(0,B-20)], 'xL':[(0,0.5*B-30)], 'yE':[(0,H+10)], 'yL':[(0,0.5*H+30)]} )
    T1_source.patch( {'xE':[(0,-(np.cos(theta_total1)*150*(T1/(T1+T2))))],'yE':[(0,-(np.sin(theta_total1)*150*(T1/(T1+T2))))], 'xL':[(0,-50-0.5*(np.cos(theta_total1)*150*(T1/(T1+T2))))], 'yL':[(0,-50-0.5*(np.sin(theta_total1)*150*(T1/(T1+T2))))]} )
    T2_source.patch( {'xS':[(0,B)],'xE':[(0,B+(np.cos(theta_total2)*150*T2/(T1+T2)))],'yS':[(0,H)],'yE':[(0,H+(np.sin(theta_total2)*150*T2/(T1+T2)))], 'xL':[(0,+25+B+0.5*(np.cos(theta_total2)*150*T2/(T1+T2)))], 'yL':[(0,-25+H+0.5*(np.sin(theta_total2)*150*T2/(T1+T2)))]} )
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
c_slider = LatexSlider(title="\\text{Cable length stretch factor (c = L/D)}=", value=float("{:.5f}".format((c))), start=c_min, end=c_max, step=0.005, width=400, css_classes=["slider"])
c_slider.on_change('value',slider_cb_fun) # callback function is called when value changes

#Mass carried by the cable car container
M_slider = LatexSlider(title="\\text{Mass carried by the system (M)}=", value_unit="\\text{Kg}", value=M, start=M_min, end=M_max, step=1.0, width=400, css_classes=["slider"])
M_slider.on_change('value',slider_cb_fun) # callback function is called when value changes

#Axial location of the carriage
X_slider = LatexSlider(title="\\text{Horizontal location of the carriage (X)}=", value_unit="\\text{m}", value=int(0.55*B_slider.value), start=int(0.2*B_slider.value), end=int(0.9*B_slider.value), step=1.0, width=400, css_classes=["slider"])
X_slider.on_change('value',slider_cb_fun) # callback function is called when value changes

#Reset Button
button_width = 400
Reset_button=Button(label='Reset', button_type='success', width=button_width)
Reset_button.on_click(callback_reset)
# ----------------------------------------------------------------- #

####################################
##    ANIMATED PLOT               ##
####################################

# Plot
plot = figure(title="", tools="", x_range=(-150,B+200), y_range=(min(-200,Lx * np.sin(theta_total1)-320),H+150),aspect_scale=2.0)
plot.plot_height=700
plot.plot_width=850
plot.toolbar.logo = None
plot.axis.axis_label_text_font_style="normal"
plot.axis.axis_label_text_font_size="14pt"
plot.axis.major_label_text_font_size="14pt"
plot.xaxis.axis_label='x (m)'
plot.yaxis.axis_label='y (m)'
plot.outline_line_width=1.5
plot.outline_line_color="#333333"
plot.outline_line_alpha=0.9

#Column Data Sources definition
# Support source
support_source_bottom = ColumnDataSource(dict(x = [0], y = [0+10.0] , src = [os.path.join(os.path.basename(os.path.dirname(__file__)), "static", "fixed_support.svg")]))
support_source_top    = ColumnDataSource(dict(x = [B], y = [H+5.0] , src = [os.path.join(os.path.basename(os.path.dirname(__file__)), "static", "fixed_support.svg")]))

#Line source for the cable
line_source_bottom = ColumnDataSource(dict(xs = [0, Lx * np.cos(theta_total1)], ys =[0, Lx * np.sin(theta_total1)] ))
line_source_top    = ColumnDataSource(dict(xs = [Lx * np.cos(theta_total1), B], ys =[Lx * np.sin(theta_total1), H] ))

# Carriage
line_source_carriage = ColumnDataSource(dict(xs = [Lx * np.cos(theta_total1),Lx * np.cos(theta_total1)], ys= [Lx * np.sin(theta_total1)-120,Lx * np.sin(theta_total1)] ))
mass_source_carriage=ColumnDataSource(dict(x = [Lx * np.cos(theta_total1)], y = [Lx * np.sin(theta_total1)-120], size=[int(M/M_max*80)] ))
connecting_pt_circle=ColumnDataSource(dict(x = [Lx * np.cos(theta_total1)], y = [ Lx * np.sin(theta_total1)] ))

#Annotations 
B_dist_source = ColumnDataSource(dict(xS=[0], xE=[B], yS=[min(-200+50,Lx * np.sin(theta_total1)-320+50)], yE=[min(-200+50,Lx * np.sin(theta_total1)-320+50)], xL=[B*0.5], yL=[min(-200+60,Lx * np.sin(theta_total1)-320+60)], text=["B"]))
H_dist_source = ColumnDataSource(dict(xS=[B+100], xE=[B+100], yS=[0], yE=[H], xL=[B+70], yL=[0.5*H], text=["H"]))
D_dist_source = ColumnDataSource(dict(xS=[+0], xE=[B-20], yS=[0+30], yE=[H+10], xL=[B*0.5-30], yL=[H*0.5+30], text=["D"]))
x_pt_circle=ColumnDataSource(dict(x = [Lx * np.cos(theta_total1)], y = [min(-200+25,Lx * np.sin(theta_total1)-320+25)] ))
y_pt_circle=ColumnDataSource(dict(x = [-150+15], y = [ Lx * np.sin(theta_total1)] ))

#Cable Tensions & Load
T1_source = ColumnDataSource(dict(xS=[0], xE=[-(np.cos(theta_total1)*150*T1/(T1+T2))], yS=[0], yE=[-(np.sin(theta_total1)*150*T1/(T1+T2))], xL=[-50-0.5*(np.cos(theta_total1)*150*T1/(T1+T2))], yL=[-50-0.5*(np.sin(theta_total1)*150*T1/(T1+T2))], name=["T_1"]))
T2_source =ColumnDataSource(dict(xS=[B], xE=[B+(np.cos(theta_total2)*150*T2/(T1+T2))], yS=[H], yE=[H+(np.sin(theta_total2)*150*T2/(T1+T2))], xL=[+25+B+0.5*(np.cos(theta_total2)*150*T2/(T1+T2))], yL=[-25+H+0.5*(np.sin(theta_total2)*150*T2/(T1+T2))], name=["T_2"]))

#Labels and arrows for annotations & cable tensions
B_dist = Arrow(end=TeeHead(line_color="#808080", line_width=1, size=10),
               start=TeeHead(line_color="#808080",line_width=1, size=10),
               x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_width=1, line_color="#808080", source=B_dist_source)
B_dist_label = LatexLabelSet(x='xL', y='yL', text='text', source=B_dist_source)

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
plot.line(x='xs', y='ys', source=line_source_bottom , line_width=10, color='#3070B3')
plot.line(x='xs', y='ys', source=line_source_top , line_width=10, color='#3070B3')
plot.circle(x='x', y='y', source=connecting_pt_circle, size=20, color="#e37222")
plot.line(x='xs', y='ys', source=line_source_carriage,  line_width=10, color="#e37222")
plot.square(x='x', y='y', size='size', source=mass_source_carriage,  color="#e37222")
plot.circle(x='x', y='y', source=x_pt_circle, size=20, color="#a2ad00")
plot.circle(x='x', y='y', source=y_pt_circle, size=20, color="#a2ad00")

plot.add_glyph(support_source_top,ImageURL(url="src", x='x', y='y', w=60, h=60, anchor="top_center"))
plot.add_glyph(support_source_bottom,ImageURL(url="src", x='x', y='y', w=60, h=60, anchor="top_center"))
plot.add_layout(T1_arrow_glyph)
plot.add_layout(T2_arrow_glyph)
plot.add_layout(T1_label_glyph)
plot.add_layout(T2_label_glyph)
plot.add_layout(B_dist)
plot.add_layout(B_dist_label)
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
    column(column(
    row(H_slider,B_slider,c_slider),
    row(M_slider,X_slider,Reset_button),
    row(plot),
    row(value_plot_distance_cable_length,value_plot_angles, value_plot_tensions)
    ))))

curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
# ----------------------------------------------------------------- #




