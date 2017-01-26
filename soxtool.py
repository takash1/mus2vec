import os

genres = ['blues', 'classical', 'country', 'disco', 'hiphop',
          'jazz', 'metal', 'pop', 'reggae', 'rock']
dirname = 'gtzan'

for g in genres:
    for i in range(100):
        src = os.path.join(dirname, g, g + ".%05d.au" % i)
        dst = os.path.join(dirname, g, g + ".%05d.wav" % i)
        # cmd = 'sox ' + src + ' -r 16k ' + dst
        cmd = 'sox ' + src + ' ' + dst
        os.system(cmd)
