from bokeh.models import ColumnDataSource
import numpy as np
from numpy import linalg as LA

class Structure:
    
    def __init__(self, masses, massSupports, trusses, trussLength, base):
        self.masses       = masses
        self.massSupports = massSupports
        self.trussLength  = trussLength
        self.trusses      = trusses
        self.base         = base
        
    def update_masses(self, displacement):
        self.masses[0].data['x'] = self.masses[0].data['x']*0 + [displacement[0]]
        self.masses[1].data['x'] = self.masses[1].data['x']*0 + [displacement[1]]
        self.masses[2].data['x'] = self.masses[2].data['x']*0 + [displacement[2]]

    def update_massSupprts(self, displacement):
        self.massSupports[0].data['x'] = self.massSupports[0].data['x']*0 + [-0.5+displacement[0], 0.5+displacement[0]]
        self.massSupports[1].data['x'] = self.massSupports[1].data['x']*0 + [-0.5+displacement[1], 0.5+displacement[1]]
        self.massSupports[2].data['x'] = self.massSupports[2].data['x']*0 + [-0.5+displacement[2], 0.5+displacement[2]]

    def update_truss_sources(self):
        noElements = 10
        
        # truss1
        x1 = self.masses[0].data['x'][0] - self.trussLength/2
        x2 = self.masses[0].data['x'][0] - self.trussLength/2
        ys = np.ones(noElements) * (self.masses[0].data['y'][0] - self.trussLength)
        xs = interpolate(x1,x2,noElements,self.trussLength)
        self.trusses[0].data = dict(
                                    x=[xs],
                                    y=[ys]
                                   )
        self.trusses[1].data = dict(
                                    x=[self.masses[0].data['x'][0] + self.trussLength/2, self.masses[0].data['x'][0] + self.trussLength/2],
                                    y=[self.masses[0].data['y'][0] - self.trussLength  ,           self.masses[0].data['y'][0]           ]
                                   )
        
        # truss3
        x1 = self.masses[0].data['x'][0] - self.trussLength/2
        x2 = self.masses[1].data['x'][0] - self.trussLength/2
        xs = interpolate(x1,x2,noElements,self.trussLength)
        
        y1 = self.masses[0].data['y'][0] 
        y2 = self.masses[1].data['y'][0] 
        ys = interpolate(y1,y2,noElements,self.trussLength)
        print('ys = ',ys)
        print('xs = ',xs)
        self.trusses[2].data =dict(
                                    x=[xs],
                                    y=[ys]
                                   )
        self.trusses[3].data =dict(
                                    x=[self.masses[0].data['x'][0] + self.trussLength/2, self.masses[1].data['x'][0] + self.trussLength/2],
                                    y=[self.masses[0].data['y'][0]                     ,           self.masses[1].data['y'][0]           ]
                                   )
        self.trusses[4].data =dict(
                                    x=[self.masses[1].data['x'][0] - self.trussLength/2, self.masses[2].data['x'][0] - self.trussLength/2],
                                    y=[self.masses[1].data['y'][0]                     ,           self.masses[2].data['y'][0]           ]
                                   )
        self.trusses[5].data =dict(
                                    x=[self.masses[1].data['x'][0] + self.trussLength/2, self.masses[2].data['x'][0] + self.trussLength/2],
                                    y=[self.masses[1].data['y'][0]                     ,           self.masses[2].data['y'][0]           ]
                                   ) 
        
def N1 (x,length):
    xi = 2*x/length - 1
    return( 0.25 * (1-xi)**2 * (2+xi) )
def N2 (x,length):
    xi = 2*x/length - 1
    return( 0.25 * (1+xi)**2 * (2-xi) )
    
def interpolate(x1,x2,noElements,length):
    nodes = np.ones(noElements)
    for i in range(noElements):
        x = i/noElements * length + x2
        nodes[i] =  N1(x,length)*x1 + N2(x,length)*x2 

    return(nodes)
    
def construct_truss_sources(massOne, massTwo, massThree, length):
    trussOne   = ColumnDataSource(
                                  data=dict(
                                            x=[massOne.data['x'][0] - length/2, massOne.data['x'][0] - length/2],
                                            y=[massOne.data['y'][0] - length  , massOne.data['y'][0]           ]
                                           )
                                 )
    trussTwo   = ColumnDataSource(
                                  data=dict(
                                            x=[massOne.data['x'][0] + length/2, massOne.data['x'][0] + length/2],
                                            y=[massOne.data['y'][0] - length  , massOne.data['y'][0]           ]
                                           )
                                 )
    trussThree = ColumnDataSource(
                                  data=dict(
                                            x=[massTwo.data['x'][0] - length/2, massTwo.data['x'][0] - length/2],
                                            y=[massOne.data['y'][0]           , massTwo.data['y'][0]           ]
                                           )
                                 )
    trussFour  = ColumnDataSource(
                                  data=dict(
                                            x=[massTwo.data['x'][0] + length/2, massTwo.data['x'][0] + length/2],
                                            y=[massOne.data['y'][0]           , massTwo.data['y'][0]           ]
                                           )
                                 )
    trussFive  = ColumnDataSource(
                                  data=dict(
                                            x=[massThree.data['x'][0] - length/2, massThree.data['x'][0] - length/2],
                                            y=[massTwo.data['y'][0]             , massThree.data['y'][0]           ]
                                           )
                                 )
    trussSix   = ColumnDataSource(
                                  data=dict(
                                            x=[massThree.data['x'][0] + length/2, massThree.data['x'][0] + length/2],
                                            y=[massTwo.data['y'][0]             , massThree.data['y'][0]           ]
                                           )
                                 )
                              
    trussSources = list()
    trussSources.append(trussOne)
    trussSources.append(trussTwo)
    trussSources.append(trussThree)
    trussSources.append(trussFour)
    trussSources.append(trussFive)
    trussSources.append(trussSix)
    
    return trussSources    
     
def construct_masses_and_supports(length):
    
    masses = list()
    massSupports = list()
    
    massOne = ColumnDataSource(data=dict(x=[0.0],y=[1.0]))
    massTwo = ColumnDataSource(data=dict(x=[0.0],y=[2.0]))
    massThree = ColumnDataSource(data=dict(x=[0.0],y=[3.0]))
    
    masses.append(massOne)
    masses.append(massTwo)
    masses.append(massThree)
    
    massOneSupport = ColumnDataSource(
                                      data=dict(
                                                x=[massOne.data['x'][0] - length/2, massOne.data['x'][0] + length/2],
                                                y=[massOne.data['y'][0]           , massOne.data['y'][0]           ]
                                               )
                                     )
    massTwoSupport = ColumnDataSource(
                                      data=dict(
                                                x=[massTwo.data['x'][0] - length/2, massTwo.data['x'][0] + length/2],
                                                y=[massTwo.data['y'][0]           , massTwo.data['y'][0]           ]
                                               )
                                     )
    massThreeSupport = ColumnDataSource(
                                      data=dict(
                                                x=[massThree.data['x'][0] - length/2, massThree.data['x'][0] + length/2],
                                                y=[massThree.data['y'][0]           , massThree.data['y'][0]           ]
                                               )
                                     )
                                      
    massSupports.append(massOneSupport)
    massSupports.append(massTwoSupport)
    massSupports.append(massThreeSupport)
    
    return masses, massSupports
     
def construct_system(M, K, C, mass, bendingStiffness, trussLength):
    pass

def solve_time_domain(M, C, K, siesmicInput):
    '''
    y = np.zeros((2,len( F[0,:] )))
    y[:,0] = x0
    a0 = np.dot(inv(M),( F[:,0] - np.dot(C,v0) - np.dot(K,x0) ))
    
    y0 = x0 - dt*v0 + (dt*dt/2)*a0

    y[:,1] = y0
    
    #A = M/(dt*dt) + C/(2*dt)

    #B = np.dot((2*M/(dt*dt) - K),y[:,0]) + np.dot((C/(2*dt) - M/(dt*dt)),y[:,0])

    #yNew = np.dot(inv(A),B)

    #y[:,1] = yNew

    for i in range(2,len(F[0,:])):
        A = (M/(dt*dt) + C/(2*dt))
        #A = dt*dt*F[:,i-1] - np.dot((dt*dt*K - 2*M),y[:,i-1]) - np.dot((M - dt*C/2),y[:,i-2])
        B = np.dot((2*M/(dt*dt) - K),y[:,i-1]) + np.dot((C/(2*dt) - M/(dt*dt)),y[:,i-2] + F[:,i-1])
        #B = M + 0.5*dt*C
        yNew = np.dot(inv(A) , B)
        y[:,i] = yNew  
    '''
    N = 3000
    t = np.zeros(N)
    for i in range(N):
        t[i] = i*0.01

    amplitude = np.zeros((3,N))
    for mass in range(3):
        for time in range(N):
            amplitude[mass,time] = np.sin(np.pi*mass*time*0.01)
            
    return amplitude

def read_siesmic_input(file):
    amplitude   = list()
    time           = list()
    
    counter = 0
    with open( file,'r' ) as f:
        for line in f:
            counter = 0
            for word in line.split():
                if (counter % 2 == 0):
                    time.append(float(word))
                else:
                    amplitude.append(float(word))
                counter += 1

    # create colors
    color = list()
    for i in amplitude:
        color.append('#33FF33')
        
    return dict(amplitude=amplitude,time=time,color=color)
    
def solve_modal_analysis(M, K):
    #eigenvalues, eigenvectors =  LA.eig(M-K)
    # hard-coded values
    eigenvalues = [1,2,3]
    eigenvectors = [
                    [0,0,0],
                    [1,-1,1],
                    [1,1,-1]
                   ]
    
    modes = [1,2,3]
    eigenvaluesDict = dict(x=modes , y=eigenvalues)
    eigenmodesDict = list()
    massXCoord = [0,0,0] # watch for these values if the coordinates change in main file
    massYCoord = [1,2,3] # watch for these values if the coordinates change in main file
    for eigenmode in eigenvectors:
        for element in range(0 , len(massXCoord)):
            massXCoord[element] += eigenmode[element]

        eigenmodesDict.append( dict(x=massXCoord,y=massYCoord) ) 
    
    return eigenvaluesDict, eigenmodesDict[0], eigenmodesDict[1], eigenmodesDict[2]

def update_mass(attr,old,new):
    pass
    
def update_bendingStiffness(attr,old,new):
    pass

def play():
    pass

def pause():    
    pass