# Convolution

This App visualized, the convolution of two functions, by explicitly showing the overlapping area. See [here](https://en.wikipedia.org/wiki/Convolution#Visual_explanation).

## Running
This app can be run by typing
```
$ bokeh serve convolution_app.py
```
into bash and then open
```
http://localhost:5006/convolution_app
```
in the browser.

## ToDos

- [x] Write simple prototype for visualization of convolution with one given function
- [x] Add support for entering arbitrary functions
- [x] Update to Bokeh 0.11
- [x] Add easier examples (e.g. Heaviside(x) convolved with cos(x*pi/2) * Heaviside(x+1) * Heaviside(1-x))
- [x] proper documentation
- [ ] add support for dynamic user view update

