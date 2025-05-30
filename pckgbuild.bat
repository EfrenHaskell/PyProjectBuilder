@echo off
set FILEPATH=%1
if exist %FILEPATH% (
	echo using package spec %FILEPATH%
) else (
	if "%FILEPATH%"=="" (
        	echo run command with: pckgbuild.bat [filename]
	) else (
		echo %FILEPATH% is not a valid path
	)
	exit /b 0
)


set "PARENTDIR=."

setlocal enabledelayedexpansion
for /f "usebackq delims=" %%A in ("%FILEPATH%") do (
	set "LINE=%%A"
	call :ExecAction "!LINE!" %PARENTDIR%
)

endlocal


:ExecAction
set "ACTION=%~1"
set "DIR=%2"
echo dir %DIR%
echo "%ACTION%"
if "%ACTION%"=="->" (
	echo forward dir
	cd %DIR%
) else if "%ACTION%"=="<-" (
	echo back dir
        cd ..
) else (
	call (
		for /f "tokens=1,2 delims= " %%A in ("%ACTION%") do (
			if "%%A"=="dir" (
				echo %%B
				set "PARENTDIR=%%B"
			) else (
				echo %%A
			)
		)
	)
)
exit /b 0

