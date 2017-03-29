from Problem import *

Visual=Visualisation()
Plotter=Graphs()
Prob = Problem(Visual,Plotter)

## Send to window
curdoc().add_root(row(column(Visual.fig,Plotter.Layout),Prob.Layout))
curdoc().title = "Bremsstrecke"
