from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Slider, Button, RadioButtonGroup, Arrow, OpenHead#, Div
from bokeh.events import Pan
from math import sin, cos, pi, atan2, sqrt, acos
from mpmath import csc
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv, LatexSlider

# create column data sources
Mass              = ColumnDataSource(data = dict(x=[],y=[]))
PendulumArm       = ColumnDataSource(data = dict(x=[0],y=[10]))
PendulumElbow     = ColumnDataSource(data = dict(x=[],y=[]))
basicPhaseDiagram = ColumnDataSource(data = dict(x=[],y=[]))
currentPoint      = ColumnDataSource(data = dict(x=[],y=[]))
KinEnergySource   = ColumnDataSource(data = dict(x=[],y=[]))
OtherEnergySource = ColumnDataSource(data = dict(x=[],y=[]))
PhiAngle          = ColumnDataSource(data=dict(x=[],y=[]))
PhiAngleText      = ColumnDataSource(data=dict(x=[],y=[],t=[]))
dPhiArrow         = ColumnDataSource(data=dict(xs=[],xe=[],ys=[],ye=[]))
dPhiArrowText     = ColumnDataSource(data=dict(x=[],y=[],t=[]))
# create characteristic properties
g           = 9.81 # constant, global scope
R2          = 2.0  # constant, global scope
glob_R      = ColumnDataSource(data=dict(val=[4.0]))
glob_m      = ColumnDataSource(data=dict(val=[5.0]))
glob_dt     = ColumnDataSource(data=dict(val=[0.1]))
glob_phi    = ColumnDataSource(data=dict(val=[0.5]))
glob_dPhi   = ColumnDataSource(data=dict(val=[1.0]))
glob_lam    = ColumnDataSource(data=dict(val=[0.0]))
glob_theta  = ColumnDataSource(data=dict(val=[0]))
glob_dTheta = ColumnDataSource(data=dict(val=[0]))
# create values that control later behaviour
inMass             = False
massSelected       = False
glob_bentDirection = ColumnDataSource(data=dict(val=[0]))
glob_TotEng        = ColumnDataSource(data=dict(val=[0]))
glob_active        = ColumnDataSource(data=dict(Active=[False]))
glob_callback      = ColumnDataSource(data=dict(cid=[None]))
# create values to disable phi0 and dphi0 slider
glob_Phi0  = ColumnDataSource(data=dict(val=[0.0]))
glob_dPhi0 = ColumnDataSource(data=dict(val=[0.0]))
# global function handels
glob_fun_plot         = ColumnDataSource(data=dict(fun=[]))
glob_fun_getNextPoint = ColumnDataSource(data=dict(fun=[]))
glob_fun_getCurrentXY = ColumnDataSource(data=dict(fun=[]))
glob_fun_moveTo       = ColumnDataSource(data=dict(fun=[]))
glob_fun_getKinEng    = ColumnDataSource(data=dict(fun=[]))

def drawPhiAngle():
    [plot] = glob_fun_plot.data["fun"] # input/
    [phi]  = glob_phi.data["val"]      # input/
    [dPhi] = glob_dPhi.data["val"]     # input/
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
    PhiAngle.data=dict(x=X,y=Y) #      /output
    if (X[2]>=0):
        PhiAngleText.data=dict(x=[X[2]],y=[Y[2]-0.1],t=[u"\u03C6"])  #      /output
    else:
        PhiAngleText.data=dict(x=[X[2]],y=[Y[2]-0.1],t=[u"-\u03C6"]) #      /output
    if (plot==plotSingle):
        X=Mass.data['x'][0]
        Y=Mass.data['y'][0]
    else:
        X=PendulumElbow.data['x'][0]
        Y=PendulumElbow.data['y'][0]
    Xe=X+dPhi*cos(phi)
    Ye=Y+dPhi*sin(phi)
    dPhiArrow.data=dict(xs=[X],xe=[Xe],ys=[Y],ye=[Ye])              #      /output
    if (Xe>X):
        dPhiArrowText.data=dict(x=[Xe],y=[Ye],t=[u"\u03C6\u0307"])  #      /output
        dPhiText.glyph.text_align="left"
    else:
        dPhiArrowText.data=dict(x=[Xe],y=[Ye],t=[u"-\u03C6\u0307"]) #      /output
        dPhiText.glyph.text_align="right"

def removePhiAngle():
    PhiAngle.data=dict(x=[],y=[])                #      /output
    PhiAngleText.data=dict(x=[],y=[],t=[])       #      /output
    dPhiArrow.data=dict(xs=[],xe=[],ys=[],ye=[]) #      /output
    dPhiArrowText.data=dict(x=[],y=[],t=[])      #      /output  

# return total energy
def getTotEng():
    [getCurrentXY] = glob_fun_getCurrentXY.data["fun"] # input/
    [getKinEng]    = glob_fun_getKinEng.data["fun"]    # input/
    [m]            = glob_m.data["val"]                # input/
    (X,Y)=getCurrentXY()
    potEng=g*m*(Y-6.0)
    kinEng=getKinEng()
    return potEng+kinEng

# return kinetic energy for simple pendulum
def getKinEngSingle():
    [dPhi] = glob_dPhi.data["val"] # input/
    [m]    = glob_m.data["val"]    # input/
    [R]    = glob_R.data["val"]    # input/
    return 0.5*m*R*R*dPhi*dPhi

# return kinetic energy for double pendulum
def getKinEngDouble():
    [dPhi]   = glob_dPhi.data["val"]   # input/
    [m]      = glob_m.data["val"]      # input/
    [R]      = glob_R.data["val"]      # input/
    [theta]  = glob_theta.data["val"]  # input/
    [dTheta] = glob_dTheta.data["val"] # input/
    return 0.5*m*((R*dPhi*sin(theta))**2+(R*dPhi*cos(theta)+R2*(dTheta+dPhi))**2)

# return double derivative of phi for a single pendulum
def ddPhi(phi,dPhi):
    [m]      = glob_m.data["val"]     # input/
    [R]      = glob_R.data["val"]     # input/
    [lam]    = glob_lam.data["val"]   # input/
    return -(g*sin(phi)+lam*dPhi/m)/R

# return double derivative of phi for a double pendulum
def ddPhiDouble(phi,dPhi,theta,dTheta):
    [m]      = glob_m.data["val"]     # input/
    [R]      = glob_R.data["val"]     # input/
    [lam]    = glob_lam.data["val"]   # input/
    if (theta==0):
        return 0
    else:
        return float(((g*cos(phi+theta)+R2*(dTheta+dPhi)**2)/R+dPhi*(dPhi*cos(theta)-lam*sin(theta)/m))/(sin(theta)+csc(theta)))

# return double derivative of theta for a double pendulum
def ddThetaDouble(phi,dPhi,ddPhi1,theta,dTheta):
    [m]      = glob_m.data["val"]     # input/
    [R]      = glob_R.data["val"]     # input/
    [lam]    = glob_lam.data["val"]   # input/
    return -(ddPhi1+R*(dPhi*dPhi*sin(theta)+(ddPhi1+lam*dPhi/m)*cos(theta))/R2+
        lam*(dTheta+dPhi)/m+g*sin(phi+theta)/R2)

# get new angles after timestep for a single pendulum
def getNextPointSingle(dt):
    [phi]  = glob_phi.data["val"]  # input/output
    [dPhi] = glob_dPhi.data["val"] # input/output
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
    glob_phi.data  = dict(val=[phi])
    glob_dPhi.data = dict(val=[dPhi])
    return getKinEngSingle()

# get new angles after timestep for a double pendulum
def getNextPointDouble(dt):
    [phi]    = glob_phi.data["val"]    # input/output
    [dPhi]   = glob_dPhi.data["val"]   # input/output
    [theta]  = glob_theta.data["val"]  # input/output
    [dTheta] = glob_dTheta.data["val"] # input/output
    # calculate current double derivative of angles
    ddPhi1   = ddPhiDouble(phi,dPhi,theta,dTheta)
    ddTheta1 = ddThetaDouble(phi,dPhi,ddPhi1,theta,dTheta)
    # calculate new angle using Taylor expansion
    phi     += dPhi*dt+0.5*dt*dt*ddPhi1
    theta   += dTheta*dt+0.5*dt*dt*ddTheta1
    # approximate new first derivative of angle
    dPhi2    = dPhi   + dt*ddPhi1
    dTheta2  = dTheta + dt*ddTheta1
    # use approximation of first derivative of angle to find new double derivative of angles
    ddPhi2   = ddPhiDouble(phi,dPhi2,theta,dTheta2)
    ddTheta2 = ddThetaDouble(phi,dPhi2,ddPhi2,theta,dTheta2)
    # update first derivative of angle using Heun
    dPhi    += 0.5*dt*(ddPhi1   + ddPhi2)
    dTheta  += 0.5*dt*(ddTheta1 + ddTheta2)
    # theta and phi should be in [-pi,pi], if this is not the case, put them back
    if (theta>pi):
        theta-=2*pi
    if (theta<-pi):
        theta+=2*pi
    if (phi>pi):
        phi-=2*pi
    if (phi<-pi):
        phi+=2*pi
    glob_phi.data    = dict(val=[phi])
    glob_dPhi.data   = dict(val=[dPhi])
    glob_theta.data  = dict(val=[theta])
    glob_dTheta.data = dict(val=[dTheta])
    return getKinEngDouble()

# plot the single pendulum
def plotSingle():
    [phi]            = glob_phi.data["val"]                            # input/
    [dPhi]           = glob_dPhi.data["val"]                           # input/
    [R]              = glob_R.data["val"]                              # input/
    [TotEng]         = glob_TotEng.data["val"]                         # input/
    PendulumArm.data = dict(x=[0, R*sin(phi)], y=[10,10.0-R*cos(phi)]) #      /output
    Mass.data        = dict(x=[R*sin(phi)],y=[10.0-R*cos(phi)])        #      /output
    [m]              = glob_m.data["val"]                              # input/
    [theta]          = glob_theta.data["val"]                          # input/output
    [dTheta]         = glob_dTheta.data["val"]                         # input/output
    currentPoint.data=dict(x=[phi],y=[dPhi])                             #      /output
    [Active]         = glob_active.data["Active"]
    if Active:
        basicPhaseDiagram.stream(dict(x=[phi],y=[dPhi]))                   #      /output
    if TotEng == 0:
        K=-4.5
    else:
        K=getKinEngSingle()*9.0/TotEng-4.5
    KinEnergySource.data=dict(x=[-4.5,-4.5, K, K], y=[12,11.5,11.5,12])  #      /output
    OtherEnergySource.data=dict(x=[K, K, 4.5, 4.5], y=[12,11.5,11.5,12]) #      /output

# plot the double pendulum
def plotDouble():
    [phi]    = glob_phi.data["val"]    # input/
    [dPhi]   = glob_dPhi.data["val"]   # input/
    [theta]  = glob_theta.data["val"]  # input/
    [R]      = glob_R.data["val"]      # input/
    [TotEng] = glob_TotEng.data["val"] # input/
    PendulumArm.data=dict(x=[0, R*sin(phi), R*sin(phi)+R2*sin(theta+phi)],
        y=[10,10.0-R*cos(phi),10.0-R*cos(phi)-R2*cos(theta+phi)]) #      /output
    PendulumElbow.data=dict(x=[R*sin(phi)],y=[10.0-R*cos(phi)])   #      /output
    Mass.data=dict(x=[R*sin(phi)+R2*sin(theta+phi)],y=[10.0-R*cos(phi)-R2*cos(theta+phi)]) #      /output
    currentPoint.data      = dict(x=[phi],y=[dPhi])                         #      /output
    [Active]         = glob_active.data["Active"]
    if Active:
        basicPhaseDiagram.stream(dict(x=[phi],y=[dPhi])) #      /output
    if TotEng == 0:
        K=-4.5
    else:
        K=getKinEngDouble()*9.0/TotEng-4.5
    KinEnergySource.data   = dict(x=[-4.5,-4.5, K, K], y=[12,11.5,11.5,12]) #      /output
    OtherEnergySource.data = dict(x=[K, K, 4.5, 4.5], y=[12,11.5,11.5,12])  #      /output

# get position of mass in single pendulum
def getCurrentXYSingle():
    [phi]    = glob_phi.data["val"]    # input/
    [theta]  = glob_theta.data["val"]  # input/
    [R]      = glob_R.data["val"]      # input/
    X=R*sin(phi)
    Y=10-R*cos(phi)
    return (X,Y)

# get position of mass in double pendulum
def getCurrentXYDouble():
    [phi]    = glob_phi.data["val"]    # input/
    [theta]  = glob_theta.data["val"]  # input/
    [R]      = glob_R.data["val"]      # input/
    X=R*sin(phi)+R2*sin(phi+theta)
    Y=10-R*cos(phi)-R2*cos(phi+theta)
    return (X,Y)

# function which carries out timestep
def evolve():
    #global plot
    [plot]         = glob_fun_plot.data["fun"]         # input/
    [getNextPoint] = glob_fun_getNextPoint.data["fun"] # input/
    [dt]           = glob_dt.data["val"]               # input/
    K=getNextPoint(dt)
    if (K>TotEng):
        #print K, "  >  ", TotEng
        pass
    plot()
    if (getTotEng()<1e-4):
        glob_active.data = dict(Active=[False])      #      /output
        [g1Pendulum]     = glob_callback.data["cid"] # input/
        curdoc().remove_periodic_callback(g1Pendulum)

# function to move the mass by clicking it
def on_mouse_move(event):
    [Active] = glob_active.data["Active"]  # input/
    [plot]   = glob_fun_plot.data["fun"]   # input/
    [moveTo] = glob_fun_moveTo.data["fun"] # input/
    if (not Active):
        moveTo(event.x,event.y)
        TotEng=getTotEng()
        glob_TotEng.data = dict(val=[TotEng]) #      /output
        plot()
        drawPhiAngle()

# function which moves mass to new angle for single pendulum
def moveToSingle(X,Y):
    [plot]        = glob_fun_plot.data["fun"] # input/
    glob_phi.data = dict(val=[atan2(X,10-Y)]) #      /output
    plot()

# function which moves mass to new position for double pendulum
def moveToDouble(X,Y):
    [plot]           = glob_fun_plot.data["fun"]       # input/
    [phi]            = glob_phi.data["val"]            # input/output
    [theta]          = glob_theta.data["val"]          # input/output
    [R]              = glob_R.data["val"]              # input/
    [bentDirection]  = glob_bentDirection.data["val"]  # input/output
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
    glob_phi.data           = dict(val=[phi])
    glob_theta.data         = dict(val=[theta])
    glob_bentDirection.data = dict(val=[bentDirection])
    # draw new position
    plot()

# store function handles (this avoids using excessive if/else statements)
glob_fun_plot.data         = dict(fun=[plotSingle])
glob_fun_getNextPoint.data = dict(fun=[getNextPointSingle])
glob_fun_getCurrentXY.data = dict(fun=[getCurrentXYSingle])
glob_fun_moveTo.data       = dict(fun=[moveToSingle])
glob_fun_getKinEng.data    = dict(fun=[getKinEngSingle])

# draw pendulum diagram
fig = figure(title="Kinetic energy balance",tools="",x_range=(-4.5,4.5),y_range=(3,12),width=500,height=500)
fig.on_event(Pan, on_mouse_move)
fig.title.text_font_size="16pt"
fig.axis.visible = False
fig.grid.visible = False
fig.toolbar.logo = None
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
phase_diagramm = figure(title="Phase diagram",tools="yzoom_in,yzoom_out,reset",x_range=(-3.14,3.14),y_range=(-5,5))
phase_diagramm.title.text_font_size="16pt"
phase_diagramm.axis.major_label_text_font_size="12pt"
phase_diagramm.axis.axis_label_text_font_style="normal"
phase_diagramm.axis.axis_label_text_font_size="12pt"
phase_diagramm.xaxis.axis_label=u"\u03C6 [rad]"
phase_diagramm.yaxis.axis_label=u"\u03C6\u0307 [rad/s]"
phase_diagramm.circle(x='x',y='y',size=2,color="#0065BD",source=basicPhaseDiagram)
phase_diagramm.circle(x='x',y='y',size=10,color="#E37222",source=currentPoint)
phase_diagramm.toolbar.logo = None
                       
TotEng=getTotEng()
glob_TotEng.data = dict(val=[TotEng])
[plot] = glob_fun_plot.data["fun"]
plot()

# add control buttons
def play():
    [Active] = glob_active.data["Active"] # input/output
    if (not Active):
        removePhiAngle()
        g1Pendulum         = curdoc().add_periodic_callback(evolve,100)
        glob_active.data   = dict(Active=[True])
        glob_callback.data = dict(cid=[g1Pendulum]) #      /output
        phi0_input.disabled = True
        dphi0_input.disabled = True
Play_button = Button(label="Play",button_type="success",width=150)
Play_button.on_click(play)

def stop():
    [Active] = glob_active.data["Active"] # input/output
    [phi]    = glob_phi.data["val"]       # input/
    [dPhi]   = glob_dPhi.data["val"]      # input/
    if (Active):
        [g1Pendulum] = glob_callback.data["cid"] # input/
        curdoc().remove_periodic_callback(g1Pendulum)
        glob_active.data  = dict(Active=[False])
        phi0_input.value  = phi
        dphi0_input.value = dPhi
        glob_dTheta.data  = dict(val=[0]) #      /output
        phi0_input.disabled = False
        dphi0_input.disabled = False
Stop_button = Button(label="Stop",button_type="success",width=150)
Stop_button.on_click(stop)

def reset():
    [Active] = glob_active.data["Active"] # input/output
    [plot] = glob_fun_plot.data["fun"]
    phi=0.5
    dPhi=1
    if (Active):
        [g1Pendulum] = glob_callback.data["cid"] # input/
        curdoc().remove_periodic_callback(g1Pendulum)
        glob_active.data   = dict(Active=[False])
        phi0_input.disabled = False
        dphi0_input.disabled = False
    mass_input.value       = 5.0
    lam_input.value        = 0.0
    phi0_input.value       = phi
    dphi0_input.value      = dPhi
    glob_phi.data          = dict(val=[phi])  #      /output
    glob_dPhi.data         = dict(val=[dPhi]) #      /output
    glob_dTheta.data       = dict(val=[0])    #      /output
    basicPhaseDiagram.data = dict(x=[],y=[])  #      /output
    plot()
Reset_button = Button(label="Reset",button_type="success",width=150)
Reset_button.on_click(reset)

def change_mass(attr,old,new):
    [plot]      = glob_fun_plot.data["fun"] # input/
    glob_m.data = dict(val=[new])           #      /output  
    TotEng=getTotEng()
    glob_TotEng.data = dict(val=[TotEng])   #      /output
    plot()
## Create slider to choose mass of blob
mass_input = LatexSlider(title="\\mathrm{Mass =}", value_unit="[\\mathrm{kg}]", value=5, start=0.5, end=10.0, step=0.1,width=200)
mass_input.on_change('value',change_mass)

def change_lam(attr,old,new):
    glob_lam.data = dict(val=[new]) #      /output
## Create slider to choose damper coefficient
lam_input = LatexSlider(title="\\mathrm{Damper\\ coefficient =}", value_unit="[\\mathrm{Ns}/\\mathrm{m}]", value=0.0, start=0.0, end=5.0, step=0.2,width=400)
lam_input.on_change('value',change_lam)

def change_phi0(attr,old,new):
    [plot]   = glob_fun_plot.data["fun"]      # input/
    [Active] = glob_active.data["Active"]     # input/
    [Phi0]   = glob_Phi0.data["val"]          # input/output
    if (not Active):
        glob_phi.data    = dict(val=[new])    #      /output
        TotEng=getTotEng()
        glob_TotEng.data = dict(val=[TotEng]) #      /output
        plot()
        Phi0=new
        glob_Phi0.data   = dict(val=[new])
        drawPhiAngle()
    elif (Phi0!=new):
        phi0_input.value=Phi0
## Create slider to choose damper coefficient
phi0_input = LatexSlider(title="\\varphi_0 =", value_unit="[\\mathrm{rad}]", value=0.5, start=-3.0, end=3.0, step=0.2,width=200)
phi0_input.on_change('value',change_phi0)

def change_phi0dot(attr,old,new):
    [plot]    = glob_fun_plot.data["fun"]     # input/
    [Active]  = glob_active.data["Active"]    # input/
    [dPhi0]   = glob_dPhi0.data["val"]        # input/output
    if (not Active):
        stop()
        glob_dPhi.data   = dict(val=[new])    #      /output
        TotEng           = getTotEng()
        glob_TotEng.data = dict(val=[TotEng]) #      /output
        plot()
        #dPhi=new
        drawPhiAngle()
    elif (dPhi0!=new):
        dphi0_input.value=dPhi0
## Create slider to choose damper coefficient
dphi0_input = LatexSlider(title="\\dot{\\varphi_0} =", value_unit="[\\mathrm{rad}/\\mathrm{s}]", value=1.0, start=-5.0, end=5.0, step=0.5,width=200)
dphi0_input.on_change('value',change_phi0dot)

# create selector for pendulum type which updates function handles and appropriate properties
def swapPendulumType(attr,old,new):
    [Active] = glob_active.data["Active"] # input/
    if (new==0):
        # if single pendulum
        plot=plotSingle
        getNextPoint=getNextPointSingle
        getCurrentXY=getCurrentXYSingle
        moveTo=moveToSingle
        getKinEng=getKinEngSingle
        glob_R.data  = dict(val=[4.0]) #      /output
        glob_dt.data = dict(val=[0.1]) #      /output
        PendulumElbow.data=dict(x=[],y=[])
    elif(new==1):
        # if double pendulum
        plot=plotDouble
        getNextPoint=getNextPointDouble
        getCurrentXY=getCurrentXYDouble
        moveTo=moveToDouble
        getKinEng=getKinEngDouble
        glob_R.data  = dict(val=[2.0])  #      /output
        glob_dt.data = dict(val=[0.05]) #      /output

    glob_fun_plot.data         = dict(fun=[plot])         #      /output
    glob_fun_getNextPoint.data = dict(fun=[getNextPoint]) #      /output
    glob_fun_getCurrentXY.data = dict(fun=[getCurrentXY]) #      /output
    glob_fun_moveTo.data       = dict(fun=[moveTo])       #      /output
    glob_fun_getKinEng.data    = dict(fun=[getKinEng])    #      /output
    
    glob_theta.data  = dict(val=[0])      #      /output
    glob_dTheta.data = dict(val=[0])      #      /output
    TotEng           = getTotEng()
    glob_TotEng.data = dict(val=[TotEng]) #      /output
    plot()
    if (not Active):
        drawPhiAngle()

pendulum_type_input = RadioButtonGroup(
        labels=["Single pendulum", "Double pendulum"], active=0)
pendulum_type_input.on_change('active',swapPendulumType)

# add app description
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1000)

## Send to window
hspace = 20
curdoc().add_root(column(description, row(column(fig,row(Play_button,Spacer(width=hspace),Stop_button,Spacer(width=hspace),Reset_button),pendulum_type_input),phase_diagramm), \
    row(mass_input,Spacer(width=hspace),lam_input,Spacer(width=hspace),phi0_input,Spacer(width=hspace),dphi0_input)))
#g1Pendulum=curdoc().add_periodic_callback(evolve,100)  # for immediate play
#glob_callback.data = dict(cid=[g1Pendulum])            # for immediate play
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '