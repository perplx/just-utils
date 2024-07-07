#!/bin/sh

src_dir='src/'
tests_dir='tests/'

# use "-v" to run coverage in verbose mode
if [ "$1" = "-v" ]; then
    verbose="-v"
else
    verbose=""
fi

# use coverage to run pytest and pytest-cov
coverage run \
    --source="$src_dir" \
    --module pytest \
    $verbose \
    "$tests_dir"


# show coverage report
coverage report -m
