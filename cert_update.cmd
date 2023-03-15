# Copy this file and rename it to cert_update.cmd; then change the path to the Bokeh apps according to your setup
cd C:\Users\ga53fiz\Desktop\Mechanics_Apps

Remove-Item C:\Users\ga53fiz\Desktop\Mechanics_Apps\fullchain.pem
Remove_Item C:\Users\ga53fiz\Desktop\Mechanics_Apps\privkey.pem

Copy-Item "C:\Certbot\live\apps.dev.bm.ed.tum.de\fullchain.pem" -Destination "C:\Users\ga53fiz\Desktop\Mechanics_Apps"
Copy-Item "C:\Certbot\live\apps.dev.bm.ed.tum.de\privkey.pem" -Destination "C:\Users\ga53fiz\Desktop\Mechanics_Apps"

#$env:Certbot_Path +='\fullchain.pem'
#xcopy $env:Certbot_Path C:\Users\ga53fiz\Desktop\Mechanics_Apps /y

#$env:Certbot_Path +='\privkey.pem'
#xcopy $env:Certbot_Path C:\Users\ga53fiz\Desktop\Mechanics_Apps /y



#fürcmd
#del C:\Users\ga53fiz\Desktop\Mechanics_Apps\fullchain.pem
#del C:\Users\ga53fiz\Desktop\Mechanics_Apps\privkey.pem
#xcopy %Certbot_Path%\fullchain.pem C:\Users\ga53fiz\Desktop\Mechanics_Apps /y

#xcopy C:\Certbot\live\apps.dev.bm.ed.tum.de\fullchain.pem C:\Users\ga53fiz\Desktop\Mechanics_Apps
#xcopy C:\Certbot\live\apps.dev.bm.ed.tum.de\privkey.pem C:\Users\ga53fiz\Desktop\Mechanics_Apps