#!/bin/sh

venv_name=".venv"
venv_path=$PWD/$venv_name
activate_path=$venv_path/Scripts/activate
alias python='py.exe'

if [ -e $venv_path ]; then
    >&2 echo "$venv_path already exists! aborting..."
    exit -1
fi

python -m venv $venv_path
source $activate_path
pip install --upgrade pip setuptools

pip install .
