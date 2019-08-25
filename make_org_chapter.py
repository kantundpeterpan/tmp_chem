import sys

prefix = sys.argv[1]

from glob import glob

files_to_load = glob('./%s*.pkl' % (prefix))
files_to_load = sorted(files_to_load)

import pickle as pkl
for i, var in enumerate(('h', 'bl', 'proc_imgs')):
    exec('%s = pkl.load(open(\'%s\', \'rb\'))' % (var, files_to_load[i]))

for he, li, im in zip(h, bl, proc_imgs):
    print('*** pending %s' % (he))
    print('#+LATEX: \makebox[\\textwidth][c]{')
    print('#+ATTR_ORG: :width 650')
    if not 'placeholder' in im:
        print('#+ATTR_LATEX: :width 1.2\\textwidth')
    else:
        print('#+ATTR_LATEX: :width 0.7\\textwidth')
    print('[[%s]]' % (im))
    print('#+LATEX: }')
    print('#+BEGIN_COMMENT html')
    print('[[%s][LINK]]' % (li))
    print('#+END_COMMENT')
    print('#+LATEX: \pagebreak[4]')
