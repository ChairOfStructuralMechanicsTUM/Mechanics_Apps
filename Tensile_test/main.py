from __future__ import division
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import Slider, Button, Div, Arrow, OpenHead, Range1d, Label, Select, ColumnDataSource, NormalHead, LabelSet
from os.path import dirname, join, split
import numpy as np
from numpy import linspace, loadtxt

from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv, LatexSlider, LatexLabel, LatexLabelSet

## set up data sources for movable objects ##
#     data sources for drawing
top_of_sample_source = ColumnDataSource(data=dict(x=[], y=[]))
bottom_of_sample_source = ColumnDataSource(data=dict(x=[], y=[]))
top_of_mounting_source = ColumnDataSource(data=dict(x=[], y=[]))
top_line_source = ColumnDataSource(data=dict(x=[], y=[]))
top_force_arrow_source = ColumnDataSource(data=dict(xS=[], yS=[], xE=[], yE=[]))
top_force_label_source = ColumnDataSource(data=dict(x=[], y=[], F=[]))
stress_strain_source = ColumnDataSource(data=dict(eps=[], sig=[]))
stress_strain_true_source = ColumnDataSource(data=dict(eps=[], sig=[]))
white_patch_left_source = ColumnDataSource(data=dict(x=[], y=[]))
white_patch_right_source = ColumnDataSource(data=dict(x=[], y=[]))
glob_callback_id = ColumnDataSource(data = dict(callback_id = [None]))
L_arrow_source = ColumnDataSource(data=dict(xS=[], yS=[], xE=[], yE=[]))
S_arrow_source = ColumnDataSource(data=dict(xS=[], yS=[], xE=[], yE=[]))
L_label_source = ColumnDataSource(data=dict(x=[], y=[], L=[]))
S_label_source = ColumnDataSource(data=dict(x=[], y=[], S=[]))
S_multiline_source = ColumnDataSource(data=dict(xs=[], ys=[]))
R_m_source = ColumnDataSource(data=dict(x=[], y=[]))
R3_label_source = ColumnDataSource(data=dict(x=[], y=[], R=[]))
m_label_source = ColumnDataSource(data=dict(x=[], y=[], m=[]))
A_source = ColumnDataSource(data=dict(x=[], y=[]))
A3_label_source = ColumnDataSource(data=dict(x=[], y=[], A=[]))
A_t_source = ColumnDataSource(data=dict(x=[], y=[]))
A4_label_source = ColumnDataSource(data=dict(x=[], y=[], A=[]))
t_label_source = ColumnDataSource(data=dict(x=[], y=[], t=[]))


steel_data_eps = linspace(0, 13, num=131)
rubber_data_eps = linspace(0, 16, num=161)
cfrp_data_eps = linspace(0, 4, num=41)

steel_data_sig = loadtxt('Tensile_test/steel_data_sig.txt')
steel_data_true_sig = loadtxt('Tensile_test/steel_data_true_sig.txt')
rubber_data_sig = loadtxt('Tensile_test/rubber_data_sig.txt')
cfrp_data_sig = loadtxt('Tensile_test/cfrp_data_sig.txt')

def changeMaterial(attr,old,new):
    reset()
    if new == "Steel":
        x_R_m = [0, 7.5]
        y_R_m = [7, 7]
        x_R3 = [0.5]
        y_R3 = [7.1]
        x_m = [0.8]
        y_m = [7]
        x_A = [10.7, 13]
        y_A = [-0.93, 5.07]
        x_A3 = [10.7]
        y_A3 = [0.2]
        x_A_t = [13, 13]
        y_A_t = [0, 5.07]
        x_A4 = [12.4]
        y_A4 = [0.2]
        x_t = [12.7]
        y_t = [0.1]
    elif new == "CFRP":
        x_R_m = [0, 4]
        y_R_m = [9.37, 9.37]
        x_R3 = [0.5]
        y_R3 = [9.47]
        x_m = [0.8]
        y_m = [9.37]
        x_A = [1, 4]
        y_A = [-1.13, 9.37]
        x_A3 = [1.5]
        y_A3 = [0.2]
        x_A_t = [4, 4]
        y_A_t = [0, 9.37]
        x_A4 = [3.4]
        y_A4 = [0.2]
        x_t = [3.7]
        y_t = [0.1]
    elif new == "Rubber":
        x_R_m = [0, 16]
        y_R_m = [3.82, 3.82]
        x_R3 = [0.5]
        y_R3 = [3.92]
        x_m = [0.8]
        y_m = [3.82]
        x_A_t = [16, 16]
        y_A_t = [0, 3.82]
        x_A4 = [15.4]
        y_A4 = [0.2]
        x_t = [15.7]
        y_t = [0.1]
        R_m_source.data = dict(x=x_R_m, y=y_R_m)
        R3_label_source.data = dict(x=x_R3, y=y_R3, R=["R"])
        m_label_source.data = dict(x=x_m, y=y_m, m=["m"])
        A_t_source.data = dict(x=x_A_t, y=y_A_t)
        A4_label_source.data = dict(x=x_A4, y=y_A4, A=["A"])
        t_label_source.data = dict(x=x_t, y=y_t, t=["t"])
    if new == "CFRP" or new == "Steel":
        R_m_source.data = dict(x=x_R_m, y=y_R_m)
        R3_label_source.data = dict(x=x_R3, y=y_R3, R=["R"])
        m_label_source.data = dict(x=x_m, y=y_m, m=["m"])
        A_source.data = dict(x=x_A, y=y_A)
        A3_label_source.data = dict(x=x_A3, y=y_A3, A=["A"])
        A_t_source.data = dict(x=x_A_t, y=y_A_t)
        A4_label_source.data = dict(x=x_A4, y=y_A4, A=["A"])
        t_label_source.data = dict(x=x_t, y=y_t, t=["t"])
        

material_select = Select(title="Material:", value="Steel",
    options=["Steel","Rubber", "CFRP"], width = 100)
material_select.on_change('value',changeMaterial)

## add app description
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)

def init():
    x_mounting = [1, 4, 4, 3, 2, 1]
    y_mounting = [10, 10, 9, 8, 8, 9]
    x_line = [-1, 6]
    y_line = [8, 8]
    xS=[2.5]
    xE=[2.5]
    yS=[9]
    yE=[11]
    xS_L=[0]
    xE_L=[0]
    yS_L=[3]
    yE_L=[8]
    xS_S=[2]
    xE_S=[3]
    yS_S=[5]
    yE_S=[5]
    x_left = [1, 2, 2, 1]
    x_right = [3, 4, 4, 3]
    y = [3, 3, 15, 15]
    x_F= [2.7]
    y_F = [10.1]
    x_L = [-0.5]
    y_L = [5.1]
    x_S = [2.35]
    y_S = [4.3]
    xs = [[2, 2], [3, 3]]
    ys = [[4.8, 5.2], [4.8, 5.2]]
    if material_select.value == "Steel":
        x_sample = [2, 3, 3, 2.875, 2.65, 2.35, 2.125, 2]
        y_sample_top = [8, 8, 4.25, 4.25, 3.25, 3.25, 4.25, 4.25]
        y_sample_bottom = [3, 3, 6.75, 6.75, 7.75, 7.75, 6.75, 6.75]
    elif material_select.value == "Rubber":
        x_sample = [2, 3, 3, 2]
        y_sample_top = [8, 8, 2, 2]
        y_sample_bottom = [3, 3, 9, 9]
    elif material_select.value == "CFRP":
        x_sample = [2, 3, 3, 2]
        y_sample_top = [8, 8, 4.5, 4.5]
        y_sample_bottom = [3, 3, 6.5, 6.5]
    top_of_mounting_source.data = dict(x=x_mounting, y=y_mounting)
    top_of_sample_source.data = dict(x=x_sample, y=y_sample_top)
    bottom_of_sample_source.data = dict(x=x_sample, y=y_sample_bottom)
    top_line_source.data = dict(x=x_line, y=y_line)
    top_force_arrow_source.stream(dict(xS=xS, yS=yS, xE=xE, yE=yE), rollover=1)
    stress_strain_source.data = dict(eps=[], sig=[])
    stress_strain_true_source.data = dict(eps=[], sig=[])
    white_patch_left_source.data = dict(x=x_left, y=y)
    white_patch_right_source.data = dict(x=x_right, y=y) 
    top_force_label_source.data = dict(x=x_F, y=y_F, F=["F"])
    L_arrow_source.stream(dict(xS=xS_L, yS=yS_L, xE=xE_L, yE=yE_L), rollover=1)
    L_label_source.data = dict(x=x_L, y=y_L, L=["L"])
    S_arrow_source.stream(dict(xS=xS_S, yS=yS_S, xE=xE_S, yE=yE_S), rollover=1)
    S_label_source.data = dict(x=x_S, y=y_S, S=["S"])
    S_multiline_source.data = dict(xs=xs, ys=ys)

    R_eH.visible = False
    R1_label.visible = False
    eH_label.visible = False
    R_eL.visible = False
    R2_label.visible = False
    eL_label.visible = False
    R_m.visible = False
    R3_label.visible = False
    m_label.visible = False
    A_L.visible = False
    A1_label.visible = False
    L_label.visible = False
    A_g.visible = False
    A2_label.visible = False
    g_label.visible = False
    A.visible = False
    A3_label.visible = False
    A_t.visible = False
    A4_label.visible = False
    t_label.visible = False
    R_p.visible = False
    R4_label.visible = False
    p_label.visible = False
    A_p.visible = False
    A_p_label.visible = False


    

i = 1
dx = 0
dL = 0
glob_i = ColumnDataSource(data=dict(i=[i]))
glob_dx = ColumnDataSource(data=dict(dx=[dx]))
glob_dL = ColumnDataSource(data=dict(dL=[dL]))

def evolve():
    [i] = glob_i.data["i"]
    [dx] = glob_dx.data["dx"]
    [dL] = glob_dL.data["dL"]
    x_left = [1, 2, 2, 1]
    x_right = [3, 4, 4, 3]
    y = [3, 3, 15, 15]
    x_mounting = [1, 4, 4, 3, 2, 1]
    y_mounting = [10, 10, 9, 8, 8, 9]
    x_line = [-1, 6]
    y_line = [8, 8]
    xS=[2.5]
    xE=[2.5]
    yS=[9]
    yE=[11]
    xS_L=[0]
    xE_L=[0]
    yS_L=[3]
    yE_L=[8]
    xS_S=[2]
    xE_S=[3]
    yS_S=[5]
    yE_S=[5]
    x_F = [2.7]
    y_F = [10.1]
    x_L = [-0.5]
    y_L = [5.1]
    x_S = [2.35]
    y_S = [4.3]
    
    if material_select.value == "Steel":
        x_sample = [2, 3, 3, 2.875, 2.65, 2.35, 2.125, 2]
        y_sample_top = [8, 8, 4.25, 4.25, 3.25, 3.25, 4.25, 4.25]
        eps = steel_data_eps[0:i]
        sig = steel_data_sig[0:i]
        sig_true = steel_data_true_sig[0:i]
        
        if i == 21:
            R_eH.visible = True
            R1_label.visible = True
            eH_label.visible = True
        if i == 31:
            R_eL.visible = True
            R2_label.visible = True
            eL_label.visible = True
            A_L.visible = True
            A1_label.visible = True
            L_label.visible = True
        if i == 76:
            R_m.visible = True
            R3_label.visible = True
            m_label.visible = True
            A_g.visible = True
            A2_label.visible = True
            g_label.visible = True
        if i == 131:
            A.visible = True
            A3_label.visible = True
            A_t.visible = True
            A4_label.visible = True
            t_label.visible = True
        if i == 132:
            pause()
            play_pause_button.disabled = True
        if i <= 76:
            dx = dx+1/608
            dL = dL+5/152
            xS_S[0] = xS_S[0]+dx
            xE_S[0] = xE_S[0]-dx
            xs = [[2+dx, 2+dx], [3-dx, 3-dx]]
            ys = [[4.8+dL/2, 5.2+dL/2], [4.8+dL/2, 5.2+dL/2]]
        elif i > 76: 
            dL = dL+2/55
            xS_S[0] = xS_S[0]+dx+(i-76)*9/2200
            xE_S[0] = xE_S[0]-dx-(i-76)*9/2200
            xs = [[2+dx+(i-76)*9/2200, 2+dx+(i-76)*9/2200], [3-dx-(i-76)*9/2200, 3-dx-(i-76)*9/2200]]
            if i <= 91:
                ys = [[4.8+dL/2, 5.2+dL/2+(i-76)*0.015], [4.8+dL/2, 5.2+dL/2+(i-76)*0.015]]
            else:
                ys = [[4.8+dL/2, 5.2+dL/2+0.225+(i-91)*0.002], [4.8+dL/2, 5.2+dL/2+0.225+(i-91)*0.002]]
        stress_strain_true_source.data = dict(eps=eps, sig=sig_true)
        for j in range(0, 8):
            y_sample_top[j] = y_sample_top[j]+dL  
        yS_S[0] = yS_S[0]+dL/2
        yE_S[0] = yE_S[0]+dL/2
        y_S[0] = y_S[0]+dL/2 
    elif material_select.value == "CFRP":
        x_sample = [2, 3, 3, 2]
        y_sample_top = [8, 8, 4.5, 4.5]
        eps = cfrp_data_eps[0:i]
        sig = cfrp_data_sig[0:i]
        if i == 25:
            R_p.visible = True
            R4_label.visible = True
            p_label.visible = True
            A_p.visible = True
            A_p_label.visible = True
        if i == 41:
            R_m.visible = True
            R3_label.visible = True
            m_label.visible = True
            A.visible = True
            A3_label.visible = True
            A_t.visible = True
            A4_label.visible = True
            t_label.visible = True
        if i == 42:
            pause()
            play_pause_button.disabled = True
        dx = dx+1/410
        dL = dL+2/41
        xS_S[0] = xS_S[0]+dx
        xE_S[0] = xE_S[0]-dx
        xs = [[2+dx, 2+dx], [3-dx, 3-dx]]
        ys = [[4.8+dL/2, 5.2+dL/2], [4.8+dL/2, 5.2+dL/2]]
        for j in range(0, 4):
            y_sample_top[j] = y_sample_top[j]+dL  
        yS_S[0] = yS_S[0]+dL/2
        yE_S[0] = yE_S[0]+dL/2
        y_S[0] = y_S[0]+dL/2 
    elif material_select.value == "Rubber":
        x_sample = [2, 3, 3, 2]
        y_sample_top = [8, 8, 2, 2]
        eps = rubber_data_eps[0:i]
        sig = rubber_data_sig[0:i]
        if i == 161:
            R_m.visible = True
            R3_label.visible = True
            m_label.visible = True
            A_t.visible = True
            A4_label.visible = True
            t_label.visible = True
        if i == 162:
            pause()
            play_pause_button.disabled = True
        dx = dx+1/805
        dL = dL+1/23
        for j in range(0, 4):
            y_sample_top[j] = y_sample_top[j]+dL  
        xS_S[0] = xS_S[0]+dx
        xE_S[0] = xE_S[0]-dx
        xs = [[2+dx, 2+dx], [3-dx, 3-dx]]
        ys = [[4.8+dL/1.9, 5.2+dL/1.9], [4.8+dL/1.9, 5.2+dL/1.9]]
        yS_S[0] = yS_S[0]+dL/1.9
        yE_S[0] = yE_S[0]+dL/1.9
        y_S[0] = y_S[0]+dL/1.9
    for j in range(0, 4):
        x_left[j] = x_left[j]+dx
        x_right[j] = x_right[j]-dx
    for j in range(0, 6):
        y_mounting[j] = y_mounting[j]+dL
    for j in range(0, 2):
        y_line[j] = y_line[j]+dL
    yS[0] = yS[0]+dL
    yE[0] = yE[0]+dL
    y_F[0] = y_F[0]+dL
    yE_L[0] = yE_L[0]+dL
    y_L[0] = y_L[0]+dL/2
    

    white_patch_left_source.data = dict(x=x_left, y=y)
    white_patch_right_source.data = dict(x=x_right, y=y)
    glob_dx.data = dict(dx=[dx])
    stress_strain_source.data = dict(eps=eps, sig=sig)
    glob_dL.data = dict(dL=[dL])
    top_of_mounting_source.data = dict(x=x_mounting, y=y_mounting)
    top_of_sample_source.data = dict(x=x_sample, y=y_sample_top)
    top_line_source.data = dict(x=x_line, y=y_line)
    top_force_arrow_source.stream(dict(xS=xS, yS=yS, xE=xE, yE=yE), rollover=1)
    top_force_label_source.data = dict(x=x_F, y=y_F, F=["F"])
    L_arrow_source.stream(dict(xS=xS_L, yS=yS_L, xE=xE_L, yE=yE_L), rollover=1)
    L_label_source.data = dict(x=x_L, y=y_L, L=["L"])
    S_arrow_source.stream(dict(xS=xS_S, yS=yS_S, xE=xE_S, yE=yE_S), rollover=1)
    S_label_source.data = dict(x=x_S, y=y_S, S=["S"])
    S_multiline_source.data = dict(xs=xs, ys=ys)

    i = i+1
    glob_i.data = dict(i=[i])
    

## Draw sample
#  initialise drawing area
p = figure(title="", tools="", x_range=(-2,7), y_range=(0,18.1), width = 360, height = 600)
#  remove graph lines
p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None
p.toolbar.logo = None
p.patch(x='x', y='y', source=top_of_sample_source, fill_color="#b3b3b3", line_width=0)
p.patch(x='x', y='y', source=bottom_of_sample_source, fill_color="#b3b3b3", line_width=0)
p.patch(x='x', y='y', source=white_patch_left_source, fill_color="#ffffff", line_width=0)
p.patch(x='x', y='y', source=white_patch_right_source, fill_color="#ffffff", line_width=0)
p.patch([1, 4, 4, 3, 2, 1], [1, 1, 2, 3, 3, 2], fill_color="#8a8a8a", line_width=0)
p.patch(x='x', y='y', source=top_of_mounting_source, fill_color="#8a8a8a", line_width=0)
p.line(x=[-1,6], y=[3,3], line_color='#A2AD00', line_width=2)
p.line(x='x', y='y', source=top_line_source, line_color='#A2AD00', line_width=2)
p.line(x=[-1,6], y=[8,8], line_color='#A2AD00', line_width=2, line_dash='dashed')
p.add_layout(Arrow(start=NormalHead(fill_color='#A2AD00',line_color="#A2AD00",line_width=1,size=10), end=NormalHead(fill_color='#A2AD00',line_color="#A2AD00",line_width=1,size=10),
    x_start=1, y_start=3, x_end=1, y_end=8, line_color="#A2AD00", line_width=2))
p.add_layout(Label(x=0.5,y=5.1,text='L\u2080',text_color='#A2AD00'))
p.add_layout(Arrow(start=NormalHead(fill_color='#A2AD00',line_color="#A2AD00",line_width=1,size=10), end=NormalHead(fill_color='#A2AD00',line_color="#A2AD00",line_width=1,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_color="#A2AD00", line_width=2, source=L_arrow_source))
p.add_layout(LabelSet(x='x',y='y',text='L',text_color='#A2AD00', source=L_label_source))
p.add_layout(Arrow(end=NormalHead(fill_color='#E37222',line_color="#E37222",line_width=1,size=10),
    x_start=2.5, y_start=2, x_end=2.5, y_end=0, line_color="#E37222", line_width=2))
p.add_layout(Arrow(end=NormalHead(fill_color='#E37222',line_color="#E37222",line_width=1,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=top_force_arrow_source,line_color="#E37222",line_width=2))
p.add_layout(Label(x=2.7,y=0.3,text='F',text_color='#E37222'))
p.add_layout(LabelSet(x='x',y='y',text='F',text_color='#E37222', source=top_force_label_source))
p.add_layout(Arrow(start=NormalHead(fill_color='#E37222',line_color="#E37222",line_width=1,size=4), end=NormalHead(fill_color='#E37222',line_color="#E37222",line_width=1,size=4),
    x_start=2, y_start=4, x_end=3, y_end=4, line_color="#E37222", line_width=2))
p.add_layout(Label(x=2.3,y=3.3,text='S\u2080',text_color='#E37222'))
p.multi_line(xs=[[2,2],[3,3]],ys=[[3.8,4.2],[3.8,4.2]],color="#E37222",line_width=2)
p.add_layout(Arrow(start=NormalHead(fill_color='#E37222',line_color="#E37222",line_width=1,size=4), end=NormalHead(fill_color='#E37222',line_color="#E37222",line_width=1,size=4),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', source=S_arrow_source, line_color="#E37222", line_width=2))
p.add_layout(LabelSet(x='x',y='y',text='S',text_color='#E37222', source=S_label_source))
p.multi_line(xs='xs',ys='ys',color="#E37222",line_width=2, source=S_multiline_source)
## Create Plot
# seems like resize is not supported anymore
#toolset = "pan,reset,resize,wheel_zoom"
plot = figure(title="", tools="", x_range=[0,17], y_range=[0,11], width = 765, height = 495)
plot.outline_line_color = "#333333"
plot.toolbar.logo = None
plot.xaxis.axis_label_text_font_size="12pt"
plot.yaxis.axis_label_text_font_size="12pt"
plot.xaxis.axis_label_text_font_style="normal"
plot.yaxis.axis_label_text_font_style="normal"
plot.xaxis.axis_label = "\u03B5 [-]"
plot.yaxis.axis_label = "\u03C3 [N/mm\u00B2]"
plot.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
plot.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
plot.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
plot.yaxis.minor_tick_line_color = None
plot.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
plot.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels
plot.line(x='eps', y='sig', source=stress_strain_source, legend_label="F/S\u2080", color='#0065BD', line_width=2)
plot.line(x='eps', y='sig', source=stress_strain_true_source, legend_label="F/S", color='#0065BD', line_width=2, line_dash='dashed')
R_eH = plot.line([0, 2], [5, 5], color='#E37222')
R1_label = Label(x=0.5,y=5.1,text='R',text_color='#E37222')
eH_label = Label(x=0.8,y=5,text='eH',text_color='#E37222', text_font_size='10pt')
plot.add_layout(R1_label)
plot.add_layout(eH_label)
R_eL = plot.line([0, 3], [4.5, 4.5], color='#E37222')
R2_label = Label(x=0.5,y=4,text='R',text_color='#E37222')
eL_label = Label(x=0.8,y=3.9,text='eL',text_color='#E37222', text_font_size='10pt')
plot.add_layout(R2_label)
plot.add_layout(eL_label)
R_m = plot.line(x='x', y='y', color='#E37222', source=R_m_source)
R3_label = LabelSet(x='x',y='y',text='R',text_color='#E37222', source=R3_label_source)
m_label = LabelSet(x='x',y='y',text='m',text_color='#E37222', text_font_size='10pt', source=m_label_source)
plot.add_layout(R3_label)
plot.add_layout(m_label)
A_L = plot.line([1, 3], [-0.5, 4.5], color='#A2AD00', line_dash='dashed')
A1_label = Label(x=0.7,y=0.2,text='A',text_color='#A2AD00')
L_label = Label(x=1,y=0.1,text='L',text_color='#A2AD00', text_font_size='10pt')
plot.add_layout(A1_label)
plot.add_layout(L_label)
A_g = plot.line([4.5, 7.5], [-0.5, 7], color='#A2AD00', line_dash='dashed')
A2_label = Label(x=4.2,y=0.2,text='A',text_color='#A2AD00')
g_label = Label(x=4.5,y=0.1,text='g',text_color='#A2AD00', text_font_size='10pt')
plot.add_layout(A2_label)
plot.add_layout(g_label)
A = plot.line(x='x', y='y', color='#A2AD00', line_dash='dashed', source=A_source)
A3_label = LabelSet(x='x',y='y',text='A',text_color='#A2AD00', source=A3_label_source)
plot.add_layout(A3_label)
A_t = plot.line(x='x', y='y', color='#A2AD00', line_dash='dashed', source=A_t_source)
A4_label = LabelSet(x='x',y='y',text='A',text_color='#A2AD00',source=A4_label_source)
t_label = LabelSet(x='x',y='y',text='t',text_color='#A2AD00', text_font_size='10pt', source=t_label_source)
plot.add_layout(A4_label)
plot.add_layout(t_label)
R_p = plot.line(x=[0, 2.4], y=[8.05, 8.05], color='#E37222')
R4_label = Label(x=0.5,y=8.15,text='R',text_color='#E37222')
p_label = Label(x=0.8,y=8.05,text='p0,2',text_color='#E37222', text_font_size='10pt')
plot.add_layout(R4_label)
plot.add_layout(p_label)
A_p = plot.line(x=[2.4-18/7, 2.4], y=[-0.95, 8.05], color='#A2AD00', line_dash='dashed')
A_p_label = Label(x=0.3,y=0.2,text='0,2%',text_color='#A2AD00')
plot.add_layout(A_p_label)


def reset():
    pause()
    init()
    play_pause_button.disabled = False
    i = 1
    dx = 0
    dL = 0
    glob_i.data = dict(i=[i])
    glob_dx.data = dict(dx=[dx])
    glob_dL.data = dict(dL=[dL])

def play_pause():
    if play_pause_button.label == "Play":
        play()
    else:
        pause()

def play():
    play_pause_button.label = "Pause"
    callback_id = curdoc().add_periodic_callback(evolve, 150) #dt in milliseconds
    glob_callback_id.data = dict(callback_id = [callback_id])
        
def pause():
    [callback_id] = glob_callback_id.data["callback_id"] 
    play_pause_button.label = "Play"
    try:
        curdoc().remove_periodic_callback(callback_id)
    except ValueError:
        print("WARNING: callback_id was already removed")


reset_button=Button(label="Reset", button_type="success", width = 100)
reset_button.on_click(reset)

play_pause_button=Button(label="Play", button_type="success", width = 100)
play_pause_button.on_click(play_pause)

changeMaterial(0, 0, "Steel")

## Send to window
layout = column(description, row(column(Spacer(height=150), material_select, Spacer(height=100), play_pause_button, reset_button), 
                column(p), column(Spacer(height=80), column(plot))))
curdoc().add_root(layout)  

## get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  
