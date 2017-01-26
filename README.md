# mus2vec

## 開発環境
- Python2.7
- Anaconda
- chainer
- scikits.talkbox
- sox

### Docker image
- takash1/ae

## Google Drive
- gtzan, models, mus2vecsファルダはGoogle Driveにある
- mus2vec以下に解凍

## gtzan
- 音楽データセット [GTZAN genre](http://marsyasweb.appspot.com/download/data_sets/)

## models
- Autoencoderのモデル定義ファイル
- 学習済みモデル

## mus2vecs
- GTZANのベクトル表現ファイル

## soxtool.py
GTZANデータセットをwavに変換する

#### issue0: 3000frame
- ```-r 16k```で変換しても3000frameに揃わない

## create_ceps.py
usage: ```$ python create_ceps.py [nceps]```
- Cepstrumに変換し、npy形式で保存する
- コマンドライン引数でmfcc次元を指定する
- 出力: ```gtzan/[genre]/[genre].[num]_[mfcc].ceps.npy```

#### issue1: warning
```
/usr/local/lib/python2.7/dist-packages/scikits/talkbox/features/mfcc.py:108: RuntimeWarning: divide by zero encountered in log10
  mspec = np.log10(np.dot(spec, fbank.T))
```

## load_mfcc.py
usage: ```$ python load_mfcc.py [nceps]```
- mfcc読み込みテスト
- コマンドライン引数でmfcc次元を指定する

## learn_ae.py
usage: ```$ python learn_ae.py [ncpes] [dim] [g]```
- [nceps] : mfccの次元数
- [dim] : Autoencoderの中間層のユニット数
- [g] : 'g'とすれば、GPUを用いて学習を行う
- Autoencoderの学習を行う
- 出力: ```models/CAE_[nceps]_[dim].model```

## learn.sh
- mfcc[13, 20, 39], ae[100, 300, 500]の学習を実行する(learn_ae.py)
- GPU使用

## encoder.py
usage: ```$ python encoder.py [nceps] [dim]```
- [nceps] : mfccの次元数
- [dim] : Autoencoderの中間層のユニット数
- Autoencoderの中間層の表現によりベクトル化する
- 次元数[dim]のベクトル表現が得られる
- 出力: ```mus2vecs/mus2vec_[ncpes]_[dim]/[genre]/[genre].[num].npy```

## extractor.sh
- mfcc[13, 20, 39], ae[100, 300, 500]のベクトル化を実行する(encoder.py)

## mus2vec.py
usage: ```$ python mus2vec.py [genre] [number] [nceps] [dim] [out]```
- [genre] [number] の楽曲の類似度が高い曲を上位[out]個を列挙する
- mfcc次元数[nceps]， Autoencoder次元数[dim]のモデルでの類似度を出す
- 同ジャンルの含有数を表示する

## mfcc_cos.py
usage: ```$ python mfcc_cos.py [genre] [number] [nceps] [out]```
- [genre] [number] の楽曲の類似度が高い曲を上位[out]個を列挙する
- mfcc次元数[nceps]の単純なCosine類似度を出す
- 同ジャンルの含有数を表示する

## test_m2v.py
usage: ```$ python test_m2v.py [nceps] [dim]```
- music2vecの正解率を出す

## m2vtest.sh
- mfcc[13, 20, 39], ae[100, 300, 500]のテストを行う(test_m2v.py)

## test_mfcc.py
usage: ```$ python test_mfcc.py [nceps]```
- mfcc_cosの正解率を出す

## mfcctest.sh
- mfcc[13, 20, 39], ae[100, 300, 500]のテストを行う(test_mfcc.py)
