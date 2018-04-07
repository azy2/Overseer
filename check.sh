#!/bin/bash

function usage() {
    echo 'Usage ./check.sh [-p|pylint] [-u|unittests] [-s|selenium] [-a|all]'
    return 0
}

function run_pylint() {
    echo '========================= pylint ========================='
    pylint --rcfile=./pylintrc ovs
    return $?
}

function run_unittests() {
    echo '======================== unittests ========================'
    nose2 -s ovs/tests/unittests/services/test_mail_service.py
    return $?
}

function run_selenium() {
    echo '======================== selenium ========================='
    PATH=.:$PATH nose2 -s ovs/tests/selenium
    return $?
}

if [ $# == 0 ]; then
    usage
fi

while [ "$1" != "" ]; do
    case $1 in
        -u|unittests)
            run_unittests
            exit $?
            ;;
        -p|pylint)
            run_pylint
            exit $?
            ;;
        -s|selenium)
            run_selenium
            exit $?
            ;;
        -a|all)
            run_pylint &&
            run_unittests &&
            run_selenium
            exit $?
            ;;
        *)
            usage
    esac
    shift
done

