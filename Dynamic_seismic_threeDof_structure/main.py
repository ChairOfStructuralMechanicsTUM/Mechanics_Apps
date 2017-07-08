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
xmin1, xmax1 = -10,10
ymin1, ymax1 = 0,10
signal_plotstructure_plot = figure(
                                      plot_width=400,
                                      plot_height=400,
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
structure_plot.xaxis.axis_label="Maximum Relative Displacement [mm]"

xmin2, xmax2 = -10,10
ymin2, ymax2 = 0,10
signal_plot = figure(
                      plot_width=400,
                      plot_height=400,
                      x_range=[xmin2,xmax2], 
                      y_range=[ymin2,ymax2],
                      tools = '',
                      title = 'Structure',
                    )
signal_plot.title.text_font_size = "25px"
signal_plot.title.align = "center"
signal_plot.grid.visible=False
signal_plot.xaxis.visible=True
signal_plot.yaxis.visible=True
signal_plot.yaxis.axis_label= "Height [m]"
signal_plot.xaxis.axis_label="Maximum Relative Displacement [mm]"

xmin3, xmax3 = -10,10
ymin3, ymax3 = 0,10
max_displacement_plot = figure(
                                  plot_width=400,
                                  plot_height=400,
                                  x_range=[xmin3,xmax3], 
                                  y_range=[ymin3,ymax3],
                                  tools = '',
                                  title = 'Structure',
                              )
max_displacement_plot.title.text_font_size = "25px"
max_displacement_plot.title.align = "center"
max_displacement_plot.grid.visible=False
max_displacement_plot.xaxis.visible=True
max_displacement_plot.yaxis.visible=True
max_displacement_plot.yaxis.axis_label= "Height [m]"
max_displacement_plot.xaxis.axis_label="Maximum Relative Displacement [mm]"

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
# Starting amount of mass in kg
mass = 10000.0

# Data structure which contains the coordinates of the masses and mass supports
masses, massSupports = construct_masses_and_supports(length = 3.0)

# Radius of the circles that represent the masses
radius = 0.5

############################ (2) truss members ################################
trussLength = 3.0 # meters

# Starting amount of bendingStiffness in N*m^2
bendingStiffness = 1000000

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
plot( time_plot, structure, radius, structure_color )

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
                      
'''
###############################################################################
Read and plot the seismic signals
###############################################################################
'''
# There will be three signals to be read
signalOne   = read_seismic_input(file='')
signalTwo   = read_seismic_input(file='')
signalThree = read_seismic_input(file='')

# Plot the signals into signal_plot
signalOne_plot   = signal_plot.line(x='time',y='amplitude',color='color',source=signalOne,line_width=3)
signalTwo_plot   = signal_plot.line(x='time',y='amplitude',color='color',source=signalOne,line_width=3)
signalThree_plot = signal_plot.line(x='time',y='amplitude',color='color',source=signalOne,line_width=3)

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
responseOne_thirdStorey_plot = max_displacement_plot.line(x='time',y='amplitude',source=responseOne_thirdStorey,line_color = "#33FF33")
responseTwo_thirdStorey_plot = max_displacement_plot.line(x='time',y='amplitude',source=responseTwo_thirdStorey,line_color = "#33FF22")
responseThree_thirdStorey_plot = max_displacement_plot.line(x='time',y='amplitude',source=responseThree_thirdStorey,line_color = "#33FF11")

# Create legend for the signal_plot
legend2 = Legend(items=[
    ("Response One  ", [responseOne_thirdStorey_plot  ]),
    ("Response Two  ", [responseTwo_thirdStorey_plot  ]),
    ("Response Three", [responseThree_thirdStorey_plot]),
], location=(0, 0))

signal_plot.add_layout(legend2, 'above')
signal_plot.legend.click_policy="hide"