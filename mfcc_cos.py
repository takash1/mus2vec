import os
import sys
import numpy as np


# Cosine similarity
def cos_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# Calculate similarity
def similar_list(target, nceps):
    v_in = np.load(target)
    v_in = v_in[1000:4000, :].flatten()
    genres = ['blues', 'classical', 'country', 'disco', 'hiphop',
              'jazz', 'metal', 'pop', 'reggae', 'rock']
    mfcc_list = []
    for g in genres:
        for i in range(10):
            fname = os.path.join('gtzan', g,
                                 g + ".%05d_%d.ceps.npy" % (i, nceps))
            if fname == target:
                continue
            v = np.load(fname)
            v = v[1000:4000, :].flatten()
            distance = cos_sim(v_in, v)
            mfcc_list.append([g, i, distance])
    return sorted(mfcc_list, key=lambda x: -x[2])


def main():
    # Arguments
    args = sys.argv
    genre = args[1]
    number = int(args[2])
    nceps = int(args[3])
    if len(args) > 4:
        sup = int(args[4])
    else:
        sup = 20

    # Load data
    fin = os.path.join('gtzan', genre,
                       genre + ".%05d_%d.ceps.npy" % (number, nceps))

    mfcc_list = similar_list(fin, nceps)

    # Display
    print "input: ", genre, "%05d" % number
    print "-" * 30
    hit = 0
    ap = 0
    for i in range(sup):
        print "%s\t%05d\t%.6f" % (mfcc_list[i][0],
                                  mfcc_list[i][1],
                                  mfcc_list[i][2])
        if genre in mfcc_list[i]:
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
