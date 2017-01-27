# coding: utf-8
import numpy as np
import numpy.linalg
import pandas as pd
import pyper as pr
import os
import sys
from collections import defaultdict
import time


def KLDiv(mu1, S1, mu2, S2):
    """正規分布間のカルバック・ライブラー情報量"""
    # 逆行列を計算
    try:
        invS1 = np.linalg.inv(S1)
    except numpy.linalg.linalg.LinAlgError:
        return -1
    try:
        invS2 = np.linalg.inv(S2)
    except numpy.linalg.linalg.LinAlgError:
        return -1

    # KL Divergenceを計算
    t1 = np.sum(np.diag(np.dot(invS2, S1)))
    t2 = (mu2 - mu1).transpose()
    t3 = mu2 - mu1
    return t1 + np.dot(np.dot(t2, invS2), t3)


def symKLDiv(mu1, S1, mu2, S2):
    """対称性のあるカルバック・ライブラー情報量"""
    return 0.5 * (KLDiv(mu1, S1, mu2, S2) + KLDiv(mu2, S2, mu1, S1))


def loadSignature(sigFile):
    """シグネチャファイルをロード"""
    mat = []
    fp = open(sigFile, "r")
    for line in fp:
        line = line.rstrip()
        mat.append([float(x) for x in line.split()])
    fp.close()
    return np.array(mat)


# Rで輸送問題を解くライブラリ
# PypeRの設定
r = pr.R(RCMD="R", use_pandas='True')
r("library(lpSolve)")


def calcEMD(sigFile1, sigFile2, nceps):
    # シグネチャをロード
    sig1 = loadSignature(sigFile1)
    sig2 = loadSignature(sigFile2)

    # シグネチャの重み（0列目）を取得
    w1 = sig1[:, 0]
    w2 = sig2[:, 0]

    # 距離行列を計算
    numFeatures = sig1.shape[0]                 # クラスタの数
    dist = np.zeros(numFeatures * numFeatures)  # 距離行列

    for i in range(numFeatures):
        mu1 = sig1[i, 1:nceps+1].reshape(nceps, 1)   # 縦ベクトル
        S1 = sig1[i, nceps+1:].reshape(nceps, nceps)
        for j in range(numFeatures):
            mu2 = sig2[j, 1:nceps+1].reshape(nceps, 1)
            S2 = sig2[j, nceps+1:].reshape(nceps, nceps)
            # 特徴量iと特徴量j間のKLダイバージェンスを計算
            dist[i * numFeatures + j] = symKLDiv(mu1, S1, mu2, S2)

    # 重みと距離行列からEMDを計算
    # transport()の引数を用意
    costs = dist.reshape(len(w1), len(w2))
    row_signs = ["<"] * len(w1)
    row_rhs = w1
    col_signs = [">"] * len(w2)
    col_rhs = w2
    # Rへデータ渡す
    r.assign('costs', costs)
    r.assign('row_signs', row_signs)
    r.assign('row_rhs', row_rhs)
    r.assign('col_signs', col_signs)
    r.assign('col_rhs', col_rhs)

    # R上で輸送問題を解く
    r("t <- lp.transport(costs, 'min', \
                         row_signs, row_rhs, col_signs, col_rhs)")

    # R上で最適な輸送量を取得
    r("flow <- t$solution")

    # pythonへ
    flow = r.get("flow")

    dist = dist.reshape(len(w1), len(w2))
    flow = np.array(flow)
    work = np.sum(flow * dist)
    emd = work / np.sum(flow)
    return emd


def similar_list(target, nceps):
    genres = ['blues', 'classical', 'country', 'disco', 'hiphop',
              'jazz', 'metal', 'pop', 'reggae', 'rock']
    emd_list = []
    for g in genres:
        for i in range(100):
            fname = os.path.join('sig', g + ".%05d_%d.sig" % (i, nceps))
            if fname == target:
                continue
            emd = calcEMD(target, fname, nceps)
            if emd < 0:
                print 'raise negative value'
                continue
            emd_list.append([g, i, emd])
    return sorted(emd_list, key=lambda x: x[2])


def main():
    # Arguments
    args = sys.argv
    genre = args[1]
    number = int(args[2])
    nceps = int(args[3])
    if len(args) > 5:
        sup = int(args[5])
    else:
        sup = 20

    # Load data
    dirname = 'sig'
    fin = os.path.join(dirname, genre + ".%05d_%d.sig" % (number, nceps))

    emd_list = similar_list(fin, nceps)

    # Display
    print "input : ", genre, "%05d" % number
    print "-" * 30
    hit = 0
    ap = 0
    for i in range(sup):
        print "%s\t%05d\t%.6f" % (emd_list[i][0],
                                  emd_list[i][1],
                                  emd_list[i][2])
        if genre in emd_list[i]:
            hit += 1
            ap += hit / float(i + 1)

    # Average Precision
    if hit == 0:
        ap = 0
    else:
        ap /= float(hit)

    print "-" * 30
    # print genre, ": %d/%d" % (hit, sup)   # Precision@sup
    print genre, "AP@%d : %f" % (sup, ap)  # Average Precision@sup


if __name__ == '__main__':
    main()
