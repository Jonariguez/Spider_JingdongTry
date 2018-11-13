"""
京东试用自动申请程序，每天仅需执行一次即可
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import time
from pyquery import PyQuery as pq

#全局变量
#打开chrome浏览器
browser = webdriver.Chrome()
#设置最长等待时间为10秒
wait = WebDriverWait(browser,10)

#打开正确/屏蔽词文件,并处理

def genekeys():
    #打开正确/屏蔽词文件,并处理
    keys = []
    for line in open("Truekeyword.txt", 'r' ,encoding='UTF-8' ):
        line = line[0:line.find('\n')]
        if line == '':
            continue;
        line = line.split('/')
        line[0] = line[0].strip()
        line[1] = line[1].strip()
        if line[0] == '':
            line[0] = []
        else:
            line[0] = line[0].split(' ')
        if line[1] == '':
            line[1] = []
        else:
            line[1] = line[1].split(' ')
        keys.append(line)
    return keys

def goodJudge(goodName, goodPrice, keys):
    """
    根据商品名称和价格判断是否试用该商品
    """
    if goodPrice < 45:
        return False

    for key in keys:
        booltrue = False
        if key[0] == []:
            booltrue = True
        for tk in key[0]:
            if tk == '':
                continue;
            if tk in goodName:
                booltrue = True
                break;
        if booltrue == False:
            continue;
        for tk in key[1]:
            if tk == '':
                continue;
            if tk in goodName:
                return False
    return True

def do_try(url):
    """
    对于某个商品申请试用
    url为申请网址 iApplyNum为当前申请成功的个数
    """
    try:
        #切换到选项卡1
        browser.switch_to.window(browser.window_handles[1])
        #访问商品网页
        browser.get(url)
        #停2秒
        time.sleep(2)

        #获取网页的html源码
        html = browser.page_source

        #初始化pyquery
        doc = pq(html)

        #获取申请试用的botton
        button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#product-intro > div.info > div.try-info.clearfix.bigImg > div.info-detail.chosen > div > div.btn-wrap > a'))
        )
        #如果上面写的不是申请试用，就申请下一个
        if button.text!='申请试用':
            return False
        #点击申请试用
        button.click()
        #找到关注并申请的按钮
        button2 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.ui-dialog > div.ui-dialog-content > div > div > div.btn > a.y'))
        )
        
        time.sleep(1)
        #点击关注
        button2.click()
        #此时试用一件商品完成
        return True
        time.sleep(2)
    #抛出超时异常
    except TimeoutException:
        #这件商品不申请了，返回
        return False


def get_try(cid, iApplyNum, maxApplyNum, keys):
    browser.get('https://try.jd.com/activity/getActivityList?page=1&cids='+cid)

    #获取网页的html源码
    html = browser.page_source

    #初始化pyquery
    doc = pq(html)

    #CSS选择器 找出总页数
    pageitem = doc('.root61 .container .w .p-wrap .p-skip').items()
    #为了应对命名空间而采用的粗暴办法
    pagestr = list(pageitem)[0].text()
    pagestr = pagestr[2:]
    pagestr = pagestr[0:pagestr.find('\n')]
    pagenum = int(pagestr)
    print("商品总页数：" + str(pagenum+1) )

    for i in range(pagenum):

        if i >=1:
            #切换到下一页
            browser.get('https://try.jd.com/activity/getActivityList?page='+str(i+1)+'&cids='+cid)
            #停2秒
            time.sleep(2)
        html = browser.page_source
        doc = pq(html)
        #CSS选择器 找出商品列表
        items = doc('.root61 .container .w .goods-list .items .con .clearfix .item').items()
        
        #迭代器转换为list类型
        items=list(items)
        
        #对于每个商品进行处理
        for item in items:
            #按钮为已申请
            if item('.try-item .try-button').text() == '已申请':
                #已经申请过的不申请
                continue
            #商品名称
            itemname = item('.try-item .p-name').text()
            #商品价格
            itempricetext = item('.try-item .p-price').text()
            #截取多余的文本
            #找不到价格 出现暂无报价的情况
            if itempricetext.find('￥') == -1:
                itemprice = 0
            else:
                itempricetext = itempricetext[itempricetext.find('￥')+1:]
                #goodPrice 商品价格
                itemprice = float(itempricetext)
            if goodJudge(itemname, itemprice, keys) == False:
                #不申请了
                continue
            
            itemurl = item('.try-item .link')
            #试用该商品
            if do_try('https:'+itemurl.attr('href')) == True:
                print("申请成功 " +str(itemprice) + "  " + itemname)
                iApplyNum = iApplyNum + 1
            #停3秒
            time.sleep(3)
            browser.switch_to.window(browser.window_handles[0])

            if iApplyNum >= maxApplyNum:
                print("已经成功申请" + str(maxApplyNum) + "件商品")
                return
        print(cid+'类:第'+str(i+1)+'页申请完成')


def trycate():
    """
    控制申请类型
    """
    #试用类型
    #家用电器737 手机数码652 电脑办公670 家居家装1620 服饰鞋包1315 生鲜美食12218 钟表奢品5025
    cids = ['737', '652' ,'670', '1620', '1315', '12218' ,'5025' , ]
    return cids

def trycid():

    keys = genekeys()
    #京东限制 每天最大申请数量为300件
    maxApplyNum = 300
    iApplyNum = 0
    #试用类型
    cids = trycate()
    browser.get('https://try.jd.com/')
    browser.get('https://try.jd.com/activity/getActivityList')
    #执行js脚本 打开一个新选项卡
    browser.execute_script('window.open()')
    browser.switch_to.window(browser.window_handles[0])
    for cid in cids:
        get_try(cid, iApplyNum, maxApplyNum, keys)


if __name__ == '__main__':
    
    browser.get('https://www.jd.com/')
    #睡眠60以足够来手动登陆，这样就获得了cookies
    time.sleep(60)
    trycid()
