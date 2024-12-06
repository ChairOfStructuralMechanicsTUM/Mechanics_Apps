# Lagrange App
This app visualizes optimization under side conditions in 2D using Lagrange multipliers. The Isocontours of the objective function f(x,y) are plotted as well as the boundarycondition g(x,y)=0. A local minimum is acieved, if the gradients of f and g  are linearly dependent (i.e. parallel).
```
L = f+lambda*g
```
differentiation grad(L) yields
```
grad(f)=-lambda*grad(g)
g=0
```
## Running
This app can be run by typing
```
$ bokeh serve lagrange_app.py
```
into bash and then open
```
http://localhost:5006/lagrange_app
```
in the browser.

##ToDos
- [x] generate running prototype
- [x] refactor code.
- [x] Use Quiver object for gradients.
- [x] add some sample functions
- [x] improve layout
- [x] add support for dynamic user view update
- [x] make app ready for **publication**
- [ ] add text info with function value (+feedback if min/max reached?)
- [ ] select tapSelect, wheelZoom, Pan by default, hide toolbar & logo (activation of tools not possible with version 0.11 upcoming 0.12?)