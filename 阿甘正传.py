from bs4 import BeautifulSoup
import requests
import os
import time
import random
from xlwt import Workbook
BASE_DIR = os.path.split(os.path.realpath(__file__))[0]
#k:表示第k条评论，id：爬取的电影id，start_page：开始页数，end_page:结束页数，status:评论人是否看过电影，comment_type：评论类型
def crawer(k,id,start_page,end_page,status,comment_type):
    datas=[]
    pro = ['122.152.196.126', '114.215.174.227', '119.185.30.75']
    # 头信息
    headers = {
        'user-Agent': 'Mozilla/5.0(Windows NT 10.0;Win64 x64)AppleWebkit/537.36(KHTML,like Gecko) chrome/58.0.3029.110 Safari/537.36',
        'Cookie': 'll="118318"; bid=p6so5zArZTg; __yadk_uid=ydkCytRKMlbsAh1ivb7N0bYUKW3MhBlk; _vwo_uuid_v2=D4A733A3523FDFC7568D69A51DDE4867D|4fee7585ab66f4445dee5f950f5bf569; __utmv=30149280.18021; _ga=GA1.2.77508533.1529731292; ps=y; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1532478651%2C%22http%3A%2F%2Fwww.so.com%2Flink%3Fm%3Dadc14eL68YE4VCMbm7pl4p5DqiGKAy2lWVVQYRb1LN4PajJXgeBMZfro0D9%252BdH93SEMZ7klzS3bL01dEeZM%252BaUKvXy3M6gZE82SCeF2ZNAzhELF5nwjsEh4w2cUI%253D%22%5D; _pk_ses.100001.4cf6=*; __utmc=30149280; __utma=223695111.1463836260.1529731331.1532440205.1532478651.5; __utmb=223695111.0.10.1532478651; __utmc=223695111; __utmz=223695111.1532478651.5.5.utmcsr=so.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; __utmt=1; douban-fav-remind=1; __utma=30149280.77508533.1529731292.1532478651.1532478974.6; __utmz=30149280.1532478974.6.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; dbcl2="180214033:UOe3dvx5nuA"; _gid=GA1.2.1962163821.1532479022; _gat_UA-7019765-1=1; ck=3BPg; push_noty_num=0; push_doumail_num=0; ap=1; __utmb=30149280.17.6.1532479001377; _pk_id.100001.4cf6=83729ec7767ac609.1529731303.5.1532479077.1532441182.',
    }
    for i in [i*20  for i in range(start_page,end_page)]:
      data=requests.get('https://movie.douban.com/subject/{0}/comments?start={1}&limit=20&sort=new_score&status={2}&&percent_type={3}'.format(id,i,status,comment_type), proxies={'http': random.choice(pro)},headers=headers)
      soup=BeautifulSoup(data.text,'lxml')
      content=soup.select('#comments > div > div.comment > p')
      print('正在爬取第{0}页'.format(int(i/20)+1))
      for row in content:
          print((k,row.text.strip()))
          data=(k,str(row.text.strip()))
          # datas.append(row.text.strip())
          datas.append(data)
          k=k+1
      if data:
       print('第{0}页爬取成功'.format(int(i / 20) + 1))
      else:
          print('第{0}页爬取失败'.format(int(i / 20) + 1))
      if i!=0 and i%100==0:
          print('随机休息三到五秒')
          time.sleep(random.randint(3,5))
    if datas:
     print(datas)
     return datas
    else:
        print('第{0}条失败'.format(k))
def write(datas,save_name):
    #datas:所爬取数据
    #save_name:保存的excel文件名，后缀为.xls,保存路径为当前文件夹
    try:
        col=0
        row=0
        book = Workbook(encoding='utf-8')
        sheet1 = book.add_sheet('Sheet 1')
        sheet1.write(row, 0, "评论编号")
        sheet1.write(row, 1, "评论详情")
        row=row+1
        for data in datas:
            sheet1.write(row, 0, data[0])
            sheet1.write(row, 1, data[1])
            row=row+1
        book.save(BASE_DIR+'\{0}'.format(save_name))
        print('保存成功，保存路径为'+BASE_DIR+'\{0}'.format(save_name))
    except:
        print('保存失败')
if __name__=='__main__':
    datas=[]
    id = 1292720
    #豆瓣只展示给用户前500条评论
    data1 = crawer(1, id, 0, 24, 'P', 'h')
    # write(data1,'阿甘正传.xls')




