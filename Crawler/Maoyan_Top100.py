import requests
from requests.exceptions import RequestException
import re
import time
import pymongo

def get_page(url,headers):
    """请求网页内容"""
    try:
        response = requests.get(url,headers,timeout=30)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response.text
        return None
    except RequestException:
        return None
    
    
def parse_page(html):
    """解析网页内容"""
    pattern = re.compile('<dd>.*?board-index.*?>(\d+).*?name"><a.*?>(.*?)</a>'
                         +'.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?'
                         +'.*?"integer">(\d\.)</i>.*?fraction">(\d)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
        '排行': item[0],
        '电影名': item[1].strip(),
        '评分': item[4] + item[5],
        '演员': item[2].strip()[3:],
        '上映时间': item[3].strip()[5:]}
        
        
def write_mongodb(content):
    """存入MongoDB"""
    client = pymongo.MongoClient('localhost',27017)
    db = client.Maoyan_Top100
    collection = db.maoyan_data
    ret = collection.insert_one(content)
    print('id:',ret.inserted_id)


def crawler(url,headers):
    html = get_page(url, headers)
    for content in parse_page(html):
        write_mongodb(content)


if __name__ == '__main__':
    urls = ['http://maoyan.com/board/4?offset={}'.format(offset) for offset in range(0,100,10)]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    for url in urls:
        crawler(url, headers)
        time.sleep(3)
    print("完成")