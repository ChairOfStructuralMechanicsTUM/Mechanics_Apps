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

load_position_slide  = LatexSlider(title="\\mathrm{Load \ Position}", value_unit='\\frac{\\mathrm{L}}{\\mathrm{10}}', value=5, start=xr_start, end=xr_end, step=1.0)
load_magnitude_slide = LatexSlider(title="\\mathrm{Load \ Amplitude}", value = 1.0, start=-1.0, end=1.0, step=2.0)
right_support_position_slide = LatexSlider(title="\\mathrm{Support \ Position}", value_unit='\\frac{\\mathrm{L}}{\\mathrm{10}}', value=xr_end, start=xr_start, end=xr_end, step=1.0)



# Button to choose type of load:
radio_button_group = RadioButtonGroup(labels=["Point Load", "Constant Load", "Triangular Load", "Temperature"], active=0, width = 600)

radio_group_left  = RadioGroup(labels=["fixed", "sliding"], active=0, inline=True)
radio_group_right = RadioGroup(labels=["fixed", "sliding"], active=0, inline=True)
radio_group_cross = RadioGroup(labels=["constant", "tapered"], active=0, inline=True) # cross-section

# Reset Button
reset_button = Button(label="Reset", button_type="success")
dummy_button = Button(label="Dummy/Test", button_type="success")
