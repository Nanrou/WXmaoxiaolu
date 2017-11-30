import os

import requests
from bs4 import BeautifulSoup

from settings import BASE_DIR

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0', 'Referer': 'http://music.163.com/'}
TEST_ARTIST_ID = 188141
TEST_SONG_ID = 519913462
ARTIST_URL = 'http://music.163.com/artist?id={artist_id}'
SONG_URL = 'http://music.163.com/api/song/lyric?os=pc&id={song_id}&lv=-1&kv=-1&tv=-1'


def get_artist(id_):
    resp = requests.get(ARTIST_URL.format(artist_id=id_), headers=HEADERS)
    return resp
    
def get_lyric(id_):
    resp = requests.get(SONG_URL.format(song_id=id_), headers=HEADERS)
    return resp
    
def scrape_all_urls_of_song():
    if os.path.exists(os.path.join(BASE_DIR, 'for_test.html')):
        with open(os.path.join(BASE_DIR, 'for_test.html'), 'r', encoding='utf-8') as rf:
            soup = BeautifulSoup(rf.read(), 'lxml')
    else:
            raise RuntimeError('need doc file')
    
    song_urls = []    
    for s in soup.find_all('ul', 'f-hide'):
        for li in s.find_all('li'):
            song_urls.append(li.a.get('href'))
    return song_urls
    
    
if __name__ == '__main__':
    scrape_all_urls_of_song()