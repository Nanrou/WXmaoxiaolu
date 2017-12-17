from extract import get_pinyin_from_word, find_rhyme_index
from db_opt import MyRedis
from random import sample
from codecs import decode
from collections import OrderedDict


def turn_informal_string_back_to_string(informal_string):
    print(informal_string.strip()[1:].strip("'"))
    pattern = "b{!a}.decode()".format(informal_string.strip()[1:].strip("'"))
    res = eval(pattern)
    return res


class Rapper:
    def __init__(self, redis=None):
        self.redis = MyRedis(redis)

    def get_words(self, content):
        rhyme_words = '有点尴尬'
        if len(content) == 2:
            _rhyme_index = find_rhyme_index(get_pinyin_from_word(content))
            if self.redis.exists(_rhyme_index):
                rhyme_words = self.redis.get(_rhyme_index)
        return rhyme_words


if __name__ == '__main__':
    import redis

    rr = redis.Redis(db=2)
    api = Rapper(rr)
    ans = api.get_words('老王')
    print(ans)
