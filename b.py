import re
import urllib
import urllib.request

from collections import deque
def savedata(data):
    savePath = 'E:\out.txt'
    f = open(savePath, 'a')
    f.write(data+"\n")
    f.close()

queue = deque()
visited = set()

url = 'http://news.dbanotes.net'
queue.append(url)
cnt = 1

while queue:
    print('已经抓取' + str(cnt) + '个界面')
    cnt += 1
    
    url = queue.popleft()
    visited |= {url}
    try:
        html = urllib.request.urlopen(url)
    except:
        print('can not open the url!')
        continue
    
    try:
        if 'html' not in html.getheader('Content-type'):
            print('not html')
    except:
        continue

    try:
        data = html.read().decode('UTF-8')
    except:
        print('can not read the data!')
        continue

    linkre = re.compile(r'href="(.+?)"')
    for x in linkre.findall(data):
        if ('http' in x) and (x not in visited) and (len(queue) < 1000):
            queue.append(x)
    savedata(url)
