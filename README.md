# Mechanics Apps
This repository contains the Python codes for webbased-visualization for mechanics principles, via Bokeh.
It contains different prototypes for web apps for the visualization of mechanics examples for the lectures of the Chair of Structural Mechanics, Prof. Müller, TUM (Technical University of Munich).

## Overview

The use of this repository is only suggested for developers. If you are only interested in using the completed apps, please visit the following website: http://www.bm.bgu.tum.de/lehre/interactive-apps/. <br>
For the math apps visit https://www.groups.ma.tum.de/en/algebra/karpfing/buecher/videoanimationen-interaktive-apps/.

Before starting developing, please take a look at our [Wiki](https://github.com/ChairOfStructuralMechanicsTUM/Mechanics_Apps/wiki). We use two different bokeh servers for different groups of apps, in order to avoid conflicts: most of the apps run on one server, some have to run on a second server since they interfere with other apps and might brake them.


This repository contains one folder for each app, with a main file and subfunction-files. The following files are important for running the server:

### Files
(.cmd is used for Windows and .sh is used for Linux. From a .sh file you can create the .exe file with the "Bat to Exe Converter" on the server) <br>
All apps run on one physical server which provides a different port for each bokeh server. <br>
We use a Windows server, therefore we use powershell and cmd scripts.

* ```appnames.conf``` the list of the names of apps that are completed and ready to run on the first bokeh server
* ```appnames_testing.conf``` the list of the names of the apps that are completed and ready to run on the second bokeh server
* ```appnames_math.conf``` the list of the names of the math apps that are completed and ready to run on another bokeh server
* ```bokehrunner.ps1``` runs a bokeh server hosting most of the bokeh apps
* ```bokehrunner_testing.ps1``` runs another bokeh server hosting critical bokeh apps (might interfere with other apps if used on the same bokeh server)
* ```bokehrunner_math.ps1``` runs a bokeh server hosting math bokeh apps
* ```server.conf``` for configuration of the server, it contains the IP address of the server, the server port and the bokeh ports (which can be multiple)
* ```server_autorun.cmd``` calls the files for running the bokeh servers (.ps1 files)
* ```server_shutdown.cmd``` kills the processes for restart

### Directories

* ```AppOverviewPage/``` contains screenshots of the apps for a webpage, such as the overview page of the [Chair of Structural Mechanics](http://www.bm.bgu.tum.de/lehre/interactive-apps/)
* ```shared/``` contains custom LaTeX support for some bokeh objects like sliders and labels
* ```Math_Apps/``` interactive math apps provided for the [Department of Mathematics](https://www.groups.ma.tum.de/en/algebra/karpfing/buecher/videoanimationen-interaktive-apps/)
* ```<other>/``` different bokeh apps in directory format (see [Bokeh User Guide](http://bokeh.pydata.org/en/latest/docs/user_guide/server.html#directory-format))
* ```.gitignore``` the files or file extensions listed here are not committed to GitHub when changed locally

## Server Architecture

We provide access to the apps through a bokeh server (http://bokeh.pydata.org/) in directory format (see http://bokeh.pydata.org/en/latest/docs/user_guide/server.html#directory-format). 

The server can be run in two modes:

* online mode: provide access to apps through the internet.
* offline mode: run the server locally

### General Server Setup

1. install Anaconda with Python version defined in the [Wiki](https://github.com/ChairOfStructuralMechanicsTUM/Mechanics_Apps/wiki/Current-Versions): https://www.anaconda.com/distribution/
2. install Git
    * Linux: see https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
    * Windows: see https://git-for-windows.github.io/
	* For Windows we also suggest a desktop version of GitHub: see https://desktop.github.com/ 
3. clone **this** repository 
    * Windows with GitHub Desktop: File -> Clone Repository
    * Linux from command line: ```git clone https://github.com/ChairOfStructuralMechanicsTUM/Mechanics_Apps.git```
    * Windows with git bash: ```git clone https://github.com/ChairOfStructuralMechanicsTUM/Mechanics_Apps.git```
4. install additional Python packages (bokeh, nodejs, flexx, twisted) <br> *Windows:* If you chose to install Anaconda for all users, right click >> Run as administrator.
5. configure the server with ```server.conf``` to your own server settings. If you want to run the server locally, just use the existing configuration. If you want to run the server online, insert the global ip address and make sure that the server port is open to the world wide web. 
6. In ```appnames.conf``` write the folder names of the apps you want to run on the server.

### Running the Server

* **Local running** (If you just want to run a single app locally)
	- open a command window and navigate to the repository folder
	- enter  ```bokeh serve --show Directory_name```
	- for example: 	```bokeh serve --show Diffraction```
	- the browser should open automatically and show the app. You can also directly access *localhost:Port* (For example *localhost:5006/Diffraction*) if your browser does not open automatically.
	
* **Web running** (If you want to publish several apps to the web)
	- add the app to the file ```appnames.conf```
	- run `server_autorun.exe` 
	- Navigate to *Global_IP:Port* in your browser (or the corresponding IP address set in ```server.conf```). For example: *127.0.0.1:5006*
	- In our case, we use a proxy name for the *IP:Port*, which is *apps.bm.bgu.tum.de:5006* in order to display a more appropriate website name.

<br>

For more information and contacts, please consult the [Wiki](https://github.com/ChairOfStructuralMechanicsTUM/Mechanics_Apps/wiki).

<br>

## Apps 

#### Technical Mechanics:
- [ ] 1) Tensile testing / Zugversuch (eb,rr)
- [ ] 2) Transverse strain / Querdehnung (eb,rr)
- [ ] 3) Double-supported beam with point load / Balken (ad)
- [x] 4) Maxwell's reciprocity theorem / Reziprozitätssatz von Maxwell (ad, me)
- [x] 5) Buckling / Knickung (ad, me)
- [ ] 6) Funicular / Seilbahn (br)
- [ ] 7) Polar moment of inertia / Polares Flächenträgheitsmoment ()
- [ ] 8) Combined moment of inertia / Zusammenges. Flächenträgheitsmoment ()
- [ ] 9) Combined center of mass moment / Zusammenges. Schwerpunktsmoment ()
- [ ] 10) Maypole / Maibaum ()
- [x] 11) Vector addition (rem, cfm)
- [ ] 12) Couple-moment (rem, cfm)
- [ ] 13) Moment is a free vector (rem, cfm)
- [ ] 14) Balken (ad, sk)

#### Supplementary course / Ergänzungskurs Technical Mechanics:
- [x] 1) Damped oscillator / Federpendel (eb, qa, ft)
- [x] 2) Pendulum / Schwerependel (eb, ft)
- [ ] 3) Base-excited oscillator / Fusspunkterregter Schwinger (eb, kb)
- [ ] 4) Tuned mass damper / Schwingungstilger (eb, rd)
- [ ] 5) Instant centre of rotation / Momentanpol der Leiter (Leiter) (ak, vu)
- [x] 6) Coriolis force/Drehscheibe-Corioliskraft (eb,ag)
- [x] 7) Boat with three swimmers / Boot mit drei Schwimmern (ma,ag)
- [x] 8) Collision / Stoss (ma,ag)
- [ ] 9) Rollercoaster (eb)
- [x] 10) Stopping distances (eb)
- [x] 11) Projectiles / Wurfgeschoss (eb)
- [ ] 12) Rolling Condition / Abrollbedingungen (eb)
- [x] 13) Rolling test / Rollversuch (eb, me)
- [ ] 14) Instant centre of rotation of the cupoler / Momentanpol der Koppel ()
- [ ] 15) Drop tube / Fallturm ()
- [ ] 16) Low-pressure area / Tiefdruck (ma)
- [ ] 17) Angular momentum / Drallerhaltung (ma, cfm)


#### Structural Dynamics:
- [ ] 1) Euler-Bernoulli Vibrations with analytical solutions (me)
- [ ] 2) 2D cantilever beam (ma, cfm, sk)
- [x] 3) Seismic three DOF structure (ma)
- [ ] 4) Shock Response Spectra (rem)
- [ ] 5) Dynamic seismic three DOF structure (mb, ft)

#### Technical Acoustics II:
- [x] 1) Diffraction (br)
- [x] 2) Vibroacoustic plates (rd)

#### Integral transform method:
- [x] 1) Sampling (br, me)
- [ ] 2) Wavelet-Transform (kb)

### Supervisors
- Francesca Taddei (ft), [@FrancescaTaddei](https://github.com/FrancescaTaddei)
- Quirin Aumann (qa), [@qaumann](https://github.com/qaumann)
- Moritz Becker (mb)
- Julian Freisinger (jf)
- Matthias Miksch (mm)
- Franziska Weber (fw)
- Hannes Englert (he)
- Corinna Schmausser (cs)
- Felix Schneider (fs)

### Developers

Please comply with the [Development Guideline](https://github.com/ChairOfStructuralMechanicsTUM/Mechanics_Apps/wiki/Development-Guidelines)
- Matthias Ebert, me, [@m3bert](https://github.com/m3bert)
- Qiaozhi Gao, qg, [@QiaozhiGao](https://github.com/QiaozhiGao)
- Martin Hefel, mh, [@MartinHefel](https://github.com/MartinHefel)
- Viola Li, vl, [@ViolaM151](https://github.com/ViolaM151)

### Former developers

- Emily Bourne, eb
- Moustafa Alsayed Ahmad, ma
- Abraham Duplaa, ad
- Benjamin Rüth, br
- Ravil Dorozhinskii, rd
- Vyshakh Unnikrishnan, vu
- Carmen Font Mata, cfm 
- Khaled Boulbrachene, kb
- Rishith Ellath Meethal, rem
- Irfan Haider, ih
- Sascha Kubisch, sk, [@ga96wec](https://github.com/ga96wec)
