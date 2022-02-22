#!/bin/bash

if [ $1 == "--help" ] || [ $1 == "-h" ]
then
  echo "Please provide at least one folder path to reduce!"
else
  python run_reduction.py $@
fi
