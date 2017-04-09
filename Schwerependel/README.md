# Pendulum/Schwerependel App

Prototype of a WebApp demonstrating a pendulum via Bokeh for the lectures at the Chair of Structural Mechanics, Prof. Müller, TUM (Technische Universität München).

The app can be run using the command "bokeh serve --show Schwerependel/" from the parent directory.

## To Do
- [ ] fix energy conservation for double pendulum
       (Lagrangian equations give same result for ddTheta but give ddPhi dependant on ddTheta, removing this dependance gives division by 0 at theta=0)
