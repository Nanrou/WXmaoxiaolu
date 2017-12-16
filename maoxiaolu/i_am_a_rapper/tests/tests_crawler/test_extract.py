import unittest
import os
import pickle
from random import choice
import re

from maoxiaolu.i_am_a_rapper.settings import BASE_DIR
from maoxiaolu.i_am_a_rapper.extract import filter_some_row, strip_timestamp_from_raw_data, find_rhyme_index


class TestExtract(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        _data_dir = os.path.join(BASE_DIR, 'data')
        _artist = choice(os.listdir(_data_dir))
        _artist_dir = os.path.join(_data_dir, _artist)
        _lyric = choice(os.listdir(_artist_dir))
        with open(os.path.join(_artist_dir, _lyric), 'rb') as rf:
            cls.raw_data = pickle.load(rf)

    def test_strip_timestamp_from_raw_data(self):
        _data = strip_timestamp_from_raw_data(self.raw_data)
        self.assertEqual(re.findall('\[\d{2}:\d{2}\.\d{2}]', _data), [])

    def test_filter_some_row(self):
        _row = ' 作曲：满舒克'
        self.assertEqual(filter_some_row(_row), True)

    def test_find_rhyme_index(self):
        _pinyin = ['jiu', 'jie']
        self.assertEqual(find_rhyme_index(_pinyin), '13:12')


if __name__ == '__main__':
    unittest.main()
