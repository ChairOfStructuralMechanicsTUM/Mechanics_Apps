from __future__ import division
#Importing spring,damper and mass
from SRS_Spring  import SRS_Spring
from SRS_Dashpot import SRS_Dashpot
from SRS_Mass    import SRS_CircularMass
from SRS_Coord   import SRS_Coord
#importing plotting objects from bokeh
from bokeh.plotting import figure
from bokeh.layouts  import column, row, Spacer, gridplot
from bokeh.io       import curdoc
from bokeh.models   import ColumnDataSource
from bokeh.models   import Select,Slider, Button, Div, HoverTool, Range1d, Arrow, NormalHead
from bokeh.models.tickers import FixedTicker
from bokeh.models.widgets import DataTable, TableColumn

from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv, LatexLabelSet #, LatexLabel
from math  import sqrt, exp, pow, pi, sin #, cos, ceil, pi, atan2, sinh, cosh
from numpy import convolve, amax, argmax


# constants
initial_spring_constant_value = 1.
initial_damping_ratio         = 0.1
initial_displacement_value    = 0
force_value = 1.
Force_duration  = 1 ## input parameters for the analytic solution
dt = 0.02

# global variables
glob_callback_id = ColumnDataSource(data = dict(callback_id = [None]))
glob_vars = dict(
        TimePeriodRatio = 1,
        mass_value      = 1,
        Te              = 1,
        W               = 1,
        WD              = 1,
        D               = 1,
        h               = [], #unit impulse response
        FI              = [], #Input force
        final           = [], #final displacement
        t               = 0,
        mass            = [],
        spring          = [],
        damper          = [],
        Active          = False
        )



def Initialise():
    load_vals = ["FI", "h"]
    FI, h     = [glob_vars.get(val) for val in load_vals] # input/
    
    #initial values given
    TimePeriodRatio = 1
    
    #calculating based on initial values
    Te         = Force_duration/TimePeriodRatio   #natural time period
    W          = 2*pi/Te # natural frequency
    mass_value = initial_spring_constant_value /pow(W,2)
    D          = initial_damping_ratio
    WD         = W * sqrt(1-pow(D,2))
    damping_coeffcient = D*2*sqrt(initial_spring_constant_value*mass_value)
    
    #making mass, spring and damper elements
    mass   = SRS_CircularMass(mass_value,0,10,2,2)
    spring = SRS_Spring((-2,.75),(-2,8),7,initial_spring_constant_value)
    damper = SRS_Dashpot((2,.75),(2,8),damping_coeffcient)
    
    t=0
    #initially rectangular impulse is applied    
    for i in range(0,1000,1): # making rectangular function 
        T= i*dt
        if (T<=1):
            FI.append(1) 
        else:
            FI.append(0)        
        x=(1/(float(mass.Getmass())*WD))*exp(-D*W*T)*sin(WD*T) 
        h.append(x) #unit impulse response
    glob_vars["final"] = dt*convolve(FI,h,mode='full') #convolution of input force and unit impulse response
    glob_vars["TimePeriodRatio"] = TimePeriodRatio #      /output
    glob_vars["mass_value"]      = mass_value #      /output
    glob_vars["Te"] = Te #      /output
    glob_vars["WD"] = WD #      /output
    glob_vars["W"]  = W  #      /output
    glob_vars["D"]  = D  #      /output
    glob_vars["t"]  = t  #      /output
    glob_vars["mass"]   = mass   #      /output
    glob_vars["spring"] = spring #      /output
    glob_vars["damper"] = damper #      /output
    
Initialise()

Bottom_Line  = ColumnDataSource(data = dict(x=[-2,2],y=[8,8]))
Linking_Line = ColumnDataSource(data = dict(x=[0,0],y=[8,10]))
displacement = ColumnDataSource(data = dict(t=[0],s=[initial_displacement_value]))
arrow_line   = ColumnDataSource(data = dict(x1=[0],y1=[15],x2=[0],y2=[12]))
omega_max    = ColumnDataSource(data = dict(time=[0],omega=[0]))
t_max        = ColumnDataSource(data = dict(time=[0],tmax=[0]))
Force_input  = ColumnDataSource(data = dict(beta=[0],phi=[0]))

#Force_input is only for visualisation, FI is used for calculation
Force_input.stream(dict(beta=[0],phi=[1]))
Force_input.stream(dict(beta=[1],phi=[1]))
Force_input.stream(dict(beta=[1.0001],phi=[0]))
Force_input.stream(dict(beta=[2],phi=[0]))

#parameter variable for parameter table
parameters = ColumnDataSource(data = dict(names1=[u'\u03c9',"Te"],names2=["D",u'\u03c9*'],values1=[round(glob_vars["W"],4),round(glob_vars["Te"],4)],values2=[round(glob_vars["D"],4),round(glob_vars["WD"],4)]))

def evolve():
    load_vals = ["FI", "final", "h", "WD", "D", "W", "t"]
    FI, final, h, WD, D, W, t = [glob_vars.get(val) for val in load_vals] # input/
    TimePeriodRatio = glob_vars["TimePeriodRatio"] # input/
    mass = glob_vars["mass"] # input/
    
    #########
    #k = spring.getSpringConstant
    maximum   = 0
    maximumat = 0
    if(t==0):
        final*=0 # reset the list 
        for i in range(0,1000,1): # finding unit response function and store
            T= i*dt
            x=(1/(float(mass.Getmass())*WD))*exp(-D*W*T)*sin(WD*T) 
            h[i] = x
        final = dt*convolve(FI,h,mode='full')
    
    maximum   = amax(final)
    maximumat = dt*argmax(final)

    omega_max.stream(dict(time=[TimePeriodRatio],omega=[maximum]))
    t_max.stream(dict(time=[TimePeriodRatio],tmax=[maximumat]))
    
    time = int(t/dt)
    try:
        move_system(-final[time])
        displacement.stream(dict(t=[t],s=[final[time]]))
    except IndexError:
        play_pause() # pause the simulation
        play_pause_button.disabled = True # disable play button to avoid the error in the next step
        print("--- WARNING: auto stop due to index time being out of bounds ---")
    t+=dt
    glob_vars["t"]     = t     #      /output
    glob_vars["h"]     = h     #      /output
    glob_vars["final"] = final #      /output

title_box = Div(text="""<h2 style="text-align:center;">Shock response spectra </h2>""",width=1000)

# sdof drawing
fig = figure(title="", tools="", x_range=(-7,7), y_range=(0,20),width=270,height=225)
fig.title.text_font_size="20pt"
fig.axis.visible = False
fig.grid.visible = False
fig.outline_line_color = None
fig.line(x=[-2,2],y=[.75,.75],color="black",line_width=3)
fig.multi_line(xs=[[-2.75,-2],[-1.75,-1.0],[-0.75,0],[.25,1],[1.25,2]],
    ys=[[0,0.75],[0,0.75],[0,0.75],[0,0.75],[0,0.75]],
    color="black",
    line_width=3)
fig.line(x='x',y='y',source=Bottom_Line,color="black",line_width=3)
fig.line(x='x',y='y',source=Linking_Line,color="black",line_width=3)
fig.toolbar.logo = None
glob_vars["spring"].plot(fig,width=2)
glob_vars["damper"].plot(fig,width=2)
glob_vars["mass"].plot(fig)
arrow = fig.add_layout(Arrow(end=NormalHead(fill_color="red"), line_color="red", line_width=2,
    x_start='x1', y_start='y1', x_end='x2', y_end='y2', source=arrow_line))

# time plot
hover = HoverTool(tooltips=[("time","@t s"), ("displacement","@s m")])
Displacement = figure(title="", y_range=(2,-2), x_range=Range1d(bounds=(0,1000), start=0, end=20), height=550, \
    toolbar_location="right", tools=[hover,"ywheel_zoom,xwheel_pan,pan,reset"]) #ywheel_zoom,xwheel_pan,reset,
Displacement.line(x='t',y='s',source=displacement,color="#e37222",line_width=2,legend="Total Displacement",muted_color="#e37222",muted_alpha=0.2)
Displacement.axis.major_label_text_font_size="12pt"
Displacement.axis.axis_label_text_font_style="normal"
Displacement.axis.axis_label_text_font_size="14pt"
Displacement.xaxis.axis_label="Time [s]"
Displacement.yaxis.axis_label="Displacement [u/(F/k)]"
Displacement.legend.location="top_right"
Displacement.legend.click_policy="mute"
Displacement.toolbar.logo = None


#maximum displacement against time of impulse to time period ratio plot
Dis_max = figure(title="", tools="", x_range=(0,3.0), y_range=(0,4), width=600, height=600)
Dis_max.circle(x='time', y='omega', source=omega_max, color="#a2ad00")
D_max_Label_source   = ColumnDataSource(data=dict(x=[-0.45,1.7], y=[2.5, -0.4], names=[ "\dfrac{U_{max}}{\dfrac{F}{K}}","\dfrac{T_0}{T_e}"]))
D_max_label = LatexLabelSet(x='x', y='y', text='names', source=D_max_Label_source, text_color = 'black', level='glyph', x_offset= 0, y_offset=0)
Dis_max.add_layout(D_max_label)
Dis_max.toolbar.logo = None

#time at which maximum displacement occurs against duration of impulse ratio plot
T_max = figure(title="", tools="", x_range=(0,3.0), y_range=(0,5), width=600, height=600)
T_max.circle(x='time', y='tmax', source=t_max, color="#a2ad00") 
T_max_Label_source   = ColumnDataSource(data=dict(x=[-0.45,1.7], y=[2.5, -0.4], names=["\dfrac{T_{max}}{T_0}", "T_{max}"]))
T_max_label = LatexLabelSet(x='x', y='y', text='names', source=T_max_Label_source, text_color = 'black', level='glyph', x_offset= 0, y_offset=0)
T_max.add_layout(T_max_label)
T_max.toolbar.logo = None

#plotting input force
InputForce = figure(title="", tools="", x_range=(0,3.0), y_range=(0,2), width=300, height=150)
InputForce.line(x='beta', y='phi', source=Force_input, color="#a2ad00")
InputForce.xaxis.axis_label="Time(s)"
InputForce.yaxis.axis_label="Force(N)"
InputForce.yaxis.ticker = FixedTicker(ticks=[0,90,180])
InputForce.toolbar.logo = None

def move_system(disp): # for moving the spring damper mass image according to the displacement of mass
    load_obj = ["mass", "spring", "damper"]
    mass, spring, damper =  [glob_vars.get(val) for val in load_obj] # input/
    mass.moveTo((0,10+disp))
    spring.draw(SRS_Coord(-2,.75),SRS_Coord(-2,8+disp))
    damper.draw(SRS_Coord(2,.75),SRS_Coord(2,8+disp))
    Bottom_Line.data=dict(x=[-2,2],y=[8+disp, 8+disp])
    Linking_Line.data=dict(x=[0,0],y=[8+disp, 10+disp])
    if force_value > 0:
        arrow_line.data=dict(x1=[0],x2=[0],y1=[15+disp],y2=[12+disp])
    else:
        arrow_line.data=dict(x1=[0],x2=[0],y1=[35+disp],y2=[32+disp])


## Create slider to choose damping coefficient
def change_damping_coefficient(attr,old,new):
    glob_vars["damper"].changeDamperCoeff(float(new*2*sqrt(initial_spring_constant_value*glob_vars["mass_value"])))
    updateParameters()
damping_coefficient_input = Slider(title="Damping coefficient [Ns/m]", value=initial_damping_ratio, callback_policy="mouseup", start=0.0, end=1, step=0.05,width=600)
damping_coefficient_input.on_change('value',change_damping_coefficient)

## Create slider to choose the frequency ratio
def change_frequency_ratio(attr,old,new):
    if (not glob_vars["Active"]):
        glob_vars["TimePeriodRatio"] = new #      /output
        updateParameters()
frequency_ratio_input = Slider(title="Impulse duration to natural period ratio", value=glob_vars["TimePeriodRatio"], start=0.1, end=3.0, step=0.1,width=600)
frequency_ratio_input.on_change('value',change_frequency_ratio)

def play_pause():
    [callback_id] = glob_callback_id.data["callback_id"]
    if play_pause_button.label == "Play":
        callback_id = curdoc().add_periodic_callback(evolve,dt*1000)
        play_pause_button.label = "Pause" # change label
        Force_select.disabled = True # disable selection during simulation run
        damping_coefficient_input.disabled = True  # disable slider during simulation run
        frequency_ratio_input.disabled = True # disable slider during simulation run
    elif play_pause_button.label == "Pause":
        curdoc().remove_periodic_callback(callback_id)
        play_pause_button.label = "Play" # change label
    glob_callback_id.data = dict(callback_id = [callback_id])

def reset(): # resets values to initial cofiguration
    play_pause_button.disabled         = False # enable play button in case of auto pause (index error)
    Force_select.disabled              = False # enable selection after reset
    damping_coefficient_input.disabled = False # enable slider after reset
    frequency_ratio_input.disabled     = False # enable slider after reset
    if play_pause_button.label == "Pause":
        play_pause()
    glob_vars["t"]=0 #      /output
    displacement.data=dict(t=[0],s=[initial_displacement_value])
    drawing_displacement = -initial_displacement_value * glob_vars["spring"].getSpringConstant
    move_system(drawing_displacement)
    if force_value > 0:
        arrow_line.data=dict(x1=[0],x2=[0],y1=[15+drawing_displacement],y2=[12+drawing_displacement])
    else:
        arrow_line.data=dict(x1=[0],x2=[0],y1=[35+drawing_displacement],y2=[32+drawing_displacement])
    updateParameters()

def reset_OmegaMax_plot():
    omega_max.data=dict(time=[0],omega=[0])
    updateParameters()

def reset_Tmax_plot():
    t_max.data=dict(time=[0],tmax=[0])
    updateParameters()

reset_button_p_af = Button(label="Reset", button_type="success", width=50)
reset_button_p_af.on_click(reset_OmegaMax_plot)
reset_button_p_pa = Button(label="Reset", button_type="success", width=50)
reset_button_p_pa.on_click(reset_Tmax_plot)

def updateParameters():
    load_vals    = ["FI", "final", "h"]
    FI, final, h = [glob_vars.get(val) for val in load_vals] # input/
    mass   = glob_vars["mass"]   # input/output
    damper = glob_vars["damper"] # input/
    
    Te = Force_duration/glob_vars["TimePeriodRatio"]
    W  = 2*pi/Te
    mass_value = initial_spring_constant_value /pow(W,2)
    mass.changeMass(mass_value)
    D  = (float(damper.getDampingCoefficient))/(2*sqrt(initial_spring_constant_value*mass_value))
    WD = W * sqrt(1-pow(D,2))  
 
    final *= 0
    for i in range(0,1000,1): # making rectangular function 
        T= i*0.02
        x=(1/(mass.Getmass()*WD))*exp(-D*W*T)*sin(WD*T) 
        h[i] = x
    glob_vars["final"] = convolve(FI,h,mode='full') #      /output
    glob_vars["h"] = h #      /output
    parameters.data = dict(names1=[u'\u03c9',"Te"],names2=["D",u'\u03c9*'],values1=[round(W,4),round(Te,4)],values2=[round(D,4),round(WD,4)])
    glob_vars["mass_value"] = mass_value #      /output
    glob_vars["Te"] = Te #      /output
    glob_vars["WD"] = WD #      /output
    glob_vars["W"]  = W  #      /output
    glob_vars["D"]  = D  #      /output

play_pause_button = Button(label="Play", button_type="success",width=100)
play_pause_button.on_click(play_pause)
reset_button = Button(label="Reset", button_type="success", width=100)
reset_button.on_click(reset)

def ChangeForce(forcetype):
    load_vals = ["FI", "final"]
    FI, final = [glob_vars.get(val) for val in load_vals] # input/
    if forcetype == "Triangular":
        Force_input.data=dict(beta=[0],phi=[0])
        Force_input.stream(dict(beta=[0],phi=[0]))
        Force_input.stream(dict(beta=[1],phi=[1]))
        Force_input.stream(dict(beta=[1.0001],phi=[0]))
        Force_input.stream(dict(beta=[2],phi=[0]))
        final *= 0
        FI *= 0
        for i in range(0,1000,1): # making triangular function 
            T= i*0.02
            if (T<=1):
                FI.append(T) 
            else:
                FI.append(0)
    elif forcetype == "Rectangular":
        Force_input.data=dict(beta=[0],phi=[0])
        Force_input.stream(dict(beta=[0],phi=[1]))
        Force_input.stream(dict(beta=[1],phi=[1]))
        Force_input.stream(dict(beta=[1.0001],phi=[0]))
        Force_input.stream(dict(beta=[2],phi=[0]))
        final *= 0
        FI *= 0
        for i in range(0,1000,1): # making rectangular function 
            T= i*0.02
            if (T<=1):
                FI.append(1) 
            else:
                FI.append(0)
    else:
        Force_input.data=dict(beta=[0],phi=[0])
        for i in range(0,100,1):
            Force_input.stream(dict(beta=[0.01*i],phi=[sin(0.01*i*pi)]))
        final *= 0
        FI *= 0
        for i in range(0,1000,1): # making sinusoidal functions
            T= i*0.02
            if (T<=1):
                FI.append(sin(T*pi)) 
            else:
                FI.append(0)
    glob_vars["final"] = final #      /output
    glob_vars["FI"]    = FI    #      /output

def ForceSelection(attr,old,new):   
    ChangeForce(new)
    
Force_select = Select(title="Force:", value="Rectangular",
    options=["Rectangular", "Triangular", "Sinusoidal"])
Force_select.on_change('value',ForceSelection)

# add parameter output
columns = [
    TableColumn(field="names1", title="Parameter"),
    TableColumn(field="values1", title="Value"),
    TableColumn(title=""),
    TableColumn(field="names2", title="Parameter"),
    TableColumn(field="values2", title="Value")
]
parameter_table = DataTable(source=parameters, columns=columns, reorderable=False, sortable=False, selectable=False, index_position=None, width=300, height=100)

# add app description
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)

## Send to window
hspace = 20
curdoc().add_root(column(description,\
    row(column(row(column(row(column(fig,column(play_pause_button,Spacer(width = 10),\
    column(Spacer(width = 10),reset_button))),column(Force_select,InputForce,parameter_table)),\
    Spacer(height=10),Displacement)),Spacer(height=hspace)),Spacer(width=30),\
    column(damping_coefficient_input,frequency_ratio_input,Spacer(height=hspace),\
    row(gridplot([Dis_max,Spacer(height=3 *hspace),T_max],ncols=1,plot_width=480,plot_height=420,merge_tools=True,toolbar_location=""),\
    column(Spacer(height=160),reset_button_p_af,Spacer(height=370),reset_button_p_pa)))\
    ),))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  
# get path of parent directory and only use the name of the Parent Directory for the tab name. 
# Replace underscores '_' and minuses '-' with blanks ' '