mapfile -t <server.conf # read configuration from file

GlobalIP="$(echo ${MAPFILE[0]%%#*} | xargs)" # remove everything after '#', then remove trailing whitespace with xargs
InputPort="$(echo ${MAPFILE[1]%%#*} | xargs)"
BokehPort="$(echo ${MAPFILE[2]%%#*} | xargs)"
BokehPortTesting="$(echo ${MAPFILE[3]%%#*} | xargs)"

echo "STARTING WEB SERVER"
echo "type "$GlobalIP":"$InputPort" in your browser to visit it!"
echo ""
echo "configuration:"
echo "GlobalIP "$GlobalIP
echo "WebServerPort "$InputPort
echo "BokehPort "$BokehPort
echo "BokehPortTesting "$BokehPortTesting
echo ""

python AppOverviewPage/twisted_server.py --bokeh-port $BokehPort --bokeh-port-testing $BokehPortTesting --input-port $InputPort --global-ip $GlobalIP
