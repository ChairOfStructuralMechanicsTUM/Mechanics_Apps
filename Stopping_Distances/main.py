from Problem import *
from os.path import dirname, join, split

# create each part of the window
Visual=Visualisation()
Plotter=Graphs()
Prob = Problem(Visual,Plotter)

## Send to window
curdoc().add_root(row(column(Visual.fig,Plotter.Layout),Prob.Layout))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
