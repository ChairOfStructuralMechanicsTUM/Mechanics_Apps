# ODE System App
Plots direction field for arbitrary functions (u(x,y) and v(x,y)) and critical points. Additionally plots streamline for 
initial value (x0,y0).

## Running
Enter 
```
$ bokeh serve odesystem_app.py
```
in bash to run the app. Then enter
```
http://localhost:5006/odesystem_app
```
in your browser to use the app in it.

##ToDos
- [x] Add streamlines
- [x] Add support for plotting of critical points
- [x] Add support for plotting of critical lines
- [x] publish this to the internet
- [x] Update to Bokeh 0.11
- [x] Add standard examples as predefined equations (circular attractor...)
- [x] Improve GUI with panels
- [x] Adjust to user's view (if function is updated)
- [x] proper documentation
- [x] Adjust to user's view (as often as possible in a performant way)
- [x] Add clickable initial condition
- [x] Change quiver plotting to use Quiver object
- [ ] Try to improve speed
- [ ] Add code for embedding.
