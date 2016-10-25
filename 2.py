#coding:utf-8
import requests
import re
import os
import string
from lxml import etree
from bs4 import BeautifulSoup
import ConfigParser

isProxyNeeded = False
conf=ConfigParser.ConfigParser()
conf.readfp(open("config.ini", "rb"))
fromChapter = conf.get("user", "FROM")
toChapter = conf.get("user", "TO")

print fromChapter
print toChapter

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



setting = NetWorkSetting()
needCheck = []
afterCheck = []
targetUrl = []
session = requests.Session()

def checkUrlWithCp(cp):
    tempUrl = setting.naviUrl + str(cp)
    if isProxyNeeded:
        result = session.get(tempUrl, headers=setting.myHeaders, proxies=setting.proxy)
    else:
        result = session.get(tempUrl, headers=setting.myHeaders)

    if result.status_code == 200:
        soup = BeautifulSoup(result.content)
        for link in soup.find_all('a'):
            if link.get('href').find(".pdf") == -1 and link.get('href').find("..") == -1:
                afterCheck.append(link.get('href'))
            elif link.get('href').find(".pdf") == -1 and link.get('href').find("topic") != -1:
                targetUrl.append(link.get('href'))

#1. put first level url to list which need to be checked.
print "1, put first level url to list which need to be checked."
target_index = 1
while target_index >= int(fromChapter) and target_index <= int(toChapter) and target_index not in needCheck:
    needCheck.append(target_index)
    target_index += 1

print needCheck

while len(needCheck) != 0:
    for item in needCheck:
        checkUrlWithCp(item)
    needCheck = afterCheck
    print afterCheck
    afterCheck = []
    print "======================"
    #print targetUrl
    f = open("target.txt", 'w+')
    for topic in targetUrl:
        f.write(topic)
        f.write('\n')
    f.close()


print "!!!======================!!!"








