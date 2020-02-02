import numpy as np
from bokeh.plotting import Figure, ColumnDataSource
from bokeh.models import Range1d
from numpy.linalg import inv
from scipy.linalg import eig
from math import cos, sin, radians, sqrt, pi, atan2

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
                                       mu, kappa, D1, D2,
                                       Amplification_source, Phase_source,
                                       k1, m1
                                      ):
    eta = []
    Amplification = []
    Phase = []
    for i in range(0,500):
        eta.append(i/100)
        eta_i = i/100

        b1 = (kappa**2)-(eta_i**2)
        b2 = 2*eta_i*kappa*D2
        b3 = (eta_i**4)-(eta_i**2)*(1+(kappa**2)+mu*(kappa**2)+4*kappa*D1*D2)+(kappa**2)
        b4 = eta_i*(2*D1*((kappa**2)-(eta_i**2))+2*kappa*D2*(1-(eta_i**2)-mu*(eta_i**2)))
        Amplification.append(sqrt(((b1**2)+(b2**2))/((b3**2)+(b4**2))))

        a1 = ((kappa*sqrt(k1/m1))**2)-((eta_i*sqrt(k1/m1))**2)
        a2 = 2*D2*kappa*sqrt(k1/m1)*eta_i*sqrt(k1/m1)
        a3 = ((eta_i*sqrt(k1/m1))**4)-((eta_i*sqrt(k1/m1))**2)*((sqrt(k1/m1)**2)+((kappa*sqrt(k1/m1))**2)+mu*((kappa*sqrt(k1/m1))**2)+4*sqrt(k1/m1)*kappa*sqrt(k1/m1)*D1*D2)+(sqrt(k1/m1)**2)*((kappa*sqrt(k1/m1))**2)
        a4 = 2*eta_i*sqrt(k1/m1)*(sqrt(k1/m1)*D1*(((kappa*sqrt(k1/m1))**2)-((eta_i*sqrt(k1/m1))**2))+D2*kappa*sqrt(k1/m1)*((sqrt(k1/m1)**2)-((eta_i*sqrt(k1/m1))**2)-mu*((eta_i*sqrt(k1/m1))**2)))
        u_Re = (a1*a3+a2*a4)/(m1*(a3**2)+(a4**2))
        u_Im = (a2*a3-a1*a4)/(m1*(a3**2)+(a4**2))
        
        Phase.append(-atan2(u_Im, u_Re))
        
    Amplification_source.data = dict(x=eta, y=Amplification)
    
    Phase_source.data = dict(x=eta, y=Phase)
    
    
def Calculate_Current_Amplification_PhaseAngle(
                                               eta_i, kappa, mu, D1, D2,
                                               Amplification_current_source, PhaseAngle_current_source,k1,m1
                                              ):
    b1 = (kappa**2)-(eta_i**2)
    b2 = 2*eta_i*kappa*D2
    b3 = (eta_i**4)-(eta_i**2)*(1+(kappa**2)+mu*(kappa**2)+4*kappa*D1*D2)+(kappa**2)
    b4 = eta_i*(2*D1*((kappa**2)-(eta_i**2))+2*kappa*D2*(1-(eta_i**2)-mu*(eta_i**2)))
    Amplification = (sqrt(((b1**2)+(b2**2))/((b3**2)+(b4**2))))

    a1 = ((kappa*sqrt(k1/m1))**2)-((eta_i*sqrt(k1/m1))**2)
    a2 = 2*D2*kappa*sqrt(k1/m1)*eta_i*sqrt(k1/m1)
    a3 = ((eta_i*sqrt(k1/m1))**4)-((eta_i*sqrt(k1/m1))**2)*((sqrt(k1/m1)**2)+((kappa*sqrt(k1/m1))**2)+mu*((kappa*sqrt(k1/m1))**2)+4*sqrt(k1/m1)*kappa*sqrt(k1/m1)*D1*D2)+(sqrt(k1/m1)**2)*((kappa*sqrt(k1/m1))**2)
    a4 = 2*eta_i*sqrt(k1/m1)*(sqrt(k1/m1)*D1*(((kappa*sqrt(k1/m1))**2)-((eta_i*sqrt(k1/m1))**2))+D2*kappa*sqrt(k1/m1)*((sqrt(k1/m1)**2)-((eta_i*sqrt(k1/m1))**2)-mu*((eta_i*sqrt(k1/m1))**2)))
    u_Re = (a1*a3+a2*a4)/(m1*(a3**2)+(a4**2))
    u_Im = (a2*a3-a1*a4)/(m1*(a3**2)+(a4**2))
        
    Phase = (-atan2(u_Im, u_Re))
    Amplification_current_source.data = dict(
                                               x=[eta_i], 
                                               y=[Amplification],
                                               c=['#0033FF']
                                              )   
    PhaseAngle_current_source.data = dict(
                                               x=[eta_i], 
                                               y=[Phase],
                                               c=['#0033FF']
                                              )                                          

def Clear_Time_History(main_displacement_time_source, topMass_displacement_time_source):
    # Get the last displacement of both main and top masses
    MainMass_end = main_displacement_time_source.data['y'][-1]
    TopMass_end  = topMass_displacement_time_source.data['y'][-1]

    # Clear the sources and initialize it with last displacement
    main_displacement_time_source.data = dict(x=[0],y=[MainMass_end])
    topMass_displacement_time_source.data = dict(x=[0],y=[TopMass_end])