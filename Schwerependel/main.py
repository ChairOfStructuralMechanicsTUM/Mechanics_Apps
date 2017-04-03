from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Slider, Button
from math import sin, cos

Mass = ColumnDataSource(data = dict(x=[],y=[]))
PendulumArm = ColumnDataSource(data = dict(x=[0],y=[10]))
PhaseDiagram = ColumnDataSource(data = dict(x=[[]],y=[[]], c=["blue"]))
basicPhaseDiagram = ColumnDataSource(data = dict(x=[],y=[]))
R=2.0
m=5.0
g=9.81
dt=0.1
phi=-1.0
dPhi=1.0
#lam=3.0
lam=0.0
PenduleType="Single"
#PenduleType="Double"
theta=0
dTheta=0
R2=2.0

def ddPhi(Phi,dPhi):
    return -(g*sin(Phi)+lam*dPhi/m)/R

def ddPhiDouble(phi,dPhi,theta,dTheta):
    global lam, R, m, R2, g
    return -lam*dPhi*sin(theta)**2/m+sin(theta)*(R2*(dTheta+dPhi*
        (dPhi+2*theta))/R+dPhi*cos(theta)+g*(cos(phi)*cos(theta)-sin(phi)*sin(theta))/R)

def ddThetaDouble(phi,dPhi,ddPhi1,theta,dTheta):
    global lam, R, m, R2, g
    return ddPhi1-lam*(dPhi*(1+R*cos(theta)/R2)+dTheta)-(g*(cos(phi)*sin(theta)+
        cos(theta)*sin(phi))+R*(dPhi*sin(theta)+cos(theta)*ddPhi1))/R2

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
        dPhi2 = dPhi+0.5*dt*ddPhi1
        ddTheta1 = ddThetaDouble(phi,dPhi,ddPhi1,theta,dTheta)
        theta2 = theta + dTheta*dt
        dTheta2 = dTheta + 0.5*dt*ddTheta1
        ddPhi2 = ddPhiDouble(phi2,dPhi2,theta2,dTheta2)
        ddTheta2 = ddThetaDouble(phi2,dPhi2,ddPhi2,theta2,dTheta2)
        phi+=dPhi*dt+ddPhi1*dt*dt*0.5
        theta+=dTheta*dt+ddTheta1*dt*dt*0.5
        dPhi = 0.5*dt*(ddPhi1 + ddPhi2)
        dTheta = 0.5*dt*(ddTheta1+ddTheta2)

def plot():
    global phi, dPhi, R, R2
    if (PenduleType=="Single"):
        PendulumArm.data=dict(x=[0, R*sin(phi)], y=[10,10.0-R*cos(phi)])
        Mass.data=dict(x=[R*sin(phi)],y=[10.0-R*cos(phi)])
        basicPhaseDiagram.stream(dict(x=[phi],y=[dPhi]))
    else:
        PendulumArm.data=dict(x=[0, R*sin(phi), R*sin(phi)+R2*sin(theta+phi)],
            y=[10,10.0-R*cos(phi),10.0-R*cos(phi)-R2*cos(theta+phi)])
        Mass.data=dict(x=[R*sin(phi)+R2*sin(theta+phi)],y=[10.0-R*cos(phi)-R2*cos(theta+phi)])
        basicPhaseDiagram.stream(dict(x=[theta],y=[dTheta]))

def evolve():
    getNextPoint()
    plot()

fig = figure(title="Schwerependel (Pendulum)",tools="",x_range=(-5,5),y_range=(2,12))
fig.title.text_font_size="20pt"
fig.axis.visible=False
fig.grid.visible=False
fig.outline_line_color = None
fig.line(x='x',y='y',source=PendulumArm,color="#808080")
fig.ellipse(x='x',y='y',width=1,height=1,source=Mass,color="#0065BD")

phase_diagramm = figure(title="Phasendiagramm (Phase diagram)",tools="",x_range=(-5,5),y_range=(-5,5))
phase_diagramm.title.text_font_size="20pt"
phase_diagramm.axis.major_label_text_font_size="12pt"
phase_diagramm.axis.axis_label_text_font_style="normal"
phase_diagramm.axis.axis_label_text_font_size="16pt"
phase_diagramm.xaxis.axis_label=u"\u03C6"
phase_diagramm.yaxis.axis_label=u"\u03C6\u0307"
phase_diagramm.multi_line(xs='x',ys='y',color='c',source=PhaseDiagram)
phase_diagramm.ellipse(x='x',y='y',width=0.1,height=0.1,color="blue",source=basicPhaseDiagram)
plot()

## Send to window
curdoc().add_root(row(fig,phase_diagramm))
curdoc().title = "Schwerependel"
#curdoc().add_periodic_callback(evolve,100)
