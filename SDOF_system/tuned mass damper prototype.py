from visual import *    # get VPython modules for animation

k_fric, mass = 0.005, 1.0                   # coeff. of kinetic friction, mass
F_applied, F_fric = -0.5, k_fric*mass*9.8   # applied force, friction
t, dt, x, v = 0.0, 0.01, 0.5, 0.9           # time, time step, initial position, velocity

# open window, draw cart, front/back wheels, track, velocity and acceleration texts
scene = display(title='Cart with fan on track', background=color.blue,center=(1,1))
cart = box(pos=(x, 0.15), width=0.2, height=0.2, length=0.36)
f_wheel = cylinder(pos=(x,0.05,.1), axis=(0,0,1), radius=0.05, length=0.02, color=color.black)
b_wheel = f_wheel.__copy__()
track = box(pos=(0.9, 0), width=0.3, height=0.02, length=1.8)

label(pos=(0.2,1), text='Velocity', height=20, box = 0, opacity=0, color=color.green)
label(pos=(0.3,0.7), text='Acceleration', height=20, box = 0, opacity=0, color=color.red)
v_curve = points(color=color.green)
a_curve = points(color=color.red)
s, offset = 0.29, 0.32        # scale and offset curves to fit the window

F_app_vec = arrow(pos=(x,0.1,0), axis=(-1,0,0), length=0.6)
F_fric_vec = arrow(pos=(x,0.2,0), axis=(-sign(v),0,0), length=0.4)

while (t+dt<3.1):
    if (scene.kb.keys): 
        k=scene.kb.getkey()
        k=scene.kb.getkey()
    a = (F_applied - F_fric*sign(v))/mass
    x = x + v*dt
    v = v + a*dt
    t = t + dt
    rate(100)
    cart.pos.x, f_wheel.pos.x, b_wheel.pos.x = x, x+0.1, x-0.1      # update cart position
    F_app_vec.pos.x, F_fric_vec.pos.x = x, x                        # update force arrows
    F_fric_vec.axis, F_fric_vec.length = (-sign(v),0,0), 0.4
    v_curve.append(pos=(2*s*t,s*v+3*offset))                        # plot v-t and a-t
    a_curve.append(pos=(2*s*t,s*a+2*offset))
    
from pylab import *    # get plotting functions

k_fric, mass = 0.005, 1.0                   # coeff. of kinetic friction, mass
F_applied, F_fric = -0.5, k_fric*mass*9.8   # applied force, friction
t, dt, v = 0.0, 0.01, 0.9                   # time, time step, initial velocity

time, vel, accel = [ ], [ ], [ ]            # declare time, velocity, accel lists

while (t+dt<3.0):        # loop for 3 seconds
    a = (F_applied - F_fric*sign(v))/mass   # acceleration
    v = v + a*dt         # update velocity
    t = t + dt
    time.append(t), vel.append(v), accel.append(a)   # store time, vel, and accel
    
figure()                 # plot v-t data
plot(time, vel)  
xlabel('Time (s)'), ylabel('Velocity (m/s)')  

figure()                 # plot a-t data
plot(time, accel)    
xlabel('Time (s)'), ylabel('Acceleration (m/s$^2$)') 
ylim(-0.6, 0.0)          # set y-axis limits

show()                   # display figures
