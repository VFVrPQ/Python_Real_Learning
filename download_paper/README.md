# download_paper

下载论文的python脚本，打算按关键字寻找某个会议的论文，然后批量下载。
目前可以通过`https://dblp.org`网站，按关键字批量下载VLDB和SIGMOD的论文。


## 环境

python3，需要下载bs4,requests两个模块。

## 思路

- 通过`https://dblp.org`网站，找到特定年份特定会议的论文下载地址；
- 再从对应的下载地址中找到论文名字和pdf的下载链接下载相应论文。

## 文件和使用

包括两个文件`download_one_paper.py`和`download_papers.py`，第一个文件用来下载一篇论文，第二个文件获得所有论文链接后调用第一个文件下载论文。
更详细的思路：[https://blog.csdn.net/MustImproved/article/details/108816382](https://blog.csdn.net/MustImproved/article/details/108816382)

用的时候直接:
```bash
$ python download_papers.py
```

## others

- SIGMOD2019 `https://dblp.org/db/conf/sigmod/sigmod2019.html`
- VLDB2020 `https://dblp.org/db/journals/vldb/vldb29.html`
- NDSS2020 `https://www.ndss-symposium.org/ndss-paper/adversarial-classification-under-differential-privacy/`
- NIPS2019 `http://papers.nips.cc/book/advances-in-neural-information-processing-systems-32-2019`
- INFOCOM2020 `https://dblp.org/db/conf/infocom/infocom2020.html#00010DWZY20` 跳转不过去