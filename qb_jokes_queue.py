import re
import urllib
import urllib.request
from collections import deque

def saveData(data, savePath):
    f = open(savePath, 'a')
    try:
        f.write(data)
    except:
        pass
    f.close()

cnt = 1
queue = deque()
visited = set()
rule_url = r'href="(.+?)"'
rule_joke = r'<div class="content">(?:.|[\r\n])*?</div>'
savePath = 'E:\qb_jokes.txt'
url_header = 'http://www.qiushibaike.com'
queue.append('/8hr/page/1')

while queue:
    url_tail = queue.popleft()
    url = url_header + url_tail
    visited |= {url_tail}
    request = urllib.request.Request(url, headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)\
             Chrome/50.0.2657.3 Safari/537.36'
    })
    
    try:
        html = urllib.request.urlopen(request)
        data = html.read()
    except:
        print('Parser Html Error!')
        continue

    linkre = re.compile(rule_url)
    try:
        data_decode = linkre.findall(data.decode("UTF-8"))
    except:
        print("Data decode error!\n")
        continue
    
    for x in data_decode:
        if ('/8hr/page/' in x) and (x not in visited) and (len(queue) < 50):
            queue.append(x)


    #jokes = re.compile(r'<h2>(.*?)</h2>')
    jokes = re.compile(rule_joke)
    try:
        joke = jokes.findall(data.decode("UTF-8"))
    except:
        print("Find jokes error!\n")
        continue
    
    for j in joke:
        j_split = j.split("<")[1].split(">")[1]
        print(str(cnt) + j_split + "\n")
        saveData(str(cnt) + j_split + "\n", savePath)
        cnt += 1
    print(len(joke))
    
