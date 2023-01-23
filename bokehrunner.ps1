#start the standard bokeh server
$ip = "apps.dev.bm.ed.tum.de"
$port = 443
Write-Host -ForegroundColor Yellow "STARTING BOKEH SERVER"
Write-Host -ForegroundColor Yellow "type ${ip}:${port} in your browser to visit it!"
Write-Host -ForegroundColor Yellow ""
Write-Host -ForegroundColor Yellow "*****configuration*****************************"
Write-Host -ForegroundColor Yellow "**** global ip: $ip"
Write-Host -ForegroundColor Yellow "**** bokeh port: $port"
Write-Host -ForegroundColor Yellow "***********************************************"

#generate appnames.conf by running `generate_appnames.cmd` via cmd
#remove Apps/shared from this list
$apps = Get-Content -Path appnames.conf

# There are two different options, uncomment one of the two lines below.
# Use SSL (served at https://${ip}:${port})
Start-Process bokeh -ArgumentList "serve $apps --port $port --allow-websocket-origin=${ip} --ssl-certfile .\fullchain.pem --ssl-keyfile .\privkey.pem"  -NoNewWindow
# Don't use SSL (served at http://${ip}:${port})
#Start-Process bokeh -ArgumentList "serve $apps --port $port --allow-websocket-origin=${ip}" -NoNewWindow