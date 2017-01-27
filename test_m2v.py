import os
import sys
import mus2vec

args = sys.argv
nceps = int(args[1])
dim = int(args[2])

genres = ['blues', 'classical', 'country', 'disco', 'hiphop',
          'jazz', 'metal', 'pop', 'reggae', 'rock']
dirname = os.path.join("mus2vecs", "mus2vec_%d_%d" % (nceps, dim))

tot = 0
ave_precision = 0
for g in genres:
    for i in range(100):
        fin = os.path.join(dirname, g, g + ".%05d.npy" % i)
        mus2vec_list = mus2vec.similar_list(fin, dirname)
        hit = 0
        ap = 0
        for j in range(len(mus2vec_list)):
            if g in mus2vec_list[j]:
                hit += 1
                ap += hit / float(j + 1)
            if hit == 100:
                break
        if hit == 0:
            ap = 0
        else:
            ap /= float(hit)
        tot += 1
        ave_precision += ap

print "AP : %f (total : %d)" % (ave_precision / float(tot), tot)
