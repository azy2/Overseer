#!/bin/bash

function usage() {
    echo 'Usage ./check.sh [-p|pylint] [-u|unittests] [-s|selenium] [-a|all]'
}

function run_pylint() {
    echo '========================= pylint ========================='
    pylint --rcfile=./pylintrc ovs
}

function run_unittests() {
    echo '======================== unittests ========================'
    nose2 -s ovs/tests/unittests
}

function run_selenium() {
    echo '======================== selenium ========================='
    PATH=.:$PATH nose2 -s ovs/tests/selenium
}

if [ $# == 0 ]; then
    usage
fi

while [ "$1" != "" ]; do
    case $1 in
        -u|unittests)
            run_unittests
            ;;
        -p|pylint)
            run_pylint
            ;;
        -s|selenium)
            run_selenium
            ;;
        -a|all)
            run_pylint
            run_unittests
            run_selenium
            ;;
        *)
            usage
    esac
    shift
done
