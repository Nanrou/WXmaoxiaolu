from extract import get_pinyin_from_word, find_rhyme_index
from db_opt import MyRedis
from random import choices

class Rapper:
    def __init__(self, redis=None):
        self.redis = MyRedis(redis)

    def get_words(self, content):
        rhyme_words = '有点尴尬'
        if len(content) == 2:
            _rhyme_index = find_rhyme_index(get_pinyin_from_word(content))
            if self.redis.exists(_rhyme_index):
                rhyme_words = self.redis.get(_rhyme_index)[0]

        if len(rhyme_words) > 4:
            rhyme_words = ','.join(choices(rhyme_words, k=4))
        else:
            rhyme_words = ','.join(rhyme_words)
        return rhyme_words


if __name__ == '__main__':
    pass
