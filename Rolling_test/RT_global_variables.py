from __future__ import division # float division only, like in python 3
from bokeh.models import ColumnDataSource
from bokeh.models import Select, Button, Slider
from bokeh.models.widgets import RadioGroup
from math import sin, cos, radians
import numpy as np

# constants
g             = 9.81
maxR          = 4.0
alpha_max     = 25.0
rampLength    = 50
rampAddLength = 5  # excess length for better visualization
max_samples   = 100
buf           = 1e-10 # buffer size for stopping criterion
# create variables
alpha         = radians(20)
t             = 0
# variables created to avoid repeated calculations
# (speeds up calculations)
SIN           = sin(alpha)
COS           = cos(alpha)


###############################################################################
###               coordinates of the triangle (for reference)               ###
###############################################################################
# ramplength L is constant
# (TX0,TY0), alpha and L are given
# (TX1,TY1) and (TX2,TY2) are calculated from this
# aswell as the center of the objects in the creation functions

# (.,TY2) stays constant during the whole simulation
# (TX2,.), (TX1,TY1) can change due to a new alpha value

#    (TX1,TY1)
#        .
#        .   .
#        .       .
#        .           .   L
#        .               .
#        .                   .
#        .                       .
#        .                      .    .
#        .                     .  alpha  .
#        ....................................
#    (TX2,TY2)                           (TX0,TY0)

TX0 = 0
TY0 = 0

TX1 = TX0 - COS*rampLength
TX2 = TX1

TY1 = TY0 + SIN*rampLength
TY2 = TY0

###############################################################################
###                    global variables                    ###
###############################################################################

# displacement, distance traveled
t_end             = [0.0,0.0,0.0]
fig0_samples      = []
fig1_samples      = []
fig2_samples      = []

# relate objects to figures
fig0_object       = "Sphere"
fig1_object       = "Full cylinder"
fig2_object       = "Hollow cylinder"

SphereXLines      = [np.array([]),np.array([])]
SphereYLines      = np.array([])


# values needed for calculations in corresponding plots
fig0_values       = dict(TX1=TX1,TY1=TY1,alpha=alpha,SIN=SIN,COS=COS,r=2.0,ri=0.5)
fig1_values       = dict(TX1=TX1,TY1=TY1,alpha=alpha,SIN=SIN,COS=COS,r=2.0,ri=0.5)
fig2_values       = dict(TX1=TX1,TY1=TY1,alpha=alpha,SIN=SIN,COS=COS,r=2.0,ri=1.5)

# lists for easy access, no CDS
fig_values        = [fig0_values,fig1_values,fig2_values]
fig_samples       = [fig0_samples,fig1_samples,fig2_samples]
fig_objects       = [fig0_object, fig1_object, fig2_object]



# global variables to stear internal stuff
fig_in_use        = [True,True,True]  # [True]*number_of_plots)  for more general case
figure_list       = [None,None,None]
glob_fun_handles  = [None,None,None]

glob_time         = dict(t=t, t_samples = np.linspace(0.0,6.0,max_samples), num_rolls=0)

# internal CDS, could be replaced by normal dicts
class fake_CDS:
    def __init__(self):
        self.data = dict()

glob_callback_id  = fake_CDS()
glob_SphereXLines = fake_CDS()
glob_SphereYLines = fake_CDS()

glob_callback_id.data  = dict(callback_id  = [None])
glob_SphereXLines.data = dict(SphereXLines = [SphereXLines])
glob_SphereYLines.data = dict(SphereYLines = [SphereYLines])


# images/icons

### bokeh bug?: ###
#"Rolling_test/static/images/first.svg" does not show reliably???
# use winner.svg for now
###             ###
icons_collection  = ["Rolling_test/static/images/winner.svg",
                     "Rolling_test/static/images/second.svg",
                     "Rolling_test/static/images/third.svg"]


###############################################################################
###                    ColumnDataScources (also global)                    ###
###############################################################################

# ColumnDataSources (especially the ones needed for plotting in figures) need to
# be defined in a class
# otherwise they won't get destroyed after reloading the page when the server
# is still running.
# Same with Buttons and Sliders.
# Avoids pending writes error and/or single document error


class RT_global_variables:
    def __init__(self):
        
        # plotting data for moving objects
        self.fig0_data         = ColumnDataSource(data = dict(x=[],y=[],w=[],c=[],a=[]))
        self.fig1_data         = ColumnDataSource(data = dict(x=[],y=[],w=[],c=[],a=[]))
        self.fig2_data         = ColumnDataSource(data = dict(x=[],y=[],w=[],c=[],a=[]))
        self.fig0_lines_data   = ColumnDataSource(data = dict(x=[],y=[]))
        self.fig1_lines_data   = ColumnDataSource(data = dict(x=[],y=[]))
        self.fig2_lines_data   = ColumnDataSource(data = dict(x=[],y=[]))
        
        
        
        # plotting data for fixed objects
        self.ramp_source0      = ColumnDataSource(data = dict(x=[TX1-rampAddLength*COS,TX0],y=[TY1+rampAddLength*SIN,TY0]))
        self.ramp_source1      = ColumnDataSource(data = dict(x=[TX1-rampAddLength*COS,TX0],y=[TY1+rampAddLength*SIN,TY0]))
        self.ramp_source2      = ColumnDataSource(data = dict(x=[TX1-rampAddLength*COS,TX0],y=[TY1+rampAddLength*SIN,TY0]))
        self.wall_source0      = ColumnDataSource(data = dict(x=[TX1-rampAddLength*COS,TX1-rampAddLength*COS],y=[TY1+rampAddLength*SIN,TY0]))
        self.wall_source1      = ColumnDataSource(data = dict(x=[TX1-rampAddLength*COS,TX1-rampAddLength*COS],y=[TY1+rampAddLength*SIN,TY0]))
        self.wall_source2      = ColumnDataSource(data = dict(x=[TX1-rampAddLength*COS,TX1-rampAddLength*COS],y=[TY1+rampAddLength*SIN,TY0]))
        
        # put them in a list for easy access in functions
        self.fig_data          = [self.fig0_data,self.fig1_data,self.fig2_data]
        self.fig_lines_data    = [self.fig0_lines_data,self.fig1_lines_data,self.fig2_lines_data]
        self.ramp_sources      = [self.ramp_source0,self.ramp_source1,self.ramp_source2]
        self.wall_sources      = [self.wall_source0,self.wall_source1,self.wall_source2]
        
        
        self.time_display      = [ColumnDataSource(data = dict(x=[],y=[],t=[])),
                             ColumnDataSource(data = dict(x=[],y=[],t=[])),
                             ColumnDataSource(data = dict(x=[],y=[],t=[]))]
        
        
        self.icon_display      = [ColumnDataSource(data = dict(x=[],y=[],img=[])),
                             ColumnDataSource(data = dict(x=[],y=[],img=[])),
                             ColumnDataSource(data = dict(x=[],y=[],img=[]))]
        
            
        ###############################################################################
        ###                                 Buttons                                 ###
        ###############################################################################
        self.start_button = Button(label="Start", button_type="success")
        self.reset_button = Button(label="Reset", button_type="success")
        
        self.mode_selection = RadioGroup(labels=["one", "all"], active=0, inline=True)
        
        
        ###############################################################################
        ###                                Selections                               ###
        ###############################################################################
        self.object_select0 = Select(title="Object:", value="Sphere", name="obj0",
            options=["Sphere", "Hollow sphere", "Full cylinder", "Hollow cylinder"])
        self.object_select1 = Select(title="Object:", value="Full cylinder", name="obj1",
            options=["Sphere", "Hollow sphere", "Full cylinder", "Hollow cylinder"])
        self.object_select2 = Select(title="Object:", value="Hollow cylinder", name="obj2",
            options=["Sphere", "Hollow sphere", "Full cylinder", "Hollow cylinder"])
        
        
        ###############################################################################
        ###                                 Sliders                                 ###
        ###############################################################################
        # radius
        self.radius_slider0 = Slider(title="Radius [m]", value=2.0, start=1.0, end=maxR, step=0.5)
        self.radius_slider1 = Slider(title="Radius [m]", value=2.0, start=1.0, end=maxR, step=0.5)
        self.radius_slider2 = Slider(title="Radius [m]", value=2.0, start=1.0, end=maxR, step=0.5)
        
        # inner radius
        # end value dependent on selected radius size
        self.ri_slider0 = Slider(title="Inner radius [m]", value=0.5, start=0.0, end=2.0, step=0.5, css_classes=["wall_slider", "obj1", "hidden"])
        self.ri_slider1 = Slider(title="Inner radius [m]", value=0.5, start=0.0, end=2.0, step=0.5, css_classes=["wall_slider", "obj2", "hidden"])
        self.ri_slider2 = Slider(title="Inner radius [m]", value=1.5, start=0.0, end=2.0, step=0.5, css_classes=["wall_slider", "obj3"])
        
        # slider for the angle
        self.alpha_slider0 = Slider(title=u"\u03B1 [\u00B0]", value=20.0, start=5.0, end=alpha_max, step=1.0)
        self.alpha_slider1 = Slider(title=u"\u03B1 [\u00B0]", value=20.0, start=5.0, end=alpha_max, step=1.0)
        self.alpha_slider2 = Slider(title=u"\u03B1 [\u00B0]", value=20.0, start=5.0, end=alpha_max, step=1.0)
