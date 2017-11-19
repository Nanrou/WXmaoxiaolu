import json
from datetime import timedelta
from random import sample

from redis import Redis
from werobot.replies import ImageReply

from .app import robot, local_client
from .tuling import talk_api


redis_db = Redis(db=2)


@robot.subscribe
def say_hi(message):
    return '谢谢你关注毛小露呀~\n回复 我要看猫 就可以看猫啦'


@robot.text
def handle_text(message):
    return message.content
    # if message == '我要看猫':
    #     if redis_db.exists('cat:imgs'):
    #         imgs = redis_db.smembers('cat:imgs')
    #     else:
    #         tmp_json = local_client.get_media_list('image', 0, 20)
    #         tmp = json.loads(tmp_json)
    #         tmp_imgs = tmp.get('items')
    #         imgs = []
    #         for item in tmp_imgs:
    #             imgs.append(item.get('media_id'))
    #         redis_db.sadd('cat:imgs', imgs)
    #     redis_db.expire('cat:imgs', timedelta(days=1))
    #     if len(imgs) > 0:
    #         that_img = sample(imgs, 1)[0]
    #         return ImageReply(media_id=that_img)
    #     else:
    #         return '猫猫都出去了'
    # else:
    #     return talk_api(message)

