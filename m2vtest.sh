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
echo '\nmfcc39 ae100'
python test_m2v.py 39 100
echo '\nmfcc39 ae300'
python test_m2v.py 39 300
echo '\nmfcc39 ae500'
python test_m2v.py 39 500
