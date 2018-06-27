# Coding Style

* for directory names use ```_``` for blank space. In the app title (see formatting hints below) use a real blank. **do not use ```-``` or CamelCase style**

# Developer Workflow

The following points are important for all developers.

* Apps that are not executable using ```bokeh serve --show app_directory``` should **not** be pushed to master, you may use a branch for experimental apps.
* Develop app in directory format (see http://bokeh.pydata.org/en/latest/docs/user_guide/server.html#directory-format).
* Use the **same** name for the directory and the title of the app. The title of the app shall explain the mechanical content - not the method of visualization. (e.g. use "conservation of momentum" instead of "boat with three swimmers"). See also coding style above.
* The Language of everything (titles, explanations, comments in code, etc.) within the whole project is **English**!
* For the description file, formulas can be added with the aid of MathJax http://docs.mathjax.org/en/latest/start.html
* If your app is completed ask your supervisor whether there are any additional improvements to be done or if the app is ready for publication.
* Write a mail to Francesca that your app is ready for publication.

## Developer Hints

* Try to avoid global variables! Otherwise the app might behave strangely. If there is no way to avoid them, please use the following naming convention: `gl[APPNAME][VARNAME]`, so to define the velocity in the Collision app for example, use `glCollisionVelocity`.
* For static resources use the static folder in the directory of the app. See Diffraction app for a use case (Diffraction/main.py:294-304, commit 188f76b15959222aa0a8bf3f55d476a52abbf221).
* For complex behaviour try to introduce objects, that bundle the functionality and the data (e.g. https://github.com/ChairOfStructuralMechanicsTUM/Mechanics_Apps/blob/master/Rollercoaster/DraggablePath.py)
* Try to avoid very long scripts. It is usually not a good idea to have more than 500 lines of code in one script, no one can understand this.
* Try to avoid very long and complex functions. It might be helpful to subdivide a function into several functions that partially solve a certain task.
* Don't use ```from ... import *```. It is hard to understand the origin of a function or variable if it is not imported explicitly. Better use ```from ... import foo, bar```.

## LaTeX support
Latex support is made available via the KaTeX library (https://khan.github.io/KaTeX/). All widgets, annotations, etc. which provide LaTeX support can be found in the folder `shared` and can be imported using:

```python
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_div import LatexDiv
```
Following, the available classes will be described. 

### App descriptions: `LatexDiv`
A class `LatexDiv` is available, which works the same way as the normal `Div` but parses also Latex input. Indstead of `Div`, use `LatexDiv`, if the document contains Latex code. The identifiers are `$ \alpha $` or `\( \alpha \)` for inline mode and `$$ \alpha $$` or `\[ \alpha \]` for display mode.

### Labels: `LatexLabel` and `LatexLabelSet`
`LatexLabel` works the same way as `Label`, but it parses everything provided with the `text` attribute as LaTeX math mode code. To escape the backslash use `\\` as in 
```python
llabel = LatexLabel(text='\\alpha',x=20,y=20)
```
`LatexLabelSet` also parses all text as LaTeX math mode, but it can also be specified, if the display mode (i.e. $$\alpha$$) should be used:
```python
llabel = LatexLabelSet(text='\\alpha',x='x',y='y',display_mode=True)
```
The default is `False`. All other attributes can be used in the same way as for the classes without LaTeX support.

# Francesca Final Acceptance and Publication

The following points are executed by Francesca only.

* Make sure that the status of finalized apps is updated in ```Mechanic_Apps/README.md``` (done by Francesca)
* Add description of app and a matching tooltip on overview page
    * put app in the right position in the hierarchy (semester, lecture).
* Add app directory name to ```appnames.conf```.
    * Maintain alphabetical order.
* Test setup by starting the server locally (```Mechanic_Apps.exe```):
    * Is the app working?
    * Can you access the app from the overview page?
* Publish new app to server:
    * Push to master branch from local machine
    * Pull from git on server
    * Relauch server using ```server_autorun.exe```.

# Formatting hints

* We use ```curdoc().title = "Appname"``` for defining the title. This title can be seen, for example in the Tab title of the browser. Your directory name should comply with the standard defined above. Use

    ```
    curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')
    ```

    This gets path of parent directory and only uses the name of the Parent Directory for the app title name. Then it replaces underscores '_' and minuses '-' with blanks ' '.
