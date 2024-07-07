#!/bin/sh

# generate the just.rst and modules.rst files
sphinx-apidoc -o docs/ src/just/

pushd docs/
    # Using the .bat file on Windows
    ./make.bat html
popd
