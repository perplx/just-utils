#!/bin/sh

# use "-v" to run coverage in verbose mode
if [ "$1" = "-v" ]; then
    verbose="-v"
else
    verbose=""
fi

# use coverage to run pytest and pytest-cov
coverage run \
    --source=just/ \
    --module pytest \
    $verbose \
    tests/

# show coverage report
coverage report -m
