python AppOverviewPage/twisted_server.py --bokeh-port 5006 --input-port 80 --global-ip 127.0.0.1 &
apps=`cat appnames.conf`
bokeh serve $apps --port 5006 --host=127.0.0.1:5006 --allow-websocket-origin=127.0.0.1:80 &
xdg-open "http://127.0.0.1"