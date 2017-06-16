mapfile -t <server.conf # read configuration from file

GlobalIP="$(echo ${MAPFILE[0]%%#*} | xargs)" # remove everything after '#', then remove trailing whitespace with xargs
InputPort="$(echo ${MAPFILE[1]%%#*} | xargs)"
BokehPortTesting="$(echo ${MAPFILE[3]%%#*} | xargs)"

echo "STARTING BOKEH SERVER"
echo "type "$GlobalIP":"$BokehPortTesting" in your browser to visit the testing server!"
echo ""
echo "configuration:"
echo "GlobalIP "$GlobalIP
echo "BokehPortTesting "$BokehPortTesting
echo ""

WebsocketOrigin="$GlobalIP:$InputPort"
apps_testing=`cat appnames_testing.conf`

bokeh serve $apps_testing --port $BokehPortTesting --host=$GlobalIP:$BokehPortTesting --allow-websocket-origin=$WebsocketOrigin

