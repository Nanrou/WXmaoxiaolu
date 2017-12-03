import redis


class MyRedis:
    def __init__(self):
        self.redis = redis.Redis()

    def save(self, rhyme_index, word):
        self.redis.sadd(rhyme_index, word)

    def get(self, rhyme_index, count=5):
        self.redis.srandmember(rhyme_index, number=count)


if __name__ == '__main__':
    pass