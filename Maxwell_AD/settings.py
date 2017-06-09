#settings file:

def init():
    #global constants:
    global a
    global b
    global FScale           #= 150.0
    global offsetKraft      #= 0.08
    global tri_size         #= 30
    global changer          #= 0
    global shift            #= 0.01
    global shift2           #= 0.015
    global ps               #= 0.3
    global plotx0           #= 0.1-ps
    global plotxf           #= 0.8+ps
    global ploty0           #= -0.1
    global plotyf           #= 1.0
    #Arrow Sources:
    global arr_scal         #= 450.0
    global arr_lw           #= 20.0
    global ground           #= 0.07
    global orig             #= Frame("o","0")
    global f1               #= Frame("F1","n1")
    global f2               #= Frame("F2","n2")
    global default          #= dict(x = [0.1,0.8], y = [0.1,0.1], size = [tri_size,tri_size])
    #seg             = dict(x0=[0.095,0.097,0.099,0.101,0.103,0.105],
    #                x1=[0.095+shift,0.097+shift,0.099+shift,0.101+shift,0.103+shift,0.105+shift],
    #                y0=[0.09]*5, y1=[0.088]*5)
    global t_line           #= dict(x=[0.7,0.9], y=[ground,ground])

    a                = 0.5
    b                = 0.7
    FScale           = 150.0
    offsetKraft      = 0.08
    tri_size         = 30
    changer          = 0
    shift            = 0.01
    shift2           = 0.015
    ps               = 0.3
    plotx0           = 0.1-ps
    plotxf           = 0.8+ps
    ploty0           = -0.1
    plotyf           = 1.0
    #Arrow Sources:
    arr_scal         = 450.0
    arr_lw           = 20.0
    ground           = 0.07
    default          = dict(x = [0.1,0.8], y = [0.1,0.1], size = [tri_size,tri_size])
    #seg             = dict(x0=[0.095,0.097,0.099,0.101,0.103,0.105],
    #                x1=[0.095+shift,0.097+shift,0.099+shift,0.101+shift,0.103+shift,0.105+shift],
    #                y0=[0.09]*5, y1=[0.088]*5)
    t_line           = dict(x=[0.7,0.9], y=[ground,ground])
