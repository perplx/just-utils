#!/bin/sh

# remove docs/ build output files
pushd 'docs/'
    rm -i just.rst
    rm -i modules.rst
    rm -irf _build/
popd
