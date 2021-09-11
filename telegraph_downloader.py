import requests
import re
import os
import time
from bs4 import BeautifulSoup as bs 

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240'}

url = input('Enter URL to scrape: ')

# what if conn error
with requests.get(url, headers=header) as r:
  bso = bs(r.text, 'lxml')

dl_urls = [''.join(['https://telegra.ph', src]) for src in [tag['src'] for tag in bso.find_all('img')]]

# title choosing
title_str = bso.title.string
h1_str = bso.find('h1').string
if not title_str == h1_str:
  print('Which title you prefer to get? DEFAULT: 2')
  print('1: ', title_str)
  print('2: ', h1_str)
  value = int(input('> '))
  if value == 1:
    title = title_str
  else:
    print('You can choose only 1 or 2. Default vaule selected.')
    title = h1_str

# make directory with title chosen
# what if another shot still exist?
try:
  os.mkdir(title)
except FileExistsError as e:
  print('Directory named as "{}" already existed.'.format(title))

  choices = (('Y', 'y'), ('N', 'n'))
  while u_choice := input('Give another shot? [Y/N] '):    
    if u_choice in choices[0]:
      os.mkdir(title + '_' + str(int(time.time())))
      break
    elif u_choice == 'N' or u_choice == 'n':
      print('Wise choice!')
      exit()
    else:
      print('This is DoA question. Just choose "Yes" or "No".')
  
os.chdir(title) # set created directory as cwd

for dl_url in dl_urls:
  fn = os.path.basename(dl_url)
  
  with requests.get(dl_url, stream=True, headers=header) as r:
    print('Downloading "{}" ...'.format(fn))
    with open(fn, 'wb') as f:
      for chunk in r.iter_content(chunk_size=2048):
        f.write(chunk)
    print('{} downloaded successfully.'.format(fn))

# check result on OS
if len(dl_urls) != len(os.listdir()):
  print('{} items planned to download. But {} items were downloaded.'.format(len(dl_urls), len(os.listdir()))
        
