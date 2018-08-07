import requests
from requests.exceptions import RequestException
from lxml import etree
import time
import jieba
import wordcloud
import re
from collections import Counter


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
           'Referer': 'https://www.cangqionglongqi.com/wukongzhuan/',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'}

def get_page(url):
    """请求网页内容"""
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response.text
        return None
    except RequestException as error:
        print('报错:',error)
        exit()
        
def parser_page_url(html_href):
    """
    解析链接、章节
    :param link_href:链接
    :param list_chapter:章节
    """
    page_content = etree.HTML(html_href)
    link_href = page_content.xpath('//*[@id="list"]/dl/dd/a/@href')
    list_chapter = page_content.xpath('//*[@id="list"]/dl/dd/a/text()')
    return (link_href, list_chapter)

def parser_content(url):
    """解析小说内容"""
    html_content = get_page(url)
    content = ''
    if html_content:
        page_contents = etree.HTML(html_content)
        contents = page_contents.xpath('//*[@id="content"]/text()')
        for i in contents:
            content += (i+'\n')
        return content.replace('\xa0'*5,'\n')

def get_urls():
    """
    拼接url
    :params urls:各个章节的url
    """
    url = 'https://www.cangqionglongqi.com/wukongzhuan/'
    html = get_page(url)
    hrefs,chapters = parser_page_url(html)
    urls = [url + href for href in hrefs]
    return (urls,chapters)

def write_txt(writer, chapt):
    """保存在txt文件"""
    with open('悟空传.txt','a',encoding='utf-8') as file:
        file.write('*'*10+chapt+'*'*10)
        file.write(writer)

def jiebas(dict=dict()):
    """jieba分析小说并提取出现次数较多的词语    """
    file = open('悟空传.txt','r',encoding='utf-8').read()
    replace_text = re.sub('\W','',file)
    words = jieba.lcut(replace_text)
    c = Counter(words)
    common_c = c.most_common(200)
    for key, value in common_c:
        if len(key) >= 2: #提取大于两个词的词语
            dict[key] = value
    return dict

def wordclouds(dict):
    """生成词云"""
    w = wordcloud.WordCloud()
    w.generate_from_frequencies(dict)
    w.to_file('wukongzhuan.jpg')

if __name__ == '__main__':
    page_urls, page_chapter = get_urls()
    for num in range(len(page_urls)-1):
        print('正在抓取%s' % page_chapter[num])
        write = parser_content(page_urls[num])
        write_txt(write, page_chapter[num])
        time.sleep(15)
    print('抓取完成')
    print('生成词云')
    dict1 = jiebas()
    wordclouds(dict1)
    print('完成')



    

