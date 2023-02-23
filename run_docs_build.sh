#!/bin/sh

sphinx-apidoc -o docs/ just/

pushd docs/

./make.bat html

popd
