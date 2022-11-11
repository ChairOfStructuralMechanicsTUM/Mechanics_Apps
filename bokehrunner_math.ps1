#start the standard bokeh server
$mapfile = Get-Content -Path server.conf
$mapfile = $mapfile.Split("#")
$ip = $mapfile[0].Trim()
$port = $mapfile[8].Trim()
Write-Host -ForegroundColor Yellow "STARTING BOKEH SERVER MATH"
Write-Host -ForegroundColor Yellow "type ${ip}:${port} in your browser to visit it!"
Write-Host -ForegroundColor Yellow ""
Write-Host -ForegroundColor Yellow "*****configuration*****************************"
Write-Host -ForegroundColor Yellow "**** global ip: $ip"
Write-Host -ForegroundColor Yellow "**** bokeh port: $port"
Write-Host -ForegroundColor Yellow "***********************************************"

$apps = Get-Content -Path appnames_math.conf

# There are two different options, uncomment one of the two lines below.
# Use SSL (served at https://${ip}:${port})
Start-Process bokeh -ArgumentList "serve $apps --port $port --allow-websocket-origin=${ip}:${port} --ssl-certfile C:\Mechanics_Apps\fullchain.pem --ssl-keyfile C:\Mechanics_Apps\privkey.pem" -NoNewWindow 
# Don't use SSL (served at http://${ip}:${port})
#Start-Process bokeh -ArgumentList "serve $apps --port $port --allow-websocket-origin=${ip}:${port}" -NoNewWindow 