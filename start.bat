@echo off
rem Open the site offline (no internet needed). Serves the built site on http://localhost:4321 with Python 3.
chcp 65001 >nul
cd /d "%~dp0"
set "DIR="
if exist "dist\index.html" set "DIR=dist"
if not defined DIR if exist "index.html" set "DIR=."
if not defined DIR (
  echo No built site found: run "npm install" and "npm run build" first.
  pause
  exit /b 1
)
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (where python >nul 2>nul && set "PY=python")
if not defined PY (
  echo Python 3 is required: https://www.python.org/downloads/
  pause
  exit /b 1
)
set "PORT=4321"
echo AI-Learning: http://localhost:%PORT%/
echo Close this window to stop.
start "" cmd /c "timeout /t 2 >nul & start http://localhost:%PORT%/"
%PY% -m http.server %PORT% --bind 127.0.0.1 --directory "%DIR%"
