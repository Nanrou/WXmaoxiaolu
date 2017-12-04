import os
import pickle
import time
from random import randint

import requests
from bs4 import BeautifulSoup

from .settings import BASE_DIR, MyLogger


logger = MyLogger(os.path.abspath(__file__).split('/')[-1])

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0',
           'Referer': 'http://music.163.com/'}
TEST_ARTIST_ID = 188141
TEST_SONG_ID = 519913462
ARTIST_URL = 'http://music.163.com/artist?id={artist_id}'
SONG_URL = 'http://music.163.com/api/song/lyric?os=pc&id={song_id}&lv=-1&kv=-1&tv=-1'

ALL_ARTIST = []


def get_artist(id_):
    resp = requests.get(ARTIST_URL.format(artist_id=id_), headers=HEADERS, timeout=3)
    return resp


def get_lyric(id_):
    resp = requests.get(SONG_URL.format(song_id=id_), headers=HEADERS, timeout=3)
    return resp


def scrape_all_urls_of_song(doc):
    soup = BeautifulSoup(doc, 'lxml')
    song_urls = []
    for s in soup.find_all('ul', 'f-hide'):
        for li in s.find_all('li'):
            song_urls.append(li.a.get('href'))
    return song_urls


def scrape_artist_name(doc):
    soup = BeautifulSoup(doc, 'lxml')
    return soup.find(id='artist-name').string


def extract_id_from_url(uri):
    if '=' in uri:
        return uri.split('=')[-1]


def handler_single_artist(id_):
    doc = get_artist(id_).text
    artist_name = scrape_artist_name(doc)
    artist_folder = os.path.join(os.path.join(BASE_DIR, 'data'), artist_name)
    if not os.path.exists(artist_folder):
        os.mkdir(artist_folder)

    _tmp = scrape_all_urls_of_song(doc)
    _llen = len(_tmp)
    all_song_id = map(extract_id_from_url, _tmp)

    for index, song_id in enumerate(all_song_id, start=1):
        time.sleep(randint(3, 5) / 10)
        lyric = get_lyric(song_id).json()  # TODO 用一下异步爬取
        with open(os.path.join(artist_folder, song_id), 'wb') as wf:
            pickle.dump(lyric, wf)
        logger.debug('finish {name} {lyric} ({i}/{sum})'.format(name=artist_name, lyric=song_id, i=index, sum=_llen))


if __name__ == '__main__':
    # single_workflow(TEST_ARTIST_ID)
    pass
