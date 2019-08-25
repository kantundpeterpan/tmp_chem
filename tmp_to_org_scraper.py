import sys
import requests
from bs4 import BeautifulSoup
import numpy as np

baseurl = 'https://www.youtube.com'
url = sys.argv[1]
text_to_replace = sys.argv[2]

html = requests.get(url).content
soup = BeautifulSoup(html)

h = [t.text.strip() for t in soup.find_all('h4')][:-1]
h = [t.replace(text_to_replace, '') for t in h]

bl = [baseurl + a['href'] for a in soup.find_all('a') if 'watch' in a['href'] and 'index' in a['href'] and not 'google' in a['href']][1:]
bl = np.unique(bl)
bl = sorted(bl, key=lambda x: int(x.split('=')[-1]))

for he, li in zip(h,bl): 
    print('** pending %s \n [[%s][LINK]]'%(he, li)) 
