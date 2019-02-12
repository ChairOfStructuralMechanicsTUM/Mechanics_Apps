# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 17:02:31 2019

@author: Boulbrachene
"""

#import numpy as np
#
from bokeh.plotting import figure, show
from math import exp,sin,pi
from scipy.integrate import quad
import matplotlib.pyplot as plt
import numpy as np

n=600
a=np.linspace(0.1,5,n)
b=np.linspace(0.1,5,n)
W=np.zeros((len(a), len(b)))


for i in range (0,len(a)):
        for j in range (0,len(b)):
            W[i][j]= a[i]**0.5 * 1 * (4-b[j])/a[i] * exp(-( (4-b[j])/a[i] )**2.0)


B,A= np.meshgrid(b,a)
plt.contourf(B,A,W)
plt.colorbar()
p = figure(x_range=(0, 5), y_range=(0, 5))
p.image(image=[W], x=0, y=0, dw=5, dh=5, palette="Spectral11")
#show(p)  # open a browser


#from os.path import dirname, split, join
#import numpy as np
#from scipy.integrate import quad
#import matplotlib.pyplot as plt 
#from math import exp
#from bokeh.plotting import Figure, show
#from bokeh.layouts import widgetbox, layout
#from bokeh.models.widgets import Button, Select, Slider,TextInput
#from sympy import sympify, lambdify
#from bokeh.io import curdoc
#
## text input window for function f(t) to be transformed
#
#plot_Wavelet= Figure(x_range=(0, 5), y_range=(0, 5), x_axis_label='b',
#                            y_axis_label='a',
#                            active_scroll="wheel_zoom",
#                            title="Wavelet transform of function")
#
#
#
####################################################################################
# ####################################################################
#
#def update():
#    """
#    Compute data depending on input function.
#    """
#
#    # Extract parameters
##    x_function = extract_parameters()
#
#    # computation of WT
#    n=100
#    a=np.linspace(0.1,5,n)
#    b=np.linspace(0.1,5,n)
#    W=np.zeros((len(a), len(b)))
#
#    for i in range (0,len(a)):
#        for j in range (0,len(b)):
#            def integrand1(t):
#                output = (t-b[j])/a[i] * exp(-( (t-b[j])/a[i] )**2.0)
#                return output
#            W[i][j]=quad(integrand1,1,2)[0]
#    
#    B,A= np.meshgrid(b,a)
#    plt.contourf(B,A,W)
#    plot_Wavelet.image(image=[W], x=0, y=0, dw=5, dh=5, palette="Spectral11")
#
#    # if sample_function_used and show_analytical_solution: # we only provide the analytical solution, if a sample function is used.
#    #     X_analytical, f_analytical = sample_fourier_transform(T_0, N)
#    #     X_analytical_source.data = dict(frequency=f_analytical.tolist(), X_real=X_analytical.real, X_imag=X_analytical.imag)
#
#    # else:  # otherwise we provide empty arrays
#    #     X_analytical_source.data = dict(frequency=[], X_real=[], X_imag=[])
#
#    # N_samples = 1000
#    # t_analytical, h = np.linspace(0, T_0, N_samples, retstep=True)
#    # x_function_analytical, _ = string_to_function_parser(f_input.value, h, ['t'])  # function to be transformed
#    # x_analytical = x_function_analytical(t_analytical)
#    # x_analytical_source.data = dict(t=t_analytical.tolist(), x=x_analytical.tolist())
#
#    # if color_interval:
#    #     t_start = - N / T_0 / 2.0
#    #     t_end = + N / T_0 / 2.0
#    #     # data for patch denoting the size of one interval
#    #     source_interval_patch.data = dict(x_patch=[t_start,t_end,t_end,t_start],
#    #                                       y_patch=[-10**3,-10**3,+10**3,+10**3])
#    #     # data for patch border lines
#    #     source_interval_bound.data = dict(x_min=[t_start,t_start],
#    #                                       x_max=[t_end,t_end],
#    #                                       y_minmax=[-10**3,-10**3])
#
## create plots
#update()
#
#
#
#curdoc().add_root(layout([[plot_Wavelet]],
#                         sizing_mode='stretch_both')) # add plots and controls to root
#curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
#





#import numpy as np
#from scipy import signal
#import matplotlib.pyplot as plt
#t = np.linspace(-1, 1, 200, endpoint=False)
#sig  = np.sin(2 * np.pi * 7 * t)
#widths = np.arange(1, 31)
#cwtmatr = signal.cwt(sig, signal.ricker, widths)
#plt.imshow(cwtmatr, extent=[0, 5, 0, 5], cmap='PRGn', aspect='auto',
#           vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
#plt.show()









