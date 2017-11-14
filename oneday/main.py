from datetime import datetime
import re

import requests
from bs4 import BeautifulSoup, NavigableString


HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}


def download_page(uri):
    resp = requests.get(uri, headers=HEADER)

    with open('home.html', 'w', encoding='utf-8') as wf:
        wf.write(resp.text)


def scrape_home():
    with open('home.html', 'r', encoding='utf-8') as rf:
        soup = BeautifulSoup(rf, 'lxml')
        div = soup.find(id='mp-2012-column-otd-block').find(id='column-otd')
        date = div.p.span.string
        dts = []
        for item in div.dl.find_all('dt'):
            dts.append(item.a.string)
        dds = []
        for item in div.dl.find_all('dd'):
            dds.append(''.join(item.stripped_strings))
        res = []
        for dt, dd in zip(dts, dds):
            res.append((dt, dd))
    return date, res


def scrape_detail():
    with open('home.html', 'r', encoding='utf-8') as rf:
        soup = BeautifulSoup(rf, 'lxml')
        date_string = soup.find(id='firstHeading').string
        date = datetime(datetime.now().year, *[int(x) for x in re.findall('\d+', date_string)])
        passed_day = (date - datetime(datetime.now().year, 1, 1)).days + 1
        remain_day = (datetime(datetime.now().year + 1, 1, 1) - date).days - 1
        all_items = []
        all_h3 = soup.find(class_='mw-parser-output').find_all('h3')
        for h3 in all_h3:
            uls = h3.find_next_sibling('ul')
            for li in uls.find_all('li'):
                all_items.append(''.join(li.stripped_strings))
        return (passed_day, remain_day), all_items


if __name__ == '__main__':
    scrape_detail()

