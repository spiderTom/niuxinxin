#coding:utf-8
import requests
import re
import os
import string
from lxml import etree
from bs4 import BeautifulSoup
import ConfigParser

isProxyNeeded = False
target_index = 1
test_url = 'http://10.133.141.219:8080/informationbrowser/nav/0'
conf=ConfigParser.ConfigParser()
conf.readfp(open("config.ini", "rb"))
fromChapter = conf.get("user", "FROM")
toChapter = conf.get("user", "TO")


class NetWorkSetting:
    def __init__(self):
        self.proxy = {
            "http": 'http://10.144.1.10:8080',
            "https": 'https://10.144.1.10:8080'}
        self.base_url = 'http://skydocs.int.net.nokia.com/Open%20BGW*Open%20BGW%20Cloud'
        self.naviUrl = 'http://10.133.141.219:8080/informationbrowser/nav/'
        self.contentUrl = 'http://10.133.141.219:8080/informationbrowser/'
        self.myHeaders = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'Referer': 'http://10.133.141.219:8080/informationbrowser/advanced/tocView.jsp?view=toc'
}

#1. get source for base url
print "1, get source for base url"
setting = NetWorkSetting()
wmp = []
session = requests.Session()

if isProxyNeeded:
    result = session.get(test_url, headers=setting.myHeaders, proxies=setting.proxy)
else:
    result = session.get(test_url, headers=setting.myHeaders)

if result.status_code == 200:
    soup = BeautifulSoup(result.content)
    for link in soup.find_all('a'):
        if link.get('href').find(".pdf") == -1 and link.get('href').find("..") == -1:
            wmp.append(link.get('href'))

#2. get second level url
print "1, get second level url"
wmp1 = []
for item in wmp:
    targeturl = setting.naviUrl + item
    if isProxyNeeded:
        result = session.get(targeturl, headers=setting.myHeaders, proxies=setting.proxy)
    else:
        result = session.get(targeturl, headers=setting.myHeaders)
    if result.status_code == 200:
        soup = BeautifulSoup(result.content)
        for link in soup.find_all('a'):
            if link.get('href').find(".pdf") == -1 and link.get('href').find("..") == -1:
                print link.get('href')
                wmp1.append(link.get('href'))



print "======================"


