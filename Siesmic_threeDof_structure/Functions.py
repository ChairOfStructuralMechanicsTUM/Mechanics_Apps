from bokeh.models import ColumnDataSource
import numpy as np
from numpy import linalg as LA
from scipy import linalg
from bokeh.models.ranges import Range1d

class Structure:
    
    def __init__(self, masses, massSupports, trusses, trussLength, base):
        
        masslist = list()
        for i in range(len(masses)):
            masslist.append( ColumnDataSource(data=masses[i]) )
        self.masses       = masslist
        
        massSupportlist = list()
        for i in range(len(massSupports)):
            massSupportlist.append( ColumnDataSource(data=massSupports[i]) )
        self.massSupports = massSupportlist

        self.trussLength  = trussLength
        
        trusslist = list()
        for i in range(len(trusses)):
            trusslist.append( ColumnDataSource(data=trusses[i]) )
        self.trusses      = trusslist
        
        self.base         = ColumnDataSource(base)
        
        # System matrices
        self.M = np.zeros((3,3))
        self.C = np.zeros((3,3))
        self.K = np.zeros((3,3))
        
    def update_system(self, displacement):
        self.update_masses(displacement)
        self.update_massSupprts(displacement)
        self.update_truss_sources()
        
    def update_masses(self, displacement):
        self.masses[0].data['x'] = self.masses[0].data['x']*0 + [displacement[0]]
        self.masses[1].data['x'] = self.masses[1].data['x']*0 + [displacement[1]]
        self.masses[2].data['x'] = self.masses[2].data['x']*0 + [displacement[2]]

    def update_massSupprts(self, displacement):
        self.massSupports[0].data['x'] = self.massSupports[0].data['x']*0 + [-self.trussLength/2+displacement[0], self.trussLength/2+displacement[0]]
        self.massSupports[1].data['x'] = self.massSupports[1].data['x']*0 + [-self.trussLength/2+displacement[1], self.trussLength/2+displacement[1]]
        self.massSupports[2].data['x'] = self.massSupports[2].data['x']*0 + [-self.trussLength/2+displacement[2], self.trussLength/2+displacement[2]]

    def update_truss_sources(self):
        noNodes = 10
        
        # truss1
        x1 = - self.trussLength/2
        x2 = self.masses[0].data['x'][0] - self.trussLength/2
        y1 = 0.0
        y2 = self.masses[0].data['y'][0]

        ys = linIntepolate(y1,y2,y1,y2,noNodes,self.trussLength)
        xs = cubicInterpolate(x1,x2,y1,y2,noNodes,self.trussLength)
        self.trusses[0].data = dict( x=xs, y=ys )

        # truss2
        x1 =   self.trussLength/2
        x2 = self.masses[0].data['x'][0] + self.trussLength/2
        y1 = self.masses[0].data['y'][0] - self.trussLength
        y2 = self.masses[0].data['y'][0] 

        xs = cubicInterpolate(x1,x2,y1,y2,noNodes,self.trussLength)
        ys = linIntepolate(y1,y2,y1,y2,noNodes,self.trussLength)
        self.trusses[1].data = dict( x=xs, y=ys )
        
        # truss3
        x1 = self.masses[0].data['x'][0] - self.trussLength/2
        x2 = self.masses[1].data['x'][0] - self.trussLength/2
        y1 = self.masses[0].data['y'][0] 
        y2 = self.masses[1].data['y'][0] 

        xs = cubicInterpolate(x1,x2,y1,y2,noNodes,self.trussLength)
        ys = linIntepolate(y1,y2,y1,y2,noNodes,self.trussLength)
        self.trusses[2].data =dict( x=xs, y=ys )

        # truss4
        x1 = self.masses[0].data['x'][0] + self.trussLength/2
        x2 = self.masses[1].data['x'][0] + self.trussLength/2
        y1 = self.masses[0].data['y'][0]
        y2 = self.masses[1].data['y'][0]  

        xs = cubicInterpolate(x1,x2,y1,y2,noNodes,self.trussLength)
        ys = linIntepolate(y1,y2,y1,y2,noNodes,self.trussLength)
        self.trusses[3].data =dict( x=xs, y=ys )
        
        # truss5 
        x1 = self.masses[1].data['x'][0] - self.trussLength/2
        x2 = self.masses[2].data['x'][0] - self.trussLength/2
        y1 = self.masses[1].data['y'][0]
        y2 = self.masses[2].data['y'][0]

        xs = cubicInterpolate(x1,x2,y1,y2,noNodes,self.trussLength)
        ys = linIntepolate(y1,y2,y1,y2,noNodes,self.trussLength)
        self.trusses[4].data =dict( x=xs, y=ys )
        
        # truss6
        x1 = self.masses[1].data['x'][0] + self.trussLength/2
        x2 = self.masses[2].data['x'][0] + self.trussLength/2
        y1 = self.masses[1].data['y'][0]
        y2 = self.masses[2].data['y'][0]

        xs = cubicInterpolate(x1,x2,y1,y2,noNodes,self.trussLength)
        ys = linIntepolate(y1,y2,y1,y2,noNodes,self.trussLength)
        self.trusses[5].data =dict( x=xs, y=ys ) 
        
        
class ModeShape( Structure ):
    
    def __init__(self, masses, massSupports, trusses, trussLength, base, frequency, modeShape):
        Structure.__init__(self, masses, massSupports, trusses, trussLength, base)
        self.frequency = frequency
        self.modeShape = modeShape
        
class SiesmicParameters():
    
    def __init__(self,a,gamma,S,eta,beta,undergroundParamter):
        self.a = a
        self.gamma = gamma
        self.S = 0 # default value, will be changed by determine_periods_and_S()
        self.eta = eta
        self.beta = beta
        self.undergroundParamter = undergroundParamter
        '''
        period[0] == TB
        period[1] == TC
        period[2] == TD
        '''
        self.periods = np.zeros(3) # default value, will be changed by determine_periods_and_S()
        self.determine_periods_and_S()
        
        self.ERSdata = ColumnDataSource(data=dict(x=[0],y=[0])) # Elastic Response Spectrum data
        
    def determine_periods_and_S(self):
        if self.undergroundParamter == 'A-R':
            self.periods[0] = 0.05
            self.periods[1] = 0.20
            self.periods[2] = 2.00
            self.S = 1.00
        elif self.undergroundParamter == 'B-R':
            self.periods[0] = 0.05
            self.periods[1] = 0.25
            self.periods[2] = 2.00
            self.S = 1.25
        elif self.undergroundParamter == 'C-R':
            self.periods[0] = 0.05
            self.periods[1] = 0.30
            self.periods[2] = 2.00
            self.S = 1.50
        elif self.undergroundParamter == 'B-T':
            self.periods[0] = 0.10
            self.periods[1] = 0.30
            self.periods[2] = 2.00
            self.S = 1.00
        elif self.undergroundParamter == 'C-T':
            self.periods[0] = 0.10
            self.periods[1] = 0.40
            self.periods[2] = 2.00
            self.S = 1.25
        elif self.undergroundParamter == 'C-S':
            self.periods[0] = 0.10
            self.periods[1] = 0.50
            self.periods[2] = 2.00
            self.S = 0.75
            
    def get_max_displacement (self, period):
        if period >= 0 and period < self.periods[0]:
            return self.a * self.gamma * self.S * (1+period/self.periods[0]*(self.beta/1-1))
        elif period >= self.periods[0] and period < self.periods[1]:
            print('period = ',period)
            return self.a * self.gamma * self.S * self.beta / 1 
        elif period > self.periods[1] and period < self.periods[2]:
            return self.a * self.gamma * self.S * self.beta / 1 * (self.periods[1]/period)
        elif (period > self.periods[2]):
            return self.a * self.gamma * self.S * self.beta / 1 * self.periods[1]**2/period**2
            
def cubic_N1 (xi):
    #xi = 2*x/length - 1
    return( 0.25 * ((1-xi)**2) * (2+xi) )
def cubic_N2 (xi):
    #xi = 2*x/length - 1
    return( 0.25 * ((1+xi)**2) * (2-xi) )
    
def cubicInterpolate(y1, y2, x1, x2, noNodes,length):
    nodes = np.ones(noNodes)
    for i in range(noNodes):
        x = (2/(noNodes-1))*i - 1
        nodes[i] =  cubic_N1(x)*y1 + cubic_N2(x)*y2

    return(nodes)
    
def linear_N1 (y,a,b):
    return( (y-b)/(a-b) )
    
def linear_N2 (y,a,b):
    return( (y-a)/(b-a) )
    
def linIntepolate(y1, y2, x1, x2, noNodes, length):
    nodes = np.ones(noNodes)
    for i in range(0, noNodes):
        x = i/(noNodes-1) * length + x1
        nodes[i] = linear_N1(x,x1,x2)*y1 + linear_N2(x,x1,x2)*y2

    return(nodes)
    
def construct_truss_sources(massOne, massTwo, massThree, length):
    trussOne   = dict(
                        x=[massOne['x'][0] - length/2, massOne['x'][0] - length/2],
                        y=[massOne['y'][0] - length  , massOne['y'][0]           ]
                     )

    trussTwo   = dict(
                        x=[massOne['x'][0] + length/2, massOne['x'][0] + length/2],
                        y=[massOne['y'][0] - length  , massOne['y'][0]           ]
                     )
    trussThree = dict(
                        x=[massTwo['x'][0] - length/2, massTwo['x'][0] - length/2],
                        y=[massOne['y'][0]           , massTwo['y'][0]           ]
                     )
    trussFour  = dict(
                        x=[massTwo['x'][0] + length/2, massTwo['x'][0] + length/2],
                        y=[massOne['y'][0]           , massTwo['y'][0]           ]
                     )
    trussFive  = dict(
                        x=[massThree['x'][0] - length/2, massThree['x'][0] - length/2],
                        y=[massTwo['y'][0]             , massThree['y'][0]           ]
                     )
    trussSix   = dict(
                        x=[massThree['x'][0] + length/2, massThree['x'][0] + length/2],
                        y=[massTwo['y'][0]             , massThree['y'][0]           ]
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
    
    massOne = dict(x=[0.0],y=[1*length])
    massTwo = dict(x=[0.0],y=[2*length])
    massThree = dict(x=[0.0],y=[3*length])
    
    masses.append(massOne)
    masses.append(massTwo)
    masses.append(massThree)
    
    massOneSupport = dict(
                            x=[massOne['x'][0] - length/2, massOne['x'][0] + length/2],
                            y=[massOne['y'][0]           , massOne['y'][0]           ]
                         )
    massTwoSupport = dict(
                            x=[massTwo['x'][0] - length/2, massTwo['x'][0] + length/2],
                            y=[massTwo['y'][0]           , massTwo['y'][0]           ]
                         )
    massThreeSupport = dict(
                            x=[massThree['x'][0] - length/2, massThree['x'][0] + length/2],
                            y=[massThree['y'][0]           , massThree['y'][0]           ]
                           )
                                      
    massSupports.append(massOneSupport)
    massSupports.append(massTwoSupport)
    massSupports.append(massThreeSupport)
    
    return masses, massSupports
     
def construct_system(structure, mass, massRation, bendingStiffness, stiffnessRatio, trussLength):
    structure.M = np.array([[massRation[0],      0      ,     0       ],
                            [      0      ,massRation[1],     0       ],
                            [      0      ,      0      ,massRation[2]]]) * mass
                           
    structure.K = np.array([
                            [stiffnessRatio[0]+stiffnessRatio[1],         -stiffnessRatio[1]        ,         0         ],
                            [        -stiffnessRatio[1]         ,stiffnessRatio[1]+stiffnessRatio[2], -stiffnessRatio[2]],
                            [                0                  ,         -stiffnessRatio[2]        ,  stiffnessRatio[2]]
                          ]) * 12 * bendingStiffness / trussLength**3
                            
    print('M = ',structure.M)
    print('K = ',structure.K)
                        
def solve_time_domain(structure, siesmicInput):
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
    
def solve_modal_analysis(structure):
    #eigenvalues, eigenvectors =  LA.eig(-structure.M + structure.K)
    eigenvalues, eigenvectors = linalg.eig(structure.K, structure.M)
    
    return eigenvalues, eigenvectors
#    # hard-coded values
#    eigenvalues = [1,2,3]
#    eigenvectors = [
#                    [0,0,0],
#                    [1,-1,1],
#                    [1,1,-1]
#                   ]
#    
#    modes = [1,2,3]
#    eigenvaluesDict = dict(x=modes , y=eigenvalues)
#    eigenmodesDict = list()
#    massXCoord = [0,0,0] # watch for these values if the coordinates change in main file
#    massYCoord = [1,2,3] # watch for these values if the coordinates change in main file
#    for eigenmode in eigenvectors:
#        for element in range(0 , len(massXCoord)):
#            massXCoord[element] += eigenmode[element]
#
#        eigenmodesDict.append( dict(x=massXCoord,y=massYCoord) ) 

def plot( plot_name, subject, radius, color ):
    plot_name.line( x='x', y='y', source=subject.massSupports[0], color='#000000', line_width=5)
    plot_name.line( x='x', y='y', source=subject.massSupports[1], color='#000000', line_width=5)
    plot_name.line( x='x', y='y', source=subject.massSupports[2], color='#000000', line_width=5)
    
    plot_name.circle( x='x',y='y',radius=radius,color=color,source=subject.masses[0] )
    plot_name.circle( x='x',y='y',radius=radius,color=color,source=subject.masses[1] )
    plot_name.circle( x='x',y='y',radius=radius,color=color,source=subject.masses[2] )
    
    plot_name.line( x='x', y='y', source=subject.trusses[0], line_width=2)
    plot_name.line( x='x', y='y', source=subject.trusses[1], line_width=2)
    plot_name.line( x='x', y='y', source=subject.trusses[2], line_width=2)
    plot_name.line( x='x', y='y', source=subject.trusses[3], line_width=2)
    plot_name.line( x='x', y='y', source=subject.trusses[4], line_width=2)
    plot_name.line( x='x', y='y', source=subject.trusses[5], line_width=2)
    
    plot_name.line( x='x', y='y', source=subject.base, color='#000000', line_width=20 )
    
def GetMaximumDisplacement( modes, siesmicParameters ):
    
    maximumDisplacement = list()
    r = np.array([1,1,1])
    
    beta = list()
    period = list()
    Sa = list()
    for i in range(0,3):
        beta.append( np.dot( modes[i].M , r ) )
        period.append( 2*np.pi / modes[i].frequency )
        
        maximumDisplacement.append( siesmicParameters.get_max_displacement(period[i]) )
        
def plot_ERS( plot, siesmicParameters ):
    n = 100
    tMin = 0.0
    tMax = siesmicParameters.periods[2] + 1
    x = np.zeros(n)
    y = np.zeros(n)

    # Determine the corresponsing Se value
    for i in range(0,n):
        T = (tMax - tMin)/n * i + tMin
        x[i] = T
        y[i] = siesmicParameters.get_max_displacement(T)

    siesmicParameters.ERSdata.data = dict(x=x, y=y)
    plot.line(x='x',y='y',source=siesmicParameters.ERSdata)
    maxVal = max(abs(i) for i in y)
    plot.y_range = Range1d(0, 1.1*maxVal)
    plot.x_range = Range1d(0, x[-1])
		