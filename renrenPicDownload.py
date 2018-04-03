#!/usr/bin/env python
# coding=utf-8

import requests
import re
import os
import json
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


def mkdirAlbumPath(albumName):
    if not os.path.exists(albumName):
        os.makedirs(albumName)
        print('相册'+albumName+'创建成功')
    path=os.path.join(os.getcwd(),albumName)
    return path


def generateJson(rawContent):
    content = rawContent[rawContent.find('{') : rawContent.find('};')+1]
    newContent = ''
    i= -1
    for k in range(0,len(content)):
        if i == -1:
            if content[k] != "'":
                newContent += content[k]
            else:
                i = k
        else:
            if content[k] == "'":
                if i - 1 >= 0 and content[i-1] == '=':
                    newContent += content[i:k+1]
                else:
                    newContent += '"' + content[i+1:k] + '"'
                i = -1
    return json.loads(newContent)


def albumListGet(s):
    url='http://photo.renren.com/photo/411879201/albumlist/v7?offset=0&limit=40&showAll=1#'
    r=s.get(url).text
    soup = BeautifulSoup(r,'html.parser')
    for item in soup.find_all('script',type='text/javascript'):
        if 'nx.data.photo' in item.getText():
            rawContent = item.getText()
            dictinfo=generateJson(rawContent)
            albumIds=[]
            albumNames=[]
            photoCounts=[]
#            print(dictinfo)
            for photo in dictinfo['albumList']['albumList']:
                temp = {}
                temp['albumId'] = photo['albumId']
                temp['albumName'] = photo['albumName']
                temp['photoCount'] = photo['photoCount']
                albumIds.append(temp['albumId'])
                albumNames.append(temp['albumName'])
                photoCounts.append(temp['photoCount'])
            return albumIds,albumNames,photoCounts


def albumListDownload(s,albumId,albumName,photoCount):
    print('进入'+albumName+',照片数量：'+str(photoCount))
    url='http://photo.renren.com/photo/411879201/album-'+albumId+'/v7'
    r=s.get(url).text
    soup=BeautifulSoup(r,'html.parser')
    for item in soup.find_all('script',type='text/javascript'):
        if 'nx.data.photo' in item.getText():
            rawContent = item.getText()
            dictinfo=generateJson(rawContent)
            i=0
            for photo in dictinfo['photoList']['photoList']:
                temp = {}
                temp['url'] = photo['url']
                print('开始下载')
                path=mkdirAlbumPath(albumName)
                try:
                    picContent=s.get(temp['url']).content
                    fileName=path+'/'+str(i)+'.jpg'
                    with open(fileName,'wb') as wf:
                        wf.write(picContent)
                        wf.close
                        i+=1
                        print('第'+str(i)+'张下载成功')
                except:
                    print('下载失败')



albumIds=[]
albumNames=[]
photoCounts=[]
s=renren_login()
albumIds,albumNames,photoCounts=albumListGet(s)
i=0
for albumId in albumIds:
    albumListDownload(s,albumId,albumNames[i],photoCounts[i])
    i+=1


