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
from bokeh.models import Arrow, OpenHead, Button, Slider, Toggle, LabelSet, Legend
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
xmin1, xmax1 = -10,10
ymin1, ymax1 = 0,10
structure_plot = figure(
                                      plot_width=400,
                                      plot_height=600,
                                      x_range=[xmin1,xmax1], 
                                      y_range=[ymin1,ymax1],
                                      
                                      title = 'Structure',
                                  )
structure_plot.title.text_font_size = "25px"
structure_plot.title.align = "center"
structure_plot.grid.visible=False
structure_plot.xaxis.visible=True
structure_plot.yaxis.visible=True
structure_plot.yaxis.axis_label= "Height [m]"
structure_plot.xaxis.axis_label="Relative Displacement [mm]"

xmin2, xmax2 = 0,1800
ymin2, ymax2 = -0.5,0.5
signal_plot = figure(
                      plot_width=1000,
                      plot_height=400,
                      x_range=[xmin2,xmax2], 
                      y_range=[ymin2,ymax2],
                      #tools = '',
                      title = 'Seismic Signals',
                    )
signal_plot.title.text_font_size = "25px"
signal_plot.title.align = "center"
signal_plot.grid.visible=False
signal_plot.xaxis.visible=True
signal_plot.yaxis.visible=True
signal_plot.yaxis.axis_label= "Amplitude [m/s"u"\u00B2]"
signal_plot.xaxis.axis_label="Time [second]"

xmin3, xmax3 = 0,1800
ymin3, ymax3 = -0.5,0.5
max_displacement_plot = figure(
                                  plot_width=1000,
                                  plot_height=400,
                                  x_range=[xmin3,xmax3], 
                                  y_range=[ymin3,ymax3],
                                  #tools = '',
                                  title = 'Structure Response (Third Storey Deflection)',
                              )
max_displacement_plot.title.text_font_size = "25px"
max_displacement_plot.title.align = "center"
max_displacement_plot.grid.visible=False
max_displacement_plot.xaxis.visible=True
max_displacement_plot.yaxis.visible=True
max_displacement_plot.yaxis.axis_label= "Amplitude [mm]"
max_displacement_plot.xaxis.axis_label="Time [second]"

'''
###############################################################################
Construct the structure
###############################################################################
'''
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
structure_color  = '#85929E'

# Starting amount of mass in kg
mass = 10000.0
massRatio = np.array([2.0, 1.5, 1.0])  

# Data structure which contains the coordinates of the masses and mass supports
masses, massSupports = construct_masses_and_supports(length = 3.0)

# Radius of the circles that represent the masses
radius = 0.5

############################ (2) truss members ################################
trussLength = 3.0 # meters

# Starting amount of bendingStiffness in N*m^2
bendingStiffness = 1000000
stiffnessRatio = np.array([3.0, 2.0, 1.0])

trussSources = construct_truss_sources(masses[0], masses[1], masses[2], trussLength)

################################# (3) base ####################################
base =dict(
              x=[masses[0]['x'][0] - trussLength/2, masses[0]['x'][0] + trussLength/2],
              y=[masses[0]['y'][0] - trussLength  , masses[0]['y'][0] - trussLength  ]
          )

############################### Create Structure ##############################
structure = Structure(masses, massSupports, trussSources, trussLength, base)

structure.update_system([0,0,0])

# Construct the mass and stiffness matric, in addition to the lebels to be defined later
construct_system(structure, mass, massRatio, bendingStiffness, stiffnessRatio, trussLength)

############################## Plot structure #################################
plot( structure_plot, structure, radius, structure_color )

# label that indicates the mass 
structure_plot.add_layout(
                      LabelSet(
                                  x='x', y='y',
                                  text='mass',
                                  text_color='black',text_font_size="10pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=structure.massIndicators
                              )
                    )
                      
# Label that indicates the stiffness
structure_plot.add_layout(
                      LabelSet(
                                  x='x', y='y',
                                  text='stiffness',
                                  text_color='black',text_font_size="10pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=structure.stiffnessIndicators
                              )
                    )
                      
'''
###############################################################################
Read and plot the seismic signals
###############################################################################
'''
# There will be three signals to be read
signalOne   = read_seismic_input(file='Dynamic_seismic_threeDof_structure/Force.txt')
signalTwo   = read_seismic_input(file='Dynamic_seismic_threeDof_structure/Force.txt')
signalThree = read_seismic_input(file='Dynamic_seismic_threeDof_structure/Force.txt')

# Plot the signals into signal_plot
signalOne_plot   = signal_plot.line(x='time',y='amplitude',source=signalOne,line_width=1)
signalTwo_plot   = signal_plot.line(x='time',y='amplitude',source=signalOne,line_width=1)
signalThree_plot = signal_plot.line(x='time',y='amplitude',source=signalOne,line_width=1)

# Create legend for the signal_plot
legend2 = Legend(items=[
    ("Signal One  ", [signalOne_plot  ]),
    ("Signal Two  ", [signalTwo_plot  ]),
    ("Signal Three", [signalThree_plot]),
], location=(0, 0))

signal_plot.add_layout(legend2, 'above')
signal_plot.legend.click_policy="hide"

'''
###############################################################################
Solve the structure (in time domain)
###############################################################################
'''
responseOne_amplitudes = solve_time_domain(structure, signalOne)
responseTwo_amplitudes = solve_time_domain(structure, signalTwo)
responseThree_amplitudes = solve_time_domain(structure, signalThree)

responseOne_thirdStorey = ColumnDataSource(data=dict(time=signalOne.data['time'],amplitude=responseOne_amplitudes[2,:]))
responseTwo_thirdStorey = ColumnDataSource(data=dict(time=signalTwo.data['time'],amplitude=responseTwo_amplitudes[2,:]))
responseThree_thirdStorey = ColumnDataSource(data=dict(time=signalThree.data['time'],amplitude=responseThree_amplitudes[2,:]))

# Plot the third floor initial displacement for each signal
responseOne_thirdStorey_plot = max_displacement_plot.line(x='time',y='amplitude',source=responseOne_thirdStorey,line_width=1)
responseTwo_thirdStorey_plot = max_displacement_plot.line(x='time',y='amplitude',source=responseTwo_thirdStorey,line_width=1)
responseThree_thirdStorey_plot = max_displacement_plot.line(x='time',y='amplitude',source=responseThree_thirdStorey,line_width=1)

# Create legend for the signal_plot
legend3 = Legend(items=[
    ("Response One  ", [responseOne_thirdStorey_plot  ]),
    ("Response Two  ", [responseTwo_thirdStorey_plot  ]),
    ("Response Three", [responseThree_thirdStorey_plot]),
], location=(0, 0))

max_displacement_plot.add_layout(legend3, 'above')
max_displacement_plot.legend.click_policy="hide"

'''
###############################################################################
Define interactivities 
###############################################################################
'''
time = 0
dt   = 0.1
periodicCallback = 0
Active = False

def update_structure():
    global time
    
    # Update time
    time += dt
    if time >= time_slider.end:
        time = 0
        time_slider.value = time_slider.start
    else:
        time_slider.value += time_slider.step
        
    if signal_choices.active == 0:
        displacement = responseOne_amplitudes[:,int(time/dt)]*10
    elif signal_choices.active == 1:
        displacement = responseTwo_amplitudes[:,int(time/dt)]*10
    elif signal_choices.active == 2:
        displacement = responseThree_amplitudes[:,int(time/dt)]*10

    structure.update_system(displacement)
    
    
def update_time(attr,old,new):
    global time
    time = new
    
    if signal_choices.active == 0:
        displacement = responseOne_amplitudes[:,int(time/dt)]*10
    elif signal_choices.active == 1:
        displacement = responseTwo_amplitudes[:,int(time/dt)]*10
    elif signal_choices.active == 2:
        displacement = responseThree_amplitudes[:,int(time/dt)]*10

    structure.update_system(displacement)
    #update_structure()
    
time_slider = Slider(
                      title=u" Time [second] ", 
                      value=0, start=0, end=300, step=0.1, width=300
                    )
time_slider.on_change('value',update_time)


signal_choices = RadioGroup(
        labels=["Signal 1", "Signal 2", "Signal 3"], active=0)

def pause():
    global Active
    # When active pause animation
    if Active == True:
        curdoc().remove_periodic_callback(update_structure)
        Active=False
    else:
        pass
        
pause_button = Button(label="Pause", button_type="success")
pause_button.on_click(pause)

def play():
    global Active, periodicCallback
    
    if Active == False:
        curdoc().add_periodic_callback(update_structure, 100)
        Active=True
        periodicCallback = 0
    else:
        pass
    
play_button = Button(label="Play", button_type="success")
play_button.on_click(play)

'''
###############################################################################
Plot everything 
###############################################################################
'''
curdoc().add_root(
                    row(
                        column(
                               structure_plot,
                               time_slider,
                               play_button,
                               pause_button
                              ),
                        column(
                               signal_plot,
                               max_displacement_plot
                              )
                       )
                 )

# get path of parent directory and only use the name of the Parent Directory 
# for the tab name. Replace underscores '_' and minuses '-' with blanks ' '		
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  