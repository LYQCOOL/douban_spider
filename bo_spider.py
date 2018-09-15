# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/8/22 16:40'
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib    # Python中的cURL库
import urllib2    # Python中的cURL库
import time    # 时间函数库，包含休眠函数sleep()
import random
pro = ['122.152.196.126', '114.215.174.227', '119.185.30.75']
url = 'https://www.cnblogs.com/lyq-biu/p/9503941.html'    # 希望刷阅读量的文章的URL
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'    # 伪装成Chrome浏览器
refererData = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=csdn%20%E6%80%9D%E6%83%B3%E7%9A%84%E9%AB%98%E5%BA%A6%20csdnzouqi&oq=csdn%20%E6%80%9D%E6%83%B3%E7%9A%84%E9%AB%98%E5%BA%A6&rsv_pq=fe7241c2000121eb&rsv_t=0dfaTIzsy%2BB%2Bh4tkKd6GtRbwj3Cp5KVva8QYLdRbzIz1CCeC1tOLcNDWcO8&rqlang=cn&rsv_enter=1&rsv_sug3=11&rsv_sug2=0&inputT=3473&rsv_sug4=3753'    # 伪装成是从baidu.com搜索到的文章
data = ''    # 将GET方法中待发送的数据设置为空
headers = {'User-Agent' : user_agent, 'Referer' : refererData}    # 构造GET方法中的Header
count = 0    # 初始化计数器
request = urllib2.Request(url, data, headers,proxies={'http': random.choice(pro)})    # 组装GET方法的请求
while 1:    # 一旦开刷就停不下来
    rec = urllib2.urlopen(request)    # 发送GET请求，获取博客文章页面资源
    page = rec.read()    # 读取页面内容到内存中的变量，这句代码可以不要
    count += 1    # 计数器加1
    print count    # 打印当前循环次数
    if count % 6:    # 每6次访问为1个循环，其中5次访问等待时间为31秒，另1次为61秒
        time.sleep(31)    # 为每次页面访问设置等待时间是必须的，过于频繁的访问会让服务器发现刷阅读量的猥琐行为并停止累计阅读次数
    else:
        time.sleep(61)
print page    # 打印页面信息，这句代码永远不会执行
