import pickle

import requests

# 能成功访问到网页
resp = requests.get('http://music.163.com/#/artist?id=188141')
assert resp.status_code == 200
assert '满舒克' in resp.text

# 爬取到信息
# 保存到本地


# 打开一个文件
# 确认里面有歌词
# 对歌词进行分割
# 存入DB中