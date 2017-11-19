import requests
import json


def talk_api(content, userid=None):
    s = requests.session()
    url = 'http://www.tuling123.com/openapi/api'
    da = {'key': '27dff84a92ec4a8eae1d354686db907a', 'info': content, 'userid': userid}
    data = json.dumps(da)
    r = s.post(url, data=data)
    j = eval(r.text)  # turn str to dict
    code = j['code']
    if code == 100000:
        recontent = j['text']
    elif code == 200000:
        recontent = j['text'] + j['url']
    elif code == 302000:
        recontent = j['text'] + j['list'][0]['info'] + j['list'][0]['detailurl']
    elif code == 308000:
        recontent = j['text'] + j['list'][0]['info'] + j['list'][0]['detailurl']
    elif code == 40004:
        recontent = 'see you tomorrow'
    else:
        recontent = 'xixixi'
    return recontent


if __name__ == '__main__':
    print(talk_api('你妈妈是谁'))
