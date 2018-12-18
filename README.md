# Spider_JingdongTry
用python爬虫模拟浏览器来自动申请京东试用。<br>
注意：此程序仅作为学习爬虫练习使用，不得扩散出去另作他用。<br>

### README 目录
* [依赖](#依赖)
* [Method_First](#Method_First)
  * [使用说明](#使用说明)
  * [功能特点](#功能特点)
* [Method_Second](#Method_Second)
  * [使用说明](#使用说明-1)
  * [功能特点](#功能特点-1)
  * [待实现的功能](#待实现的功能)
* [参考资料](#参考资料)

### 依赖
* Python 3.6
* ChromeDriver([官网地址](https://sites.google.com/a/chromium.org/chromedriver/))
* selenium 3.14.1
* pyquery 1.4

## Method_First
作者：[Jonariguez](https://github.com/Jonariguez)

* 已经申请过的商品就不会再申请了
* 申请的时候采用**headless模式**进行，就不用浏览器界面了，无限接近**无扰模式**
* 程序开始运行时会打开Chrome浏览器并打开[京东官网登录界面](https://passport.jd.com/new/login.aspx),只需要在该浏览器登录即可，登录成功之后浏览器会关闭，此时便开始申请商品。

### 使用说明
1. **先根据config.py完成自定义设置**
2. 直接运行Try_selenium.py文件即可
3. 程序开始会自动打开浏览器，手动登录账号
4. 登录成功后浏览器会及时关闭，程序开始申请试用

### 功能特点
- [x] 采用headless模式，无浏览器界面
- [x] 分离自定义设置文件config
- [x] 指定申请商品个数或者页数
- [x] 可自定义用户登录所用时间(**该功能已删除并改进为即登即申**)
- [x] 是否申请完成后自动关机
- [x] 只申请自己喜欢的商品并可过滤掉不喜欢的商品
  - [x] 按商品名称
  - [ ] 按商品价格
- [x] 登录成功直接开始申请，无需等待


## Method_Second
作者：[jzplp](https://github.com/jzplp)

### 使用说明
1. 鼠标双击打开mian.py文件。（执行）
2. 程序自动打开浏览器，显示京东登陆界面。
3. 人工手动登陆京东账号。
4. 程序自动检测登陆成功，自动关闭浏览器，并开始试用。
5. 程序运行可能需要一小时左右，试用结束后会自动关闭。试用期间不能关闭(黑色的)命令窗口。

### 功能特点
* 代码是在Method_First的之前代码上改动的。
* 自动检测是否登陆成功
* 登陆成功后自动关闭浏览器，以headless模式运行
* 商品过滤
  * 控制商品售价，低于某个数值便不申请
  * 实现了简单的关键字过滤功能，出现某些关键字便不申请
* 限制每天申请商品的个数，超过便不申请
* 可以控制申请商品的类别
* 在商品列表页面排除已经申请过的和过滤掉的商品
* 申请完成后自动在log.txt中记录申请的时间和申请数量

### 待实现的功能
- [ ] 优化程序结构
- [x] 在商品列表处剔除已经申请过的商品
- [x] 自动检测登陆成功并5秒后开始试用
- [x] 登陆成功后自动关闭浏览器，用headless模式试用
- [ ] 断点续申
  - [ ] 记录申请过的类别和页数，当天第二次打开时从此处开始继续
  - [ ] 记录申请过的商品数，当天第二次打开时继续计数
- [ ] 申请完成可以自动关闭电脑
- [ ] 添加图形界面


## 参考资料
* Python3网络爬虫开发实战  <br>
  https://germey.gitbooks.io/python3webspider/content/
* xmlns属性导致pyquery查询元素失败 <br>
  https://blog.csdn.net/zx1245773445/article/details/82821642
* python3 chromedriver + selenium 禁止日志console打印 <br>
  https://www.websoft88.com/seo/article/3743.html