import os
import sys
import numpy as np
from scikits.talkbox.features import mfcc
import chainer
from chainer import cuda, Function, gradient_check, Variable
from chainer import optimizers, serializers, utils
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L

args = sys.argv
nceps = int(args[1])
dim = int(args[2])

# Choose model
if nceps == 13:
    if dim == 100:
        import models.cae_13_100
        model = models.cae_13_100.ConvAE()
        serializers.load_npz('models/CAE_13_100.model', model)
    elif dim == 300:
        import models.cae_13_300
        model = models.cae_13_300.ConvAE()
        serializers.load_npz('models/CAE_13_300.model', model)
    elif dim == 500:
        import models.cae_13_500
        model = models.cae_13_500.ConvAE()
        serializers.load_npz('models/CAE_13_500.model', model)
    else:
        print 'Argument(dim) Error'
        sys.exit(1)
elif nceps == 20:
    if dim == 100:
        import models.cae_20_100
        model = models.cae_20_100.ConvAE()
        serializers.load_npz('models/CAE_20_100.model', model)
    elif dim == 300:
        import models.cae_20_300
        model = models.cae_20_300.ConvAE()
        serializers.load_npz('models/CAE_20_300.model', model)
    elif dim == 500:
        import models.cae_20_500
        model = models.cae_20_500.ConvAE()
        serializers.load_npz('models/CAE_20_500.model', model)
    else:
        print 'Argument(dim) Error'
        sys.exit(1)
elif nceps == 39:
    if dim == 100:
        import models.cae_39_100
        model = models.cae_39_100.ConvAE()
        serializers.load_npz('models/CAE_39_100.model', model)
    elif dim == 300:
        import models.cae_39_300
        model = models.cae_39_300.ConvAE()
        serializers.load_npz('models/CAE_39_300.model', model)
    elif dim == 500:
        import models.cae_39_500
        model = models.cae_39_500.ConvAE()
        serializers.load_npz('models/CAE_39_500.model', model)
    else:
        print 'Argument(dim) Error'
        sys.exit(1)
else:
    print 'Argument(nceps) Error'
    sys.exit(1)


# Load data
genres = ['blues', 'classical', 'country', 'disco', 'hiphop',
          'jazz', 'metal', 'pop', 'reggae', 'rock']
dir_in = 'gtzan'
v = []
for g in genres:
    for i in range(100):
        fname = os.path.join(dir_in, g, g + ".%05d_%d.ceps.npy" % (i, nceps))
        ceps = np.load(fname)
        v.append(ceps[1000:4000, :])

# Encode
n, h, w = np.array(v).shape
xtest = np.array(v).astype(np.float32).reshape(n, 1, h, w)
x = Variable(xtest, volatile='on')
yt = model.encode(x).data

# Save
dir_out = os.path.join("mus2vecs", "mus2vec_%d_%d" % (nceps, dim))
if not os.path.isdir(dir_out):
    os.mkdir(dir_out)
for d in genres:
    if not os.path.isdir(os.path.join(dir_out, d)):
        os.mkdir(os.path.join(dir_out, d))
for i in range(n):
    dst = np.array(yt[i, :].reshape(1, dim)[0])
    fn = os.path.join(dir_out, genres[i / 100],
                      genres[i / 100] + ".%05d.npy" % (i % 100))
    np.save(fn, dst)
