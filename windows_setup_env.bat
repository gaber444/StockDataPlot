@echo off
setlocal

:: Check if pyenv is installed
where pyenv >nul 2>&1
if %errorlevel% neq 0 (
    echo Pyenv not found, installing...
    powershell -Command "Invoke-WebRequest -Uri https://pyenv.run | Invoke-Expression"
    setx PATH "%USERPROFILE%\.pyenv\pyenv-win\bin;%USERPROFILE%\.pyenv\pyenv-win\shims;%PATH%"
)

:: Set the Python version
set "PYTHON_VERSION=3.10.13"

:: Check if the specific Python version is installed
pyenv versions | findstr /C:"%PYTHON_VERSION%" >nul
if %errorlevel% neq 0 (
    pyenv install %PYTHON_VERSION%
)

:: Set the local Python version for the project
pyenv local %PYTHON_VERSION%

:: Create virtual environment
python -m venv stocks

:: Activate virtual environment
call stocks\Scripts\activate

:: Upgrade setuptools and pip
pip install --upgrade setuptools pip

:: Prerequisites for packages
pip install wheel build

:: Install packages from requirements.txt
pip install -r requirements.txt

endlocal
