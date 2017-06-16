python AppOverviewPage/twisted_server.py --bokeh-port 5006 --bokeh-port-testing 5100 --input-port 8080 --global-ip 127.0.0.1 &
apps=`cat appnames.conf`
appstest=`cat appnames_testing.conf`
bokeh serve $apps --port 5006 --host=127.0.0.1:5006 --allow-websocket-origin=127.0.0.1:8080 &
bokeh serve $appstest --port 5100 --host=127.0.0.1:5100 --allow-websocket-origin=127.0.0.1:8080 &
xdg-open "http://127.0.0.1:8080"