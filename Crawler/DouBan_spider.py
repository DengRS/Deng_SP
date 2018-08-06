import requests, time
import urllib.parse
import json, csv
from requests.packages import urllib3

headers = {
    'Host': 'movie.douban.com',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Referer': 'https://movie.douban.com/tag/'}

def get_page(Url):
    """请求网页内容"""
    try:
        response = requests.get(Url, headers=headers, verify=False) #关闭证书验证
        urllib3.disable_warnings()  # 忽略证书验证的警告
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response.text
        return None
    except Exception:
        return None

def douban_spider():
    """存储在csv文件中"""
    lyst = []
    for i in range(0, 100, 20): #网页的页数
        from_data = {
            'sort': 'T',
            'range': '0,10',
            'tags': '',
            'start': i,
            'genres': '剧情'
        }
        print("正在下载第%d页数据" % ((i // 20) + 1))
        url = "https://movie.douban.com/j/new_search_subjects?"
        data = urllib.parse.urlencode(from_data)
        page_url = url + data
        html = get_page(page_url)
        if html != None:
            page = json.loads(html)
            for info in page.get('data'):
                tuple = (info.get('title'), info.get('directors')[0], info.get('rate'), info.get('url'))
                lyst.append(tuple)
            time.sleep(2)
    head = ['片名', '导演', '评分', '链接']
    rows = lyst
    with open('C:/Users/deng_/Desktop/豆瓣影评.csv', 'a') as file:
        f_csv = csv.writer(file)
        f_csv.writerow(head)
        f_csv.writerows(rows)


if __name__ == "__main__":
    douban_spider()
