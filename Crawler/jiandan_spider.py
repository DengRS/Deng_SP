from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
import requests
import os

'''屏蔽掉浏览器界面'''
URL = 'http://jandan.net/ooxx/page-3'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options = chrome_options)
wait = WebDriverWait(browser, 10)
browser.get(URL)


def next_page():  # 点击下一页
    button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'previous-comment-page')))
    return button

def current_page():  # 获取当前页数
    page = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'current-comment-page')))
    return page.text

def parse_html(lyst):
    """
    :param img:单个图片链接
    :param lyst:存储图片链接
    """
    imgs_info = browser.find_elements_by_xpath('//*[@id="comments"]/ol/li//p/img')
    for img in imgs_info:
        img = img.get_attribute('src')
        if img[len(img) - 3:] == 'jpg':  # 剔除广告的'.gif'图片
            lyst.append(img)


def dowmloader(url):
    '''图片下载'''
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        return None
    except Exception:
        return None


def save_img(img_content, num):
    """
    :param img_content:二进制数据
    :param num:图片保存的次序
    """
    with open(str(num) + '.jpg', 'wb') as f:
        f.write(img_content)


def jandan_crawler(lyst):
    '''
    :param max_page:抓取网页的最大页数
    '''
    try:
        max_page = current_page()
        pages = int(max_page[1:len(max_page) - 1])
        for page in range(pages,1,-1):
            print('正在抓取煎蛋网第%d页图片' % page)
            parse_html(lyst)
            time.sleep(3)
            button = next_page()
            button.click()
        return lyst
    except TimeoutException:
        print("超时,程序退出")
        exit()


if __name__ == '__main__':
    os.chdir('C:/Users/deng_/Desktop/jiandan')
    lyst = []
    num = 1
    url_info = jandan_crawler(lyst)
    for url in url_info:
        img_content = dowmloader(url)
        if img_content:
            print('正在保存图片：' + str(num) + '.jpg')
            save_img(img_content, num)
            num += 1
    print('煎蛋网图片抓取完成')
    browser.close()