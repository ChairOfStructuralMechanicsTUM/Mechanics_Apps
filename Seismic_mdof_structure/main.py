'''
###############################################################################
Imports
###############################################################################
'''
import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.io import curdoc
from Functions import *
from bokeh.models import Arrow, OpenHead, Button, Slider
from bokeh.layouts import column, row
from bokeh.models.widgets import TextInput
from os.path import dirname, join, split
from Functions import *

'''
###############################################################################
Create the plotting domain 
###############################################################################
'''
xmin, xmax = -2.5,2.5
ymin, ymax = 0,5
time_plot = figure(
                      plot_width=400,
                      plot_height=400,
                      x_range=[xmin,xmax], 
                      y_range=[ymin,ymax],
                      
                      title = '',
                  )
time_plot.title.text_font_size = "25px"
time_plot.title.align = "center"
time_plot.grid.visible=False
time_plot.xaxis.visible=False
time_plot.yaxis.visible=False

modes_plot = figure(
                      plot_width=400,
                      plot_height=400,
                      x_range=[xmin,xmax], 
                      y_range=[ymin,ymax],
                      
                      title = '',
                   )
modes_plot.title.text_font_size = "25px"
modes_plot.title.align = "center"
modes_plot.grid.visible=False
modes_plot.xaxis.visible=False
modes_plot.yaxis.visible=False

siesmic_input_plot = figure(
                      plot_width=400,
                      plot_height=400,
                      x_range=[0.0,2000], 
                      y_range=[-1.0,1.0],
                      
                      title = '',
                   )
siesmic_input_plot.title.text_font_size = "25px"
siesmic_input_plot.title.align = "center"
siesmic_input_plot.grid.visible=False
siesmic_input_plot.xaxis.visible=False
siesmic_input_plot.yaxis.visible=False

Active = True

'''
###############################################################################
Define the objects to be plotted within the plotting domain
    (1) truss members
    (2) masses
    (3) base
###############################################################################
'''
################################ (1) masses ###################################
'''
                                ====Mass3===
                                |          |
                                |          |
                                ====Mass2===
                                |          |
                                |          |
                                ====Mass1===
                                |          |
                                |          |
                               BASE-BASE-BASE
                                   <--->
'''
# Amount of mass in kg
mass = 1.0

# Data structure which contain the coordinates of the masses and mass supports
masses, massSupports = construct_masses_and_supports(length = 1.0)

# Add the masses representted by circles to the plot
radius = 0.2
color  = "#FF33FF"

############################ (2) truss members ################################
trussLength = 1.0
bendingStiffness = 1.0
# The convention used here is that the first entry of both the x and y vectors
# represent the lower node and the second represents the upper node
trussSources = construct_truss_sources(masses[0], masses[1], masses[2], trussLength)

################################# (3) base ####################################
base = ColumnDataSource(
                        data=dict(
                                  x=[masses[0].data['x'][0] - 1.5, masses[0].data['x'][0] + 1.5],
                                  y=[masses[0].data['y'][0] - 1.0, masses[0].data['y'][0] - 1.0]
                                 )
                       )

############################### Create Structure ##############################
structure = Structure(masses, massSupports, trussSources, trussLength, base)

############################## Plot structure #################################
time_plot.line( x='x', y='y', source=structure.massSupports[0], line_width=4)
time_plot.line( x='x', y='y', source=structure.massSupports[1], line_width=4)
time_plot.line( x='x', y='y', source=structure.massSupports[2], line_width=4)

time_plot.circle( x='x',y='y',radius=radius,color=color,source=structure.masses[0] )
time_plot.circle( x='x',y='y',radius=radius,color=color,source=structure.masses[1] )
time_plot.circle( x='x',y='y',radius=radius,color=color,source=structure.masses[2] )

time_plot.line( x='x', y='y', source=structure.trusses[0], line_width=2)
time_plot.line( x='x', y='y', source=structure.trusses[1], line_width=2)
time_plot.line( x='x', y='y', source=structure.trusses[2], line_width=2)
time_plot.line( x='x', y='y', source=structure.trusses[3], line_width=2)
time_plot.line( x='x', y='y', source=structure.trusses[4], line_width=2)
time_plot.line( x='x', y='y', source=structure.trusses[5], line_width=2)

time_plot.line( x='x', y='y', source=structure.base,   line_width=10)
'''
###############################################################################
Construct the system of equations that needs to be solved
###############################################################################
'''
# Initialize the mass, stiffness, and damping matrices respectively
M = np.zeros((3,3))
K = np.zeros((3,3))
C = np.zeros((3,3))

construct_system(M, K, C, mass, bendingStiffness, trussLength)

'''
###############################################################################
Define here the time loop that leads to the solution of the system of equations
in time domain
###############################################################################
'''
# siesmicInput is an array which has a list of time in seconds in its first 
# index and a list of the ampitude in m/s2 in its second index
siesmicInput = ColumnDataSource(data=dict(amplitude=[0],time=[0],color=["33FF33"]))
siesmicInput.data = read_siesmic_input(file='data/preDefinedTwo.txt')

# Plot the siesmic input signal into the siesmic_input_plot
siesmic_input_plot.line( x='time', y='amplitude', color="#33FF33", source=siesmicInput,   line_width=1)
siesmic_input_plot.circle(x='time', y='amplitude', color="color", source=siesmicInput, radius=1)

siesmicInput.data['color'][100] = siesmicInput.data['color'][100]*0 + '#000000'

# the solution data structure consists of a vector which contains the time-doma
# -in displacement of the massesm in addition to the displacement of the base
solution = ColumnDataSource(data=dict(time=[0],amplitude=[0]))
solution = solve_time_domain(M, C, K, siesmicInput)

'''
###############################################################################
Define here the function that solves the eignevalue problem in order to obtain
the modal parametes (here, the eigenfrequencies and the eigenmodes)
###############################################################################
'''
###################### Solve the eigenvalue problem ###########################
# Construct default data sources
eigenvalues = ColumnDataSource(data=dict(x=[1,2,3],y=[0,0,0]))
eigenmodeOne   = ColumnDataSource(data=dict(x=[1,1,1],y=[1,2,3]))
eigenmodeTwo   = ColumnDataSource(data=dict(x=[1,1,1],y=[1,2,3]))
eigenmodeThree = ColumnDataSource(data=dict(x=[1,1,1],y=[1,2,3]))

# Update the default data sources
eigenvalues, eigenmodeOne, eigenmodeTwo, eigenmodeThree = solve_modal_analysis(M, K)

# plot the eigenmode shapes into the modes_plot
colorList = ['#33FF33' , '#FF33FF', '#FFFF33'] # colors represent the three modes

########################## Output the results #################################
modes_plot.line(x='x', y='y', source=eigenmodeOne, line_width=2, color=colorList[0])
modes_plot.line(x='x', y='y', source=eigenmodeTwo, line_width=2, color=colorList[1])
modes_plot.line(x='x', y='y', source=eigenmodeThree, line_width=2, color=colorList[2])

modes_plot.circle(x='x', y='y', source=eigenmodeOne, fill_color="white", size=8)
modes_plot.circle(x='x', y='y', source=eigenmodeTwo, fill_color="white", size=8)
modes_plot.circle(x='x', y='y', source=eigenmodeThree, fill_color="white", size=8)

'''
###############################################################################
Define here the main interactivities which are:
    (1) sliders to modify the amount of masses
    (2) sliders to modify the bending stiffness of the trusses
    (3) time slider to enable the user to trace the time evolution of the masse
        s' displacement
    (4) Play bottun for the time slider to play automatically
    (5) Pause bottun for the time slider to pause from playing
    (6) data collecting box where the user can define the siesmic input data fi
        -le to read from, in addition to a bottun that the user needs to press
        in order for the new defined data file to be read and correspondingly 
        the system to be solved/re-solved
###############################################################################
'''
############################ (1) masses slider ################################
mass_Slider = Slider(
                       title=u" Mass of the individual point mass (kg) ",
                       value=1, start=0, end=10, step=0.1,width=600
                    )
mass_Slider.on_change('value',update_mass)

def update_mass(attr,old,new):
    global mass
    mass = new
    
    construct_system(M, K, C, mass, bendingStiffness, trussLength)
    compute_system()

####################### (2) bending stiffness slider ##########################
bendingStiffness_Slider = Slider(
                                   title=u" Bending stiffness of the individual column () ",
                                   value=0, start=0, end=30, step=0.01,width=600
                                )
bendingStiffness_Slider.on_change('value',update_bendingStiffness)

def update_bendingStiffness(attr,old,new):
    global bendingStiffness
    bendingStiffness = new
    
    construct_system(M, K, C, mass, bendingStiffness, trussLength)
    compute_system()
    
############################# (3) time slider #################################
def update_time(attr,old,new):
    global counter
    timeStep = 0.01 #seconds
    masses[0].data = dict(x=[solution[0,int(new/timeStep)]] , y=masses[0].data['y'])
    masses[1].data = dict(x=[solution[1,int(new/timeStep)]] , y=masses[1].data['y'])
    masses[2].data = dict(x=[solution[2,int(new/timeStep)]] , y=masses[2].data['y'])
    
    counter = int(new/timeStep)
    
time_Slider = Slider(
                       title=u" Time (second) ",
                       value=0, start=0, end=30, step=0.01,width=600
                    )
time_Slider.on_change('value',update_time)


############################# (4) Play button #################################  
def play():
    print('pressed!')
    timeStep = 0.01 #seconds
    period = timeStep*1000
    curdoc().add_periodic_callback(play_system, period)
      
play_button = Button(label="Play", button_type="success")
play_button.on_click(play)

counter = 0
def play_system():
    global counter

    counter += 1
    time_Slider.value = counter*0.01

    displacement = [solution[0,counter], solution[1,counter], solution[2,counter]]

    structure.update_masses( displacement )
    structure.update_massSupprts( displacement )
    structure.update_truss_sources()
    
    #color = siesmicInput.data['color']
    #color[counter] = '#000000'
    #siesmicInput.data['color'] = siesmicInput.data['color']*0 + color

    siesmicInput.data['color'][counter] = siesmicInput.data['color'][counter]*0 + '#000000'

############################ (5) Pause button #################################
pause_button = Button(label="Pause", button_type="success")
pause_button.on_click(pause)

def pause():
    curdoc().remove_periodic_callback(play_system)

############################### (6) data box ##################################
text_input = TextInput(value="default", title="Label:")

def compute_system():
    '''
    Here we need to:
        (1) construct/re-construct the siesmic-signal and its plot
        (2) compute/re-compute the eigenfrequencies and eigenmodes and plot them
        (3) compute/re-compute the time dependent solution of the system
    '''
    global siesmicInput, eigenvalues, eigenmodeOne, eigenmodeTwo, eigenmodeThree, solution
    
    curdoc().remove_periodic_callback(play_system)
    time_Slider.value = 0.0
    
    ################################## (1) ####################################
    #siesmicInput = read_siesmic_input(file=text_input.value)
    
    ################################## (2) ####################################
    eigenvalues, eigenmodeOne, eigenmodeTwo, eigenmodeThree = solve_modal_analysis(M, K)
    
    ################################## (3) ####################################
    solution = solve_time_domain(M, C, K, siesmicInput)
    
enter_data_button = Button(label="Pause", button_type="success")
enter_data_button.on_click(compute_system)

'''
###############################################################################
Construct and show the resulting plot
###############################################################################
'''
curdoc().add_root(
                  row(
                      column(
                             time_plot,
                             siesmic_input_plot
                            ),
                      modes_plot,
                      column(
                             play_button,
                             time_Slider
                            )
                     )
                 )    
# get path of parent directory and only use the name of the Parent Directory 
# for the tab name. Replace underscores '_' and minuses '-' with blanks ' '		
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  