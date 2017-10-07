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
    
def phase_function_plot( m, c, We, Omega_max, n_points, plot_width, plot_height ):
    # Maximum eta calculation
    eta_max = Omega_max / We
    
    D = c / (2*m*We)
    
    # Construct x and y axis of the plot
    eta = np.linspace(0, eta_max, n_points)
    tan_alpha = 2*D*eta / (1-eta**2)
    alpha = np.arctan( tan_alpha )
    
    # Construct the graph
    source = ColumnDataSource(data = dict(x = eta, y = alpha))
    # Maximum Vr calculation
    alpha_max = np.pi
    
    plot = Figure(
                    plot_width = plot_width,
                    plot_height= plot_height,
                    x_range  =(0, eta_max),
                    y_range  =(0, alpha_max*1.2), # Multiplied by 1.2 to give more space at the top
                    title = 'Collision Play Ground',
                    tools=''
                 )
    
    plot.line(x='x',y='y', source = source)
    
    return plot
    
def force_forced_amplfication_function_plot( m, k, c, F, We, Omega_max, n_points, plot_width, plot_height ):
    # Maximum eta calculation
    eta_max = Omega_max / We
    
    D = c / (2*m*We)
    
    # Construct x and y axis of the plot
    eta = np.linspace(0, eta_max, n_points)
    V  = np.abs( F/k / np.sqrt( (1-eta**2)**2 + (2*D*eta)**2 ) )
    
    # Construct the graph
    source = ColumnDataSource(data = dict(x = eta, y = V))
    # Maximum Vr calculation
    V_max = np.max(V)
    
    plot = Figure(
                    plot_width = plot_width,
                    plot_height= plot_height,
                    x_range  =(0, eta_max),
                    y_range  =(0, V_max*1.2), # Multiplied by 1.2 to give more space at the top
                    title = 'Collision Play Ground',
                    tools=''
                 )
    
    plot.line(x='x',y='y', source = source)
    
    return plot