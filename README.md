# Mechanics Apps
Webbased visualization for mechanics content via Bokeh
This Repository contains different prototypes for WebApps for the visualization of mechanics example for the lectures of the Chair of Strcutrual Mechnaics, Prof. M�ller, TUM (Technische Universit�t M�nchen).

## Server Architecture

We provide access to the apps through a bokeh server in directory format (see http://bokeh.pydata.org/en/latest/docs/user_guide/server.html#directory-format). Our overview website is hosted by a nginx server which forwards requests to the bokeh server.

The server can be run in two modes:

* online mode: provide access to apps through the internet.
* offline mode: run the server locally and present apps to
lecture audience.

### Server Setup

1. install Anaconda with python version 2.7: https://www.continuum.io/downloads
2. install additional python packages (bokeh, nodejs, flexx, twisted) by running ```$ ./installer.sh```
3. configure the server with ```server.conf```. If you want to run the server locally, just use the existing configuration.
4. run ```$ ./serverrunner.sh```. If you want to use port 80 run it as sudo.
5. run ```$ ./bokehrunner.sh```.
6. access ```127.0.0.1``` in your browser

## ToDos
### Selected Apps

#### Technical mechanics I (jf):
- [x] 1) Tensile testing/Zugversuch (eb)
- [x] 2) Transverse strain/Querdehnung (eb)
- [ ] 3) Doble-supported beam with point load/Balken (ad)
- [ ] 4) Maxwell's reciprocity theorem/Reziprozit�tssatz von Maxwell (ad)
- [ ] 5) Buckling/Knickung (ad)

#### Supplementary course/Erg�nzungskurs Technical mechanics (ft):
- [ ] 1) Spring pendulum/Federpendel (sp)
- [ ] 2) Pendulum/Schwerependel (sp)
- [ ] 3) Base-excited oscillator/Fu�punkterregter Schwinger (sp)
- [ ] 4) Tuned mass damper/Schwingungstilger (sp)
- [ ] 5) Instant centre of rotation/Momentanpol der Leiter (Leiter) (ak)
- [x] 6) Coriolis force/Drehscheibe-Corioliskraft (eb)
- [ ] 7) Boat with three swimmers/Boot mit drei Schwimmern (ma)
- [ ] 8) Collision/Sto� (ma)
- [ ] 9) Rollercoaster (eb)

#### Structural dynamics (cs):
- [ ] 1) Euler-Bernoulli Vibrations with analytical solutions (ak)
- [ ] 2) FEM Example (ma)
- [ ] 3) Seismic example (ak)


#### Technical Acoustics II (ag):
- [x] 1) Diffraction (br)

### Proper Documentation & Refactoring

#### Technical mechanics I:
- [x] 1) Zugversuch/Tensile testing
- [x] 2) Querdehnung/Transverse strain
- [ ] 3) Doble-supported beam with point load/Balken
- [ ] 4) Maxwell's reciprocity theorem/Reziprozit�tssatz von Maxwell
- [ ] 5) Buckling/Knickung

#### Supplementary course/Erg�nzungskurs Technical mechanics:
- [ ] 1) Spring pendulum/Federpendel
- [ ] 2) Pendulum/Schwerependel
- [ ] 3) Base-excited oscillator/Fu�punkterregter Schwinger
- [ ] 4) Tuned mass damper/Schwingungstilger
- [ ] 5) Instant centre of rotation/Momentanpol der Leiter (Leiter)
- [x] 6) Coriolis force/Drehscheibe-Corioliskraft
- [ ] 7) Boat with three swimmers/Boot mit drei Schwimmern
- [ ] 8) Collision/Sto�
- [ ] 9) Rollercoaster

#### Structural dynamics (cs):
- [ ] 1) Euler-Bernoulli Vibrations with analytical solutions
- [ ] 2) FEM Example
- [ ] 3) Seismic example

#### Technical Acoustics II (ag):
- [x] 1) Diffraction

### Reference person for theoretical questions
- Francesca Taddei ft
- Axel Greim ag
- Moritz Becker mb
- Corinna Schmausser cs
- Julian Freisinger jf

### Developers
- Emily Bourne em
- Moustafa Alsayed Ahmad ma
- Siddeshwaran Parthiban sp
- Antonios Kamariotis ak
- Abraham Duplaa ad
- Banjamin R�th br
