#!/bin/sh
echo 'mfcc13 ae100'
python learn_ae.py 13 100 g
echo '\nmfcc13 ae300'
python learn_ae.py 13 300 g
echo '\nmfcc13 ae500'
python learn_ae.py 13 500 g
echo '\nmfcc20 ae100'
python learn_ae.py 20 100 g
echo '\nmfcc20 ae300'
python learn_ae.py 20 300 g
echo '\nmfcc20 ae500'
python learn_ae.py 20 500 g
echo '\nmfcc39 ae100'
python learn_ae.py 39 100 g
echo '\nmfcc39 ae300'
python learn_ae.py 39 300 g
echo '\nmfcc39 ae500'
python learn_ae.py 39 500 g
