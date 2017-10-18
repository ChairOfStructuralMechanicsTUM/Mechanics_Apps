from scipy.optimize import minimize
import numpy as np

g = lambda x, y: x ** 2 + y ** 2 - 3

x0, y0 = (5,1)

f = lambda x: (x[0]-x0)**2+(x[1]-y0)**2
df = lambda x: np.array([2*(x[0]-x0),2*(x[1]-y0)])

cons = ({'type': 'eq', 'fun': lambda x:  g(x[0],x[1])})

x, y = minimize(f,[x0,y0],constraints=cons,jac=df)['x']

print "(%f,%f)" % (x,y)
