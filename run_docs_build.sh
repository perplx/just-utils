#!/bin/sh

# generate the just.rst and modules.rst files
sphinx-apidoc -o docs/ just/

pushd docs/
    # Using the .bat file on Windows
    ./make.bat html
popd
