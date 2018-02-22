#!/bin/bash

now=$(date +"%Y%m%d_%H%M")
mkdir "migrations/V"$now"__"$1".py"