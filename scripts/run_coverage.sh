#!/bin/sh

# run coverage report
# must be run after `pip install -e .`, otherwise will report "CoverageWarning: No data was collected"

# paths
src_dir='src/'
tests_dir='tests/'

# use "-v" to run coverage in verbose mode
if [ "$1" = "-v" ]; then
    verbose="-v"
else
    verbose=""
fi

pytest \
    --cov-report term-missing \
    --cov="$src_dir" \
    "$tests_dir"

# show coverage report
coverage report -m
