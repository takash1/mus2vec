#!/bin/sh
echo 'mfcc13 ae100'
python test_m2v.py 13 100
echo '\nmfcc13 ae300'
python test_m2v.py 13 300
echo '\nmfcc13 ae500'
python test_m2v.py 13 500
echo '\nmfcc20 ae100'
python test_m2v.py 20 100
echo '\nmfcc20 ae300'
python test_m2v.py 20 300
echo '\nmfcc20 ae500'
python test_m2v.py 20 500
echo '\nmfcc30 ae100'
python test_m2v.py 30 100
echo '\nmfcc30 ae300'
python test_m2v.py 30 300
echo '\nmfcc30 ae500'
python test_m2v.py 30 500
