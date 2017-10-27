from MoveMassTool import *
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Slider, Button, RadioButtonGroup, Arrow, OpenHead, Div
from bokeh.events import Pan
from math import sin, cos, pi, atan2, sqrt, acos
from mpmath import csc
from os.path import dirname, join, split

# create column data sources
Mass = ColumnDataSource(data = dict(x=[],y=[]))
PendulumArm = ColumnDataSource(data = dict(x=[0],y=[10]))
PendulumElbow = ColumnDataSource(data = dict(x=[],y=[]))
basicPhaseDiagram = ColumnDataSource(data = dict(x=[],y=[]))
currentPoint = ColumnDataSource(data = dict(x=[],y=[]))
KinEnergySource = ColumnDataSource(data = dict(x=[],y=[]))
OtherEnergySource = ColumnDataSource(data = dict(x=[],y=[]))
PhiAngle = ColumnDataSource(data=dict(x=[],y=[]))
PhiAngleText = ColumnDataSource(data=dict(x=[],y=[],t=[]))
dPhiArrow = ColumnDataSource(data=dict(xs=[],xe=[],ys=[],ye=[]))
dPhiArrowText = ColumnDataSource(data=dict(x=[],y=[],t=[]))
# create characteristic properties
R=4.0
m=5.0
g=9.81
dt=0.1
phi=0.5
dPhi=1.0
lam=0.0
theta=0
dTheta=0
R2=2.0
# create values that control later behaviour
Active=True
inMass=False
massSelected=False
bentDirection=0
TotEng=0
# create values to disable phi0 and dphi0 slider
Phi0=0.0
dPhi0=0.0

def drawPhiAngle():
    global PhiAngle, PhiAngleText, dPhiArrow, dPhiArrowText, phi, dPhi
    X=[]
    Y=[]
    for i in range(0,6):
        X.append(0.5*sin(i*phi/5.0))
        Y.append(10.0-0.5*cos(i*phi/5.0))
    X.append(X[4])
    Y.append(Y[5])
    X.append(X[5])
    Y.append(Y[5])
    X.append(X[5])
    Y.append(Y[4])
    PhiAngle.data=dict(x=X,y=Y)
    if (X[2]>=0):
        PhiAngleText.data=dict(x=[X[2]],y=[Y[2]-0.1],t=[u"\u03C6"])
    else:
        PhiAngleText.data=dict(x=[X[2]],y=[Y[2]-0.1],t=[u"-\u03C6"])
    if (plot==plotSingle):
        X=Mass.data['x'][0]
        Y=Mass.data['y'][0]
    else:
        X=PendulumElbow.data['x'][0]
        Y=PendulumElbow.data['y'][0]
    Xe=X+dPhi*cos(phi)
    Ye=Y+dPhi*sin(phi)
    dPhiArrow.data=dict(xs=[X],xe=[Xe],ys=[Y],ye=[Ye])
    if (Xe>X):
        dPhiArrowText.data=dict(x=[Xe],y=[Ye],t=[u"\u03C6\u0307"])
        dPhiText.glyph.text_align="left"
    else:
        dPhiArrowText.data=dict(x=[Xe],y=[Ye],t=[u"-\u03C6\u0307"])
        dPhiText.glyph.text_align="right"

def removePhiAngle():
    global PhiAngle, PhiAngleText, dPhiArrow, dPhiArrowText
    PhiAngle.data=dict(x=[],y=[])
    PhiAngleText.data=dict(x=[],y=[],t=[])
    dPhiArrow.data=dict(xs=[],xe=[],ys=[],ye=[])
    dPhiArrowText.data=dict(x=[],y=[],t=[])    

# return total energy
def getTotEng():
    global getCurrentXY, g, getKinEng
    (X,Y)=getCurrentXY()
    potEng=g*m*(Y-6.0)
    kinEng=getKinEng()
    return potEng+kinEng

# return kinetic energy for simple pendulum
def getKinEngSingle():
    return 0.5*m*R*R*dPhi*dPhi

# return kinetic energy for double pendulum
def getKinEngDouble():
    return 0.5*m*((R*dPhi*sin(theta))**2+(R*dPhi*cos(theta)+R2*(dTheta+dPhi))**2)

# return double derivative of phi for a single pendulum
def ddPhi(Phi,dPhi):
    global g, lam, m, R
    return -(g*sin(Phi)+lam*dPhi/m)/R

# return double derivative of phi for a double pendulum
def ddPhiDouble(phi,dPhi,theta,dTheta):
    global lam, R, m, g, R2
    if (theta==0):
        return 0
    else:
        return float(((g*cos(phi+theta)+R2*(dTheta+dPhi)**2)/R+dPhi*(dPhi*cos(theta)-lam*sin(theta)/m))/(sin(theta)+csc(theta)))

# return double derivative of theta for a double pendulum
def ddThetaDouble(phi,dPhi,ddPhi1,theta,dTheta):
    global lam, R, m, R2, g
    return -(ddPhi1+R*(dPhi*dPhi*sin(theta)+(ddPhi1+lam*dPhi/m)*cos(theta))/R2+
        lam*(dTheta+dPhi)/m+g*sin(phi+theta)/R2)

# get new angles after timestep for a single pendulum
def getNextPointSingle(dt):
    global phi, dPhi
    # find acceleration
    a=ddPhi(phi,dPhi)
    # update phi using Taylor expansion
    phi+=dPhi*dt+a*dt*dt*0.5
    # update derivative of phi using Heun
    dPhi+=0.5*dt*(a+ddPhi(phi,dPhi+dt*a))
    # if phi not in [-pi,pi], put it back
    if (phi>pi):
        phi-=2*pi
    if (phi<-pi):
        phi+=2*pi
    return getKinEngSingle()

# get new angles after timestep for a double pendulum
def getNextPointDouble(dt):
    global phi, dPhi, theta, dTheta
    # calculate current double derivative of angles
    ddPhi1 = ddPhiDouble(phi,dPhi,theta,dTheta)
    ddTheta1 = ddThetaDouble(phi,dPhi,ddPhi1,theta,dTheta)
    # calculate new angle using Taylor expansion
    phi+= dPhi*dt+0.5*dt*dt*ddPhi1
    theta+= dTheta*dt+0.5*dt*dt*ddTheta1
    # approximate new first derivative of angle
    dPhi2 = dPhi+dt*ddPhi1
    dTheta2 = dTheta + dt*ddTheta1
    # use approximation of first derivative of angle to find new double derivative of angles
    ddPhi2 = ddPhiDouble(phi,dPhi2,theta,dTheta2)
    ddTheta2 = ddThetaDouble(phi,dPhi2,ddPhi2,theta,dTheta2)
    # update first derivative of angle using Heun
    dPhi += 0.5*dt*(ddPhi1 + ddPhi2)
    dTheta += 0.5*dt*(ddTheta1+ddTheta2)
    # theta and phi should be in [-pi,pi], if this is not the case, put them back
    if (theta>pi):
        theta-=2*pi
    if (theta<-pi):
        theta+=2*pi
    if (phi>pi):
        phi-=2*pi
    if (phi<-pi):
        phi+=2*pi
    return getKinEngDouble()

# plot the single pendulum
def plotSingle():
    global phi, dPhi, R, PendulumArm, Mass, basicPhaseDiagram, TotEng
    PendulumArm.data=dict(x=[0, R*sin(phi)], y=[10,10.0-R*cos(phi)])
    Mass.data=dict(x=[R*sin(phi)],y=[10.0-R*cos(phi)])
    basicPhaseDiagram.stream(dict(x=[phi],y=[dPhi]))
    K=getKinEngSingle()*9.0/TotEng-4.5
    KinEnergySource.data=dict(x=[-4.5,-4.5, K, K], y=[12,11.5,11.5,12])
    OtherEnergySource.data=dict(x=[K, K, 4.5, 4.5], y=[12,11.5,11.5,12])
    currentPoint.data=dict(x=[phi],y=[dPhi])

# plot the double pendulum
def plotDouble():
    global phi, dPhi, theta, R, PendulumArm, Mass, basicPhaseDiagram, TotEng
    PendulumArm.data=dict(x=[0, R*sin(phi), R*sin(phi)+R2*sin(theta+phi)],
        y=[10,10.0-R*cos(phi),10.0-R*cos(phi)-R2*cos(theta+phi)])
    PendulumElbow.data=dict(x=[R*sin(phi)],y=[10.0-R*cos(phi)])
    Mass.data=dict(x=[R*sin(phi)+R2*sin(theta+phi)],y=[10.0-R*cos(phi)-R2*cos(theta+phi)])
    basicPhaseDiagram.stream(dict(x=[phi],y=[dPhi]))
    K=getKinEngDouble()*9.0/TotEng-4.5
    KinEnergySource.data=dict(x=[-4.5,-4.5, K, K], y=[12,11.5,11.5,12])
    OtherEnergySource.data=dict(x=[K, K, 4.5, 4.5], y=[12,11.5,11.5,12])
    currentPoint.data=dict(x=[phi],y=[dPhi])

# get position of mass in single pendulum
def getCurrentXYSingle():
    global R, sin, theta
    X=R*sin(phi)
    Y=10-R*cos(phi)
    return (X,Y)

# get position of mass in double pendulum
def getCurrentXYDouble():
    global R, R2, sin, theta
    X=R*sin(phi)+R2*sin(phi+theta)
    Y=10-R*cos(phi)-R2*cos(phi+theta)
    return (X,Y)

# function which carries out timestep
def evolve():
    global getNextPoint, currentPoint, phi, dPhi, plot, dt
    K=getNextPoint(dt)
    #if (K>TotEng):
    #    print K, "  >  ", TotEng
    plot()
    if (getTotEng()<1e-4):
        global Active
        Active=False
        curdoc().remove_periodic_callback(evolve)

# function to move the mass by clicking it
def on_mouse_move(event):
    global Active, TotEng
    if (not Active):
        moveTo(event.x,event.y)
        TotEng=getTotEng()
        plot()
        drawPhiAngle()

# function which moves mass to new angle for single pendulum
def moveToSingle(X,Y):
    global phi
    phi=atan2(X,10-Y)
    plot()

# function which moves mass to new position for double pendulum
def moveToDouble(X,Y):
    global phi, theta, bentDirection, R
    r=sqrt((10.0-Y)**2+X**2)/2.0
    # if the mouse is outside the region of possible positions
    if (r>=R):
        # then the pendulum is taut
        theta=0
        phi=atan2(X,10-Y)
        bentDirection=0
    # else it is bent
    else:
        # if the direction of the bending has not been chosen
        if (bentDirection==0):
            # choose such that it is in the direction indicated by gravity
            bentDirection=-X/abs(X)
        # if it has been chosen then it should not flip arbitrarily at x=0
        # find angle from origin to mass
        bigAngle=atan2(X,10-Y)
        # find deviation from bigAngle due to bending of pendulum arm
        littleAngle=bentDirection*acos(r/R)
        phi=bigAngle+littleAngle
        theta=-2*littleAngle
    # draw new position
    plot()

# store function handles (this avoids using excessive if/else statements)
plot=plotSingle
getNextPoint=getNextPointSingle
getCurrentXY=getCurrentXYSingle
moveTo=moveToSingle
getKinEng=getKinEngSingle

# draw pendulum diagram
fig = figure(title="Kinetic energy balance",tools="",x_range=(-4.5,4.5),y_range=(3,12),width=500,height=500)
fig.add_tools(MoveMassTool())
fig.on_event(Pan, on_mouse_move)
fig.title.text_font_size="16pt"
fig.axis.visible=False
fig.grid.visible=False
fig.outline_line_color = None
fig.line(x='x',y='y',source=PendulumArm,color="#808080")
fig.ellipse(x='x',y='y',width=0.1,height=0.1,source=PendulumElbow,color="#808080")
fig.ellipse(x='x',y='y',width=1,height=1,source=Mass,color="#0065BD")
fig.patch(x='x',y='y',source=KinEnergySource,color="#E37222")
fig.patch(x='x',y='y',source=OtherEnergySource,color="#808080")
fig.line(x='x',y='y',source=PhiAngle,color="black")
fig.text(x='x',y='y',text='t',source=PhiAngleText,color="black",text_baseline="top",text_align="center")
arrow_glyph = Arrow(end=OpenHead(line_color="black",line_width=2,size=6),
    x_start='xs', y_start='ys', x_end='xe', y_end='ye',source=dPhiArrow,
    line_color="black",line_width=2)
fig.add_layout(arrow_glyph)
dPhiText = fig.text(x='x',y='y',text='t',source=dPhiArrowText,color="black",text_align="left")

# draw phase diagram
phase_diagramm = figure(title="Phase diagram",tools="",x_range=(-3.14,3.14),y_range=(-5,5))
phase_diagramm.title.text_font_size="16pt"
phase_diagramm.axis.major_label_text_font_size="12pt"
phase_diagramm.axis.axis_label_text_font_style="normal"
phase_diagramm.axis.axis_label_text_font_size="12pt"
phase_diagramm.xaxis.axis_label=u"\u03C6 [rad]"
phase_diagramm.yaxis.axis_label=u"\u03C6\u0307 [rad/s]"
phase_diagramm.ellipse(x='x',y='y',width=0.02,height=0.02,color="#0065BD",source=basicPhaseDiagram)
phase_diagramm.ellipse(x='x',y='y',width=0.2,height=0.2,color="#E37222",source=currentPoint)

TotEng=getTotEng()
plot()

# add control buttons
def play():
    global Active
    if (not Active):
        removePhiAngle()
        curdoc().add_periodic_callback(evolve,100)
        Active=True
Play_button = Button(label="Play",button_type="success",width=150)
Play_button.on_click(play)

def stop():
    global Active, phi0_input, phi, dphi0_input, dPhi, dTheta
    if (Active):
        curdoc().remove_periodic_callback(evolve)
        Active=False
        phi0_input.value=phi
        dphi0_input.value=dPhi
    dTheta=0
        
Stop_button = Button(label="Stop",button_type="success",width=150)
Stop_button.on_click(stop)

def reset():
    global Active, phi0_input, phi, dphi0_input, dPhi, basicPhaseDiagram, dTheta
    phi=0.5
    dPhi=1
    if (Active):
        curdoc().remove_periodic_callback(evolve)
        Active=False
    mass_input.value=5.0
    lam_input.value=0.0
    phi0_input.value=phi
    dphi0_input.value=dPhi
    dTheta=0
    basicPhaseDiagram.data=dict(x=[],y=[])
        
Reset_button = Button(label="Reset",button_type="success",width=150)
Reset_button.on_click(reset)

def change_mass(attr,old,new):
    global m, TotEng
    m=new
    TotEng=getTotEng()
    plot()
## Create slider to choose mass of blob
mass_input = Slider(title="Mass [kg]", value=5, start=0.5, end=10.0, step=0.1,width=200)
mass_input.on_change('value',change_mass)

def change_lam(attr,old,new):
    global lam
    lam=new
## Create slider to choose damper coefficient
lam_input = Slider(title=u"Damper coefficient [N*s/m]", value=0.0, start=0.0, end=5.0, step=0.2,width=400)
lam_input.on_change('value',change_lam)

def change_phi0(attr,old,new):
    global Active, phi, phi0_input, TotEng, Phi0
    if (not Active):
        phi=new
        TotEng=getTotEng()
        plot()
        Phi0=new
        drawPhiAngle()
    elif (Phi0!=new):
        phi0_input.value=Phi0
## Create slider to choose damper coefficient
phi0_input = Slider(title=u"\u03C6\u2080 [rad]", value=0.0, start=-3.0, end=3.0, step=0.2,width=200)
phi0_input.on_change('value',change_phi0)

def change_phi0dot(attr,old,new):
    global Active, dPhi, dphi0_input,TotEng, dPhi0
    if (not Active):
        stop()
        dPhi=new
        TotEng=getTotEng()
        plot()
        dPhi=new
        drawPhiAngle()
    elif (dPhi0!=new):
        dphi0_input.value=dPhi0
## Create slider to choose damper coefficient
dphi0_input = Slider(title=u"\u03C6\u0307\u2080 [rad/s]", value=0.0, start=-5.0, end=5.0, step=0.5,width=200)
dphi0_input.on_change('value',change_phi0dot)

# create selector for pendulum type which updates function handles and appropriate properties
def swapPendulumType(attr,old,new):
    global plot, getNextPoint, getCurrentXY, moveTo, getKinEng, R, dt, TotEng, theta, dTheta
    if (new==0):
        # if single pendulum
        plot=plotSingle
        getNextPoint=getNextPointSingle
        getCurrentXY=getCurrentXYSingle
        moveTo=moveToSingle
        getKinEng=getKinEngSingle
        R=4.0
        dt=0.1
        PendulumElbow.data=dict(x=[],y=[])
    elif(new==1):
        # if double pendulum
        plot=plotDouble
        getNextPoint=getNextPointDouble
        getCurrentXY=getCurrentXYDouble
        moveTo=moveToDouble
        getKinEng=getKinEngDouble
        R=2.0
        dt=0.05
    theta=0
    dTheta=0
    TotEng=getTotEng()
    plot()
    if (not Active):
        drawPhiAngle()

pendulum_type_input = RadioButtonGroup(
        labels=["Single pendulum", "Double pendulum"], active=0)
pendulum_type_input.on_change('active',swapPendulumType)

# add app description
description_filename = join(dirname(__file__), "description.html")
description = Div(text=open(description_filename).read(), render_as_text=False, width=1200)

## Send to window
hspace = 20
curdoc().add_root(column(description, row(column(fig,row(Play_button,Spacer(width=hspace),Stop_button,Spacer(width=hspace),Reset_button),pendulum_type_input),phase_diagramm), \
    row(mass_input,Spacer(width=hspace),lam_input,Spacer(width=hspace),phi0_input,Spacer(width=hspace),dphi0_input)))
curdoc().add_periodic_callback(evolve,100)
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
