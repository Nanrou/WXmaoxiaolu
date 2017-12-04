from .extract import get_pinyin_from_word, find_rhyme_index
from .db_opt import MyRedis


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
    pass
