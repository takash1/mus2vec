import chainer
from chainer import cuda, Function, gradient_check, Variable
from chainer import optimizers, serializers, utils
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L

NCEPS = 13
DIM = 500


# Define model
class ConvAE(Chain):
    def __init__(self):
        super(ConvAE, self).__init__(
            enc1=L.Convolution2D(1, 100, (1, NCEPS)),
            enc2=L.Convolution2D(100, 50, (1, 1)),
            enc3=L.Convolution2D(50, 10, (1, 1)),
            enc4=L.Convolution2D(10, 1000, (3000, 1)),
            enc5=L.Convolution2D(1000, DIM, (1, 1)),
            dec5=L.Deconvolution2D(DIM, 1000, (1, 1)),
            dec4=L.Deconvolution2D(1000, 10, (3000, 1)),
            dec3=L.Deconvolution2D(10, 50, (1, 1)),
            dec2=L.Deconvolution2D(50, 100, (1, 1)),
            dec1=L.Deconvolution2D(100, 1, (1, NCEPS))
        )

    def __call__(self, x, layer):
        return F.mean_squared_error(self.fwd(x, layer), x)

    def fwd(self, x, layer):
        return self.decode(self.encode(x, layer), layer)

    def encode(self, x, layer=5):
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
        e = F.relu(self.enc5(e))
        if layer == 5:
            return e

    def decode(self, x, layer):
        if layer == 5:
            x = F.relu(self.dec5(x))
        if layer >= 4:
            x = F.relu(self.dec4(x))
        if layer >= 3:
            x = F.relu(self.dec3(x))
        if layer >= 2:
            x = F.relu(self.dec2(x))
        if layer >= 1:
            d = self.dec1(x)
        return d
