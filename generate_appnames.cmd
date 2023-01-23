echo "Remove old file..."
del appnames.conf
echo "Create list of folders in Apps\* , exclude Apps\shared..."
dir "Apps" /B | findstr /v /i "shared" > tmp.conf
echo "Add prefix Apps\... for all apps in list..."
for /f "tokens=*" %%a in (tmp.conf) do (echo Apps\%%a) >> appnames.conf
echo "Clean up temporary file..."
del tmp.conf