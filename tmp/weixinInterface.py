# -*- coding:utf-8 -*-

import hashlib
import web
import os
import lxml
from lxml import etree


class WeixinInterface:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        data = web.input()
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr

        token = '123weixin123'

        l = [token, timestamp, nonce]
        l.sort()
        s = l[0]+l[1]+l[2]

        hashcode = hashlib.sha1(s).hexdigest()

        if hashcode == signature:
            return echostr
