GlobalIP=127.0.0.1
BokehPort=3100
IncomingPort=80
bokeh serve Diffraktion Zugversuch Querdehnung Rollercoaster Drehscheibe-Corioliskraft --port $BokehPort --host $GlobalIP:$BokehPort --allow-websocket-origin=$GlobalIP &
sudo python twisted_server.py
