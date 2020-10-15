import numpy as np
from numpy.linalg import inv
from bokeh.models import ColumnDataSource

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
        
        trusslist = list()
        for i in range(len(trusses)):
            trusslist.append( ColumnDataSource(data=trusses[i]) )
        self.trusses      = trusslist
        
        self.trussLength  = trussLength
        self.base         = ColumnDataSource(base)
        
        # System matrices
        self.M = np.zeros((3,3))
        self.C = np.zeros((3,3))
        self.K = np.zeros((3,3))
        
        # Mass locations
        self.massLocations = np.zeros((3,2))
        
        # Force indicator (forces indicate in the plotting domain the force 
        # carried by each of the truss members besides the location where to
        # display the force values) ((Here default value are given))
        self.forces = ColumnDataSource(
                                       data=dict(
                                                 x=[0,0,0],
                                                 y=[0,0,0],
                                                 force=['Force = ','Force = ','Force = ']
                                                )
                                      )
                                      
        self.massIndicators = ColumnDataSource(
                                               data=dict(
                                                         x=[0,0,0],
                                                         y=[0,0,0],
                                                         mass=['','','']
                                                        )
                                              )
                                               
        self.stiffnessIndicators = ColumnDataSource(
                                                    data=dict(
                                                              x=[0,0,0],
                                                              y=[0,0,0],
                                                              stiffness=['','','']
                                                             )
                                                   )
                                                    
        self.maximumDisplacement = ColumnDataSource(data=dict(storey=["First","Seconds","Third"],maxDisp=[0.0,0.0,0.0]))
        
    def update_system(self, displacement):
        self.update_masses(displacement)
        self.update_mass_indicator_locaiton()
        self.update_massSupprts(displacement)
        self.update_stiffness_indicator_locaiton()
        self.update_truss_sources()
        
    def update_masses(self, displacement):
        self.masses[0].data = dict(x=[displacement[0]] , y=self.masses[0].data['y'])
        self.masses[1].data = dict(x=[displacement[1]] , y=self.masses[1].data['y'])
        self.masses[2].data = dict(x=[displacement[2]] , y=self.masses[2].data['y'])

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
        y1 = 0.0
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

    def update_force_indicator_location(self):
        # first force indicator
        x1 = (self.trusses[1].data['x'][0] + self.trusses[1].data['x'][1]) / 2 + 2.5 # where 2.5 is an offset value
        y1 = (self.trusses[1].data['y'][1] + self.trusses[1].data['y'][0]) / 2
        
        # second force indicator
        x2 = (self.trusses[3].data['x'][0] + self.trusses[3].data['x'][1]) / 2 + 2.5
        y2 = (self.trusses[3].data['y'][1] + self.trusses[3].data['y'][0]) / 2
              
        # third force indicator
        x3 = (self.trusses[5].data['x'][0] + self.trusses[5].data['x'][1]) / 2 + 2.5
        y3 = (self.trusses[5].data['y'][1] + self.trusses[5].data['y'][0]) / 2
              
        # update the source fle
        self.forces.data = dict(x=[x1,x2,x3],y=[y1,y2,y3],force=self.forces.data['force'])
             
        
    def update_mass_indicator_locaiton(self):
        updateLocation = list()
        for i in self.masses:
            updateLocation.append( i.data['y'][0] + 0.5 )
        self.massIndicators.data = dict(
                                        x=[self.masses[0].data['x'][0], self.masses[1].data['x'][0], self.masses[2].data['x'][0]],
                                        y=updateLocation,
                                        mass=self.massIndicators.data['mass']
                                       )
        
        # Update the value of the maximum displacement of the structure in the table
        self.update_maximum_displacement()
        
    def update_stiffness_indicator_locaiton(self):
        updateLocationX = list()
        updateLocationY = list()
        counter = 0
        for i in self.massSupports:
            updateLocationY.append( (i.data['y'][0] + self.trussLength*counter) / 2 )
            updateLocationX.append( (i.data['x'][1] + 1.0) )
            counter += 1
        self.stiffnessIndicators.data = dict(
                                             x=updateLocationX,
                                             y=updateLocationY,
                                             stiffness=self.stiffnessIndicators.data['stiffness']
                                            )
        
    def update_maximum_displacement(self):
        self.maximumDisplacement.data = dict(
                                             storey=["First","Seconds","Third"],
                                             maxDisp=[
                                                      round(self.masses[0].data['x'][0],3),
                                                      round(self.masses[1].data['x'][0],3),
                                                      round(self.masses[2].data['x'][0],3)
                                                     ]
                                            )
        
def cubic_N1 (xi):
    return 0.25 * (1-xi)*(1-xi) * (2+xi)
def cubic_N2 (xi):
    return 0.25 * (1+xi)*(1+xi) * (2-xi)
    
def cubicInterpolate(y1, y2, x1, x2, noNodes,length):
    nodes = np.ones(noNodes)
    i = 0.0
    while i<noNodes:
        x = i*2.0/(float(noNodes)-1.0) - 1.0
        nodes[int(i)] = cubic_N1(x)*y1 + cubic_N2(x)*y2
        i += 1.0

    return nodes
    
def linear_N1 (y,a,b):
    return( (y-b)/(a-b) )
    
def linear_N2 (y,a,b):
    return( (y-a)/(b-a) )
    
def linIntepolate(y1, y2, x1, x2, noNodes, length):
    nodes = np.ones(noNodes)
    i = 0.0
    while i<noNodes:
        x = i/(noNodes-1) * length + x1
        nodes[int(i)] = linear_N1(x,x1,x2)*y1 + linear_N2(x,x1,x2)*y2
        i += 1

    return nodes

def solve_time_domain(structure, seismicInput):
    dt = seismicInput.data['time'][1] - seismicInput.data['time'][0]
    N  = len(seismicInput.data['amplitude'])
    
    M = structure.M
    C = structure.C
    K = structure.K
    #I = np.array([[1,0,0],[0,1,0],[0,0,1]])
    
    F = np.zeros((3,N))
    F[0,:] = seismicInput.data['amplitude']
    x0 = np.array([0.0,0.0,0.0])
    v0 = np.array([0.0,0.0,0.0])
    
    ###########################################################################
    ######### Generalized-alpha (high order time integration method) ##########
    ###### Credit to inplementation of Mate Pentek from Statik Lehrstuhl ######
    ###########################################################################
    y = np.zeros((3,len( F[0,:] ))) # 3 refers to the number of dofs (3 storeys)
    
    y[:,0] = x0
    a0 = np.dot(inv(M),( np.dot(-M,F[:,0]) - np.dot(C,v0) - np.dot(K,x0) ))
    
    u0 = np.array([0.0,0.0,0.0])
    v0 = np.array([0.0,0.0,0.0])
    a0 = np.array([0.0,0.0,0.0])
    f0 = F[:,0]
    u1 = u0
    v1 = v0
    a1 = a0
    f1 = f0
    
    pInf = 0.15
    alphaM = (2.0 * pInf - 1.0) / (pInf + 1.0)
    alphaF = pInf / (pInf + 1.0)
    beta = 0.25 * (1 - alphaM + alphaF)**2
    gamma = 0.5 - alphaM + alphaF
    
        # coefficients for LHS
    a1h = (1.0 - alphaM) / (beta * dt**2)
    a2h = (1.0 - alphaF) * gamma / (beta * dt)
    a3h = 1.0 - alphaF

    # coefficients for mass
    a1m = a1h
    a2m = a1h * dt
    a3m = (1.0 - alphaM - 2.0 * beta) / (2.0 * beta)
    
    #coefficients for damping
    a1b = (1.0 - alphaF) * gamma / (beta * dt)
    a2b = (1.0 - alphaF) * gamma / beta - 1.0
    a3b = (1.0 - alphaF) * (0.5 * gamma / beta - 1.0) * dt
    
    # coefficient for stiffness
    a1k = -1.0 * alphaF
    
    # coefficients for velocity update
    a1v = gamma / (beta * dt)
    a2v = 1.0 - gamma / beta
    a3v = (1.0 - gamma / (2 * beta)) * dt
    
    # coefficients for acceleration update
    a1a = a1v / (dt * gamma)
    a2a = -1.0 / (beta * dt)
    a3a = 1.0 - 1.0 / (2.0 * beta) 
    #y0 = x0 - dt*v0 + (dt*dt/2)*a0
    #y[:,1] = y0
    
    #A = M + dt*gamma2*C + dt*dt*beta2*K
    #invA = inv(A)
    for i in range(1,len(F[0,:])):
        #A = (M/(dt*dt) + C/(2*dt))
        
        #tempVec = y[:,i-1] + 0.5*(-np.dot(M,F[:,i-1])-np.dot(C,y_dot[:,i-1])-np.dot(K,y[:,i-1]))*dt
        #y[:,i] = y[:,i-1] + tempVec*dt
        #y_dot[:,i] = np.dot(inv(I+C) , tempVec + 0.5*(-np.dot(M,F[:,i])-np.dot(K,y[:,i])))

        #B = np.dot( 2*M/(dt*dt) - K, y[:,i-1]) + np.dot((C/(2*dt) - M/(dt*dt)) , y[:,i-2] + np.dot(-M,F[:,i-1]))

        #print('np.dot(-M,F[:,i]) = ',np.dot(-M,F[:,i]))
        Ff = (1.0 - alphaF) * np.dot(-M,F[:,i]) + alphaF * f0
        #print('F = ',F)
		
        LHS = a1h * M + a2h * C + a3h * K 
        RHS = np.dot(M,(a1m * u0 + a2m * v0 + a3m * a0))
        RHS += np.dot(C,(a1b * u0 + a2b * v0 + a3b * a0)) 
        RHS += np.dot(a1k * K, u0) + Ff

        # update self.f1
        f1 = np.dot(-M,F[:,i])
        
        # updates self.u1,v1,a1
        u1 = np.linalg.solve(LHS, RHS)
        y[:,i] = u1
        v1 = a1v * (u1 - u0) + a2v * v0 + a3v * a0
        a1 = a1a * (u1 - u0) + a2a * v0 + a3a * a0

        u0 = u1
        v0 = v1
        a0 = a1
        
        # update the force   
        f0 = f1
    
    '''
    ###########################################################################
    ################## Low-order time integration method ######################
    ###########################################################################
    y = np.zeros((3,len( F[0,:] )))
    y[:,0] = x0
    a0 = np.dot(inv(M),( F[:,0] - np.dot(C,v0) - np.dot(K,x0) ))
    
    y0 = x0 - dt*v0 + (dt*dt/2)*a0

    y[:,1] = y0
    

    for i in range(2,len(F[0,:])):
        A = M/(dt**2) + C/dt + K
        B = -np.dot(M,F[:,i]) + np.dot(M/(dt**2) , 2*y[:,i-1]-y[:,i-2]) + np.dot(C/dt,y[:,i-1])
        yNew = np.dot(inv(A) , B)
        y[:,i] = yNew 
    '''
    return y
    
def construct_truss_sources(massOne, massTwo, massThree, length):
    
    # The convention used here is that the first entry of both the x and y vectors
    # represent the lower node and the second represents the upper node

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
     
def construct_system(structure, mass, massRatio, bendingStiffness, stiffnessRatio, trussLength):
    structure.massIndicators.data = dict(
                                         x=structure.massIndicators.data['x'],
                                         y=structure.massIndicators.data['y'],
                                         mass=[str(massRatio[0])+'m',str(massRatio[1])+'m',str(massRatio[2])+'m']
                                        )
    
    structure.stiffnessIndicators.data = dict(
                                     x=structure.stiffnessIndicators.data['x'],
                                     y=structure.stiffnessIndicators.data['y'],
                                     stiffness=[str(stiffnessRatio[0])+'EI',str(stiffnessRatio[1])+'EI',str(stiffnessRatio[2])+'EI']
                                    )
    
    structure.M = np.array([[massRatio[0],      0      ,     0       ],
                            [      0      ,massRatio[1],     0       ],
                            [      0      ,      0      ,massRatio[2]]]) * mass
                           
    structure.K = np.array([
                            [stiffnessRatio[0]+stiffnessRatio[1],         -stiffnessRatio[1]        ,         0         ],
                            [        -stiffnessRatio[1]         ,stiffnessRatio[1]+stiffnessRatio[2], -stiffnessRatio[2]],
                            [                0                  ,         -stiffnessRatio[2]        ,  stiffnessRatio[2]]
                          ]) * 12 * bendingStiffness / trussLength**3
                            
                            
    '''
    Rayleigh damping coefficients were chosen based on the following formula:
    alpha = 2*w1*w2/(w2**2-w1**2) * (w2*xsi1 - w1*xsi2)
    beta  = 2/(w2**2-w1**2) * (w2*xsi2 - w1*xsi1)
    **the equation brought from paper "EVALUATION OF ADDED MASS MODELING
    APPROACHES FOR THE DESIGN OF MEMBRANE STRUCTURES BY FULLY COUPLED FSI 
    SIMULATIONS"
    
    w1 --- angular frequency of the first mode
    w2 --- angular frequency of the second mode
    xsi1 --- damping ratio of first mode
    xsi2 --- damping ratio of second mode
    
    for the given structure, w1 and w2 equal 12.498 rad/sec and 26.722 rad/sec
    respectively. And since we need the damping ratio of the structure to be 
    5 %, hence xsi1 and xsi2 are assigned with 0.05. As a result, alpha and 
    beta equal to 0.8515 and 0.0026 respectively.
    '''
    structure.C = 0.8515*structure.M + 0.0026*structure.K
                            
def plot( plot_name, subject, radius, color ):
    plot_name.line( x='x', y='y', source=subject.massSupports[0], color=color, line_width=5)
    plot_name.line( x='x', y='y', source=subject.massSupports[1], color=color, line_width=5)
    plot_name.line( x='x', y='y', source=subject.massSupports[2], color=color, line_width=5)
    
    plot_name.circle( x='x',y='y',radius=radius,color=color,source=subject.masses[0] )
    plot_name.circle( x='x',y='y',radius=radius,color=color,source=subject.masses[1] )
    plot_name.circle( x='x',y='y',radius=radius,color=color,source=subject.masses[2] )
    
    plot_name.line( x='x', y='y', color=color, source=subject.trusses[0], line_width=2)
    plot_name.line( x='x', y='y', color=color, source=subject.trusses[1], line_width=2)
    plot_name.line( x='x', y='y', color=color, source=subject.trusses[2], line_width=2)
    plot_name.line( x='x', y='y', color=color, source=subject.trusses[3], line_width=2)
    plot_name.line( x='x', y='y', color=color, source=subject.trusses[4], line_width=2)
    plot_name.line( x='x', y='y', color=color, source=subject.trusses[5], line_width=2)
    
    plot_name.line( x='x', y='y', source=subject.base, color='#000000', line_width=5 )
    
def read_seismic_input(file, scale):
    amplitude   = list()
    time           = list()
    
    wordCounter = 0
    lineCounter = 0
    npts = 0
    
    with open( file,'r' ) as f:
        for line in f:
            #counter = 0
            for word in line.split():
                if lineCounter == 3 and wordCounter == 2:
                    npts = int(word)
                    
                if lineCounter == 3 and wordCounter == 6:
                    dt = float(word)
                
                if lineCounter >= 4:
                    amplitude.append(float(word)*9.81*scale)

                wordCounter += 1
            wordCounter = 0
            lineCounter += 1

    # Create time list
    for i in range(0,npts):
        time.append(i*dt)
        
    return ColumnDataSource(data=dict(amplitude=np.array(amplitude),time=np.array(time)))

def read_ERS_data(file):
    acceleration = list()
    period = list()
    wordCounter = 0
    lineCounter = 0
    
    with open( file,'r' ) as f:
        for line in f:
            for word in line.split(','):
                if lineCounter > 45 and lineCounter < 157: #input data situated between line 45 and 157 in the data file
                    if wordCounter == 0:
                        #print(word)
                        period.append(float(word))
                    elif wordCounter == 5:
                        acceleration.append(float(word)*9.81) # multiplication by 9.81 to convert it to m/sec/sec
                    wordCounter += 1
                #wordCounter += 1
            wordCounter = 0
            lineCounter += 1
    
    return ColumnDataSource(data=dict(period=period,acceleration=acceleration))

def read_KOKE_ERS_data(file):
    acceleration = list()
    period = list()
    wordCounter = 0
    lineCounter = 0
    
    with open( file,'r' ) as f:
        for line in f:
            for word in line.split(','):
                if lineCounter > 66 and lineCounter < 178: #input data situated between line 67 and 179 in the data file
                    if wordCounter == 0:
                        #print(word)
                        period.append(float(word))
                    elif wordCounter == 10:
                        acceleration.append(float(word)*9.81) # multiplication by 9.81 to convert it to m/sec/sec
                    wordCounter += 1
                #wordCounter += 1
            wordCounter = 0
            lineCounter += 1
    
    return ColumnDataSource(data=dict(period=period,acceleration=acceleration))
    
def Read_ERS_info(file):

    data = list()
    wordCounter = -1
    lineCounter = 0                    
    with open( file, 'r') as f:
        for line in f:
            if lineCounter == 34:
                for word in line.split(','):
                    if wordCounter >= 9 and wordCounter <= 15:
                        data.append(word)
                    wordCounter += 1
            lineCounter += 1

    return data

def Read_Kobe_ERS_info(file):

    data = list()
    wordCounter = -1
    lineCounter = 0                    
    with open( file, 'r') as f:
        for line in f:
            if lineCounter == 40:
                for word in line.split(','):
                    if wordCounter >= 9 and wordCounter <= 15:
                        data.append(word)
                    wordCounter += 1
            lineCounter += 1

    return data