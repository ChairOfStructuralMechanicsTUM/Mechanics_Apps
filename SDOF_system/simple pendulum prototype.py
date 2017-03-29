from __future__ import print_function, division
from visual import *
from visual.graph import *

L0=.1 #the natural length of the spring
k=15 #spring constant

#the holder is the top plate for the spring
holder= box(pos=vector(-.1,.1,0), size=vector(.1,.005,.1))

#the ball and the spring should be obvious
#note that the ball has a trail
ball=sphere(pos=vector(-.1,-L0+.1,0), radius=0.02, color=color.red, make_trail=true)
spring=helix(pos=holder.pos, axis=ball.pos-holder.pos, radius=.02, coils=10)

ball.m=0.1 #mass of the ball in kg
ball.p=ball.m*vector(0,0,0) #starting momentum mass times velocity

dr=vector(0,-0.05,0) #this is the displacement of the spring
ball.pos=ball.pos+dr

g=vector(0,-9.8,0) #gravitational field
t=0
dt=0.01 #size of the time step

#putting the loop as "while True" means it runs forever
#you could change this to while t< 10: or something
while t<3: 
    rate(100) #this says 100 calculations per second
    
    #L is the length of the spring, from the holder to the ball
    L=ball.pos-holder.pos
    
    #remember that mag(R) gives the magnitude of vector R
    #remember that norm(R) gives the unit vector for R
    Fs=-k*(mag(L)-L0)*norm(L) #this is Hooke's law
    
    #this calculates the net force
    F=Fs+ball.m*g
    
    #update the momentum
    ball.p=ball.p+F*dt
    
    #update the position of the ball
    ball.pos= ball.pos +ball.p*dt/ball.m
    #this next line updates the spring
    spring.axis=ball.pos-holder.pos
    


