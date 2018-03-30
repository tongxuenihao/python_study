import requests
from bs4 import BeautifulSoup
import os
f = requests.get('http://tieba.baidu.com/p/3181528205').text
#用BS解析html
s = BeautifulSoup(f,'lxml')
s_imgs = s.find_all('img', pic_type = "0")

i=0
if not os.path.exists('北理校花'):
    os.makedirs('北理校花')
path = os.path.join(os.getcwd(),"北理校花")
for s_img in s_imgs:
    img_url = s_img['src']
    img_content = requests.get(img_url).content
    file_name = str(i) + '.jpg'
    os.chdir(path)
    with open(file_name, 'wb') as wf:
        wf.write(img_content)
    i += 1

