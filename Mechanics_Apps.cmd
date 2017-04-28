start "webserver" python AppOverviewPage/twisted_server.py --bokeh-port 5006 --input-port 80 --global-ip 127.0.0.1"
set /p apps=<appnames.conf
start "bokehserver" bokeh serve %apps% --port 5006 --host=127.0.0.1:5006 --allow-websocket-origin=127.0.0.1:80
start http://127.0.0.1