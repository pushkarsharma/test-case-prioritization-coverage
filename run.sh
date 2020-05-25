#!/bin/bash

pwd=$(pwd)
sed -i 's|_PROJECT_DIR_|'$pwd'|g' shell/*
sed -i 's|_PROJECT_DIR_|'$pwd'|g' processing/*

shell/compile-generator.sh
processing/parser.py
processing/selector.py
shell/test-suite-evaluator.sh
shell/output-comparator.sh