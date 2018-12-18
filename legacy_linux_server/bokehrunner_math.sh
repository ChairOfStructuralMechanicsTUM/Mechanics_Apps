mapfile -t <server.conf # read configuration from file

GlobalIP="$(echo ${MAPFILE[0]%%#*} | xargs)" # remove everything after '#', then remove trailing whitespace with xargs
BokehPortMath="$(echo ${MAPFILE[4]%%#*} | xargs)"

echo "STARTING BOKEH SERVER"
echo "type "$GlobalIP":"$BokehPortMath" in your browser to visit it!"
echo ""
echo "configuration:"
echo "GlobalIP "$GlobalIP
echo "BokehPort "$BokehPortMath
echo ""

WebsocketOrigin="$GlobalIP:$BokehPortMath"
apps=`cat appnames_math.conf`

bokeh serve $apps --port $BokehPortMath --allow-websocket-origin=$WebsocketOrigin

