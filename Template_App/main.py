"""
Tamplate App - provides a template for new apps
"""
# general imports
import numpy as np

# bokeh imports
from bokeh.io             import curdoc
from bokeh.plotting       import figure
from bokeh.models         import ColumnDataSource, LabelSet, Arrow, OpenHead
from bokeh.models.glyphs  import MultiLine, Rect, ImageURL #, Patch, 
from bokeh.models.widgets import Paragraph, Button, RadioButtonGroup, RadioGroup #CheckboxGroup
from bokeh.layouts        import column, row, widgetbox, layout, Spacer

# internal imports
from TA_constants import (
    slide_support_img, fixed_support_img,
    xsl, ysl, xsr, ysr,
    support_width, support_height
)

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
cds_support_left  = ColumnDataSource(data=dict(sp_img=[fixed_support_img], x=[xsl] , y=[ysl]))
cds_support_right = ColumnDataSource(data=dict(sp_img=[slide_support_img], x=[xsr] , y=[ysr]))





###################################
#             Figures             #
###################################

### define the figure ###
# the shown attributes should always be set
# if no tool is needed set tools="" or toolbar_location=None
# for more attributes have a look at the bokeh documentation
figure_name = figure(title="Example Figure", x_range=(-1,5), y_range=(-0.5,2.5), height=300, width=400, tools="pan, wheel_zoom, reset")
figure_name.toolbar.logo = None # do not display the bokeh logo


### add the support images ###
# urls and coordinates are provided by a ColumnDataSource
# anchor specifies at which position of the image the x and y coordinates are referring to
# width and height could also be set using constants defined in TA_constants.py and imported here in main.py
figure_name.add_glyph(cds_support_left,  ImageURL(url="sp_img", x='x', y='y', w=0.66, h=0.4, anchor="center"))
figure_name.add_glyph(cds_support_right, ImageURL(url="sp_img", x='x', y='y', w=support_width, h=support_height, anchor="center"))



###################################
#           Page Layout           #
###################################

description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1000)


curdoc().add_root(column(
    description,
    figure_name
))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '


