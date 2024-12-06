from __future__ import division
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import Button, Arrow, Label, Select, ColumnDataSource, NormalHead, LabelSet
#from os.path import dirname, join, split, abspath
import numpy as np
from numpy import linspace, loadtxt

#import sys, inspect
#currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
#parentdir = join(dirname(currentdir), "shared/")
#sys.path.insert(0,parentdir) 
#from latex_support import LatexDiv, LatexLabelSet

# Using pathlib
import pathlib
import sys, inspect
shareddir = str(pathlib.Path(__file__).parent.parent.resolve() / "shared" ) + "/"
sys.path.insert(0,shareddir)
from latex_support import LatexDiv, LatexLabelSet

app_base_path = pathlib.Path(__file__).resolve().parents[0]

## data sources 
top_of_sample_source = ColumnDataSource(data=dict(x=[], y=[]))
bottom_of_sample_source = ColumnDataSource(data=dict(x=[], y=[]))
top_of_mounting_source = ColumnDataSource(data=dict(x=[], y=[]))
top_line_source = ColumnDataSource(data=dict(x=[], y=[]))
top_force_arrow_source = ColumnDataSource(data=dict(xS=[], yS=[], xE=[], yE=[]))
bottom_force_arrow_source = ColumnDataSource(data=dict(xS=[], yS=[], xE=[], yE=[]))
top_force_label_source = ColumnDataSource(data=dict(x=[], y=[], F=[]))
bottom_force_label_source = ColumnDataSource(data=dict(x=[], y=[], F=[]))
stress_strain_source = ColumnDataSource(data=dict(eps=[], sig=[]))
stress_strain_true_source = ColumnDataSource(data=dict(eps=[], sig=[]))
stress_strain_load_source = ColumnDataSource(data=dict(eps=[], sig=[]))
stress_strain_unload_source = ColumnDataSource(data=dict(eps=[], sig=[]))
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
current_data_source = ColumnDataSource(data=dict(x=[], y=[]))
glob_i = ColumnDataSource(data=dict(i=[]))
glob_dx = ColumnDataSource(data=dict(dx=[]))
glob_dL = ColumnDataSource(data=dict(dL=[]))

## values for epsilon
steel_data_eps = linspace(0, 13, num=131)
steel_data_unload_eps = linspace(5.5, 2.8, num=28)
steel_data_unload_eps[27] = 2.86
rubber_data_load_eps = linspace(0, 10, num=101)
rubber_data_unload_eps = linspace(10, 0.2, num=99)
rubber_data_eps = linspace(0.2, 16, num=159)
cfrp_data_eps = linspace(0, 4, num=41)
cfrp_data_unload_eps = linspace(3.5, 0.8, num=28)
cfrp_data_unload_eps[27] = 0.885

## values for sigma
steel_data = loadtxt(str(app_base_path.relative_to(app_base_path.parent)/"steel_data_sig.txt"))
steel_data_sig = steel_data[0]
steel_data_true_sig = steel_data[1]
steel_data_unload_sig = loadtxt('Tensile_test/steel_data_unload_sig.txt')
rubber_data = loadtxt('Tensile_test/rubber_data_sig.txt')
rubber_data_sig = rubber_data[0]
rubber_data_true_sig = rubber_data[1]
rubber_data_load_sig = loadtxt('Tensile_test/rubber_data_load_sig.txt')
rubber_data_unload_sig = loadtxt('Tensile_test/rubber_data_unload_sig.txt')
cfrp_data = loadtxt('Tensile_test/cfrp_data_sig.txt')
cfrp_data_sig = cfrp_data[0]
cfrp_data_true_sig = cfrp_data[1]
cfrp_data_unload_sig = loadtxt('Tensile_test/cfrp_data_unload_sig.txt')

## if the user chooses another material, the position of the coefficients is changed and the coefficient description is adapted
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
        layout.children[1] = row(column(Spacer(height=10), material_select, steel_description, row(Spacer(width=75), play_pause_button), 
                             row(Spacer(width=75), reset_button)), column(p), column(Spacer(height=89), column(plot)))
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
        layout.children[1] = row(column(Spacer(height=10), material_select, cfrp_description, row(Spacer(width=75), play_pause_button), 
                             row(Spacer(width=75), reset_button)), column(p), column(Spacer(height=89), column(plot)))
    elif new == "Rubber":
        x_R_m = [0, 16]
        y_R_m = [4.09, 4.09]
        x_R3 = [0.5]
        y_R3 = [4.19]
        x_m = [0.8]
        y_m = [4.09]
        x_A_t = [16, 16]
        y_A_t = [0, 4.09]
        x_A4 = [15.4]
        y_A4 = [0.2]
        x_t = [15.7]
        y_t = [0.1]
        layout.children[1] = row(column(Spacer(height=10), material_select, rubber_description, row(Spacer(width=75), play_pause_button), 
                             row(Spacer(width=75), reset_button)), column(p), column(Spacer(height=89), column(plot)))
    if new == "CFRP" or new == "Steel":
        A_source.data = dict(x=x_A, y=y_A)
        A3_label_source.data = dict(x=x_A3, y=y_A3, A=["A"])
    R_m_source.data = dict(x=x_R_m, y=y_R_m)
    R3_label_source.data = dict(x=x_R3, y=y_R3, R=["R"])
    m_label_source.data = dict(x=x_m, y=y_m, m=["m"])
    A_t_source.data = dict(x=x_A_t, y=y_A_t)
    A4_label_source.data = dict(x=x_A4, y=y_A4, A=["A"])
    t_label_source.data = dict(x=x_t, y=y_t, t=["t"])

## add app description
description_filename = str(app_base_path / "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)

## add coefficient description
steel_filename = str(app_base_path / "steel_description.html")
steel_description = LatexDiv(text=open(steel_filename).read(), render_as_text=False, width=250)
cfrp_filename = str(app_base_path / "cfrp_description.html")
cfrp_description = LatexDiv(text=open(cfrp_filename).read(), render_as_text=False, width=250)
rubber_filename = str(app_base_path / "rubber_description.html")
rubber_description = LatexDiv(text=open(rubber_filename).read(), render_as_text=False, width=250)

## initial values
def init():
    i = [1]
    dx = [0]
    dL = [0]
    x_mounting = [1, 4, 4, 3, 2, 1]
    y_mounting = [10, 10, 9, 8, 8, 9]
    x_line = [-1, 6]
    y_line = [8, 8]
    xS_top=[2.5]
    xE_top=[2.5]
    yS_top=[9]
    yE_top=[9]
    xS_bottom=[2.5]
    xE_bottom=[2.5]
    yS_bottom=[2]
    yE_bottom=[2]
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
    x_F_top = [2.7]
    y_F_top = [8.6]
    x_F_bottom = [2.7]
    y_F_bottom = [1.8]
    x_L = [-0.5]
    y_L = [5.1]
    x_S = [2.35]
    y_S = [4.3]
    xs = [[2, 2], [3, 3]]
    ys = [[4.8, 5.2], [4.8, 5.2]]
    x_circle = [0]
    y_circle = [0]
    if material_select.value == "Steel":
        x_sample = [2, 3, 3, 2.85, 2.65, 2.35, 2.15, 2]
        y_sample_top = [8, 8, 4.375, 4.375, 3.56, 3.56, 4.375, 4.375]
        y_sample_bottom = [3, 3, 6.625, 6.625, 7.44, 7.44, 6.625, 6.625]
    elif material_select.value == "Rubber":
        x_sample = [2, 3, 3, 2]
        y_sample_top = [8, 8, 2.31, 2.31]
        y_sample_bottom = [3, 3, 8.69, 8.69]
    elif material_select.value == "CFRP":
        x_sample = [2, 3, 3, 2]
        y_sample_top = [8, 8, 4.71, 4.71]
        y_sample_bottom = [3, 3, 6.29, 6.29]
    bottom_of_sample_source.data = dict(x=x_sample, y=y_sample_bottom)
    top_of_mounting_source.data = dict(x=x_mounting, y=y_mounting)
    top_of_sample_source.data = dict(x=x_sample, y=y_sample_top)
    top_line_source.data = dict(x=x_line, y=y_line)
    top_force_arrow_source.stream(dict(xS=xS_top, yS=yS_top, xE=xE_top, yE=yE_top), rollover=1)
    bottom_force_arrow_source.stream(dict(xS=xS_bottom, yS=yS_bottom, xE=xE_bottom, yE=yE_bottom), rollover=1)
    stress_strain_source.data = dict(eps=[], sig=[])
    stress_strain_true_source.data = dict(eps=[], sig=[])
    stress_strain_load_source.data = dict(eps=[], sig=[])
    stress_strain_unload_source.data = dict(eps=[], sig=[])
    white_patch_left_source.data = dict(x=x_left, y=y)
    white_patch_right_source.data = dict(x=x_right, y=y) 
    top_force_label_source.data = dict(x=x_F_top, y=y_F_top, F=["F"])
    bottom_force_label_source.data = dict(x=x_F_bottom, y=y_F_bottom, F=["F"])
    L_arrow_source.stream(dict(xS=xS_L, yS=yS_L, xE=xE_L, yE=yE_L), rollover=1)
    L_label_source.data = dict(x=x_L, y=y_L, L=["L"])
    S_arrow_source.stream(dict(xS=xS_S, yS=yS_S, xE=xE_S, yE=yE_S), rollover=1)
    S_label_source.data = dict(x=x_S, y=y_S, S=["S"])
    S_multiline_source.data = dict(xs=xs, ys=ys)
    current_data_source.data = dict(x=x_circle, y=y_circle)
    glob_i.data = dict(i=i)
    glob_dx.data = dict(dx=dx)
    glob_dL.data = dict(dL=dL)

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
    top_force_arrow.visible = False
    bottom_force_arrow.visible = False
    top_force_label.visible = False
    bottom_force_label.visible = False

## draw stress-strain curve and deformation of the sample
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
    xS_top=[2.5]
    xE_top=[2.5]
    yS_top=[9]
    yE_top=[9]
    xS_bottom=[2.5]
    xE_bottom=[2.5]
    yS_bottom=[2]
    yE_bottom=[2]
    xS_L=[0]
    xE_L=[0]
    yS_L=[3]
    yE_L=[8]
    xS_S=[2]
    xE_S=[3]
    yS_S=[5]
    yE_S=[5]
    x_F_top = [2.7]
    y_F_top = [8.6]
    x_F_bottom = [2.7]
    y_F_bottom = [1.8]
    x_L = [-0.5]
    y_L = [5.1]
    x_S = [2.35]
    y_S = [4.3]
    if material_select.value == "Steel":
        x_sample = [2, 3, 3, 2.85, 2.65, 2.35, 2.15, 2]
        y_sample_top = [8, 8, 4.375, 4.375, 3.56, 3.56, 4.375, 4.375]
        eps_load = []
        sig_load = []
        if i == 1 or i == 84 or i == 85:
            top_force_arrow.visible = False
            bottom_force_arrow.visible = False
            top_force_label.visible = False
            bottom_force_label.visible = False
        else:
            top_force_arrow.visible = True
            bottom_force_arrow.visible = True
            top_force_label.visible = True
            bottom_force_label.visible = True
        if i > 0 and i <= 56: 
            eps = steel_data_eps[0:i]
            sig = steel_data_sig[0:i]
            sig_true = steel_data_true_sig[0:i]
            eps_unload = steel_data_unload_eps[0:0]
            sig_unload = steel_data_unload_sig[0:0]
            x_circle = [eps[i-1]]
            y_circle = [sig[i-1]]
            dx = dx+11/5600
            dL = dL+33/1120
            if i <= 21 or i > 33:
                yE_top[0] = yE_top[0]+dL+(2/7)*sig[i-1]
                yE_bottom[0] = yE_bottom[0]-(2/7)*sig[i-1]
                y_F_top[0] = y_F_top[0]+dL+(2/7)*sig[i-1]
                y_F_bottom[0] = y_F_bottom[0]-(2/7)*sig[i-1]
            elif i > 21 and i <= 33:
                yE_top[0] = yE_top[0]+dL+(2/7)*sig[20]
                yE_bottom[0] = yE_bottom[0]-(2/7)*sig[20]
                y_F_top[0] = y_F_top[0]+dL+(2/7)*sig[20]
                y_F_bottom[0] = y_F_bottom[0]-(2/7)*sig[20]
        elif i > 56 and i <= 84:
            eps = steel_data_eps[0:56]
            sig = steel_data_sig[0:56]
            sig_true = steel_data_true_sig[0:56]
            eps_unload = steel_data_unload_eps[0:i-56]
            sig_unload = steel_data_unload_sig[0:i-56]
            x_circle = [eps_unload[i-56-1]]
            y_circle = [sig_unload[i-56-1]]
            dx = dx-11/5600
            dL = dL-33/1120
            yE_top[0] = yE_top[0]+dL+(2/7)*sig_unload[i-56-1]
            yE_bottom[0] = yE_bottom[0]-(2/7)*sig_unload[i-56-1]
            y_F_top[0] = y_F_top[0]+dL+(2/7)*sig_unload[i-56-1]
            y_F_bottom[0] = y_F_bottom[0]-(2/7)*sig_unload[i-56-1]
        elif i > 84 and i <= 112:
            eps = steel_data_eps[0:56]
            sig = steel_data_sig[0:56]
            sig_true = steel_data_true_sig[0:56]
            eps_unload = steel_data_unload_eps[0:28]
            sig_unload = steel_data_unload_sig[0:28]
            x_circle = [eps_unload[112-i]]
            y_circle = [sig_unload[112-i]]
            dx = dx+11/5600
            dL = dL+33/1120
            yE_top[0] = yE_top[0]+dL+(2/7)*sig_unload[112-i]
            yE_bottom[0] = yE_bottom[0]-(2/7)*sig_unload[112-i]
            y_F_top[0] = y_F_top[0]+dL+(2/7)*sig_unload[112-i]
            y_F_bottom[0] = y_F_bottom[0]-(2/7)*sig_unload[112-i]
        elif i > 112 and i <= 187:
            eps = steel_data_eps[0:i-56]
            sig = steel_data_sig[0:i-56]
            sig_true = steel_data_true_sig[0:i-56]
            eps_unload = steel_data_unload_eps[0:28]
            sig_unload = steel_data_unload_sig[0:28]
            x_circle = [eps[i-56-1]]
            y_circle = [sig[i-56-1]]
            dL = dL+0.03
            yE_top[0] = yE_top[0]+dL+(2/7)*sig[i-56-1]
            yE_bottom[0] = yE_bottom[0]-(2/7)*sig[i-56-1]
            y_F_top[0] = y_F_top[0]+dL+(2/7)*sig[i-56-1]
            y_F_bottom[0] = y_F_bottom[0]-(2/7)*sig[i-56-1]
        if i > 112 and i <= 132:
            dx = dx+0.002
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
        if i == 132:
            R_m.visible = True
            R3_label.visible = True
            m_label.visible = True
            A_g.visible = True
            A2_label.visible = True
            g_label.visible = True
        if i == 187:
            A.visible = True
            A3_label.visible = True
            A_t.visible = True
            A4_label.visible = True
            t_label.visible = True
            pause()
            play_pause_button.disabled = True
        if i <= 132:
            xS_S[0] = xS_S[0]+dx
            xE_S[0] = xE_S[0]-dx
            xs = [[2+dx, 2+dx], [3-dx, 3-dx]]
            ys = [[4.8+dL/2, 5.2+dL/2], [4.8+dL/2, 5.2+dL/2]]
        elif i > 132: 
            xS_S[0] = xS_S[0]+dx+(i-132)*1/275
            xE_S[0] = xE_S[0]-dx-(i-132)*1/275
            xs = [[2+dx+(i-132)*1/275, 2+dx+(i-132)*1/275], [3-dx-(i-132)*1/275, 3-dx-(i-132)*1/275]]
            if i <= 147:
                ys = [[4.8+dL/2, 5.2+dL/2+(i-132)*0.015], [4.8+dL/2, 5.2+dL/2+(i-132)*0.015]]
            else:
                ys = [[4.8+dL/2, 5.2+dL/2+0.225+(i-147)*0.002], [4.8+dL/2, 5.2+dL/2+0.225+(i-147)*0.002]]
        for j in range(0, 8):
            y_sample_top[j] = y_sample_top[j]+dL  
        yS_S[0] = yS_S[0]+dL/2
        yE_S[0] = yE_S[0]+dL/2
        y_S[0] = y_S[0]+dL/2 
    elif material_select.value == "CFRP":
        x_sample = [2, 3, 3, 2]
        y_sample_top = [8, 8, 4.71, 4.71]
        eps_load = []
        sig_load = []
        if i == 1 or i == 64 or i == 65:
            top_force_arrow.visible = False
            bottom_force_arrow.visible = False
            top_force_label.visible = False
            bottom_force_label.visible = False
        else:
            top_force_arrow.visible = True
            bottom_force_arrow.visible = True
            top_force_label.visible = True
            bottom_force_label.visible = True
        if i > 0 and i <= 36: 
            eps = cfrp_data_eps[0:i]
            sig = cfrp_data_sig[0:i]
            sig_true = cfrp_data_true_sig[0:i]
            eps_unload = cfrp_data_unload_eps[0:0]
            sig_unload = cfrp_data_unload_sig[0:0]
            x_circle = [eps[i-1]]
            y_circle = [sig[i-1]]
            dx = dx+7/3600
            dL = dL+7/180
            yE_top[0] = yE_top[0]+dL+(2.6/9.37)*sig[i-1]
            yE_bottom[0] = yE_bottom[0]-(2.6/9.37)*sig[i-1]
            y_F_top[0] = y_F_top[0]+dL+(2.6/9.37)*sig[i-1]
            y_F_bottom[0] = y_F_bottom[0]-(2.6/9.37)*sig[i-1]
        elif i > 36 and i <= 64:
            eps = cfrp_data_eps[0:36]
            sig = cfrp_data_sig[0:36]
            sig_true = cfrp_data_true_sig[0:36]
            eps_unload = cfrp_data_unload_eps[0:i-36]
            sig_unload = cfrp_data_unload_sig[0:i-36]
            x_circle = [eps_unload[i-36-1]]
            y_circle = [sig_unload[i-36-1]]
            dx = dx-7/3600
            dL = dL-7/180
            yE_top[0] = yE_top[0]+dL+(2.6/9.37)*sig_unload[i-36-1]
            yE_bottom[0] = yE_bottom[0]-(2.6/9.37)*sig_unload[i-36-1]
            y_F_top[0] = y_F_top[0]+dL+(2.6/9.37)*sig_unload[i-36-1]
            y_F_bottom[0] = y_F_bottom[0]-(2.6/9.37)*sig_unload[i-36-1]
        elif i > 64 and i <= 92:
            eps = cfrp_data_eps[0:36]
            sig = cfrp_data_sig[0:36]
            sig_true = cfrp_data_true_sig[0:36]
            eps_unload = cfrp_data_unload_eps[0:28]
            sig_unload = cfrp_data_unload_sig[0:28]
            x_circle = [eps_unload[92-i]]
            y_circle = [sig_unload[92-i]]
            dx = dx+7/3600
            dL = dL+7/180
            yE_top[0] = yE_top[0]+dL+(2.6/9.37)*sig_unload[92-i]
            yE_bottom[0] = yE_bottom[0]-(2.6/9.37)*sig_unload[92-i]
            y_F_top[0] = y_F_top[0]+dL+(2.6/9.37)*sig_unload[92-i]
            y_F_bottom[0] = y_F_bottom[0]-(2.6/9.37)*sig_unload[92-i]
        elif i > 92:
            eps = cfrp_data_eps[0:i-56]
            sig = cfrp_data_sig[0:i-56]
            sig_true = cfrp_data_true_sig[0:i-56]
            eps_unload = cfrp_data_unload_eps[0:28]
            sig_unload = cfrp_data_unload_sig[0:28]
            x_circle = [eps[i-56-1]]
            y_circle = [sig[i-56-1]]
            dx = dx+0.002
            dL = dL+0.04
            yE_top[0] = yE_top[0]+dL+(2.6/9.37)*sig[i-56-1]
            yE_bottom[0] = yE_bottom[0]-(2.6/9.37)*sig[i-56-1]
            y_F_top[0] = y_F_top[0]+dL+(2.6/9.37)*sig[i-56-1]
            y_F_bottom[0] = y_F_bottom[0]-(2.6/9.37)*sig[i-56-1]
        if i == 25:
            R_p.visible = True
            R4_label.visible = True
            p_label.visible = True
            A_p.visible = True
            A_p_label.visible = True
        if i == 97:
            R_m.visible = True
            R3_label.visible = True
            m_label.visible = True
            A.visible = True
            A3_label.visible = True
            A_t.visible = True
            A4_label.visible = True
            t_label.visible = True
            pause()
            play_pause_button.disabled = True     
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
        y_sample_top = [8, 8, 2.31, 2.31]
        if i == 1 or i == 200 or i == 201:
            top_force_arrow.visible = False
            bottom_force_arrow.visible = False
            top_force_label.visible = False
            bottom_force_label.visible = False
        else:
            top_force_arrow.visible = True
            bottom_force_arrow.visible = True
            top_force_label.visible = True
            bottom_force_label.visible = True
        if i > 0 and i <= 101: 
            eps = []
            sig = []
            sig_true = []
            eps_unload = []
            sig_unload = []
            eps_load = rubber_data_load_eps[0:i]
            sig_load = rubber_data_load_sig[0:i]
            x_circle = [eps_load[i-1]]
            y_circle = [sig_load[i-1]]
            dx = dx+3/2020
            dL = dL+4/101
            yE_top[0] = yE_top[0]+dL+(1.2/4.09)*sig_load[i-1]
            yE_bottom[0] = yE_bottom[0]-(1.2/4.09)*sig_load[i-1]
            y_F_top[0] = y_F_top[0]+dL+(1.2/4.09)*sig_load[i-1]
            y_F_bottom[0] = y_F_bottom[0]-(1.2/4.09)*sig_load[i-1]
        elif i > 101 and i <= 200:
            eps = []
            sig = []
            sig_true = []
            eps_unload = rubber_data_unload_eps[0:i-101]
            sig_unload = rubber_data_unload_sig[0:i-101]
            eps_load = rubber_data_load_eps[0:101]
            sig_load = rubber_data_load_sig[0:101]
            x_circle = [eps_unload[i-101-1]]
            y_circle = [sig_unload[i-101-1]]
            dx = dx-3/2020
            dL = dL-4/101
            yE_top[0] = yE_top[0]+dL+(1.2/4.09)*sig_unload[i-101-1]
            yE_bottom[0] = yE_bottom[0]-(1.2/4.09)*sig_unload[i-101-1]
            y_F_top[0] = y_F_top[0]+dL+(1.2/4.09)*sig_unload[i-101-1]
            y_F_bottom[0] = y_F_bottom[0]-(1.2/4.09)*sig_unload[i-101-1]
        elif i > 200:
            eps = rubber_data_eps[0:i-200]
            sig = rubber_data_sig[0:i-200]
            sig_true = rubber_data_true_sig[0:i-200]
            eps_unload = rubber_data_unload_eps[0:99]
            sig_unload = rubber_data_unload_sig[0:99]
            eps_load = rubber_data_load_eps[0:101]
            sig_load = rubber_data_load_sig[0:101]
            x_circle = [eps[i-201]]
            y_circle = [sig[i-201]]
            dx = dx+399/267650
            dL = dL+1064/26765
            yE_top[0] = yE_top[0]+dL+(1.2/4.09)*sig[i-201]
            yE_bottom[0] = yE_bottom[0]-(1.2/4.09)*sig[i-201]
            y_F_top[0] = y_F_top[0]+dL+(1.2/4.09)*sig[i-201]
            y_F_bottom[0] = y_F_bottom[0]-(1.2/4.09)*sig[i-201]
        if i == 359:
            R_m.visible = True
            R3_label.visible = True
            m_label.visible = True
            A_t.visible = True
            A4_label.visible = True
            t_label.visible = True
            pause()
            play_pause_button.disabled = True
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
    yS_top[0] = yS_top[0]+dL
    yE_L[0] = yE_L[0]+dL
    y_L[0] = y_L[0]+dL/2
    i = i+1
    top_of_mounting_source.data = dict(x=x_mounting, y=y_mounting)
    top_of_sample_source.data = dict(x=x_sample, y=y_sample_top)
    top_line_source.data = dict(x=x_line, y=y_line)
    top_force_arrow_source.stream(dict(xS=xS_top, yS=yS_top, xE=xE_top, yE=yE_top), rollover=1)
    bottom_force_arrow_source.stream(dict(xS=xS_bottom, yS=yS_bottom, xE=xE_bottom, yE=yE_bottom), rollover=1)
    stress_strain_source.data = dict(eps=eps, sig=sig)
    stress_strain_true_source.data = dict(eps=eps, sig=sig_true)
    stress_strain_load_source.data = dict(eps=eps_load, sig=sig_load)
    stress_strain_unload_source.data = dict(eps=eps_unload, sig=sig_unload)
    white_patch_left_source.data = dict(x=x_left, y=y)
    white_patch_right_source.data = dict(x=x_right, y=y) 
    top_force_label_source.data = dict(x=x_F_top, y=y_F_top, F=["F"])
    bottom_force_label_source.data = dict(x=x_F_bottom, y=y_F_bottom, F=["F"])
    L_arrow_source.stream(dict(xS=xS_L, yS=yS_L, xE=xE_L, yE=yE_L), rollover=1)
    L_label_source.data = dict(x=x_L, y=y_L, L=["L"])
    S_arrow_source.stream(dict(xS=xS_S, yS=yS_S, xE=xE_S, yE=yE_S), rollover=1)
    S_label_source.data = dict(x=x_S, y=y_S, S=["S"])
    S_multiline_source.data = dict(xs=xs, ys=ys)
    current_data_source.data = dict(x=x_circle, y=y_circle)
    glob_i.data = dict(i=[i])
    glob_dx.data = dict(dx=[dx])
    glob_dL.data = dict(dL=[dL])   

## Draw sample
p = figure(title="", tools="", x_range=(-2,6.5), y_range=(-0.7,18.1), width = 310, height = 565)
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
bottom_force_arrow = Arrow(end=NormalHead(fill_color='#E37222',line_color="#E37222",line_width=1,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', source=bottom_force_arrow_source,line_color="#E37222", line_width=2)
p.add_layout(bottom_force_arrow)
top_force_arrow = Arrow(end=NormalHead(fill_color='#E37222',line_color="#E37222",line_width=1,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',source=top_force_arrow_source,line_color="#E37222",line_width=2)
p.add_layout(top_force_arrow)
bottom_force_label = LabelSet(x='x',y='y',text='F',text_color='#E37222', source=bottom_force_label_source)
p.add_layout(bottom_force_label)
top_force_label = LabelSet(x='x',y='y',text='F',text_color='#E37222', source=top_force_label_source)
p.add_layout(top_force_label)
p.add_layout(Arrow(start=NormalHead(fill_color='#E37222',line_color="#E37222",line_width=1,size=4), end=NormalHead(fill_color='#E37222',line_color="#E37222",line_width=1,size=4),
    x_start=2, y_start=4, x_end=3, y_end=4, line_color="#E37222", line_width=2))
p.add_layout(Label(x=2.3,y=3.3,text='S\u2080',text_color='#E37222'))
p.multi_line(xs=[[2,2],[3,3]],ys=[[3.8,4.2],[3.8,4.2]],color="#E37222",line_width=2)
p.add_layout(Arrow(start=NormalHead(fill_color='#E37222',line_color="#E37222",line_width=1,size=4), end=NormalHead(fill_color='#E37222',line_color="#E37222",line_width=1,size=4),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', source=S_arrow_source, line_color="#E37222", line_width=2))
p.add_layout(LabelSet(x='x',y='y',text='S',text_color='#E37222', source=S_label_source))
p.multi_line(xs='xs',ys='ys',color="#E37222",line_width=2, source=S_multiline_source)

## Create Plot
plot = figure(title="", tools="", x_range=[0,17], y_range=[0,11], width = 700, height = 450)
plot.outline_line_color = "#333333"
plot.toolbar.logo = None
plot.xaxis.axis_label_text_font_size="12pt"
plot.yaxis.axis_label_text_font_size="12pt"
plot.xaxis.axis_label_text_font_style="normal"
plot.yaxis.axis_label_text_font_style="normal"
plot.xaxis.axis_label = "\u03B5 [%]"
plot.yaxis.axis_label = "\u03C3 [N/mm\u00B2]"
plot.xaxis.major_tick_line_color = None 
plot.xaxis.minor_tick_line_color = None 
plot.yaxis.major_tick_line_color = None 
plot.yaxis.minor_tick_line_color = None
plot.xaxis.major_label_text_font_size = '0pt' 
plot.yaxis.major_label_text_font_size = '0pt'  
plot.line(x='eps', y='sig', source=stress_strain_source, legend_label="F/S\u2080", color='#0065BD', line_width=2)
plot.line(x='eps', y='sig', source=stress_strain_true_source, legend_label="F/S", color='#0065BD', line_width=2, line_dash='dashed')
plot.line(x='eps', y='sig', source=stress_strain_load_source, color='#0065BD', line_width=2)
plot.line(x='eps', y='sig', source=stress_strain_unload_source, color='#0065BD', line_width=2)
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
p_label = Label(x=0.8,y=8.05,text='p0.2',text_color='#E37222', text_font_size='10pt')
plot.add_layout(R4_label)
plot.add_layout(p_label)
A_p = plot.line(x=[2.4-18/7, 2.4], y=[-0.95, 8.05], color='#A2AD00', line_dash='dashed')
A_p_label = Label(x=0.3,y=0.2,text='0.2%',text_color='#A2AD00')
plot.add_layout(A_p_label)
plot.circle(x='x', y='y', fill_color='black', line_color='black', radius=0.1, source=current_data_source)

def reset():
    pause()
    init()
    play_pause_button.disabled = False

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

## define buttons and drop down menu
reset_button=Button(label="Reset", button_type="success", width = 100)
reset_button.on_click(reset)
play_pause_button=Button(label="Play", button_type="success", width = 100)
play_pause_button.on_click(play_pause)
material_select = Select(title="Material:", value="Steel",
    options=["Steel","Rubber", "CFRP"], width = 250)
material_select.on_change('value',changeMaterial)

## app layout
layout = column(description, row(column(Spacer(height=10), material_select, steel_description, row(Spacer(width=75), play_pause_button), 
         row(Spacer(width=75), reset_button)), column(p), column(Spacer(height=89), column(plot))))

## set initial material to "Steel"
changeMaterial(0, 0, "Steel")

## Send to window
curdoc().add_root(layout)  

## get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
curdoc().title = str(app_base_path.relative_to(app_base_path.parent)).replace("_"," ").replace("-"," ")