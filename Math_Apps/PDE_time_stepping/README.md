# Partial Differential Equation App
This app visualizes, how different PDE Solvers solve different PDEs. The user can interactively change stepwidth (in time and space) and initial condition. One can also choose from 2 different solvers (explicit Euler, implicit Euler, implicit midpoint rule) and 2 different PDEs (Heat transport and wave equation) as well as from an implicit and an explicit solver for each PDE. For comparison the analytical solution is shown, which is derived using a fourier series approach.

## Running
Enter 
```
$ bokeh serve pde_app.py
```
in bash to run the app. Then enter
```
http://localhost:5006/pde_app
```
in your browser to use the app in it.

##ToDos
- [x] publish this to the internet
- [x] Update to Bokeh 0.11
- [x] Add analytical solution
- [x] Modify App to support non-homogeneous Dirichlet BC in the analytical solution
- [x] proper documentation
- [ ] Add automatic refresh on zooming
- [ ] Add symplectic integrator (e.g. Leapfrog)
- [ ] Add "PLAY" button for continuous time.
- [ ] Add code for embedding.
