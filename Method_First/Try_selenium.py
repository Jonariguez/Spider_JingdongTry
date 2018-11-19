#coding=utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import time
import re
from pyquery import PyQuery as pq

#browser_for_login为正常浏览器，用于登录
browser_for_login = webdriver.Chrome()

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
#无头模式
browser = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(browser,10)

#所有的sleep为了是减慢速度, 防止被检查异常
def do_try(url):
    try:
        browser.switch_to.window(browser.window_handles[1])
        browser.get(url)
        time.sleep(2)
        button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#product-intro > div.info > div.try-info.clearfix.bigImg > div.info-detail.chosen > div > div.btn-wrap > a'))
        )
        #如果按钮不是‘申请使用’，则说明该商品申请出错或者已经申请过了，则跳回到试用商品列表界面
        if button.text!='申请试用':
            browser.switch_to.window(browser.window_handles[0])
            return
        button.click()
        #等待关注商铺的信息出来，然后点击关注即可。如果无需关注，则可能会抛出超时异常
        button2 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.ui-dialog > div.ui-dialog-content > div > div > div.btn > a.y'))
        )
        time.sleep(1)
        button2.click()

        time.sleep(2)
        browser.switch_to.window(browser.window_handles[0])
    except TimeoutException:
        browser.switch_to.window(browser.window_handles[0])     #抛出超时异常则返回到试用商品列表界面即可
        return


def get_try(page):
    url='https://try.jd.com/activity/getActivityList'+'?page='+str(page)
    browser.get(url)

    time.sleep(2)

    html = browser.page_source
    #print(html)

    #利用PyQuery获得所有关于试用商品跳转的class=item的<li>标签
    doc = pq(html)
    #因为已经申请过的商品的<li>标签中的class除了item，还有applied，故将其删除之后申请便可跳过已申请的商品
    doc('.applied').remove()
    items = doc('.root61 .container .w .goods-list .items .con .clearfix .item').items()
    #print(type(items))
    #print(items)
    items=list(items)

    for item in items:
        #获得每个商品的标题，如果进行商品过滤则有可能有用
        title = item('.p-name').text()
        try_url = 'https:'+item('.link').attr('href')
        print(title)
        print(try_url)
        time.sleep(1)
        do_try(try_url)
        print("申请成功")
        print('')


def Control_try(total_page):
    browser.execute_script('window.open()')
    browser.switch_to.window(browser.window_handles[0])
    for page in range(1,total_page+1):
        print('开始申请第'+str(page)+'页')
        get_try(page)
        print('第'+str(page)+'页申请完成')

#成功登录后将browser_for_login的cookies取出放到无头browser中即可
def login():
    browser_for_login.get('https://www.jd.com')
    #睡眠40秒以有足够时间来登录
    time.sleep(40)
    cookies = browser_for_login.get_cookies()
    browser_for_login.close()
    browser.get('https://www.jd.com')
    for cookie in cookies:
        browser.add_cookie(cookie)

    browser.get('https://www.jd.com')


if __name__ == '__main__':
    login()
    #申请前3页
    Control_try(3)