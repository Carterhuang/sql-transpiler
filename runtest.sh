#!/bin/sh

python -m unittest transpile_test generate_sql_regression_test

rm ./*.pyc
