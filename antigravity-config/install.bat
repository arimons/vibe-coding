@echo off
chcp 65001 > nul
set "SCRIPT_DIR=%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -Command "[Console]::OutputEncoding = [Console]::InputEncoding = [System.Text.Encoding]::UTF8; Invoke-Expression (Get-Content -LiteralPath '%~dp0install.ps1' -Raw -Encoding UTF8)"
pause
