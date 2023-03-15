import numpy as np
from scipy.integrate import quad
from math import sin, cos, pi, exp

def Find_Heaviside_Wavelet_Two(T0,amp,Resolut):
    """
    This function computes the wavelet transform of a heaviside function
    input:
        T0: float, representing the time where the step happen
        amp: float, representing the amplitude of the step
        Resolut: int, representing the resolution of the result
    return:
        a: array_like of size (1xResolut), discretization of the y-axis
        b: array_like of size (1xResolut), discretization of the x-axis
        W: array_like of size (ResolutxResolut), matrix containing the wavelet transform value at each (a,b)
    """
    a = np.linspace(0.1, 5, Resolut)
    b = np.linspace(0.1, 5, Resolut)
    W = np.zeros((Resolut, Resolut))
    
    for i in range (0,Resolut):
        for j in range (0,Resolut):
            def integrand1(t):
                output = a[i]**-0.5 * amp * exp(-(((t-b[j])/a[i])**2)/2) * cos(5*((t-b[j])/a[i]))
                return output
            W[i][j]=quad(integrand1, T0, 15)[0]
    
    return a,b,W

def Find_Rectangular_Wavelet_Two(T0,T1,amp,Resolut):
    """
    This function computes the wavelet transform of a rectangular function
    input:
        T0: float, representing the time where the first step happen
        T1: float, representing the time where the second step happen
        amp: float, representing the amplitude of the step
        Resolut: int, representing the resolution of the result
    return:
        a: array_like of size (1xResolut), discretization of the y-axis
        b: array_like of size (1xResolut), discretization of the x-axis
        W: array_like of size (ResolutxResolut), matrix containing the wavelet transform value at each (a,b)
    """
    a=np.linspace(0.1,5,Resolut)
    b=np.linspace(0.1,5,Resolut)
    W = np.zeros((Resolut, Resolut))
    
    for i in range (0,Resolut):
        for j in range (0,Resolut):
            def integrand1(t):
                output = a[i]**-0.5 * amp * exp(-(((t-b[j])/a[i])**2)/2) * cos(5*((t-b[j])/a[i]))
                return output
            W[i][j]=quad(integrand1, T0, T1)[0]

    return a,b,W

def Find_Dirac_Wavelet_Two(T0, amp,Resolut):
    """
    This function computes the wavelet transform of a dirac function
    input:
        T0: float, representing the impulse happen
        amp: float, representing the amplitude of the impulse
        Resolut: int, representing the resolution of the result
    return:
        a: array_like of size (1xResolut), discretization of the y-axis
        b: array_like of size (1xResolut), discretization of the x-axis
        W: array_like of size (ResolutxResolut), matrix containing the wavelet transform value at each (a,b)
    """
    a=np.linspace(0.1,5,Resolut)
    b=np.linspace(0.1,5,Resolut)
    W = np.zeros((Resolut, Resolut))
    
    for i in range (0,Resolut):
        for j in range (0,Resolut):
            W[i][j]= a[i]**-0.5 * amp * exp(-(((T0-b[j])/a[i])**2)/2) * cos(5*((T0-b[j])/a[i]))
    
    return a,b,W

def Find_Trig_Wavelet_Two(index, frequency, Resolut):
    """
    This function computes the wavelet transform of sin and cos functions
    input:
        index: int, defining which trigonometric function to be used {0 -> sin, 1 -> cos}
        frequency: float, representing the the frequency of the trigonometric function
        Resolut: int, representing the resolution of the result
    return:
        a: array_like of size (1xResolut), discretization of the y-axis
        b: array_like of size (1xResolut), discretization of the x-axis
        W: array_like of size (ResolutxResolut), matrix containing the wavelet transform value at each (a,b)
    """
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

    return a,b,W

def Find_Custom_Wavelet_Two(user_func,Resolut):
    """
    This function computes the wavelet transform of sin and cos functions
    input:
        user_func: string, defining the user defined function
        Resolut: int, representing the resolution of the result
    return:
        a: array_like of size (1xResolut), discretization of the y-axis
        b: array_like of size (1xResolut), discretization of the x-axis
        W: array_like of size (ResolutxResolut), matrix containing the wavelet transform value at each (a,b)
    """
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
    
    return a,b,W