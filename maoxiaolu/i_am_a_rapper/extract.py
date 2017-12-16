import os
import json
import re
from random import choice
import pickle

import jieba
from pypinyin import lazy_pinyin

from settings import BASE_DIR, MyLogger

logger = MyLogger(os.path.abspath(__file__).split('/')[-1])

RhymeIndex = [('1', ['a', 'ia', 'ua']), ('2', ['ai', 'uai']), ('3', ['an', 'ian', 'uan']),
              ('4', ['ang', 'iang', 'uang']), ('5', ['ao', 'iao']), ('6', ['e', 'o', 'uo']), ('7', ['ei', 'ui']),
              ('8', ['en', 'in', 'un']), ('9', ['eng', 'ing', 'ong', 'iong']), ('10', ['er']), ('11', ['i']),
              ('12', ['ie', 'ye']), ('13', ['ou', 'iu']), ('14', ['u']), ('16', ['ue']),
              ('15', ['qu', 'xu', 'yu', 'v'])]

RhymeDict = {'ui': '7', 'uan': '3', 'ian': '3', 'iu': '13', 'en': '8', 'ue': '16', 'ing': '9', 'a': '1', 'ei': '7',
             'eng': '9', 'uo': '6', 'ye': '12', 'in': '8', 'ou': '13', 'ao': '5', 'uang': '4', 'ong': '9', 'ang': '4',
             'ai': '2', 'ua': '1', 'uai': '2', 'an': '3', 'iao': '5', 'ia': '1', 'ie': '12', 'iong': '9', 'i': '11',
             'er': '10', 'e': '6', 'u': '14', 'un': '8', 'iang': '4', 'o': '6', 'qu': '15', 'xu': '15', 'yu': '15',
             'v': '15'}


def strip_timestamp_from_raw_data(raw_data):
    try:
        data = raw_data.get('lrc').get('lyric')
    except AttributeError:
        raise RuntimeError('cant find lrc in file')
    try:
        data = re.sub('\[\d{2}:\d{2}\.\d{2}]', '', data)
    except TypeError:
        raise RuntimeError('wrong data type')
    return data


SPECIAL_STINGS = ('作词', '作曲', '编曲', '监制', 'by', '混音')


def filter_some_row(single_row):
    return any(s in single_row for s in SPECIAL_STINGS)


def split_words(single_row):
    return jieba.cut(single_row, cut_all=True)


def get_pinyin_from_word(words):
    return lazy_pinyin(words, errors='ignore')


def find_rhyme_index(pinyin):  # 找到韵脚对应的index
    rhyme_index = []
    for one in pinyin:
        while one:
            if one in RhymeDict:
                rhyme_index.append(RhymeDict[one])
                break
            one = one[1:]
        else:
            logger.info('cant find rhyme: {}'.format(pinyin))
            return '0:0'
    return ':'.join(rhyme_index)


def handler_single_lyric(raw_data):
    data = strip_timestamp_from_raw_data(raw_data)
    word_rhyme_dict = {}
    for row in data.split('\n'):
        row = row.strip()
        if len(row) < 2 or filter_some_row(row):
            continue
        all_word = set(i for i in split_words(row) if len(i) == 2)
        all_word.add(row[-2:])
        for word in all_word:
            word_rhyme_dict[word] = find_rhyme_index(get_pinyin_from_word(word))
    return word_rhyme_dict


if __name__ == '__main__':
    _data_dir = os.path.join(BASE_DIR, 'data')
    _artist = choice(os.listdir(_data_dir))
    _artist_dir = os.path.join(_data_dir, _artist)
    _lyric = choice(os.listdir(_artist_dir))
    with open(os.path.join(_artist_dir, _lyric), 'rb') as rf:
        raw_data = pickle.load(rf)
    res = handler_single_lyric(raw_data)
    print(res)

    from db_opt import MyRedis

    rr = MyRedis()
    for k, v in res.items():
        rr.save(v, k)
