from bokeh.models.widgets import Button, RadioButtonGroup, RadioGroup

from os.path import dirname, join, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexSlider



## inner app imports
from NFR_constants import (
        xr_start, xr_end # rod coords
        )


### Sliders and Buttons:
class NFR_GUIControl(object):
    def __init__(self):
        
        self.load_position_slider  = LatexSlider(title="\\mathrm{Load \ Position}", value_unit='\\frac{\\mathrm{L}}{\\mathrm{10}}', value=(xr_end-xr_start)/2, start=xr_start, end=xr_end, step=1.0)
        #load_magnitude_slide = LatexSlider(title="\\mathrm{Load \ Amplitude}", value = 1.0, start=-1.0, end=1.0, step=2.0)
        # TODO: change words from slide to slider
        
        
        # Button to choose type of load:
        self.radio_button_group = RadioButtonGroup(labels=["Point Load", "Constant Load", "Triangular Load", "Temperature"], active=0, width = 600)
        
        self.radio_group_left  = RadioGroup(labels=["fixed", "sliding"], active=0, inline=True)
        self.radio_group_right = RadioGroup(labels=["fixed", "sliding"], active=1, inline=True)
        #radio_group_cross = RadioGroup(labels=["constant", "tapered"], active=0, inline=True) # cross-section
        self.radio_group_ampl  = RadioGroup(labels=["-1", "+1"], active=1, inline=True) # amplitude
        
        # Reset Button
        self.reset_button = Button(label="Reset", button_type="success")
        self.line_button  = Button(label="Show line", button_type="success")
