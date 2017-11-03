# -*- coding:utf-8 -*-

import hashlib
import web
import os
from lxml import etree
import time
from tuling import talk_api


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

    def POST(self):
        str_xml = web.data()
        xml = etree.fromstring(str_xml)
        msgTpye = xml.find('MsgType').text
        fromUser = xml.find('FromUserName').text
        userid = fromUser.split('-')[-1]
        toUser = xml.find('ToUserName').text
        if msgTpye == 'text':
            content = xml.find('Content').text
            recontent = talk_api(content, userid)
            return self.render.reply_text(fromUser, toUser, int(time.time()), recontent)
        elif msgTpye == 'voice':
            content = xml.find('Recognition').text
            recontent = talk_api(content, userid)
            return self.render.reply_text(fromUser, toUser, int(time.time()), recontent)
        elif msgTpye == 'image':
            pass
        else:
            pass
