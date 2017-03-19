mapfile -t <server.conf # read configuration from file

GlobalIP="$(echo ${MAPFILE[0]%%#*} | xargs)" # remove everything after '#', then remove trailing whitespace with xargs
InputPort="$(echo ${MAPFILE[1]%%#*} | xargs)"
BokehPort="$(echo ${MAPFILE[2]%%#*} | xargs)"

echo "STARTING WEB SERVER"
echo "type "$GlobalIP":"$InputPort" in your browser to visit it!"
echo ""
echo "configuration:"
echo "GlobalIP "$GlobalIP
echo "WebServerPort "$InputPort
echo "BokehServerPort "$BokehPort
echo ""


python twisted_server.py --bokeh-port $BokehPort --input-port $InputPort --global-ip $GlobalIP
