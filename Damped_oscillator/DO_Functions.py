import numpy as np
from bokeh.plotting import Figure, ColumnDataSource

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
    eta = np.linspace(0, eta_max, n_points)
    tan_alpha = 2*D*eta / (1-eta**2)
    alpha = np.arctan( tan_alpha )
    
    # Construct the graph
    function_source.data = dict(x = eta, y = alpha)
    # Maximum Vr calculation
    alpha_max = np.pi
    
    # Calculate the plot boundaries
    frequencyRatio_range.end = eta_max
    phaseAngle_range.start = 0
    phaseAngle_range.end   = 1.2 * alpha_max
    
    eta_current = Omega/We
    alpha_current = np.arctan( 2*D*eta / (1-eta**2) )
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