from bokeh.models import ColumnDataSource
import numpy as np
from numpy import linalg as LA
from scipy import linalg
from bokeh.models.ranges import Range1d
from bokeh.models.widgets import Div

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
        
    def update_system(self, displacement):
        self.update_masses(displacement)
        self.update_mass_indicator_locaiton()
        self.update_massSupprts(displacement)
        self.update_stiffness_indicator_locaiton()
        self.update_truss_sources()
        #print('truss1 = ',self.trusses[1].data['x'])
        
    def update_masses(self, displacement):
        self.masses[0].data = dict(x=[displacement[0]] , y=self.masses[0].data['y'])
        self.masses[1].data = dict(x=[displacement[1]] , y=self.masses[1].data['y'])
        self.masses[2].data = dict(x=[displacement[2]] , y=self.masses[2].data['y'])

        self.update_mass_indicator_locaiton

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
              
#    def update_force_indicator_value(self, forces):
#        
#        self.forces.data = dict(
#                                x = self.forces.data['x'],
#                                y = self.forces.data['y'],
#                                force = ['Force = '+str(forces[0])+' N','Force = '+str(forces[1])+' N','Force = '+str(forces[2])+' N']
#                               )
        
    def update_mass_indicator_locaiton(self):
        updateLocation = list()
        for i in self.masses:
            updateLocation.append( i.data['y'][0] + 0.5 )
        self.massIndicators.data = dict(
                                        x=[self.masses[0].data['x'][0], self.masses[1].data['x'][0], self.masses[2].data['x'][0]],
                                        y=updateLocation,
                                        mass=self.massIndicators.data['mass']
                                       )
        
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
        
class Mode( Structure ):
    
    def __init__(self, ID, masses, massSupports, trusses, trussLength, base, frequency, modeShape):
        Structure.__init__(self, masses, massSupports, trusses, trussLength, base)
        self.id = ID
        self.frequency = frequency
        self.modeShape = modeShape
        self.maxModeShape = np.array([0,0,0]) # 0 is a default value
        self.locationInERS = ColumnDataSource(data=dict(x=[0],y=[0])) # with default values
        self.participationFactor = 0 # 0 is a default value
        
        self.multiplier_text = Div(text="""<b>\u03b2S\u2090/\u03C9\u00B2 =</b> """+ str(0))
        self.frequency_text  = Div(text="""<b>Natural Frequency =</b> """)
    
    def get_maximum_displacement( self, siesmicParameters ):
        r = np.ones(3)
        self.participationFactor = np.dot( self.modeShape, np.dot( self.M, r ) )
        period = 2*np.pi / self.frequency
        Sa = siesmicParameters.get_Sa( period )
        
        multiplier = self.participationFactor*Sa*(1/self.frequency**2)
        
        self.modify_mode_text( multiplier )
        
        self.maxModeShape = multiplier*self.modeShape
        return self.maxModeShape

    def modify_location_in_ERS( self, siesmicParameters ):
        period = 2*np.pi / self.frequency
        Sa = siesmicParameters.get_Sa( period )
        self.locationInERS.data = dict(x=[period,period,0],y=[0,Sa,Sa])
        
    def modify_mode_text(self, multiplier):  
        if self.id == 2:
            self.multiplier_text.text = " "u"<b>\u03b2S"u"\u2090(T)/"u"\u03C9"u"\u00B2 = </b>"+ str(multiplier)
        elif self.id == 1:
            self.multiplier_text.text = " "u"<b>\u03b2S"u"\u2090(T)/"u"\u03C9"u"\u00B2 = </b>"+ str(multiplier)
        elif self.id == 0:
            self.multiplier_text.text = " "u"<b>\u03b2S"u"\u2090(T)/"u"\u03C9"u"\u00B2 = </b>"+ str(multiplier)
        #self.multiplier_text.text = """<b>Multiplier =</b> """ 
        
    def modify_frequency_text(self):
        self.frequency_text.text = """<b>Natural Frequency =</b> """ + str(self.frequency) + " rad/sec"
        
    def normalize_mode_shape(self):
        m = np.dot(self.modeShape , np.dot(self.M , self.modeShape))
        if m != 1:
            self.modeShape = self.modeShape / np.sqrt(m)
            
    def normalized_mode_withMax_one(self):
        maxAmplitude = 0.0
        for component in self.modeShape:
            if abs(component) > maxAmplitude:
                maxAmplitude = abs(component)
            
        return self.modeShape / maxAmplitude
        
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
        
        self.informationTable = ColumnDataSource(
                                                 data=dict(
                                                           subject=['Period (second)','Participation Factor (\u03b2)','Modal Mass',
                                                                    'Spectral Acceleration (m/s\u2082)','Total Force (N)',
                                                                    'First Storey Max. Displacement (m)','Second Storey Max. Displacement',
                                                                    'Third Storey Max. Displacement','First Storey Total Force',
                                                                    'Second Storey Total Force','Third Storey Total Force'],
                                                            modeOne  =[0,0,0,0,0,0,0,0,0,0,0],
                                                            modeTwo  =[0,0,0,0,0,0,0,0,0,0,0],
                                                            modeThree=[0,0,0,0,0,0,0,0,0,0,0]
                                                          )
                                                )
        
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
            
    def get_Sa (self, period):
        if period >= 0 and period < self.periods[0]:
            return self.a * self.gamma * self.S * (1+period/self.periods[0]*(self.beta/1-1))
        elif period >= self.periods[0] and period < self.periods[1]:
            return self.a * self.gamma * self.S * self.beta / 1 
        elif period >= self.periods[1] and period < self.periods[2]:
            return self.a * self.gamma * self.S * self.beta / 1 * (self.periods[1]/period)
        elif (period >= self.periods[2]):
            return self.a * self.gamma * self.S * self.beta / 1 * self.periods[1]*self.periods[2]/period**2

    def update_data_table(self, modes):
        
        data = np.zeros((11,3))
        
        counter = 2
        for mode in modes:
            # fill-in the period
            data[0,counter] = 2*np.pi / mode.frequency
    
            # fill-in the Participation Factor
            data[1,counter] = mode.participationFactor

            # fill-in the Modal mass
            data[2,counter] = 0

            # fill-in the Spectral acceleration
            data[3,counter] = self.get_Sa(data[0,counter])
            
            # fill-in the First Storey Max. Displacement
            data[5,counter] = mode.maxModeShape[0]
            # fill-in the Second Storey Max. Displacement
            data[6,counter] = mode.maxModeShape[1]
            # fill-in the Third Storey Max. Displacement
            data[7,counter] = mode.maxModeShape[2]
            
            
            maxForce = np.dot(mode.K , mode.maxModeShape)
            # fill-in the First Storey Total Force
            data[8,counter] = maxForce[0]
            # fill-in the Second Storey Total Force
            data[9,counter] = maxForce[1]
            # fill-in the Third Storey Total Force
            data[10,counter] = maxForce[2]

            # fill-in the Total Force
            data[4,counter] = maxForce[0] + maxForce[1] + maxForce[2]

            counter -= 1
        
        # update the table data
        self.informationTable.data = dict(
                                          subject = self.informationTable.data['subject'],
                                          modeOne = data[:,0],
                                          modeTwo = data[:,1],
                                          modeThree = data[:,2]
                                         )
def cubic_N1 (xi):
    #print('xi = ',xi)
    #print('cubic_N1 = ',0.25 * ((1-xi)*(1-xi)) * (2+xi))
    return 0.25 * (1-xi)*(1-xi) * (2+xi)
def cubic_N2 (xi):
    #print('xi = ',xi)
    #print('cubic_N2 = ',0.25 * ((1+xi)*(1+xi)) * (2-xi))
    return 0.25 * (1+xi)*(1+xi) * (2-xi)
    
def cubicInterpolate(y1, y2, x1, x2, noNodes,length):
    nodes = np.ones(noNodes)
    i = 0.0
    while i<noNodes:
        x = i*2.0/(float(noNodes)-1.0) - 1.0
        nodes[int(i)] = cubic_N1(x)*y1 + cubic_N2(x)*y2
        #print('value = ',nodes[int(i)])
        i += 1.0
        #print('------------------------------')

    return(nodes)
    
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

    return(nodes)
    
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
        
        maximumDisplacement.append( siesmicParameters.get_Sa(period[i]) )
        
def update_ERS_plot_data( siesmicParameters ):
    n = 1000
    tMin = 0.0
    tMax = siesmicParameters.periods[2] + 1
    x = np.zeros(n)
    y = np.zeros(n)

    # Determine the corresponsing Se value
    for i in range(0,n):
        T = (tMax - tMin)/n * i + tMin
        x[i] = T
        y[i] = siesmicParameters.get_Sa(T)

    siesmicParameters.ERSdata.data = dict(x=x, y=y)