echo "updating conda..."
conda update conda
echo "installing bokeh..."
conda install bokeh=0.12.4
echo "installing nodejs..."
conda install -c bokeh nodejs
echo "installing flexx..."
conda install -c bokeh flexx
echo "installing twisted..."
conda install twisted
echo "installing vtk..."
conda install vtk
echo "installing tornado 4.4.2...."
conda install tornado=4.4.2

