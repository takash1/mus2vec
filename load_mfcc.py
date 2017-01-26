import os
import sys
import numpy as np
from scikits.talkbox.features import mfcc

genres = ['blues', 'classical', 'country', 'disco', 'hiphop',
          'jazz', 'metal', 'pop', 'reggae', 'rock']
dirname = 'gtzan'
nceps = int(sys.argv[1])
v = []

for g in genres:
    for i in range(100):
        fname = os.path.join(dirname, g, g + ".%05d_%d.ceps.npy" % (i, nceps))
        ceps = np.load(fname)
        v.append(ceps[1000:4000, :])

print np.array(v).shape
