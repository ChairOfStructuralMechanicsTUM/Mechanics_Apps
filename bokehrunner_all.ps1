#start the standard bokeh server
$ip = "apps.bm.ed.tum.de"
$port = 443
Write-Host -ForegroundColor Yellow "STARTING BOKEH SERVER"
Write-Host -ForegroundColor Yellow "type ${ip}:${port} in your browser to visit it!"
Write-Host -ForegroundColor Yellow ""
Write-Host -ForegroundColor Yellow "*****configuration*****************************"
Write-Host -ForegroundColor Yellow "**** global ip: $ip"
Write-Host -ForegroundColor Yellow "**** bokeh port: $port"
Write-Host -ForegroundColor Yellow "***********************************************"

#generate appnames _all.conf by running `dir * /AD /B > appnames_all.conf` via cmd
#manually remove the following folders: .git AppOverviewPage shared
#manually add all folders from appnames_math.conf
$apps = Get-Content -Path appnames_all.conf

# There are two different options, uncomment one of the two lines below.
# Use SSL (served at https://${ip}:${port})
Start-Process bokeh -ArgumentList "serve $apps --port $port --allow-websocket-origin=${ip} --ssl-certfile C:\Mechanics_Apps\fullchain.pem --ssl-keyfile C:\Mechanics_Apps\privkey.pem"  -NoNewWindow 
# Don't use SSL (served at http://${ip}:${port})
#Start-Process bokeh -ArgumentList "serve $apps --port $port --allow-websocket-origin=${ip}" -NoNewWindow 