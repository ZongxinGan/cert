# -*- coding: utf8 -*-

from multiprocessing import Pool
#import sys
import requests
import re
from bs4 import BeautifulSoup
import sqlite3
import threading
import time
from random import sample
#from selenium import webdriver
#reload(sys)
#sys.setdefaultencoding('utf8')
dbfile = 'sqldb.db'
min_num=2

__user_agent = [
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
    "Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
    "Mozilla/2.02E (Win95; U)",
    "Mozilla/3.01Gold (Win95; I)",
    "Mozilla/4.8 [en] (Windows NT 5.1; U)",
    "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)",
    "HTC_Dream Mozilla/5.0 (Linux; U; Android 1.5; en-ca; Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; de-DE) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; sdk Build/CUPCAKE) AppleWebkit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; htc_bahamas Build/CRB17) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1-update1; de-de; HTC Desire 1.19.161.5 Build/ERE27) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-ch; HTC Hero Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; HTC Legend Build/cupcake) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-de; HTC Magic Build/PLAT-RC33) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1 FirePHP/0.3",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; HTC_TATTOO_A3288 Build/DRC79) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.0; en-us; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; T-Mobile G1 Build/CRB43) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari 525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-gb; T-Mobile_G2_Touch Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Droid Build/FRG22D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Milestone Build/ SHOLS_U2_01.03.1) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.0.1; de-de; Milestone Build/SHOLS_U2_01.14.0) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522  (KHTML, like Gecko) Safari/419.3",
    "Mozilla/5.0 (Linux; U; Android 1.1; en-gb; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-ca; GT-P1000M Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 3.0.1; fr-fr; A500 Build/HRI66) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.6; es-es; SonyEricssonX10i Build/R1FA016) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; SonyEricssonX10i Build/R1AA056) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
]


def get_ua():
    return sample(__user_agent, 1)[0]

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'User-Agent': get_ua()
}


class Fetch_proxy:
    def __init(self):
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
        cursor.execute('create table if not exists enableips(ip char(50) primary key,date char(50))')
        conn.commit()
        conn.close()
    def spider(self):
        get_all_proxy()

    def fetch(self):
        self.check()
        return fetch_proxy()

    def fetch_many(self, num):
        self.check()
        return fetch_proxy_many(num)

    def delete(self, ip):
        delete_ip(ip)

    def check(self):
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
        rows = cursor.execute('select * from enableips')
        iplist = []
        for row in rows:
            iplist.append(row[0])

        if len(iplist) < min_num:
            print 'proxy list too short! spider it'
            self.spider()
        cursor.close()
        conn.close()


class IsEnable(threading.Thread):
    def __init__(self,ip):
        super(IsEnable,self).__init__()
        self.ip=ip
        self.headers=headers
        self.proxies={
        'http':'http://%s'%ip
        }
    def run(self):
        try:
            html=requests.get('http://httpbin.org/ip',headers=self.headers,proxies=self.proxies,timeout=5).text
            result=eval(html)['origin']
            if len(result.split(','))==2:
                return
            if result in self.ip:
                self.insert_into_sql()
        except:
            return

    def insert_into_sql(self):
        conn=sqlite3.connect(dbfile)
        cursor=conn.cursor()
        try:
            date=time.strftime('%Y-%m-%d %X', time.localtime() )
            cursor.execute("insert into enableips(ip,date) values(?,?)",(self.ip,date,))
            print(self.ip)
        except:
            conn.close()
            return
        cursor.close()
        conn.commit()
        conn.close()



def fetch_proxy():
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    rows = cursor.execute('select * from enableips')
    iplist = []
    for row in rows:
        iplist.append(row[0])
    return sample(iplist, 1)[0]


def fetch_proxy_many(num):
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    rows = cursor.execute('select * from enableips')
    iplist = []
    for row in rows:
        iplist.append(row[0])
    return sample(iplist, num)


def delete_ip(ip):
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    cursor.execute('delete from enableips where ip=?', (ip, ))
    print('delete ', ip)
    cursor.close()
    conn.commit()
    conn.close()

def delete_all_ip():
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    cursor.execute('delete from enableips')
    cursor.close()
    conn.commit()
    conn.close()
    

def get_from_ipcn():
    urls = ['http://proxy.ipcn.org/proxylist.html',
            'http://proxy.ipcn.org/proxylist2.html']
    tmp_headers=headers
    tmp_headers['Host']='proxy.ipcn.org'
    for url in urls:
        try:
            html = requests.get(url,headers=tmp_headers,timeout=10)
            html.encoding = 'gbk'            
        except:
            print 'open url error',url
            continue
        ips = re.findall('\\d+\\.\\d+\\.\\d+\\.\\d+:\\d+', html.text)
        threadings = []
        for ip in ips:
            print "ipcn",ip
            work = IsEnable(ip)
            work.setDaemon(True)
            threadings.append(work)
        for work in threadings:
            work.start()


def get_from_xicidaili():
    urls = ['http://www.xicidaili.com/nn/', 'http://www.xicidaili.com/nn/2',
            'http://www.xicidaili.com/nn/3', 'http://www.xicidaili.com/wn/']
    tmp_headers=headers
    tmp_headers['Host']='www.xicidaili.com'
    for pageurl in urls:
        try:
            html = requests.get(pageurl, headers=tmp_headers, timeout=10).text
        except:
            print 'open url error',pageurl
            continue
        table = BeautifulSoup(html, 'lxml').find('table',id='ip_list').find_all('tr')
        iplist = []
        for tr in table[1:]:
            tds = tr.find_all('td')
            ip = tds[1].get_text() + ':' + tds[2].get_text()
            iplist.append(ip)
        threadings = []
        for ip in iplist:
            print "xicidaili",ip
            work = IsEnable(ip)
            work.setDaemon(True)
            threadings.append(work)
        for work in threadings:
            work.start()


def get_from_kxdaili():
    urls = ['http://www.kxdaili.com/dailiip/1/%s.html',
            'http://www.kxdaili.com/dailiip/2/%s.html']
    tmp_headers=headers
    tmp_headers['Host']='www.kxdaili.com'
    for url in urls:
        page = 1
        while page <= 10:
            try:
                tmp_url= url % page
                html = requests.get(tmp_url,headers=tmp_headers,timeout=10).text.encode('ISO-8859-1').decode('utf-8', 'ignore')
                page += 1
            except:
                print 'open url error',tmp_url
                page += 1
                continue
            try:
                table = BeautifulSoup(html, 'lxml').find('table').find_all('tr')
            except:
                page += 1
                continue
            iplist = []
            for tr in table[1:]:
                tds = tr.find_all('td')
                ip = tds[0].get_text() + ':' + tds[1].get_text()
                iplist.append(ip)
            threadings = []
            for ip in iplist:
                print "kxdaili",ip
                work = IsEnable(ip)
                work.setDaemon(True)
                threadings.append(work)
            for work in threadings:
                work.start()


def get_from_66ip():
    urls=['http://www.66ip.cn/nmtq.php?getnum=200&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=0&proxytype=2&api=66ip',
          'http://www.66ip.cn/nmtq.php?getnum=200&isp=0&anonymoustype=4&start=&ports=&export=&ipaddress=&area=0&proxytype=2&api=66ip']
    tmp_headers=headers
    tmp_headers['Host']='www.66ip.cn'
    tmp_headers['Accept-Encoding']='Accept-Encoding:gzip, deflate, sdch'
    #browser = webdriver.PhantomJS()
    for pageurl in urls:
        try:
            #browser.get(url)
            #html =browser.page_source
            html=requests.get(pageurl,headers=tmp_headers,timeout=10).text
        except:
            print 'open url error',pageurl
            continue
        iplist=re.findall('\d+\.\d+\.\d+\.\d+:\d+',html)
        threadings=[]
        for ip in iplist:
            print "66ip",ip
            work=IsEnable(ip)
            work.setDaemon(True)
            threadings.append(work)
        for work in threadings:
            work.start()


def get_from_proxylists():
    urls = ['http://www.proxylists.net/http_highanon.txt']
    tmp_headers=headers
    tmp_headers['Host']='www.proxylists.net'
    for pageurl in urls:
        try:
            html = requests.get(pageurl, headers=tmp_headers, timeout=10).text
        except:
            continue
        iplist = re.findall('\\d+\\.\\d+\\.\\d+\\.\\d+:\\d+', html)
        threadings = []
        for ip in iplist:
            print "proxylists",ip
            work = IsEnable(ip)
            work.setDaemon(True)
            threadings.append(work)
        for work in threadings:
            work.start()


def get_from_ip181():
    urls = ['http://www.ip181.com/','http://www.ip181.com/daili/2.html','http://www.ip181.com/daili/3.html']
    tmp_headers=headers
    tmp_headers['Host']='www.ip181.com'
    for pageurl in urls:
        try:
            html = requests.get(pageurl, headers=tmp_headers, timeout=10).text
        except:
            print 'open url error',pageurl
            continue
        table = BeautifulSoup(html, 'lxml').find('table',cellpadding='0').find_all('tr')
        iplist = []
        for tr in table[1:]:
            tds = tr.find_all('td')
            ip = tds[0].get_text() + ':' + tds[1].get_text()
            iplist.append(ip)
        threadings = []
        for ip in iplist:
            print "ip181",ip
            work = IsEnable(ip)
            work.setDaemon(True)
            threadings.append(work)
        for work in threadings:
            work.start()


def get_from_kuaidaili():
    urls = ['http://www.kuaidaili.com/free/inha/', 'http://www.kuaidaili.com/free/inha/2/',
            'http://www.kuaidaili.com/free/outha/', 'http://www.kuaidaili.com/free/outha/2/']
    tmp_headers=headers
    tmp_headers['Host']='www.kuaidaili.com'
    for pageurl in urls:
        try:
            html = requests.get(pageurl, headers=headers, timeout=10).text
        except:
            print 'open url error',pageurl
            continue
        table = BeautifulSoup(html, 'lxml').find('tbody').find_all('tr')
        iplist = []
        for tr in table[1:]:
            tds = tr.find_all('td')
            ip = tds[0].get_text() + ':' + tds[1].get_text()
            iplist.append(ip)
        threadings = []
        for ip in iplist:
            print "kuaidaili",ip
            work = IsEnable(ip)
            work.setDaemon(True)
            threadings.append(work)
        for work in threadings:
            work.start()


def get_from_yundaili():
    urls = ['http://www.ip3366.net/?stype=1&page=1', 'http://www.ip3366.net/?stype=1&page=2',
            'http://www.ip3366.net/?stype=1&page=3','http://www.ip3366.net/?stype=1&page=4']
    tmp_headers=headers
    tmp_headers['Host']='www.ip3366.net'
    for pageurl in urls:
        try:
            html = requests.get(pageurl, headers=headers, timeout=10).text
        except:
            print 'open url error',pageurl
            continue
        table = BeautifulSoup(html, 'lxml').find('tbody').find_all('tr')
        iplist = []
        for tr in table[0:]:
            tds = tr.find_all('td')
            ip = tds[0].get_text() + ':' + tds[1].get_text()
            iplist.append(ip)
        threadings = []
        for ip in iplist:
            print "yundaili",ip
            work = IsEnable(ip)
            work.setDaemon(True)
            threadings.append(work)
        for work in threadings:
            work.start()
                 

def get_all_proxy():
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    cursor.execute('create table if not exists enableips(ip char(50) primary key,date char(50))')
    conn.commit()
    conn.close()
    try:
        get_from_ipcn()
        print 'get_from_ipcn success'
    except:
        print 'get_from_ipcn failed'
    try:
        get_from_xicidaili()
        print 'get_from_xicidaili success'
    except:
        print 'get_from_xicidaili failed'
    try:
        get_from_kxdaili()
        print 'get_from_kxdaili success'
    except:
        print 'get_from_kxdaili failed'
    try:
        get_from_66ip()
        print 'get_from_66ip success'
    except:
        print 'get_from_66ip failed'
    try:
        get_from_proxylists()
        print 'get_from_proxylists success'
    except:
        print 'get_from_proxylists failed'
    try:
        get_from_ip181()
        print 'get_from_ip181 success'
    except:
        print 'get_from_ip181 failed'
    try:
        get_from_kuaidaili()
        print 'get_from_kuaidaili success'
    except:
        print 'get_from_kuaidaili failed'
    try:
        get_from_yundaili()
        print 'get_from_yundaili success'
    except:
        print 'get_from_yundaili failed'
    

def check_module(module_name):
    if module_name == 'get_from_ipcn':
        get_from_ipcn()
    elif module_name == 'get_from_xicidaili':
        get_from_xicidaili()
    elif module_name == 'get_from_kxdaili':
        get_from_kxdaili()
    elif module_name == 'get_from_66ip':
        get_from_66ip()
    elif module_name == 'get_from_proxylists':
        get_from_proxylists()
    elif module_name == 'get_from_ip181':
        get_from_ip181()
    elif module_name == 'get_from_kuaidaili':
        get_from_kuaidaili()
    elif module_name == 'get_from_yundaili':
        get_from_yundaili()


def process_pool():
    module_list=['get_from_ipcn','get_from_kxdaili','get_from_xicidaili','get_from_66ip','get_from_proxylists','get_from_ip181','get_from_kuaidaili','get_from_yundaili']
    pool = Pool(processes=4)
    for i in module_list:
        pool.apply_async(check_module, (i,))
    pool.close()
    pool.join()


if __name__ == '__main__':
    #freeze_support()
    delete_all_ip()
    process_pool()
    
    #get_all_proxy()

    