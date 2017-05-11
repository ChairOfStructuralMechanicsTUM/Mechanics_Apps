from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.models import ColumnDataSource, Slider, Arrow, OpenHead, Button, TextInput, Paragraph
from bokeh.io import curdoc
from math import sqrt, sin, cos, floor
from os.path import dirname, join, split

m=3
a_half=0.75
mu=10.0
h=2.5
t=0.0
dt=0.1
phi=0.0
x0=0.0
y0=6.0
lam=10.0
tFalling=sqrt((h-0.1)*2.0/9.81)
dPhi=m*sqrt(19.62*h)*a_half/(m*(h*h+a_half*a_half)+mu*a_half*2.0*(a_half*a_half/3.0+h*h))

swingingBase = ColumnDataSource(data=dict(x=[[x0,-a_half],[-a_half,a_half],[a_half,x0]],y=[[y0,y0-h],[y0-h,y0-h],[y0-h,y0]],w=[1,10,1]))
ball = ColumnDataSource(data = dict(x=[a_half-0.1],y=[y0]))
arrowSources = ColumnDataSource(data = dict(xs=[-a_half,-a_half-0.5],xe=[a_half,-a_half-0.5],ys=[y0-h-0.5,y0-h],ye=[y0-h-0.5,y0]))
arrowTextSources = ColumnDataSource(data = dict(x=[0,-a_half-1],y=[y0-h-1,y0-h/2.0],t=['a','h']))
VhArrow = ColumnDataSource(data = dict(xs=[],ys=[],xe=[],ye=[]))
VhText = ColumnDataSource(data = dict(x=[],y=[],t=[]))
dPhiArrow = ColumnDataSource(data = dict(xs=[],ys=[],xe=[],ye=[]))
dPhiText = ColumnDataSource(data = dict(x=[],y=[],t=[]))

Marked=False
Active=False

def releaseBall():
    global t
    Y=y0-0.5*9.81*t*t
    if (t>tFalling or t>tFalling-0.05):
        ball.data=dict(x=[a_half-0.1],y=[y0-h+0.1])
        curdoc().remove_periodic_callback(releaseBall)
        curdoc().add_periodic_callback(startSwinging,100)
        t=0.0
        VhArrow.data=dict(xs=[a_half-0.1],xe=[a_half-0.1],ys=[y0-h], ye=[y0-h-1])
        VhText.data=dict(x=[a_half-0.1],y=[y0-h-1],t=[u"v\u2095"])
        dPhiArrow.data=dict(xs=[0],xe=[-1],ys=[y0-0.5],ye=[y0-0.5])
        dPhiText.data=dict(x=[-1],y=[y0-0.5],t=[u"\u03C6\u0307 "])
    else:
        ball.data=dict(x=[a_half-0.1],y=[Y])
        t+=dt

# return double derivative of phi for a simple pendulum
def ddPhi(Phi,dPhi):
    global lam, m, h
    return -(9.81*sin(Phi)+lam*dPhi/m)/h

def startSwinging ():
    global phi, dPhi, dt, a_half, h, y0, swingingBase, ball
    # velocity verlet
    a=ddPhi(phi,dPhi)
    phi+=dPhi*dt+a*dt*dt*0.5
    dPhi+=0.5*dt*(a+ddPhi(phi,dPhi+dt*a))
    SIN=sin(phi)
    COS=cos(phi)
    AHalfY0h1=a_half*COS-h*SIN
    AHalfY0h2=-a_half*SIN-h*COS+y0
    MAHalfY0h1=-a_half*COS-h*SIN
    MAHalfY0h2=a_half*SIN-h*COS+y0
    swingingBase.data=dict(x=[[x0,MAHalfY0h1],[MAHalfY0h1,AHalfY0h1],[AHalfY0h1,x0]],
        y=[[y0,MAHalfY0h2],[MAHalfY0h2,AHalfY0h2],[AHalfY0h2,y0]],w=[1,10,1])
    ball.data=dict(x=[(a_half-0.1)*COS-(h-0.1)*SIN],y=[y0-(h-0.1)*COS-a_half*SIN])
    if (abs(a)<1e-2 and abs(dPhi)<1e-2):
        global Active, ArrowGlyphs
        curdoc().remove_periodic_callback(startSwinging)
        Active=False
        arrowSources.data = dict(xs=[-a_half,-a_half-0.5],xe=[a_half,-a_half-0.5],ys=[y0-h-0.5,y0-h],ye=[y0-h-0.5,y0])
        ArrowText.visible=True
        VhArrow.data=dict(xs=[],ys=[],xe=[],ye=[])
        VhText.data=dict(x=[],y=[],t=[])
        dPhiArrow.data=dict(xs=[],ys=[],xe=[],ye=[])
        dPhiText.data=dict(x=[],y=[],t=[])

p = figure(x_range=(-5,5),y_range=(0,7),tools="",width=750,height=525)
p.multi_line(xs='x',ys='y',line_width='w',color="#808080",source=swingingBase)
p.ellipse(x='x',y='y',width=0.2,height=0.2,source=ball,color="#0065BD")
arrowHead = OpenHead(line_color="black",line_width=2,size=10)
ArrowGlyphs = Arrow(start=arrowHead, end=arrowHead,source=arrowSources,
    x_start='xs', y_start='ys', x_end='xe', y_end='ye',line_color="black",line_width=2)
p.add_layout(ArrowGlyphs)
ArrowText=p.text(x='x', y='y',text='t',text_color='black',text_font_size="15pt",source=arrowTextSources)
VhArrowGlyph = Arrow(end=arrowHead,source=VhArrow, x_start='xs', y_start='ys',
    x_end='xe', y_end='ye',line_color="black",line_width=2)
p.add_layout(VhArrowGlyph)
p.text(x='x', y='y',text='t',text_color='black',text_font_size="15pt",
    source=VhText,text_align="center",text_baseline="top")
dPhiArrowGlyph = Arrow(end=arrowHead,source=dPhiArrow, x_start='xs', y_start='ys',
    x_end='xe', y_end='ye',line_color="black",line_width=2)
p.add_layout(dPhiArrowGlyph)
p.text(x='x', y='y',text='t',text_color='black',text_font_size="15pt",
    source=dPhiText,text_align="right",text_baseline="middle")
p.grid.visible=False
p.axis.visible=False

def changeA(attr,old,new):
    global Active, a_half, swingingBase, h, ball, y0, x0, arrowSources, arrowTextSources
    if (not Active):
        a_half=new/2.0
        swingingBase.data=dict(x=[[x0,-a_half],[-a_half,a_half],[a_half,x0]],y=[[y0,y0-h],[y0-h,y0-h],[y0-h,y0]],w=[1,10,1])
        ball.data = dict(x=[a_half-0.1],y=[y0])
        arrowSources.data=dict(xs=[-a_half,-a_half-0.5],xe=[a_half,-a_half-0.5],ys=[y0-h-0.5,y0-h],ye=[y0-h-0.5,y0])
        arrowTextSources.data = dict(x=[0,-a_half-1],y=[y0-h-1,y0-h/2.0],t=['a','h'])
    elif (new/2.0!=a_half):
        a_input.value=a_half*2.0

def changeH(attr,old,new):
    global Active, h, swingingBase, a_half, y0, arrowSources, arrowTextSources
    if (not Active):
        h=new
        swingingBase.data=dict(x=[[x0,-a_half],[-a_half,a_half],[a_half,x0]],y=[[y0,y0-h],[y0-h,y0-h],[y0-h,y0]],w=[1,10,1])
        arrowSources.data=dict(xs=[-a_half,-a_half-0.5],xe=[a_half,-a_half-0.5],ys=[y0-h-0.5,y0-h],ye=[y0-h-0.5,y0])
        arrowTextSources.data = dict(x=[0,-a_half-1],y=[y0-h-1,y0-h/2.0],t=['a','h'])
    elif (new!=h):
        h_input.value=h

def changeBallMass(attr,old,new):
    global Active, m
    if (not Active):
        m=new
    elif (new!=m):
        mk_input.value=m

def changeBaseMass(attr,old,new):
    global Active, mu
    if (not Active):
        mu=new/2.0/a_half
    elif (new!=mu*a_half*2):
        ms_input.value=mu*a_half*2

## Create sliders
a_input = Slider(title="a [m]", value=2*a_half, start=0.5, end=8.0, step=1)
a_input.on_change('value',changeA)

h_input = Slider(title="h [m]", value=h, start=0.5, end=4.0, step=0.5)
h_input.on_change('value',changeH)

mk_input = Slider(title=u"m\u2096 [kg]", value=m, start=0.5, end=10.0, step=0.5)
mk_input.on_change('value',changeBallMass)

ms_input = Slider(title=u"m\u209B [kg]", value=mu*a_half*2, start=0.5, end=40.0, step=0.5)
ms_input.on_change('value',changeBaseMass)

def removeMark(attr,old,new):
    global Marked
    if (Marked):
        VhMark.text=""
        dPhiMark.text=""

userVh = TextInput(value="", title=u"v\u2095 = (1 d.p)",width=200)
userVh.on_change('value',removeMark)
VhMark = Paragraph(text="")
userDPhi = TextInput(value="", title=u"\u03C6\u0307 = (2 d.p)",width=200)
userDPhi.on_change('value',removeMark)
dPhiMark = Paragraph(text="")

def markUserInput():
    global Marked, dPhi, h
    Vh=sqrt(19.62*h)
    Vh10=floor(Vh*10)
    Vh100=floor(Vh*100)
    if (Vh100-Vh10*10>=5):
        Vh=(Vh10+1)/10.0
    else:
        Vh=Vh10/10.0
    try:
        if (abs(float(userVh.value)-Vh)<=0.05):
            VhMark.text=u"\u2714"
        else:
            VhMark.text=u"\u2717"
    except:
        VhMark.text=u"\u2717"
    dPhi100=floor(dPhi*100)
    dPhi1000=floor(dPhi*1000)
    if (dPhi1000-dPhi100*10>=5):
        dPhiR=(dPhi100+1)/100.0
    else:
        dPhiR=dPhi100/100.0
    try:
        if (abs(float(userDPhi.value)-dPhiR)<=0.05):
            dPhiMark.text=u"\u2714"
        else:
            dPhiMark.text=u"\u2717"
    except:
        dPhiMark.text=u"\u2717"
    Marked=True

def test ():
    global Active, t, tFalling,dPhi, a_half, m, h, mu, phi, ArrowGlyphs, ArrowText
    if (not Active):
        t=0.0
        tFalling=sqrt((h-0.1)*2.0/9.81)
        phi=0.0
        dPhi=m*sqrt(19.62*h)*a_half/(m*(h*h+a_half*a_half)+mu*a_half*2.0*(a_half*a_half/3.0+h*h))
        curdoc().add_periodic_callback(releaseBall,100)
        markUserInput()
        Active=True
        arrowSources.data=dict(xs=[],ys=[],xe=[],ye=[])
        ArrowText.visible=False

test_button = Button(label="Uberprüfen", button_type="success")
test_button.on_click(test)

def reset():
    global Active, t, ball, phi, arrowSources, a_half, y0, h, ArrowText, VhArrow, VhText, dPhiArrow, dPhiText
    a_input.value=1.5
    h_input.value=2.5
    mk_input.value=3
    ms_input.value=15
    ball.data = dict(x=[a_half-0.1],y=[y0])
    if (Active):
        Active=False
        t=0.0
        phi=0.0
        try:
            curdoc().remove_periodic_callback(releaseBall)
        except:
            curdoc().remove_periodic_callback(startSwinging)
        arrowSources.data = dict(xs=[-a_half,-a_half-0.5],xe=[a_half,-a_half-0.5],ys=[y0-h-0.5,y0-h],ye=[y0-h-0.5,y0])
        ArrowText.visible=True
        VhArrow.data=dict(xs=[],ys=[],xe=[],ye=[])
        VhText.data=dict(x=[],y=[],t=[])
        dPhiArrow.data=dict(xs=[],ys=[],xe=[],ye=[])
        dPhiText.data=dict(x=[],y=[],t=[])

reset_button = Button(label="Reset", button_type="success")
reset_button.on_click(reset)

## Send to window
curdoc().add_root(row(p,column(a_input,h_input,mk_input,ms_input,row(userVh,VhMark),row(userDPhi,dPhiMark),test_button,reset_button)))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
