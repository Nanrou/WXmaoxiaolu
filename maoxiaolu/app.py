import os
import sys
import logging
import json
from datetime import timedelta
from random import sample
from logging import handlers

BASEPATH = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger('wx')
logger.setLevel(logging.DEBUG)

handler = handlers.RotatingFileHandler(
    'wx',
    maxBytes=10,
    backupCount=3,
)
logger.addHandler(handler)

sys.path.append(os.path.abspath('.'))

from redis import Redis
from werobot import WeRoBot
from werobot.client import Client
from werobot.config import Config
from werobot.logger import enable_pretty_logging
from werobot.replies import ImageReply

from tuling import talk_api

enable_pretty_logging(logger, 'debug')

dev = Config(
    TOKEN='luluaiamao',
    SERVER="auto",
    HOST="127.0.0.1",
    PORT="8888",
    SESSION_STORAGE=None,
    APP_ID='wx75358df345194f95',
    APP_SECRET='5cb7f57f79672901572e8832977cb469',
    ENCODING_AES_KEY='GSNR3TnAcalECiQXixBTwrTmO3qdHTXRfQH8XiFcLQj'

)

cc = dev
robot = WeRoBot(config=cc)
local_client = Client(config=cc)
redis_db = Redis(db=2)


@robot.subscribe
def say_hi(message):
    return '谢谢你关注毛小露呀~\n回复 我要看猫 就可以看猫啦'


@robot.text
def handle_text(message):
    if message == '我要看猫':
        if redis_db.exists('cat:imgs'):
            imgs = redis_db.smembers('cat:imgs')
        else:
            tmp_json = local_client.get_media_list('image', 0, 20)
            tmp = json.loads(tmp_json)
            tmp_imgs = tmp.get('items')
            imgs = []
            for item in tmp_imgs:
                imgs.append(item.get('media_id'))
            redis_db.sadd('cat:imgs', imgs)
        redis_db.expire('cat:imgs', timedelta(days=1))
        if len(imgs) > 0:
            that_img = sample(imgs, 1)[0]
            return ImageReply(media_id=that_img)
        else:
            return '猫猫都出去了'
    else:
        return talk_api(message)


if __name__ == '__main__':
    robot.run()
