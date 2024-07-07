#!/bin/sh

# Run a local web-server for the docs html output directory.

server_port='8080'

pushd 'docs/_build/html/'

    python -m http.server $server_port

popd
