# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 09:37:15 2019

@author: 26249
"""

import requests
import pymysql as msql
from urllib.request import quote
from fake_useragent import UserAgent
from lxml import etree

ua=UserAgent()
infos=[]
def spider(url):
    try:
        response=requests.get(url,headers={"User-Agent":ua.random})
    except:
        try:
            if response.status_code !=200:
                response = requests.get(url, headers={"User-Agent": ua.random})
        except:
            pass

    try:
        HTML=etree.HTML(response.text)
        lis=HTML.xpath('//ul[@class="video-contain clearfix"]/li')
        
        for li in lis:
            info={
                    'title':li.xpath('./a/@title')[0],
                    'href':"https:"+li.xpath('./a/@href')[0],
                    'time':li.xpath('.//span/text()')[0].strip()
            }
            infos.append(info)
    except:
        pass

def save_to_mysql(key,infos):
    conn=msql.connect('localhost','root','root','python')    
    cursor = conn.cursor()
    sql_createTb = """CREATE TABLE IF NOT EXISTS  {}(
                     id INT NOT NULL AUTO_INCREMENT,
                     title  VARCHAR(500),
                     href char(80),
                     time CHAR(80),
                     PRIMARY KEY(id))
                     """.format(key)
    cursor.execute(sql_createTb)

    for info in infos:
        title=info['title']
        href=info['href']
        time=info['time']
        sql = '''insert into {}(title,href,time) value(%s,%s,%s)'''.format(key)
        cursor.execute(sql, (title,href,time))
        conn.commit()
    conn.close()
    
def main():
    key=input("请输入搜索内容：")
    pages=int(input("爬取页数："))
    for page in range(1,pages+1):
        print("第"+str(page)+"页")
        url="https://search.bilibili.com/all?keyword="+quote(key)+"&page="+str(page)+""
        spider(url)
    print(infos)
    save_to_mysql(key,infos)

if __name__ == '__main__':
    main()










