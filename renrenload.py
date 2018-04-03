#!/usr/bin/env python
# coding=utf-8

import requests
import re
from bs4 import BeautifulSoup

posturl = 'http://renren.com/PLogin.do'
headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
postdata = {
    'domain':'logindomain',
    'email':'524255527@qq.com',
    'password':'******'
}

s=requests.session()
r=s.post(posturl,postdata,headers)
f = s.get('http://photo.renren.com/photo/411879201/albumlist/v7?offset=0&limit=40#').text
soup=BeautifulSoup(f,'html.parser')
print(soup)

