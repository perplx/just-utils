#!/bin/sh

pushd docs/_build/html

python -m http.server 8080

popd
