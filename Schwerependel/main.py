from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Slider, Button, RadioButtonGroup
from math import sin, cos, pi

Mass = ColumnDataSource(data = dict(x=[],y=[]))
PendulumArm = ColumnDataSource(data = dict(x=[0],y=[10]))
#PhaseDiagram = ColumnDataSource(data = dict(x=[[]],y=[[]], c=["blue"]))
basicPhaseDiagram = ColumnDataSource(data = dict(x=[],y=[]))
currentPoint = ColumnDataSource(data = dict(x=[],y=[]))
R=4.0
m=5.0
g=9.81
dt=0.1
phi=-1.0
dPhi=0.0
lam=0.0
PenduleType="Single"
theta=0
dTheta=0
R2=2.0
Active=True

def ddPhi(Phi,dPhi):
    return -(g*sin(Phi)+lam*dPhi/m)/R

def ddPhiDouble(phi,dPhi,theta,dTheta):
    global lam, R, m, g
    return g*cos(phi+theta)*sin(theta)/R-lam*dPhi*sin(theta)**2/m

def ddThetaDouble(phi,dPhi,ddPhi1,theta,dTheta):
    global lam, R, m, R2, g
    return -(ddPhi1+R*(dPhi*dPhi*sin(theta)+(ddPhi1+lam*dPhi/m)*cos(theta))/R2+
        lam*(dTheta+dPhi)/m+g*sin(phi+theta)/R2)

def getNextPointSingle():
    global phi, dPhi, dt
    a=ddPhi(phi,dPhi)
    oldPhi=phi
    phi+=dPhi*dt+a*dt*dt*0.5
    dPhi+=0.5*dt*a+0.5*dt*ddPhi(oldPhi+dPhi*dt,dPhi+0.5*dt*a)
    if (phi>pi):
        phi-=2*pi
    if (phi<-pi):
        phi+=2*pi

def getNextPointDouble():
    global phi, dPhi, theta, dTheta, dt
    ddPhi1 = ddPhiDouble(phi,dPhi,theta,dTheta)
    phi2 = phi+dPhi*dt
    dPhi2 = dPhi+dt*ddPhi1
    ddTheta1 = ddThetaDouble(phi,dPhi,ddPhi1,theta,dTheta)
    theta2 = theta + dTheta*dt
    dTheta2 = dTheta + dt*ddTheta1
    ddPhi2 = ddPhiDouble(phi2,dPhi2,theta2,dTheta2)
    ddTheta2 = ddThetaDouble(phi2,dPhi2,ddPhi2,theta2,dTheta2)
    phi+=dPhi*dt+ddPhi1*dt*dt*0.5
    theta+=dTheta*dt+ddTheta1*dt*dt*0.5
    dPhi += 0.5*dt*(ddPhi1 + ddPhi2)
    dTheta += 0.5*dt*(ddTheta1+ddTheta2)
    if (theta>pi):
        theta-=2*pi
    if (theta<-pi):
        theta+=2*pi
    if (phi>pi):
        phi-=2*pi
    if (phi<-pi):
        phi+=2*pi

"""
def getNextPoint():
    global phi, dPhi, dt
    if (PenduleType=="Single"):
        a=ddPhi(phi,dPhi)
        oldPhi=phi
        phi+=dPhi*dt+a*dt*dt*0.5
        dPhi+=0.5*dt*a+0.5*dt*ddPhi(oldPhi+dPhi*dt,dPhi+0.5*dt*a)
    else:
        global theta, dTheta
        ddPhi1 = ddPhiDouble(phi,dPhi,theta,dTheta)
        phi2 = phi+dPhi*dt
        dPhi2 = dPhi+dt*ddPhi1
        ddTheta1 = ddThetaDouble(phi,dPhi,ddPhi1,theta,dTheta)
        theta2 = theta + dTheta*dt
        dTheta2 = dTheta + dt*ddTheta1
        ddPhi2 = ddPhiDouble(phi2,dPhi2,theta2,dTheta2)
        ddTheta2 = ddThetaDouble(phi2,dPhi2,ddPhi2,theta2,dTheta2)
        phi+=dPhi*dt+ddPhi1*dt*dt*0.5
        theta+=dTheta*dt+ddTheta1*dt*dt*0.5
        dPhi += 0.5*dt*(ddPhi1 + ddPhi2)
        dTheta += 0.5*dt*(ddTheta1+ddTheta2)
        if (theta>pi):
            theta-=2*pi
        if (theta<-pi):
            theta+=2*pi
    if (phi>pi):
        phi-=2*pi
    if (phi<-pi):
        phi+=2*pi
"""

def plotSingle():
    global phi, dPhi, R, PendulumArm, Mass, basicPhaseDiagram
    PendulumArm.data=dict(x=[0, R*sin(phi)], y=[10,10.0-R*cos(phi)])
    Mass.data=dict(x=[R*sin(phi)],y=[10.0-R*cos(phi)])
    basicPhaseDiagram.stream(dict(x=[phi],y=[dPhi]))

def plotDouble():
    global phi, dPhi, theta, R, PendulumArm, Mass, basicPhaseDiagram
    PendulumArm.data=dict(x=[0, R*sin(phi), R*sin(phi)+R2*sin(theta+phi)],
        y=[10,10.0-R*cos(phi),10.0-R*cos(phi)-R2*cos(theta+phi)])
    Mass.data=dict(x=[R*sin(phi)+R2*sin(theta+phi)],y=[10.0-R*cos(phi)-R2*cos(theta+phi)])
    basicPhaseDiagram.stream(dict(x=[phi],y=[dPhi]))

"""
def plot():
    global phi, dPhi, R, R2
    if (PenduleType=="Single"):
        PendulumArm.data=dict(x=[0, R*sin(phi)], y=[10,10.0-R*cos(phi)])
        Mass.data=dict(x=[R*sin(phi)],y=[10.0-R*cos(phi)])
    else:
        global theta
        PendulumArm.data=dict(x=[0, R*sin(phi), R*sin(phi)+R2*sin(theta+phi)],
            y=[10,10.0-R*cos(phi),10.0-R*cos(phi)-R2*cos(theta+phi)])
        Mass.data=dict(x=[R*sin(phi)+R2*sin(theta+phi)],y=[10.0-R*cos(phi)-R2*cos(theta+phi)])
    basicPhaseDiagram.stream(dict(x=[phi],y=[dPhi]))
"""

def evolve():
    getNextPoint()
    currentPoint.data=dict(x=[phi],y=[dPhi])
    plot()

plot=plotSingle
getNextPoint=getNextPointSingle

fig = figure(title="Schwerependel (Pendulum)",tools="",x_range=(-4.5,4.5),y_range=(3,12),width=500,height=500)
fig.title.text_font_size="20pt"
fig.axis.visible=False
fig.grid.visible=False
fig.outline_line_color = None
fig.line(x='x',y='y',source=PendulumArm,color="#808080")
fig.ellipse(x='x',y='y',width=1,height=1,source=Mass,color="#0065BD")

phase_diagramm = figure(title="Phasendiagramm (Phase diagram)",tools="",x_range=(-3.14,3.14),y_range=(-5,5))
phase_diagramm.title.text_font_size="20pt"
phase_diagramm.axis.major_label_text_font_size="12pt"
phase_diagramm.axis.axis_label_text_font_style="normal"
phase_diagramm.axis.axis_label_text_font_size="16pt"
phase_diagramm.xaxis.axis_label=u"\u03C6"
phase_diagramm.yaxis.axis_label=u"\u03C6\u0307"
#phase_diagramm.multi_line(xs='x',ys='y',color='c',source=PhaseDiagram)
phase_diagramm.ellipse(x='x',y='y',width=0.1,height=0.1,color="#0065BD",source=basicPhaseDiagram)
phase_diagramm.ellipse(x='x',y='y',width=0.2,height=0.2,color="#E37222",source=currentPoint)
plot()

def play():
    global Active
    if (not Active):
        curdoc().add_periodic_callback(evolve,100)
        Active=True
Play_button = Button(label="Play",button_type="success")
Play_button.on_click(play)

def stop():
    global Active, phi0_input, phi, dphi0_input, dPhi
    if (Active):
        curdoc().remove_periodic_callback(evolve)
        Active=False
        phi0_input.value=phi
        dphi0_input.value=dPhi
        
Stop_button = Button(label="Stop",button_type="success")
Stop_button.on_click(stop)

def change_mass(attr,old,new):
    global m
    m=new
## Create slider to choose mass of blob
mass_input = Slider(title="Masse (mass) [kg]", value=5, start=0.5, end=10.0, step=0.1,width=200)
mass_input.on_change('value',change_mass)

def change_lam(attr,old,new):
    global lam
    lam=new
## Create slider to choose damper coefficient
lam_input = Slider(title=u"D\u00E4mpfungskonstante (Damper Coefficient) [N*s/m]", value=0.0, start=0.0, end=5.0, step=0.2,width=400)
lam_input.on_change('value',change_lam)

def change_phi0(attr,old,new):
    global Active, phi, phi0_input
    if (not Active):
        phi=new
        plot()
## Create slider to choose damper coefficient
phi0_input = Slider(title=u"\u03C6\u2080", value=0.0, start=-3.0, end=3.0, step=0.2,width=200)
phi0_input.on_change('value',change_phi0)

def change_phi0dot(attr,old,new):
    global Active, dPhi, dphi0_input
    if (not Active):
        stop()
        dPhi=new
        plot()
## Create slider to choose damper coefficient
dphi0_input = Slider(title=u"\u03C6\u0307\u2080", value=0.0, start=-5.0, end=5.0, step=0.5,width=200)
dphi0_input.on_change('value',change_phi0dot)

def swapPendulumType(attr,old,new):
    global plot, getNextPoint, R, dt
    if (new==0):
        plot=plotSingle
        getNextPoint=getNextPointSingle
        R=4.0
        dt=0.1
    elif(new==1):
        plot=plotDouble
        getNextPoint=getNextPointDouble
        R=2.0
        dt=0.05

pendulum_type_input = RadioButtonGroup(
        labels=["Single Pendulum", "Double Pendulum"], active=0)
pendulum_type_input.on_change('active',swapPendulumType)

## Send to window
curdoc().add_root(column(row(column(fig,row(Play_button,Stop_button),pendulum_type_input),phase_diagramm),row(mass_input,lam_input,phi0_input,dphi0_input)))
curdoc().title = "Schwerependel"
curdoc().add_periodic_callback(evolve,100)
