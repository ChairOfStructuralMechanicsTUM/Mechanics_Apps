from Problem import *

Visual=Visualisation()
Plotter=Graphs()
Prob = Problem(Visual,Plotter)

## Send to window
curdoc().add_root(row(column(Visual.disp(),Plotter.disp()),Prob.disp()))
curdoc().title = "Bremsstrecke"
