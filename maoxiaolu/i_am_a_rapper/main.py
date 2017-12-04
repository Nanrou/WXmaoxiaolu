import os
import pickle

from settings import BASE_DIR, MyLogger
from crawler import handler_single_artist
from extract import handler_single_lyric
from db_opt import MyRedis


logger = MyLogger(os.path.abspath(__file__).split('/')[-1])

ARTIST_DICT = {'红花会': '1049144', 'PGone': '1197115', 'VaVa': '1038099', 'AY楊佬叁': '12258420', '艾福杰尼': '12127564',
               'BooM黄旭': '12065096', 'Bridge': '12493701', 'GAI爷': '1211046', 'TizzyT': '1204010',
               'JonyJ': '784257', '小青龙': '12199576', '辉子': '12371082', '孙八一': '1089111', '谢帝': '847107',
               '马思维': '1132392', 'Mc光光': '187903', '性感的拖鞋': '789380', 'Lu1': '4037', '徐真真': '12094099'}


def download_all():
    for artist, id_ in ARTIST_DICT.items():
        logger.debug('------------ start {} ------------'.format(artist))
        handler_single_artist(id_)
        logger.debug('------------ finish {} ------------'.format(artist))


def extract_all():
    _redis = MyRedis()
    _data_dir = os.path.join(BASE_DIR, 'data')
    for artist in os.listdir(_data_dir):
        artist_dir = os.path.join(_data_dir, artist)
        for lyric in os.listdir(artist_dir):
            with open(os.path.join(artist_dir, lyric), 'rb') as rf:
                raw_data = pickle.load(rf)
            try:
                res = handler_single_lyric(raw_data)
            except RuntimeError as e:
                logger.warning('{}: {} is {}'.format(artist, lyric, e))
                continue
            for k, v in res.items():
                if v:  # 防止空值
                    _redis.save(v, k)
            logger.debug('------------ finish {} ------------'.format(lyric))
        logger.debug('------------ finish {} ------------'.format(artist))


if __name__ == '__main__':
    # download_all()
    # extract_all()
    import os
    from os.path import join, getsize
    total_file = 0
    total_size = 0
    for root, dirs, files in os.walk('./data'):
        # print(root, "consumes", end="")
        # print(sum([getsize(join(root, name)) for name in files]), end="")
        # print("bytes in", len(files), "non-directory files")

        total_file += len(files)
        total_size += sum([getsize(join(root, name)) for name in files])
    print(total_file, total_size)
