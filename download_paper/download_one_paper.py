import requests
import os
from bs4 import BeautifulSoup

# 关键词
TITLE_SHAI= ['privacy', 'private', 'differential', 'local', 'location', 'crowd', 'spatial']

def get_paper(url, folder, filename):
    '''下载单篇论文
        :param url: 要下载的论文url
        :param folder: 保存在本地的路径
        :param filename: 保存在本地的文件名
    '''
    #try:
    if not os.path.exists(folder): # 若文件夹不存在，则创建
        os.mkdir(folder)

    path= folder + '/' + filename
    if not os.path.exists(path): # 若文件不存在，则创建
        r= requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
            f.close()
            print("%s文件保存成功" % (filename))
    else:
        print("%s文件已存在" % (filename))
    #except:
    #    print("%s:爬取失败" % (url))

def getHTMLText(url):
    try:
        r= requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding= r.apparent_encoding
        return r.text
    except:
        return "getHTMLText error!"

def get_paper_name(html):
    '''获取论文标题，根据论文标题关键词筛选
    '''
    soup= BeautifulSoup(html, 'html.parser')
    title=''
    for content in soup.find('h1'):
        title=str(content)
    title= title.replace(':', '-') # 将标题中的冒号改为-

    for shai in TITLE_SHAI: # 根据关键字筛选
        if shai in title.lower():
            return True, title
    return False, title  

def get_pdf_url(html):
    '''获得pdf的链接
    '''
    soup= BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'): #
        # <a class="btn big stretched red" href="/doi/pdf/10.1145/3299869.3319891" title="View or Download as a PDF file"><i aria-hidden="true" class="icon-pdf-file"></i>PDF</a>
        url= link.get('href')
        if (url!=None) and (url[0:9]=='/doi/pdf/'): # SIGMOD
            return 'https://dl.acm.org'+link.get('href')
        if (url!=None) and (url[0:38]=='https://link.springer.com/content/pdf/'): # VLDB
            return url
    return None 


def download_one_paper(url, year, typ, conf):
    '''获得下载url，和论文名字（根据论文名字关键词筛选），下载单篇论文
        :param url: 
        :param year: 出版年份
        :param typ: ccf认证类别
        :param conf: 会议名
    '''
    print(url)
    html= getHTMLText(url)
    #print(html.prettify())
    like, papername= get_paper_name(html)
    if like==False:
        print('没有关键字： %s' % (papername))
        return 
    pdf_url= get_pdf_url(html)
    get_paper(url=pdf_url, folder='./paper', filename=year+'-'+typ+'-'+conf+'-'+papername+'.pdf')
    

if __name__ == "__main__":
    #print(len('https://link.springer.com/content/pdf/'))
    download_one_paper('https://dl.acm.org/doi/10.1145/3299869.3319891', '2019', 'A', 'SIGMOD')
    #download_one_paper('https://link.springer.com/article/10.1007/s00778-019-00568-7', '2020', 'A', 'VLDB')
    
    #download_one_paper('https://ieeexplore.ieee.org/document/9155359', '2020', 'A', 'INFOCOM') # failure