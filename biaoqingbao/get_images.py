# coding:utf8

import re
import requests
import os

name = input("请输入你想要的图片：")

url = "http://image.baidu.com/search/flip?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1460997499750_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word={}".format(name)

html = requests.get(url).text

image_path = os.path.join(os.path.dirname(__file__),"images/{}".format(name))

pic_url = re.findall('"objURL":"(.*?)",',html,re.S)

if not os.path.exists(image_path):
    os.makedirs(image_path)

i = 0
for each in pic_url:
    file_name = image_path + '/' + str(i) + '.jpg'
    print(each)
    try:
        pic = requests.get(each,timeout=10)
    except:
        print('当前图片无法下载')
        continue
    f = open(file_name,'wb')
    f.write(pic.content)
    f.close()
    i += 1

