@echo off
set Address=utahbroadband.com
set LogDir=C:\pingtest
set /a i=1

REM create unique file name
For /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
For /f "tokens=1-3 delims=/:/ " %%a in ('time /t') do (set mytime=%%a-%%b-%%c)
set fileName="%mydate%_%mytime%.log"
set fileName=%fileName: =% 

REM create directory and open in explorer
md %LogDir%
%SystemRoot%\explorer.exe "%LogDir%"

REM Run initial trace route
echo PingTest script to monitor network connection.  Control-C to exit.
echo Tests connection by pinging %Address%.  Logs to %LogDir%\%fileName%.
echo %date% %time% Initial tracert (trace route) to %Address% >> %LogDir%\%fileName%
tracert %Address% >> %LogDir%\%fileName%
echo Begin pinging %Address% >> %LogDir%\%fileName%
:Loop
REM about 2 second delay
PING -n 3 -w 1 127.0.0.1>nul
echo %SystemRoot%\system32\ping.exe -n 1 -l 8 %Address% | %SystemRoot%\system32\find.exe "TTL=" > NUL
if %ERRORLEVEL% EQU 0 goto :Loop
REM ICMP echo request timed-out
echo %date% %time% PING ERROR %i%
echo %date% %time% PING ERROR %i% >> %LogDir%\%fileName%
tracert -d %Address% >> %LogDir%\%fileName%
set /a i+=1
goto Loop