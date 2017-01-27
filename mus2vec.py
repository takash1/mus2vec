import os
import sys
import numpy as np


# Cosine similarity
def cos_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# Calculate similarity
def similar_list(target, dirname):
    v_in = np.load(target)
    genres = ['blues', 'classical', 'country', 'disco', 'hiphop',
              'jazz', 'metal', 'pop', 'reggae', 'rock']
    mus2vec_list = []
    for g in genres:
        for i in range(100):
            fname = os.path.join(dirname, g, g + ".%05d.npy" % i)
            if fname == target:
                continue
            v = np.load(fname)
            distance = cos_sim(v_in, v)
            mus2vec_list.append([g, i, distance])
    return sorted(mus2vec_list, key=lambda x: -x[2])


def main():
    # Arguments
    args = sys.argv
    genre = args[1]
    number = int(args[2])
    nceps = int(args[3])
    dim = int(args[4])
    if len(args) > 5:
        sup = int(args[5])
    else:
        sup = 20

    # Load data
    dirname = os.path.join("mus2vecs", "mus2vec_%d_%d" % (nceps, dim))
    fin = os.path.join(dirname, genre, genre + ".%05d.npy" % number)

    mus2vec_list = similar_list(fin, dirname)

    # Display
    print "input : ", genre, "%05d" % number
    print "-" * 30
    hit = 0
    ap = 0
    for i in range(sup):
        print "%s\t%05d\t%.6f" % (mus2vec_list[i][0],
                                  mus2vec_list[i][1],
                                  mus2vec_list[i][2])
        if genre in mus2vec_list[i]:
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
