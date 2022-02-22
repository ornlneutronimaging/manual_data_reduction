#!/bin/bash

if [ $1 == "--help" ] || [ $1 == "-h" ]
then
  echo "Please provide at least one folder path to reduce!"
else
   source /opt/anaconda/bin/activate /opt/anaconda/envs/ImagingReduction 
   python /SNS/users/j35/git/manual_data_reduction/run_reduction.py $@
fi
