import os
import sys
import numpy as np
import scipy.io.wavfile
from scikits.talkbox.features import mfcc


def write_ceps(ceps, fn, nceps):
    base_fn, ext = os.path.splitext(fn)
    data_fn = base_fn + "_%d" % nceps + ".ceps"
    np.save(data_fn, ceps)


def create_ceps(fn, nceps):
    sample_rate, X = scipy.io.wavfile.read(fn)
    ceps, mspec, spec = mfcc(X, nceps=nceps)
    write_ceps(ceps, fn, nceps)


genres = ['blues', 'classical', 'country', 'disco', 'hiphop',
          'jazz', 'metal', 'pop', 'reggae', 'rock']
dirname = 'gtzan'
nceps = int(sys.argv[1])

for g in genres:
    for i in range(100):
        fname = os.path.join(dirname, g, g + ".%05d.wav" % i)
        create_ceps(fname, nceps)
