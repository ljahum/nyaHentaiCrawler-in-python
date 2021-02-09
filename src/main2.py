from bs4 import BeautifulSoup
# from icecream import *
import requests
import time
import re
import os
import configparser
# from test import html
import time

headers = {
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br",
    "referer": "https://zha.doghentai.com/",
    "sec-fetch-dest": "image",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
}
def getMangaInfo(url):
    print(url)
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'lxml')  # 解析html变成beautifulsoup对象
    tag = soup.find("img", attrs={'class': 'lazyload'})  # 查找img标签
    attr = tag.attrs
    name = attr['alt']
    name = name.replace("\?", '')                         # 获取本子名字
    name = name.replace(":", '')
    name = name.replace(" ", '')
    name = name.replace("\*", '')
    name = name.replace("/", '')
    
    ID_Downloader =  (re.findall('\d+', attr['data-src'], re.ASCII)[1])   # 获取漫画下载页面id
    suffix =  attr['data-src'].split('.')[-1]                       # 获取后缀
                                                                    # 正则表达式获取本子页数
    picnum = soup.find(text=re.compile("共 \w+ 頁"))
    picnum = re.findall('\w+', picnum, re.ASCII)[0]
    print('name:',name )
    print('页数', picnum)
    # print('suffix')
    # print('ID_Downloader')
    return name, picnum, suffix, ID_Downloader

def getPic(picNum, outPutroot, suffix,id):
    for i in range(1,int(picNum)+1):
        url = 'https://i0.nyacdn.com/galleries/'+id+'/'+str(i)+'.'+suffix
        file = outPutroot+str(i) + '.'+suffix
        print("Downloading "+url)
        # print(os.path.exists(file))
        if os.path.exists(file) == False:
            try:
                time.sleep(3)
                r = requests.get(url, headers=headers, timeout=5)
                r.raise_for_status()
                with open(file, "wb") as f:  # 开始写文件，wb代表写二进制文件
                    f.write(r.content)
            except Exception as e:
                print(e,'\n出错了 手动下吧（')
            print('done')
        else:
            print('done')
        
        # input()




def main(ulist, root):
    output_directory = 'C://Users//16953//Desktop//爬虫//output//'
    output_directory = root + '//output//'
    # input()
    for url in ulist:
        name, picnum, suffix, ID = getMangaInfo(url)

        output_path = output_directory + name+'//'
        output_path.replace('\\','//')

        # print('输出位置:',output_path)
        if os.path.exists(output_path) == False:
            os.mkdir(output_path)
        getPic(picnum, output_path, suffix, ID)


def initCfg(root_dir):
    cf = configparser.ConfigParser()
    cf.read(root_dir+"/config.ini")
    num = int(cf.get('data', 'number'))
    print('爬取数量:',num)
    ans =[]
    print("爬取链接:")
    for i in range(num):
        url = cf.get('manga url', 'url'+str(i))
        ans.append(url)
        print(url)
    return ans,num

if __name__ == '__main__':
    root = os.getcwd()
    root = (root.replace('\\', '//'))
    ulist,num = initCfg(root)
    input('按任意键继续..')
    main(ulist, root)
    print("变态喵绅士漫画爬取完毕！！！o((>ω<))o")
    input('按任意键退出..')
    
