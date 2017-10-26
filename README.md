# Mechanics Apps
This repository contains the python codes for webbased-visualization for mechanics principles, via Bokeh.
It contains different prototypes for WebApps for the visualization of mechanics example for the lectures of the Chair of Strcutrual Mechnaics, Prof. Müller, TUM (Technical University of Munich).

## Overview
The use of this repository is only suggested for developers. If you are only interested in using the completed apps, please visit the following website:
http://www.bm.bgu.tum.de/lehre/interactive-apps/
We use two different bokeh servers for different groups of apps, in order to avoid conflicts: the simplest apps run on one server, the most complex ones run on a second server.

This repository contains one folder for each App, with a main file and subfunction-files. The following files are important for the installation of the Bokeh framework:

### Files
(.cmd is used for windows and .sh is udes for Linux. From a .sh file you can create the .exe file with http://www.f2ko.de/en/b2e.php)

* ```installer.cmd/sh``` for installation of the current bokeh version and the necessary python packages
* ```server_autorun.cmd/sh``` calls the files for running the bokeh servers (bokehrunner.sh and bokehrunner_testing.sh)
* ```bokehrunner.sh``` runs a bokeh server hosting the simplest bokeh apps
* ```bokehrunner_testing.sh``` runs another bokeh server hosting the more advanced bokeh apps (or prototypes)
* ```appnames.conf``` the list of the names of the simple apps that are completed and ready to run on the first bokeh server
* ```appnames_testing.conf``` the list of the names of the complex apps that are completed and ready to run on the second bokeh server
* ```server.conf``` for configuration of the server, it contains the IP Address of the server, the server port and the bokeh ports (which can be multiple)

### Directories

* ```AppOverviewPage/``` contains screenshots of the apps for a webpage, such as the overview page of the Chair of Structural Mechanics (http://www.bm.bgu.tum.de/lehre/interactive-apps/)
* ```<other>/``` different bokeh apps in directory format (see http://bokeh.pydata.org/en/latest/docs/user_guide/server.html#directory-format)

## Server Architecture

We provide access to the apps through a bokeh server (http://bokeh.pydata.org/) in directory format (see http://bokeh.pydata.org/en/latest/docs/user_guide/server.html#directory-format). 

The server can be run in two modes:

* online mode: provide access to apps through the internet.
* offline mode: run the server locally

### General Server Setup

If you are using a Linux system, please execute the ```.sh``` scripts, under Windows use the ```.cmd``` scripts if available.

1. install Anaconda with python **version 2.7**: https://www.continuum.io/downloads (Choose installation for all users if possible)
2. install Git
    * Linux: see https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
    * Windows: see https://git-for-windows.github.io/
	* For windows we also suggest a desktop version of github: see https://desktop.github.com/ 
3. clone **this** repository (*Linux:* from command line, *Windows:* by opening git bash) ```git clone https://github.com/ChairOfStructuralMechanicsTUM/Mechanics_Apps.git```)
4. install additional python packages (bokeh, nodejs, flexx, twisted) by running ```$ ./installer.sh```, ```$ ./installer.cmd```. *Windows:* Right click on script >> Run as administrator. Please check the version of tornado, which is being installed automatically. Bokeh is not compatible with tornado verions >= 4.5, so please make sure, that tornado version 4.4.2 is installed.
5. configure the server with ```server.conf``` to your own server settings. If you want to run the server locally, just use the existing configuration. If you want to run the server online, insert the global ip address and make sure that the server port is open to the world wide web. 
6. In ```appnames.conf``` write the folder names of the apps you want to run on the server.

### Running the Server

* **Local running** 
	- If you just want to run a single app locally:
		- open a command window and enter:  ```boke serve --show Directory_name```
		
		- For example: 	```boke serve --show Diffraction```
		
	- The browser should open automatically, showing the app. You can also directly access *localhost:Port* (For example *localhost:5006/Diffraction*) if your browser does not open automatically.
	
* **Web running** 
	- If you want to publish to the web, 
		- add the app to the file ```appnames.conf```
		- run server_autorun.exe. 
		- Navigate to *Global_IP:Port* in your browser (or the corresponding IP address set in ```server.conf```). For example: *127.0.0.1:5006*
		- In our case, we use a proxy name for the *IP:Port*, which is *apps.bm.bgu.tum.de:5006* in order to display a more approrpate website name.

### Apps 

#### Technical mechanics (jf):
- [ ] 1) Tensile testing/Zugversuch (eb,rr)
- [ ] 2) Transverse strain/Querdehnung (eb,rr)
- [ ] 3) Doble-supported beam with point load/Balken (ad)
- [x] 4) Maxwell's reciprocity theorem/Reziprozitaetssatz von Maxwell (ad)
- [x] 5) Buckling/Knickung (ad)
- [ ] 6) Funicular/Seilbahn (br)
- [ ] 7) Polar moment of inertia/Polares Flaechentraegheitmoments/ ()
- [ ] 8) Combined moment of inertia/Zusammenges. Flaechentraegheitmoments ()
- [ ] 9) Combined center of mass moment/Zusammenges. Schwerpunktsmoment ()
- [ ] 10) Maypole/Maibaum ()
- [x] 11) Vector addition (rem)
- [x] 12) Couple-moment (rem)
- [ ] 13) Moment is a free vector (rem)

#### Supplementary course/Ergaenzungskurs Technical mechanics (ft, qa):
- [x] 1) Damped oscillator/Federpendel (eb, qa, ft)
- [x] 2) Pendulum/Schwerependel (eb, ft)
- [ ] 3) Base-excited oscillator/Fusspunkterregter Schwinger (eb)
- [ ] 4) Tuned mass damper/Schwingungstilger (eb, rd)
- [ ] 5) Instant centre of rotation/Momentanpol der Leiter (Leiter) (ak, vu)
- [ ] 6) Coriolis force/Drehscheibe-Corioliskraft (eb)
- [ ] 7) Boat with three swimmers/Boot mit drei Schwimmern (ma)
- [ ] 8) Collision/Stoss (ma)
- [x] 9) Rollercoaster (eb)
- [x] 10) Stopping distances (eb)
- [x] 11) Projectiles/Wurfgeschoss (eb)
- [ ] 12) Rolling Condition/Abrollbedingungen (eb)
- [ ] 13) Rolling test/Rollversuch (eb)
- [ ] 14) Instant centre of rotation of the cupoler/Momentanpol der Koppel ()
- [ ] 15) Drop tube/Fallturm ()
- [ ] 16) Low-pressure area/Tiefdruck (ma)
- [ ] 17) Angular momentum/Drallerhaltung2 ()


#### Structural dynamics (cs):
- [ ] 1) Euler-Bernoulli Vibrations with analytical solutions (ak)
- [ ] 2) 2D cantilever beam (ma)
- [x] 3) Seismic example (ma)

#### Technical Acoustics II (ag, cw):
- [x] 1) Diffraction (br)
- [ ] 2) Vibroacoustic plates (rd)

#### Integral transform method (fm, he):
- [x] 1) Sampling (br)

### Supervisors
- Francesca Taddei (ft)
- Axel Greim (ag)
- Quirin Aumann (qa)
- Moritz Becker (mb)
- Julian Freisinger (jf)
- Franziska Mittermeier (fm)
- Hannes Englert (he)
- Corinna Schmausser (cs)
- Christoph Winter (cw)

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
