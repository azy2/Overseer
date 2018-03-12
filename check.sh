#!/usr/bin/env bash

pylint --rcfile=./pylintrc ovs
nose2
