"""
说明：文件下载地址不能直接是桌面

"""

import requests
import json
import urllib.parse
from lxml import etree
import re
import  os


# baseurl = 'https://image.baidu.com/search/index?tn=baiduimage&fm=result&ie=utf-8&word='
baseurl = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&rn=60&word='
headers = {
        'Accept':'image/webp,image/apng,image/*,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
imglist = []
pattren = '{"thumbURL":"(.*?)","'
# word = input('请输入要搜索图片')
# page = input('图片的页数')
word = '眼药水'
page = '20'

url = baseurl + word +'&pn=' + page

for htmlpage in range(int(page)+1):
    htmlpage += htmlpage*60
    url = baseurl + word + '&pn=' + str(htmlpage)
    print(url)
    html = requests.get(url, headers=headers)
    html = html.json()
    data = html['data']
    for (index,value) in enumerate(data):
        try:
            # print(value)
            # print(type(value))
            # print(value['thumbURL'])
            imglist.append(value['thumbURL'])
            # print('--------------------------------------------')
        except KeyError:
            pass
    print(imglist)
    print(len(imglist))
    for (index,imgurl) in enumerate(imglist):
        try:
            response = requests.get(url=imgurl,headers=headers)
            img = response.content
            # print(img)
            f = open('C:\\Users\\StarDust\\Desktop\\眼药水/{}.jpg'.format(index), 'wb')
            f.write(img)
            f.close()
            # with open('‪C:\\Users\\hanson\\Desktop\\image\\x.jpg','wb') as f:
            #     f.write(img)
        except OSError:
            pass