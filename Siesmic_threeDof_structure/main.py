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
from bokeh.models import Arrow, OpenHead, Button, Slider, Toggle, LabelSet
from bokeh.layouts import column, row, widgetbox
from bokeh.models.widgets import TextInput, RadioGroup, Div, DataTable,TableColumn,DateFormatter
from os.path import dirname, join, split
from Functions import *
from bokeh.models.ranges import Range1d
from bokeh.models.layouts import Spacer

'''
###############################################################################
Create the plotting domain 
###############################################################################
'''
xmin, xmax = -10,10
ymin, ymax = 0,10
time_plot = figure(
                      plot_width=400,
                      plot_height=400,
                      x_range=[xmin,xmax], 
                      y_range=[ymin,ymax],
                      
                      title = 'Structure',
                  )
time_plot.title.text_font_size = "25px"
time_plot.title.align = "center"
time_plot.grid.visible=False
time_plot.xaxis.visible=True
time_plot.yaxis.visible=True
time_plot.yaxis.axis_label= "Height (m)"
time_plot.xaxis.axis_label="Maximum Relative Displacement (mm)"

mode_one = figure(
                      plot_width=200,
                      plot_height=400,
                      x_range=[xmin/2,xmax/2], 
                      y_range=[ymin,ymax],
                      
                      title = 'First Mode',
                   )
mode_one.title.text_font_size = "25px"
mode_one.title.align = "center"
mode_one.grid.visible=False
mode_one.xaxis.visible=False
mode_one.yaxis.visible=True
mode_one.yaxis.axis_label= "Height (m)"

mode_two = figure(
                      plot_width=200,
                      plot_height=400,
                      x_range=[xmin/2,xmax/2], 
                      y_range=[ymin,ymax],
                     
                      title = 'Second Mode',
                   )
mode_two.title.text_font_size = "25px"
mode_two.title.align = "center"
mode_two.grid.visible=False
mode_two.xaxis.visible=False
mode_two.yaxis.visible=True
mode_two.yaxis.axis_label= "Height (m)"

mode_three = figure(
                      plot_width=200,
                      plot_height=400,
                      x_range=[xmin/2,xmax/2], 
                      y_range=[ymin,ymax],
                      
                      title = 'Third Mode',
                   )
mode_three.title.text_font_size = "25px"
mode_three.title.align = "center"
mode_three.grid.visible=False
mode_three.xaxis.visible=False
mode_three.yaxis.visible=True
mode_three.yaxis.axis_label= "Height (m)"

ERSplot = figure(
                      plot_width=400,
                      plot_height=400,
                      x_range=[0,3.0], 
                      y_range=[0,3.0],
                      
                      title = 'Elastic Response Spectrum',
                   )
ERSplot.title.text_font_size = "25px"
ERSplot.title.align = "center"
ERSplot.grid.visible=True
ERSplot.xaxis.visible=True
ERSplot.xaxis.visible=True
ERSplot.xaxis.axis_label= 'Period ( second )'
ERSplot.yaxis.visible=True
ERSplot.yaxis.axis_label= 'S'+'\u2090'+' ( m/s'+'\u00B2'+' )'

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
    (1) masses
    (2) truss members
    (3) base
###############################################################################
'''
###################### Structure general properties ###########################
massRatio = np.array([2.0, 1.5, 1.0])  
stiffnessRatio = np.array([3.0, 2.0, 1.0])
structure_color  = '#85929E'

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
# Starting amount of mass in kg
mass = 10000.0

# Data structure which contains the coordinates of the masses and mass supports
masses, massSupports = construct_masses_and_supports(length = 3.0)

# Add the masses representted by circles to the plot
radius = 0.5

############################ (2) truss members ################################
trussLength = 3.0

# Starting amount of bendingStiffness in N*m^2
bendingStiffness = 10000

trussSources = construct_truss_sources(masses[0], masses[1], masses[2], trussLength)

################################# (3) base ####################################
base =dict(
              x=[masses[0]['x'][0] - trussLength/2, masses[0]['x'][0] + trussLength/2],
              y=[masses[0]['y'][0] - trussLength  , masses[0]['y'][0] - trussLength  ]
          )

############################### Create Structure ##############################
structure = Structure(masses, massSupports, trussSources, trussLength, base)
#structure.update_force_indicator_location()
#structure.update_force_indicator_value([0,0,0]) # initial state of the structure has zero forces

############################## Plot structure #################################
plot( time_plot, structure, radius, structure_color )

# label that indicates the mass 
time_plot.add_layout(
                      LabelSet(
                                  x='x', y='y',
                                  text='mass',
                                  text_color='black',text_font_size="5pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=structure.massIndicators
                              )
                    )
                      
# Label that indicates the stiffness
time_plot.add_layout(
                      LabelSet(
                                  x='x', y='y',
                                  text='stiffness',
                                  text_color='black',text_font_size="5pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=structure.stiffnessIndicators
                              )
                    )
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
in time domain (not needed right now!)
###############################################################################
'''
#timeStep = 0.01 #seconds
#
## siesmicInput is an array which has a list of time in seconds in its first 
## index and a list of the ampitude in m/s2 in its second index
#siesmicInput = ColumnDataSource(data=dict(amplitude=[0],time=[0],color=["33FF33"]))
#siesmicInput.data = read_siesmic_input(file='data/preDefinedTwo.txt')
#
## Plot the siesmic input signal into the siesmic_input_plot
#siesmic_input_plot.line( x='time', y='amplitude', color="#33FF33", source=siesmicInput,   line_width=1)
#siesmic_input_plot.circle(x='time', y='amplitude', color="color", source=siesmicInput, radius=0.01)
#
## Modify the y-range of the signal plot
#maxValue = max(abs(i) for i in siesmicInput.data['amplitude'])
#
#siesmic_input_plot.y_range = Range1d(-maxValue, maxValue)
#siesmic_input_plot.x_range = Range1d(0, siesmicInput.data['time'][-1])
#
#siesmicInput.data['color'][100] = siesmicInput.data['color'][100]*0 + '#000000'
#
## the solution data structure consists of a vector which contains the time-doma
## -in displacement of the massesm in addition to the displacement of the base
#solution = ColumnDataSource(data=dict(time=[0],amplitude=[0]))
#solution = solve_time_domain(structure, siesmicInput)

'''
###############################################################################
Define here the function that solves the eignevalue problem in order to obtain
the modal parametes (here, the eigenfrequencies and the eigenmodes)
###############################################################################
'''
###################### Solve the eigenvalue problem ###########################
# Construct the modes
modes = list()
for i in range(0,3):
    modes.append( Mode(i, masses, massSupports, trussSources, trussLength, base, frequency=0, modeShape=np.zeros(3)) )

# Get the modal parameters
eigenvalues, eigenvectors = solve_modal_analysis(structure)

# update the modes with the new values
counter = 0
for mode in modes:
    construct_system(mode, mass, massRatio, bendingStiffness, stiffnessRatio, trussLength)
    mode.frequency = np.sqrt(eigenvalues[counter].real)
    mode.modeShape = eigenvectors[:,counter].real
    mode.normalize_mode_shape()
    mode.update_system( mode.modeShape ) # displacement represented by the mode shape itself
    mode.modify_frequency_text()

    counter += 1

########################## Output the results #################################
mode_colors = ['#0000FF','#00FF00','#D4AC0D']

plot( mode_one  , modes[2], radius, mode_colors[0])
plot( mode_two  , modes[1], radius, mode_colors[1])
plot( mode_three, modes[0], radius, mode_colors[2])
'''
###############################################################################
Construct the Elastic Response Spectrum
###############################################################################
'''
# Construct the siesmic parametes for the building
# INITIALIZE WITH DEFAULT VALUES
siesmicParameters = SiesmicParameters(a=0.4,gamma=1.0,S=1.0,eta=1.0,beta=2.5,undergroundParamter = 'A-R')
#GetMaximumDisplacement(modes,siesmicParameters)

update_ERS_plot_data( siesmicParameters )

ERSplot.line(x='x',y='y',source=siesmicParameters.ERSdata)

counter = 0
for mode in modes:
    mode.modify_location_in_ERS(siesmicParameters)
    ERSplot.line(x='x',y='y',source=mode.locationInERS,color=mode_colors[counter])
    counter+=1

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
################################ Solve System #################################
def solve_system():
    
    if int(mass_input.value) < 1000 or int(mass_input.value) > 1e10:
        mass_input.value = "Mass is either too small or too big, adjust it!"
    elif int(stiffness_input.value) < 1e3 or int(stiffness_input.value) > 1e9:
        stiffness_input.value = "Stiffness is either too small or too big, adjust it!"
    else:
        construct_system(structure, int(mass_input.value), massRatio, int(stiffness_input.value), stiffnessRatio, trussLength)
    # Re-solve the eigenvalue problem
    eigenvalues, eigenvectors = solve_modal_analysis(structure)

    # update the modes with the new values
    counter = 0
    for mode in modes: 
        # Re-construct the mode matrices (mass and stiffness matrices)
        construct_system(mode, int(mass_input.value), massRatio, int(stiffness_input.value), stiffnessRatio, trussLength)
        
        # Update the natural frequency and mode shape
        mode.frequency = np.sqrt(eigenvalues[counter].real)
        mode.modeShape = eigenvectors[:,counter].real

        # Normalize the mode shape so that the product modeShape*MassMatrix*modeShape = 1
        mode.normalize_mode_shape()
        
        # Update thee plot of the mode shapes
        mode.update_system( mode.normalized_mode_withMax_one() )
        
        # Update the text shows the freuency below the mode plot
        mode.modify_frequency_text()

        # Update the location of the mode shapes in the ERS diagram
        mode.modify_location_in_ERS(siesmicParameters)
        
        counter += 1
    
    siesmicParameters.update_data_table(modes)
    # Show the updated deformed configuration whenever the solve system button is pushed
    if ( def_config_button.active ):
        show_def_config(True)
    else:
        pass
    
solve_system_button = Button(label="Solve System", button_type="success")
solve_system_button.on_click(solve_system)

############################### (6) data box ##################################
mass_input = TextInput(value="10000", title="Mass (kg)")
stiffness_input = TextInput(value="10000", title="Stiffness(N*m"+"\u00B2"+")")

##################### (7) Choices possible to modify ERS ######################
Erdbebenzonen_text = Div(text="""<b>Earthquake Zones</b>""")
Erdbebenzonen_choices = RadioGroup(
        labels=["Zone 0", "Zone 1", "Zone 2", "Zone 3"], active=1)
Bedeutungsbeiwert_text = Div(text="""<b>Bedeutungsbeiwert</b>""")
Bedeutungsbeiwert_choices = RadioGroup(
        labels=["Residential Building", "School or Residential Complexes", "Hospital"], active=0)
untergrundParamter_text = Div(text="""<b>Underground Parameter</b>""")
untergrundParamter_choices = RadioGroup(
        labels=["A-R", "B-R", "C-R", "B-T", "C-T", "C-S"], active=0)

def calculate_ERS():
    # re-assign "Erdbebenzonen" value
    a = 0
    value1 = Erdbebenzonen_choices.active
    if value1 == 0:
        a = 0.0
    if value1 == 1:
        a = 0.4
    elif value1 == 2:
        a = 0.6
    elif value1 == 3:
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
    siesmicParameters.determine_periods_and_S
    
    # Plot the updated Elastic Response Spectrum
    update_ERS_plot_data( siesmicParameters )
    
    for mode in modes:
        mode.modify_location_in_ERS(siesmicParameters)
    
calculate_ERS_button = Button(label="Re-calculate Elastic Response Spectrum", button_type="success")
calculate_ERS_button.on_click(calculate_ERS)

#################### (8) Choose which configuration to show ###################
def_undef_choices_text = Div(text="""<b>Choose which configuration to show</b> """)

def show_def_config(active):
    
    if active == True:
        undef_config_button.active = False
        maxes = np.zeros((3,3))
        counter = 0
        for mode in modes:
            maxes[:,counter] = mode.get_maximum_displacement(siesmicParameters)
            counter += 1
            
        maximumDisp = np.sqrt( maxes[:,0]**2 + maxes[:,1]**2 + maxes[:,2]**2 ) * 1000 # to convert to mm
        structure.update_system( maximumDisp )
        structure.massLocations[:,1] = maximumDisp
        #plot( time_plot, structure, radius, color)
        
#        # Calculate forces
#        force1 = (12*bendingStiffness*stiffnessRatio[0] / trussLength**3) * structure.masses[0].data['x'][0]
#        force2 = (12*bendingStiffness*stiffnessRatio[1] / trussLength**3) * (structure.masses[1].data['x'][0] - structure.masses[0].data['x'][0])
#        force3 = (12*bendingStiffness*stiffnessRatio[2] / trussLength**3) * (structure.masses[2].data['x'][0] - structure.masses[1].data['x'][0])
#        structure.update_force_indicator_value( [int(force1),int(force2),int(force3)] )
    else:
        pass
    
def show_undef_config(active):
    if active == True:
        def_config_button.active = False
        structure.update_system( np.zeros(3) )
        structure.update_force_indicator_location()
        
    else:
        pass

def_config_button = Toggle(label="Deformed Configuration", button_type="success",width=25)
def_config_button.on_click(show_def_config)

undef_config_button = Toggle(label="Undeformed Configuration", button_type="success",width=25)
undef_config_button.on_click(show_undef_config)

columns = [
            TableColumn(field="subject", title="Subject"),
            TableColumn(field="modeOne", title="Mode One"),
            TableColumn(field="modeTwo", title="Mode Two"),
            TableColumn(field="modeThree", title="Mode Three"),
          ]   
data_table = DataTable(source=siesmicParameters.informationTable, columns=columns, width=600, height=800)
'''
###############################################################################
Construct and show the resulting plot
###############################################################################
'''       
# add app description
description_filename = join(dirname(__file__), "description.html")
description = Div(text=open(description_filename).read(), render_as_text=False, width=1200)

curdoc().add_root(
                    column(
                            description,
                            row(
                                column(
                                        row(
                                            time_plot, 
                                            column(
                                                   def_undef_choices_text, 
                                                   row(
                                                       undef_config_button,
                                                       Spacer(width=180), 
                                                       def_config_button
                                                      ),
                                                   mass_input,
                                                   stiffness_input,
                                                   solve_system_button
                                                  )
                                           ),
                                        row(
                                            column(mode_one,modes[2].frequency_text,modes[2].multiplier_text),
                                            column(mode_two,modes[1].frequency_text,modes[1].multiplier_text),
                                            column(mode_three,modes[0].frequency_text,modes[0].multiplier_text)
                                           )
                                      ),
                                column(
                                       Erdbebenzonen_text,Erdbebenzonen_choices,
                                       Bedeutungsbeiwert_text,Bedeutungsbeiwert_choices,
                                       untergrundParamter_text,untergrundParamter_choices
                                      ),
                                column(
                                       ERSplot, calculate_ERS_button,data_table
                                      )
                               )
                          )
                 )
# get path of parent directory and only use the name of the Parent Directory 
# for the tab name. Replace underscores '_' and minuses '-' with blanks ' '		
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  