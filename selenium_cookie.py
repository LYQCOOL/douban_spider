from selenium import webdriver
import time
import random
import requests
from bs4 import BeautifulSoup
from xlwt import Workbook
import os


def get_cookies(phone, passwords):
    # 利用selenim模拟登录获取cookie
    try:
        print('开始获取cookie')
        # 打开谷歌浏览器
        opt = webdriver.ChromeOptions()
        # 设置成无界面
        # opt.set_headless()
        driver = webdriver.Chrome(options=opt)
        driver.get('https://movie.douban.com/')
        driver.refresh()
        button = driver.find_elements_by_css_selector('#db-global-nav > div > div.top-nav-info > a.nav-login')
        button[0].click()
        driver.refresh()
        time.sleep(2)
        inputs = driver.find_elements_by_css_selector('#email')
        inputs[0].send_keys(phone)
        pwd = driver.find_elements_by_css_selector('#password')
        pwd[0].send_keys(passwords)
        driver.find_elements_by_css_selector('#lzform > div:nth-child(8) > input')[0].click()
        driver.refresh()
        cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
        cookiestr = ';'.join(item for item in cookie)
        print('获取cookie成功')
        return cookiestr
    except:
        print('获取cookie异常')


def crawer(k, id, start_page, end_page, status, comment_type, cookie):
    '''
    k:表示第k条评论，
    id：爬取的电影id，
    start_page：开始页数，
    end_page:结束页数，
    status:评论人是否看过电影，
    comment_type：评论类型
    '''
    datas = []
    pro = ['122.152.196.126', '114.215.174.227', '119.185.30.75']
    # 头信息
    headers = {
        'user-Agent': 'Mozilla/5.0(Windows NT 10.0;Win64 x64)AppleWebkit/537.36(KHTML,like Gecko) chrome/58.0.3029.110 Safari/537.36',
        'Cookie': cookie
    }
    for i in [i * 20 for i in range(start_page, end_page)]:
        data = requests.get(
            'https://movie.douban.com/subject/{0}/comments?start={1}&limit=20&sort=new_score&status={2}&&percent_type={3}'.format(
                id, i, status, comment_type), proxies={'http': random.choice(pro)}, headers=headers)
        soup = BeautifulSoup(data.text, 'lxml')
        content = soup.select('#comments > div > div.comment > p')
        print('正在爬取第{0}页'.format(int(i / 20) + 1))
        for row in content:
            print((k, row.text.strip()))
            data = (k, str(row.text.strip()))
            # datas.append(row.text.strip())
            datas.append(data)
            k = k + 1
        if data:
            print('第{0}页爬取成功'.format(int(i / 20) + 1))
        else:
            print('第{0}页爬取失败'.format(int(i / 20) + 1))
        if i != 0 and i % 100 == 0:
            print('页数为6的倍数随机休息三到五秒')
            time.sleep(random.randint(3, 5))
    if datas:
        print(datas)
        return datas
    else:
        print('第{0}条失败'.format(k))


def write(datas, save_name):
    '''
    datas:所爬取数据
    save_name:保存的excel文件名，后缀为.xls,保存路径为当前文件夹
    '''
    try:
        # 获取根目录
        BASE_DIR = os.path.split(os.path.realpath(__file__))[0]
        col = 0
        row = 0
        book = Workbook(encoding='utf-8')
        sheet1 = book.add_sheet('Sheet 1')
        sheet1.write(row, 0, "评论编号")
        sheet1.write(row, 1, "评论详情")
        row = row + 1
        for data in datas:
            sheet1.write(row, 0, data[0])
            sheet1.write(row, 1, data[1])
            row = row + 1
        book.save(BASE_DIR + '\{0}'.format(save_name))
        print('保存成功，保存路径为' + BASE_DIR + '\{0}'.format(save_name))
    except:
        print('保存失败')


if __name__ == '__main__':
    cookie = get_cookies('17738722825', 'lyq112358')
    id = 1292720
    # 豆瓣只展示给用户前500条评论，修改相应参数就可以爬去相应评论
    datas = crawer(1, id, 0, 24, 'P', 'h', cookie)
    # 文件名后缀必须是.xls结尾
    write(datas, 'a.xls')
