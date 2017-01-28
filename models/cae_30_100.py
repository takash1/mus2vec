import chainer
from chainer import cuda, Function, gradient_check, Variable
from chainer import optimizers, serializers, utils
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L

NCEPS = 30
DIM = 100


# Define model
class ConvAE(Chain):
    def __init__(self):
        super(ConvAE, self).__init__(
            enc1=L.Convolution2D(1, 50, (7, NCEPS), stride=2, pad=(3, 0)),
            enc2=L.Convolution2D(50, 50, (5, 1), stride=2, pad=(2, 0)),
            enc3=L.Convolution2D(50, 1, (3, 1), pad=(1, 0)),
            enc4=L.Convolution2D(1, DIM, (750, 1)),
            dec4=L.Deconvolution2D(DIM, 1, (750, 1)),
            dec3=L.Deconvolution2D(1, 50, (3, 1), pad=(1, 0)),
            dec2=L.Deconvolution2D(50, 50, (4, 1), stride=2, pad=(1, 0)),
            dec1=L.Deconvolution2D(50, 1, (6, NCEPS), stride=2, pad=(2, 0))
        )

    def __call__(self, x, layer, train):
        return F.mean_squared_error(self.fwd(x, layer, train), x)

    def fwd(self, x, layer, train):
        return self.decode(self.encode(x, layer, train), layer)

    def encode(self, x, layer=4, train=False):
        x = F.dropout(x, ratio=0.1, train=train)
        e = F.relu(self.enc1(x))
        if layer == 1:
            return e
        e = F.relu(self.enc2(e))
        if layer == 2:
            return e
        e = F.relu(self.enc3(e))
        if layer == 3:
            return e
        e = F.relu(self.enc4(e))
        if layer == 4:
            return e

    def decode(self, x, layer):
        if layer == 4:
            x = F.relu(self.dec4(x))
        if layer >= 3:
            x = F.relu(self.dec3(x))
        if layer >= 2:
            x = F.relu(self.dec2(x))
        if layer >= 1:
            d = self.dec1(x)
        return d
