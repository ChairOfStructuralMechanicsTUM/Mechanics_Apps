#start the standard bokeh server
$mapfile = Get-Content -Path server.conf
$mapfile = $mapfile.Split("#")
$ip = $mapfile[0].Trim()
$port = $mapfile[6].Trim()
Write-Host -ForegroundColor Yellow "STARTING BOKEH SERVER TESTING"
Write-Host -ForegroundColor Yellow "type ${ip}:${port} in your browser to visit it!"
Write-Host -ForegroundColor Yellow ""
Write-Host -ForegroundColor Yellow "*****configuration*****************************"
Write-Host -ForegroundColor Yellow "**** global ip: $ip"
Write-Host -ForegroundColor Yellow "**** bokeh port: $port"
Write-Host -ForegroundColor Yellow "***********************************************"

$apps = Get-Content -Path appnames_testing.conf

Start-Process bokeh -ArgumentList "serve $apps --port $port --allow-websocket-origin=${ip}:${port}" -NoNewWindow