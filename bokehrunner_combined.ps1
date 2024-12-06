#creating logfile to save the errors occuring in the ps while testing new developments
# Start-Transcript -Path "C:\Users\ga53fiz\Desktop\Mechanics_Apps\logfile.txt"

# initializing conda directly
& "C:\Users\ga53fiz\Anaconda3\shell\condabin\conda-hook.ps1"
conda activate base


#first starting old Apps then staring new Apps in diffrent environment
#one IP-adress for both ports
$ip = "apps.bm.ed.tum.de"
$port_old = 443
$port_new = 8443  # Neuer Port für die neue Umgebung
$env_newApps = "MechanicApps_updated"  # Name der neuen Umgebung
$env_oldApps = "MechanicApps"  # Name der alten Umgebung

Write-Host -ForegroundColor Yellow "STARTING BOKEH SERVERS"
Write-Host -ForegroundColor Yellow "type ${ip}:${port_old} for old apps and ${ip}:${port_new} for new apps"
Write-Host -ForegroundColor Yellow "************************************************"

#Start old Apps
Write-Host -ForegroundColor Yellow "STARTING THE OLD APPS"
Write-Host -ForegroundColor Yellow "type ${ip}:${port_old} in your browser to visit it!"
Write-Host -ForegroundColor Yellow ""
Write-Host -ForegroundColor Yellow "*****configuration*****************************"
Write-Host -ForegroundColor Yellow "**** global ip: $ip"
Write-Host -ForegroundColor Yellow "**** bokeh port: $port_old"
Write-Host -ForegroundColor Yellow "***********************************************"

#names of apps
Write-Host -ForegroundColor Yellow "The appnames getting loaded"
$apps_old = Get-Content -Path appnames_old.conf
$apps_new = Get-Content -Path appnames_new.conf
Write-Host -ForegroundColor Yellow "The appnames loading was sucessfull"

# Start the old Bokeh server (NO SSL)
Write-Host -ForegroundColor Yellow "The old environment is activated"
# & conda activate $env_oldApps
# &conda activate base
Write-Host -ForegroundColor Yellow "Activation old env was sucessfull"
Start-Process bokeh -ArgumentList "serve $apps_old --port $port_old --allow-websocket-origin=${ip} --ssl-certfile .\fullchain.pem --ssl-keyfile .\privkey.pem"  -NoNewWindow
& conda deactivate
#Start new Apps
Write-Host -ForegroundColor Yellow "STARTING THE NEW APPS"
Write-Host -ForegroundColor Yellow "type ${ip}:${port_old} in your browser to visit it!"
Write-Host -ForegroundColor Yellow ""
Write-Host -ForegroundColor Yellow "*****configuration*****************************"
Write-Host -ForegroundColor Yellow "**** global ip: $ip"
Write-Host -ForegroundColor Yellow "**** bokeh port: $port_new"
Write-Host -ForegroundColor Yellow "***********************************************"

# Activate the new environment and start the new Bokeh server (with SSL)
Write-Host -ForegroundColor Yellow "The new environment is activated"
# & conda env list
& conda activate $env_newApps

Start-Process bokeh -ArgumentList "serve $apps_new --port $port_new --allow-websocket-origin=${ip}:8443 --ssl-certfile .\fullchain.pem --ssl-keyfile .\privkey.pem" -NoNewWindow

# Starting the env try2.0
# Write-Host -ForegroundColor Yellow "The new environment is activated"
# conda run -n $env_newApps bokeh serve $apps_new --port $port_new --allow-websocket-origin=${ip}:8443 --ssl-certfile .\fullchain.pem --ssl-keyfile .\privkey.pem

# Stoping the transcript of errors in the powershell
# Stop-Transcript