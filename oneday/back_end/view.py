import re
from datetime import datetime

from scrape_util import calculate_datetime, get_data_from_redis


def welcome(name=None):
    if name is None:
        return {'message': 'Welcome to API Star!'}
    return {'message': 'Welcome to API Star, %s!' % name}


def that_day(date_string):
    if not re.match('\d{4}-\d{1,2}-\d{1,2}', date_string):
        _now = datetime.now()
        date_string = '{}-{}-{}'.format(*[str(x) for x in [_now.year, _now.month, _now.day]])
    _p, _r = calculate_datetime(date_string)
    _data = get_data_from_redis(date_string)[0]
    return {'passed_day': _p, 'remain_day': _r, 'data': _data}
