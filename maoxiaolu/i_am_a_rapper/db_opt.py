from random import randint
import pickle

import redis


class MyRedis:
    def __init__(self, rr=None):
        if rr is None:
            self.redis = redis.Redis()
        else:
            self.redis = rr

    def save(self, rhyme_index, word):
        return self.redis.sadd(rhyme_index, word)

    def get(self, rhyme_index, count=None):
        if count is None:
            count = randint(5, 8)
        return [word.decode() for word in self.redis.srandmember(rhyme_index, number=count)]

    def exists(self, rhyme_index):
        return self.redis.exists(rhyme_index)

    def dump(self):
        _dump_obj = {}
        for key in self.redis.keys('*:*'):
            _dump_obj[key] = tuple(self.redis.smembers(key))
        with open('rapper_dump.pickle', 'wb') as wf:
            pickle.dump(_dump_obj, wf)

    def load(self, file):
        with open(file, 'rb') as rf:
            _rapper_obj = pickle.load(rf)
        for k, vs in _rapper_obj.items():
            for v in vs:
                self.redis.sadd(k, v)


if __name__ == '__main__':
    tt = redis.Redis(db=2)
    db = MyRedis(tt)
    db.load('./rapper_dump.pickle')
