import redis


class MyRedis:
    def __init__(self):
        self.redis = redis.Redis()

    def save(self, rhyme_index, word):
        return self.redis.sadd(rhyme_index, word)

    def get(self, rhyme_index, count=5):
        return [word.decode('utf-8') for word in self.redis.srandmember(rhyme_index, number=count)]

    def exists(self, rhyme_index):
        return self.redis.exists(rhyme_index)

    def dump(self):
        pass


if __name__ == '__main__':
    pass