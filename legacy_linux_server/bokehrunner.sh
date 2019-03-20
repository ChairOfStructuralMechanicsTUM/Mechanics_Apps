mapfile -t <server.conf # read configuration from file

GlobalIP="$(echo ${MAPFILE[0]%%#*} | xargs)" # remove everything after '#', then remove trailing whitespace with xargs
BokehPort="$(echo ${MAPFILE[2]%%#*} | xargs)"

echo "STARTING BOKEH SERVER"
echo "type "$GlobalIP":"$BokehPort" in your browser to visit it!"
echo ""
echo "configuration:"
echo "GlobalIP "$GlobalIP
echo "BokehPort "$BokehPort
echo ""

WebsocketOrigin="$GlobalIP:$BokehPort"
apps=`cat appnames.conf`

bokeh serve $apps --port $BokehPort --allow-websocket-origin=$WebsocketOrigin

