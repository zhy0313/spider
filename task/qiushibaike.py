#!/usr/bin/python
# coding=utf-8
from __init__ import *

def crawl(conn):
    headers = {}
    for i in range(1, 13):
        qiuUrl = 'https://www.qiushibaike.com/8hr/page' + str(i)
        req = requests.get(qiuUrl, headers=headers)
        req.encoding = 'utf-8'
        html = req.content
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        # maindiv = soup.find('div', 'main')
        # div = maindiv.find('div', 'col1')
        tags = soup.find_all('div', 'block')
        curTime = int(time.time())
        cardType = 1
        authorId = 1

        for tag in tags:
            curTime = curTime + 1800
            url = 'https://www.qiushibaike.com' + tag.find('a', 'contentHerf')['href']
            spans = tag.find('a', 'contentHerf').find_all('span')
            desc = spans[0].text
            thumbnail = []
            thumb = tag.find('div', 'thumb')
            if thumb is not None:
                thumb = 'http:' + thumb.find('img')['src']
                thumbnail.append(thumb)
            thumbnail = json.dumps(thumbnail)
            try:
                cur = conn.cursor()
                cur.execute("SET NAMES utf8");
                sql = "insert into dis_entertainment (type, author_id, description, thumbnail, url, date) select %s, %s, %s, %s, %s, %s FROM DUAL WHERE NOT EXISTS(SELECT url FROM dis_entertainment WHERE url =%s)";
                cur.execute(sql, (cardType, authorId, desc, thumbnail, url, curTime, url))
            except Exception as err:
                logging.debug(err)
            finally:
                cur.close()
        conn.commit()
        conn.close()
