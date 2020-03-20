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
from bokeh.models import Arrow, OpenHead, Button, Slider, Toggle, LabelSet, Legend,CustomJS
from bokeh.layouts import column, row, widgetbox
from bokeh.models.widgets import TextInput, RadioGroup, Div, DataTable,TableColumn,DateFormatter
from os.path import dirname, join, split
from Functions import *
from bokeh.models.ranges import Range1d
from bokeh.models.layouts import Spacer
from bokeh.models.ranges import Range
from bokeh.models.renderers import GlyphRenderer
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexDiv, LatexLabel, LatexLabelSet, LatexSlider, LatexLegend

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
structure_plot.axis.axis_label_text_font_style="normal"
structure_plot.yaxis.axis_label_text_font_size= "20px"
structure_plot.yaxis.axis_label= "Height [m]"
structure_plot.xaxis.axis_label_text_font_size= "20px"
structure_plot.xaxis.axis_label="Relative Displacement [mm]"

xmin2, xmax2 = 0,1800
ymin2, ymax2 = -0.5,0.5
signal_plot = figure(
                      plot_width=700,
                      plot_height=500,
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
signal_plot.axis.axis_label_text_font_style="normal"
signal_plot.yaxis.axis_label_text_font_size= "20px"
signal_plot.yaxis.axis_label= "Amplitude [m/s"u"\u00B2]"
signal_plot.xaxis.axis_label_text_font_size= "20px"
signal_plot.xaxis.axis_label="Time [second]"

xmin3, xmax3 = 0,1000
ymin3, ymax3 = -0.5,0.5
max_displacement_plot = figure(
                                  plot_width=720,
                                  plot_height=500,
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
max_displacement_plot.axis.axis_label_text_font_style="normal"
max_displacement_plot.yaxis.axis_label_text_font_size= "20px"
max_displacement_plot.yaxis.axis_label= "Amplitude [mm]"
max_displacement_plot.xaxis.axis_label_text_font_size= "20px"
max_displacement_plot.xaxis.axis_label="Time [second]"

ERSplot = figure(
                      plot_width=800,
                      plot_height=800,
                      x_range=[0,3.0], 
                      y_range=[0,3.0],
                      
                      title = 'Elastic Response Spectrum',
                   )
ERSplot.title.text_font_size = "25px"
ERSplot.title.align = "center"
ERSplot.grid.visible=True
ERSplot.xaxis.visible=True
ERSplot.xaxis.visible=True
ERSplot.axis.axis_label_text_font_style="normal"
ERSplot.xaxis.axis_label_text_font_size= "20px"
ERSplot.xaxis.axis_label= 'Period [second]'
ERSplot.yaxis.visible=True
ERSplot.yaxis.axis_label_text_font_size= "20px"
ERSplot.yaxis.axis_label= "S"u"\u2090 [m/s"u"\u00B2]"
'''
###############################################################################
input the scale value
###############################################################################
'''
initial_scale_value1=1
initial_scale_value2=1
initial_scale_value3=1
initial_scale_value4=1

glob_scale_value1=ColumnDataSource(data=dict(initial_scale_value1=[initial_scale_value1]))
glob_scale_value2=ColumnDataSource(data=dict(initial_scale_value2=[initial_scale_value2]))
glob_scale_value3=ColumnDataSource(data=dict(initial_scale_value3=[initial_scale_value3]))
glob_scale_value4=ColumnDataSource(data=dict(initial_scale_value4=[initial_scale_value4]))


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
mass = 1000.0
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
                      LatexLabelSet(
                                  x='x', y='y',
                                  text='mass',
                                  text_color='black',text_font_size="10pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=structure.massIndicators
                              )
                    )
                      
# Label that indicates the stiffness
structure_plot.add_layout(
                      LatexLabelSet(
                                  x='x', y='y',
                                  text='stiffness',
                                  text_color='black',text_font_size="10pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=structure.stiffnessIndicators
                              )
                    )
                      
color = ["#0065BD","#E37222","#808080","#A2AD00"]
'''
###############################################################################
set the scale value
###############################################################################
'''

'''
###############################################################################
Read and plot the seismic signals
###############################################################################
'''
# There will be Four signals to be read
signalOne   = read_seismic_input(file='Dynamic_seismic_threeDof_structure/Time_domain_signals/San_Ramon_Fire_Station/RSN215_LIVERMOR_A-SRM070.AT2', scale = initial_scale_value1
)
signalTwo   = read_seismic_input(file='Dynamic_seismic_threeDof_structure/Time_domain_signals/Rio_Hondo/RSN8837_14383980_CIRIOHNE1.AT2', scale = initial_scale_value2
)
signalThree = read_seismic_input(file='Dynamic_seismic_threeDof_structure/Time_domain_signals/Bevagna/RSN4346_UBMARCHE.P_A-BEV000.AT2', scale = initial_scale_value3)
signalFour = read_seismic_input(file='Dynamic_seismic_threeDof_structure/Time_domain_signals/Kobe_new/RSN1106_KOBE_KJM000.AT2', scale = initial_scale_value4)
# Calculate the maximum achieved amplitude in all three signals

def change_scaleV1(attr, old, new):
    #[initial_scale_value1]=glob_scale_value1.data["initial_scale_value1"]
    initial_scale_value1=float(new)
    glob_scale_value1.data=dict(initial_scale_value1=[initial_scale_value1])    

initial_scale_value_input1=Slider(title="Scale Value for Signal one", value=initial_scale_value1,start=0,end=10,step=0.5, width=200)
initial_scale_value_input1.on_change('value', change_scaleV1)



def change_scaleV2(attr, old, new):
    #[initial_scale_value2]=glob_scale_value2.data["initial_scale_value2"]
    initial_scale_value2=float(new)
    glob_scale_value2.data=dict(initial_scale_value2=[initial_scale_value2])

initial_scale_value_input2=Slider(title="Scale Value for Signal Two", value=initial_scale_value2,start=0,end=10,step=0.5, width=200)
initial_scale_value_input2.on_change('value',change_scaleV2)

def change_scaleV3(attr, old, new):
    #[initial_scale_value3]=glob_scale_value3.data["initial_scale_value3"]
    initial_scale_value3=float(new)
    glob_scale_value3.data=dict(initial_scale_value3=[initial_scale_value3])

initial_scale_value_input3=Slider(title="Scale Value for Signal Three", value=initial_scale_value3,start=0,end=10,step=0.5, width=200)
initial_scale_value_input3.on_change('value',change_scaleV3)

def change_scaleV4(attr, old, new):
    #[initial_scale_value4]=glob_scale_value4.data["initial_scale_value4"]
    initial_scale_value4=float(new)
    glob_scale_value4.data=dict(initial_scale_value4=[initial_scale_value4])

initial_scale_value_input4=Slider(title="Scale Value for Signal Four", value=initial_scale_value4,start=0,end=2,step=0.1, width=200)
initial_scale_value_input4.on_change('value',change_scaleV4)

print(initial_scale_value1)
maxAmplitude = 0
for element in signalOne.data['amplitude']:
    if abs(element) > maxAmplitude:
        maxAmplitude = abs(element)
        
for element in signalTwo.data['amplitude']:
    if abs(element) > maxAmplitude:
        maxAmplitude = abs(element)
        
for element in signalThree.data['amplitude']:
    if abs(element) > maxAmplitude:
        maxAmplitude = abs(element)

for element in signalFour.data['amplitude']:
    if abs(element) > maxAmplitude:
        maxAmplitude = abs(element)
        
# Calculate the maximum achieved time in all three signals and max time-step
maxTime = 0
maxTimeStep = 0

if maxTime < signalOne.data['time'][-1]:
    maxTime = abs(signalOne.data['time'][-1])
if maxTime < signalTwo.data['time'][-1]:
    maxTime = abs(signalTwo.data['time'][-1])
if maxTime < signalThree.data['time'][-1]:
    maxTime = abs(signalThree.data['time'][-1])
if maxTime < signalFour.data['time'][-1]:
    maxTime = abs(signalFour.data['time'][-1])
    
if maxTimeStep < signalOne.data['time'][1] - signalOne.data['time'][0]:
    maxTimeStep = signalOne.data['time'][1] - signalOne.data['time'][0]
if maxTimeStep < signalTwo.data['time'][1] - signalTwo.data['time'][0]:
    maxTimeStep = signalTwo.data['time'][1] - signalTwo.data['time'][0]
if maxTimeStep < signalThree.data['time'][1] - signalThree.data['time'][0]:
    maxTimeStep = signalThree.data['time'][1] - signalThree.data['time'][0]
if maxTimeStep < signalFour.data['time'][1] - signalFour.data['time'][0]:
    maxTimeStep = signalFour.data['time'][1] - signalFour.data['time'][0]
        
# Modify the plotting ranges of the signal_plot
signal_plot.y_range.start = -maxAmplitude
signal_plot.y_range.end = maxAmplitude #= Range(-maxAmplitude,maxAmplitude)
signal_plot.x_range.start = 0
signal_plot.x_range.end = maxTime/5 #= Range(0,maxTime)

print('maxTime = ',maxTime)
print('maxTimeStep = ',maxTimeStep)

# Plot the signals into signal_plot
signalOne_plot   = signal_plot.line(x='time',y='amplitude',source=signalOne,line_width=1,color=color[0])
signalTwo_plot   = signal_plot.line(x='time',y='amplitude',source=signalTwo,line_width=1,color=color[1])
signalThree_plot = signal_plot.line(x='time',y='amplitude',source=signalThree,line_width=1,color=color[2])
signalFour_plot  = signal_plot.line(x='time',y='amplitude',source=signalFour,line_width=1,color=color[3])
# Create legend for the signal_plot
legend2 = Legend(items=[
    ("Signal One  ", [signalOne_plot  ]),
    ("Signal Two  ", [signalTwo_plot  ]),
    ("Signal Three", [signalThree_plot]),
    ("Signal Four", [signalFour_plot]),
], location=(0, 0))

signal_plot.add_layout(legend2, 'above')
signal_plot.legend.click_policy="hide"

'''
###############################################################################
Reading ERS data
###############################################################################
'''
ERS_dataOne = read_ERS_data(file='Dynamic_seismic_threeDof_structure/Time_domain_signals/San_Ramon_Fire_Station/_SearchResults.csv')
ERS_dataTwo = read_ERS_data(file='Dynamic_seismic_threeDof_structure/Time_domain_signals/Rio_Hondo/_SearchResults.csv')
ERS_dataThree = read_ERS_data(file='Dynamic_seismic_threeDof_structure/Time_domain_signals/Bevagna/_SearchResults.csv')
ERS_dataFour = read_KOKE_ERS_data(file='Dynamic_seismic_threeDof_structure/Time_domain_signals/Kobe_new/_SearchResults.csv')

# Plot the ERS_data into signal_plot
ERS_dataOne_plot   = ERSplot.line(x='period',y='acceleration',source=ERS_dataOne,line_width=1,color=color[0])
ERS_dataTwo_plot   = ERSplot.line(x='period',y='acceleration',source=ERS_dataTwo,line_width=1,color=color[1])
ERS_dataThree_plot = ERSplot.line(x='period',y='acceleration',source=ERS_dataThree,line_width=1,color=color[2])
ERS_dataFour_plot = ERSplot.line(x='period',y='acceleration',source=ERS_dataFour,line_width=1,color=color[3])
# Calculate the maximum achieved amplitude in all three signals
maxAcceleration = 0
for element in ERS_dataOne.data['acceleration']:
    if abs(element) > maxAcceleration:
        maxAcceleration = abs(element)
        
for element in ERS_dataTwo.data['acceleration']:
    if abs(element) > maxAcceleration:
        maxAcceleration = abs(element)
        
for element in ERS_dataThree.data['acceleration']:
    if abs(element) > maxAcceleration:
        maxAcceleration = abs(element)

for element in ERS_dataFour.data['acceleration']:
    if abs(element) > maxAcceleration:
        maxAcceleration = abs(element)
        
maxPeriod = 0
if maxPeriod < ERS_dataOne.data['period'][-1]:
    maxPeriod = abs(ERS_dataOne.data['period'][-1])
if maxPeriod < ERS_dataTwo.data['period'][-1]:
    maxPeriod = abs(ERS_dataTwo.data['period'][-1])
if maxPeriod < ERS_dataTwo.data['period'][-1]:
    maxPeriod = abs(ERS_dataTwo.data['period'][-1])
    
ERSplot.y_range.start = 0
ERSplot.y_range.end = maxAcceleration
ERSplot.x_range.start = 0
ERSplot.x_range.end = maxPeriod

# Create legend for the signal_plot
legend3 = Legend(items=[
    ("ERS Signal One  ", [ERS_dataOne_plot  ]),
    ("ERS Signal Two  ", [ERS_dataTwo_plot  ]),
    ("ERS Signal Three", [ERS_dataThree_plot]),
    ("ERS Signal Four", [ERS_dataFour_plot]),
], location=(0, 0))

ERSplot.add_layout(legend3, 'above')
ERSplot.legend.click_policy="hide"

############################ ERS data information #############################
ERS_dataOne_info = Read_ERS_info(file='Dynamic_seismic_threeDof_structure/Time_domain_signals/San_Ramon_Fire_Station/_SearchResults.csv')
ERS_dataTwo_info = Read_ERS_info(file='Dynamic_seismic_threeDof_structure/Time_domain_signals/Rio_Hondo/_SearchResults.csv')
ERS_dataThree_info = Read_ERS_info(file='Dynamic_seismic_threeDof_structure/Time_domain_signals/Bevagna/_SearchResults.csv')
ERS_dataFour_info = Read_Kobe_ERS_info(file='Dynamic_seismic_threeDof_structure/Time_domain_signals/Kobe_new/_SearchResults.csv')

informationTable = ColumnDataSource(
                                     data=dict(
                                               subject=[ 'Year',
                                                        'Station Name', 'Magnitude',
                                                        'Mechanism', 'Rjb (km)',
                                                        'Rrup (km)'],
                                                signalOne  =ERS_dataOne_info,
                                                signalTwo  =ERS_dataTwo_info,
                                                signalThree=ERS_dataThree_info,
                                                signalFour =ERS_dataFour_info
                                              )
                                    )
columns = [
            TableColumn(field="subject", title="Subject"),
            TableColumn(field="signalOne", title="Signal One"),
            TableColumn(field="signalTwo", title="Signal Two"),
            TableColumn(field="signalThree", title="Signal Three"),
            TableColumn(field="signalFour", title="Signal Four"),
          ]   
data_table = DataTable(source=informationTable, columns=columns, width=900, height=280)
data_table_title = Div(text="""<b>Information about the seismic signals</b> """,width = 600)

'''
###############################################################################
Solve the structure (in time domain)
###############################################################################
'''
responseOne_amplitudes = solve_time_domain(structure, signalOne)
responseTwo_amplitudes = solve_time_domain(structure, signalTwo)
responseThree_amplitudes = solve_time_domain(structure, signalThree)
responseFour_amplitudes = solve_time_domain(structure, signalFour)



# Note: multiplied by 1000 to convert from meter to millimeter
responseOne_thirdStorey = ColumnDataSource(data=dict(time=signalOne.data['time'],amplitude=responseOne_amplitudes[2,:]*1000))
responseTwo_thirdStorey = ColumnDataSource(data=dict(time=signalTwo.data['time'],amplitude=responseTwo_amplitudes[2,:]*1000))
responseThree_thirdStorey = ColumnDataSource(data=dict(time=signalThree.data['time'],amplitude=responseThree_amplitudes[2,:]*1000))
responseFour_thirdStorey = ColumnDataSource(data=dict(time=signalFour.data['time'],amplitude=responseFour_amplitudes[2,:]*1000))
# Plot the third floor initial displacement for each signal
responseOne_thirdStorey_plot = max_displacement_plot.line(x='time',y='amplitude',source=responseOne_thirdStorey,line_width=1,color=color[0])
responseTwo_thirdStorey_plot = max_displacement_plot.line(x='time',y='amplitude',source=responseTwo_thirdStorey,line_width=1,color=color[1])
responseThree_thirdStorey_plot = max_displacement_plot.line(x='time',y='amplitude',source=responseThree_thirdStorey,line_width=1,color=color[2])
responseFour_thirdStorey_plot = max_displacement_plot.line(x='time',y='amplitude',source=responseFour_thirdStorey,line_width=1,color=color[3])
# Calculate the maximum achieved amplitude in all three signals
maxResponseAmplitude = 0
for element in responseOne_thirdStorey.data['amplitude']:
    if abs(element) > maxResponseAmplitude:
        maxResponseAmplitude = abs(element)
        
for element in responseTwo_thirdStorey.data['amplitude']:
    if abs(element) > maxResponseAmplitude:
        maxResponseAmplitude = abs(element)
        
for element in responseThree_thirdStorey.data['amplitude']:
    if abs(element) > maxResponseAmplitude:
        maxResponseAmplitude = abs(element)

for element in responseFour_thirdStorey.data['amplitude']:
    if abs(element) > maxResponseAmplitude:
        maxResponseAmplitude = abs(element)

max_displacement_plot.y_range.start = -maxResponseAmplitude
max_displacement_plot.y_range.end = maxResponseAmplitude #= Range(-maxAmplitude,maxAmplitude)
max_displacement_plot.x_range.start = 0
max_displacement_plot.x_range.end = maxTime/6 #= Range(0,maxTime)

# Create legend for the signal_plot
legend3 = Legend(items=[
    ("Response One  ", [responseOne_thirdStorey_plot  ]),
    ("Response Two  ", [responseTwo_thirdStorey_plot  ]),
    ("Response Three", [responseThree_thirdStorey_plot]),
    ("Response Four ", [responseFour_thirdStorey_plot]),
], location=(0, 0))

max_displacement_plot.add_layout(legend3, 'above')
max_displacement_plot.legend.click_policy="hide"

'''
###############################################################################
Define interactivities 
###############################################################################
'''
time = 0
dt   = maxTimeStep
periodicCallback = 0
Active = False

def update_structure():
    global time
    
    # Update time
    time += maxTimeStep
    if time >= time_slider.end:
        time = 0
        time_slider.value = time_slider.start
    else:
        time_slider.value += time_slider.step
        
    if signal_choices.active == 0:
        displacement = responseOne_amplitudes[:,int(time/maxTimeStep)]*1000
    elif signal_choices.active == 1:
        displacement = responseTwo_amplitudes[:,int(time/maxTimeStep)]*1000
    elif signal_choices.active == 2:
        displacement = responseThree_amplitudes[:,int(time/maxTimeStep)]*1000
    elif signal_choices.active == 3:
        displacement = responseFour_amplitudes[:,int(time/maxTimeStep)]*1000
    structure.update_system(displacement)
    
    
def update_time(attr,old,new):
    global time
    time = new
    
    if signal_choices.active == 0:
        if time < signalOne.data['time'][-1]:
            displacement = responseOne_amplitudes[:,int(time/maxTimeStep)]*1000
        else:
            displacement = responseOne_amplitudes[:,0]*1000
            time = 0
            time_slider.value = time_slider.start
    elif signal_choices.active == 1:
        if time < signalTwo.data['time'][-1]:
            displacement = responseTwo_amplitudes[:,int(time/maxTimeStep)]*1000
        else:
            displacement = responseTwo_amplitudes[:,0]*1000
            time = 0
            time_slider.value = time_slider.start
    elif signal_choices.active == 2:
        if time < signalThree.data['time'][-1]:
            displacement = responseThree_amplitudes[:,int(time/maxTimeStep)]*1000
        else:
            displacement = responseThree_amplitudes[:,0]*1000
            time = 0
            time_slider.value = time_slider.start
    elif signal_choices.active == 3:
        if time < signalFour.data['time'][-1]:
            displacement = responseFour_amplitudes[:,int(time/maxTimeStep)]*1000
        else:
            displacement = responseFour_amplitudes[:,0]*1000
            time = 0
            time_slider.value = time_slider.start
            
    structure.update_system(displacement)
    #update_structure()
    
time_slider = Slider(
                      title=u" Time [second] ", 
                      value=0, start=0, end=maxTime, step=maxTimeStep, width=300
                    )
time_slider.on_change('value',update_time)


signal_choices = RadioGroup(
        labels=["Response One", "Response Two", "Response Three","Response Four"], active=0)

def playPause():
    if playPause_button.label == 'Play':
        play()
    else:
        pause()

glob_callback_id = ColumnDataSource(data = dict(callback_id = [None]))

def pause():
    [callback_id] = glob_callback_id.data['callback_id']
    playPause_button.label = "Play"
    try:
        curdoc().remove_periodic_callback(callback_id) 
    except ValueError:
        print("WARNING: callback_id was already removed - this can happen if stop was pressed after pause, usually no serious problem; if stop was not called this part should be changed")
        # callback_id is not set to None or similar, the object hex-code stays -> no if == None possible -> use try/except
    except:
        print("This error is not covered: ", sys.exc_info()[0])
        raise

def play():
    [callback_id] = glob_callback_id.data['callback_id']
    playPause_button.label = "Pause"
    callback_id=curdoc().add_periodic_callback(update_structure,100)
    glob_callback_id.data = dict(callback_id = [callback_id])

def stop():
    pause()
    global structure
    global time_slider
    if signal_choices.active == 0:
        drawing_displacement = responseOne_amplitudes[:,0]*1000
    elif signal_choices.active == 1:
        drawing_displacement = responseTwo_amplitudes[:,0]*1000
    elif signal_choices.active == 2:
        drawing_displacement = responseThree_amplitudes[:,0]*1000
    elif signal_choices.active == 3:
        drawing_displacement = responseFour_amplitudes[:,0]*1000
    structure.update_system(drawing_displacement)
    time_slider.value = 0

stop_button = Button(label="Stop", button_type="success")
stop_button.on_click(stop)

#def playPause():
    #global Active, periodicCallback
    
    #if Active == False:
        #curdoc().add_periodic_callback(update_structure,100)
        #Active=True
        #periodicCallback = 0
        #playPause_button.label = "Pause"
    #else:
        #curdoc().remove_periodic_callback(update_structure)
        #Active=False
        #playPause_button.label = "Play"
    
playPause_button = Button(label="Play", button_type="success")
playPause_button.on_click(playPause)
'''
###############################################################################
Replot
###############################################################################
'''


def re_plot():
    #initil the plot of seimic Signal
    amplitude   = list()
    time           = list()
    global signalOne
    signalOne.data=dict(amplitude=np.array(amplitude),time=np.array(time))
    global signalTwo
    signalTwo.data=dict(amplitude=np.array(amplitude),time=np.array(time))
    global signalThree
    signalThree.data=dict(amplitude=np.array(amplitude),time=np.array(time))
    global signalFour
    signalFour.data=dict(amplitude=np.array(amplitude),time=np.array(time))
    [initial_scale_value1]=glob_scale_value1.data["initial_scale_value1"]
    [initial_scale_value2]=glob_scale_value2.data["initial_scale_value2"]
    [initial_scale_value3]=glob_scale_value3.data["initial_scale_value3"]
    [initial_scale_value4]=glob_scale_value4.data["initial_scale_value4"]
    signalOne   = read_seismic_input(file='Dynamic_seismic_threeDof_structure/Time_domain_signals/San_Ramon_Fire_Station/RSN215_LIVERMOR_A-SRM070.AT2', scale = initial_scale_value1)
    signalTwo   = read_seismic_input(file='Dynamic_seismic_threeDof_structure/Time_domain_signals/Rio_Hondo/RSN8837_14383980_CIRIOHNE1.AT2', scale = initial_scale_value2)
    signalThree = read_seismic_input(file='Dynamic_seismic_threeDof_structure/Time_domain_signals/Bevagna/RSN4346_UBMARCHE.P_A-BEV000.AT2', scale = initial_scale_value3)
    signalFour  = read_seismic_input(file='Dynamic_seismic_threeDof_structure/Time_domain_signals/Kobe_new/RSN1106_KOBE_KJM000.AT2', scale = initial_scale_value4)
    
    maxAmplitude = 0
    for element in signalOne.data['amplitude']:
        if abs(element) > maxAmplitude:
           maxAmplitude = abs(element)
        
    for element in signalTwo.data['amplitude']:
        if abs(element) > maxAmplitude:
            maxAmplitude = abs(element)
        
    for element in signalThree.data['amplitude']:
        if abs(element) > maxAmplitude:
           maxAmplitude = abs(element)

    for element in signalFour.data['amplitude']:
   
        if abs(element) > maxAmplitude:
           maxAmplitude = abs(element)
        
    # Calculate the maximum achieved time in all three signals and max time-step
    maxTime = 0
    maxTimeStep = 0

    if maxTime < signalOne.data['time'][-1]:
       maxTime = abs(signalOne.data['time'][-1])
    if maxTime < signalTwo.data['time'][-1]:
       maxTime = abs(signalTwo.data['time'][-1])
    if maxTime < signalThree.data['time'][-1]:
       maxTime = abs(signalThree.data['time'][-1])
    if maxTime < signalFour.data['time'][-1]:
       maxTime = abs(signalFour.data['time'][-1])
    
    if maxTimeStep < signalOne.data['time'][1] - signalOne.data['time'][0]:
       maxTimeStep = signalOne.data['time'][1] - signalOne.data['time'][0]
    if maxTimeStep < signalTwo.data['time'][1] - signalTwo.data['time'][0]:
       maxTimeStep = signalTwo.data['time'][1] - signalTwo.data['time'][0]
    if maxTimeStep < signalThree.data['time'][1] - signalThree.data['time'][0]:
       maxTimeStep = signalThree.data['time'][1] - signalThree.data['time'][0]
    if maxTimeStep < signalFour.data['time'][1] - signalFour.data['time'][0]:
       maxTimeStep = signalFour.data['time'][1] - signalFour.data['time'][0]
    global signal_plot    
    # Modify the plotting ranges of the signal_plot
    signal_plot.y_range.start = -maxAmplitude
    signal_plot.y_range.end = maxAmplitude #= Range(-maxAmplitude,maxAmplitude)
    signal_plot.x_range.start = 0
    signal_plot.x_range.end = maxTime/5 #= Range(0,maxTime)
    
    signalOne_plot   =  signal_plot.line(x='time',y='amplitude',source=signalOne,line_width=1,color=color[0])
    signalTwo_plot   =  signal_plot.line(x='time',y='amplitude',source=signalTwo,line_width=1,color=color[1])
    signalThree_plot =  signal_plot.line(x='time',y='amplitude',source=signalThree,line_width=1,color=color[2])
    signalFour_plot  =  signal_plot.line(x='time',y='amplitude',source=signalFour,line_width=1,color=color[3])
    
    amplitude   = list()
    time           = list()
    global responseOne_amplitudes, responseTwo_amplitudes, responseThree_amplitudes, responseFour_amplitudes

    
    responseOne_amplitudes = solve_time_domain(structure, signalOne)
    responseTwo_amplitudes = solve_time_domain(structure, signalTwo)
    responseThree_amplitudes = solve_time_domain(structure, signalThree)
    responseFour_amplitudes = solve_time_domain(structure, signalFour)
    # Note: multiplied by 1000 to convert from meter to millimeter
    
    global responseOne_thirdStorey
    responseOne_thirdStorey.data=dict(amplitude=np.array(amplitude),time=np.array(time))
    global responseTwo_thirdStorey
    responseTwo_thirdStorey.data=dict(amplitude=np.array(amplitude),time=np.array(time))
    global responseThree_thirdStorey
    responseThree_thirdStorey.data=dict(amplitude=np.array(amplitude),time=np.array(time))
    global responseFour_thirdStorey
    responseFour_thirdStorey.data=dict(amplitude=np.array(amplitude),time=np.array(time))
    responseOne_thirdStorey = ColumnDataSource(data=dict(time=signalOne.data['time'],amplitude=responseOne_amplitudes[2,:]*1000))
    responseTwo_thirdStorey = ColumnDataSource(data=dict(time=signalTwo.data['time'],amplitude=responseTwo_amplitudes[2,:]*1000))
    responseThree_thirdStorey = ColumnDataSource(data=dict(time=signalThree.data['time'],amplitude=responseThree_amplitudes[2,:]*1000))
    responseFour_thirdStorey = ColumnDataSource(data=dict(time=signalFour.data['time'],amplitude=responseFour_amplitudes[2,:]*1000))
    # Calculate the maximum achieved amplitude in all three signals
    maxResponseAmplitude = 0
    for element in responseOne_thirdStorey.data['amplitude']:
        if abs(element) > maxResponseAmplitude:
            maxResponseAmplitude = abs(element)
            
    for element in responseTwo_thirdStorey.data['amplitude']:
        if abs(element) > maxResponseAmplitude:
            maxResponseAmplitude = abs(element)
            
    for element in responseThree_thirdStorey.data['amplitude']:
        if abs(element) > maxResponseAmplitude:
            maxResponseAmplitude = abs(element)

    for element in responseFour_thirdStorey.data['amplitude']:
        if abs(element) > maxResponseAmplitude:
            maxResponseAmplitude = abs(element)
    global max_displacement_plot
    global responseOne_thirdStorey_plot
    global responseTwo_thirdStorey_plot
    global responseThree_thirdStorey_plot
    global responseFour_thirdStorey_plot
    responseOne_thirdStorey_plot = max_displacement_plot.line(x='time',y='amplitude',source=responseOne_thirdStorey,line_width=1,color=color[0])
    responseTwo_thirdStorey_plot = max_displacement_plot.line(x='time',y='amplitude',source=responseTwo_thirdStorey,line_width=1,color=color[1])
    responseThree_thirdStorey_plot = max_displacement_plot.line(x='time',y='amplitude',source=responseThree_thirdStorey,line_width=1,color=color[2])
    responseFour_thirdStorey_plot = max_displacement_plot.line(x='time',y='amplitude',source=responseFour_thirdStorey,line_width=1,color=color[3])
    max_displacement_plot.y_range.start = -maxResponseAmplitude
    max_displacement_plot.y_range.end = maxResponseAmplitude #= Range(-maxAmplitude,maxAmplitude)
    max_displacement_plot.x_range.start = 0
    max_displacement_plot.x_range.end = maxTime/6 #= Range(0,maxTime)

    time = 0
    
    dt   = maxTimeStep
    periodicCallback = 0
    Active = False

    def update_structure():
        global time
        
        # Update time
        time += maxTimeStep
        if time >= time_slider.end:
            time = 0
            time_slider.value = time_slider.start
        else:
            time_slider.value += time_slider.step
            
        if signal_choices.active == 0:
            displacement = responseOne_amplitudes[:,int(time/maxTimeStep)]*1000
        elif signal_choices.active == 1:
            displacement = responseTwo_amplitudes[:,int(time/maxTimeStep)]*1000
        elif signal_choices.active == 2:
            displacement = responseThree_amplitudes[:,int(time/maxTimeStep)]*1000
        elif signal_choices.active == 3:
            displacement = responseFour_amplitudes[:,int(time/maxTimeStep)]*1000
        structure.update_system(displacement)
     
        
    def update_time(attr,old,new):
        global time
        time = new
        
        if signal_choices.active == 0:
            if time < signalOne.data['time'][-1]:
                displacement = responseOne_amplitudes[:,int(time/maxTimeStep)]*1000
            else:
                displacement = responseOne_amplitudes[:,0]*1000
                time = 0
                time_slider.value = time_slider.start
        elif signal_choices.active == 1:
            if time < signalTwo.data['time'][-1]:
                displacement = responseTwo_amplitudes[:,int(time/maxTimeStep)]*1000
            else:
                displacement = responseTwo_amplitudes[:,0]*1000
                time = 0
                time_slider.value = time_slider.start
        elif signal_choices.active == 2:
            if time < signalThree.data['time'][-1]:
                displacement = responseThree_amplitudes[:,int(time/maxTimeStep)]*1000
            else:
                displacement = responseThree_amplitudes[:,0]*1000
                time = 0
                time_slider.value = time_slider.start
        elif signal_choices.active == 3:
            if time < signalFour.data['time'][-1]:
                displacement = responseFour_amplitudes[:,int(time/maxTimeStep)]*1000
            else:
                displacement = responseFour_amplitudes[:,0]*1000
                time = 0
                time_slider.value = time_slider.start
                
        structure.update_system(displacement)
    

re_plot_button = Button(label="Refresh", button_type="success")
re_plot_button.on_click(re_plot)


'''
###############################################################################
Plot everything 
###############################################################################
'''
curdoc().add_root(
                    row(
                        column(
                               Spacer(height=80),
                               row(Spacer(width=20),column(signal_choices,
                               structure_plot,
                               time_slider,
                               playPause_button,
                               stop_button,re_plot_button,),)
                               
                              ),
                        
                        column(
                               max_displacement_plot,
                               signal_plot,
                              ),
                        column(
                               row( 
                                  column(
                                         Spacer(height=200),
                                         initial_scale_value_input1,
                                         initial_scale_value_input2,
                                         initial_scale_value_input3,
                                         initial_scale_value_input4,
                                         ),
                                         ERSplot,
                               ),
                               row(Spacer(width=120), column(data_table_title,
                               data_table,),                             
                                     
                       )
                 )
             )
)

# get path of parent directory and only use the name of the Parent Directory 
# for the tab name. Replace underscores '_' and minuses '-' with blanks ' '		
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  