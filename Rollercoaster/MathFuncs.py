def find2Deriv (x,f):
    temp=[0,(f[2]-f[1])/(x[2]-x[1])-(f[1]-f[0])/(x[1]-x[0])]
    uDiag=[(x[2]-x[0])/3.0]
    for i in range(1,len(x)-2):
        b=(f[i+2]-f[i+1])/(x[i+2]-x[i+1])-(f[i+1]-f[i])/(x[i+1]-x[i])
        lNow=(x[i+1]-x[i])/(6.0*uDiag[i-1])
        temp.append(b-lNow*temp[i])
        uDiag.append((x[i+2]-x[i])/3.0-lNow*(x[i+1]-x[i])/6.0)
    n=len(uDiag)
    temp[n]/=uDiag[n-1]
    for i in range(n-1,0,-1):
        temp[i]=(temp[i]-(x[i+1]-x[i])*temp[i+1]/6.0)/uDiag[i-1]
    temp.append(0)
    return temp

def cubicSpline(x,f):
    f2=find2Deriv(x,f)
    Y=[]
    for i in range(0,len(x)-1):
        h=x[i+1]-x[i];
        xnow=x[i]
        Y.append(f[i])
        # test and optimise number
        for j in range(1,20):
            xnow+=h/20.0
            Y.append((f2[i]*(x[i+1]-xnow)**3 + f2[i+1]*(xnow-x[i])**3)/(h*6.0)
                + ((f[i+1]-f[i])/h + (f2[i]-f2[i+1])*h/6.0)*(xnow-x[i])+f[i]-f2[i]*h**2/6.0)
    Y.append(f[len(x)-1])
    return Y

def sign (x):
    if (x>0):
        return 1
    elif (x<0):
        return -1
    else:
        return 0
