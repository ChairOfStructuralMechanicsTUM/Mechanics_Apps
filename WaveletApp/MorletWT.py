import numpy as np
from scipy.integrate import quad
from math import sin, cos, pi, exp
import time

def Find_Heaviside_Morlet_WT(T0,amp,Resolut):
    tic = time.time()
    # computation of WT
    a = np.linspace(0.1, 5, Resolut)
    b = np.linspace(0.1, 5, Resolut)
    W = np.zeros((Resolut, Resolut))
    
    for i in range (0,Resolut):
        for j in range (0,Resolut):
            def integrand1(t):
                output = a[i]**-0.5 * amp * exp(-(((t-b[j])/a[i])**2)/2) * cos(5*((t-b[j])/a[i]))
                return output
            W[i][j]=quad(integrand1, T0, 15)[0]
    
    toc = time.time()
    print (str(toc-tic) + ' sec Elapsed' )
    return a,b,W

def Find_Rectangular_Morlet_WT(T0,T1,amp,Resolut):
    tic = time.time()
    # computation of WT
    a=np.linspace(0.1,5,Resolut)
    b=np.linspace(0.1,5,Resolut)
    W = np.zeros((Resolut, Resolut))
    
    for i in range (0,Resolut):
        for j in range (0,Resolut):
            def integrand1(t):
                output = a[i]**-0.5 * amp * exp(-(((t-b[j])/a[i])**2)/2) * cos(5*((t-b[j])/a[i]))
                return output
            W[i][j]=quad(integrand1, T0, T1)[0]
    
    toc = time.time()
    print (str(toc-tic) + ' sec Elapsed' )
    return a,b,W

def Find_Dirac_Morlet_WT(T0, amp,Resolut):
    tic = time.time()
    # computation of WT
    a=np.linspace(0.1,5,Resolut)
    b=np.linspace(0.1,5,Resolut)
    W = np.zeros((Resolut, Resolut))
    
    for i in range (0,Resolut):
        for j in range (0,Resolut):
            W[i][j]= a[i]**-0.5 * amp * exp(-(((T0-b[j])/a[i])**2)/2) * cos(5*((T0-b[j])/a[i]))
    
    toc = time.time()
    print (str(toc-tic) + ' sec Elapsed' )
    return a,b,W

def Find_Trig_Morlet_WT(index, frequency, Resolut):
    tic = time.time()
    a=np.linspace(0.1,5,Resolut)
    b=np.linspace(0.1,5,Resolut)
    W=np.zeros((Resolut, Resolut))

    if (index == 0):

        for i in range (0,Resolut):
            for j in range (0,Resolut):
                def integrand1(t):
                    output = a[i]**-0.5 * np.sin(2 * np.pi * frequency * t) * exp(-(((t-b[j])/a[i])**2)/2) * cos(5*((t-b[j])/a[i]))
                    return output
                W[i][j]=quad(integrand1, -10, 15)[0]

    else:
        for i in range (0,Resolut):
            for j in range (0,Resolut):
                def integrand1(t):
                    output = a[i]**-0.5 * np.cos(2 * np.pi * frequency * t) * exp(-(((t-b[j])/a[i])**2)/2) * cos(5*((t-b[j])/a[i]))
                    return output
                W[i][j]=quad(integrand1, -10, 15)[0]
    
    toc = time.time()
    print (str(toc-tic) + ' sec Elapsed' )
    return a,b,W

def Find_Custom_Morlet_WT(user_func,Resolut):
    tic = time.time()
    a=np.linspace(0.1,5,Resolut)
    b=np.linspace(0.1,5,Resolut)
    W = np.zeros((Resolut, Resolut))
   
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
    for i in range (0,Resolut):
        for j in range (0,Resolut):
            def integrand(t):
                safe_dict['t'] = t
                try:
                    return a[i]**-0.5 * eval(user_func, safe_dict) * exp(-(((t-b[j])/a[i])**2)/2) * cos(5*((t-b[j])/a[i]))
                except NameError:
                    pass
            W[i][j]=quad(integrand, -10, 15)[0]
    
    toc = time.time()
    print (str(toc-tic) + ' sec Elapsed' )
    return a,b,W