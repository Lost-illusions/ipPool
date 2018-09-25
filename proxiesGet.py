#! /usr/bin/python3
'''
随机选取网站爬取10个ip地址
'''
import requests
from bs4 import BeautifulSoup
from lxml import etree
import random
import pymongo
import subprocess

user_agents = [
    'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 '
    'Mobile/13B143 Safari/601.1]',
    'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/48.0.2564.23 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/48.0.2564.23 Mobile Safari/537.36']
headers = {
    'User-Agent':random.choice(user_agents),
    'Accept-Language': 'zh-CN,zh;q=0.9'
}


class IpGet(object):

    def __init__(self,num=10):
        self.user_agents = ['Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 ',
                            'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/48.0.2564.23 Mobile Safari/537.36',
                            'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/48.0.2564.23 Mobile Safari/537.36']
        self.headers = {'User-Agent':random.choice(user_agents)}
        self.proxies = []
        self.client = pymongo.MongoClient('localhost',27017)
        self.db = self.client['tool']
        self.collect = self.db['ip']
        self.num = num

    def checkIp(self):
        '''
        检查ip是否可用，丢包>0的删除
        :return:
        '''
        for data in self.collect.find():
            ping = subprocess.Popen(['ping', '-c 2', '112.247.207.107'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, error = ping.communicate()
            out = str(out.decode('gbk'))
            loss = int(out[out.find('packet loss')-3:out.find('packet loss')-2])
            if loss:
                self.collect.remove({'ip':data['ip']})
        num = self.collect.count()
        while not num == 10:
            self.get(10-num)
            self.checkIp()
            num = self.collect.count()


    def get(self,num):
        f = [self.get_1,self.get_3]
        try:
            f[random.randint(0,len(f)-1)](num)
        except:
            f[random.randint(0,len(f)-1)](num)
        for proxy in self.proxies:
            self.collect.insert(proxy)

    def get_1(self,num):
        url = 'http://www.data5u.com/free/index.html'
        r = requests.get(url,headers=self.headers)
        selector = etree.HTML(r.content)
        dataList = selector.xpath('/html/body/div[5]/ul/li[2]/ul')[1:]
        mask = random.sample(range(0,len(dataList)),num)
        for i in mask:
            self.proxies.append({'http':dataList[i][0][0].text,'ip':dataList[i][1][0].text,'port':dataList[i][3][0][0].text})

    def get_2(self,num):
        '''
        端口是图片格式需要识别
        :return:
        '''
        url = 'https://proxy.mimvp.com/freesole.php?proxy=in_hp&sort=&page=1'
        r = requests.get(url,headers=self.headers)
        selector = etree.HTML(r.content)
        dataList = selector.xpath('//*[@id="mimvp-body"]/div[2]/div/table/tbody/tr')

    def get_3(self,num):
        url = 'http://www.iphai.com/free/ng'
        r = requests.get(url,headers=self.headers)
        soup = BeautifulSoup(r.content,'lxml')
        dataList = soup.find_all('tr')[1:]
        mask = random.sample(range(0,len(dataList)),num)
        for i in mask:
            tds = dataList[i].find_all('td')
            http = tds[3].get_text('','\n')
            if http == '':
                http = 'http'
            self.proxies.append({'http':http,'ip':tds[0].get_text('','\n'),'port':tds[1].get_text('','\n')})



