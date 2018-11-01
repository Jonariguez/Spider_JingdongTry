from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import time
import re
from pyquery import PyQuery as pq

#打开chrome浏览器
browser = webdriver.Chrome()
#设置最长等待时间为10秒
wait = WebDriverWait(browser,10)

<<<<<<< HEAD:Try_selenium.py
=======
#所有的sleep为了是减慢速度，防止被检查异常
>>>>>>> 75e3b3673de22edce474881147ed8b485529f323:Method_First/Try_selenium.py
def do_try(url):
    try:
        #切换到选项卡1
        browser.switch_to.window(browser.window_handles[1])
        #访问商品网页
        browser.get(url)
        #停2秒
        time.sleep(2)
        #获取申请试用的botton
        button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#product-intro > div.info > div.try-info.clearfix.bigImg > div.info-detail.chosen > div > div.btn-wrap > a'))
        )
<<<<<<< HEAD:Try_selenium.py
        #如果上面写的不是申请试用，就申请下一个
=======
        #如果按钮不是‘申请使用’，则说明该商品申请出错或者已经申请过了，则跳回到试用商品列表界面
>>>>>>> 75e3b3673de22edce474881147ed8b485529f323:Method_First/Try_selenium.py
        if button.text!='申请试用':
            #切换到选项卡0
            browser.switch_to.window(browser.window_handles[0])
            return
        #点击申请试用
        button.click()
<<<<<<< HEAD:Try_selenium.py
        #找到关注并申请的按钮
=======
        #等待关注商铺的信息出来，然后点击关注即可。如果无需关注，则可能会抛出超时异常
>>>>>>> 75e3b3673de22edce474881147ed8b485529f323:Method_First/Try_selenium.py
        button2 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.ui-dialog > div.ui-dialog-content > div > div > div.btn > a.y'))
        )
        
        time.sleep(1)
        #点击关注
        button2.click()
        #此时试用一件商品完成
        time.sleep(2)
        #切换到选项卡0
        browser.switch_to.window(browser.window_handles[0])
    #抛出超时异常
    except TimeoutException:
<<<<<<< HEAD:Try_selenium.py
        #切换到选项卡0
        browser.switch_to.window(browser.window_handles[0])
        #这件商品不申请了，返回
=======
        browser.switch_to.window(browser.window_handles[0])     #抛出超时异常则返回到试用商品列表界面即可
>>>>>>> 75e3b3673de22edce474881147ed8b485529f323:Method_First/Try_selenium.py
        return


def get_try(page):
    url='https://try.jd.com/activity/getActivityList'+'?page='+str(page)
    browser.get(url)

    #获取网页的html源码
    html = browser.page_source

<<<<<<< HEAD:Try_selenium.py
    #初始化pyquery
    doc = pq(html)

    #CSS选择器 找出总页数
    pageitem = doc('.root61 .container .w .p-wrap .p-skip').items()
    #为了应对命名空间而采用的粗暴办法
    pagestr = list(pageitem)[0].text()
    pagestr = pagestr[2:]
    pagestr = pagestr[0:pagestr.find('\n')]
    pagenum = int(pagestr)
    print("商品总页数：" + str(pagenum) )

    for i in range(pagenum):

        if i >=1:
            #切换到下一页
            browser.get('https://try.jd.com/activity/getActivityList?page='+str(i+1))
            #停2秒
            time.sleep(2)
        html = browser.page_source
        doc = pq(html)
        #CSS选择器 找出未申请的商品列表
        items = doc('.root61 .container .w .goods-list .items .con .clearfix .item .try-item .link').items()
        #print(type(items))
        #print(items)
        #迭代器转换为list类型
        items=list(items)
        #items = items[0:2]
        if i == 0:
            #执行js脚本 打开一个新选项卡
            browser.execute_script('window.open()')
        
        for item in items:
            #停1秒
            time.sleep(1)
            #试用该商品
            do_try('https:'+item.attr('href'))
            #停2秒
            time.sleep(2)

        print('第'+str(i)+'页申请完成')
=======
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
>>>>>>> 75e3b3673de22edce474881147ed8b485529f323:Method_First/Try_selenium.py



if __name__ == '__main__':
    browser.get('https://www.jd.com/')
<<<<<<< HEAD:Try_selenium.py
    #睡眠60以足够来手动登陆，这样就获得了cookies
    time.sleep(60)
    get_try()
=======

    #睡眠50以足够来手动登陆，这样就获得了cookies
    time.sleep(50)
    Control_try(2)
>>>>>>> 75e3b3673de22edce474881147ed8b485529f323:Method_First/Try_selenium.py
