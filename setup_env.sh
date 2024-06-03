#!/bin/bash

# Check if pyenv is installed
if ! command -v pyenv &> /dev/null; then
    echo "Pyenv not found, installing..."
    curl https://pyenv.run | bash

    # Add pyenv to the path and initialize
    export PATH="$HOME/.pyenv/bin:$PATH"
    eval "$(pyenv init --path)"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
fi

#Set the python version for the use
PYTHON_VERSION=3.10.13

#Install specific version if not already installed
if ! pyenv version | grep -q $PYTHON_VERSION; then
    pyenv install $PYTHON_VERSION
fi 

#Set the local Python version for the project
pyenv local $PYTHON_VERSION

#Create virtual environment
python3 -m venv stocks

#Activate virtual environment
source stocks/bin/activate

#upgrade setuptools and pip
pip install --upgrade setuptools pip

#prerequest for packages
pip install wheel build

#install packages from the requirements.txt
pip install -r requirements.txt

