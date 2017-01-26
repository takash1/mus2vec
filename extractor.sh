#!/bin/sh
echo 'mfcc13 ae100'
python encoder.py 13 100
echo 'mfcc13 ae300'
python encoder.py 13 300
echo 'mfcc13 ae500'
python encoder.py 13 500
echo 'mfcc20 ae100'
python encoder.py 20 100
echo 'mfcc20 ae300'
python encoder.py 20 300
echo 'mfcc20 ae500'
python encoder.py 20 500
echo 'mfcc39 ae100'
python encoder.py 39 100
echo 'mfcc39 ae300'
python encoder.py 39 300
echo 'mfcc39 ae500'
python encoder.py 39 500
