import unittest
import os

import re

from crawler import scrape_all_urls_of_song

class TestScrape(unittest.TestCase):
            
    def test_get_artist_return_right_thing(self):
        self.assertNotEqual(len(scrape_all_urls_of_song()), 0)
        
    def test_scrape_right_place(self):
        self.assertEqual(all(map(lambda x: re.match('/song\?id=\d+', x), scrape_all_urls_of_song())), True)
                
    
if __name__ == '__main__':
    unittest.main()