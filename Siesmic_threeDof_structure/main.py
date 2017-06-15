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
from bokeh.layouts import column, row, widgetbox
from bokeh.models.widgets import TextInput, RadioGroup, Div
from os.path import dirname, join, split
from Functions import *
from bokeh.models.ranges import Range1d
from bokeh.models.layouts import Spacer


'''
###############################################################################
Create the plotting domain 
###############################################################################
'''
xmin, xmax = -2.5,2.5
ymin, ymax = 0,10
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
time_plot.xaxis.visible=True
time_plot.yaxis.visible=False

mode_one = figure(
                      plot_width=200,
                      plot_height=400,
                      x_range=[xmin,xmax], 
                      y_range=[ymin,ymax],
                      
                      title = '',
                   )
mode_one.title.text_font_size = "25px"
mode_one.title.align = "center"
mode_one.grid.visible=False
mode_one.xaxis.visible=False
mode_one.yaxis.visible=False

mode_two = figure(
                      plot_width=200,
                      plot_height=400,
                      x_range=[xmin,xmax], 
                      y_range=[ymin,ymax],
                     
                      title = '',
                   )
mode_two.title.text_font_size = "25px"
mode_two.title.align = "center"
mode_two.grid.visible=False
mode_two.xaxis.visible=False
mode_two.yaxis.visible=False

mode_three = figure(
                      plot_width=200,
                      plot_height=400,
                      x_range=[xmin,xmax], 
                      y_range=[ymin,ymax],
                      
                      title = '',
                   )
mode_three.title.text_font_size = "25px"
mode_three.title.align = "center"
mode_three.grid.visible=False
mode_three.xaxis.visible=False
mode_three.yaxis.visible=False

ERSplot = figure(
                      plot_width=400,
                      plot_height=400,
                      x_range=[0,0.15], 
                      y_range=[0,0.5],
                      
                      title = 'Elastic Response Spectrum',
                   )
ERSplot.title.text_font_size = "25px"
ERSplot.title.align = "center"
ERSplot.grid.visible=True
ERSplot.xaxis.visible=True
ERSplot.yaxis.visible=True

siesmic_input_plot = figure(
                      plot_width=800,
                      plot_height=200,
                      x_range=[0.0,2000], 
                      y_range=[-1.0,1.0],
                      tools = '',
                      title = 'Siesmic Input Signal'
                   )
siesmic_input_plot.title.text_font_size = "25px"
siesmic_input_plot.title.align = "center"
siesmic_input_plot.grid.visible=True
siesmic_input_plot.xaxis.visible=True
siesmic_input_plot.yaxis.visible=True
siesmic_input_plot.xaxis.axis_label = 'Time (second)'
siesmic_input_plot.yaxis.axis_label = 'Acceleration (meter^2/second)'

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
mass = 6000.0

# Mass ratios
# 1st floor has 3x, 2nd floor has 2x, and 3rd floor has 1x of a constant mass
massRatio = np.array([2.0, 1.5, 1.0])  
stiffnessRatio = np.array([3.0, 2.0, 1.0])

# Data structure which contain the coordinates of the masses and mass supports
masses, massSupports = construct_masses_and_supports(length = 3.0)

# Add the masses representted by circles to the plot
radius = 0.5
color  = "#FF33FF"

############################ (2) truss members ################################
trussLength = 3.0
bendingStiffness = 89.6e6
# The convention used here is that the first entry of both the x and y vectors
# represent the lower node and the second represents the upper node
trussSources = construct_truss_sources(masses[0], masses[1], masses[2], trussLength)

################################# (3) base ####################################
base =dict(
              x=[masses[0]['x'][0] - trussLength/2, masses[0]['x'][0] + trussLength/2],
              y=[masses[0]['y'][0] - trussLength  , masses[0]['y'][0] - trussLength  ]
          )


############################### Create Structure ##############################
structure = Structure(masses, massSupports, trussSources, trussLength, base)

############################## Plot structure #################################
plot( time_plot, structure, radius, color)

'''
###############################################################################
Construct the system of equations that needs to be solved
###############################################################################
'''
# Initialize the mass, stiffness, and damping matrices respectively
construct_system(structure, mass, massRatio, bendingStiffness, stiffnessRatio, trussLength)

'''
###############################################################################
Define here the time loop that leads to the solution of the system of equations
in time domain
###############################################################################
'''
timeStep = 0.01 #seconds

# siesmicInput is an array which has a list of time in seconds in its first 
# index and a list of the ampitude in m/s2 in its second index
siesmicInput = ColumnDataSource(data=dict(amplitude=[0],time=[0],color=["33FF33"]))
siesmicInput.data = read_siesmic_input(file='data/preDefinedTwo.txt')

# Plot the siesmic input signal into the siesmic_input_plot
siesmic_input_plot.line( x='time', y='amplitude', color="#33FF33", source=siesmicInput,   line_width=1)
siesmic_input_plot.circle(x='time', y='amplitude', color="color", source=siesmicInput, radius=0.01)

# Modify the y-range of the signal plot
maxValue = max(abs(i) for i in siesmicInput.data['amplitude'])

siesmic_input_plot.y_range = Range1d(-maxValue, maxValue)
siesmic_input_plot.x_range = Range1d(0, siesmicInput.data['time'][-1])

siesmicInput.data['color'][100] = siesmicInput.data['color'][100]*0 + '#000000'

# the solution data structure consists of a vector which contains the time-doma
# -in displacement of the massesm in addition to the displacement of the base
solution = ColumnDataSource(data=dict(time=[0],amplitude=[0]))
solution = solve_time_domain(structure, siesmicInput)

'''
###############################################################################
Define here the function that solves the eignevalue problem in order to obtain
the modal parametes (here, the eigenfrequencies and the eigenmodes)
###############################################################################
'''
###################### Solve the eigenvalue problem ###########################
# Construct default data sources
modes = list()
for i in range(0,3):
    modes.append( ModeShape(masses, massSupports, trussSources, trussLength, base, frequency=0, modeShape=np.zeros(3)) )

# Get the modal parameters
eigenvalues, eigenvectors = solve_modal_analysis(structure)

# update the modes with the new values
counter = 0
for mode in modes:
    construct_system(mode, mass, massRatio, bendingStiffness, stiffnessRatio, trussLength)
    mode.update_system( eigenvectors[:,counter].real )
    mode.frequency = np.sqrt(eigenvalues[counter].real)
    mode.modeShape = eigenvectors[:,counter].real

    counter += 1
    

    
# plot the eigenmode shapes into the modes_plot
colorList = ['#33FF33' , '#FF33FF', '#FFFF33'] # colors represent the three modes

# Construct the siesmic parametes for the building
# INITIALIZE WITH DEFAULT VALUES
siesmicParameters = SiesmicParameters(a=0.4,gamma=1.0,S=1.0,eta=1.0,beta=2.5,undergroundParamter = 'A-R')
GetMaximumDisplacement(modes,siesmicParameters)

########################## Output the results #################################
plot( mode_one  , modes[0], radius, color)
plot( mode_two  , modes[1], radius, color)
plot( mode_three, modes[2], radius, color)
'''
###############################################################################
Construc the Elastic Response Spectrum
###############################################################################
'''
plot_ERS(ERSplot, siesmicParameters )

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
def update_mass(attr,old,new):
    construct_system(structure, new, massRatio, bendingStiffness, stiffnessRatio, trussLength)
    
mass_Slider = Slider(
                       title=u" Mass of the individual point mass (kg) ",
                       value=6000, start=5000, end=10000, step=100,width=600
                    )
mass_Slider.on_change('value',update_mass)

####################### (2) bending stiffness slider ##########################
def update_bendingStiffness(attr,old,new):
    construct_system(structure, mass, massRatio, new, stiffnessRatio, trussLength)
    
bendingStiffness_Slider = Slider(
                                   title=u" Bending stiffness of the individual column () ",
                                   value=89e6, start=80e6, end=100e6, step=1e6,width=600
                                )
bendingStiffness_Slider.on_change('value',update_bendingStiffness)
    
############################# (3) time slider #################################
def update_time(attr,old,new):
    global counter
    
    displacement = [solution[0,counter], solution[1,counter], solution[2,counter]]

#    structure.update_masses( displacement )
#    structure.update_massSupprts( displacement )
#    structure.update_truss_sources()
    
    counter = int(new/timeStep)
    
time_Slider = Slider(
                       title=u" Time (second) ",
                       value=0, start=0, end=30, step=0.01,width=600
                    )
time_Slider.on_change('value',update_time)


############################# (4) Play button #################################  
def play():
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

#    structure.update_masses( displacement )
#    structure.update_massSupprts( displacement )
#    structure.update_truss_sources()
    
    print('value = ',radio_group.active)
    #color = siesmicInput.data['color']
    #color[counter] = '#000000'
    #siesmicInput.data['color'] = siesmicInput.data['color']*0 + color

    siesmicInput.data['color'][counter] = siesmicInput.data['color'][counter]*0 + '#000000'

############################ (5) Pause button #################################
def pause():
    curdoc().remove_periodic_callback(play_system)
    
pause_button = Button(label="Pause", button_type="success")
pause_button.on_click(pause)

################################ Solve System #################################
def solve_system():
    eigenvalues, eigenvectors = solve_modal_analysis(structure)
    print('eigenvectors = ',eigenvectors)
    # update the modes with the new values
    counter = 0
    for mode in modes:
        construct_system(mode, mass, massRatio, bendingStiffness, stiffnessRatio, trussLength)
        mode.update_system( eigenvectors[:,counter].real )
        mode.frequency = np.sqrt(eigenvalues[counter].real)
        mode.modeShape = eigenvectors[:,counter].real
    
        counter += 1
    
solve_system_button = Button(label="Solve System", button_type="success")
solve_system_button.on_click(solve_system)

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
    eigenvalues, eigenmodeOne, eigenmodeTwo, eigenmodeThree = solve_modal_analysis(structure)
    
    ################################## (3) ####################################
    solution = solve_time_domain(structure, siesmicInput)
    
enter_data_button = Button(label="Pause", button_type="success")
enter_data_button.on_click(compute_system)

Erdbebenzonen_text = Div(text="""<b>Erdbebenzonen</b>""")
Erdbebenzonen_choices = RadioGroup(
        labels=["Zone 0", "Zone 1", "Zone 2", "Zone 3"], active=0)
Bedeutungsbeiwert_text = Div(text="""<b>Bedeutungsbeiwert</b>""")
Bedeutungsbeiwert_choices = RadioGroup(
        labels=["Residential Building", "School or Residential Complexe", "Hospital"], active=0)
untergrundParamter_text = Div(text="""<b>Untergrundparamter</b>""")
untergrundParamter_choices = RadioGroup(
        labels=["A-R", "B-R", "C-R", "B-T", "C-T", "C-S"], active=0)

def_undef_choices_text = Div(text="""<b>Choose which configuration to show</b>""")


def show_undef_config():
    maxes = np.zeros((3,3))
    counter = 0
    for mode in modes:
        maxes[:,counter] = mode.get_maximum_displacement(siesmicParameters)
        counter += 1
        
    maximumDisp = np.sqrt( maxes[:,0]**2 + maxes[:,1]**2 + maxes[:,2]**2 )
    structure.update_system( maximumDisp )
    structure.massLocations[:,1] = maximumDisp
    plot( time_plot, structure, radius, color)
    
def show_def_config():
    structure.update_system( np.zeros(3) )
    plot( time_plot, structure, radius, color)

undef_config_button = Button(label="Undeformed_Configuration", button_type="success",width=25)
undef_config_button.on_click(show_undef_config)

def_config_button = Button(label="Deformed_Configuration", button_type="success",width=25)
def_config_button.on_click(show_def_config)

def calculate_ERS():
    # re-assign "Erdbebenzonen" value
    a = 0
    value1 = Erdbebenzonen_choices.active
    if value1 == 0:
        a = 0.4
    elif value1 == 1:
        a = 0.6
    elif value1 == 2:
        a = 0.8
    
    # re-assign "Bedeutungsbeiwert"
    gamma = 0
    value2 = Bedeutungsbeiwert_choices.active
    if value2 == 0:
        gamma = 1.0
    elif value2 == 1:
        gamma = 1.2
    elif value2 == 2:
        gamma = 1.4
    
    # re-assign "untergrundParamter"
    value3 = untergrundParamter_choices.active
    undergroundParameter = 0
    if value3 == 0:
        undergroundParameter = "A-R"
    elif value3 == 1:
        undergroundParameter = "B-R"
    elif value3 == 2:
        undergroundParameter = "C-R"
    elif value3 == 3:
        undergroundParameter = "B-T"
    elif value3 == 4:
        undergroundParameter = "C-T"
    elif value3 == 5:
        undergroundParameter = "C-S"
        
    # modify the object of SiesmicParameters with the update values
    siesmicParameters.a = a
    siesmicParameters.gamma = gamma
    siesmicParameters.undergroundParamter = undergroundParameter
    
    # Plot the updated Elastic Response Spectrum
    plot_ERS(ERSplot, siesmicParameters)
    
calculate_ERS_button = Button(label="Re-calculate Elastic Response Spectrum", button_type="success")
calculate_ERS_button.on_click(calculate_ERS)
'''
###############################################################################
Construct and show the resulting plot
###############################################################################
'''
curdoc().add_root(
                  row(
                      column(
                             row(
                                   column(time_plot, def_undef_choices_text, row(undef_config_button, Spacer(width=180), def_config_button)),
                                   mode_one,
                                   mode_two,
                                   mode_three,
                                ),
                             Spacer(height=60),
                             siesmic_input_plot
                            ),
                      column(
                             play_button,
                             pause_button,
                             Spacer(height=60),
                             time_Slider,
                             bendingStiffness_Slider,
                             mass_Slider,
                             row(column(
                                         Erdbebenzonen_text,Erdbebenzonen_choices,
                                         Bedeutungsbeiwert_text,Bedeutungsbeiwert_choices,
                                         untergrundParamter_text,untergrundParamter_choices),
                                 column(ERSplot, calculate_ERS_button, solve_system_button)
                                )
                            )
                     )
                 )    
# get path of parent directory and only use the name of the Parent Directory 
# for the tab name. Replace underscores '_' and minuses '-' with blanks ' '		
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  