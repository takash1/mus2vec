# coding:utf-8
'''
mfcc_to_signature.py
usage: python mfcc_to_signature.py [nceps] [nk]
各曲のMFCCをシグネチャに変換する
'''

import os
import struct
import sys
import numpy as np
import scipy.cluster
import glob


def vq(mfcc, k):
    """mfccのベクトル集合をk個のクラスタにベクトル量子化"""
    codebook, destortion = scipy.cluster.vq.kmeans(mfcc, k)
    code, dist = scipy.cluster.vq.vq(mfcc, codebook)
    return code


if __name__ == "__main__":
    nceps = int(sys.argv[1])
    nk = int(sys.argv[2])
    mfccDir = "gtzan"
    sigDir = "sig"

    if not os.path.exists(sigDir):
        os.mkdir(sigDir)

    genres = ['blues', 'classical', 'country', 'disco', 'hiphop',
              'jazz', 'metal', 'pop', 'reggae', 'rock']

    for g in genres:
        for i in range(10):
            mfccFile = os.path.join(mfccDir, g,
                                    g + ".%05d_%d.ceps.npy" % (i, nceps))
            sigFile = os.path.join(sigDir,
                                   g + ".%05d_%d_%d.sig" % (i, nceps, nk))
            print mfccFile, "=>", sigFile
            fout = open(sigFile, "w")
            ceps = np.load(mfccFile)
            ceps = ceps[1000:4000, :]

            # MFCCをベクトル量子化してコードを求める
            code = vq(ceps, nk)

            # 各クラスタのデータ数、平均ベクトル、
            # 共分散行列を求めてシグネチャとする
            for k in range(nk):
                # クラスタkのフレームのみ抽出
                frames = np.array([ceps[j] for j in range(len(ceps))
                                  if code[j] == k])
                # MFCCの各次元の平均をとって平均ベクトルを求める
                m = np.apply_along_axis(np.mean, 0, frames)  # 0は縦方向
                # MFCCの各次元間での分散・共分散行列を求める
                sigma = np.cov(frames.T)
                # 重み（各クラスタのデータ数）
                w = len(frames)
                # このクラスタの特徴量をフラット形式で出力
                # 1行が重み1個
                # 平均ベクトルnceps個、分散・共分散行列nceps*nceps個の計421個の数値列
                features = np.hstack((w, m, sigma.flatten()))
                features = [str(x) for x in features]
                fout.write(" ".join(features) + "\n")
            fout.close()
