import numpy as np
from bokeh.plotting import Figure, ColumnDataSource
from bokeh.models import Range1d
from numpy.linalg import inv
from scipy.linalg import eig

def Base_forced_amplification_function_plot( m, c, We, Omega_max, n_points, plot_width, plot_height ):
    
    # Maximum eta calculation
    eta_max = Omega_max / We
    
    D = c / (2*m*We)
    
    # Construct x and y axis of the plot
    eta = np.linspace(0, eta_max, n_points)
    Vr  = np.abs( eta**2 / np.sqrt( (1-eta**2)**2 + (2*D*eta)**2 ) )
    
    # Construct the graph
    source = ColumnDataSource(data = dict(x = eta, y = Vr))
    # Maximum Vr calculation
    Vr_max = np.max(Vr)
    
    plot = Figure(
                    plot_width = plot_width,
                    plot_height= plot_height,
                    x_range  =(0, eta_max),
                    y_range  =(0, Vr_max*1.2), # Multiplied by 1.2 to give more space at the top
                    title = 'Collision Play Ground',
                    tools=''
                 )
    
    plot.line(x='x',y='y', source = source)
    
    return plot
    
def phaseAngle_function( m, k, c, Fo, Omega_max, Omega, n_points,
                         function_source, state_source,
                         phaseAngle_range, frequencyRatio_range):
    # Maximum eta calculation
    We = np.sqrt(k/m)
    eta_max = Omega_max / We
    D = c / (2*m*We)
    
    # Construct x and y axis of the plot
    eta = np.linspace(0, eta_max, 500)
    tan_alpha = 2*D*eta / (1-eta**2)
    alpha = np.arctan( tan_alpha )
    for i in range(0,len(alpha)): # This for loop tries to pull the negative angles
        if alpha[i] < 0:          # to the positive side because the np.tan assumes
            alpha[i] += np.pi     # the domain of the tan function from -pi to pi;
                                  # however, it should be from 0 to pi
                                  
    # Construct the graph
    function_source.data = dict(x = eta, y = alpha)
    # Maximum Vr calculation
    alpha_max = np.pi
    
    # Calculate the plot boundaries
    frequencyRatio_range.end = eta_max
    phaseAngle_range.start = 0
    phaseAngle_range.end   = 1.2 * alpha_max
    
    eta_current = Omega/We
    alpha_current = np.arctan( 2*D*eta_current / (1-eta_current**2) )
    if alpha_current < 0:
        alpha_current += np.pi
    state_source.data = dict(x = [eta_current], y = [alpha_current])
    
def force_forced_amplfication_function( 
                                       m, k, c, Fo, Omega_max, Omega, n_points,
                                       function_source, state_source,
                                       amplification_range, frequencyRatio_range
                                      ):
    # Maximum eta calculation
    We = np.sqrt(k/m)
    eta_max = Omega_max / We
    D = c / (2*m*We)
    
    # Construct x and y axis of the plot
    eta = np.linspace(0, eta_max, n_points)
    V  = np.abs( Fo/k / np.sqrt( (1-eta**2)**2 + (2*D*eta)**2 ) )
    
    # Construct the graph
    function_source.data = dict(x = eta, y = V)

    # Determine the maximum value of the amplification factor
    V_max = np.max(function_source.data['y'])

    # Define the boundaries of the plot
    frequencyRatio_range.end =  eta_max
    amplification_range.start = 0
    amplification_range.end =  abs(V_max*1.2) # Multiplied by 1.2 to give more space at the top
    
    V_of_Omega = np.abs( Fo/k / np.sqrt( (1-(Omega/We)**2)**2 + (2*D*Omega/We)**2 ) )
    state_source.data = dict(x = [Omega/We], y = [V_of_Omega])
    
def Calculate_MagnificationFactor_PhaseAngle( 
                                       m1, m2, k1, k2, c2, Fo, Omega_max, Omega, n_points,
                                       Amplification1_source, Amplification2_source, Phase1_source, Phase2_source,
                                       amplification_range, phaseAngle_range, frequencyRatio_range,
                                      ):
    # Calculate eigenfrequencies
    M_eigen = np.array([
                        [m1, 0],
                        [ 0,m2]
                      ])
    K_eigen = np.array([
                        [k1+k2, -k2],
                        [ -k2 ,  k2]
                      ])

    eigenvalues, eigenvectors = eig(K_eigen, -1j*M_eigen)

    We1 = min(np.sqrt(abs(eigenvalues[0])) , np.sqrt(abs(eigenvalues[1])))
    We2 = max(np.sqrt(abs(eigenvalues[0])) , np.sqrt(abs(eigenvalues[1])))
    
    eta_max1 = Omega_max / We1
    eta_max2 = Omega_max / We2
    
    #eta_max = max(eta_max1, eta_max2)
    
    # Construct x and y axis of the plot
    eta1 = np.linspace(0, eta_max1, n_points)
    eta2 = np.linspace(0, eta_max2, n_points)
    omega = np.linspace(0, Omega_max, n_points)
    
    # Construction of the linear problem to calculate the magnificatio factors
    # and the phase angles. Source: http://www.brown.edu/Departments/Engineering/Courses/En4/Notes/vibrations_mdof/vibrations_mdof.htm
    M = np.array([
                     [1, 0, 0,  0],
                     [0, 1, 0,  0],
                     [0, 0, m1, 0],
                     [0, 0, 0, m2]
                ])
    D = np.array([
                     [  0  ,  0  , -1  ,  0],
                     [  0  ,  0  ,  0  , -1],
                     [k1+k2, -k2 , c2  , -c2],
                     [ -k2 ,  k2 , -c2 ,  c2]
                ])
    F = np.array([0, 0, Fo, 0])
    
    Y = list()
    for i in range(0,n_points):
        inverse = inv(omega[i]*1j*M + D) 
        vector = np.dot( inverse , F )
        Y.append(vector)
    Y = np.transpose( np.array(Y) )

    # Interpretation of the result
    Amplification1 = np.sqrt(np.real(Y[0,:])**2 + np.imag(Y[0,:])**2) / (Fo/k1)
    Amplification2 = np.sqrt(np.real(Y[1,:])**2 + np.imag(Y[1,:])**2) / (Fo/k2)
    
    Phase1 = np.arctan(-np.imag(Y[0,:]) / np.real(Y[0,:]))
    Phase2 = np.arctan(-np.imag(Y[1,:]) / np.real(Y[1,:]))
    for i in range(0,len(Phase1)):
        if Phase1[i] < 0:
            Phase1[i] += np.pi
    for i in range(0,len(Phase2)):
        if Phase2[i] < 0:
            Phase2[i] += np.pi
    
    # Define again the source files
    Amplification1_source.data = dict(x=eta1, y=Amplification1)
    Amplification2_source.data = dict(x=eta2, y=Amplification2)
    
    Phase1_source.data = dict(x=eta1, y=Phase1)
    Phase2_source.data = dict(x=eta2, y=Phase2)
    
    # Determine maximum amplification and phase angle
    Max_Amplification = max( np.max(Amplification1) , np.max(Amplification2) )
    Max_PhaseAngle    = max( np.max(Phase1) , np.max(Phase2) )
    
    # Define the boundaries of the plot
    frequencyRatio_range.end =  max(eta_max1, eta_max2)
    amplification_range.start = 0
    amplification_range.end =  abs(Max_Amplification*1.2) # Multiplied by 1.2 to give more space at the top
    
    phaseAngle_range.start = 0
    phaseAngle_range.end = abs(Max_PhaseAngle*1.2)
    
    
def Calculate_Current_Amplification_PhaseAngle(
                                               m1, m2, k1, k2, c2, Fo, Omega_max, Omega,
                                               Amplification_current_source, PhaseAngle_current_source
                                              ):
    # Calculate eigenfrequencies
    M_eigen = np.array([
                        [m1, 0],
                        [ 0,m2]
                      ])
    K_eigen = np.array([
                        [k1+k2, -k2],
                        [ -k2 ,  k2]
                      ])

    eigenvalues, eigenvectors = eig(K_eigen, -1j*M_eigen)
  
    We1 = min(np.sqrt(abs(eigenvalues[0])) , np.sqrt(abs(eigenvalues[1])))#np.sqrt(k1/m1)
    We2 = max(np.sqrt(abs(eigenvalues[0])) , np.sqrt(abs(eigenvalues[1])))#np.sqrt(k2/m2)
    
    # Construction of the linear problem to calculate the magnificatio factors
    # and the phase angles. Source: http://www.brown.edu/Departments/Engineering/Courses/En4/Notes/vibrations_mdof/vibrations_mdof.htm
    M = np.array([
                     [1, 0, 0,  0],
                     [0, 1, 0,  0],
                     [0, 0, m1, 0],
                     [0, 0, 0, m2]
                ])
    D = np.array([
                     [  0  ,  0  , -1  ,  0],
                     [  0  ,  0  ,  0  , -1],
                     [k1+k2, -k2 , c2  , -c2],
                     [ -k2 ,  k2 , -c2 ,  c2]
                ])
    F = np.array([0, 0, Fo, 0])
    
    # Define the current position of the system in the amplificatio factor and
    # phase-angle diagrams
    Y_current = np.dot( inv(Omega*1j*M+D), F )
    
    eta_1 = Omega / We1
    eta_2 = Omega / We2
    
    Amplification_current_1 = np.sqrt(np.real(Y_current[0])**2 + np.imag(Y_current[0])**2) / (Fo/k1)
    Amplification_current_2 = np.sqrt(np.real(Y_current[1])**2 + np.imag(Y_current[1])**2) / (Fo/k2)
    
    Phase_current_1 = np.arctan(-np.imag(Y_current[0]) / np.real(Y_current[0]))#np.real( np.tan( np.conjugate(Y[0,:]) / Y[0,:] ) / (2*1j) )
    Phase_current_2 = np.arctan(-np.imag(Y_current[1]) / np.real(Y_current[1]))#np.real( np.tan( np.conjugate(Y[1,:]) / Y[1,:] ) / (2*1j) )
    if Phase_current_1 < 0:
        Phase_current_1 += np.pi
    if Phase_current_2 < 0:
        Phase_current_2 += np.pi
#    Amplification_current_source.data = dict(
#                                               x=[eta_1,eta_2], 
#                                               y=[Amplification_current_1,Amplification_current_2],
#                                               c=['#0033FF', '#330011']
#                                              )
#    PhaseAngle_current_source.data = dict(
#                                               x=[eta_1,eta_2], 
#                                               y=[Phase_current_1,Phase_current_2],
#                                               c=['#0033FF', '#330011']
#                                              )
    ### To show only the main mass' state ###
    Amplification_current_source.data = dict(
                                               x=[eta_1], 
                                               y=[Amplification_current_1],
                                               c=['#0033FF']
                                              )
    PhaseAngle_current_source.data = dict(
                                               x=[eta_1], 
                                               y=[Phase_current_1],
                                               c=['#0033FF']
                                              )
    
def Clear_Time_History(main_displacement_time_source, topMass_displacement_time_source):
    # Get the last displacement of both main and top masses
    MainMass_end = main_displacement_time_source.data['y'][-1]
    TopMass_end  = topMass_displacement_time_source.data['y'][-1]

    # Clear the sources and initialize it with last displacement
    main_displacement_time_source.data = dict(x=[0],y=[MainMass_end])
    topMass_displacement_time_source.data = dict(x=[0],y=[TopMass_end])