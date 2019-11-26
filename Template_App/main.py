"""
Tamplate App - provides a template for new apps
"""
# general imports
import numpy as np

# bokeh imports
from bokeh.io             import curdoc
from bokeh.plotting       import Figure
from bokeh.models         import ColumnDataSource, LabelSet, Arrow, OpenHead
from bokeh.models.glyphs  import MultiLine, Rect ,ImageURL #, Patch, 
from bokeh.models.widgets import Paragraph, Button, RadioButtonGroup, RadioGroup #CheckboxGroup
from bokeh.layouts        import column, row, widgetbox, layout, Spacer

# internal imports

# latex integration
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexDiv, LatexLabel, LatexLabelSet, LatexSlider, LatexLegend

# ----------------------------------------------------------------- #

###############################
#      ColumnDataSources      #
###############################








###################################
#           Page Layout           #
###################################

description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1000)


curdoc().add_root(column(
    description
))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '


