import requests
import itchat
from lxml import etree
import threading


def get_soup():  #获得’心灵鸡汤‘
    url = 'http://www.59xihuan.cn/index_1.html'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'}
    res = requests.get(url, headers=header).content.decode('utf-8')
    selector = etree.HTML(res)
    soup_text = selector.xpath('//div[@class = "mLeft"]/div[1]/div[2]/div[2]/text()')[0]
    soup_text = soup_text.replace('\r\n','').strip()
    return soup_text

soup = get_soup()

def send_msg():  #定时向你的微信群里发'鸡汤'
    #itchat.auto_login(enableCmdQR=2) #登陆的时候使用命令行显示二维码,数字调大小
    itchat.auto_login()
    chatrooms = itchat.search_chatrooms('你的群名')[0]['UserName']
    itchat.send(soup,toUserName=chatrooms)
    timer = threading.Timer(3600, send_msg)
    timer.start()

send_msg()