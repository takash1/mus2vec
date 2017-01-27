import chainer
from chainer import cuda, Function, gradient_check, Variable
from chainer import optimizers, serializers, utils
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L

NCEPS = 13
DIM = 300


# Define model
class ConvAE(Chain):
    def __init__(self):
        super(ConvAE, self).__init__(
            enc1=L.Convolution2D(1, 100, (1, NCEPS)),
            enc2=L.Convolution2D(100, 50, (1, NCEPS)),
            enc3=L.Convolution2D(50, 10, (1, 1)),
            enc4=L.Convolution2D(10, 1000, (3000, 1)),
            enc5=L.Convolution2D(1000, DIM, (1, 1)),
            dec5=L.Deconvolution2D(DIM, 1000, (1, 1)),
            dec4=L.Deconvolution2D(1000, 10, (3000, 1)),
            dec3=L.Deconvolution2D(10, 50, (1, 1)),
            dec2=L.Deconvolution2D(50, 100, (1, 1)),
            dec1=L.Deconvolution2D(100, 1, (1, NCEPS))
        )

    def __call__(self, x):
        return F.mean_squared_error(self.fwd(x), x)

    def fwd(self, x):
        return self.decode(self.encode(x))

    def encode(self, x):
        e1 = F.relu(self.enc1(x))
        e2 = F.relu(self.enc2(e1))
        e3 = F.relu(self.enc3(e2))
        e4 = F.relu(self.enc4(e3))
        e5 = F.relu(self.enc5(e4))
        return e5

    def decode(self, x):
        d5 = F.relu(self.dec4(x))
        d4 = F.relu(self.dec4(d5))
        d3 = F.relu(self.dec3(d4))
        d2 = F.relu(self.dec2(d3))
        d1 = self.dec1(d2)
        return d1
