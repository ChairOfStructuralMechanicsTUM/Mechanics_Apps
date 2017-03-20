from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from MathFuncs import *
from MoveNodeTool import *
from math import sqrt, floor

RollerNodeSource = []
RollerPointXPos = []
RollerPointYPos = []
RollerCoasterPathSource = ColumnDataSource(data=dict(x=[],y=[]))

currentNode=-1
TotPoints=9
Deriv2X=[]
Deriv2Y=[]

def PathInit (fig):
    global RollerPointXPos,RollerPointYPos,RollerNodeSource, TotPoints, Deriv2X, Deriv2Y
    #Ramp
    #X = [1,2.5,4,5.5,7,8.5,10,11.5,13]
    #Y = [13,11.5,10,8.5,7,5.5,4,2.5,1]
    X = [1, 3.5, 6.64, 8.7, 6.8, 5.54, 10.0, 11.67, 13.9]
    Y = [13, 3.3, 1.4, 3.8, 5.4, 3.16, 1.4, 4.8, 6.4]
    # Create and save path nodes
    for i in range(0,len(X)):
        RollerNodeSource.append(ColumnDataSource(data=dict(x=[X[i]],y=[Y[i]])))
        RollerPointXPos.append(X[i])
        RollerPointYPos.append(Y[i])
        fig.ellipse(x='x',y='y',width=1,height=1,source=RollerNodeSource[i], 
            fill_color="#CCCCC6",line_color=None)
    # calculate and save path
    (X,Deriv2X)=cubicSpline(RollerPointXPos)
    (Y,Deriv2Y)=cubicSpline(RollerPointYPos)
    RollerCoasterPathSource.data=dict(x=X,y=Y)
    TotPoints=len(X)

def find2Deriv (x,f):
    # solve A x = b  with :
    # b=temp
    temp=[0,(f[2]-f[1])/(x[2]-x[1])-(f[1]-f[0])/(x[1]-x[0])]
    # x=f''
    # A_{ii}=(h_i+h_{i+1})/3
    uDiag=[(x[2]-x[0])/3.0]
    # A_{i,i+1}=A_{i+1,i}=h_{i+1}/6
    # solve using LU decomposition in O(n)
    for i in range(1,len(x)-2):
        # temp [i+2] would equal :
        b=(f[i+2]-f[i+1])/(x[i+2]-x[i+1])-(f[i+1]-f[i])/(x[i+1]-x[i])
        # we solve L y = b in the first loop
        # lNow = upper diag of L (only vals of L to determine)
        lNow=(x[i+1]-x[i])/(6.0*uDiag[i-1])
        # create/solve for y
        temp.append(b-lNow*temp[i])
        # create A_{i,i}=U_{i,i}
        uDiag.append((x[i+2]-x[i])/3.0-lNow*(x[i+1]-x[i])/6.0)
    n=len(uDiag)
    # solve U x = y
    temp[n]/=uDiag[n-1]
    for i in range(n-1,0,-1):
        temp[i]=(temp[i]-(x[i+1]-x[i])*temp[i+1]/6.0)/uDiag[i-1]
    temp.append(0)
    return temp

def cubicSpline(f):
    x=range(0,len(f))
    # find 2nd deriv of f (solution to cubic spline problem)
    f2=find2Deriv(x,f)
    Y=[]
    for i in range(0,len(x)-1):
        xnow=i
        # create path from 20 points (1 at node 19 between nodes)
        Y.append(f[i])
        for j in range(1,20):
            xnow+=1.0/20.0
            Y.append((f2[i]*(i+1-xnow)**3 + f2[i+1]*(xnow-i)**3)/6.0
                + (f[i+1]-f[i] + (f2[i]-f2[i+1])/6.0)*(xnow-i)+f[i]-f2[i]/6.0)
    # add final node to path
    Y.append(f[len(x)-1])
    return (Y,f2)

# return Y(t)
def getHeight(xnow):
    i=int(floor(xnow))
    return ((Deriv2Y[i]*(i+1-xnow)**3 + Deriv2Y[i+1]*(xnow-i)**3)/6.0
        + ((RollerPointYPos[i+1]-RollerPointYPos[i])
        + (Deriv2Y[i]-Deriv2Y[i+1])/6.0)*(xnow-i)+RollerPointYPos[i]-Deriv2Y[i]/6.0)

# return point (X(t),Y(t))
def getPoint(xnow):
    i=int(floor(xnow))
    return ((Deriv2X[i]*(i+1-xnow)**3 + Deriv2X[i+1]*(xnow-i)**3)/6.0
        + ((RollerPointXPos[i+1]-RollerPointXPos[i])
        + (Deriv2X[i]-Deriv2X[i+1])/6.0)*(xnow-i)+RollerPointXPos[i]-Deriv2X[i]/6.0,
        (Deriv2Y[i]*(i+1-xnow)**3 + Deriv2Y[i+1]*(xnow-i)**3)/6.0
        + ((RollerPointYPos[i+1]-RollerPointYPos[i])
        + (Deriv2Y[i]-Deriv2Y[i+1])/6.0)*(xnow-i)+RollerPointYPos[i]-Deriv2Y[i]/6.0)

## function to simplify :    getDistance(xnow,xnext)
# return dx/dt
def dX(t):
    i=int(floor(t))
    return ((Deriv2X[i+1]*(t-i)**2-Deriv2X[i]*(i+1-t)**2)/2.0
        +RollerPointXPos[i+1]-RollerPointXPos[i]+(Deriv2X[i]-Deriv2X[i+1])/6.0)
# return dy/dt
def dY(t):
    i=int(floor(t))
    return ((Deriv2Y[i+1]*(t-i)**2-Deriv2Y[i]*(i+1-t)**2)/2.0
        +RollerPointYPos[i+1]-RollerPointYPos[i]+(Deriv2Y[i]-Deriv2Y[i+1])/6.0)

# get distance between (X(t_1),Y(t_1)) and (X(t_2),Y(t_2)) (t_1=xnow, t_2=xnext)
def getDistance(xnow,xnext):
    # L= \int_xnow^xnext \sqrt{(dx/dt)^2+(dy/dt)^2} sign(dx/dt) dt
    # we use simpson's rule (O(h^4))
    # \int_x1^x2 f(x) dx = h/6 (f(x1)+4f((x1+x2)/2)+f(x2)
    return (sqrt(dX(xnow)**2+dY(xnow)**2)*sign(dX(xnow))
        + 4*sqrt(dX((xnow+xnext)/2.0)**2+dY((xnow+xnext)/2.0)**2)*sign(dX((xnow+xnext)/2.0))
        + sqrt(dX(xnext)**2+dY(xnext)**2)*sign(dX(xnext)))*abs(xnext-xnow)/6.0

# Find normal vector
def normal (i):
   (dx,dy)=deriv (i);
   return (-dy,dx)

# Find derivative of path
def deriv (t):
    # find nearest nodes
    i1=int(floor(t*20))
    i2=int(floor(t*20))+1
    # use finite differences to compute derivative
    global RollerCoasterPathSource
    dx=RollerCoasterPathSource.data ['x'][i2]- RollerCoasterPathSource.data ['x'][i1]
    if (dx==0):
        return (0,1)
    dy=( RollerCoasterPathSource.data ['y'][i2]- RollerCoasterPathSource.data ['y'][i1])/dx
    # derivative = (1,dy), to "see" path travelling backwards (i.e. loops)
    # we invert derivative if dx=-1
    dx=sign(dx)
    dy*=dx
    # normalise derivative
    norme=sqrt(dx**2+dy**2)
    dx=dx/norme
    dy=dy/norme
    return (dx,dy)

# find index of node in which coordinates are found
# (return -1 if not in a node)
def inNode (xPos,yPos):
    global RollerPointXPos,RollerPointYPos
    for i in range(0,len(RollerPointXPos)):
        if (abs(xPos-RollerPointXPos[i])<=1 and abs(yPos-RollerPointYPos[i])<=1):
            return i
    return -1

# modify path by dragging nodes
def modify_path(attr, old, new):
    global currentNode, RollerNodeSource, RollerPointXPos,RollerPointYPos, Deriv2X, Deriv2Y, RollerCoasterPathSource
    # if there is a previous node (not first time the function is called)
    # and the node has not been released (new['x']=-1 on release to prepare for future calls)
    if (len(old)==1 and new[0][u'x']!=-1):
        # if first call for this node
        if (currentNode==-1):
            # determine which node and remember it
            XStart=old[0][u'x']
            YStart=old[0][u'y']
            currentNode=inNode(XStart,YStart)
        # if not first call then move node
        if (currentNode!=-1):
            # update node position
            RollerNodeSource[currentNode].data=dict(x=[new[0][u'x']],y=[new[0][u'y']])
            RollerPointXPos[currentNode]=new[0][u'x']
            RollerPointYPos[currentNode]=new[0][u'y']
            # update path
            (X,Deriv2X) = cubicSpline(RollerPointXPos)
            (Y, Deriv2Y) = cubicSpline(RollerPointYPos)
            RollerCoasterPathSource.data=dict(x=X,y=Y)
        return 1
    else:
        # when node is released reset current node to -1
        # so a new node is moved next time
        currentNode=-1
        return -1

# changes between Ramp/Bumps/Loop nodes
# nodes are provided in arguments
def drawPath (X,Y):
    # save nodes in easily accessible list
    global RollerPointXPos, RollerPointYPos, RollerNodeSource, Deriv2X, Deriv2Y, RollerCoasterPathSource
    RollerPointXPos=X
    RollerPointYPos=Y
    # update nodes
    for i in range(0,len(X)):
        RollerNodeSource[i].data=dict(x=[X[i]],y=[Y[i]])
    # calculate new path
    (X,Deriv2X) = cubicSpline(RollerPointXPos)
    (Y, Deriv2Y) = cubicSpline(RollerPointYPos)
    # update path
    RollerCoasterPathSource.data=dict(x=X,y=Y)
