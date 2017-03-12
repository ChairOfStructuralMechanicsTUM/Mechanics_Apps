# Server Architecture

We provide access to the apps through a bokeh server in directory format (see http://bokeh.pydata.org/en/latest/docs/user_guide/server.html#directory-format). Our overview website is hosted by a nginx server which forwards requests to the bokeh server.

The server can be run in two modes:

* [x] online mode: provide access to apps through the internet.
* [ ] offline mode: run the server locally and present apps to
lecture audience.

## ToDos

- [x] works on Linux?
- [ ] works on Windows?
- [ ] works on MacOS?
- [ ] create installer scripts automatically performing setup (lecturers can easily install framework on their machines)
- [ ] test setup online mode on webserver

## Contents

Here we provide the necessary components for the server that is used for providing access to our mechanic apps.

* ```Mechanic_Apps/server/data``` static data. Html pages, images, ```.css``` stylesheets or ```.js``` libraries.
* ```Mechanic_Apps/server/nginx``` server configuration. Configuration file for Nginx server.

## Setup

1. please install the following on your computer:
    * Anaconda with python version 2.7: https://www.continuum.io/downloads
    * Bokeh: ```conda install bokeh```
    * Nodejs: ```conda install -c bokeh nodejs```
    * Flexx: ```conda install -c bokeh flexx```
    * nginx: ```sudo apt-get install nginx-full```
2. copy ```Mechanic_Apps/server/data``` to your file system root ```sudo cp Mechanic_Apps/server/data /```.
3. setup the nginx server
    * replace the nginx configuration file ```nginx.conf``` (usually in ```/etc/nginx/```) with ```Mechanic_Apps/server/nginx/nginx.conf```
    * start the server ```$ sudo nginx```, if the server is already running, reload the configuration file ```$ sudo nginx -s reload$.```
    * test the server by opening ```127.0.0.1``` in your browser
4. start bokeh apps with ```Mechanic_Apps/apprunner.sh```. The script wraps the following command: ```$ bokeh serve <APPNAME> --prefix=apps/ --port 5100 --host 127.0.0.1:80```
    * ```<APPNAME>``` applications to be run, given in directory-format. We start the app by defining the directiry name here (e.g. Diffraktion).
    * ```--port 5100``` defines the port. Bokeh server runs on port ```5100```
    * ```--host 127.0.0.1:80``` defines the whitelist for incoming requests. User requests applications from port 80, nginx forwards the requests to the bokeh server on port 5100.

## Alternative: Twisted

pure python!

* install twisted ```conda install twisted```
