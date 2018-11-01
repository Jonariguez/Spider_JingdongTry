from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import time
import re
from pyquery import PyQuery as pq


browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)

#所有的sleep为了是减慢速度，防止被检查异常
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

    html = browser.page_source

    #利用PyQuery获得所有关于试用商品跳转的class=try-item的div标签
    doc = pq(html)
    items = doc('.root61 .container .w .goods-list .items .con .clearfix .item .try-item').items()
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
        time.sleep(2)

def Control_try(total_page):
    browser.get('https://try.jd.com/')
    browser.execute_script('window.open()')
    browser.switch_to.window(browser.window_handles[0])
    for page in range(1,total_page+1):
        get_try(page)



if __name__ == '__main__':
    browser.get('https://www.jd.com/')

    #睡眠50以足够来手动登陆，这样就获得了cookies
    time.sleep(50)
    Control_try(2)