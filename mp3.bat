@echo off
:: %~dp0 refers to the directory where this .bat file is located
:: This allows the script to run from anywhere without hardcoding paths
python "%~dp0main.py" %*