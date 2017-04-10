# Mechanics Apps
Webbased visualization for mechanics content via Bokeh
This Repository contains different prototypes for WebApps for the visualization of mechanics example for the lectures of the Chair of Strcutrual Mechnaics, Prof. Müller, TUM (Technical University of Munich).

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
    * Under Linux and MacOS you can natively execute ```.sh``` scripts from the terminal.
    * If you have problems executing ```.sh``` under windows, install Git (https://git-for-windows.github.io/) or Cygwin (http://www.cygwin.com/).
5. run ```$ ./bokehrunner.sh```.
6. access ```127.0.0.1``` in your browser

### Server Login

1. Access the VPN network of LRZ: see https://www.lrz.de/services/netz/mobil/vpn_en/
    * install Cisco AnyConnect (easy on Windows, more complicated for other OS)
https://www.lrz.de/services/netz/mobil/vpn_en/anyconnect_en/
    * log on to
https://asa-cluster.lrz.de with your credentials: max.mustermann(at)tum.de
2. connect to the VM
    * install PuTTY http://www.putty.org/
    * connect to the VM via PuTTY.

## ToDos
### Selected Apps

#### Technical mechanics I (jf):
:white_check_mark: 1) Tensile testing/Zugversuch (eb)
:white_check_mark: 2) Transverse strain/Querdehnung (eb)
:black_square_button: 3) Doble-supported beam with point load/Balken (ad)
:black_square_button: 4) Maxwell's reciprocity theorem/Reziprozitätssatz von Maxwell (ad)
:black_square_button: 5) Buckling/Knickung (ad)
:black_square_button: 6) Funicular/Seilbahn (br)
:white_medium_square: 7) Polar moment of inertia/Polares Flächenträgheitmoments/ ()
:white_medium_square: 8) Combined moment of inertia/Zusammenges. Flächenträgheitmoments ()
:white_medium_square: 9) Combined center of mass moment/Zusammenges. Schwerpunktsmoment ()
:white_medium_square: 10) Maibaum/Maypole (ak)

#### Supplementary course/Ergänzungskurs Technical mechanics (ft):
:white_check_mark: 1) Spring pendulum/Federpendel (eb)
:white_check_mark: 2) Pendulum/Schwerependel (eb)
:white_check_mark: 3) Base-excited oscillator/Fusspunkterregter Schwinger (eb)
:white_check_mark: 4) Tuned mass damper/Schwingungstilger (eb)
:white_check_mark: 5) Instant centre of rotation/Momentanpol der Leiter (Leiter) (ak)
:white_check_mark: 6) Coriolis force/Drehscheibe-Corioliskraft (eb)
:white_medium_square: 7) Boat with three swimmers/Boot mit drei Schwimmern (ma)
:black_square_button: 8) Collision/Stoss (ma)
:white_check_mark: 9) Rollercoaster (eb)
:white_check_mark: 10) Stopping distances (eb)
:white_check_mark: 11) Projectiles/Wurfgeschoss (eb)
:white_medium_square: 12) Rolling Condition/Abrollbedingungen ()
:white_medium_square: 13) Rolling test/Rollversuch ()
:white_medium_square: 14) Instant centre of rotation of the cupoler/Momentanpol der Koppel (ak)
:white_medium_square: 15) Drop tube/Fallturm (ak)
:white_medium_square: 16) Low-pressure area/Tiefdruck ()
:white_medium_square: 17) Angular momentum/Drallerhaltung2 ()


#### Structural dynamics (cs):
:black_square_button: 1) Euler-Bernoulli Vibrations with analytical solutions (ak)
:black_square_button: 2) FEM Example (ma)
:white_medium_square: 3) Seismic example (ak)

#### Technical Acoustics II (ag):
:white_check_mark: 1) Diffraction (br)

Legend

:white_check_mark: finished

:black_square_button: ongoing

:white_medium_square: planned

### Reference person for theoretical questions
- Francesca Taddei ft
- Axel Greim ag
- Moritz Becker mb
- Corinna Schmausser cs
- Julian Freisinger jf

### Developers
- Emily Bourne eb
- Moustafa Alsayed Ahmad ma
- Siddeshwaran Parthiban sp
- Antonios Kamariotis ak
- Abraham Duplaa ad
- Benjamin Rüth br
