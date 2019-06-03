from __future__ import division # float division only, like in python 3
from bokeh.models import Select, Button, Slider
from bokeh.models.widgets import RadioGroup

from RT_global_variables import maxR, alpha_max


###############################################################################
###                                 Buttons                                 ###
###############################################################################
start_button = Button(label="Start", button_type="success")
reset_button = Button(label="Reset", button_type="success")

mode_selection = RadioGroup(labels=["one", "all"], active=0, inline=True)


###############################################################################
###                                Selections                               ###
###############################################################################
object_select0 = Select(title="Object:", value="Sphere", name="obj0",
    options=["Sphere", "Hollow sphere", "Full cylinder", "Hollow cylinder"])
object_select1 = Select(title="Object:", value="Full cylinder", name="obj1",
    options=["Sphere", "Hollow sphere", "Full cylinder", "Hollow cylinder"])
object_select2 = Select(title="Object:", value="Hollow cylinder", name="obj2",
    options=["Sphere", "Hollow sphere", "Full cylinder", "Hollow cylinder"])


###############################################################################
###                                 Sliders                                 ###
###############################################################################
# radius
radius_slider0 = Slider(title="Radius [m]", value=2.0, start=1.0, end=maxR, step=0.5)
radius_slider1 = Slider(title="Radius [m]", value=2.0, start=1.0, end=maxR, step=0.5)
radius_slider2 = Slider(title="Radius [m]", value=2.0, start=1.0, end=maxR, step=0.5)

# inner radius
# end value dependent on selected radius size
ri_slider0 = Slider(title="Inner radius [m]", value=0.5, start=0.0, end=2.0, step=0.5, css_classes=["wall_slider", "obj1", "hidden"])
ri_slider1 = Slider(title="Inner radius [m]", value=0.5, start=0.0, end=2.0, step=0.5, css_classes=["wall_slider", "obj2", "hidden"])
ri_slider2 = Slider(title="Inner radius [m]", value=1.5, start=0.0, end=2.0, step=0.5, css_classes=["wall_slider", "obj3"])

# slider for the angle
alpha_slider0 = Slider(title=u"\u03B1 [\u00B0]", value=20.0, start=5.0, end=alpha_max, step=1.0)
alpha_slider1 = Slider(title=u"\u03B1 [\u00B0]", value=20.0, start=5.0, end=alpha_max, step=1.0)
alpha_slider2 = Slider(title=u"\u03B1 [\u00B0]", value=20.0, start=5.0, end=alpha_max, step=1.0)