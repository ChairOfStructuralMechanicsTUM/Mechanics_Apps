# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 17:59:10 2019

@author: Boulbrachene
"""
import numpy as np
from math import exp
import matplotlib.pyplot as plt

n=200
timedisc=800
t=np.linspace(-20,20,timedisc)
a=np.linspace(0.1,5,n)
x=t*np.exp(-t**2)
IntLimit= np.zeros(n)
#y= np.exp(-t**2)*np.cos(5*t)
for i in range (0,n):
#    print('a index:', i+1)
    for j in range (timedisc/2,timedisc):
        y=t[j]/a[i] * exp(-( t[j]/a[i] )**2.0)
        if (y < 1e-5):
            IntLimit[i]=t[j]
#            print a[i]
#            print t[j]
#            print y
            break
        
    
#plt.plot(t,x)
plt.plot(a,IntLimit)
#slope= (IntLimit[199] - IntLimit[100])/(a[199]-a[100])
#print slope
coefs, res, _, _, _ = np.polyfit(a,IntLimit,3, full = True)
print coefs
lim= coefs[0] + coefs[1]*a + coefs[2]*a + coefs[3]*a
plt.plot(a,lim)