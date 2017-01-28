import os
import sys
import numpy as np
import cupy as cp
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

# Use GPU or not
if len(args) > 3 and args[3] == 'g':
    enable_cupy = True
else:
    enable_cupy = False

# Choose model
if nceps == 13:
    if dim == 100:
        import models.cae_13_100
        model = models.cae_13_100.ConvAE()
    elif dim == 300:
        import models.cae_13_300
        model = models.cae_13_300.ConvAE()
    elif dim == 500:
        import models.cae_13_500
        model = models.cae_13_500.ConvAE()
    else:
        print 'Argument(dim) Error'
        sys.exit(1)
elif nceps == 20:
    if dim == 100:
        import models.cae_20_100
        model = models.cae_20_100.ConvAE()
    elif dim == 300:
        import models.cae_20_300
        model = models.cae_20_300.ConvAE()
    elif dim == 500:
        import models.cae_20_500
        model = models.cae_20_500.ConvAE()
    else:
        print 'Argument(dim) Error'
        sys.exit(1)
elif nceps == 30:
    if dim == 100:
        import models.cae_30_100
        model = models.cae_30_100.ConvAE()
    elif dim == 300:
        import models.cae_30_300
        model = models.cae_30_300.ConvAE()
    elif dim == 500:
        import models.cae_30_500
        model = models.cae_30_500.ConvAE()
    else:
        print 'Argument(dim) Error'
        sys.exit(1)
else:
    print 'Argument(nceps) Error'
    sys.exit(1)


# Load data
genres = ['blues', 'classical', 'country', 'disco', 'hiphop',
          'jazz', 'metal', 'pop', 'reggae', 'rock']
dirname = 'gtzan'
v = []

for g in genres:
    for i in range(10, 100):
        fname = os.path.join(dirname, g, g + ".%05d_%d.ceps.npy" % (i, nceps))
        ceps = np.load(fname)
        v.append(ceps[1000:4000, :])

n, h, w = np.array(v).shape
if enable_cupy:
    xtrain = cp.array(v).astype(cp.float32).reshape(n, 1, h, w)
else:
    xtrain = np.array(v).astype(np.float32).reshape(n, 1, h, w)


# Initialize model
if enable_cupy:
    model.to_gpu()
    chainer.cuda.get_device(0).use()
optimizer = optimizers.SGD()
optimizer.setup(model)


# Learn
epoch = 200
bs = 100
print "epoch", "\t", "loss"
for j in range(epoch):
    sffindx = np.random.permutation(n)
    for i in range(0, n, bs):
        x = Variable(xtrain[sffindx[i:(i+bs) if (i+bs) < n else n]])
        model.zerograds()
        loss = model(x, layer=(j/50+1), train=True)
        loss.backward()
        optimizer.update()
    print j+1, "\t", loss.data

# Save
serializers.save_npz("models/CAE_%d_%d.model" % (nceps, dim), model)
