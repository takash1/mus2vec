#!/bin/sh
echo 'mfcc13 k4'
python mfcc_to_sig.py 13 4
echo '\nmfcc13 k16'
python mfcc_to_sig.py 13 16
echo '\nmfcc13 k32'
python mfcc_to_sig.py 13 32
echo '\nmfcc20 k4'
python mfcc_to_sig.py 20 4
echo '\nmfcc20 k16'
python mfcc_to_sig.py 20 16
echo '\nmfcc20 k32'
python mfcc_to_sig.py 20 32
echo '\nmfcc30 k4'
python mfcc_to_sig.py 30 4
echo '\nmfcc30 k16'
python mfcc_to_sig.py 30 16
echo '\nmfcc30 k32'
python mfcc_to_sig.py 30 32
