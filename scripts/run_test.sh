#!/bin/bash

# This is a very simple proof of concept
# $1 is the base directory where the tests are
# $2 is the test to run
# I'm not doing any kind of checking

set +e
set +x

TEST_DIR=$1
TEST=$2
export LC_ALL="en"

pushd $TEST_DIR

if [ ! -d $TEST_DIR/.venv ]; then
    echo "Creating virtualenv"
    virtualenv $TEST_DIR/.venv
    source $TEST_DIR/.venv/bin/activate
else
    echo "Virtualenv exists, activating"
    source $TEST_DIR/.venv/bin/activate
fi

sleep 10

if [ -f requirements.txt ]; then
    echo "requirements file found, running pip"
    pip install -r $TEST_DIR/requirements.txt
fi

sleep 10

if [ -f test-requirements.txt ]; then
    echo "test-requirements file found, running pip"
    pip install -r $TEST_DIR/test-requirements.txt
fi

echo "Running test now"
python -m unittest $TEST
