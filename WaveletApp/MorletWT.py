import numpy as np
from scipy.integrate import quad
from math import sin, cos, pi, exp

def Find_Heaviside_Morlet_WT(T0,amp,Resolut):
    # computation of WT
    n = Resolut
    a = np.linspace(0.1, 5, n)
    b = np.linspace(0.1, 5, n)
    W = np.zeros((len(a), len(b)))
    
    for i in range (0,len(a)):
        for j in range (0,len(b)):
            def integrand1(t):
                output = a[i]**-0.5 * amp * exp(-(((t-b[j])/a[i])**2)/2) * cos(5*((t-b[j])/a[i]))
                return output
            W[i][j]=quad(integrand1, T0, 15)[0]
    return a,b,W
    # fig, ax = plt.subplots()
    # A, B = np.meshgrid(a, b)
    # contour = ax.contourf(A, B, W, extend='both', cmap='Spectral')
    # try:
    #     filled_contours(plot_Wavelet,  contour)
    # except:
    #     traceback.print_exc()
    #     raise
    # plot_Wavelet.patches(xs='a', ys='b', source=WaveLet_source, color='c', alpha='a')
    # plot_Wavelet.add_layout(color_bar, 'right')

def Find_Rectangular_Morlet_WT(T0,T1,amp,Resolut):
    # computation of WT
    n=Resolut
    a=np.linspace(0.1,5,n)
    b=np.linspace(0.1,5,n)
    W=np.zeros((len(a), len(b)))
    
    for i in range (0,len(a)):
        for j in range (0,len(b)):
            def integrand1(t):
                output = a[i]**-0.5 * amp * exp(-(((t-b[j])/a[i])**2)/2) * cos(5*((t-b[j])/a[i]))
                return output
            W[i][j]=quad(integrand1, T0, T1)[0]
    return a,b,W
    #plot_Wavelet.add_layout(color_bar, 'right')

def Find_Dirac_Morlet_WT(T0, amp,Resolut):
    # computation of WT
    n=Resolut
    a=np.linspace(0.1,5,n)
    b=np.linspace(0.1,5,n)
    W=np.zeros((len(a), len(b)))

    for i in range (0,len(a)):
        for j in range (0,len(b)):
            W[i][j]= a[i]**-0.5 * amp * exp(-(((T0-b[j])/a[i])**2)/2) * cos(5*((T0-b[j])/a[i]))
    return a,b,W
    #plot_Wavelet.add_layout(color_bar, 'right')

def Find_Custom_Morlet_WT(user_func,Resolut):
    n=Resolut
    a=np.linspace(0.1,5,n)
    b=np.linspace(0.1,5,n)
    W=np.zeros((len(a), len(b)))
   
    #make a list of safe functions
    safe_dict = {
        'sin' : sin,
        'cos' : cos,
        'pi' : pi,
        'exp' : exp,
    }
    # WT= "exp(-(((t-b)/a)**2)/2) * cos(5*((t-b)/a))"
    # Stand_WT= "((t-b)/a) * exp(-((t-b)/a)**2)"
    # eval(Stand_WT, safe_dict)
    for i, a_i in enumerate(a):
        for j, b_j in enumerate(b):
            def integrand(t):
                safe_dict['t'] = t
                try:
                    return a[i]**-0.5 * eval(user_func, safe_dict) * exp(-(((t-b[j])/a[i])**2)/2) * cos(5*((t-b[j])/a[i]))
                except NameError:
                    pass
            W[i][j]=quad(integrand, -10, 15)[0]
    return a,b,W
    #plot_Wavelet.add_layout(color_bar, 'right')