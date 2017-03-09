# Rollercoaster App

Prototype of a WebApp demonstrating Transverse Strain via Bokeh for the lectures at the Chair of Structural Mechanics, Prof. Müller, TUM (Technische Universität München).

The app can be run using the command "bokeh serve --show Rollercoaster/" from the parent directory.

## To Do
- [ ] Find a smooth interpolation of a loop-the-loop (currently using cubic interpolation)
      
      ideas:
          - use interpolation with x=f(y) for zones where x_i>x_{i+1}
- [ ] Add force arrows
- [ ] add cart
- [ ] add energy bar chart
