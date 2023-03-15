# Boundary Value Problem
This App visualized, how one can solve a boundary value problem using the [shooting method](https://en.wikipedia.org/wiki/Shooting_method).

## Running
This app can be run by typing
```
$ bokeh serve boundaryVal_app.py
```
into bash and then open
```
http://localhost:5006/boundaryVal_app
```
in the browser.

## ToDos
- [x] Change the structure of the code towards the style in the sliders example.
- [x] Find workaround for button issue
- [x] Fix issue with plotting of old results
- [x] publish app on the internet.
- [x] publish app with run_apps.py script on top level!
- [x] Update to Bokeh 0.11
- [x] Speed up app, **currently to slow for publication!**
- [x] proper documentation
- [ ] Find another (more complicated) BVP which can be solved with this method
- [ ] Add code for embedding
- [ ] Fix issue with buttons (see simpleButton.py minimal working example)
