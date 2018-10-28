from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import time
from pyquery import PyQuery as pq


browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
#product-intro > div.info > div.try-info.clearfix.bigImg > div.info-detail.chosen > div > div.btn-wrap > a
#product-intro > div.info > div.try-info.clearfix.bigImg > div.info-detail.chosen > div > div.btn-wrap > a
def do_try(url):
    try:
        browser.switch_to.window(browser.window_handles[1])
        browser.get(url)
        time.sleep(2)
        button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#product-intro > div.info > div.try-info.clearfix.bigImg > div.info-detail.chosen > div > div.btn-wrap > a'))
        )
        if button.text!='申请试用':
            browser.switch_to.window(browser.window_handles[0])
            return
        button.click()
        button2 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.ui-dialog > div.ui-dialog-content > div > div > div.btn > a.y'))
        )
        time.sleep(1)
        button2.click()

        time.sleep(2)
        browser.switch_to.window(browser.window_handles[0])
    except TimeoutException:
        do_try(url)


def get_try():
    browser.get('https://try.jd.com/')
    browser.get('https://try.jd.com/activity/getActivityList')

    html = browser.page_source
    doc = pq(html)
    items = doc('.root61 .container .w .goods-list .items .con .clearfix .item .try-item .link').items()
    print(type(items))
    print(items)
    items=list(items)

    browser.execute_script('window.open()')
    i=0
    for item in items:
        i+=1
        print(item.attr('href'))
        time.sleep(1)
        do_try('https:'+item.attr('href'))
        time.sleep(2)
        if i==20:
            break



if __name__ == '__main__':
    browser.get('https://www.jd.com/')
    #睡眠50以足够来手动登陆，这样就获得了cookies
    time.sleep(50)
    get_try()