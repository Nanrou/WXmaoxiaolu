import os
import sys
import logging
from logging import handlers

BASEPATH = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger('wx')
logger.setLevel(logging.DEBUG)

handler = handlers.RotatingFileHandler(
    os.path.join(BASEPATH, 'wx'),
    maxBytes=10,
    backupCount=3,
)
logger.addHandler(handler)

sys.path.append(os.path.abspath('.'))

from werobot import WeRoBot
from werobot.client import Client
from werobot.config import Config
from werobot.logger import enable_pretty_logging

enable_pretty_logging(logger, 'debug')

dev = Config(
    TOKEN='luluaiamao',
    SERVER="auto",
    HOST="127.0.0.1",
    PORT="8888",
    SESSION_STORAGE=None,
    APP_ID='1234567',
    APP_SECRET='1234567',
    #    ENCODING_AES_KEY = 'lulu'
)

cc = dev
robot = WeRoBot(config=cc)
local_client = Client(config=cc)

if __name__ == '__main__':
    robot.run()
