import unittest
import os
import re

from maoxiaolu.i_am_a_rapper.settings import BASE_DIR
from maoxiaolu.i_am_a_rapper.crawler import get_artist, get_lyric, TEST_ARTIST_ID, TEST_SONG_ID, scrape_all_urls_of_song, extract_id_from_url, scrape_artist_name


@unittest.skip
class TestRequest(unittest.TestCase):

    def test_get_artist_success(self):
        self.assertEqual(get_artist(TEST_ARTIST_ID).status_code, 200)

    def test_get_lyric_success(self):
        self.assertEqual(get_lyric(TEST_SONG_ID).status_code, 200)


class TestScrape(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(os.path.join(BASE_DIR, 'for_test.html')):
            with open(os.path.join(BASE_DIR, 'for_test.html'), 'w', encoding='utf-8') as wf:
                wf.write(get_artist(TEST_ARTIST_ID))
        with open(os.path.join(BASE_DIR, 'for_test.html'), 'r', encoding='utf-8') as rf:
            cls.doc = rf.read()

    def test_get_artist_return_right_thing(self):
        self.assertNotEqual(len(scrape_all_urls_of_song(self.doc)), 0)

    def test_scrape_right_place(self):
        self.assertEqual(all(map(lambda x: re.match('/song\?id=\d+', x), scrape_all_urls_of_song(self.doc))), True)

    def test_scrape_artist_name(self):
        self.assertEqual(scrape_artist_name(self.doc), '满舒克')

    def test_split_id_from_url(self):
        _uri = '/song?id=123456'
        self.assertEqual(extract_id_from_url(_uri), '123456')


if __name__ == '__main__':
    unittest.main()
