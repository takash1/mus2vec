import os
import sys
import mfccAve_cos

args = sys.argv
nceps = int(args[1])

genres = ['blues', 'classical', 'country', 'disco', 'hiphop',
          'jazz', 'metal', 'pop', 'reggae', 'rock']

tot = 0
ave_precision = 0
for g in genres:
    for i in range(10):
        fin = os.path.join('gtzan', g, g + ".%05d_%d.ceps.npy" % (i, nceps))
        mfcc_list = mfccAve_cos.similar_list(fin, nceps)
        hit = 0
        ap = 0
        for j in range(len(mfcc_list)):
            if g in mfcc_list[j]:
                hit += 1
                ap += hit / float(j + 1)
            if hit == 10:
                break
        if hit == 0:
            ap = 0
        else:
            ap /= float(hit)
        tot += 1
        ave_precision += ap

print "AP : %f (total : %d)" % (ave_precision / float(tot), tot)
