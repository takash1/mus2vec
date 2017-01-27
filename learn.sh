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
echo '\nmfcc30 ae100'
python learn_ae.py 30 100 g
echo '\nmfcc30 ae300'
python learn_ae.py 30 300 g
echo '\nmfcc30 ae500'
python learn_ae.py 30 500 g
