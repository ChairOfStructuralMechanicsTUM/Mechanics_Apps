# Mechanics Apps
Webbased visualization for mechanics content via Bokeh
This Repository contains different prototypes for WebApps for the visualization of mechanics example for the lectures of the Chair of Strcutrual Mechnaics, Prof. Mï¿½ller, TUM (Technische Universitï¿½t Mï¿½nchen).

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
- [x] 1) Tensile testing/Zugversuch (eb)
- [x] 2) Transverse strain/Querdehnung (eb)
- [ ] 3) Doble-supported beam with point load/Balken (ad)
- [ ] 4) Maxwell's reciprocity theorem/Reziprozitätssatz von Maxwell (ad)
- [ ] 5) Buckling/Knickung (ad)
- [ ] 6) Seilbahn/Funicular (br)
- [ ] 7) Polares Flächenträgheitmoments/Polar moment of inertia ()
- [ ] 8) Zusammenges. Flächenträgheitmoments/ Combined moment of inertia ()
- [ ] 9) Zusammenges. Schwerpunktsmoment/Combined center of mass moment

#### Supplementary course/Ergï¿½nzungskurs Technical mechanics (ft):
- [ ] 1) Spring pendulum/Federpendel (eb)
- [ ] 2) Pendulum/Schwerependel (eb)
- [ ] 3) Base-excited oscillator/Fusspunkterregter Schwinger (eb)
- [ ] 4) Tuned mass damper/Schwingungstilger (eb)
- [ ] 5) Instant centre of rotation/Momentanpol der Leiter (Leiter) (ak)
- [x] 6) Coriolis force/Drehscheibe-Corioliskraft (eb)
- [ ] 7) Boat with three swimmers/Boot mit drei Schwimmern (ma)
- [ ] 8) Collision/Stoss (ma)
- [x] 9) Rollercoaster (eb)
- [x] 10)Stopping distances (eb)
- [x] 11) Wurfgeschoss/Projectiles (eb)
- [ ] 12) Abrollbedingungen/Rolling Condition 
- [ ] 13) Rollversuch/Rolling test ()

#### Structural dynamics (cs):
- [ ] 1) Euler-Bernoulli Vibrations with analytical solutions (ak)
- [ ] 2) FEM Example (ma)
- [ ] 3) Seismic example (ak)

#### Technical Acoustics II (ag):
- [x] 1) Diffraction (br)

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
- Banjamin Rüth br
