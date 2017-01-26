import os
import sys
import mfcc_cos

args = sys.argv
nceps = int(args[1])

genres = ['blues', 'classical', 'country', 'disco', 'hiphop',
          'jazz', 'metal', 'pop', 'reggae', 'rock']

sup = 20
hit = 0
tot = 0
for g in genres:
    for i in range(100):
        fin = os.path.join('gtzan', g, g + ".%05d_%d.ceps.npy" % (i, nceps))
        mfcc_list = mfcc_cos.similar_list(fin, nceps)
        for j in range(sup):
            if g in mfcc_list[j]:
                hit += 1
        tot += 20

print "%f%% (%d/%d)" % (hit/float(tot)*100, hit, tot)
