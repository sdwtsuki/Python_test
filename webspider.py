import urllib.request
import requests
import urllib.parse
from bs4 import BeautifulSoup
import random
import socket
import json
import re
import scrapy
import time
from lxml import etree
import csv
import xlwt
import pymongo
import pymysql
from multiprocessing import Pool

head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'}

# response = urllib.request.urlopen('https://www.baidu.com/')
# http = response.read()
# http = http.decode('utf-8')
# print(http)



# #下载猫图
# url = 'http://placekitten.com/400/400'
# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
# req = urllib.request.Request(url = url ,headers = headers)
# response = urllib.request.urlopen(req)
# img = response.read()
# print(img)
# with open('D:\Downloads\cat_img.jpg','wb') as f:
#     f.write(img)



#有道词典自动翻译
# content = input('请输入需要翻译的内容：')
# url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
# data = {'i':content,'from':'AUTO','to':'AUTO','smartresult':'dict','client':'fanyideskweb','salt':'1525401155986','sign':'4ed16a6301c3999a80b30508505a4784','doctype':'json','version':'2.1','keyfrom':'fanyi.web','action':'FY_BY_CLICKBUTTION','typoResult':'false'}
# data = urllib.parse.urlencode(data).encode('utf-8')

# rqs = urllib.request.Request(url,data,head)
# response = urllib.request.urlopen(rqs)
# html = response.read().decode('utf-8')
# target = json.loads(html)
# print('翻译结果：'+ target['translateResult'][0][0]['tgt'])



# #随机检测代理ip地址（待完善）
# socket.setdefaulttimeout(5)
# ip_test = 'http://ip.chinaz.com/getip.aspx'
# ip_provide = 'http://www.xicidaili.com/nn/2'
# ip_provide_rqt = urllib.request.Request(url = ip_provide,headers = head)
# ip_provide_html = urllib.request.urlopen(ip_provide_rqt).read().decode('utf-8')
# soup = BeautifulSoup(ip_provide_html,'lxml')
# trlist = soup.find_all('tr')
# hostlist = []
# for i in range(len(trlist)):
#     if i>=1:
#         ip = trlist[i].find_all('td')[1].text
#         port = trlist[i].find_all('td')[2].text
#         protocol = trlist[i].find_all('td')[5].text.lower()
#         host = ip + ':' + port
#         if protocol != 'https':
#             hostlist.append(host)
#
# ip_choice = random.choice(hostlist)
# print(len(hostlist))
# proxy_support = urllib.request.ProxyHandler({'http':ip_choice})
# opener = urllib.request.build_opener(proxy_support)
# urllib.request.install_opener(opener)
# rqt = urllib.request.Request(url = ip_test,headers = head)
# http = urllib.request.urlopen(rqt).read().decode('utf-8')
# print(http)



# #爬取酷狗TOP500数据
# def getInfo(url):
#     web_data = requests.get(url,headers = head)
#     soup = BeautifulSoup(web_data.text,'lxml')
#     ranks = soup.select('span.pc_temp_num')
#     titles = soup.select('div.pc_temp_songlist > ul > li > a')
#     times = soup.select('span.pc_temp_tips_r > span')
#     for rank,title,time in zip(ranks,titles,times):
#         #print(title.get_text().split('-')[1])
#         data = {
#             'rank':rank.get_text().strip(),
#             'singer': title.get_text().split('-')[0],
#             'song': title.get_text().split('-')[1],
#             'time': time.get_text().strip()
#         }
#         print(data)
# if __name__ == '__main__':
#     #urls = ['http://www.kugou.com/yy/rank/home/{}-8888.html'].format(str(i)) for i in range(1,24)
#     urls = []
#     for i in range(1,20):
#         urls.append('http://www.kugou.com/yy/rank/home/%s-8888.html' % str(i))
#     for url in urls:
#         print(url)
#         getInfo(url)
#     time.sleep(2)



# #爬取斗破苍穹
# file = open('D:\Downloads\斗破苍穹.txt','a')
# def getInfo():
#     res = requests.get(url, headers=head)
#     if res.status_code == requests.codes.ok:
#         contents = re.findall('<p>(.*?)</p>', res.content.decode('utf-8'), re.S)
#         for text in contents:
#             file.write(text + '\n')
# if __name__ == '__main__':
#     for i in range(1,10):
#         url = 'http://www.doupoxs.com/doupocangqiong/%d.html' % i
#         getInfo()
#         print('正在写入第%d页' % i)
#         time.sleep(2)
#     file.close()
#     print('爬取完成')



# #爬取糗事百科
# file = open('D:\Downloads\糗事百科.txt', 'a+')
# info_lists = []
# def judge_sex(class_name):
#     if class_name == 'manIcon':
#         return "男"
#     elif class_name == 'womenIcon':
#         return '女'
#
# def get_info(url):
#     res = requests.get(url,headers = head)
#     ids = re.findall('<h2>(.*?)</h2>',res.content.decode('utf-8'),re.S)
#     levels = re.findall('<div class="articleGender \D+Icon">(.*?)</div>', res.content.decode('utf-8'),re.S)
#     sexs = re.findall('<div class="articleGender (.*?)">', res.content.decode('utf-8'),re.S)
#     contents = re.findall('<div class="content">.*?<span></span>.*?</div>',res.content.decode('utf-8'),re.S)
#     laughs = re.findall('<span class="stats-vote"><i class="number">(.*?)</i>.*?</span>',res.content.decode('utf-8'),re.S)
#     comments = re.findall('<i class="number">(.*?)</i>', res.content.decode('utf-8'),re.S)
#     for id,level,sex,content,laugh,comment in zip(ids,levels,sexs,contents,laughs,comments):
#         info = {
#             'id': id,
#             'level': level,
#             'sex': judge_sex(sex),
#             'content': content,
#             'laugh': laugh,
#             'comment': comment
#         }
#         info_lists.append(info)
#     for info_list in info_lists:
#         file.write(info_list['id'] + '\n')
#         file.write(info_list['level'] + '\n')
#         file.write(info_list['sex'] + '\n')
#         file.write(info_list['content'] + '\n')
#         file.write(info_list['laugh'] + '\n')
#         file.write(info_list['comment'] + '\n')
#
# if __name__ == '__main__':
#     for i in range(1,10):
#         url = 'https://www.qiushibaike.com/text/page/%d' % i
#         get_info(url)
#         print('正在写入第%d页' % i)
#         time.sleep(2)
#     file.close()
#     print('爬取完成')



# #爬取豆瓣图书
# fp = open('D:\Downloads\豆瓣.csv','w')
# def get_info(url):
#     res = requests.get(url,headers = head).content.decode("utf-8")
#     selector = etree.HTML(res)
#     infos = selector.xpath('//tr[@class = "item"]')
#     for info in infos:
#         book_url = info.xpath('td[1]/a/@href')[0]
#         name = info.xpath('td[2]/div/a/@title')[0]
#         book_info = info.xpath('td/p/span/text()')[0]
#         author = info.xpath('td/p/text()')[0].split('/')[0]
#         print(author)
#         writer = csv.writer(fp)
#         writer.writerow((book_url,name,book_info,author))
#
# if __name__ == "__main__":
#     for i in range(0,250,25):
#         url = 'https://book.douban.com/top250?start=%d' % i
#         get_info(url)
#         time.sleep(2)
#     fp.close()


# #爬取起点中文网【自编 :（没什么效率】
# book = xlwt.Workbook(encoding='utf-8')
# sheet = book.add_sheet('sheet1')
# content = []
# def get_info(url):
#     res = requests.get(url,headers = head).content.decode("utf-8")
#     selector = etree.HTML(res)
#     infos = selector.xpath('//div[@class = "book-mid-info"]')
#
#     for info in infos:
#         book_name = info.xpath('h4/a/text()')[0]
#         book_author = info.xpath('p/a[@class = "name"]/text()')[0]
#         book_type = info.xpath('p/a[2]/text()')[0]+'·'+info.xpath('p/a[3]/text()')[0]
#         book_status = info.xpath('p[1]/span/text()')[0]
#         book_synopsis = info.xpath('p[2]/text()')[0]
#         book_wordcount = info.xpath('p[3]/span/text()')[0]
#         content.append([book_name,book_author,book_type,book_status,book_synopsis,book_wordcount])
#
#
# if __name__ == "__main__":
#     for i in range(0,10):
#         url = 'https://www.qidian.com/all?page=%d' % i
#         get_info(url)
#         time.sleep(1)
#     print(len(content))
#     for i in range(0,len(content)):
#         sheet.write(i,0,content[i][0])
#         sheet.write(i,1,content[i][1])
#         sheet.write(i,2, content[i][2])
#         sheet.write(i,3, content[i][3])
#         sheet.write(i,4, content[i][4])
#         sheet.write(i,5, content[i][5])
#         print('正在写入第 %d 条数据' % i)
#     book.save('D:\Downloads\起点.xls')



#爬取妹子网图片并下载
from urllib.request import urlretrieve
#head = {'Referer':'http://www.mzitu.com/','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'}
# res = requests.get('http://www.mzitu.com/132537/56',headers = head).content.decode('utf-8')
# path = 'D:\Downloads\meizi/'
# http = etree.HTML(res)
# imgs = http.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
# print(imgs)
# photo = requests.get(imgs,headers = head).content
# print(photo)
# fp = open('D:\Downloads\meizi/1','wb')
# fp.write(photo)
# fp.close()
# print('下载图片')



# #多进程爬取简书网并存入mongoDB数据库
# urls = []
# for i in range(1,20):
#     urls.append('https://www.jianshu.com/c/bDHhpK?order_by=added_at&page=%d' % i)
#
# print(urls)
# url = ''
# client = pymongo.MongoClient('localhost',27017)
# mydb = client['mydb']
# jianshu = mydb['jianshu']
#
# def spider(url):
#     res = requests.get(url,headers = head).content.decode('utf-8')
#     selector = etree.HTML(res)
#     infos = selector.xpath('//ul[@class="note-list"]/li')
#     for info in infos:
#         try:
#             author = info.xpath('div/div[1]/div/a/text()')[0]
#             time = info.xpath('div/div[1]/div/span/@data-shared-at')[0]
#             title = info.xpath('div/a/text()')[0]
#             content = info.xpath('div/p/text()')[0]
#             view = info.xpath('div/div[2]/a[1]/text()')[1].strip()
#             comment = info.xpath('div/div[2]/a[2]/text()')[1].strip()
#             like = info.xpath('div/div[2]/span[1]/text()')[0].strip()
#             data ={
#                 'author': author,
#                 'time': time,
#                 'title': title,
#                 'content': content,
#                 'view': view,
#                 'comment': comment,
#                 'like': like
#             }
#             jianshu.insert_one(data)
#             print('写入数据库')
#         except IndexError:
#             pass
#
# if __name__ == "__main__":
#     print(type(urls))
#     # for url in urls:
#     #     url = url
#     #     spider(url)
#     pool = Pool(processes=4)
#     pool.map(spider,urls)



# #cookie模拟登录
# url = 'https://www.douban.com/'
# header = {
#     'Cookie':''
# }
# data = {
#     'source':'index_nav',
#     'form_email':'948363505@qq.com',
#     'form_password':'zlc950324'
# }
# html = requests.get(url,headers = header)
# print(html.text)



#爬取拉勾网招聘信息并存入MongoDB
# header = {
#     'Accept':'application/json, text/javascript, */*; q=0.01',
#     'Accept-Encoding':'gzip, deflate, br',
#     'Accept-Language':'zh-CN,zh;q=0.9',
#     'Connection':'keep-alive',
#     'Content-Length':'25',
#     'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
#     'Cookie':'',
#     'Host':'www.lagou.com',
#     'Origin':'https://www.lagou.com',
#     'Referer':'https://www.lagou.com/jobs/list_python?city=%E4%B8%8A%E6%B5%B7&cl=false&fromSearch=true&labelWords=&suginput=',
#     'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
#     'X-Anit-Forge-Code':'0',
#     'X-Anit-Forge-Token':'None',
#     'X-Requested-With':'XMLHttpRequest'
# }
# lagouwang = pymongo.MongoClient(host='localhost',port=27017)['mydb']['lagouwang']
#
# def get_page(url,params):
#     html = requests.post(url,data=params,headers =header)
#     json_data = json.loads(html.content.decode('utf-8'))
#     print(json_data)
#     total_count = json_data['content']['positionResult']['totalCount']
#     page_number = int(total_count/15) if int(total_count/15)<30 else 30
#     for page in range(2,page_number+1):
#         get_info(url, page)
#
#
# def get_info(url,page):
#     params = {
#         'first': 'true',
#         'pn': str(page),
#         'kd': 'python'
#     }
#     try:
#         html = requests.post(url,data=params,headers = header)
#         json_data = json.loads(html.text)
#         results = json_data['content']['positionResult']['result']
#         for result in results:
#             info ={
#                 "companyFullName": result["companyFullName"],
#                 'salary': result['salary'],
#                 "firstType": result["firstType"],
#             }
#             lagouwang.insert_one(info)
#             time.sleep(0.2)
#         print('写入第'+str(page)+'页数据')
#
#     except requests.exceptions.ConnectionError:
#         pass
#
#
# if __name__ == '__main__':
#     url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false'
#     params = {
#         'first': 'true',
#         'pn':'1',
#         'kd':'python'
#     }
#     get_page(url,params)


