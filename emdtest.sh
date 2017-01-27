#!/bin/sh
echo 'mfcc13'
python test_emd.py 13 16
echo '\nmfcc20'
python test_emd.py 20 30
echo '\nmfcc30'
python test_emd.py 30 50
