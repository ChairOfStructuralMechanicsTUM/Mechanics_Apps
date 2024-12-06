# Mandelbrot App

This App allows an interactive zoomable view of the mandelbrot set. The script ```mandel_static.py``` allows the generation of static pictures of the mandelbrot set.

## Running
This app can be run by typing
```
$ bokeh serve mandelbrot_app.py
```
into bash and then open
```
http://localhost:5006/mandelbrot_app
```
in the browser.

## ToDo 
- [x] Add Mandelbrot
- [x] update to Bokeh version 11
- [x] Documentation
- [ ] Add Feigenbaum
- [ ] Add other Julia? Add arbitrary Julia?
- [ ] Do different versions using techniques from [here](https://www.ibm.com/developerworks/community/blogs/jfp/entry/How_To_Compute_Mandelbrodt_Set_Quickly?lang=en) 