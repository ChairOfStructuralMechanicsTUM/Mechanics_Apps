import numpy as np
from scipy.integrate import quad
from math import sin, cos, pi, exp
import time

def Find_Heaviside_SWT(T0,amp,Resolut):
    tic = time.time()
    # computation of WT
    a = np.linspace(0.1, 5, Resolut)
    b = np.linspace(0.1, 5, Resolut)
    W = np.zeros((Resolut, Resolut))
    ###############################################
    # timedisc=600
    # CompT=np.linspace(-20,20,timedisc)
    # IntLimit= np.zeros(Resolut)
    # for i in range (0,Resolut):
    #     for j in range (300 ,timedisc):
    #         y=CompT[j]/a[i] * exp(-( CompT[j]/a[i] )**2.0)
    #         if (y < 0.00001):
    #             IntLimit[i]=CompT[j]
    #             break
    ###############################################

    for i in range (0,Resolut):
        for j in range (0,Resolut):
            def integrand1(t):
                output = a[i]**-0.5 * amp * (t-b[j])/a[i] * exp(-( (t-b[j])/a[i] )**2.0)
                return output
            W[i][j]=quad(integrand1, T0, 15)[0]

    toc = time.time()
    print (str(toc-tic) + ' sec Elapsed' )
    return a,b,W

def Find_Rectangular_SWT(T0,T1,amp,Resolut):
    # computation of WT
    tic = time.time()
    a=np.linspace(0.1,5,Resolut)
    b=np.linspace(0.1,5,Resolut)
    W=np.zeros((Resolut, Resolut))
    for i in range (0,Resolut):
        for j in range (0,Resolut):
            def integrand1(t):
                output = a[i]**-0.5 * amp * (t-b[j])/a[i] * exp(-( (t-b[j])/a[i] )**2.0)
                return output
            W[i][j]=quad(integrand1, T0, T1)[0]

    toc = time.time()
    print (str(toc-tic) + ' sec Elapsed' )
    return a,b,W


def Find_Dirac_SWT(T0, amp,Resolut):
    # computation of WT
    a=np.linspace(0.1,5,Resolut)
    b=np.linspace(0.1,5,Resolut)
    W=np.zeros((Resolut, Resolut))

    for i in range (0,Resolut):
        for j in range (0,Resolut):
            W[i][j]= a[i]**-0.5 * amp * (T0-b[j])/a[i] * exp(-( (T0-b[j])/a[i] )**2.0)
    return a,b,W


def Find_Trig_SWT(index, frequency, Resolut):
    tic = time.time()
    a=np.linspace(0.1,5,Resolut)
    b=np.linspace(0.1,5,Resolut)
    W=np.zeros((Resolut, Resolut))

    if (index == 0):

        for i in range (0,Resolut):
            for j in range (0,Resolut):
                def integrand1(t):
                    output = a[i]**-0.5 * np.sin(2 * np.pi * frequency * t) * (t-b[j])/a[i] * exp(-( (t-b[j])/a[i] )**2.0)
                    return output
                W[i][j]=quad(integrand1, -10, 15)[0]

    else:
        for i in range (0,Resolut):
            for j in range (0,Resolut):
                def integrand1(t):
                    output = a[i]**-0.5 * np.cos(2 * np.pi * frequency * t) * (t-b[j])/a[i] * exp(-( (t-b[j])/a[i] )**2.0)
                    return output
                W[i][j]=quad(integrand1, -10, 15)[0]
    
    toc = time.time()
    print (str(toc-tic) + ' sec Elapsed' )
    return a,b,W


def Find_Custom_SWT(user_func,Resolut):
    tic = time.time()
    a=np.linspace(0.1,5,Resolut)
    b=np.linspace(0.1,5,Resolut)
    W=np.zeros((Resolut, Resolut))
    #coefs = np.array([ 9.30997155e-05, -9.61148864e-04,  3.57882087e+00,  2.28956214e-02])
   
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
                    return a_i**-0.5 * eval(user_func, safe_dict) * (t-b_j)/a_i * exp(-( (t-b_j)/a_i )**2.0)
                except NameError:
                    pass
            #W[i][j]=quad(integrand, -(coefs[0] + coefs[1]*a[i] + coefs[2]*a[i] + coefs[3]*a[i]),  coefs[0] + coefs[1]*a[i] + coefs[2]*a[i] + coefs[3]*a[i])[0]
            W[i][j]=quad(integrand, -10, 15)[0]
    toc = time.time()
    print (str(toc-tic) + ' sec Elapsed' )
    return a,b,W