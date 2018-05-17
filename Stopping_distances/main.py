from Problem import Problem
from Graphs import Graphs
from Visualisation import Visualisation
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_div import LatexDiv
from bokeh.io import curdoc
from bokeh.layouts import column, row

# create each part of the window
Visual=Visualisation()
Plotter=Graphs()
Prob = Problem(Visual,Plotter)

# add app description
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)

## Send to window
curdoc().add_root(column(description, row(column(Visual.fig,Plotter.Layout),Prob.Layout)))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
