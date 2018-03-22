# -*- coding:utf-8 -*-
import os
import requests
from lxml import etree
from Queue import Queue
import datetime
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def PagePool(word, sfile):
    '''
    :param word: 关键词
    :param sfile: 保存抓取结果的文件
    :return: 无
    '''
    if os.path.exists(sfile):
        print "file already exists"
        #return
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'en-us;q=0.5,en;q=0.3',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
    }
    url = 'http://news.baidu.com/ns?ct=0&rn=20&ie=utf-8&bs=' + word + '&rsv_bp=1&sr=0&cl=2&f=8&prevct=no&tn=newstitle&word=' + word

    page_pool = set(url)    #url池，用来记录已经被爬取过的url
    page_queue = Queue()    #url队列，保存等待被爬取的url
    page_queue.put(url)

    while not page_queue.empty():
        url = page_queue.get()
        html = requests.get(url=url, headers=headers)
        #先获取当前页面的带爬取url
        urls = etree.HTML(html.content).xpath('//p[@id="page"]//a')
        for u in urls:
            _url = 'http://news.baidu.com' + u.get('href')
            if _url not in page_pool:
                page_pool.add(_url)
                page_queue.put(_url)
        #爬取当前页
        GetFromPage(html, sfile)

def GetFromPage(html, sfile):
    '''
    :param html:页面响应
    :param sfile: 保存抓取结果的文件
    :return: 无
    '''
    html_content = html.content
    html_content = html_content.replace('<em>', '')     #删除em元素，防止提取题目被干扰
    html_content = html_content.replace('</em>', '')

    dom_tree = etree.HTML(html_content)
    ems = dom_tree.xpath('//h3[@class="c-title"]//a')
    author = dom_tree.xpath('//div[@class="c-title-author"]')

    for e,t in zip(ems, author):
        title = e.text
        _str = t.text
        #需要处理特殊情况，因为有时候百度不返回新闻发布时间，而是显示n小时前，或者n分钟前，或者n秒前
        #处理办法是用当前时间减去时间差，计算得到文章发布时间
        if '小时' in t.text:
            hours = int(filter(str.isdigit, _str.encode('utf-8')))
            _author, _ = _str.strip().split()
            _date = datetime.datetime.now()-datetime.timedelta(hours=hours)
            _date = _date.strftime('%Y年%m月%d日 %H:%M')
        elif '分钟' in t.text:
            minutes = int(filter(str.isdigit, _str.encode('utf-8')))
            _author, _ = _str.strip().split()
            _date = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
            _date = _date.strftime('%Y年%m月%d日 %H:%M')
        elif '秒' in t.text:
            seconds = int(filter(str.isdigit, _str.encode('utf-8')))
            _author, _ = _str.strip().split()
            _date = datetime.datetime.now() - datetime.timedelta(seconds=seconds)
            _date = _date.strftime('%Y年%m月%d日 %H:%M')
        else:
            # print _str.strip().split()[0].encode('utf-8')
            _author, _date, _time = _str.strip().split()
            _date = _date + ' ' + _time

        print title, _author, _date

        #结果存储结构：文章标题///发布商///时间
        #为什么用///分割三个元素，因为用' '、'/'、','等可能和标题内容产生冲突
        with open(sfile, 'a') as f:
            f.write(title+'///'+_author+'///'+_date+'\n')


if __name__ == '__main__':
    keyword = "雄安新区"
    store_file = "2018_1_12.txt"
    PagePool(keyword, store_file)