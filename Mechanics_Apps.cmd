start "webserver" python AppOverviewPage/twisted_server.py --bokeh-port 5006 --bokeh-port-testing 5100 --input-port 8080 --global-ip 127.0.0.1"
set /p apps=<appnames.conf
set /p appstest=<appnames_testing.conf
start "bokehserver" bokeh serve %apps% --port 5006 --host=127.0.0.1:5006 --allow-websocket-origin=127.0.0.1:8080
start "bokehserver" bokeh serve %appstest% --port 5100 --host=127.0.0.1:5100 --allow-websocket-origin=127.0.0.1:8080
start http://127.0.0.1:8080