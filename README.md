# Mechanics Apps
Webbased visualization for mechanics content via Bokeh
This Repository contains different prototypes for WebApps for the visualization of mechanics example for the lectures of the Chair of Strcutrual Mechnaics, Prof. Müller, TUM (Technical University of Munich).

## Overview

### Files

* ```Mechanic_Apps.exe``` one click executable for apps. A browser windows pops up, where the individual apps are presented
* ```Mechanic_Apps.cmd/sh``` corresponding shell scripts. Using http://www.f2ko.de/en/b2e.php the exe is created
* ```serverrunner.sh``` runs a python server hosting the overview page
* ```bokehrunner.sh``` runs a bokeh server hosting the bokeh apps
* ```installer.cmd/sh``` for installation of python packages
* ```appnames.conf``` all names of the apps that are run on the bokeh server are collected here
* ```server.conf``` for configuration of the server

### Directories

* ```AppOverviewPage/``` all data for the overview page is collected here
* ```<other>/``` different bokeh apps in directory format (see http://bokeh.pydata.org/en/latest/docs/user_guide/server.html#directory-format)

## Server Architecture

We provide access to the apps through a bokeh server in directory format (see http://bokeh.pydata.org/en/latest/docs/user_guide/server.html#directory-format). Our overview website is hosted by a python twisted (https://twistedmatrix.com/trac/). From there requests are forwarded requests to the bokeh server (http://bokeh.pydata.org/).

The server can be run in two modes:

* online mode: provide access to apps through the internet.
* offline mode: run the server locally and present apps to
lecture audience.

### General Server Setup

If you are using a Linux system, please execute the ```.sh``` scripts, under Windows use the ```.cmd``` scripts if available.

1. install Anaconda with python **version 2.7**: https://www.continuum.io/downloads (Choose installation for all users if possible)
2. install Git
    * Linux: see https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
    * Windows: see https://git-for-windows.github.io/
3. clone **this** repository (*Linux:* from command line, *Windows:* by opening git bash) ```git clone https://github.com/ChairOfStructuralMechanicsTUM/Mechanics_Apps.git```)
4. install additional python packages (bokeh, nodejs, flexx, twisted) by running ```$ ./installer.sh```, ```$ ./installer.cmd```. *Windows:* Right click on script >> Run as administrator. Please check the version of tornado, which is being installed automatically. Bokeh is not compatible with tornado verions >= 4.5, so please make sure, that tornado version 4.4.2 is installed.
5. configure the server with ```server.conf```. If you want to run the server locally, just use the existing configuration. If you want to run the server online, insert the global ip address and make sure that the server port is open to the world wide web. In ```appnames.conf``` write the folder names of the apps you want to run on the server.

### Running the Server

* **Local running** If you just want to use the apps locally, just run Mechanic_Apps.exe (or Linux .sh). You can also access 127.0.0.1:8080 if your browser does not open automatically.
* **Web running** If you want to publish to the web, run server_autorun ```$ ./serverrunner.sh``` and ```$ ./bokehrunner.sh```. Access your global IP in your browser (or the corresponding IP address set in ```server.conf```)

### Server Login to LRZ Windows VM

This guide explains the necessary steps for accessing the Server Setup at TUM: We access a Windows VM running at LRZ (https://www.lrz.de/services/serverbetrieb/).

1. Access the VPN network of LRZ: see https://www.lrz.de/services/netz/mobil/vpn_en/
    * install Cisco AnyConnect (easy on Windows, more complicated for other OS)
https://www.lrz.de/services/netz/mobil/vpn_en/anyconnect_en/
    * log on to
https://asa-cluster.lrz.de with your credentials: max.mustermann(at)tum.de
2. connect to the VM
    * use a remote desktop client (on Ubuntu ```remmina```)
    * get the address of the server from Francesca or Julian
    * make sure that your LRZ account has the right to access the server.
    * Use your LRZ credentials for login (your have to add the prefix ```ads\``` to your username: ads\ga00xxx).

### Apps

#### Technical mechanics (jf):
- [ ][ ] 1) Tensile testing/Zugversuch (eb)
- [ ][ ] 2) Transverse strain/Querdehnung (eb)
- [ ] 3) Doble-supported beam with point load/Balken (ad)
- [ ] 4) Maxwell's reciprocity theorem/Reziprozitaetssatz von Maxwell (ad)
- [ ] 5) Buckling/Knickung (ad)
- [ ] 6) Funicular/Seilbahn (br)
- [ ] 7) Polar moment of inertia/Polares Flaechentraegheitmoments/ ()
- [ ] 8) Combined moment of inertia/Zusammenges. Flaechentraegheitmoments ()
- [ ] 9) Combined center of mass moment/Zusammenges. Schwerpunktsmoment ()
- [ ] 10) Maypole/Maibaum ()
- [ ] 11) Vector addition (rem)
- [ ] 12) What is a moment (rem)
- [ ] 13) Moment is a free vector (rem)

#### Supplementary course/Ergaenzungskurs Technical mechanics (ft, qa):
- [x] 1) Spring pendulum/Federpendel (eb, qa)
- [ ] 2) Pendulum/Schwerependel (eb)
- [ ] 3) Base-excited oscillator/Fusspunkterregter Schwinger (eb)
- [ ] 4) Tuned mass damper/Schwingungstilger (eb, rd)
- [ ] 5) Instant centre of rotation/Momentanpol der Leiter (Leiter) (ak, vu)
- [ ] 6) Coriolis force/Drehscheibe-Corioliskraft (eb)
- [ ] 7) Boat with three swimmers/Boot mit drei Schwimmern (ma)
- [ ] 8) Collision/Stoss (ma)
- [x] 9) Rollercoaster (eb)
- [ ] 10) Stopping distances (eb)
- [x] 11) Projectiles/Wurfgeschoss (eb)
- [ ] 12) Rolling Condition/Abrollbedingungen (eb)
- [ ] 13) Rolling test/Rollversuch (eb)
- [ ] 14) Instant centre of rotation of the cupoler/Momentanpol der Koppel ()
- [ ] 15) Drop tube/Fallturm ()
- [ ] 16) Low-pressure area/Tiefdruck (ma)
- [ ] 17) Angular momentum/Drallerhaltung2 ()


#### Structural dynamics (cs):
- [x] 1) Euler-Bernoulli Vibrations with analytical solutions (ak)
- [ ] 2) FEM Example (ma)
- [ ] 3) Seismic example (ma)

#### Technical Acoustics II (ag):
- [x] 1) Diffraction (br)

#### Integral transform method (fm, he):
- [ ] 1) Leakage (br)

### Supervisors
- Francesca Taddei ft
- Axel Greim ag
- Quirin Aumann qa
- Moritz Becker mb
- Julian Freisinger jf
- Franziska Mittermeier fm
- Hannes Englert he
- Corinna Schmausser cs

### Developers

Please comply with the [DevelopmentGuideline](DevelopmentGuideline.pdf)

- Emily Bourne, eb
- Moustafa Alsayed Ahmad, ma
- Antonios Kamariotis, ak
- Abraham Duplaa, ad
- Benjamin Rueth, br
- Rishith Ellath Meethal, rem
- Ravil Dorozhinskii, rd
- Razieh Rezaei, rr
- Vyshakh Unnikrishnan, vu
