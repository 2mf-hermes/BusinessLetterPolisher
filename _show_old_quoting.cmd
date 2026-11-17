@echo off
rem Proof of the old, broken template: the quotes were stored inside the variable,
rem so every later "%VAR%\file" expansion produced ""F:\Program Files (Portable)\...
set TARGET="F:\Program Files (Portable)\BusinessLetterPolisher"
echo [old] robocopy command cmd would run:
echo [old]   robocopy "%SOURCE%" "%TARGET%"
echo [old] start command cmd would run:
echo [old]   start "" "%TARGET%\app.exe"
set "FIXED=F:\Program Files (Portable)\BusinessLetterPolisher"
echo [new] start command cmd would run:
echo [new]   start "" "%FIXED%\app.exe"
