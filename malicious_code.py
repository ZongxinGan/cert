# -*- coding:utf-8 -*-

#import chardet
import re
import uuid
from random import sample
from time import sleep
import requests
from bs4 import BeautifulSoup
import os
import time
#import sqlite3
import MySQLdb
import Fetch_proxy
import Parse_config
from requests.adapters import HTTPAdapter

sleep_num = 5
requests.adapters.DEFAULT_RETRIES = 5

config_f='config.ini'
realdir=os.path.split(os.path.realpath(__file__))[0]
cf = Parse_config.config_parse(os.path.join(realdir,config_f))
dbhost=cf.get_dbhost()
dbuser=cf.get_dbuser()
dbpwd=cf.get_dbpwd()
dbname=cf.get_dbname()

pagenum=cf.get_page_num()


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


def init_headers():
    headers = { "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                     "Accept-Encoding":"gzip, deflate, sdch",
                     "Accept-Language":"zh-CN,zh;q=0.8",
                     "Referer":"http://www.cert.org.cn",
                     "User-Agent":get_ua(),
                     "Cache-Control":"max-age=0",
                     "Host":"www.cert.org.cn",
                     "Connection":"keep-alive",
                     "Upgrade-Insecure-Requests":"1",
                     "X-Forwarded-For":""
                     }
    return headers

class Professor():
    def __init__(self,num,url):
        self.db = MySQLdb.connect(dbhost,dbuser,dbpwd,dbname,charset='utf8')
        self.cursor = self.db.cursor()
        if url == '':
            self.url = 'http://www.cert.org.cn/publish/main/10/index_'+str(num)+'.html'
        else:
            self.url = url
        self.ua = get_ua()
        self.headers = { "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                     "Accept-Encoding":"gzip, deflate, sdch",
                     "Accept-Language":"zh-CN,zh;q=0.8",
                     "Referer":"http://www.cert.org.cn/publish/main/10/index.html",
                     "User-Agent":self.ua,
                     "Host":"www.cert.org.cn",
                     "Connection":"keep-alive",
                     "Upgrade-Insecure-Requests":"1",
                     }
        
    def open_url_with_soup(self,url,retries=3):        
        sleep(sleep_num)
        self.headers = { "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                     "Accept-Encoding":"gzip, deflate, sdch",
                     "Accept-Language":"zh-CN,zh;q=0.8",
                     "Referer":"http://www.cert.org.cn/publish/main/10/index.html",
                     "User-Agent": get_ua(),
                     "Host":"www.cert.org.cn",
                     "Connection":"keep-alive",
                     "Upgrade-Insecure-Requests":"1",
                     "Cache-Control":"max-age=0",
                        
                     }
        
        proxy_get=Fetch_proxy.Fetch_proxy()
        while True:
            proxy_ip=proxy_get.fetch()
            self.seq = requests.Session()
            self.proxies={
            'http':'http://%s'%proxy_ip
            }
            self.seq.mount('http://', HTTPAdapter(max_retries=5))
            try:
                self.headers=init_headers()
                res=requests.get(url,headers=self.headers,proxies=self.proxies,timeout=5)
                res.encoding = 'utf-8'
                if res.status_code == 200:
                    break
            except requests.exceptions.HTTPError as e:
                print 'proxy is expiered ',proxy_ip
                proxy_get.delete(proxy_ip)
                print e 
                exit
            except requests.exceptions.ConnectionError as e:
                print 'proxy is expiered ',proxy_ip
                proxy_get.delete(proxy_ip)
                print e 
                exit 
            except:
                print 'proxy is expiered ',proxy_ip
                proxy_get.delete(proxy_ip)
                exit 
                
        if res.status_code == 200:
            html = BeautifulSoup(res.text,'html5lib')
            print "open url "+str(url)+ "  success "
            if html.find_all(name="div", attrs={"class":"con_list"}) or html.findAll(name="div",attrs={"class":"con_list1"}) :
                return html
            else:
                sleep(5)
                return self.open_url_with_soup(url)
        else:
            print "open url "+str(url)+ "  fail "
            sleep(5)
            
    def get_url_list(self):
        html = self.open_url_with_soup(self.url)
        table = html.findAll(name="div",attrs={"class":"con_list"})
        self.get_vul_info(table)
        
    def get_vul_info(self,table):
        vul = table[0].findAll('li')
        for i in vul:
            vulinfo = i.findAll('a')
            title = vulinfo[0].text.encode('utf-8').strip()
            dateinfo = i.findAll('span')
            try:
                date = re.search(r'\[(\S+)\]', dateinfo[0].encode('utf-8'), re.S).group(1)

            except:
                pass

            try:
                href = re.search(r'window\.open\(\"(\S+)\"\)', vulinfo[0].encode('utf-8'), re.S).group(1)

            except:
                pass
            self.get_content(title,date,"http://www.cert.org.cn" + href)

                
    def get_content(self,title,date,url):
        
        tag = self.check_title(title)
        if tag == 1:
            print title," already exists!"
            return 1
        print title," not exists!"
        
        insert_array=[]
        html = self.open_url_with_soup(url)
        try:
            content = html.findAll(name="div",attrs={"class":"artil_content"})
            contents = content[0].text.encode('utf-8').strip()
            content_html = content[0].encode('utf-8').strip()
            
            try:
                imgs = content[0].findAll('img')
                for img in imgs:
                    img_url = "http://www.cert.org.cn" + img['src']
                    img_name = img['src'].split('/')[-1]
                    uuuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(img_name)))                  
                    try:
                        re_path = "${cloudUrl}/system/viewImage.do?imageID=" + uuuid
                        ori_path = img['src'].split('.')[0]
                        try:
                            ori_path = ori_path.replace('(','\(')
                            ori_path = ori_path.replace(')','\)')
                        except Exception,e:
                            pass
                        pattern = re.compile(str(ori_path))
                        contents = pattern.sub(str(re_path), contents)
                        content_html = pattern.sub(str(re_path), content_html)

                    except Exception,e:
                        print e
                        pass
                    try:
                        directory = "/opt/scloud/public/image"
                        filename = "/opt/scloud/public/image/" + uuuid + "." + img_name.split('.')[-1]
                        tmp_directory = "/image"
                        tmp_filename = "/image/" + uuuid + "." + img_name.split('.')[-1]
                        res = requests.get(img_url,headers=self.headers,timeout=5)
                        img_content = res.content
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                        with open(filename,'wb') as f:
                            f.write(img_content)
                    except Exception,e:
                        print e
                        pass
                    
            except Exception,e:
                print e
                pass
            
        except Exception,e:
            print e
            contents = ''
            pass
        
        insert_array.append(title)       
        insert_array.append(contents.replace('\'','\\\''))
        insert_array.append(content_html.replace('\'','\\\''))
        insert_array.append(date)
        insert_array.append(time.strftime('%Y-%m-%d %X', time.localtime() ))
        insert_array.append(2)

        self.insert_into_table(insert_array)
        
    
    def check_title(self,title):
        sql="select * from t_threat_cncert where title='%s'" % (title)
        total = self.cursor.execute(sql)
        tag = 0;
        if total == 0:
            return tag
        else:
            tag = 1
        return tag        
    
    def insert_into_table(self,insert_list):
        sql="insert into t_threat_cncert(title,contents,contentsHTML,publishTime,createTime,dataType) values('{0}','{1}','{2}','{3}','{4}','{5}')"  .format(insert_list[0],insert_list[1],insert_list[2],insert_list[3],insert_list[4],insert_list[5])
        try:
            self.cursor.execute(sql)
            self.db.commit()
            self.write_record(insert_list[0]+" insert success")
            print insert_list[0],"insert success"
        except Exception,e:
            self.write_record(insert_list[0]+" insert error")
            print insert_list[0],"insert error"
            print e
            self.db.rollback()

    
    def write_record(self,tmp):
        fp = open('spider.log','a')
        ISOTIMEFORMAT='%Y-%m-%d %X'
        tt = time.strftime( ISOTIMEFORMAT, time.localtime() )
        fp.write(tt+' '+ tmp+'\n')
        fp.close()



if __name__=="__main__":
    
    for i in range(1,pagenum+1):
        print 'start spider page ' + str(i)
        if i == 1:
            p = Professor(i,'http://www.cert.org.cn/publish/main/10/index.html')
            p.get_url_list()
        else:
            p = Professor(i,'')
            p.get_url_list()

