#!/usr/bin/env python
# coding=utf-8

import requests
import re
import os
from bs4 import BeautifulSoup

def renren_login():
    posturl = 'http://renren.com/PLogin.do'
    headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    postdata = {
        'domain':'logindomain',
        'email':'524255527@qq.com',
        'password':'xue12155175'
    }

    s=requests.session()
    r=s.post(posturl,postdata,headers)
    soup=BeautifulSoup(r.text,'html.parser')
    if '人人直播' in soup.title.string:
        print('登录成功')
    return s

def albumId_get(s):
    f = s.get('http://photo.renren.com/photo/411879201/albumlist/v7?offset=0&limit=40&showAll=1#').text
    soup=BeautifulSoup(f,'html.parser')
#    print(soup)
    pattern=re.compile(r'"albumId":"(.*?)",')
    soup=soup.decode('utf-8')
    albumIds=re.findall(pattern,soup)
    print(albumIds)
    return s,albumIds

def albumName_get(s):
    f = s.get('http://photo.renren.com/photo/411879201/albumlist/v7?offset=0&limit=40&showAll=1#').text
    soup=BeautifulSoup(f,'lxml')
#    print(soup)
    pattern=re.compile(r'"albumName":"(.*?)",')
    soup=soup.decode('utf-8')
    albumNames=re.findall(pattern,soup)
    print(albumNames)
    return s,albumNames

def mkdir_album_path(s,albumId):
    if not os.path.exists(albumId):
        os.makedirs(albumId)
        print('相册'+albumId+'创建成功')
    path=os.path.join(os.getcwd(),albumId)
    return path

def pic_download(s,albumId,path):
    url='http://photo.renren.com/photo/411879201/album-'+albumId+'/v7'
    r=s.get(url).text
    soup=BeautifulSoup(r,'lxml')
    soup=soup.decode('utf-8')
    pattern=re.compile(r'"url":"(.*?).jpg"},')
    pic_list=re.findall(pattern,soup)
    i = 0
    try:
        for pic_url in pic_list:
            pic_content=requests.get(pic_url).content
            file_name=path+'/'+str(i)+'.jpg'
            with open(file_name,'wb') as wf:
                wf.write(pic_content)
                wf.close()
                print('第'+ str(i) +'张下载完成')
            i += 1
    except:
        print('下载错误')
        return


#def getPhotoList():
#		url='http://photo.renren.com/photo/411879201/albumlist/v7?offset=0&limit=40&showAll=1#'
#        soup = BeautifulSoup(url)
#        for item in soup.find_all('script',type='text/javascript'):
#            if 'nx.data.photo' in item.getText():
#                rawContent = item.getText()
#                dictinfo = Common.generateJson(rawContent)
#                for photo in dictinfo['photoList']['photoList']:
#                    temp = {}
#                    temp['albumId'] = photo['albumId']
#                    temp['photoId'] = photo['photoId']
#                    temp['ownerId'] = photo['ownerId']
#                    self.photoList.append(temp)


s=renren_login()
#getPhotoList()
s,albumIds=albumId_get(s)
s,albumNames=albumName_get(s)
i=0
for albumName in albumNames:
    print(albumName)
    path=mkdir_album_path(s,albumName)
    pic_download(s,albumIds[i],path)
    i+=1


