import sys
import requests
from bs4 import BeautifulSoup
import numpy as np
import os
from multiprocessing import Pool

def get_soup(link):
    return str(BeautifulSoup(requests.get(link).content))

def invert_image(tup):
    i, im = tup
    os.system('convert %s -channel RGB -negate %s' % (im, './tmp_proc_img/'+prefix+'/'+str(i)+'.png'))

baseurl = 'https://www.youtube.com'
url = sys.argv[1]
text_to_replace = sys.argv[2]
prefix = sys.argv[3]

html = requests.get(url).content
soup = BeautifulSoup(html)

placeholder_img = './placeholder.png'

h = [t.text.strip() for t in soup.find_all('h4') if 'Quantum' in t.text.strip()]
h = [t.replace(text_to_replace, '').split(' - ')[-1].strip() for t in h]

bl = [baseurl + a['href'] for a in soup.find_all('a') if 'watch' in a['href'] and 'index' in a['href'] and not 'google' in a['href']][-(len(h)):]
bl = np.unique(bl)
bl = sorted(bl, key=lambda x: int(x.split('=')[-1]))

with Pool(None) as p:
    soups = p.map(get_soup, bl)

soups = [BeautifulSoup(soup) for soup in soups]
im_links = []
for soup in soups:
    i = 0
    for t in soup.find_all('p', attrs={'id':'eow-description'})[0].find_all('a'):
        if '.png' in t.text:
            im_links.append(t.text)
            i+=1
    if i == 0:
        im_links.append(placeholder_img)

#im_links = [[t for t in soup.find_all('p', attrs={'id':'eow-description'})[0].find_all('a') if '.png' in t.text for soup in soups]

#im_links = [t.text if '.png' in t.text else placeholder_img for t in im_links]

if not os.path.exists('./tmp_raw_img/%s' % (prefix)):
    os.mkdir('./tmp_raw_img/%s' % (prefix))

for i, im_link in enumerate(im_links):
    if not 'placeholder' in im_link:
        os.system('wget %s -O ./tmp_raw_img/%s/%s.png' % (im_link, prefix, i ))
    else:
        os.system('cp ./placeholder.png ./tmp_raw_img/%s/%s.png' % (prefix, i))

from glob import glob

raw_imgs = glob('./tmp_raw_img/%s/*.png' % (prefix))
raw_imgs = sorted(raw_imgs, key = lambda x: int(x.split('/')[-1].split('.')[0]))

if not os.path.exists('./tmp_proc_img/%s' % (prefix)):
    os.mkdir('./tmp_proc_img/%s' % (prefix))

with Pool(None) as p:
    p.map(invert_image, enumerate(raw_imgs))

#for i, im in enumerate(raw_imgs):
#    os.system('convert %s -channel RGB -negate %s' % (im, './tmp_proc_img/'+prefix+'/'+str(i)+'.png'))

proc_imgs = glob('./tmp_proc_img/%s/*.png' % (prefix))
proc_imgs = sorted(proc_imgs, key = lambda x: int(x.split('/')[-1].split('.')[0]))
#proc_imgs = [os.path.abspath(i) for i in proc_imgs]

import pickle as pkl

pkl.dump(h, open('%s_headlines.pkl'%(prefix), 'wb'))
pkl.dump(bl, open('%s_links.pkl' % (prefix), 'wb'))
pkl.dump(proc_imgs, open('%s_proc_imgs.pkl' % (prefix), 'wb'))

