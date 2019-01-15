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

* Try to avoid global variables! Otherwise the app might behave strangely. In most cases, global variables can be replaced by `ColumnDataSource` objects (see [ColumnDataSource objects](#columndatasource-objects)). If there is no way to avoid them, please use the following naming convention: `gl[APPNAME][VARNAME]`, so to define the velocity in the Collision app for example, use `glCollisionVelocity`.
* Name classes and corresponding files by the app name. For example in Mechanic_Apps/SDOF use the name `SDOF_Spring` for the spring class to avoid strange behaviour by unwanted imports.
* For static resources use the static folder in the directory of the app. See Diffraction app for a use case (Diffraction/main.py:294-304, commit 188f76b15959222aa0a8bf3f55d476a52abbf221).
* For complex behaviour try to introduce objects, that bundle the functionality and the data (e.g. https://github.com/ChairOfStructuralMechanicsTUM/Mechanics_Apps/blob/master/Rollercoaster/DraggablePath.py)
* Try to avoid very long scripts. It is usually not a good idea to have more than 500 lines of code in one script, no one can understand this.
* Try to avoid very long and complex functions. It might be helpful to subdivide a function into several functions that partially solve a certain task.
* Don't use ```from ... import *```. It is hard to understand the origin of a function or variable if it is not imported explicitly. Better use ```from ... import foo, bar```.

## Debugging with Visual Studio Code
It is possible to debug the bokeh apps using a custom launch configuration in Visual Studio Code. It is pssoble to add breakpoints and monitor your variables in VS Code. You have to add the following code to your `launch.json`:

```json
{   
    "name": "Bokeh App", 
    "type": "python", 
    "request": "launch", 
    "stopOnEntry": false,
    "module": "bokeh", 
    "args": [ "serve", "--show", "${fileDirname}" ], 
    "console": "integratedTerminal",
}
```
More information on launch configurations: https://code.visualstudio.com/docs/editor/debugging.

## LaTeX support
Latex support is made available via the KaTeX library (https://khan.github.io/KaTeX/). All widgets, annotations, etc. which provide LaTeX support can be found in the folder `shared` and can be imported using:

```python
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv, LatexLabel, LatexLabelSet, LatexSlider, LatexLegend
```
Following, the available classes will be described. Except in `LatexDiv`, the backslash has to be escaped with `\\`, as in:
```python
llabel = LatexLabel(text='\\alpha',x=20,y=20)
```

### App descriptions: `LatexDiv`
A class `LatexDiv` is available, which works the same way as the normal `Div` but parses also Latex input. Indstead of `Div`, use `LatexDiv`, if the document contains Latex code. The identifiers are `$ \alpha $` or `\( \alpha \)` for inline mode and `$$ \alpha $$` or `\[ \alpha \]` for display mode.

### Labels: `LatexLabel` and `LatexLabelSet`
`LatexLabel` works the same way as `Label`, but it parses everything provided with the `text` attribute as LaTeX math mode code.

`LatexLabelSet` also parses all text as LaTeX math mode, but it can also be specified, if the display mode (i.e. $$\alpha$$) should be used:
```python
llabel = LatexLabelSet(text='\\alpha',x='x',y='y',display_mode=True)
```
The default is `False`. All other attributes can be used in the same way as for the classes without LaTeX support.

### Slider: `LatexSlider`
The `LatexSlider` renders everything provided with the `title` attribute as LaTeX math mode code. The new attribute `value_unit` is LaTeX code that will be displayed after the value of the slider. Example:
```python
slider= LatexSlider(title="\\sigma_x=",value_unit='\\frac{\\mathrm{N}}{\\mathrm{mm}^2}',value= 0,start = -10, end = 10, step = 0.5)
```

### Legend: `LatexLegend`
`LatexSlider` renders everything provided in the `items` attribute as LaTeX math mode code. Use `max_label_width` to specify the width of the legend box, as the automatic calculation is not yet implementd. Example:
```python
legend = LatexLegend(items=[
    ("\\text{Solution part: }\\frac{1}{2}\\cosh(\\lambda\\xi)", [data1]),
    ("\\text{Solution part: }-\\frac{1}{2} \\frac{c(\\lambda)}{s(\\lambda)} \\sinh(\\lambda\\xi)", [data2]),
], location=(0, 0), spacing=10, max_label_width=870)
plot.add_layout(legend,'above')
```

## Deprecated Functions
The following list provides some code snippets to help replacing deprecated Bokeh functions.
 
### Periodic Callback
old (deprecated in Bokeh 0.12.15):
```python
curdoc().add_periodic_callback(foo,100)
curdoc().remove_periodic_callback(foo)
```
- foo: callback function to execute periodically
- 100 milliseconds between each execution

new:
```python
callback_id = curdoc().add_periodic_callback(foo,100)
curdoc().remove_periodic_callback(callback_id)
```
- return callback ID to a new variable `callback_id`
- call remove function using the callback ID instead of callback function foo


## `ColumnDataSource` objects
Instead of using global variables like in this code
```python
class m_class:
    val = 1
    def __init__(self, v):
        self.val = v
    def __str__(self):
        return str(self.val)+"\n"
    def addone(self):
        self.val += 1

x1 = 3.1
x2 = 10
y = [2.4, 1.0]
m = m_class(4)

def foo():
    global x1, x2, y, m
    x1 += 1
    y.sort()
    m.addone()

foo()
```
one can avoid them by using Bokeh's `ColumnDataSource` objects.
```python
from bokeh.models import ColumnDataSource

global_x = ColumnDataSource(data = dict(x1 = [3.1], x2 = [10]))
global_y = ColumnDataSource(data = dict(y = [[2.4,1.0]]))  # store list in list for consistency, otherwise y = global_y.data["y"]
global_m = ColumnDataSource(data = dict(m = [m_class(4)]))


def foo():
    # "load" global variables
    [x1] = global_x.data["x1"]
    [y] = global_y.data["y"]
    [m] = global_m.data["m"]
    
    x1 += 1
    y.sort()
    m.addone()
    
    # save global variables
    global_x.data = dict(x1 = [x1], x2 = [10]) # if x2 is dismissed, global_x only consists of x1
    # y and m were changed by in-place-operations saved in the same object -> no save necessary

foo()
```

* ColumnDataSources can hold any number of variables using a dictionary and lists.
* Updating single variables of a ColumnDataSource is **not** possible. Always update the whole dict, otherwise variables will get lost.
* All "global" variables need to be loaded in the specific function. If in-place-operations were used, the saving step is optional.


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
