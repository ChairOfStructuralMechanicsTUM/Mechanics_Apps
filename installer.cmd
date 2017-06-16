@echo off
echo updating conda...
conda update conda
echo installing bokeh...
conda install bokeh=0.12.5
echo installing nodejs...
conda install -c bokeh nodejs
echo installing twisted...
conda install twisted
echo installing flexx...
conda install -c conda-forge flexx
echo installing vtk...
conda install vtk
