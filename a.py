import re
import urllib
import urllib.request
from collections import deque

def saveData(data):
    savePath = 'E:\qb.txt'
    f = open(savePath, 'a')
    f.write(data + "\n")
    f.close()

queue = deque()
visited = set()

queue.append('http://www.qiushibaike.com')
cnt = 1

while queue:
    url = queue.popleft()
    visited |= {url}
    request = urllib.request.Request(url, headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2657.3 Safari/537.36'
    })
    
    try:
        html = urllib.request.urlopen(request)
        data = html.read()
        saveData(url)
    except:
        print('Parser Html Error!')
        continue

    linkre = re.compile(r'href="(.+?)"')

    try:
        data_decode = linkre.findall(data.decode())
    except:
        continue
    
    for x in data_decode:
        if ('http' in x) and (x not in visited) and (len(queue) < 500):
            queue.append(x)

    print('Spider ' + str(cnt) + ' Page Already!')
    cnt += 1
