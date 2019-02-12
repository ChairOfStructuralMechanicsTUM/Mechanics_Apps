# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 00:06:39 2019

@author: Boulbrachene
"""

from scipy.integrate import quad
from sympy import sympify, lambdify
from sympy.utilities.lambdify import lambdastr

f="x^2"
print(f)

sym=sympify(f)
print(sym)

backtostr= str(sym)
print(backtostr)
print(quad(lambda x: eval(backtostr), 0, 1)[0])

lam=lambdify('x',f)
print(lam)
print(lam(2))

lambdast=lambdastr('x',f)
print(lambdast)

#quad(lambda x: lam, 0, 1)