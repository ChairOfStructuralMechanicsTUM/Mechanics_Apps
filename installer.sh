echo "updating conda..."
conda update conda
echo "installing bokeh..."
conda install bokeh
echo "installing nodejs..."
conda install -c bokeh nodejs
echo "installing flexx..."
conda install -c bokeh flexx
echo "installing vtk..."
conda install vtk
echo "installing tornado"
conda install tornado
echo "installing pscript..."
conda install -c conda-forge pscript

