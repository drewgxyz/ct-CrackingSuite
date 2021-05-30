@echo off
WEVTUTIL EL > .\LOGLIST.TXT
wevtutil cl Application
for /f %%a in ( .\LOGLIST.TXT ) do WEVTUTIL CL "%%a"
del .\LOGLIST.TXT
timeout 15
:noAdmin
echo You must run this script as an Administrator!
echo.
:theEnd