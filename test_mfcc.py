import os
import sys
import mfcc_cos

args = sys.argv
nceps = int(args[1])

genres = ['blues', 'classical', 'country', 'disco', 'hiphop',
          'jazz', 'metal', 'pop', 'reggae', 'rock']

tot = 0
ave_precision = 0
for g in genres:
    for i in range(100):
        fin = os.path.join('gtzan', g, g + ".%05d_%d.ceps.npy" % (i, nceps))
        mfcc_list = mfcc_cos.similar_list(fin, nceps)
        hit = 0
        ap = 0
        for j in range(len(mfcc_list)):
            if g in mfcc_list[j]:
                hit += 1
                ap += hit / float(i + 1)
            if hit == 100:
                break
        if hit == 0:
            ap = 0
        else:
            ap /= float(hit)
        tot += 1
        ave_precision += ap

print "AP@%d : %f (total : %d)" % (sup, ave_precision / float(tot), tot)
