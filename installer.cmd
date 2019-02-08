@echo off
echo updating conda...
conda update conda
echo installing bokeh...
conda install bokeh=1.0.2
echo installing nodejs...
conda install -c bokeh nodejs
echo installing flexx...
conda install -c conda-forge flexx
echo installing vtk...
conda install vtk
echo installing pscript...
conda install -c conda-forge pscript
