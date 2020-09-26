import requests
import os
from bs4 import BeautifulSoup
# 本地导入
from download_one_paper import getHTMLText, download_one_paper

def get_paper_url_list(html):
    '''获取所有论文的下载地址
    '''
    paper_url_list= []

    soup= BeautifulSoup(html, 'html.parser')
    for content in soup.find_all('a'):
        url= content.get('href')
        if (url!=None) and (url[0:16]=='https://doi.org/'):
            paper_url_list.append(url)
    paper_url_list= list(set(paper_url_list)) # 去重
    return paper_url_list

if __name__ == "__main__":
    conf_list=[
        {
            'url':'https://dblp.org/db/journals/vldb/vldb29.html',
            'year':'2020',
            'typ':'A',
            'conf':'VLDB'
        },
        {
            'url':'https://dblp.org/db/journals/vldb/vldb28.html',
            'year':'2019',
            'typ':'A',
            'conf':'VLDB'
        },
        '''
        {
            'url':'https://dblp.org/db/conf/sigmod/sigmod2019.html',
            'year':'2019',
            'typ':'A',
            'conf':'SIGMOD'
        }'''
    ]
    for conf in conf_list:
        conf_url= conf['url'] # 获取会议的网站
        html= getHTMLText(conf_url)
        paper_url_list= get_paper_url_list(html) # 获取所有论文的下载地址

        totnum_list= len(paper_url_list)
        for i in range(len(paper_url_list)):
            print('\ndealing with %d/%d=%f%%' % (i+1, totnum_list, 100.0*(i+1)/totnum_list)) # 用来观察进度
            paper_url= paper_url_list[i] # paper_url= 'https://doi.org/10.1145/3299869.3314037'
            download_one_paper(paper_url, conf['year'], conf['typ'], conf['conf'])