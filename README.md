# Spider_JingdongTry
用selenium模拟浏览器来自动申请京东试用。<br>
注意：此程序仅作为学习爬虫练习使用，不得扩散出去另作他用。<br>

### 依赖
* Python 3.6
* ChromeDriver([官网地址](https://sites.google.com/a/chromium.org/chromedriver/))
* selenium 3.14.1
* pyquery 1.4

### 使用说明

1. 直接点击py文件即可执行
2. 待浏览器打开京东后，手动登陆京东账户。
3. 等待若干秒后，程序自动执行。
4. 程序运行大概需要一小时以上。期间不能关闭模拟的浏览器。

### 功能
#### Method_First
作者：[Jonariguez](https://github.com/Jonariguez)

* 待添加

#### Method_Second
作者：[jzplp](https://github.com/jzplp)

* 代码是在Method_First的之前代码上改动的。
* 商品售价低于某个数值便不申请
* 实现了简单的商品关键字过滤。
* 统计成功申请的商品个数，每天限制300个
* 可以限制商品类别

### 参考资料

* Python3网络爬虫开发实战  <br>
  https://germey.gitbooks.io/python3webspider/content/
* xmlns属性导致pyquery查询元素失败 <br>
  https://blog.csdn.net/zx1245773445/article/details/82821642
