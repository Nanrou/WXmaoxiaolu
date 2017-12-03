import unittest
import os

from settings import BASE_DIR
from crawler import get_artist, get_lyric, TEST_ARTIST_ID, TEST_SONG_ID


class TestRequest(unittest.TestCase):

    #@classmethod
    #def setUpClass(cls):
    #    cls.resp = get_artist(TEST_ARTIST_ID)
        
    #@classmethod
    #def tearDownClass(cls):
    #    with open(os.path.join(BASE_DIR, 'for_test.html'), 'w', encoding='utf-8') as wf:
    #        wf.write(cls.resp.text)
        
    def test_get_artist_success(self):      
        self.assertEqual(get_artist(TEST_ARTIST_ID).status_code, 200)

    def test_get_lynic_success(self):
        self.assertEqual(get_lyric(TEST_SONG_ID).status_code, 200)
    
if __name__ == '__main__':
    unittest.main()