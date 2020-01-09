'''
###############################################################################
Imports
###############################################################################
'''
import numpy as np
from bokeh.plotting import figure
from bokeh.io import curdoc
from S3S_Functions import S3S_Mode, S3S_Structure, S3S_SeismicParameters
import S3S_Functions as fc
from bokeh.models import Button, Toggle, LabelSet
from bokeh.layouts import column, row
from bokeh.models.widgets import TextInput, RadioGroup, Div, DataTable, TableColumn
from os.path import dirname, join, split
from bokeh.models.layouts import Spacer

from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv

'''
###############################################################################
Create the plotting domain 
###############################################################################
'''
xmin, xmax = -10,10
ymin, ymax = 0,10
time_plot  = figure(
                      plot_width=400,
                      plot_height=400,
                      x_range=[xmin,xmax], 
                      y_range=[ymin,ymax],
                      
                      title = 'Structure',
                   )
time_plot.title.text_font_size = "25px"
time_plot.title.align          = "center"
time_plot.grid.visible         = False
time_plot.xaxis.visible        = True
time_plot.yaxis.visible        = True
time_plot.toolbar.logo         = None
time_plot.yaxis.axis_label     = "Height [m]"
time_plot.xaxis.axis_label     = "Maximum Relative Displacement [mm]"

mode_one = figure(
                      plot_width  = 300,
                      plot_height = 400,
                      x_range     = [xmin/2,xmax/2], 
                      y_range     = [ymin,ymax],
                      tools       = '',
                      title       = 'First Mode',
                   )
mode_one.title.text_font_size = "25px"
mode_one.title.align          = "center"
mode_one.grid.visible         = False
mode_one.xaxis.visible        = True
mode_one.yaxis.visible        = True
mode_one.toolbar.logo         = None
mode_one.yaxis.axis_label     = "Height [m]"
mode_one.xaxis.axis_label     = "Normalized Displacement"

mode_two = figure(
                      plot_width  = 300,
                      plot_height = 400,
                      x_range     = [xmin/2,xmax/2], 
                      y_range     = [ymin,ymax],  
                      tools       = '',
                      title       = 'Second Mode',
                   )
mode_two.title.text_font_size = "25px"
mode_two.title.align          = "center"
mode_two.grid.visible         = False
mode_two.xaxis.visible        = True
mode_two.yaxis.visible        = True
mode_two.toolbar.logo         = None
mode_two.yaxis.axis_label     = "Height [m]"
mode_two.xaxis.axis_label     = "Normalized Displacement"

mode_three = figure(
                      plot_width  = 300,
                      plot_height = 400,
                      x_range     = [xmin/2,xmax/2], 
                      y_range     = [ymin,ymax],
                      tools       = '',
                      title       = 'Third Mode',
                   )
mode_three.title.text_font_size = "25px"
mode_three.title.align          = "center"
mode_three.grid.visible         = False
mode_three.xaxis.visible        = True
mode_three.yaxis.visible        = True
mode_three.toolbar.logo         = None
mode_three.yaxis.axis_label     = "Height [m]"
mode_three.xaxis.axis_label     = "Normalized Displacement"

ERSplot = figure(
                      plot_width  = 400,
                      plot_height = 400,
                      x_range     = [0,3.0], 
                      y_range     = [0,3.0],
                      
                      title       = 'Elastic Response Spectrum',
                   )
ERSplot.title.text_font_size = "25px"
ERSplot.title.align          = "center"
ERSplot.grid.visible         = True
ERSplot.xaxis.visible        = True
ERSplot.xaxis.visible        = True
ERSplot.toolbar.logo         = None
ERSplot.xaxis.axis_label     = 'Period [second]'
ERSplot.yaxis.visible        = True
ERSplot.yaxis.axis_label     = "S"u"\u2090 [m/s"u"\u00B2]"

siesmic_input_plot = figure(
                      plot_width  = 800,
                      plot_height = 200,
                      x_range     = [0.0,2000], 
                      y_range     = [-1.0,1.0],
                      tools       = '',
                      title       = 'Siesmic Input Signal'
                   )
siesmic_input_plot.title.text_font_size = "25px"
siesmic_input_plot.title.align          = "center"
siesmic_input_plot.grid.visible         = True
siesmic_input_plot.xaxis.visible        = True
siesmic_input_plot.yaxis.visible        = True
siesmic_input_plot.xaxis.axis_label     = 'Time [second]'
siesmic_input_plot.yaxis.axis_label     = 'Acceleration [meter"u"\u00B2/second]'

Active = True

'''
###############################################################################
Define the objects to be plotted within the plotting domain
    (1) masses
    (2) truss members
    (3) base
These three elements will then form the structure which is an object that holds
all of the information
###############################################################################
'''
###################### Structure general properties ###########################
massRatio       = np.array([2.0, 1.5, 1.0])  
stiffnessRatio  = np.array([3.0, 2.0, 1.0])
structure_color = '#85929E'

################################ (1) masses ###################################
'''
                                 trussLength
                                <---------->
                                ====Mass3===
                                |          |
                                |          |
                                ====Mass2===
                                |          |
                                |          |
                                ====Mass1===   ^
                                |          |   | trussLength
                                |          |   |
                               BASE-BASE-BASE  v
                                   <--->
'''
# Starting amount of mass in kg
mass = 10000.0

# Data structure which contains the coordinates of the masses and mass supports
masses, massSupports = fc.construct_masses_and_supports(length = 3.0)

# Radius of the circles that represent the masses
radius = 0.5

############################ (2) truss members ################################
trussLength = 3.0 # meters

# Starting amount of bendingStiffness in N*m^2
bendingStiffness = 1000000

trussSources = fc.construct_truss_sources(masses[0], masses[1], masses[2], trussLength)

################################# (3) base ####################################
base =dict(
              x=[masses[0]['x'][0] - trussLength/2, masses[0]['x'][0] + trussLength/2],
              y=[masses[0]['y'][0] - trussLength  , masses[0]['y'][0] - trussLength  ]
          )

############################### Create Structure ##############################
structure = S3S_Structure(masses, massSupports, trussSources, trussLength, base)

structure.update_system([0,0,0])

# Construct the mass and stiffness matric, in addition to the lebels to be defined later
fc.construct_system(structure, mass, massRatio, bendingStiffness, stiffnessRatio, trussLength)

############################## Plot structure #################################
fc.plot( time_plot, structure, radius, structure_color )

# label that indicates the mass 
time_plot.add_layout(
                      LabelSet(
                                  x='x', y='y',
                                  text='mass',
                                  text_color='black',text_font_size="10pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=structure.massIndicators
                              )
                    )
                      
# Label that indicates the stiffness
time_plot.add_layout(
                      LabelSet(
                                  x='x', y='y',
                                  text='stiffness',
                                  text_color='black',text_font_size="10pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=structure.stiffnessIndicators
                              )
                    )

#'''
################################################################################
#Define here the time loop that leads to the solution of the system of equations
#in time domain (not needed right now!)
################################################################################
#'''
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
    modes.append( S3S_Mode(i, masses, massSupports, trussSources, trussLength, base, frequency=0, modeShape=np.zeros(3)) )

# Get the modal parameters
eigenvalues, eigenvectors = fc.solve_modal_analysis(structure)

# update the modes with the new values
counter = 0
for mode in modes:
    fc.construct_system(mode, mass, massRatio, bendingStiffness, stiffnessRatio, trussLength)
    mode.frequency = np.sqrt(eigenvalues[counter].real)
    mode.modeShape = eigenvectors[:,counter].real
    mode.normalize_mode_shape()
    mode.update_system( mode.modeShape ) # displacement represented by the mode shape itself
    mode.modify_frequency_text()

    counter += 1

########################## Output the results #################################
mode_colors = ['#A2AD00','#E37222','#64A0C8']

fc.plot( mode_one  , modes[2], radius, mode_colors[2])
fc.plot( mode_two  , modes[1], radius, mode_colors[1])
fc.plot( mode_three, modes[0], radius, mode_colors[0])
'''
###############################################################################
Construct the Elastic Response Spectrum
###############################################################################
'''
# Construct the siesmic parametes for the building
# INITIALIZE WITH DEFAULT VALUES
siesmicParameters = S3S_SeismicParameters(a=0.4,gamma=1.0,S=1.0,eta=1.0,beta=2.5,undergroundParamter = 'A-R')
#GetMaximumDisplacement(modes,siesmicParameters)

# To construct the ERS plot data source
fc.update_ERS_plot_data( siesmicParameters )

# plot the line drawn by the ERS data source
ERSplot.line(x='x',y='y',source=siesmicParameters.ERSdata,color='black')

# Allocate each mode in the ERS plot
counter = 0
for mode in modes:
    mode.modify_location_in_ERS(siesmicParameters)
    maxes = mode.get_maximum_displacement(siesmicParameters) # maxes will be used just to let the function run
    ERSplot.line(x='x',y='y',source=mode.locationInERS,color=mode_colors[counter])
    counter+=1

ERS_plot_text = Div(text="""<b>Note: This plot is designed for systems with damping ratio of 5%</b> """)

'''
###############################################################################
Define here the main interactivities which are:
    (1) Solve button
    (2) Mass input
    (3) Stiffness input
    (4) Choices possible to modify ERS and the corresponding "Re-calculate ERS plot"
    (6) Choose which configuration of the structure whether it's deformed or 
        undeformed to be plotted
    (7) Table that summerizes everything about the problem and the obtained sol
        -ion
###############################################################################
'''
###################################### (1) ####################################
def solve_system():
    
    if int(mass_input.value) < 1000 or int(mass_input.value) > 1e10:
        mass_input.value = "Mass is either too small or too big, adjust it!"
    elif int(stiffness_input.value) < 1e3 or int(stiffness_input.value) > 1e9:
        stiffness_input.value = "Stiffness is either too small or too big, adjust it!"
    else:
        fc.construct_system(structure, int(mass_input.value), massRatio, int(stiffness_input.value), stiffnessRatio, trussLength)
    # Re-solve the eigenvalue problem
    eigenvalues, eigenvectors = fc.solve_modal_analysis(structure)

    # update the modes with the new values
    counter = 0
    for mode in modes: 
        # Re-construct the mode matrices (mass and stiffness matrices)
        fc.construct_system(mode, int(mass_input.value), massRatio, int(stiffness_input.value), stiffnessRatio, trussLength)
        
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
        
        S3S_maxes = mode.get_maximum_displacement(siesmicParameters) # S3S_maxes will be used just to let the function run
        
        counter += 1
    
    siesmicParameters.update_data_table(modes)
    # Show the updated deformed configuration whenever the solve system button is pushed
    if ( def_config_button.active ):
        show_def_config(True)
    else:
        pass
    
solve_system_button = Button(label="Solve System", button_type="success")
solve_system_button.on_click(solve_system)

##################################### (2) #####################################
mass_input = TextInput(value="10000", title="Mass [kg]")

##################################### (3) #####################################
stiffness_input = TextInput(value="10000000", title="Stiffness [N*m"u"\u00B2]")

##################################### (4) #####################################
Erdbebenzonen_text = Div(text="""<b>Earthquake Zones</b>""")
Erdbebenzonen_choices = RadioGroup(
        labels=["Zone 1", "Zone 2", "Zone 3"], active=0)
Bedeutungsbeiwert_text = Div(text="""<b>Importance Coefficient</b>""")
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
    siesmicParameters.determine_periods_and_S()
    
    # Plot the updated Elastic Response Spectrum
    fc.update_ERS_plot_data( siesmicParameters )
    
    for mode in modes:
        mode.modify_location_in_ERS(siesmicParameters)
    
calculate_ERS_button = Button(label="Re-calculate Elastic Response Spectrum", button_type="success")
calculate_ERS_button.on_click(calculate_ERS)

#################################### (5) ######################################
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

##################################### (6) #####################################
columns = [
            TableColumn(field="subject", title="Subject"),
            TableColumn(field="modeOne", title="Mode One"),
            TableColumn(field="modeTwo", title="Mode Two"),
            TableColumn(field="modeThree", title="Mode Three"),
          ]   
data_table = DataTable(source=siesmicParameters.informationTable, columns=columns, width=600, height=350)
data_table_text = Div(text="""<b>Input Data and Results of the Modal Analysis</b> """,width = 600)

##################################### (7) #####################################
columns = [
            TableColumn(field="storey", title="Storey"),
            TableColumn(field="maxDisp", title="Maximum Displacement [mm]"),
          ]   
max_disp_data_table = DataTable(source=structure.maximumDisplacement, columns=columns, width=400, height=150)
max_disp_data_table_text = Div(text="""<b>Maximum Displacement Achieved by the Structure</b> """,width = 600)

'''
###############################################################################
Construct and show the resulting plot
###############################################################################
'''       
# add app description
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)

curdoc().add_root(
                    column(
                            description,
                            row(
                                column(
                                        row(
                                            time_plot, Spacer(width=25),
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
                                       ERSplot, 
                                       ERS_plot_text, 
                                       calculate_ERS_button,
                                       data_table_text,
                                       data_table, 
                                       max_disp_data_table_text,
                                       max_disp_data_table
                                      )
                               )
                          )
                 )
# get path of parent directory and only use the name of the Parent Directory 
# for the tab name. Replace underscores '_' and minuses '-' with blanks ' '		
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  