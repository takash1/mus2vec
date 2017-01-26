import os
import sys
import mus2vec

args = sys.argv
nceps = int(args[1])
dim = int(args[2])

genres = ['blues', 'classical', 'country', 'disco', 'hiphop',
          'jazz', 'metal', 'pop', 'reggae', 'rock']
dirname = os.path.join("mus2vecs", "mus2vec_%d_%d" % (nceps, dim))

sup = 20
hit = 0
tot = 0
for g in genres:
    for i in range(100):
        fin = os.path.join(dirname, g, g + ".%05d.npy" % i)
        mus2vec_list = mus2vec.similar_list(fin, dirname)
        for j in range(sup):
            if g in mus2vec_list[j]:
                hit += 1
        tot += 20

print "%f%% (%d/%d)" % (hit/float(tot)*100, hit, tot)
