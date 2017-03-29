# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 14:23:43 2017

@author: sam
"""

from visual import *
from random import uniform,random
from visual.controls import *

display(center=(1,0,0),background=(1,1,1), autoscale=False, range=(2,2,2),        
        width=600, height=600,  forward=(-.4,-.3,-1)) #camera position

distant_light(direction=(1,1,1), color=color.red)
n       = 2
dt      = 1./8.
position   = []
stiffness   = []
box(pos=(-1,0,0), width=2, height=2, length= 2, color=color.black)
box(pos=(0,-.36,0), width=2, height=.2, length= 5, color=color.black,opacity=.3)
for i in arange(n):
    spring  = helix(pos=(0,0,0), axis=(5,0,0), radius=0.2, color=color.red, length=1.)
    position.append(spring)
    ko      = box(pos=(0,0,0), width=.5, height=.5, length= .5, color= color.blue)
    stiffness.append(ko)

k0      = 1.
k1      = 1.

m0      = 1.
m1      = 1.

l00     = 1.
l01     = 1.

l0      = 1.
l1      = 1.1

x0      = l0
x1      = l0+l1

v0      = 0.
v1      = 0.


y = 1.
print x1
def updateposition():
    global x0,x1
    stiffness[0].x      = x0
    position[0].length = l0
    
    stiffness[1].x      = x1
    position[1].x      = l0
    position[1].length = l1

    

def process():
    global l0,v0,x0,l1,v1,x1
    #mass m0
    dx0     = l0-l00
    f0     = -k0*dx0
    dx1     = l1-l01
    f1     = -k1*dx1
    a0      = (f0-f1)/m0
    v0      += a0*dt
    x0      += v0*dt
    l0      = x0
    #mass m1
    a1      = f1/m1
    v1      += a1*dt
    x1      += v1*dt
    l1      = x1-x0
    
    
    updateposition()
    
while 1:
    rate (100)
    y   += .1
    process()