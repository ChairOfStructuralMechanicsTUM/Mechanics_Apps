import numpy as np
from numpy.linalg import inv

def solve_time_domain(structure, seismicInput):
    
    M = structure.M
    C = structure.C
    K = structure.K
    
    F = seismicInput 
    
    x0 = np.array([0,0,0])
    v0 = np.array([0,0,0])
    
    dt = 0.1
    
    y = np.zeros((3,len( F[0,:] ))) # 3 refers to the number of dofs (3 storeys)
    y[:,0] = x0
    a0 = np.dot(inv(M),( np.dot(-M,F[:,0]) - np.dot(C,v0) - np.dot(K,x0) ))
    
    y0 = x0 - dt*v0 + (dt*dt/2)*a0

    y[:,1] = y0

    for i in range(2,len(F[0,:])):
        A = (M/(dt*dt) + C/(2*dt))

        B = np.dot(
                   2*M/(dt*dt) - K,
                   y[:,i-1]) + np.dot((C/(2*dt) - M/(dt*dt)),y[:,i-2] + F[:,i-1]
                  )

        yNew = np.dot(inv(A) , B)
        
        y[:,i] = yNew  

    return y