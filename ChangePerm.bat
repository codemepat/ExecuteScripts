@echo off
for /f "tokens=*" %%i in (listfiles.txt) do icacls "%%i" /grant Users:(OI)(CI)R


