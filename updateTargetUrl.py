#coding:utf-8
import requests
import re
import os
import string
from lxml import etree
from bs4 import BeautifulSoup


isProxyNeeded = False


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
pictureNeedCheck = []
urlHasIssuePicture = []
pictureName = []
session = requests.Session()


contentUrl = ''

fread = open("targetUrl.txt", 'r')
lines = fread.readlines()
fwrite = open("issuePictureUrl.txt", 'w+')
fsourcewrite = open("pictureUrl.txt", 'w+')
for line in lines:
    #print line
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~!!!!"
    if isProxyNeeded:
        result = session.get(line, headers=setting.myHeaders, proxies=setting.proxy, timeout=5)
    else:
        result = session.get(line, headers=setting.myHeaders, timeout=15)
    if result.status_code == 200:
        soup = BeautifulSoup(result.content)
        for link in soup.find_all('img'):
            if str(link).find("width") != -1:
                print "=========================="
                print link.get('width')
                print link
                picture = line
                current = picture.rfind("/")
                picture = picture[:current]
                picture += '/' + link.get('src')
                fsourcewrite.write(picture)
                fsourcewrite.write('\n')
                if link.get('width') != None and int(link.get('width')) >= 686:
                    print link.get('width')
                    fwrite.write(line)
fread.close()
fwrite.close()
fsourcewrite.close()
print "it is the end!!"

