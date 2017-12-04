import pypinyin

from extract import get_pinyin_from_word, find_rhyme_index
from db_opt import MyRedis


def rapper_api(content):
    rhyme_words = '有点尴尬'
    if len(content) == 2:
        _redis = MyRedis()  # 上线时替换掉
        _rhyme_index = find_rhyme_index(get_pinyin_from_word(content))
        if _redis.exists(_rhyme_index):
            rhyme_words = _redis.get(_rhyme_index)

    return rhyme_words


if __name__ == '__main__':
    print(rapper_api('老王'))
