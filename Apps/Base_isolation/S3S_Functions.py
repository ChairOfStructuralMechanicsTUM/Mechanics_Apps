from __future__ import division

from bokeh.models import ColumnDataSource
import numpy as np
from scipy import linalg
from bokeh.models.widgets import Div

from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv

class S3S_Structure:
    
    def __init__(self, masses, massSupports, trusses, trussLength, base, isolation):
        
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
        
        isolationlist = list()
        for i in range(len(isolation)):
            isolationlist.append( ColumnDataSource(data=isolation[i]) )
        self.isolation      = isolationlist

        self.trusses_patch = ColumnDataSource(data=dict(x=np.concatenate((self.trusses[0].data['x'] , self.trusses[1].data['x'][::-1])), y=np.concatenate((self.trusses[0].data['y'] , self.trusses[1].data['y'][::-1])) ))
        self.trussLength  = trussLength
        self.base         = ColumnDataSource(base)
        
        # System matrices
        self.M = np.zeros((2,2))
        self.C = np.zeros((2,2))
        self.K = np.zeros((2,2))
        
        # Mass locations
        self.massLocations = np.zeros((2,2))
        
        # Force indicator (forces indicate in the plotting domain the force 
        # carried by each of the truss members besides the location where to
        # display the force values) ((Here default value are given))
        self.forces = ColumnDataSource(
                                       data=dict(
                                                 x=[0,0],
                                                 y=[0,0],
                                                 force=['Force = ','Force = ']
                                                )
                                      )
                                      
        self.massIndicators = ColumnDataSource(
                                               data=dict(
                                                         x=[0,0],
                                                         y=[0,0],
                                                         mass=['','']
                                                        )
                                              )
                                               
        self.stiffnessIndicators = ColumnDataSource(
                                                    data=dict(
                                                              x=[0,0],
                                                              y=[0,0],
                                                              stiffness=['','']
                                                             )
                                                   )
                                                    
        self.maximumDisplacement = ColumnDataSource(data=dict(storey=["First","Seconds"],maxDisp=[0.0,0.0]))
       
    def update_system(self, displacement):
        self.update_masses(displacement)
        self.update_mass_indicator_locaiton()
        self.update_massSupprts(displacement)
        self.update_stiffness_indicator_locaiton()
        self.update_truss_sources()
        self.update_isolation()
        
    def update_masses(self, displacement):
        self.masses[0].data = dict(x=[displacement[0]] , y=self.masses[0].data['y'])
        self.masses[1].data = dict(x=[displacement[1]] , y=self.masses[1].data['y'])
        
        self.update_mass_indicator_locaiton

    def update_massSupprts(self, displacement):
        self.massSupports[0].data['x'] = self.massSupports[0].data['x']*0 + [-self.trussLength/2+displacement[0], self.trussLength/2+displacement[0]]
        self.massSupports[1].data['x'] = self.massSupports[1].data['x']*0 + [-self.trussLength/2+displacement[1], self.trussLength/2+displacement[1]]

    def update_truss_sources(self):
        noNodes = 10
        
        # truss1
        x1 = - self.trussLength/2
        x2 = self.masses[0].data['x'][0] - self.trussLength/2
        y1 = 0.0
        y2 = self.masses[0].data['y'][0] - self.trussLength/2

        ys = linIntepolate(y1,y2,y1,y2,noNodes,self.trussLength/3)
        xs = cubicInterpolate(x1,x2,y1,y2,noNodes,self.trussLength)
        
        self.trusses[0].data = dict( x=xs, y=ys )

        # truss2
        x1 =   self.trussLength/2
        x2 = self.masses[0].data['x'][0] + self.trussLength/2
        y1 = 0.0
        y2 = self.masses[0].data['y'][0] - self.trussLength/2

        xs = cubicInterpolate(x1,x2,y1,y2,noNodes,self.trussLength)
        ys = linIntepolate(y1,y2,y1,y2,noNodes,self.trussLength/3)
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
        
        new_x = np.concatenate((self.trusses[0].data['x'] , self.trusses[1].data['x'][::-1]))
        new_y = np.concatenate((self.trusses[0].data['y'] , self.trusses[1].data['y'][::-1]))
        self.trusses_patch.data = dict(x=new_x, y=new_y)

    def update_isolation(self):
        noNodes = 10
        
        # isolation left
        x1 = - self.trussLength
        x2 = self.masses[0].data['x'][0] - self.trussLength/2
        y1 = 0.0
        y2 = self.masses[0].data['y'][0] 

        ys = linIntepolate(y1,y2,y1,y2,noNodes,self.trussLength)
        xs = cubicInterpolate(x1,x2,y1,y2,noNodes,self.trussLength)
        
        self.isolation[0].data = dict( x=xs, y=ys )

        # isolation right
        x1 =   self.trussLength/2
        x2 = self.masses[0].data['x'][0] + self.trussLength/2
        y1 = 0.0
        y2 = self.masses[0].data['y'][0] 

        xs = cubicInterpolate(x1,x2,y1,y2,noNodes,self.trussLength)
        ys = linIntepolate(y1,y2,y1,y2,noNodes,self.trussLength)
        self.isolation[1].data = dict( x=xs, y=ys )

    def update_force_indicator_location(self):
        # first force indicator
        x1 = (self.trusses[1].data['x'][0] + self.trusses[1].data['x'][1]) / 2 + 2.5 # where 2.5 is an offset value
        y1 = (self.trusses[1].data['y'][1] + self.trusses[1].data['y'][0]) / 2
        
        # second force indicator
        x2 = (self.trusses[3].data['x'][0] + self.trusses[3].data['x'][1]) / 2 + 2.5
        y2 = (self.trusses[3].data['y'][1] + self.trusses[3].data['y'][0]) / 2
              
        # update the source fle
        self.forces.data = dict(x=[x1,x2],y=[y1,y2],force=self.forces.data['force'])
              

    def update_mass_indicator_locaiton(self):
        updateLocation = list()
        for i in self.masses:
            updateLocation.append( i.data['y'][0] + 0.5 )
        self.massIndicators.data = dict(
                                        x=[self.masses[0].data['x'][0], self.masses[1].data['x'][0]],
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
                                             storey=["First","Seconds"],
                                             maxDisp=[
                                                      round(self.masses[0].data['x'][0],2),
                                                      round(self.masses[1].data['x'][0],2)
                                                     ]       
                                             )
                                             
class S3S_Mode( S3S_Structure ):
    
    def __init__(self, ID, masses, massSupports, trusses, trussLength, base, isolation, frequency, modeShape):
        S3S_Structure.__init__(self, masses, massSupports, trusses, trussLength, base, isolation)
        self.id = ID
        self.frequency = frequency
        self.modeShape = modeShape
        self.maxModeShape = np.array([0,0]) # 0 is a default value
        self.locationInERS = ColumnDataSource(data=dict(x=[0],y=[0])) # with default values
        self.participationFactor = 0 # 0 is a default value
        
        self.multiplier_text = LatexDiv(text=" $\\displaystyle\\frac{\\beta S_a(T) }{ \\omega^2} ="+ str(0) + "$", width=300)
        self.frequency_text  = LatexDiv(text="""<b>Natural Frequency =</b> """, width=300)
    
    def get_maximum_displacement( self, siesmicParameters ):
        r = np.ones(2)
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
        self.multiplier_text.text = " $\\displaystyle\\frac{\\beta S_a(T)}{ \\omega^2} ="+ '{:.3f}'.format(multiplier) + "$"
        
    def modify_frequency_text(self):
        self.frequency_text.text = "$\\text{Natural Frequency} = " + '{:.3f}'.format(self.frequency) + "\\, \\frac{\\mathrm{rad}}{\\mathrm{s}}$"
        
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




class S3S_SeismicParameters():
    
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
                                                           subject=['Period [second]',"Participation Factor ("u"\u03b2)","Modal Mass ("u"\u03b1)",
                                                                    "Spectral Acceleration [m/s"u"\u00B2]",'Total Force [N]',
                                                                    'First Storey Max. Displacement [mm]','Second Storey Max. Displacement [mm]',
                                                                    'First Storey Total Force [N]',
                                                                    'Second Storey Total Force [N]'],
                                                            modeOne  =[0,0,0,0,0,0,0,0,0],
                                                            modeTwo  =[0,0,0,0,0,0,0,0,0]
                                                          )
                                                )
        self.informationTable_two = ColumnDataSource(
                                                    data=dict(
                                                                subject = ['Period [second]', "Spectral Acceleration [m/s"u"\u00B2]",
                                                                           'Total Force [N]','Second Storey Max. Displacement [mm]'],
                                                                iso        = [0,0,0,0],
                                                                noiso      = [0,0,0,0]
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
        
        data = np.zeros((9,3))
        
        counter = 1
        for mode in modes:
            # fill-in the period
            data[0,counter] = round(2*np.pi / mode.frequency , 2)
    
            # fill-in the Participation Factor
            data[1,counter] = round(mode.participationFactor, 2)

            # fill-in the Modal mass
            tempValue = 0
            for comp in modes:
                tempValue += comp.participationFactor**2
            data[2,counter] = round(mode.participationFactor**2 / tempValue , 2)

            # fill-in the Spectral acceleration
            data[3,counter] = round(self.get_Sa(data[0,counter]) , 2)
            
            # fill-in the First Storey Max. Displacement
            data[5,counter] = round(mode.maxModeShape[0] * 1000 , 2) # to convert to mm
            # fill-in the Second Storey Max. Displacement
            data[6,counter] = round(mode.maxModeShape[1] * 1000 , 2) # to convert to mm 
            
            
            
            maxForce = np.dot(mode.K , mode.maxModeShape)
            # fill-in the First Storey Total Force
            data[7,counter] = round(maxForce[0] , 2)
            # fill-in the Second Storey Total Force
            data[8,counter] = round(maxForce[1] , 2)

            # fill-in the Total Force
            data[4,counter] = round(maxForce[0] + maxForce[1] , 2)

            counter -= 1
        
        # update the table data
        self.informationTable.data = dict(
                                          subject = self.informationTable.data['subject'],
                                          modeOne = data[:,0],
                                          modeTwo = data[:,1],
                                         )

    def update_data_table_two(self, mode): 

        data = np.zeros((4,2))
        # fill-in the period
        data[0,1] = round(2*np.pi / mode.frequency , 2)
        data[0,0] = round(2*np.pi / np.sqrt((mode.K[1,1])/(mode.M[1,1])) , 2)
    

        # fill-in the Spectral acceleration
        data[1,1] = round(self.get_Sa(data[0,1]) , 2)
        data[1,0] = round(self.get_Sa(data[0,0]) , 2)

        maxForce = np.dot(mode.K , mode.maxModeShape)

        # fill-in the Total Force
        data[2,1] = round(maxForce[1] , 2)
        data[2,0] = round(mode.M[1,1]*data[1,0] , 2)  
             
        #  fill-in the Second Storey Max. Displacement
        data[3,1] = round(mode.maxModeShape[0] * 1000 , 2) # to convert to mm 
        data[3,0] = round((data[2,0]/mode.K[1,1])* 1000 , 2) # to convert to mm  

        self.informationTable_two.data = dict(
                                          subject = self.informationTable_two.data['subject'],
                                          noiso = data[:,1],    
                                          iso = data[:,0],
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
        i += 1.0

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
    
def construct_truss_sources(massOne, massTwo, length):
    
    # The convention used here is that the first entry of both the x and y vectors
    # represent the lower node and the second represents the upper node

    trussOne   = dict(
                        x=[massOne['x'][0] - length/2, massOne['x'][0] - length/2],
                        y=[massOne['y'][0] - length  , massOne['y'][0] - length*2/3]
                     )

    trussTwo   = dict(
                        x=[massOne['x'][0] + length/2, massOne['x'][0] + length/2],
                        y=[massOne['y'][0] - length  , massOne['y'][0] - length*2/3]
                     )
    trussThree = dict(
                        x=[massTwo['x'][0] - length/2, massTwo['x'][0] - length/2],
                        y=[massOne['y'][0]           , massTwo['y'][0]           ]
                     )
    trussFour  = dict(
                        x=[massTwo['x'][0] + length/2, massTwo['x'][0] + length/2],
                        y=[massOne['y'][0]           , massTwo['y'][0]           ]
                     )
                       
    trussSources = list()
    trussSources.append(trussOne)
    trussSources.append(trussTwo)
    trussSources.append(trussThree)
    trussSources.append(trussFour)
   
    
    return trussSources    
def construct_isolation(massOne, massTwo, length):    
    isolationOne   = dict(
                        x=[massOne['x'][0] - length/2, massOne['x'][0] - length/2],
                        y=[massOne['y'][0] - length  , massOne['y'][0]           ]
                     )

    isolationTwo   = dict(
                        x=[massOne['x'][0] + length/2, massOne['x'][0] + length/2],
                        y=[massOne['y'][0] - length  , massOne['y'][0]           ]
                     ) 

    isolationlist = list()
    isolationlist.append(isolationOne)            
    isolationlist.append(isolationTwo)
    return isolationlist 

def construct_masses_and_supports(length):
    
    masses = list()
    massSupports = list()
    
    massOne = dict(x=[0.0],y=[length/3])
    massTwo = dict(x=[0.0],y=[length*4/3])

    masses.append(massOne)
    masses.append(massTwo)
    
    massOneSupport = dict(
                            x=[massOne['x'][0] - length/2, massOne['x'][0] + length/2],
                            y=[massOne['y'][0]          , massOne['y'][0]            ]
                         )
    massTwoSupport = dict(
                            x=[massTwo['x'][0] - length/2, massTwo['x'][0] + length/2],
                            y=[massTwo['y'][0]           , massTwo['y'][0]           ]
                         )
                                      
    massSupports.append(massOneSupport)
    massSupports.append(massTwoSupport)
    
    return masses, massSupports
     
def construct_system(structure, mass, massRatio, bendingStiffness, stiffnessRatio, trussLength):
    structure.massIndicators.data = dict(
                                         x=structure.massIndicators.data['x'],
                                         y=structure.massIndicators.data['y'],
                                         mass=[str(massRatio[0])+'m',str(massRatio[1])+'m']
                                        )
    
    structure.stiffnessIndicators.data = dict(
                                     x=structure.stiffnessIndicators.data['x'],
                                     y=structure.stiffnessIndicators.data['y'],
                                     stiffness=[str(stiffnessRatio[0])+'EI',str(stiffnessRatio[1])+'EI']
                                    )
    
    structure.M = np.array([[massRatio[0],      0       ],
                            [      0      ,massRatio[1] ]]) * mass
                           
    structure.K = np.array([
                            [stiffnessRatio[0]+stiffnessRatio[1],         -stiffnessRatio[1]        ],
                            [        -stiffnessRatio[1]         ,stiffnessRatio[1]                   ],
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

    amplitude = np.zeros((2,N))
    for mass in range(2):
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
    plot_name.patch( x='x', y='y', source=subject.trusses_patch , color='#AEACAC' , alpha=1)

    plot_name.line( x='x', y='y', source=subject.massSupports[0], color='#484848', line_width=5)
    plot_name.line( x='x', y='y', source=subject.massSupports[1], color='#484848', line_width=5)
    
    plot_name.circle( x='x',y='y',radius=radius,color='#484848',source=subject.masses[0] )
    plot_name.circle( x='x',y='y',radius=radius,color='#484848',source=subject.masses[1] )

    plot_name.line( x='x', y='y', color='#484848', source=subject.trusses[2], line_width=2)
    plot_name.line( x='x', y='y', color='#484848', source=subject.trusses[3], line_width=2)
    
    
def GetMaximumDisplacement( modes, siesmicParameters ):
    
    maximumDisplacement = list()
    r = np.array([1,1])
    
    beta = list()
    period = list()
    Sa = list() # never used?
    for i in range(0,2):
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
